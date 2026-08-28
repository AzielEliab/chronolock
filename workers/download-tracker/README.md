# chronolock download tracker

Isolated Worker `chronolock-download-tracker`. Project `chronolock`.
KV namespace `CHRONOLOCK_DOWNLOADS` bound as `DOWNLOADS`.
totalKey `chronolock|__total__`. Does not 302 to GitHub on `/download`.
Serves gzip via `ASSETS.fetch`, `Cache-Control: private, no-store`.

`/v1` never increments DOWNLOADS KV.

## Use with Grok, ChatGPT, Venice

- OpenAPI: `https://chronolock-download-tracker.vibelock.workers.dev/openapi.json`
- Health: `GET /v1/health` → `{ok, product, version:"0.1.0"}`
- Setup HTML: `GET /ai`
- Anchors: `GET /v1/anchors`
- Advisory: `POST /v1/advisory` `{geo, language?}`

Banner: advisory, not a scheduler, not targeting, not virality.

CORS `*` on API routes.
