from logsleuth import config


def test_missing_file_returns_defaults(tmp_path):
    assert config.load_config(tmp_path / "nope.toml") == config.DEFAULTS


def test_file_overrides_defaults(tmp_path):
    cfg = tmp_path / "logsleuth.toml"
    cfg.write_text('default_format = "csv"\ntop = 3\n')
    loaded = config.load_config(cfg)
    assert loaded["default_format"] == "csv"
    assert loaded["top"] == 3
    assert loaded["default_type"] is None
