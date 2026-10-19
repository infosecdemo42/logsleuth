"""Serialise parsed entries to JSON or CSV."""

from __future__ import annotations

import json
from typing import Iterable, List

FORMATS = ("json", "jsonl", "csv")


def to_json(entries: Iterable, indent: int = 2) -> str:
    return json.dumps([e.to_dict() for e in entries], indent=indent)


def to_jsonl(entries: Iterable) -> str:
    """One compact JSON object per line (JSON Lines / ndjson)."""
    return "\n".join(json.dumps(e.to_dict(), separators=(",", ":")) for e in entries)


def to_csv(entries: Iterable) -> str:
    rows: List[str] = []
    header_written = False
    for entry in entries:
        data = entry.to_dict()
        if not header_written:
            rows.append(",".join(data.keys()))
            header_written = True
        rows.append(",".join("" if v is None else str(v) for v in data.values()))
    return "\n".join(rows) + ("\n" if rows else "")


def render(entries: Iterable, fmt: str) -> str:
    if fmt == "json":
        return to_json(entries)
    if fmt == "jsonl":
        return to_jsonl(entries)
    if fmt == "csv":
        return to_csv(entries)
    raise ValueError(f"unknown format {fmt!r}; expected one of {FORMATS}")
