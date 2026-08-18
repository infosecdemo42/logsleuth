"""Command-line entry point for logsleuth."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Iterable, Optional, Sequence

from logsleuth import config, export, stats
from logsleuth.parsers import nginx, syslog


def detect_type(path: Path) -> str:
    """Guess the log type from the filename."""
    name = path.name.lower()
    if "auth" in name or "secure" in name:
        return "auth"
    return "nginx"


def load_entries(path: Path, log_type: str) -> Iterable:
    if log_type == "nginx":
        return nginx.parse_file(path)
    if log_type == "auth":
        return syslog.parse_file(path)
    raise SystemExit(f"unsupported log type: {log_type}")


def cmd_parse(args: argparse.Namespace) -> int:
    for entry in load_entries(args.path, args.type or detect_type(args.path)):
        print(json.dumps(entry.to_dict()))
    return 0


def cmd_stats(args: argparse.Namespace) -> int:
    log_type = args.type or detect_type(args.path)
    entries = load_entries(args.path, log_type)
    if log_type == "auth":
        summary = stats.summarize_auth(entries)
    else:
        summary = stats.summarize_access(entries)
    print(json.dumps(summary, indent=2))
    return 0


def cmd_export(args: argparse.Namespace) -> int:
    entries = load_entries(args.path, args.type or detect_type(args.path))
    text = export.render(entries, args.format)
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="logsleuth",
        description="Parse and triage common server logs.",
    )
    parser.add_argument(
        "--config", dest="config_path", type=Path, default=None,
        help=f"config file (default: {config.DEFAULT_PATH})",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_parse = sub.add_parser("parse", help="print each entry as JSON")
    p_parse.add_argument("path", type=Path)
    p_parse.add_argument("--type", choices=["nginx", "auth"], default=None)
    p_parse.set_defaults(func=cmd_parse)

    p_stats = sub.add_parser("stats", help="summarise a log file")
    p_stats.add_argument("path", type=Path)
    p_stats.add_argument("--type", choices=["nginx", "auth"], default=None)
    p_stats.set_defaults(func=cmd_stats)

    p_export = sub.add_parser("export", help="write entries as JSON or CSV")
    p_export.add_argument("path", type=Path)
    p_export.add_argument("--type", choices=["nginx", "auth"], default=None)
    p_export.add_argument("--format", choices=export.FORMATS, default="json")
    p_export.add_argument("-o", "--output", type=Path, default=None)
    p_export.set_defaults(func=cmd_export)

    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.config = config.load_config(getattr(args, "config_path", None))
    if getattr(args, "type", None) is None and args.config["default_type"]:
        args.type = args.config["default_type"]
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
