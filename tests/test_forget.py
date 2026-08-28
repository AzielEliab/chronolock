"""forget() drops last inputs; no on-disk store."""

from __future__ import annotations

from pathlib import Path

from chronolock.engine import ChronoLock


def test_forget_drops_last_inputs() -> None:
    clock = ChronoLock(nonce=b"forget-nonce-16b")
    clock.advise("France")
    assert clock.last_inputs == {"geo": "France"}
    assert clock.nonce is not None
    clock.forget()
    assert clock.last_inputs is None
    assert clock.nonce is None
    assert clock.forgotten is True


def test_context_manager_forgets() -> None:
    with ChronoLock(nonce=b"ctx-nonce-16bytes") as clock:
        clock.advise("Italy")
        assert clock.last_inputs is not None
    assert clock.forgotten is True
    assert clock.last_inputs is None


def test_no_data_directory_created(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    clock = ChronoLock()
    clock.advise("Poland")
    clock.forget()
    names = {p.name for p in tmp_path.iterdir()}
    assert ".chronolock" not in names
    assert "chronolock.db" not in names
    sqlite = list(tmp_path.rglob("*.sqlite")) + list(tmp_path.rglob("*.db"))
    assert sqlite == []


def test_package_source_has_no_persistence() -> None:
    import inspect
    from pathlib import Path as P

    import chronolock

    root = P(inspect.getfile(chronolock)).resolve().parent
    blob = ""
    for py in root.glob("*.py"):
        blob += py.read_text(encoding="utf-8")
    for banned in ("sqlite3", "sklearn", "tensorflow"):
        assert banned not in blob, banned
