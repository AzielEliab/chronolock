"""JSON import/export for ChronoLock. Process memory only. Author: Aziel Eliab.

No ``.chronolock`` store. No sqlite. Import holds the last document in
this process; ``forget_imported()`` drops it. Export writes a file the
caller named — that is the user's file, not a hidden product store.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from chronolock import __version__

AUTHOR = "Aziel Eliab"
PRODUCT = "ChronoLock"

_LAST: dict[str, Any] | None = None


def _as_path(path: str | Path) -> Path:
    return Path(path)


def last_imported() -> dict[str, Any] | None:
    if _LAST is None:
        return None
    return dict(_LAST)


def forget_imported() -> None:
    global _LAST
    _LAST = None


def import_json(path: str | Path) -> dict[str, Any]:
    """Read a JSON object. Keep it in process memory only."""
    global _LAST
    pth = _as_path(path)
    doc = json.loads(pth.read_text(encoding="utf-8"))
    if not isinstance(doc, dict):
        raise ValueError("JSON object required")
    _LAST = dict(doc)
    return {
        "ok": True,
        "imported": str(pth),
        "keys": sorted(str(k) for k in doc.keys()),
        "author": AUTHOR,
        "product": PRODUCT,
        "version": __version__,
    }


def export_json(path: str | Path) -> dict[str, Any]:
    """Write a JSON document the caller named. Does not create a hidden store."""
    pth = _as_path(path)
    payload: Any = dict(_LAST) if isinstance(_LAST, dict) else {}
    doc = {
        "product": PRODUCT,
        "package": "chronolock",
        "version": __version__,
        "author": AUTHOR,
        "payload": payload,
    }
    pth.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {
        "ok": True,
        "exported": str(pth),
        "author": AUTHOR,
        "product": PRODUCT,
        "version": __version__,
    }
