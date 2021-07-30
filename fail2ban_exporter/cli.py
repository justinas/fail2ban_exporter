#!/usr/bin/env python3
"""Command-line entrypoint"""
import argparse
import os

from time import sleep

from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY

from .collector import GaugeCollector


ADDR = os.getenv("LISTEN_ADDRESS", "localhost")
PORT = int(os.getenv("LISTEN_PORT", 9180))


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

    # Run HTTP server
    start_http_server(PORT, ADDR)
    REGISTRY.register(GaugeCollector(args.ignored_jails))
    while True:
        sleep(10)


if __name__ == "__main__":
    main()
