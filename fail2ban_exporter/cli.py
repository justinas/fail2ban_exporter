#!/usr/bin/env python3
"""Command-line entrypoint"""
import argparse
import logging
import os
import sys

from time import sleep

from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY

from .client import Fail2BanClient, Fail2BanClientError
from .collector import Collector


def main():
    """Command-line entrypoint"""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-a",
        "--addr",
        default=os.getenv("LISTEN_ADDRESS", "0.0.0.0"),
        help="Listen on this address",
    )
    parser.add_argument(
        "-p",
        "--port",
        default=int(os.getenv("LISTEN_PORT", "9180")),
        type=int,
        help="Listen on this port",
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Debug mode",
    )
    parser.add_argument(
        "-i",
        "--ignore-jail",
        action="append",
        dest="ignored_jails",
        default=[],
        help="Ignore a jail. This argument can appear many times.",
    )

    args = parser.parse_args()

    if args.debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    log_format = "%(asctime)s - %(levelname)-7s - %(message)s"
    logging.basicConfig(format=log_format, level=log_level)

    client = Fail2BanClient(args.ignored_jails)
    try:
        # Attempt to call fail2ban-client to check whether we are able to communicate
        # with the fail2ban server via the exposed socket
        client.status()
    except Fail2BanClientError as err:
        logging.error("Failed to communicate with fail2ban: %s", err)
        logging.warning(
            (
                "Please ensure the exporter is running with the appropriate privileges"
                " to communicate with the fail2ban server"
            )
        )
        sys.exit()

    REGISTRY.register(Collector(client))

    # Run HTTP server
    logging.info("Listening to http://%s:%d", args.addr, args.port)
    start_http_server(args.port, args.addr)
    while True:
        sleep(10)


if __name__ == "__main__":
    main()
