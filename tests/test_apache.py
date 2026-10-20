import pytest

from logsleuth.parsers import apache
from tests.conftest import FIXTURES


def test_parse_basic_line():
    line = ('203.0.113.77 - - [18/Oct/2026:12:00:01 +0000] "GET /index.html HTTP/1.1" 200 3471 '
            '"-" "Mozilla/5.0"')
    entry = apache.parse_line(line)
    assert entry.ip == "203.0.113.77"
    assert entry.status == 200


def test_hostname_client_is_accepted():
    # HostnameLookups On produces a hostname in %h
    line = 'crawler.example.net - - [18/Oct/2026:12:01:30 +0000] "GET /robots.txt HTTP/1.1" 200 68 "-" "ExampleBot/1.0"'
    assert apache.parse_line(line).ip == "crawler.example.net"


def test_fixture_parses_fully():
    entries = list(apache.parse_file(FIXTURES / "apache_access.log"))
    assert len(entries) == 4
