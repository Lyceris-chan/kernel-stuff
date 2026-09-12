# sleepy-kernel

Custom Arch Linux kernel for one machine: an AMD Ryzen 7 7700 (Zen 4) desktop
with a Radeon RX 9070 XT (Navi 48 / RDNA 4).

The single package lives in [`sleepy-next/`](sleepy-next/) and builds
`linux-sleepy-next`, currently based on **Linux 7.3-rc2**.

This is not a general-purpose kernel; the configuration is opinionated for the
hardware above.

## Documentation

| Document | Purpose |
|---|---|
| [`sleepy-next/docs/README.md`](sleepy-next/docs/README.md) | Project overview and target hardware |
| [`sleepy-next/docs/GUIDE.md`](sleepy-next/docs/GUIDE.md) | Toolchain, `PROFILE_PEAK`, and `net-tune` |
| [`sleepy-next/PATCH_SOURCES.md`](sleepy-next/PATCH_SOURCES.md) | Per-patch provenance ledger |
| [`CHANGELOG.md`](CHANGELOG.md) | Changes by kernel version and `pkgrel` |
| [`LESSONS.md`](LESSONS.md) | Incident log — read before repeating a past mistake |
| [`CLAUDE.md`](CLAUDE.md) | Maintenance rules and durable findings |

## Build

```bash
cd sleepy-next
rm -rf src pkg
updpkgsums          # after any source=() or patch-file edit
makepkg -f -s -c
```

The build produces `linux-sleepy-next-<version>-x86_64.pkg.tar.zst` and a
matching `-headers` package.

## Repository layout

| Path | Purpose |
|---|---|
| `sleepy-next/` | The kernel package — `PKGBUILD`, `config`, `patches/`, `net-tune/`, `docs/` |
| `CHANGELOG.md` | Release history |
| `LESSONS.md` | Incident log |
| `CLAUDE.md` | Maintenance rules |
| `repos/` | Cloned upstream git repos for patch extraction (gitignored) |

## History

Until 2026-09-12 the repository also carried a 7.2 `linux-sleepy` package at the
root, alongside `sleepy-next/`. It was dropped in favour of the single 7.3
package; its `PKGBUILD`, `patches/`, `config`, `disable_configs.py` and
`net-tune/` remain in git history. The `net-tune` service it used to own is now
shipped by `linux-sleepy-next`.
