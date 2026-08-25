import json

from logsleuth import cli


def test_detect_type_by_name(tmp_path):
    assert cli.detect_type(tmp_path / "access.log") == "nginx"
    assert cli.detect_type(tmp_path / "auth.log") == "auth"
    assert cli.detect_type(tmp_path / "secure") == "auth"


def test_parse_command_emits_json_lines(access_log, capsys):
    assert cli.main(["parse", str(access_log)]) == 0
    lines = capsys.readouterr().out.strip().splitlines()
    assert len(lines) == 15
    assert json.loads(lines[0])["ip"] == "203.0.113.10"


def test_stats_command(access_log, capsys):
    assert cli.main(["stats", str(access_log)]) == 0
    summary = json.loads(capsys.readouterr().out)
    assert summary["requests"] == 15


def test_stats_auth(auth_log, capsys):
    assert cli.main(["stats", str(auth_log)]) == 0
    summary = json.loads(capsys.readouterr().out)
    assert summary["failed_logins"] == 7
    assert summary["accepted_users"] == ["alice", "deploy"]


def test_export_csv_to_file(access_log, tmp_path):
    out = tmp_path / "out.csv"
    assert cli.main(["export", str(access_log), "--format", "csv", "-o", str(out)]) == 0
    assert out.read_text().splitlines()[0].startswith("ip,user,time")


def test_filter_by_status_class(access_log, capsys):
    assert cli.main(["filter", str(access_log), "--status", "5xx"]) == 0
    lines = capsys.readouterr().out.strip().splitlines()
    assert len(lines) == 3
    assert all(json.loads(l)["status"] >= 500 for l in lines)


def test_filter_no_match_exits_1(access_log, capsys):
    assert cli.main(["filter", str(access_log), "--ip", "203.0.113.99"]) == 1
    assert capsys.readouterr().out == ""


def test_status_spec_matching():
    assert cli._status_matches(404, "404")
    assert cli._status_matches(404, "4xx")
    assert cli._status_matches(404, "400-499")
    assert not cli._status_matches(500, "4xx")
