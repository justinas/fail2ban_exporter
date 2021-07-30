#!/usr/bin/env python3
"""Command-line entrypoint"""
import argparse
import os

from time import sleep

from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY

from .client import Fail2BanClient
from .collector import Collector


ADDR = os.getenv("LISTEN_ADDRESS", "localhost")
PORT = int(os.getenv("LISTEN_PORT", "9180"))


def main():
    """Command-line entrypoint"""
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-ij",
        "--ignore-jail",
        action="append",
        dest="ignored_jails",
        default=[],
        help="Ignore a jail. This argument can appear many times.",
    )
    args = parser.parse_args()

    client = Fail2BanClient(args.ignored_jails)

    # Run HTTP server
    start_http_server(PORT, ADDR)
    REGISTRY.register(Collector(client))
    while True:
        sleep(10)


if __name__ == "__main__":
    main()
