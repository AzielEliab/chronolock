---
name: ChronoLock
description: Use when calling ChronoLock hosted /v1 or installing the local package. Dual surface: Worker /v1 + catalog MCP. This Worker /v1/mesh/* PROXY to aziel-runtime via AZIEL_RUNTIME. Suite mesh default OFF. QNM-BUILD-1.0 live|locked|isolated. QNS-CD-1.0 photon QNS1 packet transfer cross-map (hub cite only; no public qnsd). No Node Gate. No auto-heal. Not anonymity. Author Aziel Eliab.
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
- `GET /v1/mesh` — PROXY suite mesh status. Default OFF. QNM live|locked|isolated. QNS-CD-1.0 photon QNS1 packet transfer cross-map in the payload. Never enables. No public qnsd.
- `GET /v1/mesh/nodes` — PROXY Live Nodes roster (5-minute presence). Same QNS-CD-1.0 cross-map.
- `POST /v1/mesh/{enable,disable,join,heartbeat,leave,broadcast}` — PROXY. Bearer required to enable. No auto-heal. Anon-broadcast is not a publish path.
- Product POSTs listed in OpenAPI

Works with ChatGPT (GPT Actions / OpenAI), Grok (xAI), Venice, Claude (Anthropic), Cursor (MCP), Glama (MCP), Perplexity, Microsoft Copilot / Bing, Google Gemini / Vertex, Mistral, Meta AI, Apple Intelligence surfaces, Amazon Q tooling, DuckAssist, You.com, Cohere, and other MCP/OpenAPI-capable assistants. Import OpenAPI as a custom tool, GPT Action, HTTP tool, or MCP server as the client allows.

## Example

```bash
curl -s -A 'Mozilla/5.0' https://chronolock-download-tracker.vibelock.workers.dev/v1/health
curl -s -A 'Mozilla/5.0' https://chronolock-download-tracker.vibelock.workers.dev/v1/skill
curl -s -A 'Mozilla/5.0' https://chronolock-download-tracker.vibelock.workers.dev/v1/mesh
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

Local UI: **Import JSON file** (`type=file`) and **Export JSON**. Then `chronolock doctor`. Worker homepage Live Nodes strip polls `GET /v1/mesh` (default OFF). QNS-CD-1.0 is a hub cite / Worker mesh cross-map only ([qnm-node](https://github.com/AzielEliab/qnm-node), [aziel-runtime](https://github.com/AzielEliab/aziel-runtime)) — not a Softwares-tab product, not a public qnsd proxy.

Works with ChatGPT (GPT Actions / OpenAI), Grok (xAI), Venice, Claude (Anthropic), Cursor (MCP), Glama (MCP), Perplexity, Microsoft Copilot / Bing, Google Gemini / Vertex, Mistral, Meta AI, Apple Intelligence surfaces, Amazon Q tooling, DuckAssist, You.com, Cohere, and other MCP/OpenAPI-capable assistants. Import catalog or Worker OpenAPI as a custom tool, GPT Action, HTTP tool, or MCP server as the client allows.
