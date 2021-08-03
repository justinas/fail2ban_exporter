#!/bin/bash
VIRTUALENV_PATH=/opt/fail2ban_exporter

# Install the exporter in a Python3 virtualenv
python3 -m venv ${VIRTUALENV_PATH}
source ${VIRTUALENV_PATH}/bin/activate
python3 setup.py install

# Symlink the exporter console entrypoint
ln -sf ${VIRTUALENV_PATH}/bin/fail2ban_exporter /usr/local/bin/fail2ban_exporter

# Setup, enable and start the systemd unit
cp fail2ban_exporter.service /etc/systemd/system/fail2ban_exporter.service

systemctl daemon-reload
systemctl enable fail2ban_exporter
systemctl start fail2ban_exporter
