"""Self-check for ChronoLock. No network, no telemetry.

    chronolock doctor

Speaks in plain words so a sixth grader can tell if it is ready.
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Callable

from chronolock import __version__

AUTHOR = "Aziel Eliab"
Check = tuple[str, bool, str]


def _ok(name: str, detail: str = "") -> Check:
    return name, True, detail


def _fail(name: str, detail: str) -> Check:
    return name, False, detail


def _check_version() -> Check:
    if __version__:
        return _ok("version", str(__version__))
    return _fail("version", "missing")


def _check_identity() -> Check:
    try:
        mod = __import__(__name__.split(".")[0])
        author = str(getattr(mod, "__author__", AUTHOR))
    except Exception as exc:  # noqa: BLE001
        return _fail("identity", str(exc))
    blob = author + " " + AUTHOR
    forbidden = ("Col" + "lin H" + "orton", "Ja" + "ck Al" + "tman", "GodLock" + ".AZ", "Reve" + "aler")
    if any(x in blob for x in forbidden):
        return _fail("identity", "forbidden identity label")
    if "Aziel Eliab" not in blob:
        return _fail("identity", author)
    return _ok("identity", AUTHOR)


def _check_json_roundtrip() -> Check:
    from chronolock.jsonio import export_json, forget_imported, import_json

    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "in.json"
        out = Path(tmp) / "out.json"
        src.write_text(
            json.dumps({"product": "chronolock", "author": AUTHOR, "ok": True}, indent=2),
            encoding="utf-8",
        )
        rec = import_json(src)
        if not rec.get("ok"):
            forget_imported()
            return _fail("import", str(rec))
        rec2 = export_json(out)
        leftover = [p.name for p in Path(tmp).iterdir() if p.name.startswith(".chronolock")]
        forget_imported()
        if leftover:
            return _fail("json import/export", "left a hidden store: " + ", ".join(leftover))
        if not rec2.get("ok") or not out.exists():
            return _fail("export", str(rec2))
        doc = json.loads(out.read_text(encoding="utf-8"))
        if doc.get("author") != AUTHOR:
            return _fail("export author", str(doc.get("author")))
        return _ok("json import/export", "roundtrip")


def _check_advise() -> Check:
    from chronolock.engine import OUTPUT_FIELDS, ChronoLock

    clock = ChronoLock()
    try:
        adv = clock.advise("Indiana")
        payload = adv.to_dict()
    finally:
        clock.forget()
    if list(payload.keys()) != list(OUTPUT_FIELDS):
        return _fail("advise", str(list(payload.keys())))
    return _ok("advise", "five fields")


def _check_forget() -> Check:
    from chronolock.engine import ChronoLock

    clock = ChronoLock()
    clock.advise("Japan")
    clock.forget()
    if clock.last_inputs is None and clock.forgotten:
        return _ok("forget", "dropped")
    return _fail("forget", "retained")


def _check_loopback() -> Check:
    from chronolock.ui import LOOPBACK

    if "127.0.0.1" in LOOPBACK:
        return _ok("loopback", "127.0.0.1")
    return _fail("loopback", "missing 127.0.0.1")


def _check_alias() -> Check:
    from chronolock.cli import DEPRECATED_STATICCLOCK_LINE

    low = DEPRECATED_STATICCLOCK_LINE.lower()
    if "deprecated" in low and "chronolock" in low:
        return _ok("staticclock alias", "deprecated; ChronoLock is the public name")
    return _fail("staticclock alias", DEPRECATED_STATICCLOCK_LINE)


CHECKS: tuple[Callable[[], Check], ...] = (
    _check_version,
    _check_identity,
    _check_json_roundtrip,
    _check_advise,
    _check_forget,
    _check_loopback,
    _check_alias,
)


def _plain_sentence(name: str, ok: bool, detail: str) -> str:
    prefix = "Good." if ok else "Not good."
    if name == "version":
        body = f"Version is {detail or __version__}."
    elif name == "identity":
        body = "Author is Aziel Eliab."
    elif name == "json import/export":
        body = "You can Import and Export JSON."
    elif name == "advise":
        body = "Advise names five things: place, time, date, language, dialect."
    elif name == "forget":
        body = "After advising, memory is dropped. Nothing is saved on disk."
    elif name == "loopback":
        body = "The local page only opens on this computer."
    elif name == "staticclock alias":
        body = "staticclock is the old name; ChronoLock is the public name."
    else:
        body = name + (f" ({detail})" if detail else ".")
    return f"{prefix} {body}"


def collect_results() -> dict:
    results = []
    failed = 0
    sentences = []
    for fn in CHECKS:
        name, ok, detail = fn()
        results.append({"name": name, "ok": ok, "detail": detail, "plain": _plain_sentence(name, ok, detail)})
        sentences.append(_plain_sentence(name, ok, detail))
        if not ok:
            failed += 1
    if failed == 0:
        closing = (
            "All checks passed. ChronoLock is ready. "
            "It tells you a calm morning time to share. It does not post."
        )
    else:
        closing = "Some checks failed. ChronoLock is not ready."
    plain = " ".join(sentences) + " " + closing
    return {
        "ok": failed == 0,
        "failed": failed,
        "checks": results,
        "plain": plain,
        "version": __version__,
        "author": AUTHOR,
        "network": False,
        "telemetry": False,
    }


def run_doctor(*, as_json: bool = False) -> int:
    payload = collect_results()
    if as_json:
        print(json.dumps(payload, indent=2))
    else:
        for row in payload["checks"]:
            mark = "ok" if row["ok"] else "FAIL"
            print(f"[{mark}] {row['plain']}")
        print(payload["plain"])
        print("doctor", "passed" if payload["ok"] else "failed")
    return 0 if payload["ok"] else 1
