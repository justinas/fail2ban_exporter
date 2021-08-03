"""Prometheus collector for fail2ban metrics - unitary tests"""
from typing import List
from unittest.mock import MagicMock

from prometheus_client.metrics_core import Metric

from fail2ban_exporter.client import Fail2BanClient
from fail2ban_exporter.collector import Collector
from fail2ban_exporter.jail_stats import JailStats


def test_collect():
    """Collect fail2ban jail metrics"""
    client = Fail2BanClient(ignored_jails=[])
    client.jails = MagicMock(return_value=["apache2", "sshd"])
    client.jail_stats = MagicMock(
        side_effect=[
            JailStats(
                jail="apache2",
                banned=7,
                banned_total=75,
                failed=46,
                failed_total=163,
            ),
            JailStats(
                jail="sshd",
                banned=41,
                banned_total=213,
                failed=146,
                failed_total=297,
            ),
        ]
    )

    collector = Collector(client)
    metrics = list(collector.collect())

    assert len(metrics) == 8

    assert get_sample_value(metrics, "fail2ban_apache2_banned") == 7
    assert get_sample_value(metrics, "fail2ban_apache2_failed") == 46
    assert get_sample_value(metrics, "fail2ban_apache2_banned_total") == 75
    assert get_sample_value(metrics, "fail2ban_apache2_failed_total") == 163

    assert get_sample_value(metrics, "fail2ban_sshd_banned") == 41
    assert get_sample_value(metrics, "fail2ban_sshd_failed") == 146
    assert get_sample_value(metrics, "fail2ban_sshd_banned_total") == 213
    assert get_sample_value(metrics, "fail2ban_sshd_failed_total") == 297


def get_sample_value(metrics: List[Metric], name: str):
    """Retrieve the sample value for a given metric

    Inspired by the test utility provided by
    prometheus_client.registry.CollectorRegistry.get_sample_value()
    """
    for metric in metrics:
        for sample in metric.samples:
            if sample.name == name:
                return sample.value
    return None
