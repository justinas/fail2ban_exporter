# fail2ban_exporter

A wrapper for `fail2ban-client` go gather
[fail2ban](https://www.fail2ban.org/wiki/index.php/Main_Page) metrics and export
them for [Prometheus](https://prometheus.io/).

![Graph](example.PNG "graph")

## Exposed metrics

For each enabled fail2ban jail, the following metrics will be exposed:

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

## Usage
### Command-line interface

```shell
$ fail2ban_exporter --help

usage: fail2ban_exporter [-h] [-a ADDR] [-p PORT] [-d] [-i IGNORED_JAILS]

optional arguments:
  -h, --help            show this help message and exit
  -a ADDR, --addr ADDR  Listen on this address
  -p PORT, --port PORT  Listen on this port
  -d, --debug           Debug mode
  -i IGNORED_JAILS, --ignore-jail IGNORED_JAILS
                        Ignore a jail. This argument can appear many times.
```

### Enviroment variables

- `LISTEN_ADDRESS`. Default: `0.0.0.0`
- `LISTEN_PORT`. Default: `9180`
- `EXEC_PATH`. Default: `/usr/bin/`

## Development
### Option 1: Run linters and tests with Tox
Install Tox:

```shell
$ sudo apt update
$ sudo apt install tox
```

Run Tox tasks for a given Python environment:

```shell
$ tox -e py39
```

Run Tox tasks for a given Python environment and force its (re)creation:


```shell
$ tox -e py39 -r
```

Run Tox task for bump and pin Python test dependency versions:


```shell
$ tox -e pippin
$ git commit -am "Bump test dependencies"
```

### Option 2: Run linters and tests in a Python virtual environment

Create and activate a Python virtualenv:

```shell
$ python3 -m venv ~/.local/share/virtualenvs/fail2ban_exporter
$ source ~/.local/share/virtualenvs/fail2ban_exporter/bin/activate
```

Install `fail2ban_exporter` in development mode; this will create a symlink to
the local development workspace:

```shell
$ python setup.py develop
```

Install lint and test dependencies:

```shell
$ pip install -r requirements_tests.txt
```

Run linters:

```shell
$ black --check --diff
$ pytest --pylint
```

Run unitary tests and show code coverage:

```shell
$ pytest --cov=fail2ban_exporter
```
