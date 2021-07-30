#!/usr/bin/env python3
"""Setup script for fail2ban exporter"""
import codecs

from setuptools import find_packages, setup


def get_long_description():
    """Reads the main README to get the program's long description"""
    with codecs.open("README.md", "r", "utf-8") as f_readme:
        return f_readme.read()


setup(
    name="fail2ban_exporter",
    version="1.0.0",
    description="A Prometheus exporter for fail2ban jail metrics",
    long_description=get_long_description(),
    author="Kylapaallikko",
    maintainer="Somfy Protect by Myfox SAS",
    maintainer_email="cloud@getmyfox.com",
    license="MIT",
    url="https://github.com/xofym/fail2ban_exporter",
    keywords="fail2ban",
    packages=find_packages(exclude=["tests.*", "tests"]),
    entry_points={"console_scripts": ["fail2ban_exporter = fail2ban_exporter.cli:main"]},
    install_requires=[
        "prometheus_client>=0.2.0,<0.3",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: System :: Networking :: Firewalls",
        "Topic :: System :: Networking :: Monitoring",
    ],
)
