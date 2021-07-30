"""Prometheus collector for fail2ban metrics"""
from prometheus_client.core import GaugeMetricFamily

from .client import Fail2BanClient


class Collector:
    """Collect fail2ban jail stats and expose them as Prometheus metrics"""

    # pylint: disable=too-few-public-methods

    def __init__(self, client: Fail2BanClient):
        self.client = client

    def collect(self):
        """Retrieve fail2ban jail stats"""
        for jail in self.client.jails():
            gauge = GaugeMetricFamily(
                "fail2ban_{}".format(snake_case(jail)), "", labels=["type"]
            )
            for label, value in self.client.jail_stats(jail):
                gauge.add_metric([snake_case(label)], float(value))
            yield gauge


def snake_case(text):
    """Normalize text to snake_case"""
    return text.strip().replace("-", "_").replace(" ", "_").lower()
