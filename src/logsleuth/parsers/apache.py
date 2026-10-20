"""Parser for Apache httpd ``combined`` LogFormat.

Differences from nginx that still need handling (see #9):
- ``%h`` may be a hostname when HostnameLookups is On
- ``%u`` may be quoted and contain spaces
- ``%b`` is ``-`` for zero-byte responses (same as nginx)
"""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Iterator, Union

from logsleuth.parsers.nginx import TIME_FORMAT, AccessEntry, ParseError

# TODO: %h hostnames, quoted %u. Currently identical to the nginx regex.
LINE_RE = re.compile(
    r"^(?P<host>\d{1,3}(?:\.\d{1,3}){3}) (?P<ident>\S+) (?P<user>\S+) \[(?P<time>[^\]]+)\] "
    r'"(?P<method>[A-Z]+) (?P<path>\S+) (?P<proto>[^"]+)" '
    r"(?P<status>\d{3}) (?P<bytes>\d+|-) "
    r'"(?P<referer>[^"]*)" "(?P<ua>[^"]*)"$'
)


def parse_line(line: str) -> AccessEntry:
    match = LINE_RE.match(line.rstrip("\r\n"))
    if match is None:
        raise ParseError(f"unrecognised apache access line: {line!r}")
    raw_bytes = match["bytes"]
    return AccessEntry(
        ip=match["host"],
        user=match["user"],
        time=datetime.strptime(match["time"], TIME_FORMAT),
        method=match["method"],
        path=match["path"],
        protocol=match["proto"],
        status=int(match["status"]),
        bytes_sent=0 if raw_bytes == "-" else int(raw_bytes),
        referer=match["referer"],
        user_agent=match["ua"],
    )


def parse_file(path: Union[str, Path]) -> Iterator[AccessEntry]:
    with open(path, encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if line.strip():
                yield parse_line(line)
