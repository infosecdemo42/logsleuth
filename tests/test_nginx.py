from datetime import timezone

import pytest

from logsleuth.parsers import nginx

SAMPLE = (
    '203.0.113.10 - - [12/Jul/2026:10:15:01 +0000] "GET / HTTP/1.1" 200 5123 '
    '"-" "Mozilla/5.0 (X11; Linux x86_64) Firefox/128.0"'
)


def test_parse_line_fields():
    entry = nginx.parse_line(SAMPLE)
    assert entry.ip == "203.0.113.10"
    assert entry.user == "-"
    assert entry.method == "GET"
    assert entry.path == "/"
    assert entry.protocol == "HTTP/1.1"
    assert entry.status == 200
    assert entry.bytes_sent == 5123
    assert entry.referer == "-"
    assert entry.user_agent.startswith("Mozilla/5.0")
    assert entry.time.year == 2026
    assert entry.time.tzinfo is not None
    assert entry.time.utcoffset() == timezone.utc.utcoffset(None)


def test_dash_bytes_becomes_zero():
    line = SAMPLE.replace(" 200 5123 ", " 502 - ")
    entry = nginx.parse_line(line)
    assert entry.status == 502
    assert entry.bytes_sent == 0


def test_authenticated_user():
    line = SAMPLE.replace("- - [", "- alice [")
    assert nginx.parse_line(line).user == "alice"


def test_garbage_line_raises():
    with pytest.raises(nginx.ParseError):
        nginx.parse_line("this is not a log line")


def test_parse_file_counts(access_log):
    entries = list(nginx.parse_file(access_log))
    assert len(entries) == 15
    assert {e.status for e in entries} == {200, 302, 404, 500, 502}


def test_to_dict_roundtrip_keys():
    data = nginx.parse_line(SAMPLE).to_dict()
    assert set(data) == {
        "ip", "user", "time", "method", "path", "protocol",
        "status", "bytes_sent", "referer", "user_agent",
    }
