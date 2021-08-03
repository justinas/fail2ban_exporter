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

        banned_total = CounterMetricFamily(
            f"{PREFIX}_banned_total",
            "Banned IPs for the given jail",
            labels=["jail"],
        )

        failed_total = CounterMetricFamily(
            f"{PREFIX}_failed_total",
            "Failed authentication attempts for the given jail",
            labels=["jail"],
        )

        banned = GaugeMetricFamily(
            f"{PREFIX}_banned",
            "Banned IPs for the given jail",
            labels=["jail"],
        )
        failed = GaugeMetricFamily(
            f"{PREFIX}_failed",
            "Failed authentication attempts for the given jail",
            labels=["jail"],
        )

        for jail in self.client.jails():
            logging.debug("Collecting metrics for jail: %s", jail)
            jail_stats = self.client.jail_stats(jail)

            banned_total.add_metric([jail], jail_stats.banned_total)
            failed_total.add_metric([jail], jail_stats.failed_total)

            banned.add_metric([jail], jail_stats.banned)
            failed.add_metric([jail], jail_stats.failed)

        yield banned_total
        yield failed_total
        yield banned
        yield failed


def snake_case(text):
    """Normalize text to snake_case"""
    return text.strip().replace("-", "_").replace(" ", "_").lower()
