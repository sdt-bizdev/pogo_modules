#!/bin/bash

# Check if the script is run with sudo privileges
if [ "$EUID" -ne 0 ]; then
    echo "Please run this script with sudo."
    exit 1
fi

# 1. Compile monitoring_code.c to create the binary pogo_server_monitor
g++ monitoring_code.cpp -o pogo_server_monitor

# 2. Move the executable to /usr/local/bin/
mv pogo_server_monitor /usr/local/bin/

# 3. Fetch the current user name and group name
username=$(whoami)
groupname=$(id -gn)

# 4. Create the systemd service unit file
cat <<EOF | tee /etc/systemd/system/pogo_server_monitor.service >/dev/null
[Unit]
Description=Server Health Monitoring Service
After=network.target
Wants=network-online.target
After=network-online.target

[Service]
Type=simple
ExecStart=/usr/local/bin/pogo_server_monitor >/dev/null 2>&1
Restart=always
RestartSec=3
User=$username
Group=$groupname

[Install]
WantedBy=multi-user.target
EOF

# 5. Reload systemd to pick up the changes
systemctl daemon-reload

# 6. Enable the service to start on boot
systemctl enable pogo_server_monitor.service

# 7. Restart the service
systemctl restart pogo_server_monitor.service