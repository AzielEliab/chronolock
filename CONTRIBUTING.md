# Contributing to ChronoLock

**Forks are first-class.** This project is Apache-2.0; you do not need
permission to fork, patch, or redistribute.

**Forks are welcome and always allowed.**

## How to run tests

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python -m pytest -q
```

Python 3.10+. Core is stdlib only (`zoneinfo`, `secrets`, `json`,
`http.server`). pytest is the dev extra. No network.

## Ground rules

1. **No persistence.** Do not add sqlite, a `.chronolock` store, a
   `.chronolock-state.json`, or a log of past advisories. Session state
   lives in memory and dies on `forget()`. `import` / `export` hold the
   last JSON document in process memory only; they write only the file
   the caller named.
2. **No user identification.** Last-known geo is a string, not a profile.
3. **No targeting, no virality optimization, no engagement metrics.**
   Do not add ML, A/B, reach scores, or outcome learning.
4. **User-facing JSON is five fields.** No scores, no confidence, no
   alternatives, no “because” in the CLI JSON or UI report. Tests may
   inspect internals. Plain text may name the 08:30–10:30 window.
5. **Keep the dependency list tiny.** Stdlib only in the core.
6. **UI binds loopback only** (`127.0.0.1:8851`). Do not listen on `0.0.0.0`.
   Port 8765 is StaticClock.
7. **Not a scheduler.** `stagger()` names times. It must not post, queue,
   or cron. Do not merge with TemporalLock.
8. New behavior needs a test that fails without the change.

## Where to change things

- Top-30 / geo resolve: `chronolock/anchors.py`
- Bundled index: `chronolock/data/index.json`, `chronolock/index.py`
- Windows / stagger: `chronolock/chronolect.py`
- Language / dialect: `chronolock/glossa.py`
- Five-basket shake: `chronolock/polarize.py`
- Session / forget: `chronolock/engine.py`
- CLI: `chronolock/cli.py` (`staticclock` is a deprecated alias)
- Local UI: `chronolock/ui.py`, `chronolock/web/` (simple view default; Import / Export JSON; Verify in plain words)
- Doctor: `chronolock/doctor.py` (plain words; no network)
- JSON import/export: `chronolock/jsonio.py` (no hidden store)

## License of contributions

By submitting a change you agree it is licensed under Apache-2.0, the
same license as the rest of the tree. Keep the copyright lines honest.
Copyright 2026 Aziel Eliab.
