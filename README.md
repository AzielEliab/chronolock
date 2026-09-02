# ChronoLock

Public name of the **Chronolect Layer** (formerly prototyped as StaticClock).
Timezone-aware linguistic alignment for non-eventful dissemination.

**Author:** Aziel Eliab
**Date:** 2026
**License:** [Apache-2.0](LICENSE)
**Version:** 0.1.0

> Meaning is not only shaped by language, but by when language arrives.
>
> The objective is not influence, but legibility.

Time-of-release is a **semantic modifier**. A Chronolect is the
interpretive state of a population shaped by local time. ChronoLock
names a **Temporal Neutral Window** (08:30–10:30 local) and, for more
than one region, a **chrono-alignment**: stagger identical content so
each region receives it in its own window.

It does **not** change wording. It is **not** a scheduler, **not**
analytics, **not** user-profiling, **not** influence engineering, **not**
virality, **not** a cron that posts. Advisory hygiene only. Failure if
used to provoke urgency.

Standalone from [TemporalLock](https://github.com/AzielEliab/temporallock)
(receipts — a different product; do not merge).

The `staticclock` console script is a **deprecated alias**: it prints one
line, then runs ChronoLock. StaticClock itself is not deleted.

**Forks are welcome and always allowed.**

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate && pip install -e ".[dev]"
chronolock ui
```


## One-click install

```bash
curl -fsSL https://chronolock-download-tracker.vibelock.workers.dev/install.sh | bash
```

The script curls the **counted** tarball from this project's Worker
(`/download`, User-Agent `Mozilla/5.0`), extracts, makes a venv, and
`pip install -e .`. Then run `chronolock ui`.

Or tap **Download** / **One-click install** on the Worker homepage:
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

Open http://127.0.0.1:8851 (loopback only). No CDN, no telemetry.
Port 8765 remains StaticClock.

Counted download: [https://chronolock-download-tracker.vibelock.workers.dev/](https://chronolock-download-tracker.vibelock.workers.dev/)

Direct tarball: [chronolock-0.1.0.tar.gz](https://chronolock-download-tracker.vibelock.workers.dev/download?asset=chronolock-0.1.0.tar.gz)

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

## Install

Python 3.10+. Stdlib only in the core (`zoneinfo`, `secrets`).

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## CLI

```bash
chronolock version
chronolock anchors
chronolock advise --geo "United States"
chronolock advise --geo "Indiana"
chronolock advise --geo "United States" --json
chronolock stagger --geo "United States" --geo "Japan"
chronolock zones
chronolock ui          # 127.0.0.1:8851
chronolock serve       # alias for ui
```

Deprecated: `staticclock …` prints one deprecation line, then the same commands.

## iPhone & Android

Flutter sources: [`mobile/`](mobile/). Application id `com.azieeliab.chronolock`. Offline. No analytics. Dark matte / gold.

Geo → five advisory fields. Not a scheduler.

```bash
cd mobile
flutter create --org com.azieeliab --project-name chronolock .
flutter pub get
flutter run
```

The `android/` and `ios/` folders in this tree are skeleton READMEs until you run `flutter create .` (this machine has no Flutter SDK on PATH). Then open `android/` in Android Studio or `ios/Runner.xcworkspace` in Xcode. Not a store listing.

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
language. A full 100+ language index is a replacement update of
`chronolock/data/index.json`, not a network fetch.

Default Temporal Neutral Window: **08:30–10:30** local. Documented
overrides (later cultural morning starts): Spain, Argentina, Egypt.

## Tests

```bash
pip install -e ".[dev]"
python -m pytest -q
```

Offline. No network. No sqlite. No `.chronolock` store.

## Layout

```
chronolock/          library (anchors, index, chronolect, glossa, polarize, engine, cli, ui)
chronolock/data/     bundled Top-30 index
tests/               pytest
docs/source/chronolect-layer.txt   the paper
docs/whitepaper.md   paper + software notes
examples/            advise once, then forget
mobile/              Flutter iPhone + Android (`flutter create .`)
```

## Use with Grok, ChatGPT, Venice

Live HTTPS runtime on the ChronoLock download-tracker Worker. Advisory only, not a scheduler, not targeting, not virality.

OpenAPI (ChatGPT GPT Actions / Venice custom HTTP / Grok custom tool):

```
https://chronolock-download-tracker.vibelock.workers.dev/openapi.json
```

Setup notes: [https://chronolock-download-tracker.vibelock.workers.dev/ai](https://chronolock-download-tracker.vibelock.workers.dev/ai)

MCP catalog (ships separately): `https://aziel-runtime.vibelock.workers.dev/mcp`

```bash
curl -sS -X POST https://chronolock-download-tracker.vibelock.workers.dev/v1/advisory \
  -H "content-type: application/json" \
  -d '{"geo": "Indiana", "language": "English"}'
```

## Honest scope

Not a scheduler. Not analytics. Not user-profiling. Not influence
engineering. Does not change wording. Timing advice only.

## License

Apache-2.0. See [LICENSE](LICENSE). Copyright 2026 Aziel Eliab.

Forks are welcome and always allowed.
