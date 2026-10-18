# logsleuth

A small command-line tool for parsing and triaging common server logs:
nginx access logs and Linux `auth.log` / `secure` files.

## Install

```bash
pip install log-sleuth
```

Or from a checkout:

```bash
pip install -e ".[dev]"
```

## Quick start

```bash
# Summarise an nginx access log
logsleuth stats access.log

# Show only 5xx responses
logsleuth filter access.log --status 5xx

# Export failed SSH logins as JSON
logsleuth export auth.log --type auth --format json
```

## Documentation

See [docs/usage.md](docs/usage.md) for every subcommand and the config file
format, and [CHANGELOG.md](CHANGELOG.md) for release notes.

## Contributing

Issues and PRs welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) first; AI
assistants should also read [AGENTS.md](AGENTS.md).

## Status

Alpha. The CLI surface may change before 1.0.
