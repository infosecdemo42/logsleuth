import pytest

from logsleuth.parsers import syslog

FAILED = "Aug  3 06:31:05 bastion sshd[2410]: Failed password for invalid user admin from 198.51.100.23 port 41022 ssh2"
SUDO = "Aug  3 07:02:44 bastion sudo:   deploy : TTY=pts/0 ; PWD=/home/deploy ; USER=root ; COMMAND=/usr/bin/systemctl restart nginx"


def test_parse_line_fields():
    entry = syslog.parse_line(FAILED)
    assert entry.host == "bastion"
    assert entry.process == "sshd"
    assert entry.pid == 2410
    assert entry.time.month == 8
    assert entry.time.day == 3
    assert (entry.time.hour, entry.time.minute, entry.time.second) == (6, 31, 5)
    assert entry.message.startswith("Failed password")


def test_process_without_pid():
    entry = syslog.parse_line(SUDO)
    assert entry.process == "sudo"
    assert entry.pid is None
    assert "COMMAND=/usr/bin/systemctl" in entry.message


def test_failed_login_extraction():
    info = syslog.parse_line(FAILED).failed_login
    assert info == {"user": "admin", "ip": "198.51.100.23", "port": 41022}


def test_accepted_login_extraction(auth_log):
    accepted = [e.accepted_login for e in syslog.parse_file(auth_log) if e.accepted_login]
    assert {a["user"] for a in accepted} == {"deploy", "alice"}


def test_non_auth_message_has_no_login_info():
    assert syslog.parse_line(SUDO).failed_login is None
    assert syslog.parse_line(SUDO).accepted_login is None


def test_garbage_raises():
    with pytest.raises(syslog.ParseError):
        syslog.parse_line("nope")


def test_parse_file_counts(auth_log):
    entries = list(syslog.parse_file(auth_log))
    assert len(entries) == 20
    assert sum(1 for e in entries if e.failed_login) == 7


def test_year_rollover_for_december_read_in_january():
    from datetime import datetime

    line = "Dec 31 23:59:58 bastion sshd[10]: Accepted publickey for deploy from 203.0.113.42 port 1 ssh2"
    entry = syslog.parse_line(line, now=datetime(2027, 1, 2, 8, 0, 0))
    assert entry.time.year == 2026


def test_same_month_uses_current_year():
    from datetime import datetime

    entry = syslog.parse_line(FAILED, now=datetime(2026, 8, 20))
    assert entry.time.year == 2026
