from collections import Counter

from logsleuth import stats
from logsleuth.parsers import nginx


def test_count_by_groups_values():
    counter = stats.count_by(["a", "b", "a", "c", "a"], key=lambda x: x)
    assert counter == Counter({"a": 3, "b": 1, "c": 1})


def test_top_n_orders_highest_first():
    counter = Counter({"a": 3, "b": 5, "c": 1})
    ranked = stats.top_n(counter, 2)
    assert ranked[0] == ("b", 5)


def test_top_n_zero_returns_empty():
    assert stats.top_n(Counter({"a": 1}), 0) == []


def test_status_classes(access_log):
    classes = stats.status_classes(nginx.parse_file(access_log))
    assert classes["2xx"] == 7
    assert classes["3xx"] == 1
    assert classes["4xx"] == 4
    assert classes["5xx"] == 3


def test_summarize_access(access_log):
    summary = stats.summarize_access(nginx.parse_file(access_log))
    assert summary["requests"] == 15
    assert summary["unique_ips"] == 5
    assert summary["bytes_sent"] > 0
    assert summary["top_ips"][0][0] in {"192.0.2.44", "203.0.113.10"}
