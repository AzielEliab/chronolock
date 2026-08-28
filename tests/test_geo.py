"""Unknown geo maps to nearest anchor without crashing."""

from __future__ import annotations

from chronolock.anchors import DEFAULT_ANCHOR, TOP_30, basket_of, resolve_geo
from chronolock.engine import ChronoLock


def test_indiana_maps_to_united_states() -> None:
    assert resolve_geo("Indiana") == "United States"


def test_unknown_geo_does_not_crash() -> None:
    adv = ChronoLock(nonce=b"unknown-geo-16byt").advise("a village that is not listed")
    assert adv.geo_location_chosen in TOP_30
    assert resolve_geo("???") == DEFAULT_ANCHOR


def test_fuzzy_and_alias_resolution() -> None:
    assert resolve_geo("USA") == "United States"
    assert resolve_geo("uk") == "United Kingdom"
    assert resolve_geo("deutschland") == "Germany"
    assert resolve_geo("") == DEFAULT_ANCHOR


def test_chosen_region_is_in_input_basket() -> None:
    geo = "Brazil"
    adv = ChronoLock(nonce=b"basket-nonce-16b").advise(geo)
    assert adv.geo_location_chosen in basket_of(resolve_geo(geo))
