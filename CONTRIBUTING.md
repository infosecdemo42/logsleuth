# Contributing

Thanks for helping out. A few ground rules keep the project easy to maintain.

## Workflow

1. Open or claim an issue before starting non-trivial work.
2. Branch from `main` using `fix/<topic>`, `feat/<topic>`, `docs/<topic>` or `chore/<topic>`.
3. Keep PRs focused. One logical change per PR.
4. Every behaviour change needs a test. Bug fixes need a regression test that fails before the fix.
5. Run `pytest` locally before pushing. CI must be green before merge.
6. Reference the issue in the PR body (`Closes #123`).

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## Style

- Standard library only for runtime dependencies.
- Type hints on public functions.
- Parsers must never silently drop lines: raise `ParseError` and let the caller decide.

## Reporting security issues

Please do not open public issues for vulnerabilities. Email the maintainer instead.
