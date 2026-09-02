"""Kid-plain README: three steps, no invented DOI, StaticClock honesty."""

from __future__ import annotations

from pathlib import Path


def test_readme_three_steps_no_doi_staticclock() -> None:
    root = Path(__file__).resolve().parent.parent
    text = (root / "README.md").read_text(encoding="utf-8")
    assert "Aziel Eliab" in text
    assert "Quick start (3 steps)" in text
    assert "chronolock ui" in text
    assert "Import JSON" in text
    assert "Export JSON" in text
    assert "Verify" in text
    assert "StaticClock" in text
    assert "deprecated" in text.lower()
    assert "10.5281" not in text
    assert "doi.org" not in text.lower()
    assert "zenodo" not in text.lower()
