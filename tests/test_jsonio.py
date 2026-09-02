"""Import/export JSON without a hidden store."""

from __future__ import annotations

import json
from pathlib import Path

from chronolock.cli import main
from chronolock.jsonio import export_json, forget_imported, import_json, last_imported


def test_import_export_roundtrip_no_hidden_store(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    src = tmp_path / "in.json"
    out = tmp_path / "out.json"
    src.write_text(json.dumps({"geo": "Indiana", "ok": True}), encoding="utf-8")
    rec = import_json(src)
    assert rec["ok"] is True
    assert rec["author"] == "Aziel Eliab"
    rec2 = export_json(out)
    assert rec2["ok"] is True
    doc = json.loads(out.read_text(encoding="utf-8"))
    assert doc["author"] == "Aziel Eliab"
    assert doc["product"] == "ChronoLock"
    assert doc["payload"]["geo"] == "Indiana"
    names = {p.name for p in tmp_path.iterdir()}
    assert ".chronolock-state.json" not in names
    assert ".chronolock" not in names
    forget_imported()
    assert last_imported() is None


def test_cli_import_export(tmp_path: Path, monkeypatch, capsys) -> None:
    monkeypatch.chdir(tmp_path)
    src = tmp_path / "a.json"
    dest = tmp_path / "b.json"
    src.write_text(json.dumps({"geo": "Japan"}), encoding="utf-8")
    assert main(["import", str(src)]) == 0
    imported = json.loads(capsys.readouterr().out)
    assert imported["ok"] is True
    assert main(["export", str(dest)]) == 0
    exported = json.loads(capsys.readouterr().out)
    assert exported["ok"] is True
    assert dest.exists()
    names = {p.name for p in tmp_path.iterdir()}
    assert ".chronolock-state.json" not in names
