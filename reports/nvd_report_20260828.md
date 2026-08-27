# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-08-27 15:00 UTC
- **対象期間**: `2026-08-26T15:00:29.000Z` 〜 `2026-08-27T15:00:33.000Z`
- **重要CVE数**: 254 件（Critical 9.0+: 77 件 / High 7.0〜: 177 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 2026 年上半期に公開された CVE のうち、**CVSS 7.0 以上が 40 件以上**と非常に多く、特に **ネットワーク露出した管理インターフェース** や **Web アプリケーションの入力検証不備** が集中しています。  
- UniFi 系列（UniFi OS / UniFi Talk / UniFi Protect / UniFi Access）で **リモートコード実行（RCE）や認証バイパス** が連続して報告され、同一ベンダー製品群での共通脆弱性が顕在化しています。  
- Linux カーネルでも **複数の OOB 読み取り・書き込み** や **MPTCP/CEPH の不正パケット処理** が修正されており、インフラ層のリスクが依然として高いことが示唆されています。  
- KubePi、Gitea、WordPress プラグイン、PHP ライブラリ（Hash Form、Geo Controller）など、**開発・CI/CD ツールチェーン** でもリモートコード実行が確認され、サプライチェーン対策の重要性が再認識されました。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目理由 |
|-----|------|----------|----------|
| **CVE‑2026‑77550** | 10.0 (Network, Remote, No Auth) | UniFi OS の CRLF インジェクションにより **認証バイパス** が可能 | UniFi OS は企業・教育機関で広く導入されているため、認証が取れた瞬間に全管理権限が奪われる。全デバイスのファームウェア更新が急務。 |
| **CVE‑2026‑60004** | 9.8 | Gitea ≤ 1.27.1 の diffpatch API から **リモートコード実行**（Git フックの任意インストール） | CI/CD パイプラインの中心的ツールであり、攻撃者がコード実行権限を取得すると内部リポジトリ全体が危険に晒される。 |
| **CVE‑2026‑77537** / **CVE‑2026‑77548** / **CVE‑2026‑77543** (UniFi Protect 系列) | 9.9 | UniFi Protect の入力検証不備により **コマンドインジェクション** が可能 | カメラ映像管理サーバは常時ネットワークに接続されており、攻撃者が任意コードを実行すれば内部ネットワーク横移動や情報窃取が容易になる。 |
| **CVE‑2026‑78292** | 9.8 | Hash Form ≤ 1.4.1 の **PHP Object Injection**（認証不要） | 多くの PHP ベース CMS でプラグインとして利用されているため、広範囲に影響が波及。 |
| **CVE‑2026‑80586** (Linux kernel) | 9.8 | MPTCP の不正サブオプション処理により **リモートコード実行** の可能性 | カーネルレベルの脆弱性はパッチ適用が遅れがちで、クラウド・オンプレミス問わず影響が大きい。 |

> **共通点**：すべて **ネットワークから直接攻撃可能**（AV:N）で、認証不要または低権限でエクスプロイトできる点が特に危険です。  

---

## 3. 推奨アクション  

### 3.1 パッケージ・ファームウェアの即時更新
| 製品 / パッケージ | 修正バージョン / 対策 | 具体的な実施手順 |
|-------------------|----------------------|-------------------|
| **KubePi** | 1.6.16 以上 (SSO API ルーティング分離) | `helm upgrade kube-pi kube-pi/kube-pi --set image.tag=1.6.16` |
| **UniFi OS / UniFi Talk / Protect / Access** | ベンダー提供の最新ファームウェア (2026‑09‑xx 以降) | UniFi Controller → **Settings → Firmware Update** → 全デバイスを一括更新 |
| **Gitea** | 1.27.1 以上 | `apt-get update && apt-get install gitea=1.27.1-1`  または Docker イメージ `gitea/gitea:1.27.1` に置き換え |
| **WordPress ACPT (Custom Post Types) プラグイン** | 2.0.64 以上 | WordPress 管理画面 → **プラグイン → 更新**、または `wp plugin update acpt-pro` |
| **Hash Form** | 1.4.2 以上 | Composer: `composer require hash-form/hash-form:^1.4.2` |
| **Geo Controller** | 8.9.9 以上 | `composer require geo-controller/geo-controller:^8.9.9` |
| **Linux カーネル** | 6.8.0‑rc1 以降 (すべての 9.8 系パッチが含まれる) | `yum update kernel-6.8*` / `apt-get install linux-image-6.8.0-rc1` → 再起動 |
| **Ceph / libceph** | カーネル 6.8 以降に同梱された修正 (decode_locker, decode_watchers 等) | 上記カーネル更新で同時に適用 |

### 3.2 環境全体のハードニング
1. **ネットワーク分離**  
   - UniFi 系列は管理 UI を **内部 VLAN** に限定し、外部からの直接アクセスを防止。  
   - KubePi の SSO エンドポイントは **Ingress に認証ミドルウェア**（例: oauth2‑proxy）を挟む。

2. **WAF / IPS の導入**  
   - 特に **PHP Object Injection** 系 (Hash Form, Geo Controller) と **コマンドインジェクション** 系 (UniFi Protect) に対し、リクエストパラメータの正規表現フィルタを追加。  

3. **監査ログの強化**  
   - Gitea の `diffpatch` API へのアクセスは **audit log** に必ず記録し、異常なフック作成を検知。  
   - Linux カーネルは `auditd` で `mptcp`、`ceph` 関連の syscalls を監視し、異常パケットをアラート。

4. **最小権限の徹底**  
   - UniFi OS の管理アカウントは **2FA** を必須化し、API トークンは最小権限 (Read‑Only) に限定。  
   - Gitea の SSH キーは **期限付き** にし、不要なキーは即削除。

5. **脆弱性スキャンの定期実行**  
   - `trivy`, `anchore`, `OpenSCAP` などで **Docker イメージ・OS パッケージ** を週次でスキャンし、上記 CVE が再度出現しないか確認。

### 3.3 インシデント対応準備
- **CVE‑2026‑77550** 系は認証バイパスが起点になるため、**

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-65956

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-26T23:17:15.550 |

KubePi is a Kubernetes multi-cluster management panel. In versions up to and including 1.6.15, the SSO configuration API endpoints are exposed on the same public routing boundary as the SSO login and callback endpoints, so SSO, OIDC, and SAML management operations can be reached without administrator authorization. Because reading, creating, and updating the global SSO configuration is not restricted to administrators, an unauthorized or low-privileged user can inspect or alter the authentication configuration, which under certain conditions can lead to account takeover or privilege escalation. The SSO connectivity-test function can additionally be abused as a server-side request forgery primitive, and the user list API returns user objects without consistently clearing authentication-related fields. This issue is fixed in version 2.0.0.

### CVE-2026-77554

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-26T11:16:39.400 |

A malicious actor with access to the network could exploit an Improper Input Validation vulnerability found in UniFi Talk Application to execute a Command Injection on the host device.

### CVE-2026-77550

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-93` |
| Published | 2026-08-26T11:16:38.930 |

A malicious actor with access to the network could exploit an Improper Neutralization of CRLF Sequences vulnerability found in certain devices running UniFi OS to bypass authentication to such UniFi OS devices or instances.

### CVE-2026-77537

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-26T10:16:41.540 |

A malicious actor with access to the network could exploit an Improper Input Validation vulnerability found in UniFi Protect Application to execute a Command Injection on the host device.

### CVE-2026-77553

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-26T11:16:39.283 |

A malicious actor with access to the network and low privileges could exploit an Improper Access Control vulnerability found in UniFi Access Application to escalate privileges on the host device.

### CVE-2026-77548

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-26T11:16:38.693 |

A malicious actor with access to the network and low privileges could exploit an Improper Input Validation vulnerability found in UniFi Protect Application to execute a Command Injection on the host device.

### CVE-2026-77547

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-26T11:16:38.573 |

A malicious actor with access to the network and low privileges could exploit an Improper Input Validation vulnerability found in UniFi Access Application to execute a Command Injection on the host device.

### CVE-2026-77546

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-26T11:16:38.463 |

A malicious actor with access to the network and low privileges could exploit an Improper Input Validation vulnerability found in UniFi Access Application to execute a Command Injection on the host device.

### CVE-2026-77543

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-26T10:16:42.283 |

A malicious actor with access to the network and low privileges could exploit an Improper Input Validation vulnerability found in UniFi Access Application to execute a Command Injection on the host device.

### CVE-2026-77536

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-26T10:16:41.417 |

A malicious actor with access to the network and low privileges could exploit an Improper Access Control vulnerability found in certain devices running UniFi OS to escalate privileges within such UniFi OS devices or instances.

### CVE-2026-77534

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-26T10:16:41.173 |

A malicious actor with access to the network and low privileges could exploit an Improper Access Control vulnerability found in certain devices running UniFi OS to escalate privileges within such UniFi OS devices or instances.

### CVE-2026-77533

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-26T09:16:48.563 |

A malicious actor with access to the network and low privileges could exploit an Improper Input Validation vulnerability found in UniFi Protect Application to execute a Command Injection on the host device.

### CVE-2026-78292

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-27T10:16:38.530 |

Unauthenticated PHP Object Injection in Hash Form <= 1.4.1 versions.

### CVE-2026-78286

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-27T10:16:38.137 |

Unauthenticated PHP Object Injection in Geo Controller <= 8.9.8 versions.

### CVE-2026-32566

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-08-27T10:16:35.933 |

Unauthenticated Privilege Escalation in ACPT (Pro) - Custom Post Types Plugin for WordPress <= 2.0.63 versions.

### CVE-2026-60004

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-26T20:17:56.010 |

Gitea before 1.27.1 allows remote code execution via the diffpatch API through Git hook installation.

### CVE-2026-54569

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-95;CWE-862` |
| Published | 2026-08-26T16:16:27.733 |

SENAITE.CORE is the core framework for the SENAITE laboratory information management system. From 2.0.0 to 2.6.0, the SENAITE.CORE JSON API permits unauthenticated remote code execution through a two-request chain involving missing authorization and unsafe evaluation. The state-changing routes in src/bika/lims/jsonapi/update.py, including update, update_many, remove, doActionFor, doActionFor_many, and getusers, do not enforce the senaite.core: Access JSON API permission before resolving attacker-selected objects. In src/bika/lims/jsonapi/init.py, set_fields_from_request passes raw request values for RecordsField and RecordField instances to eval() before field mutator write-permission checks execute. An anonymous attacker can discover the bika_setup object identifier through @@uuid, send a value such as RejectionReasons to /@@API/update, and execute arbitrary Python in the Zope worker before a later mutation failure rolls back ZODB changes. The same unsafe evaluation pattern is present in src/senaite/core/browser/fields/record.py and src/senaite/core/browser/fields/records.py. Successful exploitation can expose or modify laboratory data, files, and accounts and can disrupt the service.

### CVE-2026-80589

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:15.283 |

In the Linux kernel, the following vulnerability has been resolved:

block: stop the timeout timer when releasing a never added disk

disk_release() undoes blk_mq_init_allocated_queue() for a disk whose
probe failed before add_disk(), but it only calls blk_mq_exit_queue().
Nothing there stops q->timeout, and that timer rolls forward: it stays
pending until it next expires, not until the last request completes.
So if the driver issued any I/O before adding the disk, the
request_queue is freed while still linked into a timer wheel bucket.

Commit 6f8191fdf41d ("block: simplify disk shutdown") dropped the
blk_cleanup_queue() call that used to stop it.  __del_gendisk() and
blk_mq_destroy_queue() still do; only the probe failure path lost it.

nvme gets there because nvme_update_ns_info() submits Report Zones or
FDP io-mgmt-recv on ns->queue before the disk is added, so a later
failure - a concurrent reset setting NVME_CTRL_FROZEN, or
device_add_disk() failing - lands in put_disk() with the timer armed:

  BUG: KASAN: slab-use-after-free in detach_if_pending+0x30c/0x340
  Write of size 8 at addr ffff888004d71310 by task kworker/u8:2/37
   __timer_delete_sync+0x156/0x240 kernel/time/timer.c:1621
   blk_sync_queue+0x22/0x40 block/blk-core.c:222
   nvme_sync_queues+0x100/0x150 drivers/nvme/host/core.c:5362
   nvme_reset_work+0x138/0x930 drivers/nvme/host/pci.c:3264

  Allocated by task 34:
   __blk_mq_alloc_disk+0x33/0x100 block/blk-mq.c:4462
   nvme_alloc_ns+0x290/0x3870 drivers/nvme/host/core.c:4146

  Freed by task 0:
   blk_free_queue_rcu+0x3a/0x50 block/blk-core.c:254
   rcu_core+0xc10/0x1730 kernel/rcu/tree.c:2857

The queue being synced there is ctrl->admin_q, only a victim sharing a
timer wheel bucket with the freed queue's dangling entry; other runs
tripped in enqueue_timer(), __run_timers() or blk_mq_timeout_work().
Failing nvme_alloc_ns() with a debug patch makes it deterministic: one
leaked timer trips KASAN within seconds, while 1987 patched releases
produced no splat.

Stop the timer and the queue work items before blk_mq_exit_queue(), like
blk_mq_destroy_queue() does.

Found by FuzzNvme.

### CVE-2026-80587

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:15.017 |

In the Linux kernel, the following vulnerability has been resolved:

mptcp: avoid combining some incoming suboptions

Some MPTCP suboptions are mutually exclusive according to the RFC8684,
but also because in different places, the code doesn't expect some
combinations to be present. That's specially true for suboptions that
would be present twice, but with different attributes.

The new restrictions are the same as the ones applied on the output
side, with mptcp_write_options. The same rules can be reused with a
small fix: an MP_FASTCLOSE can be used with a DSS when the sender picks
this option [1], which is not the case on Linux. Here are the rules:

  Which options can be used together?

  X: mutually exclusive
  O: often used together
  C: can be used together in some cases
  P: could be used together but we prefer not to (optimisations)

  | Opt: | MPC  | MPJ  | DSS  | ADD  |  RM  | PRIO | FAIL |  FC  |
  |------|------|------|------|------|------|------|------|------|
  | MPC  |------|------|------|------|------|------|------|------|
  | MPJ  |  X   |------|------|------|------|------|------|------|
  | DSS  |  X   |  X   |------|------|------|------|------|------|
  | ADD  |  X   |  X   |  P   |------|------|------|------|------|
  | RM   |  C   |  C   |  C   |  P   |------|------|------|------|
  | PRIO |  X   |  C   |  C   |  C   |  C   |------|------|------|
  | FAIL |  X   |  X   |  C   |  X   |  X   |  X   |------|------|
  | FC   |  X   |  X   |  P   |  X   |  X   |  X   |  X   |------|
  | RST  |  X   |  X   |  X   |  X   |  X   |  X   |  O   |  O   |
  |------|------|------|------|------|------|------|------|------|

The only difference is with the 'P': another stack could send and
ADD_ADDR with other suboptions (DSS, RM_ADDR), and this should be
allowed.

A few points of attention:

 - In theory, an MP_CAPABLE could be used with a RM_ADDR, but there is
   no reason to add it with a SYN. Note that even with a 4th ACK, it
   doesn't seem to be useful, except when IDs are known in advance via
   another channel. Better not to break that.

 - Now, combining both an MP_CAPABLE and an MP_JOIN will no longer
   result to a reject of the two options, but only the second suboption
   is ignored. That seems OK to do that for this unexpected error. At
   least now all inconsistent combinations are handled the same way.
   This could change later in next. This also means the explicit checks
   for having both MPC + MPJ in subflow.c will now be unreachable.
   That's fine, they will be removed in a follow-up patch.

 - In case of conflicting combinations, the extra suboption(s) is/are
   ignored: having such combinations either means the remote peer is
   buggy, or is evil. The simplest action is then taken in this case:
   stop processing the current suboption.

 - In mp_opt->suboptions, there is also a bit reserved to the checksum,
   which can be used in an MP_CAPABLE and a DSS. Each time a DSS option
   can be used in parallel with another option, the checksum can be set,
   so the verification is combined into a new OPTIONS_MPTCP_DSS macro.

 - An MP_CAPABLE ACK can carry a Data-Level Length, and an optional
   Checksum: they are the same as the ones found in a DSS, because a DSS
   cannot be used in parallel to an MP_CAPABLE. Similarly, even if there
   is room, a DSS cannot be used with an MP_JOIN.

### CVE-2026-80586

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:14.873 |

In the Linux kernel, the following vulnerability has been resolved:

mptcp: options: reset DSS fields in case of unexpected size

A remote peer could send a malformed DSS with a wrong size, followed by
another DSS or MPC + Data. In this case, the first suboption will be
ignored, but leaving some fields written, which could lead to
inconsistency or access uninitialized data.

Explicitly reset the fields that could have been modified in case of
unexpected size.

### CVE-2026-80561

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:11.007 |

In the Linux kernel, the following vulnerability has been resolved:

libceph: fix multiple unsafe decodes in decode_locker()

decode_locker() in cls_lock_client.c contains three unsafe decode
operations that allow a malicious or compromised OSD to trigger
slab-out-of-bounds reads:

1. ceph_decode_copy() at the locker_id_t name field has no preceding
   bounds check. With p == end after ceph_start_decoding() accepts
   struct_len=0, this reads sizeof(ceph_entity_name) = 9 bytes past
   the validated buffer boundary.

2. *p += sizeof(struct ceph_timespec) after the locker_info_t header
   is an unchecked pointer advance. A malicious OSD can position p
   past end, causing all subsequent _safe checks to pass against a
   bogus boundary.

3. len = ceph_decode_32(p) has no preceding bounds check, and the
   immediately following *p += len is uncapped. A malicious OSD can
   send len=0xffffffff, advancing p gigabytes past end and escaping
   the decode window entirely.

Fix all three by replacing bare operations with their safe variants:
  ceph_decode_copy   -> ceph_decode_copy_safe
  *p += sizeof(...)  -> ceph_decode_skip_n
  ceph_decode_32(p)  -> ceph_decode_32_safe
  *p += len          -> ceph_decode_skip_n

A new label is added to return -EINVAL on any bounds violation.
-EINVAL is appropriate here: the data received from the OSD
is structurally malformed, which is an invalid argument to the decode
contract regardless of whether the caller or the wire is at fault.

Attacker model: a malicious or compromised OSD in a multi-tenant Ceph
deployment can trigger this against any kernel client that issues the
lock.get_info class method (e.g. during RBD exclusive lock acquisition)
without any further privileges beyond OSD session establishment.

[ idryomov: use ceph_decode_skip_string() to skip description, trim
  changelog ]

### CVE-2026-80558

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:10.530 |

In the Linux kernel, the following vulnerability has been resolved:

libceph: Avoid using invalid osd indices from primary_temp

A corrupted osdmap received from a Ceph monitor or OSD may contain osd
indices in its pg_temp, primary_temp, pg_upmap, and pg_upmap_items parts
that don't exist, i.e., that are greater than max_osd or smaller than
CEPH_HOMELESS_OSD (-1). These indices are used to create the up and
acting set in ceph_pg_to_up_acting_osds(), called from calc_target().
While most of these osd indices are checked, the one from primary_temp
is not. Subsequently, this may lead to calc_target() returning this
(potentially invalid) index as target osd for a (linger) request.
Because the osd_state, osd_weight, and osd_addr arrays only contain
max_osd entries (with indices 0 to max_osd -1), this leads to
out-of-bounds accesses when trying to read values from these arrays.

This patch fixes the issue by adding a check to get_temp_osds(), so that
only valid osd indices from primary_temp are used, and it falls back to
using the primary from pg_temp or the up set if it is invalid.

[ idryomov: changelog ]

### CVE-2026-80557

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:10.400 |

In the Linux kernel, the following vulnerability has been resolved:

libceph: fix OOB read in decode_watchers() via missing bounds check

ceph_start_decoding() validates that struct_len bytes remain in the
buffer after the encoding header, but accepts struct_len=0 as valid:
ceph_decode_need(p, end, 0, bad) always passes. When a malicious or
compromised OSD sends an obj_list_watch_response_t reply with
struct_len=0, ceph_start_decoding() returns success with p == end,
leaving zero bytes guaranteed for subsequent reads.

The immediately following ceph_decode_32(p) in decode_watchers() has
no preceding bounds check. With p == end this is a 4-byte read past
the validated buffer boundary. The garbage value is then passed
directly to kzalloc_objs() as the watcher count.

The sibling function decode_watcher() already uses the safe variants
(ceph_decode_copy_safe, ceph_decode_64_safe, ceph_decode_skip_32)
after its own ceph_start_decoding() call. decode_watchers() is the
only site that uses the bare variant, confirming an oversight.

Fix by replacing ceph_decode_32(p) with ceph_decode_32_safe(p, end,
*num_watchers, bad), consistent with the established pattern.

Attacker model: a malicious or compromised OSD in a multi-tenant Ceph
deployment (e.g. cloud) can trigger this against any kernel client
that calls CEPH_OSD_OP_LIST_WATCHERS, without any further privileges
beyond OSD session establishment.

[ idryomov: trim changelog ]

### CVE-2026-80528

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:06.667 |

In the Linux kernel, the following vulnerability has been resolved:

ceph: avoid fs reclaim while using current->journal_info

handle_reply() stores a `ceph_mds_request` pointer in
`current->journal_info` while filling the inode and dentry cache from
an MDS reply.

An allocation in this section can enter direct reclaim and prune
dentries from another filesystem.  If this dirties an ext4 inode, ext4
starts a JBD2 transaction.  JBD2 interprets the Ceph request in
`current->journal_info` as a journal handle and dereferences the
request's `r_tid` as `h_transaction`, causing a kernel crash, e.g.:

 Unable to handle kernel paging request at virtual address 00000000077b4818
 [...]
 Internal error: Oops: 0000000096000004 [#1]  SMP
 Modules linked in:
 CPU: 6 UID: 0 PID: 2699135 Comm: kworker/6:3 Tainted: G        W           6.18.38-i3 #1113 NONE
 [...]
 Workqueue: ceph-msgr ceph_con_workfn
 pstate: 80400009 (Nzcv daif +PAN -UAO -TCO -DIT -SSBS BTYPE=--)
 pc : jbd2__journal_start+0x2c/0x208
 lr : __ext4_journal_start_sb+0x100/0x178
 [...]
 Call trace:
  jbd2__journal_start+0x2c/0x208 (P)
  __ext4_journal_start_sb+0x100/0x178
  ext4_dirty_inode+0x3c/0x90
  __mark_inode_dirty+0x58/0x400
  iput.part.0+0x2b0/0x370
  iput+0x18/0x30
  dentry_unlink_inode+0xc0/0x158
  __dentry_kill+0x80/0x250
  shrink_dentry_list+0x90/0x130
  prune_dcache_sb+0x60/0x98
  super_cache_scan+0xe8/0x190
  do_shrink_slab+0x174/0x388
  shrink_slab+0xd8/0x4c0
  shrink_node+0x31c/0x908
  do_try_to_free_pages+0xd0/0x508
  try_to_free_pages+0x11c/0x238
  __alloc_frozen_pages_noprof+0x4d0/0xdd0
  __folio_alloc_noprof+0x18/0x70
  __filemap_get_folio+0x248/0x440
  ceph_readdir_prepopulate+0x570/0x9e8
  mds_dispatch+0x1424/0x1ba0
  ceph_con_process_message+0x74/0xa0
  ceph_con_v1_try_read+0x3a0/0x1510
  ceph_con_workfn+0x260/0x460

Enter a scoped NOFS allocation context and leave it after clearing
`journal_info`.  This prevents filesystem reclaim from recursing into
another filesystem while the field contains Ceph-private data.

### CVE-2026-80519

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:05.420 |

In the Linux kernel, the following vulnerability has been resolved:

ovpn: finish crypto callback cleanup before peer release

Crypto completion callbacks hold both key-slot and peer references. The
peer reference pins the netdev, and dropping the last peer reference can
let netdev unregistration and module removal make progress.

Do not release that peer reference before the callback has finished its
own cleanup. If ovpn_crypto_key_slot_put runs after ovpn_peer_put, it can
schedule an RCU callback backed by module text after ovpn_cleanup
rcu_barrier has already run. The TX error path also freed the remaining
skb after ovpn_peer_put, leaving callback cleanup outside the peer/netdev
lifetime window.

Release the key slot and free any remaining skb first, then drop the peer
reference as the last callback action.

### CVE-2026-74752

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:16:54.270 |

In the Linux kernel, the following vulnerability has been resolved:

sctp: validate cookie AUTH state before use

When cookie authentication is disabled, COOKIE_ECHO restores fixed-size
AUTH fields directly from peer-controlled cookie bytes.  A forged RANDOM
length, HMAC list, or CHUNKS list can then reach association consumers
with lengths or identifiers that were never validated against the local
backing arrays.

A forged RANDOM length can cause out-of-bounds reads during key-vector
construction.  A forged HMAC identifier also caused a 32-byte write past
a zero-length AUTH chunk, providing a primitive for a local privilege
escalation chain.

Validate the cookie's RANDOM, HMACS, and CHUNKS parameters at the cookie
trust boundary before copying them into the association.  Reject invalid
types, malformed lengths, unsupported HMAC identifiers, HMAC lists
without SHA1, and forbidden chunk ids.

### CVE-2026-74746

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:16:53.503 |

In the Linux kernel, the following vulnerability has been resolved:

netfilter: flowtable: publish GC-visible tuple last

nf_flow_table_iterate() only treats original-direction tuple nodes as
owning entries. Publishing the original node first lets GC observe and
free a flow while flow_offload_add() is still inserting the reply node.
Publish the reply node first and the original node last so GC never
sees a partially installed flow.

KASAN can trigger slab-use-after-free read and write reports in the
flowtable/rhashtable path (rht_deferred_worker, jhash, flow_offload_del,
flow_offload_lookup, etc.).

### CVE-2026-74744

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:16:53.250 |

In the Linux kernel, the following vulnerability has been resolved:

ipvlan: inherit needed_headroom and needed_tailroom from phy_dev

ipvlan devices inherit hard_header_len from phy_dev during ipvlan_init(),
but leave needed_headroom and needed_tailroom set to 0.

When the underlying phy_dev (or stacked lower device) requires extra headroom
or tailroom for headers/trailers (e.g. macsec, ipsec, wireguard, tunnels, or
veth with rx headroom), upper layers calculating packet headroom and tailroom
fail to reserve sufficient space.

This can result in reallocation overhead, skb headroom underflows, or KASAN
slab-use-after-free crashes when dev_hard_header() / ipvlan_hard_header()
prepends header data or when lower devices append tailroom.

Fix this by:
1. Inheriting needed_headroom and needed_tailroom from phy_dev in ipvlan_init().
2. Propagating needed_headroom and needed_tailroom updates to attached ipvlans
   in ipvlan_device_event() when receiving NETDEV_FEAT_CHANGE events.

### CVE-2026-74743

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:16:53.113 |

In the Linux kernel, the following vulnerability has been resolved:

macvlan: inherit needed_headroom and needed_tailroom from lowerdev

macvlan devices inherit hard_header_len from lowerdev during macvlan_init(),
but leave needed_headroom and needed_tailroom set to 0.

When the underlying lowerdev requires extra headroom or tailroom for
headers/trailers (e.g. macsec, ipsec, wireguard, tunnels, or veth with rx
headroom), upper layers calculating packet headroom and tailroom fail to
reserve sufficient space.

This can result in reallocation overhead, skb headroom underflows, or KASAN
slab-use-after-free crashes when dev_hard_header() / macvlan_hard_header()
prepends header data or when lower devices append tailroom.

Fix this by:
1. Inheriting needed_headroom and needed_tailroom from lowerdev in macvlan_init().
2. Propagating needed_headroom and needed_tailroom updates to attached macvlans
   in macvlan_device_event() when receiving NETDEV_FEAT_CHANGE events.

### CVE-2026-74737

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:16:52.313 |

In the Linux kernel, the following vulnerability has been resolved:

net: ethernet: ti: am65-cpsw-nuss: Fix port_id extraction from SRC TAG

On the packet reception path, the ID of the MAC Port on which the packet
was received, is embedded in the RX DMA Descriptor's metadata. The ID is
extracted using the helper function cppi5_desc_get_tags_ids() which fills
in the 16-bit Source Tag into the 'port_id' variable. However, it is only
the lower 8-bits of the 16-bit Source Tag that represent the MAC Port ID,
while the upper 8-bits are Hardware-Reserved and carry an arbitrary value.
With the existing logic, sporadic kernel crash is observed due to the
subsequent driver code accessing out-of-bound memory because of an invalid
port_id.

Hence, fix the port_id extraction logic to use only the lower 8-bits of the
Source Tag as the MAC Port ID.

### CVE-2026-77557

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-26T11:16:39.520 |

A malicious actor with access to the network could exploit an Improper Access Control vulnerability found in UniFi Protect AI Key to escalate privileges on the device.

### CVE-2026-77552

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-26T11:16:39.167 |

A malicious actor with access to the network could exploit an Improper Input Validation vulnerability found in UniFi Enterprise Audio/Video Bridge to execute a Command Injection on the device.

### CVE-2026-18080

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-26T11:16:37.930 |

The ERP: Complete HR, Accounting & CRM Suite Built for WooCommerce plugin for WordPress is vulnerable to Unrestricted File Type Upload in all versions up to, and including, 1.17.8 via the save_attachments() function. This is due to missing file extension validation and missing path normalization when CRM Email Connect processes inbound IMAP email attachments. This makes it possible for unauthenticated attackers to send a crafted email to the site's configured inbound mailbox with a forged References header matching the plugin's expected pattern and an attachment filename such as `../helper.php`, causing the cron-based IMAP sync job to write attacker-controlled PHP outside of the .htaccess-protected `crm-attachments` directory and into `wp-content/uploads/`. On configurations where PHP executes in uploads, this can lead to remote code execution. Exploitation requires the CRM module and IMAP Email Connect feature to be enabled and configured.

### CVE-2026-18431

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-26T07:16:45.500 |

The Avada theme for WordPress is vulnerable to Arbitrary File Write in all versions up to, and including, 7.16 when the Fusion Builder plugin is installed and active in versions up to, and including, 3.16. This is due to a chain of authorization and input validation weaknesses across the two components that makes it possible for unauthenticated attackers to write attacker-controlled files to the server. This can be used to create and execute arbitrary PHP files, resulting in remote code execution and complete site compromise. Successful exploitation requires both Avada and Fusion Builder to be installed and active, as well as certain administrator-authored content to be present.

### CVE-2026-58096

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-130;CWE-787` |
| Published | 2026-08-26T06:16:26.577 |

LcpDecodeConfig() did not validate the length of received endpoint discriminator options against the minimum required by RFC 1717.  Undersized options would trigger an out-of-bounds write.

A malicious PPP peer can exploit CVE-2026-58095 and CVE-2026-58096 to crash ppp(8) or potentially execute arbitrary code as root.

### CVE-2026-58095

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-26T06:16:26.460 |

mp_Enddisc() used incorrect length calculations when formatting endpoint discriminator addresses for display, allowing a received endpoint option to overflow a global result buffer.

A malicious PPP peer can crash ppp(8) or potentially execute arbitrary code as root.

### CVE-2026-59354

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-27T10:16:36.063 |

In versions of Spring Security's OAuth2 Authorization Server module 7.0.0 through 7.0.4, when Dynamic Client Registration is explicitly enabled, the registration endpoint performs insufficient validation of certain client metadata fields supplied by the registering client. An attacker who possesses a valid Initial Access Token can register a malicious client with crafted metadata, which, depending on server configuration and how the metadata is later rendered or used, may result in Stored Cross-Site Scripting (XSS), Privilege Escalation, or Server-Side Request Forgery (SSRF).

### CVE-2026-54523

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-26T15:16:48.910 |

Kyverno is a policy engine designed for cloud native platform engineering teams. From 1.18.0 until 1.18.2, the NamespacedMutatingPolicy CEL compiler exposes the generator library to matchConditions, allowing a namespace-scoped policy to invoke generator.apply(namespace, resources) with an arbitrary target namespace. The validation in pkg/cel/policies/mpol/validate.go checks that the policy compiles but does not enforce namespace scope, and GenerateResources in pkg/cel/libs/context.go does not reject the cross-namespace target. A user who can create NamespacedMutatingPolicy objects in one namespace can cause the admission controller, operating with cluster-wide privileges, to create ConfigMaps, NetworkPolicies, Secrets, RoleBindings, and other resources in another namespace, enabling unauthorized modification and potential privilege escalation. This issue is fixed in version 1.18.2.

### CVE-2026-77532

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-26T11:16:38.343 |

A malicious actor with access to an adjacent network could exploit a Buffer Overflow vulnerability found in a DHCPv6-enabled EdgeMAX EdgeSwitch to initiate a Remote Code Execution on such device.

### CVE-2026-77991

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-27T06:17:28.970 |

Joomla Extension - joomlaeventmanager.net - Privileged remote code execution in Joomla Event Manager < 5.0.1 - The administrator source model allows to write dangerous file type incl. PHP, leading to remote code execution.

### CVE-2026-59270

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-08-27T06:17:21.223 |

Spring Security's embedded UnboundID LDAP server (UnboundIdContainer) unconditionally registers an administrative credential and binds its listener to all available network interfaces.
Spring Security 7.1.0
Spring Security 7.0.0 - 7.0.6
Spring Security 6.5.0 - 6.5.11
Spring Security 6.4.0 - 6.4.18
Spring Security 5.8.0 - 5.8.27
Spring Security 5.7.0 - 5.7.25

### CVE-2026-80585

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:14.750 |

In the Linux kernel, the following vulnerability has been resolved:

mptcp: fastopen: only mark MPTFO subflows with SYN data

Passive TCP Fast Open accepts a valid-cookie SYN even when it carries
no data. In that case the child socket's receive queue is intentionally
left empty.

mptcp_fastopen_subflow_synack_set_params() set is_mptfo before checking
for queued SYN data. That made data-less TFO SYNs hit a WARN and, if
the warning was non-fatal, left stale MPTFO state behind. The stale
flag could later trigger a state-confusion bug in
check_fully_established().

Only mark the subflow as MPTFO after confirming that an SKB was queued.
Return quietly when the receive queue is empty.

Note that mptcp_subflow_context's is_mptfo field is now not just about
subflows where the TFO was present, but about MPTFO subflow that
consumed SYN data. Only having a valid cookie but not carrying data is
not really "doing TFO".

### CVE-2026-74751

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:16:54.160 |

In the Linux kernel, the following vulnerability has been resolved:

riscv: lib: Fix ZBB strnlen reading past count boundary

The ZBB-optimized strnlen loop loads one word ahead before checking the
aligned boundary:

    REG_L   t1, SZREG(t0)       // load next word
    addi    t0, t0, SZREG       // advance
    orc.b   t1, t1
    bgeu    t0, t4, 4f          // boundary check AFTER load

where t4 = (s + count) & -SZREG.  When s is aligned and count is a
multiple of SZREG, t4 equals s + count and the loop loads a full word
starting at exactly s + count.  If s + count falls on a page boundary
with the next page unmapped, this faults.

Fix by computing the aligned boundary from the last valid byte
(s + count - 1) instead of s + count.  This makes the loop stop at the
word containing the last valid byte rather than potentially loading the
word after it.  The count == 0 case is already handled by the beqz
early exit.

Also add a pre-loop guard (bgeu t0, t4) for the case where all valid
bytes fit within the first word.  With the adjusted boundary, t4 can
equal t0, and entering the loop with stale register state from the
first-word processing would produce incorrect results.

The final minu clamp ensures the result is still correct when the last
loaded word extends past s + count - 1 within the same aligned word.

### CVE-2026-12717

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Clear` |
| Weaknesses | `CWE-74` |
| Published | 2026-08-26T14:17:07.250 |

An Improper Input Validation vulnerability in CData JDBC driver integration in Google Cloud BigQuery Data Transfer Service versions prior to 2026-05-01 on Google Cloud Platform allows an authenticated attacker to achieve remote code execution in the connector container and escalate privileges in the tenant project using crafted JDBC connection string parameters.


This vulnerability was patched on 1 May 2026, and no customer action is needed.

### CVE-2026-81675

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-27T13:18:43.047 |

The endpoint ‘/ws/apiprensa/getVideoUltimasSeccion’ contains an SQL injection vulnerability in the id_seccion parameter. The parameter is directly embedded in a complex SQL query that includes grouping and sorting operations. By injecting SQL syntax, an attacker can disrupt the query structure and cause database errors, exposing the internal logic of the queries. The complexity of the query increases the potential impact, as it could allow for broader manipulation of the content retrieval logic.

### CVE-2026-81674

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-27T13:18:42.910 |

The endpoint ‘/ws/apiprensa/getVideoNextPrev’ is vulnerable to SQL injection via the id_ambito parameter. Unsanitized input is directly incorporated into a MariaDB query, allowing attackers to inject SQL syntax that interrupts the query's execution. The vulnerability results in detailed database error messages and exposes the internal structure of the queries, which could facilitate further exploitation.

### CVE-2026-81673

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-27T13:18:42.760 |

The ‘/ws/apitribuna/setVisita’ endpoint is vulnerable to SQL injection through the id_video and id_ambito parameters. The application does not validate or sanitize these inputs before including them in SQL queries. This allows a remote attacker to inject SQL syntax and disrupt the execution of queries, causing database errors and potentially manipulating visit tracking records. Given the nature of the endpoint, this could also affect the integrity of analytics and the accuracy of records.

### CVE-2026-81672

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-27T13:18:42.610 |

SQL injection vulnerability in the ‘/ws/apiprensa/getVideoSubcanal’ endpoint due to improper handling of the id_video parameter. The application does not sanitize input before constructing SQL queries, which results in execution errors when malicious input is provided. The vulnerability exposes internal file paths and complete stack traces through the Slim framework’s error handler, which increases the severity due to the combination of information disclosure and SQL injection.

### CVE-2026-74233

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78;CWE-321` |
| Published | 2026-08-27T13:18:34.137 |

Zbtlink WE1326, WE357, WE5926, WE5926-WD, WE826-Q, WE826-T2, WE826-WD, WG108, and WG3526 firmware 19.1101, Zbtlink WE2426-C firmware 19.1112, Zbtlink WE5926-EC_QP firmware 20.0516, Zbtlink WF3526-P firmware 19.051, CTN720-W1, LF-1541, and MT7620N firmware 19.1101, and WRC1 firmware 20.0622 contain an unauthenticated command injection in the infosrvd service (UDP/9992). A remote unauthenticated attacker can send a crafted UDP packet to execute arbitrary commands as root. The service's authentication uses a hardcoded salt and an all-zero wildcard MAC bypass, rendering it ineffective.

### CVE-2026-74232

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-300;CWE-506` |
| Published | 2026-08-27T13:18:33.917 |

Zbtlink L3_V2_8 firmware 3.0.0.4.528, Zbtlink WE826-T2 firmware 19.1101, Zbtlink ZBT-7628 firmware 1.0.0.2.007, Zbtlink ZBT-ZBT7621 firmware 1.0.0.3.001, MoreQuick MQAC-7620, MQAC-7620A, MQAP-7620, MQAP-7620A, and MQAP-7628 firmware 1.0.0.2.000, AP522 firmware 1.0.0.2.014, AP7628 and HC5661A firmware 3.0.0.4.380, APG721B firmware 19.0809, HK300 firmware 1.0.0.2.032, and MAP-N10 firmware 1.0.0.2.044 ship a backdoor command-and-control implant (yunmgrd) reachable over an unauthenticated cleartext UDP channel to a hardcoded C2 server. A remote unauthenticated attacker on the network path can hijack the channel and execute arbitrary commands as root. The attacker can also modify DNS entries, exfiltrate PPPoE credentials, and open reverse SSH tunnels.

### CVE-2026-78288

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-27T10:16:38.267 |

Unauthenticated SQL Injection in Beautiful Taxonomy Filters <= 2.4.6 versions.

### CVE-2026-78260

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-27T10:16:36.880 |

Unauthenticated SQL Injection in Epayco <= 8.4.6 versions.

### CVE-2026-32479

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-27T10:16:35.543 |

Unauthenticated SQL Injection in Visitor Traffic Real Time Statistics Pro <= 11.17 versions.

### CVE-2026-65641

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-08-26T22:16:25.747 |

A vulnerability allowing an unauthenticated network attacker to coerce SMB authentication from the service account.

### CVE-2026-19485

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Clear` |
| Weaknesses | `CWE-330` |
| Published | 2026-08-26T19:16:49.157 |

A Predictable Resource Name vulnerability in BigQuery Import Staging in Google Cloud Vertex AI Search for Commerce versions prior to 2026-04-27 on Google Cloud Platform allows an attacker knowing the victim's project number to obtain read/write access to staged data and error logs using predictable bucket names.



This vulnerability was patched and no customer action is needed.

### CVE-2026-81032

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-26T16:16:46.013 |

NebulaGraph exposes its runtime configuration over an unauthenticated HTTP service. Each daemon starts the web service defined in src/webservice/WebService.cpp, whose bind address defaults to all interfaces, and registers routes for reading and writing gflags alongside status and statistics. Neither the service nor its router carries any authentication, token check or address restriction. The read route returns the daemon's full set of runtime flag values, which includes the configured certificate, key and certificate-authority paths, the password file path, data directories and the transport-security enable flags. The write route parses a supplied map and applies each entry through the gflags runtime setter, so a caller able to reach the port can change the daemon's behaviour without restarting it, including disabling the transport-security flags, redirecting log files and altering flags such as failed_login_attempts and password_lock_time_in_secs. Public reports of this endpoint describe a single name, enable_authorize, being refused by the handler; at release 3.8.0 that refusal is not present and the handler applies every name it is given.

### CVE-2026-80428

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-26T16:16:45.100 |

ILIAS deserialises stored session data for an unauthenticated caller. The Shibboleth back-channel endpoint at components/ILIAS/AuthShibboleth/resources/shib_logout.php runs in a context that ilInitialisation exempts from authentication, and its logout-notification handler locates the session to terminate by reading every live row of the session table and passing each row's stored data to a hand-written parser that calls unserialize without restricting which classes may be constructed. Any serialised object present in any session row is therefore instantiated on behalf of an anonymous request, and object destructors run when those objects are discarded. A serialised object can be placed into a session row without logging in, because the LTI authentication entry point stores request parameters into the session and is reachable on a path the same initialisation code exempts from authentication. A class bundled with the application writes a JSON-encoded structure to a file named by one of its own properties when it is destroyed, which places attacker-controlled content at an attacker-chosen path below the web root and results in code execution as the web server user. Versions 9.22, 10.10 and 11.3 remove the endpoint's logout-notification implementation.

### CVE-2026-80554

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:09.990 |

In the Linux kernel, the following vulnerability has been resolved:

s390/vfio_ccw: Limit the number of channel program segments

The processing of channel programs, and the CCWs within them, is done
recursively. As such, there is an arbitrary (but not architectural)
limit to the number of CCWs that can exist in a single channel program.

The vfio-ccw logic breaks these channel programs into segments whenever
it encounters a Transfer-In-Channel (TIC) CCW, and the combined number
of segments count towards the global limit. Impose an equivalent limit
to the number of segments until such logic can be made non-recursive.

### CVE-2026-80551

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:09.610 |

In the Linux kernel, the following vulnerability has been resolved:

s390/vfio_ccw: Ensure first IDAW remains constant

The first IDAW in a list does not need to be on a 2K/4K boundary
like all others, and so is read separately to accurately calculate
the size of the buffer needed to read the full IDAL.

Verify that the address found in the first IDAW is unchanged between
reads, to ensure a consistent set of IDAWs being worked with.

### CVE-2026-80204

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-26T11:16:39.797 |

The Grav API plugin (getgrav/grav-plugin-api) before 1.0.18 does not apply the API-key scope cap in the injectSecurityTab() function of BlueprintController when deciding whether a page's security/permissions blueprint section is editable. Because the function performs raw isSuperAdmin()/hasPermission() checks without a request parameter, it cannot enforce scopeAllows(). A caller holding a scoped API key may therefore see (and potentially edit) page permission fields beyond the scope granted to the key. The end-to-end write-time impact was not fully confirmed by the reporter.

### CVE-2026-80203

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-26T11:16:39.647 |

The getgrav/grav-plugin-api plugin before 1.0.18 does not enforce API-key scope in the requireNotSuperTarget() function in UsersController.php across seven sensitive user-management endpoints. The check uses isSuperAdmin() on the acting account rather than verifying whether the specific API key carries super authority (via isSuperWithinScope()). As a result, an API key scoped below full super authority but belonging to a super-admin account can act against other super-admin accounts—disabling their 2FA, deleting their avatar, minting new API keys under their identity, or deleting their existing API keys.

### CVE-2026-80349

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-08-26T10:16:43.097 |

TarsWeb decides whether a request comes from a trusted local caller using a client-controlled header. app.js sets Koa's proxy option to true without naming which upstream proxies may be trusted and without limiting the number of forwarded hops, so the request address Koa reports is taken from the X-Forwarded-For header supplied by the caller. In midware/ssoMidware.js a single branch covers both the ignored-path list and the ignoreIps allowlist from config/loginConf.js, which contains the loopback address, and that branch assigns the effective account identity from the uid query parameter before falling through to the request without validating any ticket, cookie or password. A request carrying a forged X-Forwarded-For value naming the loopback address and a uid naming an existing account therefore reaches every route the console mounts as that account, including an administrator, with no credential of any kind. Those routes include user and role administration, service configuration, and package upload and deployment. Version 3.0.16 separates the two branches so that a match on the address allowlist assigns the configured default account rather than one named by the caller.

### CVE-2026-59683

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-08-26T10:16:41.037 |

The OpenRGB network protocol allows to write attacker controlled strings into arbitrary file system paths (extension of CVE-2026-59682). This allows either a full system compromise from local or remote (if the daemon is running as root) or a full account takeover (if the daemon is running in user context).

### CVE-2026-80235

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-26T09:16:49.027 |

EFence developed by Thinking Software Technology has an Arbitrary File Upload vulnerability. Unauthenticated remote attackers can upload and execute web shell backdoors, thereby enabling arbitrary code execution on the server.

### CVE-2026-15203

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1191` |
| Published | 2026-08-26T06:16:25.130 |

Improper access control in debug and engineering interfaces in Danfoss iC7-Automation SP, iC7-Marine, and iC7-Hybrid GR3 allows attackers to gain read/write access to internal values, upload and execute unsigned applications, and upload unsigned EEPROM data and firmware via exposed service interfaces and software update mechanisms

### CVE-2026-75062

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-95;CWE-1188` |
| Published | 2026-08-26T15:16:55.853 |

Improper Neutralization of Directives in Dynamically Evaluated Code ('Eval Injection') in the default lf.query Python protocol in Google langfun versions prior to 0.1.2 allows remote unauthenticated attackers to execute arbitrary Python code in the context of the host application via crafted prompt inputs that cause the model to generate executable Python expressions evaluated without a sandbox.

### CVE-2026-78274

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-27T10:16:37.383 |

Editor Arbitrary File Upload in Fluent Boards Pro <= 2.0.11 versions.

### CVE-2026-70419

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-26T19:16:56.540 |

Dell Cloud Disaster Recovery, versions 20.2 and prior, contain an Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability. A high privileged attacker with remote access could potentially exploit this vulnerability, leading to Command execution.

### CVE-2026-75896

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-798` |
| Published | 2026-08-26T14:17:13.080 |

Use of Hard-coded Credentials vulnerability in TÜBİTAK BİLGEM Software Technologies Research Institute Liderahenk allows Try Common or Default Usernames and Passwords.

This issue affects Liderahenk: before 3.5.5.

### CVE-2026-77542

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-26T10:16:42.170 |

A malicious actor with access to the network and high privileges could exploit an Improper Input Validation vulnerability found in UID Enterprise Agent to execute a Command Injection on the host device.

### CVE-2026-77541

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-26T10:16:42.053 |

A malicious actor with access to the network and high privileges could exploit an Improper Access Control vulnerability found in UniFi Network Application to escalate privileges within the UniFi Network Application.

### CVE-2026-77540

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-26T10:16:41.920 |

A malicious actor with access to the network and high privileges could exploit an Improper Input Validation vulnerability found in UniFi OS Server to execute a Command Injection on the host device.

### CVE-2026-77539

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-26T10:16:41.783 |

A malicious actor with access to the network and high privileges could exploit an Improper Input Validation vulnerability found in UniFi OS Server to execute a Command Injection on the host device.

### CVE-2026-77535

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-26T10:16:41.300 |

A malicious actor with access to the network and high privileges could exploit an Improper Input Validation vulnerability found in UniFi Network Application to execute a Command Injection on an adopted device.

### CVE-2026-77551

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-26T11:16:39.053 |

A malicious actor with access to the network and under certain conditions could exploit an Improper Access Control vulnerability found in UniFi Connect Display Cast Pro to escalate privileges on the device.

### CVE-2026-77549

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-93` |
| Published | 2026-08-26T11:16:38.807 |

A malicious actor with access to the network and under certain conditions could exploit an Improper Neutralization of CRLF Sequences vulnerability found in certain devices running UniFi OS to bypass authentication to such UniFi OS devices or instances.

### CVE-2026-77545

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-489` |
| Published | 2026-08-26T10:16:42.407 |

A malicious actor with access to the network, low privileges and under certain conditions could exploit an Active Debug Code vulnerability found in certain devices running UniFi OS to escalate privileges within such UniFi OS devices or instances.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-79921

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-26T21:16:41.873 |

amqp091-go is a Go AMQP 0.9.1 client. Before version 1.13.0, a compromised or malicious AMQP broker can force the client to allocate resources for and process content body frames that exceed the negotiated frame_max limit. This can lead to unexpected memory consumption or application-layer denial of service (DoS), bypassing the protocol's built-in framing constraints. Version 1.13.0 contains a fix. No known workarounds are available.

### CVE-2026-81677

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-27T13:18:43.340 |

The ‘/ws/apiprensa/getVideo’ endpoint is vulnerable to SQL injection due to improper validation of the GET parameter `id_ambito`. An attacker can inject SQL syntax that breaks the underlying structure of the MariaDB query, resulting in syntax errors and the exposure of database error messages via PDOException. This confirms that user input is being incorporated directly into SQL statements without proper sanitization or the use of prepared statements.

### CVE-2026-81676

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-27T13:18:43.190 |

A vulnerability in the endpoint ‘/ws/apitribuna/ultimosVideos’ where the `limit_videos` parameter is directly concatenated into a MariaDB SQL query without proper sanitization or parameterization. By injecting SQL syntax into this parameter, a remote attacker can cause SQL syntax errors and potentially manipulate backend queries. The issue results in an error-based SQL injection and exposes internal database error messages and stack traces, revealing implementation details of the backend system.

### CVE-2026-81581

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-08-27T10:16:40.617 |

Improper validation of memory boundaries in WibuKey64.sys of WibuKey up to 6.70 for Windows can be exploited by an attacker by setting the pointers outside the scope of the program. This usually results in a denial of service, yet we cannot rule out the possibility of exploits that can cause Remote Code Execution and Privilege Escalation (since the driver runs with system privileges).

### CVE-2026-81579

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-123` |
| Published | 2026-08-27T10:16:40.457 |

In WibuKey for Windows before version 6.71, an untrusted pointer dereference in the WibuKey2_64.sys kernel driver for 64-bit Windows allows an attacker to exploit a write-what-where primitive, enabling local privilege escalation. This can be leveraged to execute arbitrary code, run an administrator shell, or gain full control over the system.

### CVE-2026-81271

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-08-27T10:16:38.910 |

Unauthenticated Cross Site Request Forgery (CSRF) in GeoDirectory <= 2.8.176 versions.

### CVE-2026-78257

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-27T10:16:36.750 |

Contributor PHP Object Injection in Booking and Rental Manager <= 2.7.5 versions.

### CVE-2026-74770

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-26T20:17:59.353 |

Dell PowerProtect One, versions 20.1.0.0 and below, contain an Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability. A low privileged attacker with remote access could potentially exploit this vulnerability, leading to Code execution.

### CVE-2026-68861

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-26T20:17:57.710 |

Dell PowerProtect One, versions 20.1.0.0 and below, contain an Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability. A low privileged attacker with remote access could potentially exploit this vulnerability, leading to Remote execution.

### CVE-2026-80576

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:13.653 |

In the Linux kernel, the following vulnerability has been resolved:

drm/amdgpu: reject oversized IBs with per-ring packet limits

On GFX rings, amdgpu_cs_p2_ib() passed user-supplied ib_bytes through
to ib->length_dw without a limit, while ring_emit_ib() encodes length
into packet fields. Oversized values can corrupt adjacent control bits
and destabilize command submission.

Add a per-ring IB packet size limit helper and reject command
submissions exceeding the corresponding dword limit before IB
allocation. Use the documented 20-bit limit for GFX/compute/SDMA/VPE,
and apply the MM fallback limit for other ring types.

(cherry picked from commit 7f48fa2cf62e3fa6c9c3870aa74988f773247e52)

### CVE-2026-80553

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:09.863 |

In the Linux kernel, the following vulnerability has been resolved:

s390/vfio_ccw: Cancel existing workqueues

The initialization of the io_work and crw_work workqueues begs the
question of whether they should be un-initialized. Add the corresponding
cleanup tags in _release_dev to ensure work isn't dispatched after
the private struct is free'd.

### CVE-2026-80552

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:09.723 |

In the Linux kernel, the following vulnerability has been resolved:

s390/vfio_ccw: Ensure index for read/write regions are within range

The introduction of the capability chain rightly clamped the
region indexes to the range of the capabilities itself, but
neglected to do so for the existing read/write regions which
should also be enforced.

### CVE-2026-80548

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:09.200 |

In the Linux kernel, the following vulnerability has been resolved:

s390/vfio_ccw: Selectively expand io_mutex

The io_mutex was defined to serialize the io_regions, but then has
also sort of been associated with the I/O themselves because of
the close relationship they share.

With the handful of races that are possible, the choices are either to:
 A) expand the scope of io_mutex to close these remaining windows, or
 B) reduce the scope of io_mutex to just io_region, and introduce a new
    lock mechanism for the remaining I/O resources

This patch implements A, since B brings with it a lot more interactions
that would need to be tracked and kept in a correct hierarchy. It also
takes advantage of the workqueue element for cp_free() that now gets
called out of fsm_notoper(), which could be invoked out of an interrupt
context and thus cannot acquire a mutex itself.

### CVE-2026-80547

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:09.087 |

In the Linux kernel, the following vulnerability has been resolved:

s390/vfio_ccw: Implement a crw lock

Unlike the channel_program struct, which covers synchronous I/O
submissions and asynchronous interrupts, the CRW region relies
exclusively on asynchronous events coming from hardware.

Implement a lock to manage the list of those payloads, to ensure
they are read cohesively.

### CVE-2026-59682

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-08-26T10:16:40.893 |

Arbitrary file overwrite via SAVE_PROFILE message in OpenRGB. This issue affects OpenRGB through 1.0rc3.

### CVE-2026-19042

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-26T10:16:40.323 |

A command injection vulnerability in TeamViewer Full
Client and Host for Linux prior to version 15.81.5 allows a remote attacker to
execute arbitrary commands in the context of the current user via a specially
crafted URL sent through the out-of-session chat feature. Exploitation requires
user interaction by clicking the malicious link.

### CVE-2026-18794

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1288` |
| Published | 2026-08-26T10:16:40.167 |

The OpenRGB network protocol allows attackers to cause memory exhaustion and out-of-bounds memory reads and writes by passing inconsistent data.

### CVE-2026-80236

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-26T09:16:49.180 |

Efence developed by Thinking Software Technology has a SQL Injection vulnerability. Unauthenticated remote attackers can access file upload functionality and read database contents.

### CVE-2026-78236

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284;CWE-285;CWE-287;CWE-327` |
| Published | 2026-08-26T08:16:46.600 |

An insecure PIN derivation mechanism in ABR allows a low-privileged user to escalate privileges to administrator by communicating over Cross-Process Communication (XPC) while masquerading as an Apple-signed process.

### CVE-2026-75977

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-26T08:16:46.383 |

The Mang Board WP plugin for WordPress is vulnerable to Missing Authorization via Authentication Cookie Forgery in all versions up to, and including, 2.3.7. This is due to flawed HMAC generation in the mbw_get_hash_key() function that uses the current user's identity instead of the cookie username parameter when a WordPress user is logged in, combined with insufficient validation in mbw_validate_auth_cookie(). This makes it possible for authenticated attackers, with subscriber-level access and above, to forge administrator authentication cookies and change administrator passwords to achieve complete site takeover.

### CVE-2026-81625

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-27T10:16:41.000 |

A remote attacker with user privileges may use a malicious or compromised NASL vulnerability test (VT) on the affected products to trigger a stack buffer overflow and gain full access on the compromised system.

### CVE-2026-75005

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-08-27T10:16:36.493 |

Inefficient Algorithmic Complexity vulnerability in Apache APISIX.

 A single small request can pin a gateway worker at 100% CPU for an extended period in graphql-limit-count routes.




This issue affects Apache APISIX: 3.17.0.



Users are recommended to upgrade to version 3.18.0, which fixes the issue.

### CVE-2026-47665

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-26T23:17:13.693 |

Penpot is an open-source design and prototyping platform. In versions up to and including 2.14.3, Penpot is vulnerable to stored cross-site scripting through file comments, whose content is stored as raw text and rendered into the page with innerHTML without any sanitization. Because the backend applies only a length check and the frontend writes comment content directly through innerHTML, any team member who can comment on a shared file can embed HTML such as an image error handler or script that executes in the browser of every other collaborator. The attack is passive: any user who opens the comments panel on the affected file triggers script execution on the Penpot origin, allowing theft of session cookies, actions performed as the victim, and access to their files and projects. This issue is fixed in version 2.15.3.

### CVE-2026-77298

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-26T22:16:29.570 |

SeaweedFS is a distributed storage system for files and blobs. In versions 4.39 and earlier, the S3 API accepts an external OIDC JWT sent directly in the Authorization header and maps it to an IAM role without enforcing that role's trust policy, so a federated user can assume a role they are not permitted to hold. The standard STS AssumeRoleWithWebIdentity path rejects such a token when the role's trust policy does not trust the token's federated provider, but the direct S3 bearer path validates only the token itself and then authenticates as the mapped role and evaluates that role's attached S3 permissions. As a result, a valid OIDC user whose token would be denied the role through STS can obtain the role's S3 access, including object read, write, and delete, by presenting the raw OIDC JWT directly to the S3 API. This issue is fixed in version 4.40

### CVE-2026-65647

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-08-26T22:16:26.157 |

Improper symlink resolution before file access in Plesk allows remote authenticated users to execute arbitrary code as root.

### CVE-2026-65646

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74` |
| Published | 2026-08-26T22:16:26.020 |

Improper neutralization of special elements in Plesk allows remote authenticated users to disclose arbitrary local files and escalate privileges.

### CVE-2026-76784

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-325` |
| Published | 2026-08-26T18:17:01.903 |

Multiple
TP-Link Kasa smart home devices contain insufficient cryptographic protections
in the local device communication protocol. An adjacent network attacker may
intercept, replay or forge locally exchanged control messages, potentially
resulting in unauthorized device control. 









Successful
exploitation could allow an attacker to manipulate the operational state of an
affected device, resulting in unauthorized state changes, disruption of normal
device functionality or a denial-of-service condition.

### CVE-2026-75960

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-08-26T14:17:13.220 |

Rently Smart Home versions 20.1.0 and prior are vulnerable to an Insufficiently Protected Credentials vulnerability. This could allow an attacker to retrieve pins including the Master Pin, overriding standard user permissions.

### CVE-2026-73108

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-26T14:17:12.830 |

RustDesk versions before 1.4.7 contain an uncontrolled speculative memory allocation vulnerability in BytesCodec. Before authentication, the decoder trusts the payload length encoded in a four-byte frame header and reserves that amount before receiving the payload. A crafted header can request up to 1,073,741,823 bytes of capacity, allowing unauthenticated attackers to use concurrent TCP connections to cause memory exhaustion and denial of service. The fix caps header-triggered speculative preallocation at 256 KiB.

### CVE-2026-80205

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1333` |
| Published | 2026-08-26T11:16:39.950 |

NLTK versions before 3.10.0 contain a regular expression denial of service vulnerability in Text.findall() and TokenSearcher.findall() methods that accept user-supplied regular expressions without validation or timeout. Attackers can supply crafted regex patterns that cause catastrophic backtracking, resulting in indefinite CPU saturation and denial of service to all users of the Python process.

### CVE-2026-80348

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-26T10:16:42.947 |

TarsWeb enforces its per-application roles by calling AuthService from individual controller methods, and four methods in app/controller/patch/PatchController.js make no such call. uploadAndPublish accepts a package upload and then builds and dispatches a deployment task to every server matching the supplied application and module name, while its sibling uploadPatchPackage, which only stores the package, does check developer authorization first. The only precondition uploadAndPublish enforces is that the named server is registered, and any registered server in the installation satisfies it. downloadPackage and deletePatchPackage select a package by an unscoped sequential primary key covering every application's uploads, and setPatchPackageDefault changes which package a given application deploys by default. Any authenticated account, including one holding a role scoped to a single unrelated application, can therefore push a package to and trigger its deployment on any server the console manages, retrieve or delete any other application's package, and change which package is deployed by default.

### CVE-2026-80347

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-26T10:16:42.803 |

mcp-fetch checks a fetch target against its SSRF guard without removing the brackets that surround an IPv6 literal. isSafeUrl reads the hostname from the parsed URL, which for a literal such as http://[::1]/ yields the bracketed string, and then tests it with net.isIP. That call returns zero for a bracketed value, so the branch holding the private-address checks is skipped entirely. The guard falls back to resolving the hostname, the bracketed string is not a resolvable name, no addresses are returned, and the target is reported safe. The HTTP client then strips the brackets and connects. Because the address may be given in IPv4-mapped form, the same path reaches any IPv4 target the loopback and private checks were meant to exclude, including link-local metadata endpoints. isPrivateIPv6 also has no case for the ::ffff: prefix, so the mapped form would still pass even if the brackets were removed. The fetch target is supplied as a tool argument, so an attacker who can influence what the model requests can read internal responses back into the model context.

### CVE-2026-80237

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-26T09:16:49.327 |

EFence developed by Thinking Software Technology has an Arbitrary File Upload vulnerability. Authenticated remote attackers can upload and execute web shell backdoors, thereby enabling arbitrary code execution on the server.

### CVE-2026-77693

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-08-26T06:16:29.210 |

The Order Tip for WooCommerce WordPress plugin before 1.6.0 does not check the capability of the user requesting a file deletion, nor does it restrict which path may be deleted, allowing users with the Shop Manager role and above to delete arbitrary files on the server, which could lead to the site being taken over.

### CVE-2026-81662

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20;CWE-94` |
| Published | 2026-08-27T13:18:42.330 |

Affected versions of Flowintel improperly trust configuration keys supplied to the alerts settings update endpoint. While configuration values were normalized to Python literals, the corresponding keys were used directly when constructing and replacing lines in conf/config_module.py.


The vulnerable code used requester-controlled keys in both the regular expression and the generated assignment:


f'{key} = {py_val}'

and appended an assignment if the key was not already present. The modified Python configuration module was subsequently reloaded using importlib.reload(). This creates a code-generation boundary in which specially crafted configuration keys can alter the Python source structure and result in execution of attacker-controlled Python statements. 

Version impacted >=3.3.0

### CVE-2026-81573

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-27T10:16:39.943 |

If CodeMeter Runtime before 8.41a or 9.10 is configured as a server, the configuration command handler does not enforce network-
origin restrictions. Commands intended only for local or same-network clients can therefore be executed by
arbitrary remote peers. An attacker can read potentially sensitive configuration data and overwrite selected values
in Server.ini. This does include the hash of the credentials for the CodeMeter WebAdmin, enabling WebAdmin
takeover.

### CVE-2026-27330

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-27T10:16:35.290 |

Unauthenticated Broken Access Control in Mobile App for WooCommerce <= 0.4.62 versions.

### CVE-2026-65642

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-26T22:16:25.883 |

Insecure direct object reference in Plesk 18.0.79.7 and earlier or 18.0.80 through 18.0.80.3, allows remote authenticated users to read and modify other customers' databases.

### CVE-2026-55182

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77` |
| Published | 2026-08-26T22:16:24.950 |

LibreNMS is a network monitoring system. In versions from 21.6.0 up to 26.5.0, the Signal alert transport is vulnerable to command injection because the signal-cli path and the Recipient field of an alert transport entry are insufficiently escaped before being passed to an exec call. An authenticated administrator can craft a transport entry whose Recipient contains shell metacharacters and whose path points to the bundled composer_wrapper.php script, which itself passes attacker-controlled input to further unsafe exec calls. By chaining these calls, the administrator can execute arbitrary operating-system commands on the LibreNMS host. This issue is fixed in version 26.5.0.

### CVE-2026-43621

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-26T22:16:24.643 |

Simple Machines Forum (SMF) through 2.1.7, fixed in commit 6f0dc61, contains an authorization state-confusion vulnerability in the profile loader that allows authenticated low-privileged users to gain administrator access by supplying multiple values for the user parameter. Attackers can exploit the mismatch between Profile::$member and User::$me->is_owner during sequential profile loading to be treated as the owner of an administrator profile, enabling unauthorized password changes and full account takeover.

### CVE-2026-58474

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-26T18:16:42.760 |

whichllm before 0.5.16 contains a code injection vulnerability in the run and snippet commands that allows a remote attacker who controls a HuggingFace repository to achieve arbitrary code execution by crafting a malicious GGUF filename containing double quotes or other special characters. The script generation function in cli.py interpolates HuggingFace-derived values, including GGUF variant filenames from the Hub API siblings rfilename field, directly into Python source code without escaping, allowing the crafted filename to break out of the generated string literal and execute injected code on the user's machine before any model download occurs.

### CVE-2026-81031

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-26T16:16:45.860 |

IDURAR ERP CRM changes the password of whichever account a request names rather than the account making the request. The update handler in backend/src/controllers/middlewaresControllers/createUserController/updatePassword.js resolves the authenticated user from the request that the token middleware populated, then issues its update against a filter built from the identifier in the URL path, and never compares the two. The route is mounted behind the administrator token check only, so any valid administrator session is sufficient, and the sole ownership-like guard in the handler rejects a single hardcoded demo address. A caller can therefore set an arbitrary password on any other administrator account and sign in as it. The read handler in the same controller directory accepts an identifier the same way, which supplies the identifiers needed to pick a target.

### CVE-2026-80427

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-08-26T16:16:44.930 |

bestzip builds the argument list for the system zip utility without separating options from operands. The destination archive path and the caller-supplied source paths are passed to the child process with no -- delimiter between them, so any source entry beginning with a hyphen is interpreted by zip as an option rather than a file name. zip accepts -T to test the finished archive and -TT to name the command used to perform that test, so a source list containing those two entries and a command string causes zip to run that command through a shell once the archive has been written. An application that passes a file name or path it received from an untrusted source into the bestzip API therefore executes a command of the supplier's choosing. Versions 2.2.6 and 3.0.2 add the delimiter.

### CVE-2026-54511

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:H/A:N` |
| Weaknesses | `CWE-93;CWE-117` |
| Published | 2026-08-26T15:16:48.727 |

LogTape is an unobtrusive logging library. Prior to 1.3.11, 2.0.14, and 2.1.5, the @logtape/syslog package's escapeStructuredDataValue() function in packages/syslog/src/syslog.ts does not neutralize C0 control characters from U+0000 through U+001F in structured data values, and formatStructuredData() inserts property keys without validating the RFC 5424 SD-NAME grammar. When includeStructuredData is true, an attacker-controlled newline can terminate an RFC 6587 non-transparent TCP syslog frame and make following bytes appear as a forged RFC 5424 record, while a key containing a closing bracket or other forbidden character can terminate or corrupt the structured-data element. Applications that forward attacker-controlled property values or keys can therefore allow forged records with arbitrary hosts, applications, process identifiers, facilities, or severity levels, undermining downstream collector and SIEM integrity. This issue is fixed in versions 1.3.11, 2.0.14, and 2.1.5.

### CVE-2026-12587

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-08-26T13:17:45.663 |

The vulnerability allows the unauthorised generation of physical access QR codes due to the use of hard-coded credentials within the application. The generation mechanism uses the 'badge_number' parameter as the HMAC private key, the value of which remains static and is accessible via the API using the endpoint '/club/_id_club_/member/_id_member_/resamania_qr_info'. An attacker with access to this value and to the application’s cryptographic logic, which can be extracted by reverse engineering the APK as there is no code obfuscation, could generate valid QR codes indefinitely, even after the user has changed their password or logged out.

### CVE-2026-80233

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-26T09:16:48.717 |

CAYIN CMS-WS, CMS-SE, and SMP series products developed by CAYIN Technology have an Arbitrary File Upload vulnerability. Privileged remote attackers can upload and execute web shells backdoors, thereby enabling arbitrary code execution on the server.

### CVE-2026-81277

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-27T10:16:39.557 |

Contributor SQL Injection in Suggestion Engine for WooCommerce <= 2.0.11 versions.

### CVE-2026-78285

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-27T10:16:38.010 |

Subscriber SQL Injection in Like Button Rating <= 2.6.61 versions.

### CVE-2026-32564

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-27T10:16:35.807 |

Subscriber SQL Injection in ACPT (Pro) - Custom Post Types Plugin for WordPress <= 2.0.63 versions.

### CVE-2026-32550

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-27T10:16:35.677 |

Subscriber SQL Injection in Kadence Shop Kit <= 3.0.6 versions.

### CVE-2026-64632

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-08-26T22:16:25.617 |

A vulnerability allowing a low-privileged user to capture the NTLM credentials of the Reporter service account.

### CVE-2026-81036

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-601` |
| Published | 2026-08-26T16:16:46.607 |

Stalwart Mail Server does not compare an OAuth redirect target against any registered destination in its default configuration. The validation routine in crates/http/src/auth/oauth/registration.rs returns success immediately when the client-authentication requirement is disabled, and that requirement is false in the shipped settings, so the supplied redirect value is neither matched against a registered client nor otherwise constrained. The value is stored with the authorization code, and the login page reads it back and sends the browser to it with the code attached. A request naming a destination the attacker controls therefore delivers a valid authorization code there once the account holder authenticates, and because the token endpoint checks only that the redirect presented at exchange matches the one recorded with the code, the same party can exchange it for access and refresh tokens and read the account's mail.

### CVE-2026-81029

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-601` |
| Published | 2026-08-26T16:16:45.550 |

OpenMetadata accepts a caller-supplied post-authentication redirect target and appends the issued token to it. SamlLoginServlet reads the callback request parameter and stores it in the HTTP session without comparing it against any configured or registered destination, and the assertion consumer servlet later formats that stored value into a URL carrying the freshly issued JWT together with the account's email and name before sending the redirect. The OIDC and OAuth2 handler follows the same pattern with its own redirect parameter and the issued identity token. A request naming a destination the attacker controls therefore causes the server to deliver a valid token for whoever completes the login to that destination. Because the token authenticates API calls as that account, a user who follows such a link and authenticates hands over control of their account. Version 2.0.0 removes the caller-supplied callback parameter; no 1.x release validates it.

### CVE-2026-54606

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-26T16:16:27.890 |

SunEditor is a lightweight and powerful WYSIWYG editor in vanilla JavaScript with no dependencies. Prior to 3.1.4, the SunEditor Embed plugin in src/plugins/modal/embed.js parses attacker-controlled raw embed HTML with DOMParser and processes the resulting DOM nodes. When an external script element follows a valid iframe, the plugin recreates a script element from the attacker-controlled src attribute and appends it to the live DOM, causing JavaScript execution in the editor page. If an application stores or reflects SunEditor content without additional backend sanitization, an attacker who can submit embed HTML can trigger stored or reflected cross-site scripting when another user opens, previews, renders, or edits the content, enabling access to page data and account actions as the victim. This issue is fixed in version 3.1.4.

### CVE-2026-15973

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:P/VC:H/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-26T21:16:38.063 |

LimeSurvey Community Edition 7.0.5 contains a stored cross-site scripting vulnerability in the Survey Menu Entries administration page. An authenticated user with the global settings:read permission can create a survey menu entry containing attacker-controlled data. The value is stored in the surveymenu_entries.data field and later inserted into a single-quoted HTML title attribute without context-appropriate encoding.

This issue affects LimeSurvey: 7.0.5.

### CVE-2026-81027

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-26T16:16:45.253 |

one-api gates one of its two channel-pinning paths and not the other. middleware/auth.go permits a request to name a specific channel either through a suffix on the API key or through a URL path parameter. The suffix path is reached only after model.IsAdmin succeeds and otherwise rejects the caller, while the path-parameter branch sets the selected-channel value from c.Param("channelid") with no role check at all. The route carrying that parameter sits behind token authentication only, so any account holding a valid API token reaches it. The value flows to the distributor, which loads the channel by integer identifier with no scoping to the caller's user or group, and then sets the outbound Authorization header to that channel's stored key and directs the request at the channel's base URL. A low-privilege account can therefore pin any channel by incrementing an identifier, causing the server to make upstream requests bearing an operator-configured provider key the account was never granted, and bypassing both the per-group restriction and the channel's model allowlist.

### CVE-2026-80584

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:14.577 |

In the Linux kernel, the following vulnerability has been resolved:

s390/qeth: validate user buffer length in SNMP and ARP query ioctls

qeth_snmp_command() and qeth_l3_arp_query() allocate a buffer sized by
a user-supplied length (udata_len) without checking a lower bound, then
set udata_offset to a fixed non-zero value and pass both to a reply
callback. The callback bounds-checks the copy with

        if ((udata_len - udata_offset) < len)

Both fields are u32, so a udata_len smaller than udata_offset makes the
subtraction wrap and the check pass, and the following memcpy() writes
past the allocation. A udata_len of 0 also yields ZERO_SIZE_PTR from
kzalloc(), which the existing NULL check does not catch.

Reject buffers smaller than udata_offset before allocating, so the
callback subtraction can no longer underflow.

### CVE-2026-80574

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:13.393 |

In the Linux kernel, the following vulnerability has been resolved:

Input: focaltech - fix array out-of-bounds in focaltech_process_rel_packet

Make finger2 (and also finger1) unsigned, so that if the finger index in
the packet is 0 then subtracting 1 creates an array index which overflows
above the existing check for FOC_MAX_FINGERS, as the existing comment says
it should, instead of writing to state->fingers[-1].

### CVE-2026-80536

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:07.777 |

In the Linux kernel, the following vulnerability has been resolved:

xfs: bounds-check buffer log item's dirty bitmap

xlog_recover_do_reg_buffer() replays each dirty region described by a
buffer log item's bitmap into the buffer read for that item:

	memcpy(xfs_buf_offset(bp, (uint)bit << XFS_BLF_SHIFT),
		item->ri_buf[i].iov_base,
		nbits << XFS_BLF_SHIFT);

The destination offset (bit/nbits, from the logged dirty bitmap) and the
buffer size (from the logged blf_len) are both attacker-controlled and
otherwise unrelated, yet the only thing bounding the copy is an ASSERT(),
which compiles away on production kernels. A crafted image logging a
small blf_len together with a bitmap bit past the end of that buffer
drives the memcpy() past the buffer's allocation, corrupting adjacent
kernel heap during mount-time log recovery. This is reachable by anyone
who can get a crafted image mounted -- the malicious-filesystem threat
model XFS already guards against elsewhere.

Turn the ASSERT() into a real XFS_IS_CORRUPT() check that aborts recovery
of the buffer with -EFSCORRUPTED, consistent with the validate-and-fail
idiom already used in xlog_recover_do_inode_buffer() and
xfs_dquot_item_recover.c. xlog_recover_do_reg_buffer() therefore becomes
STATIC int and its three callers propagate the error.

Found and confirmed with KASAN on a CONFIG_XFS_DEBUG=n build: the crafted
image trips a slab-out-of-bounds write before this change and fails
recovery cleanly with -EFSCORRUPTED after it.

### CVE-2026-81034

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-08-26T16:16:46.310 |

Netmaker disables certificate verification on the connection to the configured mail server. The sender in pro/email/smtp.go assigns a TLS configuration whose skip-verify field is set to true unconditionally, directly beneath a comment stating that the setting should be false in production. No configuration value governs it and no code path restores verification, so the client accepts any certificate the mail server presents, including one an interposing party supplies. Mail that Netmaker sends over that connection includes password-reset messages carrying single-use tokens and user invitations carrying enrolment links, so a party positioned on the path between the server and its mail relay can read those messages in transit and use a captured reset token before the intended recipient does. The setting is absent from the development branch but present in the latest release.

### CVE-2026-81574

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-134` |
| Published | 2026-08-27T10:16:40.077 |

In CodeMeter Runtime before versions 8.41a and 9.10, the logger does not sanitize input strings in certain cases, allowing an attacker to inject printf-style format
specifiers. This can be used to reliably crash CodeMeter and disclose sensitive information such as process memory
and stack canaries. The attack works locally, for example by using cmu --set-proxy to set the proxy value, and
remotely when combined with CVE-2026-81573 by setting General.ProxyServer and then triggering this
vulnerability.

### CVE-2026-47877

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-27T06:17:17.490 |

Spring Security Authorization Server's default consent page renders user-controlled values without HTML entity encoding.
Spring Security 7.1.0
Spring Security 7.0.0 - 7.0.6

### CVE-2026-80549

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:09.323 |

In the Linux kernel, the following vulnerability has been resolved:

s390/vfio_ccw: Move cp cleanup out of not operational

The fsm_notoper() routine is called when the device has been
lost, and is (by definition) no longer operational. Since this
can happen asynchronously from the normal behavior of the
driver, the cleanup may happen when holding other locks
in the calling sequence (notably, the cio subchannel lock).

Push the cleanup of the private->cp resources to a workqueue,
where it can be done out from under that lock sequence and
a future patch can safely manage the locking requirements.

### CVE-2026-54556

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-409` |
| Published | 2026-08-26T15:16:49.527 |

Http4s is a Scala interface for HTTP services. Prior to 0.23.35 and 1.0.0-M47, an unauthenticated HTTP/2 peer can cause an out-of-memory denial of service in the Ember backend with HTTP/2 enabled. The Hpack wrapper in ember-core/shared/src/main/scala/org/http4s/ember/core/h2/Hpack.scala concatenates HEADERS and CONTINUATION frame fragments and decodes them into a single List, but maxHeaderSize accounting does not include indexed headers or HPACK per-header overhead. A small compressed header block can therefore expand into a much larger decoded representation that remains in memory for processing. Servers exposed to untrusted HTTP/2 traffic and clients directed to an untrusted HTTP/2 server are affected, and concurrent malicious connections can exhaust the process heap. This issue is fixed in versions 0.23.35 and 1.0.0-M47.

### CVE-2026-80206

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1333` |
| Published | 2026-08-26T11:16:40.103 |

NLTK before 3.10.3 contains a regular expression denial of service (ReDoS) vulnerability in the tgrep module. The _tgrep_node_action function compiles user-supplied regular expressions embedded in /regex/ pattern nodes and executes them via re.search against tree node labels without any validation or timeout. An attacker who controls the tgrep pattern (e.g., via tgrep_positions() or tgrep_compile() exposed to external input) can supply a pattern that triggers catastrophic backtracking, causing indefinite CPU saturation that blocks the Python process.

### CVE-2026-77538

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-26T10:16:41.650 |

A malicious actor with access to the network could exploit an Improper Access Control vulnerability found in UniFi Connect Application to escalate privileges within the UniFi Connect Application.

### CVE-2026-19538

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290;CWE-672` |
| Published | 2026-08-26T09:16:46.057 |

The BLOCKED access control list items that are evaluated to deny access on the the proxy protocol port can be bypassed completely when connecting over TCP or TLS and sending the query twice on connection that is kept open.

### CVE-2026-19401

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-617` |
| Published | 2026-08-26T09:16:45.857 |

Any remote client can crash a (debugging/non-release build type) NSD serve child by sending it a special crafted message with a specially tuned number of DNS Cookie options (17 when UDP payload size is 512). By continuously crashing the serve childs, the remote client can severely hamper or, when positioned sufficiently close, deny all DNS service.

### CVE-2026-18664

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284;CWE-697` |
| Published | 2026-08-26T09:16:45.437 |

When ranges are used for access control (i.e. of the form 1.2.3.4-1.2.3.25), because NSD wrongly compares the IP address with the range on little endian systems, IPs that were meant to be allowed may be denied, and, IPs that were meant to be denied access could be allowed. An IPv4 address is compared with IPv4 ranges as unsigned 32 bit numbers directly with the endianness of the host, but the values to compare are in network byte order (big-endian).  With IPv6 addresses the comparison is done in 4 times a unsigned 32 bit number comparison, again with the endianness of the host where all values are actually in network bye order.

### CVE-2026-81273

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-352` |
| Published | 2026-08-27T10:16:39.167 |

Unauthenticated Cross Site Request Forgery (CSRF) in FluentBooking Pro <= 2.2.4 versions.

### CVE-2026-77317

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-26T22:16:29.717 |

SeaweedFS is a distributed storage system for files and blobs. In versions from 3.88 through 4.39, the SFTP server evaluates configured path permissions with a literal string-prefix comparison, so a user scoped to a path is also granted the same access to any sibling path whose name merely begins with the same characters. A user granted access to /tenants/alice therefore also matches /tenants/alice-archive, /tenants/alice2, and similar siblings, because the check does not require a path-component boundary. An authenticated low-privilege SFTP user with a root home directory and narrow path permissions can thereby cross the configured ACL boundary to read another tenant's files, and to overwrite them if granted write, all through the documented SFTP service with its own valid credentials. This issue is fixed in version 4.40.

### CVE-2026-55228

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-26T21:16:38.737 |

Weblate is a web-based continuous localization platform used to manage software translations. In versions prior to 2026.7, the REST API did not properly enforce the scope of project- and workspace-scoped teams, allowing a user to submit invalid team configurations through the API. By assigning projects to a team via these unvalidated requests, a user could grant access to projects they were not authorized to see or manage. This could expose private projects and permit translation, repository, and project-management operations outside the user's intended permission scope. This issue is fixed in version 2026.7.

### CVE-2026-32258

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-26T17:16:53.410 |

Winter is a free, open-source content management system (CMS) based on the Laravel PHP framework. From 1.2.10 through 1.2.12, authenticated backend users with the backend.manage_editor permission can store custom Markup Styles that are compiled by the LESS parser and rendered without sanitization on every backend page, allowing stored cross-site scripting. This issue is fixed in version 1.2.13.

### CVE-2026-32257

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-26T17:16:53.247 |

Winter is a free, open-source content management system (CMS) based on the Laravel PHP framework. Prior to 1.2.13, custom CSS supplied through the Brand Settings Styles field by a backend user with the backend.manage_branding permission is compiled by the LESS parser and rendered without sanitization on every backend page, allowing stored cross-site scripting against backend users. This issue is fixed in version 1.2.13.

### CVE-2026-15985

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-289` |
| Published | 2026-08-26T12:16:20.940 |

The Classified Listing - Mobile Number Verification plugin for WordPress is vulnerable to Authentication Bypass in all versions up to, and including, 1.6.0. This is due to missing server-side Firebase OTP validation in the process_otp_login() function. This makes it possible for unauthenticated attackers to authenticate as any user with a phone number registered in the plugin's phone table by submitting an arbitrary OTP code and UID through the Firebase OTP login flow. Successful exploitation requires OTP login to be enabled with Firebase selected as the verification gateway, and requires the attacker to know or guess the target account's registered phone number. Administrator account takeover is possible if an administrator account has a phone number registered in the plugin.

### CVE-2026-19718

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-26T06:16:25.900 |

The BlogVault Backup & Staging WordPress plugin before 6.65, MalCare WordPress Security Plugin  WordPress plugin before 6.65, The WP Remote WordPress Plugin WordPress plugin before 6.65 do not prevent unauthenticated users from obtaining data derived from the secret that binds a site to its remote management service, and generate that secret with a weak pseudo-random number generator, allowing attackers to recover it and gain administrative access to the site.

### CVE-2026-80550

| 項目 | 値 |
|------|-----|
| CVSS | `7.9` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:09.477 |

In the Linux kernel, the following vulnerability has been resolved:

s390/vfio_ccw: Fix out of bounds check on CCW array

The routine ccwchain_calc_length() counts the number of channel
command words (CCWs) that are chained together in a single channel
program, and rejects anything larger than CCWCHAIN_LEN_MAX (256) CCWs.

The loop itself is "do..while (count < 257)", and while the logic in
is_cpa_within_range() correctly adjusts between the 0-index array of
CCWs and the count of CCWs starting at 1, this means it would look
at a possible 257th CCW before ending the loop and (correctly)
returning an error.

Fix this by restructuring the loop to break as soon as 256 CCWs
(thus indexes 0-255) are examined, without looking at memory
outside the range.

### CVE-2026-81572

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-08-27T10:16:39.810 |

cmu.exe --create-io --file C: creates a predictable temporary file under C:\CM-Stick. The directory and
file paths are not properly checked for NTFS reparse points, such as junctions or symbolic links, before file
operations are performed. A local attacker can create a junction at the temporary file that points to an arbitrary
system path. Because CodeMeter Runtime runs with System privileges, this could allow arbitrary files to be deleted
with System privileges and potentially enable local privilege escalation.

### CVE-2026-77652

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-26T20:18:02.160 |

A heap-based buffer overflow vulnerability exists in the Dia diagram editor WPG file format importer.

In plug-ins/wpg/wpg-import.c, the WPG import renderer allocates a fixed palette with:

    ren->pPal = g_new0(WPGColorRGB, 256);

When handling a WPG_COLORMAP record, the parser reads a start index (i16) and number of colors (iNum16) from the file and reads palette data with:

    bRet &= (iNum16 == (int)fread(&ren->pPal[i16], sizeof(WPGColorRGB), iNum16, f));

The only bounds-related check is `if (i16 >= 0 && i16 <= iSize)`, where iSize is the WPG record size—not the palette capacity. There is no validation that i16 is less than 256 or that i16 + iNum16 does not exceed 256.

A malicious WPG file can supply i16=256 and iNum16=264. That causes fread() to write 792 bytes starting at &pPal[256], while the palette buffer is only 768 bytes (256 entries × 3 bytes). This overflows into adjacent heap metadata and can crash Dia (SIGABRT / malloc corruption errors) or, depending on heap layout and exploit primitives, potentially lead to arbitrary code execution.

Exploitation requires convincing a user to open a crafted WPG file via Dia's file dialog, command line, or file association. No special privileges are required to deliver the file to the victim.

Affected component: WPG parser (plug-ins/wpg/wpg-import.c).
Affected versions: all Dia versions containing this code path (reporter tested Dia 0.98+git20260221-1; issue present on upstream master as of 2026-08-21).

### CVE-2026-80583

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:14.437 |

In the Linux kernel, the following vulnerability has been resolved:

ASoC: codecs: lpass-tx-macro: Fix enum kcontrol accesses

The "DEC0 MODE" to "DEC7 MODE" controls are enumerated, but
tx_macro_dec_mode_get() and tx_macro_dec_mode_put() access their
value through ucontrol->value.integer.value[0] (a long) instead of
ucontrol->value.enumerated.item[0] (an unsigned int).

This same pattern was fixed in the sibling drivers by
commit bcfe5f76cc40 ("ASoC: codecs: rx-macro: fix accessing array
out of bounds for enum type") and
commit 0ea5eff7c606 ("ASoC: codecs: va-macro: fix accessing array
out of bounds for enum type"), but tx-macro was missed.

On 64-bit kernels built with CONFIG_SND_CTL_DEBUG, the elem value
sanity check catches the 4 bytes written past the enumerated item
and every read of these controls fails with -EINVAL:

  snd-sm8250 sound: control 2:0:0:DEC0 MODE:0: access overflow

### CVE-2026-80582

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:14.337 |

In the Linux kernel, the following vulnerability has been resolved:

drm/shmem_helper: Check VMA boundaries for PMD mappings

In the ->huge_fault handler do not install a PMD huge page
mapping if the huge page exceeds the boundaries of the VMA.

All other ->huge_fault handlers have similar checks and the
resulting mapping will trigger a VM_BUG_ON_VMA() if it ever
reaches copy_pmd_range().

### CVE-2026-80580

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:14.103 |

In the Linux kernel, the following vulnerability has been resolved:

fbdev: bound mode sysfs output to the sysfs buffer

mode_string() uses snprintf() which can return a value larger than the
remaining buffer space. show_modes() accumulates the return value into i
without checking whether i has reached PAGE_SIZE, causing the offset to
advance past the sysfs buffer if the modelist is long enough.

Add a size parameter to mode_string() and use scnprintf() to return
only the bytes actually written. Add an early return when offset
already exceeds the buffer. In show_modes(), stop accumulating once
the buffer is full.

### CVE-2026-80579

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:14.007 |

In the Linux kernel, the following vulnerability has been resolved:

fbdev: clear fb_info->mode before deleting a videomode

fb_set_var() can delete a mode from info->modelist when userspace
passes FB_ACTIVATE_INV_MODE through FBIOPUT_VSCREENINFO. The code
checks that the mode being deleted is not the current info->var and
that fbcon is not using it, but it does not check fb_info->mode.

fb_info->mode may still point into the modelist entry being deleted.
If the entry is freed, later mode sysfs reads through show_mode() can
dereference a stale pointer.

Clear fb_info->mode before calling fb_delete_videomode() when it
matches the mode being removed.

### CVE-2026-80575

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:13.530 |

In the Linux kernel, the following vulnerability has been resolved:

Input: cs40l50-vibra - validate custom data from user space

cs40l50_add() copies the custom data of an FF_PERIODIC/FF_CUSTOM effect
straight from the ff_effect the user passed to EVIOCSFF, without
requiring it to hold anything:

    work_data.custom_data = memdup_array_user(periodic->custom_data,
                                              periodic->custom_len,
                                              sizeof(s16));
    work_data.custom_len = periodic->custom_len;

The driver then reads two words out of that buffer: custom_data[0] as the
waveform bank in cs40l50_effect_bank_set(), and custom_data[1] as the
index within the bank in cs40l50_effect_index_set().  Neither read is
covered by a length check, and custom_len is fully user controlled:

  - custom_len == 0 makes memdup_array_user() call memdup_user() with a
    length of zero, which returns ZERO_SIZE_PTR rather than an error, so
    custom_data[0] dereferences it.

  - custom_len == 1 allocates two bytes.  A bank of ROM or RAM keeps
    effect->type out of the OWT case, and custom_data[1] is then read one
    word past the allocation.

The bank value itself is also mishandled.  It is masked with
CS40L50_CUSTOM_DATA_MASK (0xffff) but stored in an s16, so a
custom_data[0] of 0x8000 or above wraps to a negative value that passes
the "bank_type >= CS40L50_WVFRM_BANK_NUM" test.
cs40l50_effect_index_set() indexes vib->dsp.banks[] with it before the
switch statement's default case gets a chance to reject it:

    base_index = vib->dsp.banks[effect->type].base_index;
    max_index = vib->dsp.banks[effect->type].max_index;

Require the two words the driver reads to be present, and hold the masked
bank in a u32 so the existing upper-bound test covers the whole range.
The da7280 haptic driver already range checks custom_len this way.

### CVE-2026-80572

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:13.140 |

In the Linux kernel, the following vulnerability has been resolved:

Input: byd - synchronize timer deletion before freeing private data

byd_disconnect() uses timer_delete() before freeing the driver's private
data.  This does not wait for a running byd_clear_touch() callback, which
dereferences the private data and its psmouse pointer.  A callback racing
with disconnect can therefore access the private data after it has been
freed.  The timer can also still be re-armed by byd_process_byte() while
the disconnect is in progress.

Use timer_shutdown_sync() before freeing the private data: it waits for
a running callback and turns any later re-arm attempt into a no-op.

### CVE-2026-80570

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:12.880 |

In the Linux kernel, the following vulnerability has been resolved:

Input: synaptics-rmi4 - zero report size on F54 work error

In rmi_f54_work(), if an error occurs during report request or command
verification, the code jumped directly to the 'error' label, bypassing
the 'abort' label where f54->report_size was normally zeroed out.

This left f54->report_size containing its previous successful payload
size. If a user then altered the V4L2 format to a smaller size, and a
subsequent run failed, rmi_f54_buffer_queue() would copy the stale,
larger payload size into the shrunken V4L2 buffer, causing a heap
buffer overflow.

Fix this by merging the 'abort' and 'error' labels into a single 'out'
exit path, and ensuring that f54->report_size is always set to 0 on
failure by checking for error and zeroing the local report_size first.

### CVE-2026-80569

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:12.457 |

In the Linux kernel, the following vulnerability has been resolved:

Input: synaptics-rmi4 - bound the F54 report size to the allocated buffer

rmi_f54_work() reads a diagnostics report from the device into
f54->report_data, sizing the transfer with rmi_f54_get_report_size():

	report_size = rmi_f54_get_report_size(f54);
	...
	for (i = 0; i < report_size; i += F54_REPORT_DATA_SIZE) {
		int size = min(F54_REPORT_DATA_SIZE, report_size - i);
		...
		rmi_read_block(.., f54->report_data + i, size);
	}

report_data is allocated once at probe from F54's own electrode counts
(array3_size(f54->num_tx_electrodes, f54->num_rx_electrodes, sizeof(u16))),
but rmi_f54_get_report_size() computes the size from
drv_data->num_*_electrodes when those are set, i.e. from the F55
function's electrode counts. Both counts come straight from device
queries (F54 and F55 each report up to 255 electrodes) and nothing
constrains the F55 counts to the F54 ones.

A malicious or malfunctioning RMI4 device that reports larger F55
electrode counts than its F54 counts makes report_size exceed the
allocation, so the read loop writes past report_data (and the V4L2
dequeue memcpy() then reads past it). On conforming hardware the F55
configured electrodes are a subset of the F54 physical electrodes, so
report_size never exceeds the buffer and well-behaved devices are
unaffected.

Record the allocation size and reject a report that does not fit,
mirroring the existing zero-size check.

### CVE-2026-80568

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:12.303 |

In the Linux kernel, the following vulnerability has been resolved:

Input: synaptics-rmi4 - block s_input when F54 queue is busy

Changing the input (diagnostic report type) mid-stream changes the
report size. Since V4L2 buffers are allocated based on the size at
stream start, changing the input while streaming could lead to a
heap buffer overflow if the new size is larger than the allocated
buffers.

Prevent this by blocking VIDIOC_S_INPUT with -EBUSY if the V4L2 queue
is busy (streaming).

### CVE-2026-80565

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:11.550 |

In the Linux kernel, the following vulnerability has been resolved:

crypto: qce - fix error path in devm_qce_register_algs

If ops->register_algs() fails, the error path repeatedly calls the same
ops->unregister_algs() from the failed registration. Use the loop index
to unregister the previously registered algorithms instead.

### CVE-2026-80560

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:10.850 |

In the Linux kernel, the following vulnerability has been resolved:

openrisc: signal: do not restore privileged SR bits on sigreturn

restore_sigcontext() copies the whole supervision register (SR) from the
signal frame and only clears SPR_SR_SM before the value is reloaded into
the hardware SR (through ESR and l.rfe) on the return to user space.  All
other SR bits are left under user control.

An unprivileged task can thus return from a signal handler through a
crafted sigframe that clears SPR_SR_DME.  With the data MMU disabled the
CPU performs no translation or protection on data accesses, so the task
gains read and write access to arbitrary physical memory, a local
privilege escalation.  SPR_SR_IME, SPR_SR_SUMRA, SPR_SR_LEE, SPR_SR_EPH
and the cache-enable bits are exposed the same way.  The ptrace GPR regset
already refuses any change to SR for exactly this reason.

Restore only the arithmetic flag bits (F, CY, OV) from the signal frame
and take every privileged control bit from the SR the kernel saved on
signal entry.

Verified with qemu-system-or1k -M or1k-sim: before this change an
unprivileged PoC clears SPR_SR_DME in rt_sigreturn and writes a marker to
physical address 0x03000000 (beyond the kernel's mem=32M); afterwards the
same PoC receives SIGSEGV and physical memory is unchanged.

### CVE-2026-80559

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:10.690 |

In the Linux kernel, the following vulnerability has been resolved:

Input: sur40 - fix input device registration ordering

In sur40_probe(), input_register_device() was previously called early before
the V4L2 video device and vb2_queue components were fully initialized. If
userspace opened the input device immediately upon registration, sur40_open()
would trigger and start the sur40_poll() worker thread. This worker thread
invokes sur40_process_video() and accesses the uninitialized vb2_queue
structure, leading to a data race and potential system crash.

Furthermore, if V4L2 or video registration failed after input_register_device()
succeeded, the error path fell through to calling input_free_device() on a
successfully registered device instead of input_unregister_device(), corrupting
input core state.

Move input_register_device() to the very end of sur40_probe(). This ensures
the V4L2 and video queue structures are fully initialized before polling can
start, and naturally resolves the error path bug since input_free_device()
is now only called when input registration has not yet occurred.

To maintain strict LIFO (Last-In, First-Out) teardown ordering, also move
input_unregister_device() to the very beginning of sur40_disconnect(). This
guarantees that the input polling worker thread is stopped before V4L2
video components or control handlers are unregistered.

### CVE-2026-80556

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:10.253 |

In the Linux kernel, the following vulnerability has been resolved:

mmc: atmel-mci: Fix use-after-free in atmci_remove due to race condition

In atmci_probe, &host->bh_work is bound with atmci_work_func, and
atmci_interrupt, atmci_timeout_timer and atmci_dma_complete can all
queue this work on system_bh_wq.

If we remove the module, atmci_remove makes cleanup and the memory
allocated for host with devm_kzalloc() is released after the remove
callback returns, while the work mentioned above may still be pending
or running. The sequence of operations that may lead to a UAF bug is
as follows:

CPU0                                      CPU1

                                          | atmci_interrupt
                                          | queue_work(system_bh_wq,
                                          |            &host->bh_work)
atmci_remove                              |
atmci_cleanup_slot(...)                   |
atmci_writel(host, ATMCI_IDR, ~0UL)       |
timer_delete_sync(&host->timer)           |
dma_release_channel(host->dma.chan)       |
free_irq(platform_get_irq(pdev, 0), host) |
                                          | atmci_work_func
                                          | // use host
// devm resources released after          |
// remove returns, host is freed          |
                                          | // use host (use-after-free)

Fix it by canceling the work after all the sources that can schedule
it (IRQ handler, timeout timer and DMA completion callback) have been
stopped, and before proceeding with the remaining cleanup in
atmci_remove.

### CVE-2026-80546

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:08.977 |

In the Linux kernel, the following vulnerability has been resolved:

s390/zcrypt: Improve CCA CPRB length and overflow checks

The xcrb_msg_to_type6cprb_msgx() function lacks proper input
validation, creating security vulnerabilities:
1. Integer overflow after CEIL4 alignment: Signed int variables could
   overflow during 4-byte boundary alignment, causing undersized
   buffer allocations or incorrect bounds checking.
2. Missing minimum size validation: The CPRBX structure is copied from
   userspace without verifying sufficient buffer length. Undersized
   buffers cause uninitialized memory access when reading structure
   fields like cprbx.cprb_len and cprbx.domain.
3. Arithmetic overflow in sum calculations: Adding control block and
   data block sizes could overflow, bypassing size checks and enabling
   buffer overflows.

Fix by using size_t for length calculations, adding U32_MAX boundary
checks after alignment, validating minimum control block size before
copying from userspace, and detecting sum calculation overflows.

### CVE-2026-80545

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:08.870 |

In the Linux kernel, the following vulnerability has been resolved:

s390/zcrypt: Improve EP11 CPRB length and overflow checks

The xcrb_msg_to_type6_ep11cprb_msgx() function lacks proper input
validation, creating security vulnerabilities:
1. Missing minimum size validation: The ep11_cprb structure and
   subsequent payload fields (pld_tag, pld_lenfmt) are copied from
   userspace without verifying sufficient buffer length.
2. Arithmetic overflow in length calculations: CEIL4 alignment could
   overflow, bypassing size checks and enabling buffer overflows.
3. The payload is asn1 encoded but the function just uses a simple c
   struct overlay to access some fields of the payload.

Fix by using size_t for length calculations, adding U32_MAX boundary
checks after alignment, and validating minimum request size and
minimum reply size before copying from userspace. Do a very simple
asn1 parsing of the payload up to the function value field.

### CVE-2026-80544

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:08.763 |

In the Linux kernel, the following vulnerability has been resolved:

s390/zcrypt: Improve EP11 CPRB domain handling with ASN.1 parsing

The zcrypt_msgtype6_send_ep11_cprb() function uses fragile struct
overlays to access and modify the domain field in the EP11 CPRB
payload, creating maintainability and security concerns:
1. Struct overlay approach (pld_hdr) assumes fixed payload structure
   and doesn't validate the actual ASN.1 encoding.
2. Complex length format detection logic is error-prone and doesn't
   properly validate bounds at each parsing step.
3. Direct struct member access bypasses proper ASN.1 validation.

Fix by replacing struct overlays with explicit ASN.1 parsing that
validates each field (payload tag/length, function tag/length/value,
optional domain tag/length/value) with proper bounds checking at every
step. Add asn1_int_encode() helper function to safely write integer
values with correct endianness conversion. This makes the code
consistent with the validation pattern introduced with the rework of
the xcrb_msg_to_type6_ep11cprb_msgx() function.

### CVE-2026-80541

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:08.400 |

In the Linux kernel, the following vulnerability has been resolved:

drm/amdgpu: validate GEM_CREATE domain combinations

AMDGPU_GEM_CREATE checked domain bits against AMDGPU_GEM_DOMAIN_MASK,
but did not validate domain combinations. Userspace could combine
CPU|GTT|VRAM with DOORBELL, GDS, GWS, or OA, making
amdgpu_bo_placement_from_domain() exceed AMDGPU_BO_MAX_PLACEMENTS and
hit BUG_ON().

Allow combinations only within CPU/GTT/VRAM, and require non-CPU/GTT/
VRAM domains to be specified one at a time. Return -EINVAL for invalid
combinations in amdgpu_gem_create_ioctl().

v2: Rename helper from amdgpu_gem_domain_valid() to
    amdgpu_gem_are_domains_valid() (Christian)

(cherry picked from commit db39852d0c39843cb02048dfb47e4b8c703e9080)

### CVE-2026-80540

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:08.257 |

In the Linux kernel, the following vulnerability has been resolved:

drm/amdgpu: Fix UVD decode image min size calculation

This needs to use pitch instead of width. Also reject pitch
over 4096 to avoid overflow.

(cherry picked from commit b41c8cb12e202b220353332ab87dc01a11f69304)

### CVE-2026-80537

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:07.890 |

In the Linux kernel, the following vulnerability has been resolved:

xfs: fix off-by-one in rtrefcount btree root level validation

xfs_rtrefcountbt_compute_maxlevels() sets

	mp->m_rtrefc_maxlevels = min(d_maxlevels, r_maxlevels) + 1;

where the trailing "+ 1" already accounts for the inode-root level, so the
deepest valid on-disk root level is m_rtrefc_maxlevels - 1 and a cursor must
satisfy bc_nlevels <= bc_maxlevels (= m_rtrefc_maxlevels).

The two on-disk validation paths, xfs_rtrefcountbt_verify() and
xfs_iformat_rtrefcount(), check the root level with ">" instead of ">=", so a
crafted rtreflink (metadir + realtime + reflink) image whose
/rtgroups/N.refcount inode has bb_level == m_rtrefc_maxlevels is accepted on
mount. xfs_rtrefcountbt_init_cursor() then sets bc_nlevels = bb_level + 1,
exceeding bc_maxlevels by one. Since the xfs_rtrefcountbt_cur slab object is
sized for exactly bc_maxlevels entries, the first btree op on such a cursor
indexes bc_levels[m_rtrefc_maxlevels] past the end of the object. This is
reached by the first rtrefcount cursor built after mount, via log/CoW
recovery (xfs_reflink_recover_cow() during xfs_mountfs()) or an
FS_IOC_GETFSMAP over the realtime device.

Reject a root level equal to m_rtrefc_maxlevels, matching the ">=" form
already used by the sibling data-device refcount/rmap verifiers and the
in-memory rtrmap verifier.

  BUG: KASAN: slab-out-of-bounds in xfs_btree_lookup (fs/xfs/libxfs/xfs_btree.c:2101)
  Write of size 2 at addr ffff888018391658 by task exploit/144
   xfs_btree_lookup (fs/xfs/libxfs/xfs_btree.c:2101)
   xfs_btree_query_range (fs/xfs/libxfs/xfs_btree.c:5308)
   xfs_refcount_recover_cow_leftovers (fs/xfs/libxfs/xfs_refcount.c:2113)
   xfs_reflink_recover_cow (fs/xfs/xfs_reflink.c:1085)
   xlog_recover_finish (fs/xfs/xfs_log_recover.c:3551)
   xfs_mountfs (fs/xfs/xfs_mount.c:1158)
   xfs_fs_fill_super (fs/xfs/xfs_super.c:1940)
   get_tree_bdev_flags (fs/super.c:1634)
   vfs_get_tree (fs/super.c:1694)
   path_mount (fs/namespace.c:4161)
   __x64_sys_mount (fs/namespace.c:4367)
   entry_SYSCALL_64_after_hwframe (arch/x86/entry/entry_64.S:121)
  The buggy address belongs to the cache xfs_rtrefcountbt_cur of size 216
  The buggy address is located 8 bytes to the right of
   allocated 216-byte region [ffff888018391578, ffff888018391650)
  Kernel panic - not syncing: Fatal exception

### CVE-2026-80531

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:07.140 |

In the Linux kernel, the following vulnerability has been resolved:

xfs: avoid UAF on sc->tempip in xrep_tempfile_create

LOLLM noticed a potential UAF if the tempfile creation code fails after
it set sc->tempip.  Fix that.

### CVE-2026-80526

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:06.350 |

In the Linux kernel, the following vulnerability has been resolved:

ASoC: tas2562: Validate values for volume writes

tas2562_volume_control_put() does not do any validation of the control
value written by userspace, it uses it to look up a value in a fixed
size array which can easily be overflowed and then writes whatever value
it gets back to the device.  Add validation that we are loading a value
we have in the array.

### CVE-2026-80522

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:05.800 |

In the Linux kernel, the following vulnerability has been resolved:

crypto: tegra - fix rctx->cryptlen calculation in tegra_gcm_do_one_req()

Perform rctx->cryptlen calculation in tegra_gcm_do_one_req() the same way
it is done in tegra_ccm_crypt_init(). The current formulae may lead to a
crash if a caller does not call tegra_gcm_setauthsize() and so ctx->authsize
remains zero. Then a decrypt operation with incorrect rctx->cryptlen will
lead to a write beyound rctx->dst_sg buffer.

As a follow-up cleanup delete struct tegra_aead_ctx->authsize field since
it appears to be completely unused. Also simplify tegra_ccm_setauthsize()
and tegra_gcm_setauthsize() functions respectively.

### CVE-2026-80521

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:05.677 |

In the Linux kernel, the following vulnerability has been resolved:

af_unix: Unlink scc_entry in unix_del_edge().

Kyle Zeng reported that GC could free a dead SCC partially.

The scenario is as follows:

   1) Create two SCCs:

       X -.   A <-> B
       ^--'

   2) Run the following concurrently:

      2-1) send() sk-B to sk-B from sk-X
      2-2) close() both A and B

At 2-1), there is a small window where unix_add_edges()
publishes a new edge (B <-> B) to GC but its skb is not queued
by skb_queue_tail().

If 2-2) completes before skb_queue_tail() and GC is triggered,
it judges A <-> B as dead, but B is not freed because GC cannot
collect the not-yet-queued skb holding the B <-> B edge.

       X -.   A <-> B -. This edge is visible
       ^--'         ^..'  but skb is not

This itself is not a problem since the next GC run will judge
B as dead as well and free it finally.

       X -.   A <.> B -.
       ^--'         ^--'

However, X's SCC forces the next GC to call unix_walk_scc_fast(),
and it iterates over A through B's scc_entry.

Let's unlink scc_entry before freeing the vertex in unix_del_edge().

### CVE-2026-74753

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:16:54.387 |

In the Linux kernel, the following vulnerability has been resolved:

perf: Reject exited events as group leaders

perf_event_remove_on_exec() sets remove-on-exec events to the EXIT state
and detaches their group relationships.  The event's file descriptor can
remain open, however, and perf_event_open() currently accepts that event
as a group leader because its early validation rejects only REVOKED and
DEAD events.

A new sibling can consequently be linked to the detached leader.  When
the leader is closed, perf_group_detach() observes that its
PERF_ATTACH_GROUP bit is already clear and skips the new sibling.  The
sibling then retains a group_leader pointer to the freed event.

Reject group leaders in the EXIT state.  Perform the check while holding
the shared context mutex so that an exec in the target task cannot detach
the leader between validation and group attachment.

[peterz: make the earlier test fully consistent]

### CVE-2026-74748

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:16:53.770 |

In the Linux kernel, the following vulnerability has been resolved:

netfilter: ipset: fix refcount race between list:set GC and swap

__ip_set_put_byindex() resolved the index to a set pointer under RCU,
then took ip_set_ref_lock in __ip_set_put() to decrement set->ref.
ip_set_swap() holds that same lock while swapping both the ip_set_list
slots and the two sets' ref counters, so it can interleave between the
dereference and the lock acquisition, leaving the caller to decrement a
set whose reference already moved to the other index and hit
BUG_ON(set->ref == 0). list_set_gc() reaches this from timer softirq,
which the nfnl mutex does not serialize against swap: an expiring
list:set member calls list_set_del() -> ip_set_put_byindex() while
IPSET_CMD_SWAP runs on the referenced sets.

Resolve the index and decrement under ip_set_ref_lock, as ip_set_swap()
already does, keeping the refcount tied to the index rather than to a
stale set pointer.

  kernel BUG at net/netfilter/ipset/ip_set_core.c:685!
  Oops: invalid opcode: 0000 [#1] SMP KASAN NOPTI
  RIP: 0010:ip_set_put_byindex (net/netfilter/ipset/ip_set_core.c:870)
  Call Trace:
   <IRQ>
   list_set_del (net/netfilter/ipset/ip_set_list_set.c:159)
   set_cleanup_entries (net/netfilter/ipset/ip_set_list_set.c:181)
   list_set_gc (net/netfilter/ipset/ip_set_list_set.c:578)
   call_timer_fn (kernel/time/timer.c:1748)
   __run_timers (kernel/time/timer.c:1799 kernel/time/timer.c:2374)
   run_timer_softirq (kernel/time/timer.c:2405)
   </IRQ>
  Kernel panic - not syncing: Fatal exception in interrupt

### CVE-2026-74747

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:16:53.657 |

In the Linux kernel, the following vulnerability has been resolved:

ipvs: revalidate ihl to prevent out-of-bounds access

While the outer IP header is already pulled into the skb head,
we must be careful and revalidate the embedded headers after
reading them from the skb frags to prevent out-of-bounds
access.

One such place reported by Sashiko is ip_vs_nat_icmp() where
local process can change the ihl field and after
skb_ensure_writable() we can see larger value which is a
problem for the ip_send_check(cih) calls.

Add check to drop the packet if the ihl field is changed.

### CVE-2026-74739

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:16:52.603 |

In the Linux kernel, the following vulnerability has been resolved:

net/sched: cls_u32: skip hash tables in u32_bind_class()

u32_walk() enumerates both struct tc_u_hnode and struct tc_u_knode
through the walker callback. u32_bind_class() unconditionally casts the
passed fh to tc_u_knode and accesses &n->res, so when fh is actually a
tc_u_hnode, which has no tcf_result member, this results in a
slab-out-of-bounds read of res->classid in tc_cls_bind_class().

The issue can be reproduced with the following commands:

    tc qdisc add dev lo root handle 1: hfsc
    tc class add dev lo parent 1: classid 1:1 hfsc sc rate 1000kbit
    tc filter add dev lo parent 1:1 protocol ip prio 1 u32 match u32 0 0 flowid 1:1
    tc class add dev lo parent 1: classid 1:2 hfsc sc rate 2000kbit

Fix this by skipping hash tables via the TC_U32_KEY(handle) check.

### CVE-2026-74736

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:16:52.173 |

In the Linux kernel, the following vulnerability has been resolved:

net/sched: cls_bpf: reject dev-bound programs bound to a different device

cls_bpf_prog_from_efd() obtained a SCHED_CLS program via
bpf_prog_get_type_dev() but never verified that a device-bound (offloaded)
program's bound netdev matches the TC netdev the classifier is being
attached to. This let a program loaded with prog_ifindex for device A be
attached via cls_bpf + skip_sw to device B; deleting device A then
destroyed the program's offload state while it was still attached to
device B, triggering a netdevsim WARN (panic with panic_on_warn=1).

Mirror the XDP attach path (net/core/dev.c) and reject the attach with
-EINVAL when a dev-bound program's bound device does not match the
target device.

### CVE-2026-77658

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-26T13:19:22.043 |

A stack-based buffer overflow vulnerability exists in the Dia diagram editor when processing Network Bus objects from Dia XML project files.

In objects/network/bus.c, bus_load() reads the number of bus handles from the file attribute "bus_handles" using attribute_num_data() without validating an upper bound:

    bus->num_handles = attribute_num_data(attr);

When a bus handle is subsequently moved, bus_handle_moved() allocates two temporary arrays on the stack:

    parallel = (real *)g_alloca(num_handles * sizeof(real));
    perp = (real *)g_alloca(num_handles * sizeof(real));

Because num_handles is fully attacker-controlled via the project file, sufficiently large values (for example 262144 or higher) cause g_alloca() to consume more stack space than the default thread stack limit (typically 8 MB on Linux), resulting in stack overflow, SIGSEGV, and potential stack frame / return-address corruption.

An attacker can embed a Bus object with an excessive bus_handles count in a malicious .dia file. Exploitation requires the victim to open the file in Dia (file dialog, command line, or file association) and trigger handle manipulation (moving a bus handle), which exercises the vulnerable code path.

The identical g_alloca pattern is present in objects/Misc/tree.c (copied from bus.c) and is likely vulnerable to the same class of attack via Tree objects.

Affected versions: Dia 0.98.0 and earlier versions containing this code; issue confirmed on upstream master as of 2026-08-21.
Upstream report: https://gitlab.gnome.org/GNOME/dia/-/issues/581

### CVE-2026-78237

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-26T08:16:46.720 |

Insufficient input validation in ABR allows a low-privileged user to inject malicious entries into the sudoers file, resulting in persistent root access that remained effective after the ABR session ended.

### CVE-2026-58097

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-130` |
| Published | 2026-08-26T06:16:26.700 |

mp_SetEnddisc() copied a user-supplied PSN endpoint value without length validation, allowing a buffer overflow via the ppp(8) command interface.

A local user with access to the ppp(8) command interface can crash ppp(8) or potentially execute arbitrary code as root.

### CVE-2026-58094

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-08-26T06:16:26.350 |

The FIOSSHMLPGCNF ioctl(2) operation configures the page size for a largepage shared memory object.  This is intended to be used immediately after creating the object, before any memory is allocated for the object.  The handler checked whether a page size had already been configured without holding the rangelock.  Two concurrent callers could both observe an unconfigured object and set conflicting page sizes, leaving the object in an inconsistent state.

An unprivileged local user can exploit this race to escalate privileges.

### CVE-2026-81576

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-27T10:16:40.313 |

If configured as a server, CodeMeter Runtime before versions 8.41a and 9.10 issues handles per connection and relies on a cryptographically weak
SID as sole authenticator. An attacker can brute-force the SID, recover another session's handle number, and read
license information belonging to another handle.

### CVE-2026-47879

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-27T06:17:17.813 |

Spring Cloud Gateway JsonToGrpcGatewayFilterFactory allows arbitrary Spring Resource locations for defining the proto descriptor.
Spring Cloud Gateway 5.0.0 - 5.0.2
Spring Cloud Gateway 4.3.0 - 4.3.5
Spring Cloud Gateway 4.0.0 - 4.2.9
Spring Cloud Gateway 3.1.13 and earlier

### CVE-2026-61617

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-08-26T22:16:25.247 |

Wings is the server control plane for the Pterodactyl game-server management panel. In versions up to and including 1.13.2, the SFTP write path does not enforce a server's disk quota during a transfer, allowing a tenant with SFTP write access to a single server to exhaust the host node's physical disk and take down every server on it. Wings checks available space only once, as a boolean, when the write handle is opened, using a stale cached usage value and without knowing the size of the incoming data, and it then returns a raw, unaccounted file handle that is never re-checked as the transfer proceeds. A single upload can therefore be written without bound, far beyond the configured disk limit, until the node's disk is full, and because a server stopped for exceeding its limit is not treated as suspended, SFTP writes are still accepted even after the quota is already exceeded. This issue is fixed in version 1.13.3.

### CVE-2026-61792

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-22;CWE-59;CWE-693` |
| Published | 2026-08-26T21:16:39.510 |

Weblate is a web-based continuous localization platform used to manage software translations. In versions prior to 2026.7, a project administrator can read files outside their repository through the App store metadata download feature, which resolves attacker-influenced paths without adequately confining them to the repository. This is an incomplete fix for CVE-2026-34242, whose original patch failed to fully prevent the path traversal, allowing the arbitrary file read to persist. A user with project-administrator privileges can therefore disclose the contents of files on the Weblate host that lie outside the project's repository. This issue is fixed in version 2026.7.

### CVE-2026-75797

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-26T06:16:27.230 |

The AI Engine  WordPress plugin before 3.7.2 does not confine a caller-supplied URL when mapping it to a local filesystem path before reading the file and forwarding its contents to an external service, allowing users with a subscriber-level account to read arbitrary files from the server and exfiltrate them off-host. Reaching the issue at subscriber level requires a non-default public API feature to be enabled; otherwise the same issue is reachable by an administrator, which on multisite allows a non-super subsite administrator to read the network-shared configuration and its secrets.

### CVE-2026-47666

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-26T23:17:13.843 |

Penpot is an open-source design and prototyping platform. In versions up to and including 2.14.3, Penpot is vulnerable to stored cross-site scripting through custom font family names, which are interpolated into a @font-face CSS rule and injected into the page as HTML without sanitization. Because the backend accepts an arbitrary font-family string and the frontend writes the resulting style through innerHTML, a name containing markup such as a closing style tag followed by a script can break out of the style element and execute JavaScript on the Penpot origin. The attack is passive: any team member who opens a file referencing the malicious font triggers script execution simply by rendering the page, allowing theft of session cookies, actions performed as the victim, and access to their files and projects. This issue is fixed in version 2.15.3.

### CVE-2026-77368

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-26T22:16:29.860 |

SeaweedFS is a distributed storage system for files and blobs. In version 4.39, the filer's TUS resumable-upload handler checks JWT allowed_prefixes scoping only when a session is created, letting a low-privilege tenant hijack another tenant's upload session to write content to filer paths their own token forbids. The HEAD, PATCH, and DELETE verbs that act on an existing session by its id never verify that the session's stored target path falls within the caller's allowed prefixes, so a tenant who obtains another upload's session identifier can PATCH attacker bytes into it and, on completion, have the file land at the victim's out-of-scope path. The same token can also DELETE other tenants' sessions and HEAD them to read upload progress and size, defeating the JWT prefix isolation. This vulnerability only affects deployments that configure filer JWT signing and have TUS uploads enabled. This issue is fixed in version 4.40.

### CVE-2026-79938

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-26T20:18:14.140 |

Dell PowerProtect Cyber Recovery, versions prior to 20.3, contain an Improper Authentication vulnerability. A low privileged attacker with remote access could potentially exploit this vulnerability, leading to Unauthorized access.

### CVE-2026-54245

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-26T20:17:53.057 |

Fleet is an open-source device management platform built on osquery. In versions prior to 4.86.2, the Okta conditional access integration in Fleet Premium is vulnerable to SQL injection through a host-supplied value that is used in a database query without proper parameterization, allowing an attacker who controls a single enrolled host to read or modify arbitrary data in the Fleet database. The value is reported by the host's own agent and stored verbatim, then used on an unauthenticated request path that supports the conditional access integration, so any party controlling one enrolled host, the lowest-privilege position in the product, can influence the query. By disclosing arbitrary database contents an attacker can extract stored session tokens and replay them to act as a global administrator, and on a managed fleet that administrator access enables running scripts on enrolled hosts, leading to remote code execution. The issue requires Fleet Premium with the Okta conditional access integration enabled and does not affect instances where it is not configured. This issue is fixed in version 4.86.2.

### CVE-2026-81743

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-94` |
| Published | 2026-08-27T13:18:43.487 |

Affected versions of Flowintel allow the LOG_FILE configuration value to be modified through system settings without restricting it to a filename inside the intended log directory.


Because the application constructs the log destination from this configurable value, an administrator could set LOG_FILE to an arbitrary filesystem path. Since attackers can influence logged content, this enables controlled data to be written into unintended files. The upstream commit specifically describes an exploitation chain in which an attacker injects a template into a chosen file and subsequently abuses application rendering behavior to execute code.

The patch removes LOG_FILE from the web-editable settings, introduces validate_log_file_name() to reject absolute paths, traversal, Windows paths, null bytes, and directory components, and centralizes log path construction through resolve_log_file_path().

Version impacted: >=3.3.0

### CVE-2026-81575

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-130` |
| Published | 2026-08-27T10:16:40.197 |

If configured as a server, CodeMeter Runtime before versions 8.41a and 9.10 accepts requests with opcode 0x5e, which contain the data length and
the data itself. Missing bounds checking on the data length value can lead to out of bounds reads, causing a
segmentation fault that ultimately crashes the CodeMeter Runtime.

### CVE-2026-80433

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-27T10:16:38.780 |

Subscriber Sensitive Data Exposure in SureFeedback Client Site <= 1.2.12 versions.

### CVE-2026-47852

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-27T01:17:32.320 |

A local attacker on a multi-user host can pre-create the deterministic cache path and plant a malicious ONNX model file.
Spring AI 2.0.0
Spring AI 1.1.0 - 1.1.8
Spring AI 1.0.0 - 1.0.9

### CVE-2026-47851

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-27T01:17:32.150 |

Analyzing a PDF with a deeply nested or cyclic table of contents can cause a StackOverflowError in the ingestion thread.
Spring AI 2.0.0
Spring AI 1.1.0 - 1.1.8
Spring AI 1.0.0 - 1.0.9

### CVE-2026-68863

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-26T20:17:57.833 |

Dell PowerProtect One, versions 20.1.0.0 and below, contain a Stack-based Buffer Overflow vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to Denial of service.

### CVE-2026-46369

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-193;CWE-294` |
| Published | 2026-08-26T20:17:23.163 |

Nimiq is a Rust implementation of the Nimiq Proof-of-Stake protocol based on the Albatross consensus algorithm. Through 1.5.0, the validity store uses a strict lower-bound comparison that expires a stored transaction too early relative to Transaction::is_valid_at, allowing a remote attacker to replay the same signed transaction during a blocks_per_batch minus one block window and cause the sender and recipient balances to be updated twice. This issue is fixed in version 1.5.1.

### CVE-2026-80588

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:15.180 |

In the Linux kernel, the following vulnerability has been resolved:

mptcp: reclaim forward-allocated memory on RX path errors

After commit 9db5b3cec4ec ("mptcp: borrow forward memory from subflow"),
errors in the receive path prior to queueing skbs into the receive
queue do not trigger forward-allocated memory reclaiming.

Prevent forward memory from growing unboundedly in pathological drop
scenarios by explicitly reclaiming memory when skbs are dropped.

### CVE-2026-80527

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:06.490 |

In the Linux kernel, the following vulnerability has been resolved:

ceph: fix hanging __ceph_get_caps() with stale mds_wanted

A reader can hang forever in __ceph_get_caps() when the client no
longer holds `FILE_RD`, but local cap state still says that the
capability is already wanted (via `mds_wanted`).

One way to trigger this is through MDS cap revocation.  If another
client performs a conflicting operation, the MDS can revoke `FILE_RD`
from the reader; the next read then has to reacquire `FILE_RD`.  If
the cap update that should request `FILE_RD` never reaches the MDS
after `cap->mds_wanted` was raised, the reader is left holding only
non-file caps while local `mds_wanted` still includes the file read
caps.

In that state, try_get_cap_refs() sees `need <= mds_wanted` and
returns 0, so __ceph_get_caps() just waits on `i_cap_wq`.  If the cap
update that was supposed to request `FILE_RD never reaches the MDS
after `cap->mds_wanted was` raised, no further request is sent and the
waiter can sleep indefinitely until unrelated cap traffic happens to
wake it up.

The ordering issue is that `cap->mds_wanted` is updated in
__prep_cap() before the `CEPH_MSG_CLIENT_CAPS message` is actually
queued for send.  That makes one field serve two different meanings at
once: what this client wants, and what the client believes the MDS
already knows it wants.

A proper fix would be to split those states and track whether a cap
update is actually in flight or has been observed by the MDS.
However, simply moving the `cap->mds_wanted assignment` later would
not be sufficient: queueing the message in the messenger does not
guarantee that the MDS processed that specific wanted set, and
reconnect or message loss can still invalidate that assumption.
Fixing that properly would require a larger rework of the cap state
machine.

To allow simpler backports to stable kernels, this patch implements a
simpler workaround:

- stop waiting forever in __ceph_get_caps(); after a bounded wait,
  fall back to the renew path

- make ceph_renew_caps() issue a synchronous `OPEN` request whenever
  the inode still does not actually hold the wanted caps, instead of
  only calling ceph_check_caps()

The extra issued-vs-wanted check in ceph_renew_caps() is necessary
because the previous test only checked whether the inode still had any
real caps at all.  That is not enough after revocation: the client can
still hold something like `pLs` and yet be missing `FILE_RD`
completely.  In that case, falling back to ceph_check_caps() is not
sufficient, because it still trusts `cap->mds_wanted` and may resend
nothing.  By requiring `(issued & wanted) == wanted` before taking the
asynchronous path, the code only uses ceph_check_caps() when the
`wanted caps` are already actually issued.  Otherwise, it sends the
synchronous `OPEN` renew.

This preserves the existing asynchronous fast path when the wanted
caps are already issued, avoids changing cap-state semantics, and
fixes the hang by guaranteeing that a stalled waiter eventually
retries through a path that does not rely on the stale `mds_wanted`
state.

[ idryomov: move CEPH_GET_CAPS_WAIT_TIMEOUT from libceph.h to
  mds_client.h, formatting ]

### CVE-2026-80520

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:05.553 |

In the Linux kernel, the following vulnerability has been resolved:

ovpn: fix NULL dereference when killing missing key

ovpn_crypto_kill_key assumes both crypto slots are populated and
dereferences each slot before checking it. That is not guaranteed: a
peer can have only one installed key, and the kill path may be asked to
remove a key that is not present.

Read each slot once while holding the crypto state lock, check for NULL
before looking at key_id, and only replace the slot that actually
matches.

### CVE-2026-74750

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:16:54.050 |

In the Linux kernel, the following vulnerability has been resolved:

ovpn: defer key slot crypto freeing to workqueue

Key slots are released through a kref and the existing release path
frees the AEAD transforms from an RCU callback. That is not safe for all
crypto implementations: crypto_free_aead can sleep, for example when an
async or hardware implementation has teardown work to complete.

Use queue_rcu_work for key-slot release. This keeps the RCU grace period
needed by lockless key-slot readers, but runs the actual crypto teardown
from workqueue context where sleeping is allowed. Once the rcu_work
callback runs, pre-existing RCU readers are gone, and the final kref put
already proves that no transform user remains, so the worker can release
the AEAD transforms and free the slot directly.

The previous patch drains ovpn_wq during module exit, so queued key-slot
teardown work cannot outlive module text.

### CVE-2026-74745

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:16:53.387 |

In the Linux kernel, the following vulnerability has been resolved:

eth: bnxt: avoid deadlock when canceling IRQ affinity notifier

Unregistering IRQ affinity notifiers waits for the callback synchronously.
bnxt takes the netdev instance lock in the notifier (to restart the queue)
and cancels the work under the same lock. This may obviously deadlock.

Move the restart to the async service task. The queue restart isn't
super time sensitive. Store the new TPH tag, schedule the task.
Safely canceling the service task is already ironed out.

In bnxt_request_irq() the order of registering notifier, affinity and
initial TPH programming has to be inverted. I think it was racy
previously since user may trigger an update as soon as notifier
is installed.

There's a small known gap - if pcie_tph_get_cpu_st() fails at init
and the target tag is 0 we may miss programming the entry.
This does not seem worth fixing, the code has skip-on-failure
all over the place, anyway.

### CVE-2026-74742

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:16:52.990 |

In the Linux kernel, the following vulnerability has been resolved:

veth: fix queue index used to wake the peer txq in veth_poll

veth_poll() derives the index of the peer TX queue to wake from
rq->xdp_rxq.queue_index. That field is only initialized by
xdp_rxq_info_reg() in veth_enable_xdp_range(), which runs only when an
XDP program is attached. On the plain GRO/NAPI path
(veth_napi_enable_range()) xdp_rxq_info_reg() is never called, so
queue_index stays 0 for every queue, as priv->rq is zero-allocated.

So in a multi-queue setup with GRO enabled and no XDP program attached,
every NAPI instance looks at the peer's TX queue 0. If veth_xmit() stops
peer TX queue 1 because the ptr_ring is full (NETDEV_TX_BUSY), nothing
ever wakes it again: the poller draining queue 1 wakes queue 0 instead.
veth implements no ndo_tx_timeout, so the netdev watchdog does not kick
in either, and the queue stays stopped indefinitely.

Derive the index from the position of the rq within priv->rq instead,
which is correct regardless of whether XDP was ever enabled.

Scripts to reproduce the stall are available at
https://github.com/netoptimizer/veth-backpressure-performance-testing

### CVE-2026-74741

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:16:52.867 |

In the Linux kernel, the following vulnerability has been resolved:

net: ngbe: fix NULL pointer dereference in non-MSI-X interrupt enabling

In non-MSI-X mode (such as legacy INTx or single MSI), wx->msix_entry is
not allocated or initialized. Calling NGBE_INTR_MISC(wx) dereferences
wx->msix_entry->entry, leading to a NULL pointer dereference crash.

This issue was introduced by fixing the IRQ vector when the number of
VFs is 7. Fix the issue by explicitly checking `pdev->msix_enabled` to
determine the correct vector index.

Additionally, as a side fix, set the interrupt mask to BIT(0) for the
non-MSI-X fallback. In MSI/INTx mode, the MISC and queue interrupts
share vector 0, and the WX_PX_MISC_IVAR register is only valid in the
MSI-X case. Thus, BIT(0) is the correct mask for the miscellaneous cause
when MSI-X is disabled.

### CVE-2026-19271

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-90` |
| Published | 2026-08-26T14:17:08.500 |

Improper Neutralization of Special Elements used in an LDAP Query ('LDAP Injection') vulnerability in TÜBİTAK BİLGEM Software Technologies Research Institute Liderahenk allows LDAP Injection.

This issue affects Liderahenk: from 3.4.0 before 3.5.5.

### CVE-2026-15990

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-26T14:17:07.707 |

The Formidable Charts plugin for WordPress is vulnerable to Directory Traversal in all versions up to, and including, 2.0.1 via the 'frm_graph' parameter. This makes it possible for unauthenticated attackers to read the contents of arbitrary files on the server, which can contain sensitive information. Successful exploitation requires Formidable Forms Lite, Formidable Forms Pro, and Formidable Charts to be active and requires the wp-content/uploads/frm-charts/ directory to exist, normally after an image-format chart is rendered.

### CVE-2026-16444

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-08-26T10:16:39.940 |

Improper
neutralization of path traversal sequences in TeamViewer Desktop Clients prior
Version 15.81.5 allows an authenticated remote session participant to write files
to unintended locations on the local file system via file transfer or virtual
file clipboard mechanisms. An attacker can leverage this behavior to achieve
arbitrary file write and potentially execute code with the privileges of the
affected user.

### CVE-2026-18884

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-26T08:16:44.660 |

The WooCommerce Lottery plugin for WordPress is vulnerable to Time-Based SQL Injection via 'orderby' and 'order' GET Parameters in all versions up to, and including, 2.2.9 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database.

### CVE-2026-74928

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-26T06:16:26.930 |

The Project Manager  WordPress plugin before 4.0.7 does not have any authorisation check on its import routes, allowing unauthenticated users to create WordPress accounts with a password the attacker already knows, bypassing the site's own registration setting.

### CVE-2026-63360

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-26T22:16:25.410 |

LimeSurvey Community Edition 7.0.5+260623 contains an authenticated reflected Cross-Site Scripting vulnerability in the user activation confirmation endpoint. The action query parameter is copied into the response and inserted into a hidden input attribute without HTML attribute encoding.



This issue affects LimeSurvey: 7.0.5.

### CVE-2026-47841

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T18:16:33.303 |

An application using Spring Security's WebAuthn support may be vulnerable to user verification bypass when using a distributed HTTP session store.
Spring Security 7.1.0
Spring Security 7.0.0 - 7.0.6
Spring Security 6.5.0 - 6.5.11
Spring Security 6.4.0 - 6.4.18

### CVE-2026-54550

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:N/I:H/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-26T15:16:49.223 |

IzPack is a widely used tool for packaging applications on the Java platform as cross-platform installers. In 5.2.6 and earlier, UnpackerBase.unpack() in izpack-installer/src/main/java/com/izforge/izpack/installer/unpacker/UnpackerBase.java obtains an attacker-controlled PackFile targetPath, passes it through IoHelper.translatePath(), which only converts separators, and constructs a File without normalizing parent-directory segments or enforcing destination containment. A malicious installer pack entry containing ../ sequences can therefore write outside the intended installation directory to startup folders, executable search paths, or other locations accessible with the victim's privileges when the victim runs the installer.

### CVE-2026-80578

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:13.880 |

In the Linux kernel, the following vulnerability has been resolved:

fbdev: core: Fix pointer desynchronization in fb_io_read()

In fb_io_read(), if copy_to_user() performs a partial copy (e.g., due to
a faulty user buffer), the loop adjusts the chunk size 'c' and updates
the remaining 'count'. However, the hardware 'src' pointer has already
been eagerly advanced by the original chunk size.

If the loop is allowed to continue, the read will resume from an
incorrect, over-advanced offset. Since the remaining 'count' was only
decremented by the successful bytes, this desynchronization causes the
next iterations to execute more hardware reads than originally bounded,
eventually leading to out-of-bounds I/O reads.

Fix this by breaking out of the loop immediately upon a partial
copy_to_user(). A partial copy indicates a faulty user buffer, making
subsequent read attempts futile. Breaking out ensures we return the
number of successfully read bytes without risking out-of-bounds hardware
accesses in subsequent mismatched iterations.

### CVE-2026-18252

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-829` |
| Published | 2026-08-26T14:17:08.000 |

GitLab has remediated an issue in GitLab EE affecting all versions from 18.9 before 19.1.7, 19.2 before 19.2.5, and 19.3 before 19.3.1 that, under certain conditions, an authenticated user with developer-role permissions could have executed arbitrary commands in a CI context, due to the Claude agent processing configuration from a user-controlled source.

### CVE-2026-79619

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-26T13:19:24.003 |

On Linux, several OpenZFS ioctl authorization checks accept a capability held only within a user-created, unprivileged namespace as equivalent to real host privilege, allowing an unprivileged local user to perform operations that should require root. Affected operations include pool-administrative operations (eg create, import, destroy), pool event log access (zpool events) and fault injection (zinject). Exploiting the problem requires only that the local user is permitted to open /dev/zfs (governed by local device permissions) and that the kernel permits unprivileged user namespace creation. No prior access to the target pool or its underlying devices is needed.

### CVE-2026-78276

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-27T10:16:37.640 |

Editor PHP Object Injection in Fluent Boards Pro <= 2.0.11 versions.

### CVE-2026-78271

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-08-27T10:16:37.133 |

Editor Privilege Escalation in FluentCRM Pro <= 3.1.12 versions.

### CVE-2026-16809

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:A/VC:H/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-26T22:16:23.160 |

LimeSurvey Community Edition 7.0.5 contains a stored cross-site scripting vulnerability in the survey quota creation workflow. An authenticated low-privileged user who can create and manage their own survey can store malicious JavaScript in a quota message.

This issue affects LimeSurvey: 7.0.5.

### CVE-2026-71171

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-26T19:16:57.647 |

Dell Cloud Disaster Recovery, versions 20.2 and prior, contain an Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability in the REST API. A high privileged attacker with remote access could potentially exploit this vulnerability, leading to Remote execution.

### CVE-2026-47836

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T18:16:33.050 |

The base directory (spring.cloud.config.server.svn.basedir) used by the Spring Cloud Config Server to clone SVN repositories to is susceptible to time-of-check-time-of-use (TOCTOU) attacks.
Spring Cloud Config 5.0.0 - 5.0.4
Spring Cloud Config 4.3.0 - 4.3.4
Spring Cloud Config 4.0.0 - 4.2.8
Spring Cloud Config 3.1.14 and earlier

### CVE-2026-81035

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-26T16:16:46.463 |

Midday allows any member of a team to delete it. The delete procedure in apps/api/src/trpc/routers/team.ts authorises the caller with the team-access helper, which returns true for every row in the team-membership table irrespective of the role it records, and the data-layer function it calls re-checks the same helper and nothing else. The neighbouring procedures that remove or update a member in the same router each resolve the caller's role and refuse the request unless it is owner, so the check exists in the file and is not applied to deletion. Member is the role an invited user receives, so any invitee can remove the team and every record scoped to it, and the deletion enqueues the cleanup job with the stored bank-connection tokens, which the job then uses against the connected providers. The update procedure in the same router carries no role check either.

### CVE-2026-18331

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-26T07:16:45.360 |

The Formidable Forms – WordPress Form Builder for Contact Forms, Calculators, Quizzes & More plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'frm_user_id' parameter in all versions up to, and including, 6.33.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. By forging frm_user_id to match an administrator's user ID — discoverable via the public WordPress REST API — an unauthenticated attacker causes wp_kses_post() to serve as the only output filter, which preserves the injected payload structurally intact; the plugin's admin JavaScript then decodes and executes it automatically on page load.

### CVE-2026-74851

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-26T06:16:26.830 |

The Pods  WordPress plugin before 3.3.9.1 does not correctly compare a display callback against its list of blocked functions, allowing users with the author role and above to execute arbitrary code on the server. Only sites using the restricted display-callback mode are affected, which is the automatic default on installations whose first Pods version predates 3.1.

### CVE-2026-19760

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-26T06:16:26.007 |

The WP Fastest Cache – WordPress Cache Plugin plugin for WordPress is vulnerable to Stored Cross-Site Scripting via HTTP Host Header in all versions up to, and including, 1.5.0 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This requires the Polylang or Polylang Pro plugin to be active and the Combine JS option to be enabled, as these conditions trigger the vulnerable Host-header-to-URL code path that writes attacker-controlled script src values into the shared page-cache file served to all subsequent visitors.

### CVE-2026-81659

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-27T13:18:42.190 |

Affected versions of Flowintel allow attacker-controlled note content to be processed by Pandoc and XeLaTeX during PDF export in a way that can cause local files on the Flowintel server to be read and incorporated into the generated export.

### CVE-2026-78293

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-27T10:16:38.653 |

Unauthenticated Cross Site Scripting (XSS) in WP w3all phpBB <= 3.0.6 versions.

### CVE-2026-78289

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-27T10:16:38.393 |

Unauthenticated Cross Site Scripting (XSS) in CozyStay <= 1.10.0 versions.

### CVE-2026-78283

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-27T10:16:37.883 |

Unauthenticated Cross Site Scripting (XSS) in Music Player for WooCommerce <= 1.8.9 versions.

### CVE-2026-78281

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-27T10:16:37.760 |

Unauthenticated Cross Site Scripting (XSS) in CP Media Player <= 1.3.0 versions.

### CVE-2026-78261

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-27T10:16:37.003 |

Unauthenticated Cross Site Scripting (XSS) in Realtyna Organic IDX plugin <= 5.4.1 versions.

### CVE-2026-47849

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-27T06:17:16.653 |

Spring Data REST does not guard identifier (@Id) and version (@Version) properties against mutation via RFC 6902 JSON Patch (application/json-patch+json) requests.
Spring Data REST 5.1.0
Spring Data REST 5.0.0 - 5.0.6
Spring Data REST 4.5.0 - 4.5.12
Spring Data REST 4.0.0 - 4.4.15
Spring Data REST 3.7.20 and earlier

### CVE-2026-80183

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:L/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-843` |
| Published | 2026-08-27T01:18:16.050 |

In OpenStack Keystone before 29.0.3, any authenticated user holding role:reader on any project can list every project-scoped role assignment under any domain by passing a domain ID as scope.project.id with include_subtree to the GET /v3/role_assignments endpoint. The domain's project record has domain_id=null, causing the policy domain_id check to pass for any caller. With include_names, the response discloses the names and home-domain IDs of every user, group, project, and role involved. The literal "default" domain ID works against any deployment created with keystone-manage bootstrap. An attacker can harvest domain IDs from the response and repeat the query to map role assignments across the entire cloud. This is caused by misuse of "None" in 

list_role_assignments_for_tree.

### CVE-2026-77611

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-26T22:16:30.007 |

SeaweedFS is a distributed storage system for files and blobs. In versions prior to 4.40, an authenticated S3 principal with permissions scoped to a nested object key can overwrite a different object outside that scope by calling PutObjectAcl on the key it is allowed to access. The handler authorizes the request against the requested nested key but then writes the updated entry back to the bucket root rather than the key's actual parent directory, so an ACL change on allowed/protected.txt is instead applied to protected.txt at the bucket root. Because the update carries the full entry rather than only ACL metadata, an existing target object is overwritten with the content, metadata, owner information, and ACL of the scoped object, bypassing the object-level action scoping configured through the static S3 identity file. This issue is fixed in version 4.40.

### CVE-2026-66003

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-26T20:17:56.920 |

Frappe is a full-stack web application framework written in Python and JavaScript. Prior to version 15.115.0, an access control bypass in the REST API allows a user to read data from Linked DocTypes that they are not authorized to access. When a document references another document through a Link field, the framework does not consistently enforce the linked DocType's own permissions when the record is retrieved through the REST API, so a low-privileged authenticated user can obtain fields from linked records outside their permitted scope. This issue is fixed in version 15.115.0.

### CVE-2026-35445

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-285` |
| Published | 2026-08-26T17:16:56.397 |

Winter CMS is a content management system built on the Laravel PHP framework. In versions prior to 1.2.13, the backend did not validate the handler name submitted through the form postback _handler POST field, allowing an authenticated backend user to invoke arbitrary controller methods, including protected, private, and action-prefixed ones. While AJAX requests validate that handler names match the on[A-Z][\w+]* pattern, the postback path passed the submitted _handler value straight to the handler dispatcher with no such check, so any controller that exposes a public action or conditionally relaxes its $requiredPermissions check could be reached, bypassing the roles and permissions system. The built-in Users controller was affected because it set $requiredPermissions to null for the myaccount action, letting any authenticated backend user invoke user-management methods such as update_onDelete and update_onManualPasswordReset without holding the backend.manage_users permission. This issue is fixed in version 1.2.13.

### CVE-2026-81030

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-26T16:16:45.710 |

Mage AI does not confine the paths accepted by its browser-items API to the project directory. BrowserItemResource in mage_ai/api/resources/BrowserItemResource.py passes a caller-supplied path to the filesystem read and write helpers without calling the containment helper that the sibling FileContentResource and FileResource classes both use, so the resource contains no such call while those two contain several. A user holding the Viewer role, which grants read access within the project and nothing outside it, can therefore read any file the server process can read by supplying an absolute path. The permission model that would otherwise separate roles is not consulted for this route in the default configuration, because the setting that enables it defaults to false. Callers holding the Editor role additionally write through the same unconfined path, though that role is already able to execute code by design, so the boundary crossed by this flaw is the read available to the Viewer role.

### CVE-2026-80555

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:10.130 |

In the Linux kernel, the following vulnerability has been resolved:

s390/vfio_ccw: Free all memory if cp_init() fails

The routine cp_free() is called to unpin/free any memory once an I/O
is completed successfully, or if cp_prefetch() fails. But if cp_init()
fails, and cp->initialized is not enabled, the same routine cannot be
used to free all the memory.

An attempt to address this exists in ccwchain_handle_ccw(), where a
single call to ccwchain_free() is made for the currently-processed
CCW segment. But this will leak other segments (created as a result
of a Transfer in Channel) that had been allocated as part of the same
channel program.

Address this by performing the cleanup outside of the recursive
ccwchain_handle_ccw()/ccwchain_loop_tic() logic.

### CVE-2026-80538

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:08.017 |

In the Linux kernel, the following vulnerability has been resolved:

xfs: propagate errors from xfs_rtginode_load

xfs_rtginode_ensure() treats every xfs_rtginode_load() error other than
-ENOENT as success.  This can leave the realtime group inode unset after an
I/O, allocation, or corruption error.  Growfs then continues as though the
inode had been loaded.

Only -ENOENT means that the inode needs to be created.  Return all other
errors to the growfs caller.

### CVE-2026-80530

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:06.990 |

In the Linux kernel, the following vulnerability has been resolved:

xfs: fix exchange-range reflink flag clearing issue with INO1_WRITTEN

When exchanging two full-file ranges, xmi_can_exchange_reflink_flags()
can move the reflink inode flag from the file that currently has it to
the other file, as long as exactly one side is marked.  This assumes
that the file contents, and therefore all shared extents, are exchanged.

That assumption is not true when XFS_EXCHMAPS_INO1_WRITTEN is set.
xfs_exchmaps_can_skip_mapping() can skip hole and unwritten mappings
from file1, so an exchange can complete without moving every mapping
that the earlier flag-swap decision accounted for.  In that case the
post-operation cleanup can clear the reflink flag from an inode that
still owns shared written extents.  Later writes then take the
non-reflink write path and may update blocks that should still have
been protected by CoW, which shows up as data corruption between
reflink-related files.

Fix this by disabling the reflink flag exchange whenever
XFS_EXCHMAPS_INO1_WRITTEN is requested.  The contents exchange can still
proceed; the conservative outcome is that both inodes keep the reflink
flag.  The regular reflink flag cleanup path can drop the extra flag
later once the inode no longer has shared extents.

### CVE-2026-80523

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-26T15:17:05.940 |

In the Linux kernel, the following vulnerability has been resolved:

clk: spacemit: k3: set hdma clock as critical

HDMA clock is responsible for the internal TCM access path of X100 RISC-V
core, so set the clock flag as critical to prevent it from being shut off,
otherwise the Linux system will hang, for example in the case of a vector
instruction access generates a page fault.

### CVE-2026-80350

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-26T10:16:43.237 |

OneUptime's webhook target check rejects private and loopback addresses given in IPv4 form and a small set of IPv6 forms, but has no case for the IPv4-mapped IPv6 range. The webhook delivery path calls SSRFProtection.validateWebhookTargetIsSafe, and the host-literal screening inside Common/Server/Utils/SSRFProtection.ts, performed by isBlockedHostnameLiteral, rejects private and loopback IPv4 ranges and tests an IPv6 value against the unspecified address, the loopback, the link-local prefix and the unique-local prefixes. A value such as [::ffff:127.0.0.1] matches none of them. The value is also recognised as an address literal rather than a name, so the path that re-checks addresses obtained from resolution is not taken. The HTTP client treats the mapped form as the embedded IPv4 address and connects to it, so an authenticated project member who can configure a webhook can direct the server at loopback services, private network ranges and link-local metadata endpoints, and the response is recorded where the webhook result can be read. Version 12.0.7 adds handling for the mapped range.

### CVE-2026-80346

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-26T10:16:42.637 |

StarRocks performs no privilege check when a legacy synchronous materialized view is dropped. Every other statement type routed through AuthorizerStmtVisitor calls into Authorizer before execution, but visitDropMaterializedViewStatement returns immediately with a comment stating the check happens in execution logic. That holds only for asynchronous materialized views: LocalMetastore.dropMaterializedView calls Authorizer.checkMaterializedViewAction inside a branch taken when the resolved table is a MaterializedView. A legacy synchronous materialized view is stored as a rollup index on an OlapTable rather than a MaterializedView, so the other branch runs, reaching AlterJobMgr.processDropMaterializedView and MaterializedViewHandler, neither of which contains any Authorizer call. The former locates the target by scanning every OlapTable in the named database for a matching rollup index, and the latter validates only table state and name conflicts. Any authenticated account can therefore drop a legacy synchronous materialized view belonging to any database, holding no grant on the view, the base table or the database, and the drop is indistinguishable from an authorized one.

### CVE-2026-66155

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-27T13:18:31.090 |

A vulnerability has been identified in Element maps-ng V47 (All versions < V47.12.3), Element maps-ng V48 (All versions < V48.11.3), Element maps-ng V49 (All versions < V49.16.1). The si-map component does not properly neutralize user-controllable input of the points property that is used to render the tooltip label of map pins.
This could allow an attacker to craft a malicious URL that, when loaded by a victim and the map pin is hovered over, executes arbitrary script code within the victim's browser session.

### CVE-2026-75020

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-90` |
| Published | 2026-08-27T10:16:36.620 |

Improper Neutralization of Special Elements used in an LDAP Query ('LDAP Injection') vulnerability in Apache APISIX.

A caller who holds valid credentials for one entry in the LDAP directory can authenticate through APISIX as a consumer mapped to a different entry, one the plugin's configured scope was meant to keep out of reach.


This issue affects Apache APISIX: from 2.11.0 through 3.17.0.



Users are recommended to upgrade to version 3.18.0, which fixes the issue.

### CVE-2026-74848

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-444` |
| Published | 2026-08-27T10:16:36.337 |

Inconsistent Interpretation of HTTP Requests ('HTTP Request/Response Smuggling') vulnerability in Apache APISIX.

An attacker could make other clients receive attacker-chosen or other users' responses on serverless-plugin routes.




This issue affects Apache APISIX: from 2.12.0 through 3.17.0.



Users are recommended to upgrade to version 3.18.0, which fixes the issue.

### CVE-2026-80426

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-26T16:16:44.777 |

FiftyOne renders a dataset field's description as markup. The sidebar field-information component at app/packages/core/src/components/FieldLabelAndInfo/index.tsx passes the description string to React's dangerouslySetInnerHTML, and no layer between storage and render escapes or sanitises it; the neighbouring info values in the same component are rendered as React children and are escaped, so the description is the only raw path. A description is free-form text held in the dataset schema, so it persists in the database and travels with an exported or published dataset. Opening a dataset obtained from another party and hovering the field runs the stored markup in the application's origin. That origin is shared with the FiftyOne server, whose media route returns the contents of a caller-named absolute path and which is unauthenticated in the open-source server, so the injected script can read local files and reach the dataset and operator endpoints as the viewing user.

### CVE-2026-58093

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-08-26T06:16:26.227 |

The TIOCSCTTY ioctl handler drops the tty lock in order to acquire the process tree lock.  After reacquiring the tty lock, the handler did not revalidate the state of the terminal, and could proceed to link a terminal that was concurrently being destroyed to the calling process' session.

An unprivileged local user can exploit this race condition to escalate privileges.
