import json

import pytest

from logsleuth import export
from logsleuth.parsers import nginx


def test_to_json_is_list_of_dicts(access_log):
    data = json.loads(export.to_json(nginx.parse_file(access_log)))
    assert isinstance(data, list)
    assert len(data) == 15
    assert data[0]["status"] == 200


def test_to_csv_header_and_rows(access_log):
    text = export.to_csv(nginx.parse_file(access_log))
    lines = text.splitlines()
    assert lines[0].startswith("ip,user,time,method,path")
    assert len(lines) == 16


def test_to_csv_empty():
    assert export.to_csv([]) == ""


def test_render_unknown_format():
    with pytest.raises(ValueError):
        export.render([], "yaml")
