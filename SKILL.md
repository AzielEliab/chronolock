---
name: ChronoLock
description: Use when calling ChronoLock hosted /v1 or installing the local package. Author Aziel Eliab.
---

# ChronoLock

Time-of-release is a semantic move. Advisory, not a scheduler. Author: **Aziel Eliab**.

**THIS IS:** timezone-aware linguistic alignment (Chronolect Layer). Public name of the layer formerly prototyped as StaticClock. The `staticclock` command still works as a deprecated alias.

**THIS IS NOT:** a scheduler, targeting tool, or analytics profile. Hosted `/v1` does not increment downloads or views.

Always send `User-Agent: Mozilla/5.0`. Cloudflare Workers may 403 an empty agent.

## Call these URLs

- Worker OpenAPI: https://chronolock-download-tracker.vibelock.workers.dev/openapi.json
- Catalog OpenAPI: https://aziel-runtime.vibelock.workers.dev/openapi.json
- MCP: `POST https://aziel-runtime.vibelock.workers.dev/mcp`
- Live skill (this markdown): `GET https://chronolock-download-tracker.vibelock.workers.dev/v1/skill`

Ops (do **not** increment downloads or views):

- `GET /v1/health` — liveness
- `GET /v1/skill` — this file
- Product POSTs listed in OpenAPI

Grok: import OpenAPI as a custom tool. ChatGPT: GPT Actions. Venice: HTTP tools.

## Example

```bash
curl -s -A 'Mozilla/5.0' https://chronolock-download-tracker.vibelock.workers.dev/v1/health
curl -s -A 'Mozilla/5.0' https://chronolock-download-tracker.vibelock.workers.dev/v1/skill
```

## Local (three steps)

```bash
curl -fsSL https://chronolock-download-tracker.vibelock.workers.dev/install.sh | bash
chronolock ui
chronolock doctor
```

Then open http://127.0.0.1:8851 (this computer only). Type a place, tap Advise. Optional Import JSON, Export JSON, Verify (plain words). Simple view is the default.

Counted download (gzip HTTP 200, no 302): https://chronolock-download-tracker.vibelock.workers.dev/download?asset=chronolock-0.1.0.tar.gz
GitHub: https://github.com/AzielEliab/chronolock

## Catalog + local UI

Author: **Aziel Eliab**. Honest scope: Advisory temporal window 08:30-10:30 local. Distinct from TemporalLock. Not a scheduler.

- Catalog product: https://aziel-runtime.vibelock.workers.dev/p/chronolock/
- Catalog OpenAPI: https://aziel-runtime.vibelock.workers.dev/openapi.json
- Catalog MCP: `POST https://aziel-runtime.vibelock.workers.dev/mcp`
- This Worker skill: `GET https://chronolock-download-tracker.vibelock.workers.dev/v1/skill`
- This Worker OpenAPI: https://chronolock-download-tracker.vibelock.workers.dev/openapi.json
- Sample payload: `GET https://chronolock-download-tracker.vibelock.workers.dev/v1/example`

Local UI: **Import JSON file** (`type=file`) and **Export JSON**. Then `chronolock doctor`.

Grok: import catalog or Worker OpenAPI as a custom tool. ChatGPT: GPT Actions. Venice: HTTP tools.
