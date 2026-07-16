"""Parser for nginx access logs in the default ``combined`` format."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterator, Union

# Default nginx "combined" log format:
# $remote_addr - $remote_user [$time_local] "$request" $status $body_bytes_sent
#   "$http_referer" "$http_user_agent"
LINE_RE = re.compile(
    r"^(?P<ip>\d{1,3}(?:\.\d{1,3}){3}) - (?P<user>\S+) \[(?P<time>[^\]]+)\] "
    r'"(?P<method>[A-Z]+) (?P<path>\S+) (?P<proto>[^"]+)" '
    r"(?P<status>\d{3}) (?P<bytes>\d+|-) "
    r'"(?P<referer>[^"]*)" "(?P<ua>[^"]*)"$'
)

TIME_FORMAT = "%d/%b/%Y:%H:%M:%S %z"


class ParseError(ValueError):
    """Raised when a line does not match the expected log format."""


@dataclass(frozen=True)
class AccessEntry:
    ip: str
    user: str
    time: datetime
    method: str
    path: str
    protocol: str
    status: int
    bytes_sent: int
    referer: str
    user_agent: str

    def to_dict(self) -> dict:
        return {
            "ip": self.ip,
            "user": self.user,
            "time": self.time.isoformat(),
            "method": self.method,
            "path": self.path,
            "protocol": self.protocol,
            "status": self.status,
            "bytes_sent": self.bytes_sent,
            "referer": self.referer,
            "user_agent": self.user_agent,
        }


def parse_line(line: str) -> AccessEntry:
    """Parse one access-log line. Raises :class:`ParseError` on mismatch."""
    match = LINE_RE.match(line.rstrip("\r\n"))
    if match is None:
        raise ParseError(f"unrecognised nginx access line: {line!r}")
    raw_bytes = match["bytes"]
    return AccessEntry(
        ip=match["ip"],
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
    """Yield an :class:`AccessEntry` for every non-blank line in *path*."""
    with open(path, encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if line.strip():
                yield parse_line(line)
