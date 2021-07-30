"""Prometheus collector for fail2ban metrics"""
import os
import re
from subprocess import PIPE, run

from prometheus_client.core import GaugeMetricFamily

CMD = os.path.join(os.getenv("EXEC_PATH", "/usr/bin/"), "fail2ban-client")
COMP = re.compile(r"\s([a-zA-Z\s]+):\t([a-zA-Z0-9-,\s]+)\n")


class GaugeCollector(object):
    def __init__(self, ignored_jails):
        self.ignored_jails = ignored_jails

    def collect(self):
        for jail in self.get_jails():
            g = GaugeMetricFamily(
                "fail2ban_{}".format(self.snake_case(jail)), "", labels=["type"]
            )
            for label, value in self.extract_data(jail):
                g.add_metric([self.snake_case(label)], float(value))
            yield g

    def get_jails(self):
        r = run([CMD, "status"], stdout=PIPE, check=True)
        m = re.search(r"Jail list:\s*([a-z\-, ]*)\n", r.stdout.decode("utf-8"))
        if not m:
            return []
        return [
            jail for jail in m.group(1).split(", ") if jail not in self.ignored_jails
        ]

    def extract_data(self, jail):
        args = [CMD, "status"]
        if jail:
            args.append(jail)
        r = run(args, stdout=PIPE, check=True)
        return re.findall(COMP, r.stdout.decode("utf-8"))

    def snake_case(self, string):
        return string.strip().replace("-", "_").replace(" ", "_").lower()
