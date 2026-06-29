#!/usr/bin/env python3
"""
test_nvd_latest_fetch.py
NVD→CIRCLフォールバック付き nvd_latest_fetch.py のユニットテスト

テストケース:
  1. NVD成功 → DBに保存
  2. NVD失敗 → CIRCLフォールバック成功 → DBに保存
  3. NVD + CIRCL 両方失敗 → RuntimeError
  4. CIRCLのlast_tsフィルタリング（古いCVEは無視）
  5. CVSSはv3優先・v2フォールバック
  6. タイムスタンプファイルの書き込み
"""
import importlib
import json
import os
import sys
import sqlite3
import tempfile
import pytest
from unittest.mock import patch, MagicMock

# ── モジュール読み込み ─────────────────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(__file__))
import nvd_latest_fetch as M


# ── フィクスチャ ──────────────────────────────────────────────────────────────
@pytest.fixture
def tmp_env(tmp_path, monkeypatch):
    """一時ディレクトリで DB・タイムスタンプファイルを使うよう切り替える"""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(M, "DB", str(tmp_path / "nvd.db"))
    monkeypatch.setattr(M, "TS_FILE", str(tmp_path / "last_timestamp.txt"))
    return tmp_path


@pytest.fixture
def fresh_conn(tmp_env):
    conn = M.ensure_db()
    yield conn
    conn.close()


# ── NVDモックレスポンス ───────────────────────────────────────────────────────
def make_nvd_response(cve_id="CVE-2026-99999", score=8.5, total=1):
    return {
        "totalResults": total,
        "timestamp": "2026-06-24T15:00:00.000Z",
        "vulnerabilities": [
            {
                "cve": {
                    "id": cve_id,
                    "published": "2026-06-24T10:00:00.000",
                    "descriptions": [{"lang": "en", "value": "Test NVD vulnerability"}],
                    "metrics": {
                        "cvssMetricV31": [
                            {"cvssData": {"baseScore": score, "vectorString": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N"}}
                        ]
                    },
                    "weaknesses": [{"description": [{"value": "CWE-79"}]}],
                    "references": [{"url": "https://example.com/nvd"}],
                }
            }
        ],
    }


# ── CIRCLモックレスポンス ─────────────────────────────────────────────────────
def make_circl_response(cve_id="CVE-2026-88888", published="2026-06-24T12:00:00"):
    return [
        {
            "id": cve_id,
            "Published": published,
            "Modified": published,
            "summary": "Test CIRCL vulnerability",
            "cvss3": "7.8",
            "cvss3-vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N",
            "cvss": "6.5",
            "cvss-vector": "AV:N/AC:L/Au:N/C:P/I:P/A:P",
            "cwe": "CWE-89",
            "references": ["https://example.com/circl"],
        }
    ]


def mock_response(data, status=200):
    """requests.get の返り値モック"""
    m = MagicMock()
    m.status_code = status
    m.json.return_value = data
    m.raise_for_status = MagicMock()
    return m


# ─────────────────────────────────────────────────────────────────────────────
# テスト 1: NVD 成功パス
# ─────────────────────────────────────────────────────────────────────────────
def test_nvd_success(tmp_env, fresh_conn):
    """NVD APIが正常に応答したとき、CVEがDBに保存される"""
    nvd_data = make_nvd_response()

    with patch("requests.get", return_value=mock_response(nvd_data)):
        fetched, new, ts = M.run_nvd(fresh_conn, last_ts=None)

    assert fetched == 1
    assert new == 1
    assert ts == "2026-06-24T15:00:00.000Z"

    cur = fresh_conn.cursor()
    cur.execute("SELECT cve_id, cvss, description FROM cves WHERE cve_id='CVE-2026-99999'")
    row = cur.fetchone()
    assert row is not None
    assert row[1] == 8.5
    assert "NVD vulnerability" in row[2]


# ─────────────────────────────────────────────────────────────────────────────
# テスト 2: NVD 失敗 → CIRCL フォールバック成功
# ─────────────────────────────────────────────────────────────────────────────
def test_circl_fallback_on_nvd_failure(tmp_env):
    """NVDが全リトライ失敗した場合にCIRCLから取得してDBに保存される"""
    circl_data = make_circl_response()

    def side_effect(url, **kwargs):
        if "nvd.nist.gov" in url:
            r = MagicMock()
            r.status_code = 503
            r.headers = {}
            r.url = url
            r.raise_for_status.side_effect = Exception("503")
            return r
        else:
            return mock_response(circl_data)

    with patch("requests.get", side_effect=side_effect):
        with patch("time.sleep"):          # リトライ待機をスキップ
            with patch("nvd_latest_fetch.MAX_RETRIES", 1):
                M.main()

    conn = sqlite3.connect(str(tmp_env / "nvd.db"))
    cur = conn.cursor()
    cur.execute("SELECT cve_id, cvss FROM cves WHERE cve_id='CVE-2026-88888'")
    row = cur.fetchone()
    conn.close()

    assert row is not None, "CIRCLフォールバックでCVEが保存されていない"
    assert row[1] == 7.8, f"CVSS v3が優先されていない: {row[1]}"


# ─────────────────────────────────────────────────────────────────────────────
# テスト 3: NVD + CIRCL 両方失敗 → RuntimeError
# ─────────────────────────────────────────────────────────────────────────────
def test_both_fail(tmp_env):
    """NVDもCIRCLも失敗した場合、RuntimeErrorが発生する"""
    import requests as req_mod

    def always_fail(url, **kwargs):
        r = MagicMock()
        r.status_code = 503
        r.headers = {}
        r.url = url
        # NVD は status_code チェックで処理、CIRCL は raise_for_status で例外
        r.raise_for_status.side_effect = req_mod.exceptions.HTTPError("503")
        return r

    with patch("requests.get", side_effect=always_fail):
        with patch("time.sleep"):
            with patch("nvd_latest_fetch.MAX_RETRIES", 1):
                with pytest.raises(RuntimeError, match="Both NVD and CIRCL failed"):
                    M.main()


# ─────────────────────────────────────────────────────────────────────────────
# テスト 4: CIRCLのlast_tsフィルタリング
# ─────────────────────────────────────────────────────────────────────────────
def test_circl_filters_old_cves(tmp_env, fresh_conn):
    """last_ts より古いCVEはCIRCLからの取得時にスキップされる"""
    last_ts = "2026-06-24T12:00:00.000Z"  # 正午

    items = [
        # 古いもの（スキップされるべき）
        {**make_circl_response("CVE-2026-OLD", "2026-06-24T10:00:00")[0]},
        # 新しいもの（保存されるべき）
        {**make_circl_response("CVE-2026-NEW", "2026-06-24T13:00:00")[0]},
    ]

    with patch("nvd_latest_fetch.circl_fetch", return_value=items):
        fetched, new, _ = M.run_circl(fresh_conn, last_ts=last_ts)

    assert fetched == 1, f"新しいCVEのみ処理されるべき: fetched={fetched}"
    assert new == 1

    cur = fresh_conn.cursor()
    cur.execute("SELECT cve_id FROM cves")
    ids = [r[0] for r in cur.fetchall()]
    assert "CVE-2026-NEW" in ids
    assert "CVE-2026-OLD" not in ids


# ─────────────────────────────────────────────────────────────────────────────
# テスト 5: CIRCL CVSS v3優先・v2フォールバック
# ─────────────────────────────────────────────────────────────────────────────
def test_circl_cvss_priority(tmp_env, fresh_conn):
    """cvss3がある場合はv3を使い、なければcvss(v2)を使う"""
    # v3あり → v3を使う
    item_v3 = make_circl_response()[0]
    s = M.circl_extract_summary(item_v3)
    assert s["cvss"] == 7.8, f"v3 (7.8) が使われるべき: {s['cvss']}"

    # v3なし → v2を使う
    item_v2 = {**item_v3}
    del item_v2["cvss3"]
    del item_v2["cvss3-vector"]
    s2 = M.circl_extract_summary(item_v2)
    assert s2["cvss"] == 6.5, f"v2 (6.5) にフォールバックすべき: {s2['cvss']}"


# ─────────────────────────────────────────────────────────────────────────────
# テスト 6: タイムスタンプの読み書き
# ─────────────────────────────────────────────────────────────────────────────
def test_timestamp_rw(tmp_env):
    """last_timestamp.txt が正しく読み書きされる"""
    assert M.read_ts() is None

    M.write_ts("2026-06-24T15:00:00.000Z")
    assert M.read_ts() == "2026-06-24T15:00:00.000Z"


# ─────────────────────────────────────────────────────────────────────────────
# テスト 7: NVD成功後にタイムスタンプが更新される
# ─────────────────────────────────────────────────────────────────────────────
def test_timestamp_written_after_nvd(tmp_env):
    """NVD正常終了後にlast_timestamp.txtが書き込まれる"""
    nvd_data = make_nvd_response()
    with patch("requests.get", return_value=mock_response(nvd_data)):
        M.main()

    ts = M.read_ts()
    assert ts == "2026-06-24T15:00:00.000Z"
