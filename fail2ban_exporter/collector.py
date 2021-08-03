"""Prometheus collector for fail2ban metrics"""
import logging
from typing import Iterator

from prometheus_client.core import CounterMetricFamily, GaugeMetricFamily
from prometheus_client.metrics_core import Metric

from .client import Fail2BanClient

PREFIX = "fail2ban"


class Collector:
    """Collect fail2ban jail stats and expose them as Prometheus metrics"""

    # pylint: disable=too-few-public-methods

    def __init__(self, client: Fail2BanClient):
        self.client = client

    def collect(self) -> Iterator[Metric]:
        """Retrieve fail2ban jail stats"""
        logging.debug("Collecting metrics")

        for jail in self.client.jails():
            logging.debug("Collecting metrics for jail: %s", jail)
            jail_stats = self.client.jail_stats(jail)
            jail_prefix = f"{PREFIX}_{snake_case(jail)}"

            # Counters
            yield CounterMetricFamily(
                f"{jail_prefix}_banned_total",
                f"Banned IPs for the {jail} jail",
                jail_stats.banned_total,
            )
            yield CounterMetricFamily(
                f"{jail_prefix}_failed_total",
                f"Failed authentication attempts for the {jail} jail",
                jail_stats.failed_total,
            )

            # Gauges
            yield GaugeMetricFamily(
                f"{jail_prefix}_banned",
                f"Banned IPs for the {jail} jail",
                jail_stats.banned,
            )
            yield GaugeMetricFamily(
                f"{jail_prefix}_failed",
                f"Failed authentication attempts for the {jail} jail",
                jail_stats.failed,
            )


def snake_case(text):
    """Normalize text to snake_case"""
    return text.strip().replace("-", "_").replace(" ", "_").lower()
