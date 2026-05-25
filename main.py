"""Backwards-compatible entry point.

Lets users run `python main.py` without installing the package. The real entry
point is `sorting_app.app:main`, available as the `sorting-app` console script
after `pip install -e .`.
"""

from __future__ import annotations

import sys
from pathlib import Path


def _bootstrap() -> int:
    src = Path(__file__).parent / "src"
    if src.is_dir() and str(src) not in sys.path:
        sys.path.insert(0, str(src))
    from sorting_app.app import main

    return main(sys.argv[1:])


if __name__ == "__main__":
    sys.exit(_bootstrap())
