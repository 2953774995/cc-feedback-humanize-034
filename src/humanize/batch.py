"""Batch formatting under one convention per unit kind.

Single-value helpers such as `humanize.naturalsize` format one value at a
time and have no notion of an unsupported unit. This module drives those
helpers over a batch of ``(value, unit)`` pairs and records any unit for
which no formatter is registered, instead of raising.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import NamedTuple

from humanize.filesize import naturalsize
from humanize.time import naturaldelta


class BatchResult(NamedTuple):
    """Outcome of a `format_many` call.

    Attributes:
        texts: Formatted result per input item, in the same order. Entries
            whose unit is unsupported are empty strings; see `unknown`.
        unknown: Names of units without a registered formatter, in the
            order of their first occurrence (deduplicated).
    """

    texts: list[str]
    unknown: list[str]


# One formatter per supported unit name. The formatter receives the raw
# value and returns the display text, so every value of a given unit kind
# follows the same convention.
_FORMATTERS: dict[str, Callable[[float], str]] = {
    "bytes": naturalsize,
    "seconds": naturaldelta,
}


def format_many(items: list[tuple[float, str]]) -> BatchResult:
    """Format a batch of ``(value, unit)`` pairs with one convention per unit.

    Args:
        items: Pairs of a numeric value and a unit name. Supported units are
            ``"bytes"`` (via `humanize.naturalsize`) and ``"seconds"`` (via
            `humanize.naturaldelta`); other unit names are recorded rather
            than raised on.

    Returns:
        BatchResult: The formatted texts (aligned with `items` by index) and
        the list of unsupported unit names encountered.
    """
    texts: list[str] = []
    unknown: list[str] = []
    for value, unit in items:
        formatter = _FORMATTERS.get(unit)
        if formatter is None:
            texts.append("")
            if unit not in unknown:
                unknown.append(unit)
        else:
            texts.append(formatter(value))
    return BatchResult(texts=texts, unknown=unknown)
