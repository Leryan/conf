#!/bin/sh
while [ 1 ]; do
    ping -q -c 1 -W 10 10.9.3.1 > /dev/null
    if [ ! "$?" = "0" ]; then
        echo "restarting openvpn in 10 seconds..."
        systemctl stop openvpn-client@bossk
        sleep 10
        systemctl start openvpn-client@bossk
    else
        echo "vpn ok"
    fi
    sleep 10
done
