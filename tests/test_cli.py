"""CLI: version, anchors, advise, zones. JSON is five fields only."""

from __future__ import annotations

import json

from chronolock import __version__
from chronolock.anchors import TOP_30
from chronolock.cli import DEPRECATED_STATICCLOCK_LINE, main, staticclock_main
from chronolock.engine import OUTPUT_FIELDS, WINDOW_TEXT, ChronoLock
from chronolock.ui import LOOPBACK, make_server
from chronolock.zones import list_timezones


def test_cli_version(capsys) -> None:
    assert main(["version"]) == 0
    assert capsys.readouterr().out.strip() == f"chronolock {__version__}"


def test_cli_anchors(capsys) -> None:
    assert main(["anchors"]) == 0
    lines = [ln for ln in capsys.readouterr().out.splitlines() if ln.strip()]
    assert lines == list(TOP_30)
    assert len(lines) == 30


def test_cli_advise_plain(capsys) -> None:
    assert main(["advise", "--geo", "United States"]) == 0
    out = capsys.readouterr().out
    for key in OUTPUT_FIELDS:
        assert f"{key}:" in out
    low = out.lower()
    assert "because" not in low
    assert "confidence" not in low
    assert "score" not in low
    assert "08:30" in out
    assert "10:30" in out


def test_cli_advise_json_only_five_fields(capsys) -> None:
    assert main(["advise", "--geo", "Indiana", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert list(payload.keys()) == list(OUTPUT_FIELDS)
    blob = json.dumps(payload).lower()
    for word in ("because", "score", "confidence"):
        assert word not in blob


def test_cli_zones_readonly_does_not_change_advisory(capsys) -> None:
    clock = ChronoLock(nonce=b"zone-nonce-16byte")
    before = clock.advise("Sweden")
    assert main(["zones"]) == 0
    out = capsys.readouterr().out
    assert "Europe/Stockholm" in out
    after = clock.advise("Sweden")
    assert before.to_dict() == after.to_dict()


def test_list_timezones_has_iana_and_local_times() -> None:
    rows = list_timezones()
    assert len(rows) == 30
    for row in rows:
        assert "iana" in row and "/" in row["iana"]
        assert ":" in row["local_time"]
        assert row["local_date"]


def test_ui_rejects_non_loopback() -> None:
    import pytest

    with pytest.raises(ValueError, match="loopback"):
        make_server("0.0.0.0", 9)
    assert "127.0.0.1" in LOOPBACK


def test_ui_handler_advise_five_fields() -> None:
    import json
    import threading
    import urllib.request

    httpd = make_server("127.0.0.1", 0)
    port = httpd.server_address[1]
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=3) as resp:
            html = resp.read().decode("utf-8")
        assert "last-known geo" in html.lower() or "Last-known geo" in html
        assert "dialect" in html.lower()
        assert "ChronoLock" in html
        req = urllib.request.Request(
            f"http://127.0.0.1:{port}/api/advise",
            data=json.dumps({"geo": "United States"}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=3) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        assert list(payload.keys()) == list(OUTPUT_FIELDS)
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_ui_get_on_8851_contains_chronolock() -> None:
    import threading
    import urllib.request

    httpd = make_server("127.0.0.1", 8851)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        with urllib.request.urlopen("http://127.0.0.1:8851/", timeout=3) as resp:
            html = resp.read().decode("utf-8")
        assert "ChronoLock" in html
        assert "08:30" in html
        assert "10:30" in html
        assert "not a scheduler" in html.lower()
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_help_lists_ui_and_version() -> None:
    from chronolock.cli import _build_parser

    text = _build_parser().format_help()
    assert "ui" in text
    assert "version" in text
    assert "127.0.0.1:8851" in text or "chronolock ui" in text


def test_deprecated_staticclock_alias_prints_one_line_then_runs(capsys) -> None:
    assert staticclock_main(["version"]) == 0
    out = capsys.readouterr().out
    lines = out.splitlines()
    assert lines[0] == DEPRECATED_STATICCLOCK_LINE
    assert f"chronolock {__version__}" in out


def test_stagger_cli_names_windows(capsys) -> None:
    assert main(["stagger", "--geo", "United States", "--geo", "Japan"]) == 0
    out = capsys.readouterr().out
    assert "08:30" in out
    assert "10:30" in out
    assert "not a scheduler" in out.lower()
    assert "America/New_York" in out or "United States" in out
    assert "Asia/Tokyo" in out or "Japan" in out
