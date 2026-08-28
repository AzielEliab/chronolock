"""Allow ``python -m chronolock`` to invoke the CLI."""

from chronolock.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
