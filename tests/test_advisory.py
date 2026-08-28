"""User-facing advisory contract: five fields, no reasoning dump."""

from __future__ import annotations

import json

from chronolock.chronolect import DEFAULT_WINDOW, in_window
from chronolock.engine import OUTPUT_FIELDS, WINDOW_TEXT, Advisory, ChronoLock
from chronolock.glossa import dialects_for, primary_language
from chronolock.index import record

BANNED = ("because", "score", "confidence", "alternative", "reason")


def _blob(advisory: Advisory) -> str:
    return json.dumps(advisory.to_dict()).lower()


def test_output_keys_exactly_five_fields() -> None:
    adv = ChronoLock(nonce=b"fixed-nonce-16b!!").advise("United States")
    keys = list(adv.to_dict().keys())
    assert keys == list(OUTPUT_FIELDS)
    assert len(keys) == 5


def test_json_has_no_because_score_or_confidence() -> None:
    adv = ChronoLock(nonce=b"fixed-nonce-16b!!").advise("Germany")
    blob = _blob(adv)
    for word in BANNED:
        assert word not in blob
    assert "because" not in adv.to_json().lower()


def test_primary_language_matches_chosen_region() -> None:
    adv = ChronoLock(nonce=b"lang-nonce-16byt").advise("Japan")
    assert adv.primary_language == primary_language(adv.geo_location_chosen)
    assert adv.primary_language == record(adv.geo_location_chosen)["language"]


def test_dialect_is_one_of_five_for_language() -> None:
    adv = ChronoLock(nonce=b"dial-nonce-16byt").advise("Spain")
    options = dialects_for(adv.primary_language)
    assert len(options) == 5
    assert adv.dialect_section in options


def test_window_0830_1030_appears_in_advisory_text() -> None:
    adv = ChronoLock(nonce=b"window-text-16byt").advise("Japan")
    text = adv.to_text()
    assert "08:30" in text
    assert "10:30" in text
    assert WINDOW_TEXT in text
    assert in_window(adv.optimal_time, DEFAULT_WINDOW)
    # JSON fields stay five; window is in the text, time is inside the window.
    assert "08:30" in WINDOW_TEXT and "10:30" in WINDOW_TEXT
