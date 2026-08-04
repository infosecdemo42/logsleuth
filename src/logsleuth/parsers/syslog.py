"""Parser for traditional BSD-syslog formatted files such as ``/var/log/auth.log``."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterator, Optional, Union

# "Oct 20 14:03:11 bastion sshd[1234]: Failed password for invalid user admin from 203.0.113.5 port 51234 ssh2"
LINE_RE = re.compile(
    r"^(?P<mon>[A-Z][a-z]{2}) +(?P<day>\d{1,2}) (?P<time>\d{2}:\d{2}:\d{2}) "
    r"(?P<host>\S+) (?P<proc>[^\[:\s]+)(?:\[(?P<pid>\d+)\])?: (?P<msg>.*)$"
)

FAILED_RE = re.compile(
    r"Failed (?:password|publickey) for (?:invalid user )?(?P<user>\S+) from (?P<ip>\S+) port (?P<port>\d+)"
)
ACCEPTED_RE = re.compile(
    r"Accepted (?:password|publickey) for (?P<user>\S+) from (?P<ip>\S+) port (?P<port>\d+)"
)

MONTHS = {m: i for i, m in enumerate(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], start=1
)}


class ParseError(ValueError):
    """Raised when a line does not match the expected syslog format."""


@dataclass(frozen=True)
class SyslogEntry:
    time: datetime
    host: str
    process: str
    pid: Optional[int]
    message: str

    def to_dict(self) -> dict:
        return {
            "time": self.time.isoformat(),
            "host": self.host,
            "process": self.process,
            "pid": self.pid,
            "message": self.message,
        }

    @property
    def failed_login(self) -> Optional[dict]:
        """If this is an sshd authentication failure, return user/ip/port."""
        match = FAILED_RE.search(self.message)
        if match is None:
            return None
        return {"user": match["user"], "ip": match["ip"], "port": int(match["port"])}

    @property
    def accepted_login(self) -> Optional[dict]:
        match = ACCEPTED_RE.search(self.message)
        if match is None:
            return None
        return {"user": match["user"], "ip": match["ip"], "port": int(match["port"])}


def _infer_year(month: int, now: Optional[datetime] = None) -> int:
    """BSD syslog timestamps carry no year; assume the current one."""
    now = now or datetime.now()
    return now.year


def parse_line(line: str, now: Optional[datetime] = None) -> SyslogEntry:
    match = LINE_RE.match(line.rstrip("\r\n"))
    if match is None:
        raise ParseError(f"unrecognised syslog line: {line!r}")
    month = MONTHS[match["mon"]]
    year = _infer_year(month, now)
    hour, minute, second = (int(x) for x in match["time"].split(":"))
    return SyslogEntry(
        time=datetime(year, month, int(match["day"]), hour, minute, second),
        host=match["host"],
        process=match["proc"],
        pid=int(match["pid"]) if match["pid"] else None,
        message=match["msg"],
    )


def parse_file(path: Union[str, Path]) -> Iterator[SyslogEntry]:
    with open(path, encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if line.strip():
                yield parse_line(line)
