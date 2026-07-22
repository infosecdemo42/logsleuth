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
