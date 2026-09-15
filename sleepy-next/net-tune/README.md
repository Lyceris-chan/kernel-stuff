# net-tune

One systemd service that applies low-latency Ethernet settings and CAKE SQM
shaping. Each half is independently toggleable in `/etc/net-tune.conf`.

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
