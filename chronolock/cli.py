"""Command-line interface for ChronoLock.

    chronolock version
    chronolock anchors
    chronolock advise --geo "United States"
    chronolock advise --geo "Indiana"
    chronolock advise --geo "United States" --json
    chronolock stagger --geo "United States" --geo "Japan"
    chronolock zones
    chronolock ui
    chronolock serve

Advisory only. Five fields. Temporal Neutral Window 08:30–10:30 local.
Not a scheduler. Forks always allowed.

The ``staticclock`` console script is a deprecated alias: it prints one
line, then runs this same CLI.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Sequence

from chronolock import __version__
from chronolock.anchors import TOP_30
from chronolock.engine import OUTPUT_FIELDS, WINDOW_TEXT, ChronoLock
from chronolock.zones import list_timezones

DEPRECATED_STATICCLOCK_LINE = (
    "staticclock is deprecated; ChronoLock is the public name. Running the same advisory."
)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="chronolock",
        description=(
            "ChronoLock — Chronolect Layer / timezone-aware linguistic alignment "
            "(Aziel Eliab, 2026). Time-of-release is a semantic modifier. "
            "Advisory hygiene, not a scheduler, not targeting, not virality. "
            "Meaning is not only shaped by language, but by when language arrives. "
            "Local UI: `chronolock ui` at http://127.0.0.1:8851."
        ),
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("version", help="Print package version.")
    sub.add_parser("anchors", help="List the Top-30 geographic anchors.")

    p_adv = sub.add_parser(
        "advise",
        help="Emit one advisory for a last-known geo (five fields only).",
    )
    p_adv.add_argument(
        "--geo",
        required=True,
        help="Last-known geo (free text) or a Top-30 country name.",
    )
    p_adv.add_argument(
        "--json",
        action="store_true",
        dest="as_json",
        help="Print the five fields as JSON. No scores, no because.",
    )

    p_st = sub.add_parser(
        "stagger",
        help=(
            "Chrono-alignment: name each region's Temporal Neutral Window "
            "in UTC. Identical content; staggered arrival. Does not post."
        ),
    )
    p_st.add_argument(
        "--geo",
        action="append",
        required=True,
        dest="geos",
        help="Repeatable. One last-known geo or Top-30 name per flag.",
    )

    sub.add_parser(
        "zones",
        help="Read-only IANA zones with computed current local times.",
    )

    p_ui = sub.add_parser(
        "ui",
        help="Serve the local advisory UI on 127.0.0.1 (no memory of past advisories).",
    )
    p_ui.add_argument("--host", default="127.0.0.1", help="Loopback host (default 127.0.0.1).")
    p_ui.add_argument("--port", type=int, default=8851, help="Port (default 8851).")

    p_serve = sub.add_parser(
        "serve",
        help="Alias for ui. Bind 127.0.0.1 only.",
    )
    p_serve.add_argument("--host", default="127.0.0.1", help="Loopback host (default 127.0.0.1).")
    p_serve.add_argument("--port", type=int, default=8851, help="Port (default 8851).")


    p_doc = sub.add_parser("doctor", help="Self-check. No network, no telemetry.")
    p_doc.add_argument("--json", action="store_true", dest="as_json", help="Print doctor results as JSON.")

    p_imp = sub.add_parser("import", help="Import a JSON document.")
    p_imp.add_argument("path")

    p_exp = sub.add_parser("export", help="Export a JSON document.")
    p_exp.add_argument("path")

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    if args.cmd == "version":
        print(f"chronolock {__version__}")
        return 0

    if args.cmd == "anchors":
        for name in TOP_30:
            print(name)
        return 0

    if args.cmd == "advise":
        clock = ChronoLock()
        try:
            advisory = clock.advise(args.geo)
        finally:
            clock.forget()
        payload = advisory.to_dict()
        if args.as_json:
            print(json.dumps(payload, indent=2, ensure_ascii=False))
        else:
            print(advisory.to_text())
        return 0

    if args.cmd == "stagger":
        clock = ChronoLock()
        try:
            rows = clock.stagger(args.geos)
        finally:
            clock.forget()
        print(
            "Chrono-alignment (advisory, not a scheduler). "
            f"Temporal Neutral Window {WINDOW_TEXT} local. "
            "Identical content; staggered arrival. Does not post."
        )
        for row in rows:
            print(
                f"{row['region']:16}  {row['iana']:36}  "
                f"{row['local_date']} {row['local_window']} local  "
                f"utc {row['utc_instant']}"
            )
        return 0

    if args.cmd == "zones":
        rows = list_timezones()
        for row in rows:
            print(
                f"{row['region']:16}  {row['iana']:36}  "
                f"{row['local_date']} {row['local_time']}  UTC{row['utc_offset']}"
            )
        return 0

    if args.cmd in {"ui", "serve"}:
        from chronolock.ui import serve

        try:
            serve(host=args.host, port=args.port)
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 2
        return 0


    if args.cmd == "doctor":
        from chronolock.doctor import run_doctor

        return run_doctor(as_json=getattr(args, "as_json", False))

    if args.cmd == "import":
        from chronolock.jsonio import import_json

        rec = import_json(args.path)
        sys.stdout.write(json.dumps(rec, indent=2, ensure_ascii=False) + "\n")
        return 0

    if args.cmd == "export":
        from chronolock.jsonio import export_json

        rec = export_json(args.path)
        sys.stdout.write(json.dumps(rec, indent=2, ensure_ascii=False) + "\n")
        return 0

    parser.error(f"unknown command {args.cmd}")
    return 2


def staticclock_main(argv: Sequence[str] | None = None) -> int:
    """Deprecated ``staticclock`` console_scripts alias."""
    print(DEPRECATED_STATICCLOCK_LINE)
    return main(argv)


if __name__ == "__main__":
    raise SystemExit(main())
