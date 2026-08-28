"""ChronoLock: timezone-aware linguistic alignment (the Chronolect Layer).

August 2026. Aziel Eliab. Apache-2.0.

Time-of-release is a semantic modifier. Chronolect is the interpretive
state shaped by local time. ChronoLock names a Temporal Neutral Window
(08:30–10:30 local) and, for several regions, a stagger so identical
content arrives in each region's own window.

This is advisory hygiene, not a scheduler, not analytics, not
user-profiling, not influence engineering. It does not change wording.
Timing advice only. Objective is not influence, but legibility.

Meaning is not only shaped by language, but by when language arrives.

Standalone from TemporalLock (receipts — a different product).
Forks are welcome and always allowed.
"""

from __future__ import annotations

from chronolock.engine import OUTPUT_FIELDS, Advisory, ChronoLock
from chronolock.zones import list_timezones

__version__ = "0.1.0"
__author__ = "Aziel Eliab"
__all__ = [
    "Advisory",
    "OUTPUT_FIELDS",
    "ChronoLock",
    "list_timezones",
    "__version__",
]
