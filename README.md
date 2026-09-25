# ChronoLock

ChronoLock names a calm morning time (08:30–10:30 local) so people can read what you share.

**Author:** Aziel Eliab
**License:** [Apache-2.0](LICENSE)
**Version:** 0.1.0

## Quick start (3 steps)

1. **Install** (Python 3.10+):

   ```bash
   python -m venv .venv && source .venv/bin/activate && pip install -e ".[dev]"
   ```

2. **Open the local page:**

   ```bash
   chronolock ui
   ```

   The terminal prints `Open http://127.0.0.1:8851/`.

3. **Type a place** (for example Indiana) and tap **Advise**. You see place, time, date, language, and dialect.

**Import JSON**, **Export JSON**, and **Verify** are under **Advanced** on that page. `chronolock doctor` runs the same checks in the terminal.

Same three steps are in [RUN.txt](RUN.txt).

## One-click install

```bash
curl -fsSL https://chronolock-download-tracker.vibelock.workers.dev/install.sh | bash
```

The script downloads the counted tarball (User-Agent `Mozilla/5.0`), extracts it, and runs `pip install -e .`. Then run `chronolock ui`.

Counted tarball: [chronolock-0.1.0.tar.gz](https://chronolock-download-tracker.vibelock.workers.dev/download?asset=chronolock-0.1.0.tar.gz)
GitHub: [https://github.com/AzielEliab/chronolock](https://github.com/AzielEliab/chronolock)

## Commands

People see short text. Add `--json` when a program should read the result.

```bash
chronolock
chronolock ui
chronolock advise --geo "Indiana"
chronolock advise --geo "United States" --json
chronolock doctor
chronolock version
```

Advanced:

```bash
chronolock anchors
chronolock stagger --geo "United States" --geo "Japan"
chronolock zones
chronolock import FILE.json
chronolock import FILE.json --json
chronolock export FILE.json
chronolock export FILE.json --json
chronolock serve       # same as ui
```

`import` / `export` keep the file in this run only. They do not write a `.chronolock` store.

The `staticclock` command is a **deprecated** alias. It prints one line, then runs ChronoLock. StaticClock itself is not deleted. Port 8765 remains StaticClock.

## What you get

Ask: “When should this be released so it is read, not reacted to?”

Input is a place (free text) or one of 30 known countries. Text output is five fields, plus the morning window:

| Field | Meaning |
|-------|---------|
| `geo_location_chosen` | One region from a five-place basket |
| `optimal_time` | Local clock time inside 08:30–10:30 |
| `optimal_date` | Local date in the chosen region |
| `primary_language` | From the bundled index |
| `dialect_section` | One of five dialectal variants |

`--json` on `advise` stays those five keys. No scores. No confidence. No alternatives. No “because”.

`stagger` names a morning window for several places. Identical content, different absolute times. It does not post.

```bash
chronolock stagger --geo "United States" --geo "Japan"
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

Version 0.1.0 ships the 30-place set plus five dialectal variants per language. Default morning window: **08:30–10:30** local. Documented later starts: Spain, Argentina, Egypt.

## iPhone & Android

Flutter sources: [`mobile/`](mobile/). Application id `com.azieeliab.chronolock`. Offline.

```bash
cd mobile
flutter create --org com.azieeliab --project-name chronolock .
flutter pub get
flutter run
```

## Tests

```bash
pip install -e ".[dev]"
python -m pytest -q
```

Offline. No network. No sqlite. No `.chronolock` store.

## About

ChronoLock names a time. It does not change wording. Timing advice only.

Not a scheduler. Not analytics. Not user-profiling. Not influence engineering.

Meaning is not only shaped by language, but by when language arrives. The objective is legibility.

Public name of the Chronolect Layer (formerly prototyped as StaticClock). Standalone from [TemporalLock](https://github.com/AzielEliab/temporallock) (receipts — a different product).

Forks are welcome and always allowed.

Paper: [docs/source/chronolect-layer.txt](docs/source/chronolect-layer.txt) · spec: [docs/whitepaper.md](docs/whitepaper.md)

How to contribute: [CONTRIBUTING.md](CONTRIBUTING.md).

## Use with ChatGPT, Grok, Venice, Claude, Cursor, Glama, Perplexity, Microsoft Copilot / Bing, Google Gemini / Vertex, Mistral, Meta AI, Apple Intelligence, Amazon Q, DuckAssist, You.com, Cohere, and other MCP/OpenAPI assistants

Catalog OpenAPI: https://aziel-runtime.vibelock.workers.dev/openapi.json
Catalog MCP: `POST https://aziel-runtime.vibelock.workers.dev/mcp`. Suite mesh `/v1/mesh/*` PROXY via `AZIEL_RUNTIME` (default OFF; QNM-BUILD-1.0 live|locked|isolated; QNS-CD-1.0 photon QNS1 packet transfer cross-map; no Node Gate; no public qnsd). Catalog MCP `mesh_*` + FragGate `slug=mesh`. Local qnsd lives in [qnm-node](https://github.com/AzielEliab/qnm-node); runtime cites in [aziel-runtime](https://github.com/AzielEliab/aziel-runtime). Not a Softwares-tab product.
This Worker skill: https://chronolock-download-tracker.vibelock.workers.dev/v1/skill
This Worker OpenAPI: https://chronolock-download-tracker.vibelock.workers.dev/openapi.json

Works with ChatGPT (GPT Actions / OpenAI), Grok (xAI), Venice, Claude (Anthropic), Cursor (MCP), Glama (MCP), Perplexity, Microsoft Copilot / Bing, Google Gemini / Vertex, Mistral, Meta AI, Apple Intelligence surfaces, Amazon Q tooling, DuckAssist, You.com, Cohere, and other MCP/OpenAPI-capable assistants.

Import the catalog or Worker OpenAPI as a custom tool, GPT Action (no auth), HTTP tool, or MCP server as the client allows. Always send `User-Agent: Mozilla/5.0`.

## Cite this

Aziel Eliab. ChronoLock. https://github.com/AzielEliab/chronolock. https://chronolock-download-tracker.vibelock.workers.dev.

- Catalog: https://aziel-runtime.vibelock.workers.dev/
- Counted download (gzip HTTP 200, no 302): https://chronolock-download-tracker.vibelock.workers.dev/download
- GitHub: https://github.com/AzielEliab/chronolock
- Citation JSON: https://chronolock-download-tracker.vibelock.workers.dev/cite.json

## License

Apache-2.0. See [LICENSE](LICENSE). Copyright 2026 Aziel Eliab.

Forks are welcome and always allowed.
