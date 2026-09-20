# net-tune

Two systemd units. `net-tune.service` applies low-latency Ethernet settings and
CAKE SQM shaping once the link is up; each half is independently toggleable in
`/etc/net-tune.conf`.

`net-tune-eee.service` is a small oneshot ordered `Before=NetworkManager.service`
that runs `net-tune.sh eee-off`, i.e. turns EEE off while the link is still
down. It exists because **switching EEE restarts auto-negotiation and drops the
link for ~3s**: done from the NetworkManager dispatcher (after activation) that
outage landed exactly when blocky resolves its DoQ upstream, leaving DNS broken
for ~11s after login on every boot (measured 2026-09-20; the flap is visible on
09-19 boots too). While the link is down the same call is free. The re-apply in
the main service therefore only touches EEE when `ethtool --show-eee` reports it
*enabled*, so `up`/`dhcp4-change` events can never flap the link again.

`linux-sleepy-next` owns this service: a build installs it, enables it through
`network-online.target.wants`, and marks `/etc/net-tune.conf` as a pacman backup
file so local edits survive kernel upgrades.

It is enabled through the **network** target, not `multi-user.target`, and that
is deliberate. A unit `multi-user.target` pulls in is waited for, so enabling an
`After=network-online.target` service there makes the whole session wait for
DHCP — 12.3s on this machine, its entire avoidable boot time. Pulled in by
`network-online.target` instead, the shaping is applied as soon as the link is
up and the desktop no longer waits for it.

## Configuration

`/etc/net-tune.conf`:

| Setting | Default | Effect |
|---|---|---|
| `ENABLE_SQM` | `yes` | Apply CAKE shaping |
| `DOWNLOAD_MBIT` | `80` | Shaping rate for ingress |
| `UPLOAD_MBIT` | `80` | Shaping rate for egress |
| `ENABLE_LATENCY` | `yes` | Low-latency Ethernet tuning (independent of SQM) |

The shipped template enables SQM at 80/80 Mbit, so an unattended build installs
shaping rather than silently disabling it. **Set your real line rate** — until
you do, CAKE caps the link at 80/80. The build's interactive prompt asks for the
speeds; with no TTY it falls back to the shipped template.

The route probe uses Quad9 (`9.9.9.9`), never `8.8.8.8`.

## Requirements

Ingress shaping needs the `ingress` qdisc, which needs
`CONFIG_NET_SCH_INGRESS=y`, plus a **named** `ifb4cake` device created
explicitly with `ip link add ifb4cake type ifb` (the `ifb` module's own
`numifbs=` parameter would name it `ifb0`). The u32 match-all idiom performs the
ingress redirect. BBR3 is the kernel-compiled TCP default; this service only
adds CAKE.

## Verify

The service checks both CAKE halves after applying and logs
`net-tune: OK - CAKE shaping active (...)` or an `ERROR` to journald, so a
missing ingress is no longer silent. To check by hand:

```bash
tc qdisc show dev <iface>              # expect root `cake` AND `qdisc ingress ffff:`
ip link show ifb4cake                  # expect `state UP`, `qdisc cake`
tc filter show dev <iface> ingress     # expect a `mirred` redirect
```

A service status of `active (exited)` is **not** proof of shaping — check the
qdiscs.

## 99-net-tune.conf

`net-tune.sh` applies `net.core.netdev_max_backlog=1000` and the `busy_poll`/
`busy_read` pair at `network-online`. Those live only in the running kernel, so
any later `sysctl --system` re-applies
`/usr/lib/sysctl.d/70-cachyos-settings.conf` (`netdev_max_backlog = 4096`) and
silently reverts them — observed live: net-tune logged
`net.core.netdev_max_backlog = 1000` at 06:43:48, and a `sysctl --system` run
afterwards put the box back on 4096 with no warning.

`99-net-tune.conf` declares the same values under `/etc/sysctl.d/`, so
`sysctl --system` now lands on the same numbers the script wants. The script
still re-asserts them per interface at boot; this drop-in only removes the
footgun.

Install it alongside the service:

```bash
sudo install -Dm644 99-net-tune.conf /etc/sysctl.d/99-net-tune.conf
```
