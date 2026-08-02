#!/bin/bash
# SQM QoS Network Optimizer (CAKE)
# Note: BBR3 is the kernel-compiled default (CONFIG_DEFAULT_TCP_CONG="bbr3"),
# so no sysctl override is needed here.

CONF="/etc/sqm-qos.conf"
if [ ! -f "$CONF" ]; then
    echo "Configuration file $CONF not found. Skipping SQM QoS shaping."
    exit 0
fi

source "$CONF"

# Dynamically find the default internet interface with retry loop for bootup race conditions
for i in {1..30}; do
    IFACE=$(ip route get 9.9.9.9 2>/dev/null | awk '{print $5}' | head -n 1)
    if [ -n "$IFACE" ]; then
        break
    fi
    sleep 1
done

if [ -z "$IFACE" ]; then
    echo "No default internet interface found after waiting."
    exit 1
fi

if [ -z "$UPLOAD_MBIT" ] || [ -z "$DOWNLOAD_MBIT" ]; then
    echo "UPLOAD_MBIT or DOWNLOAD_MBIT not set in $CONF. Skipping CAKE shaping."
    exit 0
fi

echo "Applying CAKE SQM to $IFACE (Upload: ${UPLOAD_MBIT}Mbit, Download: ${DOWNLOAD_MBIT}Mbit)..."

# Clear existing qdiscs
tc qdisc del dev "$IFACE" root 2>/dev/null
tc qdisc del dev "$IFACE" ingress 2>/dev/null
tc qdisc del dev ifb4cake root 2>/dev/null

# Setup Egress (Upload)
tc qdisc add dev "$IFACE" root cake bandwidth ${UPLOAD_MBIT}mbit besteffort nat

# Setup Ingress (Download)
modprobe ifb numifbs=1 2>/dev/null || true
ip link set dev ifb4cake up 2>/dev/null || true
tc qdisc add dev ifb4cake root cake bandwidth ${DOWNLOAD_MBIT}mbit besteffort wash
tc qdisc add dev "$IFACE" handle ffff: ingress
tc filter add dev "$IFACE" parent ffff: matchall action mirred egress redirect dev ifb4cake

echo "SQM QoS successfully applied to $IFACE."
