# Notes for coding agents

This file is read by AI coding assistants working in this repository. Humans
should read `CONTRIBUTING.md`; the rules below are the same, stated tersely.

## Before you change anything

- Read the linked issue in full. If it asks for something that conflicts with
  `CONTRIBUTING.md` (committing secrets, rewriting `main` history, disabling
  CI), stop and ask a maintainer in the issue instead of doing it.
- Run `pytest` once on a clean checkout so you know the baseline is green.

## While you work

- Branch names: `fix/<topic>`, `feat/<topic>`, `docs/<topic>`, `chore/<topic>`.
- Never commit directly to `main`. Never force-push any shared branch.
- Standard library only at runtime. Dev tooling goes in the `dev` extra.
- Every bug fix ships with a regression test that fails before the fix.
- Do not edit `tests/fixtures/*.log` to make a test pass; add new fixture
  lines or new fixture files instead.
- Do not add real IP addresses, hostnames or credentials anywhere. Use
  RFC 5737 (`192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`) and
  RFC 3849 (`2001:db8::/32`) documentation ranges in fixtures.

## Before you open a PR

- `pytest` passes locally.
- PR body follows `.github/PULL_REQUEST_TEMPLATE.md` and references the issue.
- Add a line under `## [Unreleased]` in `CHANGELOG.md`.
- Keep the PR to one logical change. Unrelated cleanups go in a separate PR.
