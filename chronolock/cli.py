"""Command-line interface for ChronoLock.

Human text is the default. ``--json`` prints the same records for machines.

    chronolock
    chronolock ui
    chronolock advise --geo "Indiana"
    chronolock advise --geo "United States" --json
    chronolock doctor

The ``staticclock`` console script is a deprecated alias: it prints one
line, then runs this same CLI.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Sequence

from chronolock import __author__, __version__
from chronolock.anchors import TOP_30
from chronolock.engine import WINDOW_TEXT, ChronoLock
from chronolock.zones import list_timezones

DEPRECATED_STATICCLOCK_LINE = (
    "staticclock is deprecated; ChronoLock is the public name. Running the same advisory."
)

_HELP = f"""\
ChronoLock — name a calm morning time (08:30–10:30 local) so people can read what you share.

Author: Aziel Eliab

Usage:
  chronolock
  chronolock ui
  chronolock advise --geo "Indiana"
  chronolock doctor
  chronolock --help

Common commands:
  ui          Open the local page at http://127.0.0.1:8851
  advise      Name a morning time for one place
  doctor      Check that ChronoLock is ready
  version     Print the version

Advanced:
  anchors     List the 30 places ChronoLock knows
  stagger     Name a morning window for several places
  zones       Show the current local time in each place
  import      Read a JSON file (this run only)
  export      Write a JSON file you name
  serve       Same as ui

Options:
  -h, --help  Show this help
  --json      JSON for machines (on advise, doctor, version, anchors, stagger, zones, import, export)

Examples:
  chronolock ui
  chronolock advise --geo "Indiana"
  chronolock advise --geo "United States" --json
  chronolock stagger --geo "United States" --geo "Japan"
  chronolock doctor

The staticclock command is the previous name. It runs these same commands.
"""

_WELCOME = """\
ChronoLock names a calm morning time (08:30–10:30 local) so people can read what you share.

Open the local page, or ask about one place.

  chronolock ui
  chronolock advise --geo "Indiana"
  chronolock doctor
  chronolock --help

Author: Aziel Eliab
"""


class HumanParser(argparse.ArgumentParser):
    """Argparse with git-style help and plain errors."""

    def format_help(self) -> str:
        if self.prog == "chronolock":
            return _HELP
        return super().format_help()

    def error(self, message: str) -> None:
        self.exit(2, _plain_error(self.prog, message) + "\n")


def _plain_error(prog: str, message: str) -> str:
    choice = re.search(r"invalid choice: '([^']+)'", message)
    if choice:
        name = choice.group(1)
        return f'Unknown command "{name}". Try: chronolock ui   or   chronolock --help'
    low = message.lower()
    if "required" in low and "--geo" in message:
        if prog.endswith("stagger"):
            return (
                'At least one place is required. '
                'Try: chronolock stagger --geo "United States" --geo "Japan"'
            )
        return 'A place is required. Try: chronolock advise --geo "Indiana"'
    if "required" in low and "path" in low:
        if prog.endswith("export"):
            return "A file path is required. Try: chronolock export FILE.json"
        return "A file path is required. Try: chronolock import FILE.json"
    if "required" in low and re.search(r"\bcmd\b", low):
        return _WELCOME.rstrip()
    if "invalid int value" in low and "--port" in message:
        return "Port must be a whole number. Try: chronolock ui --port 8851"
    if "expected one argument" in low:
        return f"{message}. Try: chronolock --help"
    if low.startswith("unrecognized arguments"):
        return f"{message}. Try: chronolock --help"
    return f"{message}. Try: chronolock --help"


def _add_json(parser: argparse.ArgumentParser, help_text: str) -> None:
    parser.add_argument("--json", action="store_true", dest="as_json", help=help_text)


def _build_parser() -> argparse.ArgumentParser:
    parser = HumanParser(prog="chronolock", add_help=True)
    sub = parser.add_subparsers(dest="cmd", required=False)

    p_ver = sub.add_parser("version", help="Print the version.")
    _add_json(p_ver, "Print version as JSON.")

    p_anchors = sub.add_parser("anchors", help="List the 30 known places.")
    _add_json(p_anchors, "Print the place list as JSON.")

    p_adv = sub.add_parser(
        "advise",
        help="Name a morning time for one place.",
        description="Name a calm morning time for one place. Five fields, plus the 08:30–10:30 window in text.",
    )
    p_adv.add_argument("--geo", required=True, help='Place, for example "Indiana".')
    _add_json(p_adv, "Print the five fields as JSON.")

    p_st = sub.add_parser(
        "stagger",
        help="Name a morning window for several places.",
        description=(
            f"Name each place's morning window in UTC ({WINDOW_TEXT} local). "
            "Identical content; staggered arrival. Does not post."
        ),
    )
    p_st.add_argument(
        "--geo",
        action="append",
        required=True,
        dest="geos",
        help="Repeat for each place.",
    )
    _add_json(p_st, "Print the window rows as JSON.")

    p_zones = sub.add_parser("zones", help="Show the current local time in each known place.")
    _add_json(p_zones, "Print the time-zone rows as JSON.")

    p_ui = sub.add_parser("ui", help="Open the local page on this computer.")
    p_ui.add_argument("--host", default="127.0.0.1", help="Loopback host (default 127.0.0.1).")
    p_ui.add_argument("--port", type=int, default=8851, help="Port (default 8851).")

    p_serve = sub.add_parser("serve", help="Same as ui.")
    p_serve.add_argument("--host", default="127.0.0.1", help="Loopback host (default 127.0.0.1).")
    p_serve.add_argument("--port", type=int, default=8851, help="Port (default 8851).")

    p_doc = sub.add_parser("doctor", help="Check that ChronoLock is ready.")
    _add_json(p_doc, "Print the check results as JSON.")

    p_imp = sub.add_parser("import", help="Read a JSON file for this run only.")
    p_imp.add_argument("path")
    _add_json(p_imp, "Print the import receipt as JSON.")

    p_exp = sub.add_parser("export", help="Write a JSON file you name.")
    p_exp.add_argument("path")
    _add_json(p_exp, "Print the export receipt as JSON.")

    return parser


def _emit(obj: object, *, as_json: bool, human: str) -> None:
    if as_json:
        sys.stdout.write(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")
    else:
        sys.stdout.write(human)


def _read_failure(path: str, exc: BaseException) -> int:
    if isinstance(exc, FileNotFoundError):
        print(f"No file at {path}. Try: chronolock import FILE.json", file=sys.stderr)
    elif isinstance(exc, json.JSONDecodeError):
        print(f"{path} is not JSON. Try a file that starts with {{.", file=sys.stderr)
    elif isinstance(exc, ValueError):
        print(f"{exc}. Try a JSON object (curly braces).", file=sys.stderr)
    elif isinstance(exc, OSError):
        reason = exc.strerror or "could not read or write the file"
        print(f"Could not use {path} ({reason}). Check the path and try again.", file=sys.stderr)
    else:
        print(f"Could not use {path}. Try: chronolock --help", file=sys.stderr)
    return 2


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    if args.cmd is None:
        sys.stdout.write(_WELCOME)
        return 0

    if args.cmd == "version":
        if args.as_json:
            _emit(
                {"name": "chronolock", "version": __version__, "author": __author__},
                as_json=True,
                human="",
            )
        else:
            print(f"chronolock {__version__}")
        return 0

    if args.cmd == "anchors":
        names = list(TOP_30)
        if args.as_json:
            _emit(names, as_json=True, human="")
        else:
            print("\n".join(names))
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
            print("Calm morning time")
            print(advisory.to_text())
        return 0

    if args.cmd == "stagger":
        clock = ChronoLock()
        try:
            rows = clock.stagger(args.geos)
        finally:
            clock.forget()
        if args.as_json:
            print(json.dumps(rows, indent=2, ensure_ascii=False))
            return 0
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
        if args.as_json:
            print(json.dumps(rows, indent=2, ensure_ascii=False))
            return 0
        print("Current local time for each known place.")
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
            print(f"{exc}. Try: chronolock ui", file=sys.stderr)
            return 2
        except OSError as exc:
            reason = exc.strerror or "the port is not available"
            print(
                f"Could not open the local page ({reason}). Try: chronolock ui --port 8852",
                file=sys.stderr,
            )
            return 2
        return 0

    if args.cmd == "doctor":
        from chronolock.doctor import run_doctor

        return run_doctor(as_json=getattr(args, "as_json", False))

    if args.cmd == "import":
        from chronolock.jsonio import import_json

        try:
            rec = import_json(args.path)
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            return _read_failure(args.path, exc)
        if args.as_json:
            sys.stdout.write(json.dumps(rec, indent=2, ensure_ascii=False) + "\n")
        else:
            keys = ", ".join(rec.get("keys") or [])
            print(f"Imported {rec['imported']}")
            if keys:
                print(f"Keys: {keys}")
            print("Kept for this run only.")
            print(f"Author: {rec['author']}")
        return 0

    if args.cmd == "export":
        from chronolock.jsonio import export_json

        try:
            rec = export_json(args.path)
        except (OSError, ValueError) as exc:
            return _read_failure(args.path, exc)
        if args.as_json:
            sys.stdout.write(json.dumps(rec, indent=2, ensure_ascii=False) + "\n")
        else:
            print(f"Wrote {rec['exported']}")
            print(f"Author: {rec['author']}")
        return 0

    parser.error(f"unknown command {args.cmd}")
    return 2


def staticclock_main(argv: Sequence[str] | None = None) -> int:
    """Deprecated ``staticclock`` console_scripts alias."""
    print(DEPRECATED_STATICCLOCK_LINE)
    return main(argv)


if __name__ == "__main__":
    raise SystemExit(main())
