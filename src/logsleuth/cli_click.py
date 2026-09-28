"""Experimental click-based CLI. Mirrors cli.py; not yet the console entry point."""

from pathlib import Path

import click

from logsleuth import cli as legacy


@click.group()
@click.option("--config", "config_path", type=click.Path(path_type=Path), default=None)
@click.pass_context
def main(ctx: click.Context, config_path):
    ctx.obj = {"config_path": config_path}


def _common(f):
    f = click.argument("path", type=click.Path(exists=True, path_type=Path))(f)
    f = click.option("--type", "log_type", type=click.Choice(["nginx", "auth"]), default=None)(f)
    return f


@main.command()
@_common
def parse(path, log_type):
    legacy.main(["parse", str(path)] + (["--type", log_type] if log_type else []))


@main.command()
@_common
def stats(path, log_type):
    legacy.main(["stats", str(path)] + (["--type", log_type] if log_type else []))
