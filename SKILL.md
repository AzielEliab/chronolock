---
name: ChronoLock
description: Use when calling ChronoLock hosted /v1 or installing the local package. Author Aziel Eliab.
---

# ChronoLock

Time-of-release is a semantic move. Advisory, not a scheduler. Author: **Aziel Eliab**.

**THIS IS:** timezone-aware linguistic alignment (Chronolect Layer).

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

## Local (after one-click install)

```bash
curl -fsSL https://chronolock-download-tracker.vibelock.workers.dev/install.sh | bash
chronolock ui
chronolock doctor
```

Then open http://127.0.0.1:8851 (loopback only).

Counted download (gzip HTTP 200, no 302): https://chronolock-download-tracker.vibelock.workers.dev/download?asset=chronolock-0.1.0.tar.gz
GitHub: https://github.com/AzielEliab/chronolock
