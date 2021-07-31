"""fail2ban-client wrapper - unitary tests"""
from typing import List
from unittest import mock

import pytest

from fail2ban_exporter.client import Fail2BanClient


@pytest.mark.parametrize(
    "stdout",
    [
        pytest.param("", id="empty status"),
        pytest.param(
            "Status\n|- Number of jail: 0\n`- Jail list:\n",
            id="no enabled jails",
        ),
        pytest.param(
            "Status\n|- Number of jail: 2\n`- Jail list:    apache2, sshd\n",
            id="two enabled jails",
        ),
    ],
)
def test_status(stdout: str):
    """fail2ban-client status <jail>"""
    client = Fail2BanClient(ignored_jails=[])

    # pylint: disable=protected-access
    client._run = mock.MagicMock(return_value=stdout)

    assert client.status() == stdout


@pytest.mark.parametrize(
    "ignored_jails, stdout, expected",
    [
        pytest.param([], "", [], id="empty status"),
        pytest.param(
            [],
            "Status\n|- Number of jail: 0\n`- Jail list:\n",
            [""],
            id="no enabled jails",
        ),
        pytest.param(
            [],
            "Status\n|- Number of jail: 1\n`- Jail list:    sshd\n",
            ["sshd"],
            id="one enabled jail",
        ),
        pytest.param(
            [],
            "Status\n|- Number of jail: 2\n`- Jail list:    apache, sshd\n",
            ["apache", "sshd"],
            id="two enabled jails",
        ),
        pytest.param(
            ["apache"],
            "Status\n|- Number of jail: 2\n`- Jail list:    apache, sshd\n",
            ["sshd"],
            id="two enabled jails, one ignored",
        ),
    ],
)
def test_jails(ignored_jails: List[str], stdout: str, expected: List[str]):
    """Retrieve jails from fail2ban-client status"""
    client = Fail2BanClient(ignored_jails=ignored_jails)

    # pylint: disable=protected-access
    client._run = mock.MagicMock(return_value=stdout)

    assert client.jails() == expected


@pytest.mark.parametrize(
    "stdout, expected",
    [
        pytest.param("", [], id="empty output"),
        pytest.param(
            (
                "Status for the jail: sshd\n"
                "|- Filter\n"
                "|  |- Currently failed:\t0\n"
                "|  |- Total failed:\t0\n"
                "|  `- File list:\t\n"
                "`- Actions\n"
                "   |- Currently banned:\t0\n"
                "   |- Total banned:\t0\n"
                "   `- Banned IP list:\n"
            ),
            [
                ("Currently failed", "0"),
                ("Total failed", "0"),
                ("Currently banned", "0"),
                ("Total banned", "0"),
            ],
            id="jail with no bans, no history",
        ),
        pytest.param(
            (
                "Status for the jail: sshd\n"
                "|- Filter\n"
                "|  |- Currently failed:\t0\n"
                "|  |- Total failed:\t0\n"
                "|  `- Journal matches:\t_SYSTEMD_UNIT=sshd.service + _COMM=sshd\n"
                "`- Actions\n"
                "   |- Currently banned:\t0\n"
                "   |- Total banned:\t0\n"
                "   `- Banned IP list:\n"
            ),
            [
                ("Currently failed", "0"),
                ("Total failed", "0"),
                ("Currently banned", "0"),
                ("Total banned", "0"),
            ],
            id="jail with no bans, no history, tailing systemd journal",
        ),
        pytest.param(
            (
                "Status for the jail: sshd\n"
                "|- Filter\n"
                "|  |- Currently failed:\t0\n"
                "|  |- Total failed:\t0\n"
                "|  `- File list:\t\n"
                "`- Actions\n"
                "   |- Currently banned:\t5\n"
                "   |- Total banned:\t5\n"
                "   `- Banned IP list:\t"
                "172.68.34.5 172.68.34.6 172.68.34.7 172.68.34.8 10.45.0.127\n"
            ),
            [
                ("Currently failed", "0"),
                ("Total failed", "0"),
                ("Currently banned", "5"),
                ("Total banned", "5"),
            ],
            id="jail with manual bans, no history",
        ),
        pytest.param(
            (
                "Status for the jail: sshd\n"
                "|- Filter\n"
                "|  |- Currently failed:\t1\n"
                "|  |- Total failed:\t9\n"
                "|  `- Journal matches:\t_SYSTEMD_UNIT=sshd.service + _COMM=sshd\n"
                "`- Actions\n"
                "   |- Currently banned:\t1\n"
                "   |- Total banned:\t1\n"
                "   `- Banned IP list:\t0.0.0.0\n"
            ),
            [
                ("Currently failed", "1"),
                ("Total failed", "9"),
                ("Currently banned", "1"),
                ("Total banned", "1"),
            ],
            id="jail with bans, history, tailing systemd journal",
        ),
    ],
)
def test_jail_stats(stdout: str, expected: List[str]):
    """Retrieve jail stats from fail2ban-client status <jail>"""
    client = Fail2BanClient(ignored_jails=[])

    # pylint: disable=protected-access
    client._run = mock.MagicMock(return_value=stdout)

    jail_stats = client.jail_stats("sshd")

    assert len(jail_stats) == len(expected)
    assert jail_stats == expected
