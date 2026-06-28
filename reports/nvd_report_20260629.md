# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-06-28 15:00 UTC
- **対象期間**: `2026-06-27T15:00:22.000Z` 〜 `2026-06-28T15:00:24.000Z`
- **重要CVE数**: 11 件（Critical 9.0+: 2 件 / High 7.0〜: 9 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
直近で公開された CVSS 7.0 以上の脆弱性は、**ネットワークサービスの遠隔コード実行・権限昇格**、**メディア処理ライブラリのメモリ破壊**、**CI/CD パイプラインやリモートデスクトップの認可バイパス** といった、攻撃者が直接システムを支配できるケースが目立ちます。特に **rsync デーモン** や **Docker バックエンドを利用した Gitea act_runner** など、インフラ層のコンポーネントで高深刻度（9.0 以上）のバッファオーバーフローが報告されており、即時のパッチ適用が求められます。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目理由・影響範囲 |
|-----|------|----------|-------------------|
| **CVE‑2024‑12084** | 9.8 (CVSS:3.1) | rsync デーモンのヒープバッファオーバーフロー | 攻撃者が任意のチェックサム長を送信するだけで、リモートから任意コード実行が可能。rsync は多くの Linux ディストリビューションでデフォルトでインストールされているため、広範囲に影響が及ぶ。 |
| **CVE‑2026‑58053** | 9.4 (CVSS:4.0) | Gitea act_runner (Docker バックエンド) のコンテナオプション不適切なマージ | `privileged: false` が指定されても `--pid=host` などの危険オプションが有効になるため、攻撃者がリモートでコンテナ内特権を取得できる。CI/CD 環境で自動化されたジョブが多数走る組織は即時対策が必要。 |
| **CVE‑2026‑58049** | 8.8 (CVSS:4.0) | FFmpeg RASC デコーダの行境界チェック不備 | 悪意ある RASC ビデオストリームをデコードすると、ヒープオーバーランが発生し、リモートコード実行やサービス停止が起こり得る。FFmpeg はメディアサーバ・ストリーミングサービスで広く利用されている。 |
| **CVE‑2026‑10643** | 8.7 (CVSS:3.1) | Zephyr OS の IP ソケット `recvmsg()` の ancilliary バッファ検証不備 | ローカル権限が低いプロセスから特権情報を上書きでき、情報漏洩＋権限昇格が可能。組み込みデバイス・IoT 向け OS での採用が増えているため、ファームウェア更新が必要。 |
| **CVE‑2026‑58054** | 8.6 (CVSS:4.0) | MyBB 1.8.40 の管理者権限委譲バイパス | 限定管理者がユーザー作成時に `Administrators` グループを選択でき、結果的にフル管理者権限取得が可能。Web フォーラムを運営している組織はすぐに権限設定の見直しとアップデートが必要。 |

---

## 3. 推奨アクション  

### 3.1 パッケージ・バージョンのアップデート
| 製品 / ライブラリ | 現行脆弱バージョン | 推奨バージョン (リリース日) | 備考 |
|-------------------|-------------------|----------------------------|------|
| **rsync** | ≤ 3.2.7 (多くのディストリビューションでデフォルト) | **3.2.8** 以上 | 公式パッチで `s2length` の長さチェックが追加。 |
| **act (Gitea act_runner)** | 0.262.0 | **0.263.0** 以上 | `container.options` のマージロジックが修正され、特権オプションが除外される。 |
| **ffmpeg** | ≤ 7.0 (含む libavcodec 7.0) | **7.1** 以上 | RASC デコーダの行境界チェックが強化。 |
| **Zephyr OS** | 3.5.0 以前 | **3.6.0** 以上 | `recvmsg()` の ancilliary バッファ検証が追加。 |
| **MyBB** | 1.8.40 | **1.8.41** 以上 | `verify_usergroup()` が管理者グループを除外するよう修正。 |
| **libssh2** | ≤ 1.11.1 | **1.11.2** 以上 | 公開鍵リストの再割当時にゼロ初期化、属性数の上限チェックが追加。 |
| **WordPress Frontend File Manager Plugin** | ≤ 23.6 | **23.7** 以上 | `wpfm_dir_path` のサニタイズ強化により任意削除が防止。 |
| **Windows Server Update Services (WSUS)** | Windows Server 2019/2022 の未パッチ版 | **2024‑03‑更新プログラム (KBxxxxxx)** | MS が提供する Elevation of Privilege 修正を適用。 |
| **RustDesk** | ≤ 1.2.3 | **1.2.4** 以上 | セッションフラグのクリアロジックが追加。 |

> **※ パッケージマネージャ例**  
> - Debian/Ubuntu: `apt-get update && apt-get install --only-upgrade rsync ffmpeg libssh2-1`  
> - RHEL/CentOS: `yum update rsync ffmpeg libssh2`  
> - Alpine: `apk upgrade rsync ffmpeg libssh2`  
> - Zephyr: ソースコードを取得し、`west update` で最新リリースへビルド。  
> - WordPress: 管理画面 → プラグイン → 更新、または手動で `frontend-file-manager.zip` を上書き。  

### 3.2 設定・運用上の緩和策
1. **rsync**: `rsyncd.conf` で `use chroot = true` を有効化し、外部からの直接アクセスを防止。  
2. **Gitea act_runner**: Docker バックエンド利用時は `privileged: false` に加えて `security_opt: ["no-new-privileges"]` を明示的に設定。  
3. **FFmpeg**: 信頼できないメディアファイルのデコードはサンドボックス化（`firejail` など）して実行。  
4. **MyBB**: 管理者権限委譲機能を無効化し、`Administrators` グループの `gid` を非表示にする。  
5. **libssh2**: 公開鍵取得時に `SSH2_REALLOC` 後のメモリを `memset` でクリアするパッチを適用、または 1.11.2 以降に更新。  
6. **WordPress**: プラグインのファイル削除機能は管理者権限のみ許可し、`wpfm_dir_path` パラ

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2024-12084

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2025-01-15T14:16:35.363Z |

A heap-based buffer overflow flaw was found in the rsync daemon. This issue is due to improper handling of attacker-controlled checksum lengths (s2length) in the code. When MAX_DIGEST_LEN exceeds the fixed SUM_LENGTH (16 bytes), an attacker can write out of bounds in the sum2 buffer.

### CVE-2026-58053

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-06-28T02:16:32.420 |

Gitea act_runner with the Docker backend (through act 0.262.0) passes a workflow's container.options string to the Docker job container's HostConfig and, when configured with privileged: false, forces only the Privileged flag off while merging options such as --pid=host, --cap-add, and --security-opt unchanged. A user who can run a workflow on a Docker-backed runner can create a job container with host namespaces and broad capabilities and escape to the host as root despite privileged mode being disabled.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-58049

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-06-28T02:16:30.477 |

FFmpeg's RASC video decoder (decode_dlta in libavcodec/rasc.c) performs 32-bit reads and writes at the row cursor before the NEXT_LINE row-boundary check and validates the DLTA region in pixel rather than byte units, so a DLTA run on a PAL8 frame can access several bytes past the row allocation. A crafted media stream using the RASC FourCC, decoded by libavcodec, triggers a bitstream-controlled out-of-bounds heap write and adjacent out-of-bounds read, leading to memory corruption.

### CVE-2026-10643

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:L/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-06-28T00:16:24.637 |

Zephyr's IP socket recvmsg() implementation (subsys/net/lib/sockets/sockets_inet.c, insert_pktinfo()) validated the user-supplied ancillary (msg_control) buffer using only the payload length (msg-msg_controllen < pktinfo_len) before writing a full control message consisting of an aligned cmsg header plus the payload. Because the check omitted the cmsg header size, a control buffer whose length falls in the under-checked window (e.g. 16-27 bytes for IPv4 IP_PKTINFO on a 64-bit target, where a single element actually occupies 28 bytes) passes the guard yet causes a fixed-size out-of-bounds write of up to one cmsg header (~12 bytes) past the end of the buffer. Under CONFIG_USERSPACE the recvmsg verifier allocates a kernel-heap copy of the control buffer sized to msg_controllen and runs the implementation against it, so the overflow corrupts kernel heap memory and is triggerable from an unprivileged userspace thread; in supervisor mode it corrupts the caller's buffer. The path is reachable on a UDP/IP socket with IP_PKTINFO/IPV6_RECVPKTINFO (or hoplimit/timestamping) enabled when the application calls recvmsg() with an undersized control buffer and a datagram is received; part of the overwritten bytes (the destination IP in ipi_addr) is influenced by the received packet. The fix makes the capacity check use NET_CMSG_SPACE(pktinfo_len) (aligned header + aligned data) and returns -ENOMEM when the buffer is too small. Affected: v3.6.0 through v4.4.0.

### CVE-2026-58054

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-06-28T02:16:32.550 |

MyBB 1.8.40 does not restrict which usergroup a limited Admin Control Panel user may assign when creating or editing users; the user module offers the Administrators group (gid 4) and its datahandler's verify_usergroup() unconditionally returns true. An admin holding only the delegated user-management permission can assign the Administrators group to an account and escalate to the full Administrator permission set.

### CVE-2026-58051

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-908` |
| Published | 2026-06-28T02:16:32.153 |

libssh2 through 1.11.1 grows its publickey list with SSH2_REALLOC but does not zero-initialize new entries before parsing populates them, so a parse failure reaching the cleanup path leaves libssh2_publickey_list_free operating on an uninitialized entry. A malicious SSH server offering the publickey subsystem can use a malformed response to make cleanup free an uninitialized, attacker-influenceable attrs pointer in a connecting libssh2 client.

### CVE-2026-58050

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:L/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-06-28T02:16:32.017 |

libssh2 through 1.11.1 reads an attacker-controlled 32-bit attribute count from a publickey-subsystem response and uses it in the allocation num_attrs * sizeof(libssh2_publickey_attribute) without bounds checking, so on 32-bit platforms the multiplication overflows to an undersized buffer. A malicious SSH server can then drive the attribute-parsing loop to write past the allocation, causing a heap buffer overflow in a connecting libssh2 client.

### CVE-2026-8095

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-06-28T00:16:25.180 |

The Frontend File Manager Plugin plugin for WordPress is vulnerable to Authenticated Arbitrary File Deletion in versions up to and including 23.6. This is due to a case-sensitive bypass of the wpfm_dir_path parameter sanitization in the wpfm_file_meta_update AJAX handler, where supplying WPFM_DIR_PATH in uppercase evades the unset check and is normalized to wpfm_dir_path by sanitize_key() during update_post_meta(), allowing an attacker to overwrite the stored file path with an arbitrary filesystem path that is then passed directly to unlink() in delete_file_locally() without any directory containment validation. This makes it possible for authenticated attackers with Subscriber-level access to delete arbitrary files on the server, including sensitive files such as wp-config.php, potentially leading to full site takeover.

### CVE-2023-35317

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H/E:U/RL:O/RC:C` |
| Weaknesses | `CWE-502` |
| Published | 2023-07-11T17:02:36.983Z |

Windows Server Update Service (WSUS) Elevation of Privilege Vulnerability

### CVE-2026-10646

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-06-28T05:16:21.083 |

Zephyr's BSD-sockets getaddrinfo() implementation (subsys/net/lib/sockets/getaddrinfo.c) passes a pointer to a stack-allocated state object (struct getaddrinfo_state ai_state) as the user_data of an asynchronous DNS resolver query. The socket layer waits on a semaphore with a timeout deliberately set slightly longer than the resolver's own per-query timeout. When that semaphore wait nonetheless times out (-EAGAIN) - which can occur when the resolver's timeout work is delayed by workqueue contention, or in the documented multi-retry configuration where CONFIG_NET_SOCKETS_DNS_TIMEOUT exceeds CONFIG_NET_SOCKETS_DNS_BACKOFF_INTERVAL - the pre-fix code retries the query (goto again) without cancelling the previous one and without resetting the semaphore. The previous query slot remains active in the resolver with its callback and the stack pointer as user_data, and ai_state-dns_id is overwritten so the stale query can no longer be cancelled. A subsequent DNS response delivered over UDP and matched by its 16-bit transaction id (in dispatcher_cb()/dns_read()), or the resolver's own delayed query-timeout work, then invokes dns_resolve_cb() against the now out-of-scope stack frame, writing through the stale pointer (state-status, state-idx, state-ai_arr[], and k_sem_give()). Because the triggering response is network-delivered and its 16-bit id is spoofable/replayable by an on- or off-path attacker, this is a network-influenceable use-after-return that can corrupt reused stack memory, leading to crashes/denial of service or memory corruption. The fix cancels the timed-out query by name and type before retrying and resets the local semaphore, eliminating the stale callback path. Affected: Zephyr v4.0.0 through v4.4.0.

### CVE-2026-58056

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-06-28T02:16:32.860 |

RustDesk gates incoming control messages on per-capability flags rather than on the session's authorized connection type, and a file-transfer session does not clear those flags. A peer holding only a valid FileTransfer authorization can inject keyboard and mouse input and reach the unguarded screenshot and display-capture handlers, acting outside its granted scope.
