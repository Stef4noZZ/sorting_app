"""ANSI terminal color codes."""

from __future__ import annotations

import os
import sys
from enum import Enum


class Color(str, Enum):
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"


def _colors_enabled() -> bool:
    if os.environ.get("NO_COLOR"):
        return False
    return sys.stdout.isatty()


def paint(text: str, color: Color) -> str:
    if not _colors_enabled():
        return text
    return f"{color.value}{text}{Color.RESET.value}"
