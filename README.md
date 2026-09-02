# ChronoLock

Public name of the **Chronolect Layer** (formerly prototyped as StaticClock).
It names a calm morning time so people read something, not yell about it.

**Author:** Aziel Eliab
**Date:** 2026
**License:** [Apache-2.0](LICENSE)
**Version:** 0.1.0

> Meaning is not only shaped by language, but by when language arrives.
>
> The objective is not influence, but legibility.

Time-of-release is a **semantic modifier**. ChronoLock names a
**Temporal Neutral Window** (08:30–10:30 local). It does **not** change
wording. It is **not** a scheduler, **not** analytics, **not**
user-profiling, **not** influence engineering, **not** virality, **not**
a cron that posts. Advisory hygiene only.

Standalone from [TemporalLock](https://github.com/AzielEliab/temporallock)
(receipts — a different product; do not merge).

The `staticclock` console script is a **deprecated alias**: it prints one
line, then runs ChronoLock. StaticClock itself is not deleted.

**Forks are welcome and always allowed.**

## Quick start (3 steps)

1. **Install** (Python 3.10+):

   ```bash
   python -m venv .venv && source .venv/bin/activate && pip install -e ".[dev]"
   ```

2. **Open the local app:**

   ```bash
   chronolock ui
   ```

3. **In the browser** at http://127.0.0.1:8851 (this computer only): type a
   place (like Indiana), tap **Advise**. You will see five things: place,
   time, date, language, dialect. Optional: **Import JSON**, **Export JSON**,
   **Verify** (plain words). Simple view is the default. No CDN, no telemetry.

That is the whole start. `chronolock doctor` says the same checks in plain
words. Port 8765 remains StaticClock.

## One-click install

```bash
curl -fsSL https://chronolock-download-tracker.vibelock.workers.dev/install.sh | bash
```

The script curls the **counted** tarball from this project's Worker
(`/download`, User-Agent `Mozilla/5.0`), extracts, makes a venv, and
`pip install -e .`. Then run `chronolock ui`.

Or tap **Download** / **One-click install** on the Worker homepage
(a 6th-grader can tap it):
https://chronolock-download-tracker.vibelock.workers.dev/

## Counted download (Cloudflare Worker)

**This is the counted download.** GitHub releases exist as a mirror.
The Worker serves the gzip itself (HTTP 200, no 302 to GitHub).

- Homepage: [https://chronolock-download-tracker.vibelock.workers.dev/](https://chronolock-download-tracker.vibelock.workers.dev/)
- Direct tarball: [chronolock-0.1.0.tar.gz](https://chronolock-download-tracker.vibelock.workers.dev/download?asset=chronolock-0.1.0.tar.gz)
- One-click install: [https://chronolock-download-tracker.vibelock.workers.dev/install.sh](https://chronolock-download-tracker.vibelock.workers.dev/install.sh)
- Skill: [https://chronolock-download-tracker.vibelock.workers.dev/v1/skill](https://chronolock-download-tracker.vibelock.workers.dev/v1/skill)
- OpenAPI: [https://chronolock-download-tracker.vibelock.workers.dev/openapi.json](https://chronolock-download-tracker.vibelock.workers.dev/openapi.json)
- GitHub: [https://github.com/AzielEliab/chronolock](https://github.com/AzielEliab/chronolock)

Isolated counter: Worker `chronolock-download-tracker`, KV `CHRONOLOCK_DOWNLOADS`. `/v1` does not increment downloads.

Paper: [docs/source/chronolect-layer.txt](docs/source/chronolect-layer.txt) · spec: [docs/whitepaper.md](docs/whitepaper.md)

How to contribute: [CONTRIBUTING.md](CONTRIBUTING.md).

---

## What it answers

“When should this be released so it is read, not reacted to?”

Input is a last-known geo (free text) or a Top-30 country. Output is
exactly five fields:

| Field | Meaning |
|-------|---------|
| `geo_location_chosen` | One region from a five-basket polarize/shake |
| `optimal_time` | Local clock time inside the Temporal Neutral Window |
| `optimal_date` | Local date in the chosen region |
| `primary_language` | From the static bundled index |
| `dialect_section` | One of five dialectal variants |

Plain text also names the window **08:30–10:30** local. JSON stays five
keys. No scores. No confidence. No alternatives. No “because”.

## Chrono-alignment (stagger)

Multi-region publication: **identical** content, different absolute
times, so each region is inside 08:30–10:30 *local*. This is advice,
not a job runner.

```bash
chronolock stagger --geo "United States" --geo "Japan"
```

Avoid midnight local, late-night Friday or Sunday, and emotionally
loaded global sync. Do not use this to provoke urgency.

## CLI

```bash
chronolock version
chronolock doctor
chronolock anchors
chronolock advise --geo "United States"
chronolock advise --geo "Indiana"
chronolock advise --geo "United States" --json
chronolock stagger --geo "United States" --geo "Japan"
chronolock zones
chronolock import FILE.json
chronolock export FILE.json
chronolock ui          # 127.0.0.1:8851
chronolock serve       # alias for ui
```

Deprecated: `staticclock …` prints one deprecation line, then the same commands.

`import` / `export` are process memory only. They do not write a
`.chronolock` store.

## iPhone & Android

Flutter sources: [`mobile/`](mobile/). Application id `com.azieeliab.chronolock`. Offline. No analytics.

```bash
cd mobile
flutter create --org com.azieeliab --project-name chronolock .
flutter pub get
flutter run
```

## Library

```python
from chronolock.engine import ChronoLock

with ChronoLock() as clock:
    adv = clock.advise("Indiana")
    print(adv.to_text())   # five fields + 08:30–10:30 window line
    rows = clock.stagger(["United States", "Japan"])
# forget() ran on exit — nonce and inputs are gone
```

v0.1 ships the Top-30 geographic set plus five dialectal variants per
language. Default Temporal Neutral Window: **08:30–10:30** local.
Documented overrides (later cultural morning starts): Spain, Argentina, Egypt.

## Tests

```bash
pip install -e ".[dev]"
python -m pytest -q
```

Offline. No network. No sqlite. No `.chronolock` store.

## Honest scope

Not a scheduler. Not analytics. Not user-profiling. Not influence
engineering. Does not change wording. Timing advice only.

## Use with Grok / ChatGPT / Venice

Catalog OpenAPI: https://aziel-runtime.vibelock.workers.dev/openapi.json
Catalog MCP: `POST https://aziel-runtime.vibelock.workers.dev/mcp`
This Worker skill: https://chronolock-download-tracker.vibelock.workers.dev/v1/skill
This Worker OpenAPI: https://chronolock-download-tracker.vibelock.workers.dev/openapi.json

Grok: import the catalog or Worker OpenAPI as a custom tool. ChatGPT: GPT Actions (no auth). Venice: HTTP tools. Always send `User-Agent: Mozilla/5.0`.

## Cite this

Aziel Eliab. ChronoLock. https://github.com/AzielEliab/chronolock. https://chronolock-download-tracker.vibelock.workers.dev.

- Catalog: https://aziel-runtime.vibelock.workers.dev/
- Worker homepage: https://chronolock-download-tracker.vibelock.workers.dev/
- Counted download (gzip HTTP 200, no 302): https://chronolock-download-tracker.vibelock.workers.dev/download
- GitHub: https://github.com/AzielEliab/chronolock
- Citation JSON: https://chronolock-download-tracker.vibelock.workers.dev/cite.json

## License

Apache-2.0. See [LICENSE](LICENSE). Copyright 2026 Aziel Eliab.

Forks are welcome and always allowed.
