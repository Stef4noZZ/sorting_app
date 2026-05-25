"""Reusable input prompts and message helpers."""

from __future__ import annotations

from collections.abc import Sequence
from enum import Enum
from typing import TypeVar

from sorting_app.ui.colors import Color, paint

E = TypeVar("E", bound=Enum)


def show_info(message: str) -> None:
    print(paint(message, Color.CYAN))


def show_success(message: str) -> None:
    print(paint(message, Color.GREEN))


def show_warning(message: str) -> None:
    print(paint(message, Color.YELLOW))


def show_error(message: str) -> None:
    print(paint(message, Color.RED))


def confirm(prompt: str) -> bool:
    answer = input(f"{prompt} [y/N]: ").strip().lower()
    return answer in {"y", "yes"}


def prompt_int(prompt: str, *, minimum: int | None = None, maximum: int | None = None) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            show_warning(">> please enter a valid integer")
            continue
        if minimum is not None and value < minimum:
            show_warning(f">> value must be >= {minimum}")
            continue
        if maximum is not None and value > maximum:
            show_warning(f">> value must be <= {maximum}")
            continue
        return value


def choose_from_options(
    title: str,
    options: Sequence[tuple[str, str]],
    *,
    allow_back: bool = False,
) -> str | None:
    """Print a numbered menu and return the chosen option's key.

    Each option is a (key, label) tuple. When `allow_back`, "0" returns None.
    """
    print()
    print(paint(f">> {title}", Color.HEADER))
    for idx, (_, label) in enumerate(options, start=1):
        print(paint(f"{idx}. {label}", Color.BLUE))
    if allow_back:
        print(paint("0. back", Color.YELLOW))

    valid = {str(i): key for i, (key, _) in enumerate(options, start=1)}
    if allow_back:
        valid["0"] = "__back__"

    while True:
        raw = input("> ").strip().lower()
        if raw in valid:
            chosen = valid[raw]
            return None if chosen == "__back__" else chosen
        if raw in {key for key, _ in options}:
            return raw
        show_warning(">> wrong input, try again")


def choose_enum(title: str, enum_cls: type[E]) -> E:
    """Present an enum's members as a numbered list and return the choice."""
    options = [(member.name.lower(), member.name) for member in enum_cls]
    key = choose_from_options(title, options)
    assert key is not None  # allow_back=False
    return enum_cls[key.upper()]
