# Async reader benchmark (2026-08-28)

1.2 GB synthetic access log, MacBook, Python 3.12.

| reader              | wall time |
|---------------------|-----------|
| `parse_file` (sync) | 41.8 s    |
| `aparse_file`       | 43.1 s    |

Regex matching is ~90% of the profile. Parking this unless we move parsing
to a C extension or multiprocessing.
