# fritz_logextractor

Reads the event log of AVM Fritz! devices over TR-064 and writes each new entry once, as a
structured log line, so a log stack (Loki, Elasticsearch, journald, …) can keep it.

The Fritz!Box keeps its event log in RAM: a reboot or a firmware update empties it, and the box
has no syslog push. This tool polls the log and forwards what is new.

> **Status: early scaffold.** Configuration and tooling are in place; the extraction itself is
> not implemented yet. See [AGENTS.md](AGENTS.md) for the planned design.

Companion to [fritz_exporter](https://github.com/pdreker/fritz_exporter), which exports the
device's metrics to Prometheus.

## Configuration

Either a YAML file (`--config`, several devices) or environment variables (one device).

| YAML key | Environment variable | Default |
|---|---|---|
| `log_level` | `FRITZ_LOG_LEVEL` | `INFO` |
| `poll_interval` | `FRITZ_POLL_INTERVAL` | `60` (seconds, at least 10) |
| `state_dir` | `FRITZ_STATE_DIR` | `/var/lib/fritzlogextractor` |
| `devices[].hostname` | `FRITZ_HOSTNAME` | `fritz.box` |
| `devices[].name` | `FRITZ_NAME` | `Fritz!Box` (env) |
| `devices[].username` | `FRITZ_USERNAME` | *(required)* |
| `devices[].password` | `FRITZ_PASSWORD` | *(required unless password_file is set)* |
| `devices[].password_file` | `FRITZ_PASSWORD_FILE` | |
| `devices[].connection_timeout` | `FRITZ_CONNECTION_TIMEOUT` | `10` (`0` disables it) |
| `devices[].use_tls` | `FRITZ_USE_TLS` | `false` |

Use a separate Fritz!Box user for the tool, with a long random password: TR-064 logs in with
MD5 digest authentication.

## Development

```bash
uv sync --all-groups
uv run ruff check . && uv run ruff format --check .
uv run ty check
uv run pytest
```

## License

Apache License 2.0, see [LICENSE.md](LICENSE.md).
