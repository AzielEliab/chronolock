"""Kid-plain README: three steps, no invented DOI, StaticClock honesty."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FULL_CLIENT_MARKERS = (
    "ChatGPT (GPT Actions / OpenAI)",
    "Grok (xAI)",
    "Venice",
    "Claude (Anthropic)",
    "Cursor (MCP)",
    "Glama (MCP)",
    "Perplexity",
    "Microsoft Copilot / Bing",
    "Google Gemini / Vertex",
    "Mistral",
    "Meta AI",
    "Apple Intelligence",
    "Amazon Q",
    "DuckAssist",
    "You.com",
    "Cohere",
    "MCP/OpenAPI-capable assistants",
)

EXCLUSIVE_HEADINGS = (
    "## Use with Grok / ChatGPT / Venice",
    "use with Grok, ChatGPT, Venice",
    "Grok: import OpenAPI as a custom tool. ChatGPT: GPT Actions. Venice: HTTP tools.",
    "Grok: import catalog or Worker OpenAPI as a custom tool. ChatGPT: GPT Actions. Venice: HTTP tools.",
    "Grok: import the catalog OpenAPI as a custom tool. ChatGPT: GPT Actions. Venice: HTTP tools.",
    "Grok: import the catalog or Worker OpenAPI as a custom tool. ChatGPT: GPT Actions (no auth). Venice: HTTP tools.",
)


def _public_copy_files() -> dict[str, str]:
    return {
        "README.md": (ROOT / "README.md").read_text(encoding="utf-8"),
        "SKILL.md": (ROOT / "SKILL.md").read_text(encoding="utf-8"),
        "workers/download-tracker/src/runtime.js": (
            ROOT / "workers/download-tracker/src/runtime.js"
        ).read_text(encoding="utf-8"),
    }


def test_readme_three_steps_no_doi_staticclock() -> None:
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "Aziel Eliab" in text
    assert "Quick start (3 steps)" in text
    assert "chronolock ui" in text
    assert "Import JSON" in text
    assert "Export JSON" in text
    assert "Verify" in text
    assert "StaticClock" in text
    assert "deprecated" in text.lower()
    assert "10.5281" not in text
    assert "doi.org" not in text.lower()
    assert "zenodo" not in text.lower()


def test_public_copy_lists_full_ai_clients_not_exclusive_three() -> None:
    for name, text in _public_copy_files().items():
        for exclusive in EXCLUSIVE_HEADINGS:
            assert exclusive not in text, f"{name} still has exclusive claim: {exclusive}"
        for marker in FULL_CLIENT_MARKERS:
            assert marker in text, f"{name} missing client marker: {marker}"
        assert "Aziel Eliab" in text
        assert text.count("Aziel Eliab") >= 1
        lowered = text.lower()
        assert "author:" in lowered or "author " in lowered
        # Public identity is Aziel Eliab only — no second byline name.
        assert "co-author" not in lowered
        assert "authored by" not in lowered or "aziel eliab" in lowered
