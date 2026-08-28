#!/usr/bin/env python3
"""One advisory, then forget. No network. No store of past advisories."""

from __future__ import annotations

from chronolock.engine import ChronoLock


def main() -> None:
    clock = ChronoLock()
    try:
        adv = clock.advise("Indiana")
        print(adv.to_text())
    finally:
        clock.forget()
    assert clock.last_inputs is None
    print("forgotten")


if __name__ == "__main__":
    main()
