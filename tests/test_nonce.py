"""One-shot nonce: same geo can differ; pinned nonce is deterministic."""

from __future__ import annotations

from chronolock.anchors import basket_of, resolve_geo
from chronolock.engine import ChronoLock

FIXED = b"test-hook-nonce!!"


def test_advise_twice_same_geo_can_differ() -> None:
    geo = "United States"
    seen: set[tuple[str, str, str]] = set()
    for _ in range(24):
        adv = ChronoLock().advise(geo)
        seen.add((adv.geo_location_chosen, adv.optimal_time, adv.dialect_section))
        basket = basket_of(resolve_geo(geo))
        assert adv.geo_location_chosen in basket
    assert len(seen) >= 2


def test_fixed_nonce_is_deterministic() -> None:
    a = ChronoLock(nonce=FIXED).advise("Canada")
    b = ChronoLock(nonce=FIXED).advise("Canada")
    assert a.to_dict() == b.to_dict()


def test_pinned_nonce_survives_two_calls_on_one_instance() -> None:
    clock = ChronoLock(nonce=FIXED)
    a = clock.advise("India")
    b = clock.advise("India")
    assert a.to_dict() == b.to_dict()
