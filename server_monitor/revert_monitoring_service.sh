#!/bin/bash

# Check if the script is run with sudo privileges
if [ "$EUID" -ne 0 ]; then
    echo "Please run this script with sudo."
    exit 1
fi

# Stop and disable the service
systemctl stop pogo_server_monitor.service
systemctl disable pogo_server_monitor.service

# Remove the systemd service unit file
rm -f /etc/systemd/system/pogo_server_monitor.service

# Remove the binary from /usr/local/bin/
rm -f /usr/local/bin/pogo_server_monitor

# Reload systemd to pick up the changes
systemctl daemon-reload

echo "Reverted changes successfully."