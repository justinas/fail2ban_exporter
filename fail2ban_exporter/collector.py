"""Prometheus collector for fail2ban metrics"""
import os
import re
from subprocess import PIPE, run

from prometheus_client.core import GaugeMetricFamily

CMD = os.path.join(os.getenv("EXEC_PATH", "/usr/bin/"), "fail2ban-client")
COMP = re.compile(r"\s([a-zA-Z\s]+):\t([a-zA-Z0-9-,\s]+)\n")


class GaugeCollector:
    """Collect fail2ban jail stats and expose them as Prometheus metrics"""

    def __init__(self, ignored_jails):
        self.ignored_jails = ignored_jails

    def collect(self):
        """Retrieve fail2ban jail stats"""
        for jail in self.get_jails():
            gauge = GaugeMetricFamily(
                "fail2ban_{}".format(snake_case(jail)), "", labels=["type"]
            )
            for label, value in self.extract_data(jail):
                gauge.add_metric([snake_case(label)], float(value))
            yield gauge

    def get_jails(self):
        """Retrieve a list of fail2ban jails"""
        result = run([CMD, "status"], stdout=PIPE, check=True)

        matches = re.search(
            r"Jail list:\s*([a-z\-, ]*)\n", result.stdout.decode("utf-8")
        )
        if not matches:
            return []

        return [
            jail
            for jail in matches.group(1).split(", ")
            if jail not in self.ignored_jails
        ]

    @staticmethod
    def extract_data(jail):
        """Parse fail2ban jail stats and extract relevant metrics"""
        args = [CMD, "status"]
        if jail:
            args.append(jail)

        result = run(args, stdout=PIPE, check=True)

        return re.findall(COMP, result.stdout.decode("utf-8"))


def snake_case(text):
    """Normalize text to snake_case"""
    return text.strip().replace("-", "_").replace(" ", "_").lower()
