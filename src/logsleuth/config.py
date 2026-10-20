"""User configuration loaded from ``~/.logsleuth.toml``.

Supported keys::

    default_type = "nginx"   # fallback when --type is omitted and detection fails
    default_format = "json"  # export format
    top = 10                 # size of top-N tables in stats output
"""

from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Any, Dict, Optional, Union

DEFAULT_PATH = "~/.logsleuth.toml"

DEFAULTS: Dict[str, Any] = {
    "default_type": None,
    "default_format": "json",
    "top": 10,
}


def load_config(path: Optional[Union[str, Path]] = None) -> Dict[str, Any]:
    """Return DEFAULTS merged with whatever the config file provides."""
    config_path = Path(path or DEFAULT_PATH)
    merged = dict(DEFAULTS)
    if not config_path.exists():
        return merged
    with open(config_path, "rb") as handle:
        merged.update(tomllib.load(handle))
    return merged
