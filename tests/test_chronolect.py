"""Analytical window 08:30-10:30 unless a documented override region."""

from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

from chronolock.chronolect import (
    DEFAULT_WINDOW,
    OVERRIDES,
    TEMPORAL_NEUTRAL_WINDOW,
    in_window,
    next_window_open,
    stagger_for_regions,
    window_for,
)
from chronolock.engine import ChronoLock

FIXED = b"window-nonce-16b"


def test_default_time_inside_analytical_window() -> None:
    # Pin a nonce and a geo whose basket avoids override regions.
    adv = ChronoLock(nonce=FIXED).advise("Japan")
    if adv.geo_location_chosen in OVERRIDES:
        assert in_window(adv.optimal_time, window_for(adv.geo_location_chosen))
    else:
        assert in_window(adv.optimal_time, DEFAULT_WINDOW)


def test_override_regions_use_documented_window() -> None:
    for region in OVERRIDES:
        # Direct pick: shake may choose a neighbor; inspect the window helper.
        assert window_for(region) != DEFAULT_WINDOW
        assert window_for("Japan") == DEFAULT_WINDOW


def test_chosen_override_time_stays_in_override_window() -> None:
    # Exhaust a few nonces until Spain itself is chosen, then check the clock.
    found = False
    for i in range(80):
        nonce = bytes([i]) * 16
        adv = ChronoLock(nonce=nonce).advise("Spain")
        if adv.geo_location_chosen == "Spain":
            assert in_window(adv.optimal_time, OVERRIDES["Spain"])
            found = True
            break
    assert found


def test_temporal_neutral_window_is_0830_1030() -> None:
    assert TEMPORAL_NEUTRAL_WINDOW == ("08:30", "10:30")
    assert DEFAULT_WINDOW == ("08:30", "10:30")


def test_stagger_for_multi_region_is_advisory_not_a_cron() -> None:
    when = datetime(2026, 8, 28, 12, 0, tzinfo=ZoneInfo("UTC"))
    rows = stagger_for_regions(
        [
            ("United States", "America/New_York", DEFAULT_WINDOW),
            ("Japan", "Asia/Tokyo", DEFAULT_WINDOW),
        ],
        when=when,
    )
    assert len(rows) == 2
    instants = {r["utc_instant"] for r in rows}
    assert len(instants) == 2  # different absolute times
    for r in rows:
        assert r["local_window"] == "08:30–10:30"
        assert "not a scheduler" in r["note"].lower()
        assert "08:30" in r["local_open"] or r["local_open"] == "08:30"
    clock = ChronoLock()
    named = clock.stagger(["United States", "Japan"], when=when)
    assert len(named) == 2
    assert named[0]["utc_instant"] != named[1]["utc_instant"]


def test_next_window_open_is_never_midnight() -> None:
    when = datetime(2026, 8, 28, 23, 0, tzinfo=ZoneInfo("America/New_York"))
    open_at = next_window_open("America/New_York", when=when)
    assert not (open_at.hour == 0 and open_at.minute == 0)
    assert open_at.hour == 8 and open_at.minute == 30
