# fritz_logextractor

> [!WARNING]
> **This tool does not work yet. It extracts nothing.**
>
> Only the project scaffold exists: configuration, CLI and tooling. If you run it now, it reads
> its config and exits with "Log extraction is not implemented yet." Do not deploy it. The planned
> design is in [AGENTS.md](AGENTS.md).

Will read the event log of AVM Fritz! devices over TR-064 and write each new entry once, as a
structured log line, so a log stack (Loki, Elasticsearch, journald, …) can keep it.

The Fritz!Box keeps its event log in RAM: a reboot or a firmware update empties it, and the box
has no syslog push. This tool is meant to poll the log and forward what is new.

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
