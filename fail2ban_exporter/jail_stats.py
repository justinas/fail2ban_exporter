"""fail2ban jail statistics"""
from dataclasses import dataclass


@dataclass
class JailStats:
    """JailStats holds statistics for a given fail2ban jail"""

    jail: str
    failed: int
    failed_total: int
    banned: int
    banned_total: int
