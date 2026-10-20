# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Changed
- **Breaking:** Python 3.11 or newer is now required (#12). The `tomli` fallback is gone.

## [0.2.0] - 2026-09-22

### Added
- `auth` log type: parser for BSD-syslog files such as `/var/log/auth.log` with
  sshd failed/accepted login extraction (`parsers/syslog.py`).
- `stats` now produces an auth-specific summary (failed logins, top failing IPs
  and users, accepted users).
- `filter` subcommand with `--ip`, `--status` (`404`, `4xx`, `400-499`) and
  `--contains`.
- `export` subcommand with `--format json|csv` and `-o`.
- User configuration from `~/.logsleuth.toml` (`default_type`, `default_format`,
  `top`) and a global `--config` flag.
- Usage docs, contributing guide, issue and PR templates.

### Fixed
- Syslog year inference across the December/January boundary (#1, #19).

## [0.1.0] - 2026-07-24

### Added
- nginx `combined` access-log parser.
- `parse` and `stats` subcommands.
- GitHub Actions CI on Python 3.11 and 3.12.

[Unreleased]: https://github.com/infosecdemo42/logsleuth/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/infosecdemo42/logsleuth/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/infosecdemo42/logsleuth/releases/tag/v0.1.0
