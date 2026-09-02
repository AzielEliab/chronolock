"""Doctor speaks in plain words and does not persist."""

from __future__ import annotations

import json

from chronolock.cli import main
from chronolock.doctor import collect_results, run_doctor


def test_doctor_passes_plain_words(capsys) -> None:
    assert main(["doctor"]) == 0
    out = capsys.readouterr().out
    assert "Aziel Eliab" in out
    assert "Good." in out
    assert "does not post" in out.lower()
    assert "doctor passed" in out
    assert "StaticClock" in out or "staticclock" in out.lower()


def test_doctor_json_payload(capsys) -> None:
    assert run_doctor(as_json=True) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["ok"] is True
    assert payload["author"] == "Aziel Eliab"
    assert payload["network"] is False
    assert "plain" in payload
    assert "Aziel Eliab" in payload["plain"]
    names = [c["name"] for c in payload["checks"]]
    assert "identity" in names
    assert "json import/export" in names
    assert "advise" in names


def test_collect_results_has_plain_per_check() -> None:
    payload = collect_results()
    assert payload["ok"] is True
    for row in payload["checks"]:
        assert row["plain"].startswith("Good.")
