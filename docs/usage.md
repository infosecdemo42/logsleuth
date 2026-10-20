# Usage

All commands take a log file path. The log type is guessed from the filename
(`auth.log` / `secure` -> `auth`, everything else -> `nginx`) and can be forced
with `--type`.

## parse

Print every entry as one JSON object per line.

```bash
logsleuth parse /var/log/nginx/access.log
logsleuth parse /var/log/auth.log --type auth
```

## stats

Summarise a file. For nginx logs you get request counts, bytes, status classes
and top IPs / paths. For auth logs you get failed vs accepted logins and the
noisiest source addresses.

```bash
logsleuth stats access.log
```

## filter

Print matching entries only. Exit status is 1 when nothing matched, which makes
it usable in shell conditionals.

```bash
logsleuth filter access.log --status 5xx
logsleuth filter access.log --status 400-499 --ip 192.0.2.44
logsleuth filter auth.log --contains "Failed password"
```

## export

Write entries to JSON (default), JSON Lines (`jsonl`, one object per line) or CSV.

```bash
logsleuth export access.log --format csv -o access.csv
logsleuth export access.log --format jsonl | jq -c 'select(.status >= 500)'
```

## Configuration

Optional `~/.logsleuth.toml`:

```toml
default_type = "nginx"
default_format = "csv"
top = 20
```

Use `--config PATH` to point at a different file.
