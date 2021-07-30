"""fail2ban-client wrapper"""
import os
import re
from typing import List
from subprocess import PIPE, run

FAIL2BAN_CLIENT = os.path.join(os.getenv("EXEC_PATH", "/usr/bin/"), "fail2ban-client")
COMP = re.compile(r"\s([a-zA-Z\s]+):\t([a-zA-Z0-9-,\s]+)\n")


class Fail2BanClient:
    """Wrapper for fail2ban-client commands"""

    def __init__(self, ignored_jails: List[str]):
        self.ignored_jails = ignored_jails

    @staticmethod
    def _run(args: List[str]):
        """Run a fail2ban-client command"""
        cmd = [FAIL2BAN_CLIENT]
        if args:
            cmd.extend(args)

        result = run(cmd, stdout=PIPE, check=True)

        return result.stdout.decode("utf-8")

    def status(self, jail: str = None) -> str:
        """Wrapper for fail2ban-client status"""
        args = ["status"]
        if jail:
            args.append(jail)

        return self._run(args)

    def jails(self) -> List[str]:
        """Retrieve a list of fail2ban jails"""
        status = self.status()

        matches = re.search(r"Jail list:\s*([a-z\-, ]*)\n", status)
        if not matches:
            return []

        return [
            jail
            for jail in matches.group(1).split(", ")
            if jail not in self.ignored_jails
        ]

    def jail_stats(self, jail: str):
        """Retrieve the stats for a given fail2ban jail"""
        jail_status = self.status(jail)
        return re.findall(COMP, jail_status)
