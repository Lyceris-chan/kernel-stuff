#!/bin/bash
# net-tune: combined CAKE SQM + low-latency ethernet tuning, applied at boot.
#
# Each part is independent — toggle ENABLE_SQM and ENABLE_LATENCY in
# /etc/net-tune.conf. Latency settings come from the ethtool(8) man page, the
# Intel Ethernet Performance Tuning Guide, the Realtek r8169 driver history
# (interrupt coalescing / EEE), and the kernel docs for busy-polling.

CONF="/etc/net-tune.conf"
[ -f "$CONF" ] && . "$CONF"

: "${ENABLE_SQM:=no}"
: "${ENABLE_LATENCY:=yes}"
: "${IFACE:=}"
# CAKE tuning (per tc-cake(8) and the CAKE bufferbloat guides):
#   DIFFSERV=besteffort  no DSCP priority tins (single tin, lowest CPU)
#   DIFFSERV=diffserv4   four tins (Bulk/BestEffort/Video/Voice) — use when
#                        you mark DSCP (e.g. nftables sets EF/AF4x on game traffic)
#   RTT=regional        30 ms AQM target; metro=10ms, internet=100ms default
#   OVERHEAD=ethernet   matches a direct Ethernet handoff to the modem/router;
#                       use docsis for cable modems, pppoe-ptm for VDSL2
: "${DIFFSERV:=diffserv4}"
: "${RTT:=regional}"
: "${OVERHEAD:=ethernet}"

if [ -z "$IFACE" ]; then
    # Find the default internet interface. The unit runs after
    # network-online.target, so the route is usually present immediately; the
    # short retry is a boot-race safety net. If no route exists yet, fall back
    # to the first carrier-up ethernet NIC so latency tuning still applies.
    for _ in $(seq 1 10); do
        IFACE=$(ip route get 9.9.9.9 2>/dev/null | awk '{print $5}' | head -n 1)
        [ -n "$IFACE" ] && break
        sleep 1
    done
fi
if [ -z "$IFACE" ]; then
    IFACE=$(ip -o link show 2>/dev/null | awk -F': ' '/state UP/ && $2 != "lo" {print $2; exit}')
fi
[ -z "$IFACE" ] && { echo "net-tune: no internet interface found"; exit 1; }

if [ "$ENABLE_LATENCY" = "yes" ]; then
    echo "net-tune: applying latency tuning to $IFACE"
    # Interrupt coalescing: disable adaptive, minimal fixed delay/frames.
    ethtool -C "$IFACE" adaptive-rx off adaptive-tx off \
        rx-usecs 0 tx-usecs 0 rx-frames 1 tx-frames 1 2>/dev/null || true
    # Energy-Efficient Ethernet off (Realtek jitter source).
    ethtool --set-eee "$IFACE" eee off 2>/dev/null || true
    # Offloads off: GRO/GSO/TSO/LRO batch packets, adding latency.
    ethtool -K "$IFACE" gro off gso off tso off lro off 2>/dev/null || true
    # Small ring buffers: less queuing delay.
    ethtool -G "$IFACE" rx 256 tx 256 2>/dev/null || true
    # Wake-on-LAN off.
    ethtool -s "$IFACE" wol d 2>/dev/null || true
    # Busy polling: poll instead of waiting on interrupts.
    sysctl -w net.core.busy_poll=50 net.core.busy_read=50 2>/dev/null || true
    # Cap the receive backlog: less queuing delay under bursts.
    sysctl -w net.core.netdev_max_backlog=1000 2>/dev/null || true
fi

if [ "$ENABLE_SQM" = "yes" ] && [ -n "$UPLOAD_MBIT" ] && [ -n "$DOWNLOAD_MBIT" ]; then
    echo "net-tune: applying CAKE SQM to $IFACE (${UPLOAD_MBIT}/${DOWNLOAD_MBIT} Mbit)"
    # Ingress (download): mirror LAN-facing traffic to ifb4cake, then shape it.
    modprobe ifb numifbs=1 2>/dev/null || true
    ip link set dev ifb4cake up 2>/dev/null || true
    tc qdisc replace dev ifb4cake root cake bandwidth "${DOWNLOAD_MBIT}mbit" \
        "${DIFFSERV}" dual-dsthost wash nat "${RTT}" "${OVERHEAD}" 2>/dev/null || true
    tc qdisc replace dev "$IFACE" handle ffff: ingress 2>/dev/null || true
    tc filter replace dev "$IFACE" parent ffff: matchall \
        action mirred egress redirect dev ifb4cake 2>/dev/null || true

    # Egress (upload): dual-srchost fairness, ack-filter for asymmetric links.
    tc qdisc replace dev "$IFACE" root cake bandwidth "${UPLOAD_MBIT}mbit" \
        "${DIFFSERV}" dual-srchost nat ack-filter "${RTT}" "${OVERHEAD}" 2>/dev/null || true
fi

exit 0
