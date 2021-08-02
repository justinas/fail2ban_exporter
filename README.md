# fail2ban_exporter
A wrapper for `fail2ban-client` go gather
[fail2ban](https://www.fail2ban.org/wiki/index.php/Main_Page) metrics and export
them for [Prometheus](https://prometheus.io/).

![Graph](example.PNG "graph")

## Exposed metrics

### Counters

- `fail2ban_<jail>_banned_total`
- `fail2ban_<jail>_failed_total`

### Gauges

- `fail2ban_<jail>_banned`
- `fail2ban_<jail>_failed`

## Installation
### Requirements
- fail2ban
- Python 3

### Setup
Run `install.sh` and fail2ban_exporter will be installed as a Systemd service.

## Enviroment variables
- **LISTEN_ADDRESS**. Default: `localhost`
- **LISTEN_PORT**. Default: `9180`
- **EXEC_PATH**. Default: `/usr/bin/`
