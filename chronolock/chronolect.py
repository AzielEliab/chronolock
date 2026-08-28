"""Chronolect: Temporal Neutral Window and chrono-alignment.

Default analytical window is 08:30–10:30 local — the Temporal Neutral
Window in THE CHRONOLECT LAYER. Time-of-release is a semantic modifier.
The picked clock time sits inside the window.

Chrono-alignment (stagger_for_regions) names a UTC instant for each
region so identical content can arrive in that region's own window.
This module does not post, queue, or cron. It does not change wording.
It is advisory hygiene, not a scheduler and not influence engineering.

Avoid midnight local, late-night Friday or Sunday, and emotionally
loaded global sync. Failure if used to provoke urgency.
"""

from __future__ import annotations

from datetime import date, datetime, time, timedelta, timezone
from typing import Sequence
from zoneinfo import ZoneInfo

from chronolock.polarize import pick_index

# Temporal Neutral Window (paper §4). 08:30–10:30 local.
DEFAULT_WINDOW: tuple[str, str] = ("08:30", "10:30")
TEMPORAL_NEUTRAL_WINDOW: tuple[str, str] = DEFAULT_WINDOW

# Documented overrides (v0.1: three). Rest of the Top-30 use DEFAULT_WINDOW.
OVERRIDES: dict[str, tuple[str, str]] = {
    "Spain": ("09:30", "11:30"),       # later Mediterranean morning
    "Argentina": ("09:30", "11:30"),   # Rioplatense later cultural start
    "Egypt": ("09:00", "11:00"),       # later administrative morning
}

HYGIENE_AVOID: tuple[str, ...] = (
    "midnight local",
    "late-night Friday",
    "late-night Sunday",
    "emotionally loaded global sync",
)


def parse_hhmm(text: str) -> time:
    hour_s, minute_s = text.split(":")
    return time(int(hour_s), int(minute_s))


def window_for(region: str) -> tuple[str, str]:
    return OVERRIDES.get(region, DEFAULT_WINDOW)


def format_window(window: tuple[str, str] | None = None) -> str:
    start, end = window or DEFAULT_WINDOW
    return f"{start}–{end}"


def slots_in(window: tuple[str, str], step_minutes: int = 15) -> list[str]:
    start = parse_hhmm(window[0])
    end = parse_hhmm(window[1])
    start_m = start.hour * 60 + start.minute
    end_m = end.hour * 60 + end.minute
    out: list[str] = []
    m = start_m
    while m <= end_m:
        out.append(f"{m // 60:02d}:{m % 60:02d}")
        m += step_minutes
    return out


def pick_time(region: str, nonce: bytes) -> str:
    window = window_for(region)
    slots = slots_in(window)
    return slots[pick_index(len(slots), nonce, b"time")]


def local_date(iana: str, when: datetime | None = None) -> date:
    tz = ZoneInfo(iana)
    now = when if when is not None else datetime.now(tz)
    if now.tzinfo is None:
        now = now.replace(tzinfo=tz)
    else:
        now = now.astimezone(tz)
    return now.date()


def in_window(hhmm: str, window: tuple[str, str]) -> bool:
    t = parse_hhmm(hhmm)
    start = parse_hhmm(window[0])
    end = parse_hhmm(window[1])
    return start <= t <= end


def is_late_night_friday_or_sunday(local_dt: datetime) -> bool:
    """True for late-night Friday or Sunday local (paper §5 avoid list)."""
    weekday = local_dt.weekday()  # Mon=0 ... Fri=4, Sun=6
    hour = local_dt.hour
    if weekday == 4 and hour >= 22:  # Friday night
        return True
    if weekday == 6 and (hour >= 22 or hour < 6):  # Sunday late / wee hours
        return True
    if weekday == 5 and hour < 6:  # after Friday midnight
        return True
    if weekday == 0 and hour < 6:  # after Sunday midnight
        return True
    return False


def next_window_open(
    iana: str,
    window: tuple[str, str] | None = None,
    when: datetime | None = None,
) -> datetime:
    """Next local opening of the Temporal Neutral Window in ``iana``.

    If today's window has already closed, name tomorrow's opening.
    Never names midnight local. Does not fire a job.
    """
    win = window or DEFAULT_WINDOW
    tz = ZoneInfo(iana)
    now = datetime.now(tz) if when is None else when
    if now.tzinfo is None:
        now = now.replace(tzinfo=tz)
    else:
        now = now.astimezone(tz)
    start = parse_hhmm(win[0])
    end = parse_hhmm(win[1])
    candidate = datetime.combine(now.date(), start, tzinfo=tz)
    close = datetime.combine(now.date(), end, tzinfo=tz)
    if now > close:
        candidate = candidate + timedelta(days=1)
    # Skip a candidate that lands in late-night Friday/Sunday (should
    # not happen for 08:30, but keep the hygiene rule explicit).
    guard = 0
    while is_late_night_friday_or_sunday(candidate) and guard < 8:
        candidate = candidate + timedelta(days=1)
        guard += 1
    if candidate.hour == 0 and candidate.minute == 0:
        candidate = candidate.replace(hour=start.hour, minute=start.minute)
    return candidate


def stagger_for_regions(
    rows: Sequence[tuple[str, str, tuple[str, str]]],
    when: datetime | None = None,
) -> list[dict[str, str]]:
    """Chrono-alignment: one UTC instant per region.

    ``rows`` is (label, iana, window). Identical content; different
    absolute times so each region receives it in its own Temporal
    Neutral Window. Advisory only — not a cron that posts.
    """
    out: list[dict[str, str]] = []
    for label, iana, window in rows:
        open_local = next_window_open(iana, window=window, when=when)
        utc = open_local.astimezone(timezone.utc)
        out.append(
            {
                "region": label,
                "iana": iana,
                "local_date": open_local.date().isoformat(),
                "local_window": format_window(window),
                "local_open": open_local.strftime("%H:%M"),
                "utc_instant": utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "note": (
                    "Advisory only. Not a scheduler. Identical content; "
                    "staggered arrival. Does not change wording."
                ),
            }
        )
    return out
