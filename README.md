# sleepy-kernel

Custom Arch Linux kernel for one machine: an AMD Ryzen 7 7700 (Zen 4) desktop
with a Radeon RX 9070 XT (Navi 48 / RDNA 4).

Two packages share one patch series:

| Directory | Package | Base |
|---|---|---|
| [`sleepy-rc/`](sleepy-rc/) | `linux-sleepy-rc` | mainline **`v7.3`** |
| [`sleepy-next/`](sleepy-next/) | `linux-sleepy-next` | linux-next snapshot **`next-20261019`** |

They are deliberately installable **side by side**: each sets its own
`_pkgsuffix`, which drives both `pkgbase` and the kernel release, so the module
directories (`/usr/lib/modules/*-sleepy-rc/` and `…-sleepy-next/`), the boot
artefacts and the pacman package names never collide. `sleepy-rc` tracks the
mainline release candidates; `sleepy-next` is the preview that carries the
incoming merge-window content early.

This is not a general-purpose kernel; the configuration is opinionated for the
hardware above.

## Documentation

| Document | Purpose |
|---|---|
| [`sleepy-rc/docs/README.md`](sleepy-rc/docs/README.md) | Project overview and target hardware |
| [`sleepy-rc/docs/GUIDE.md`](sleepy-rc/docs/GUIDE.md) | Toolchain, `PROFILE_PEAK`, and `net-tune` |
| [`sleepy-rc/PATCH_SOURCES.md`](sleepy-rc/PATCH_SOURCES.md) | **Authoritative** per-patch provenance ledger for the series |
| [`sleepy-next/PATCH_SOURCES.md`](sleepy-next/PATCH_SOURCES.md) | Preview-only deltas: skips, exclusions, rebases |
| [`CHANGELOG.md`](CHANGELOG.md) | Changes by kernel version and `pkgrel` |
| [`LESSONS.md`](LESSONS.md) | Incident log — read before repeating a past mistake |
| [`CLAUDE.md`](CLAUDE.md) | Maintenance rules and durable findings |

## Build

Pick the package directory; the steps are identical.

```bash
cd sleepy-rc          # or: cd sleepy-next
rm -rf src pkg
updpkgsums            # after any source=() or patch-file edit
makepkg -f -s -c
```

The build produces `linux-sleepy-rc-<version>-x86_64.pkg.tar.zst` or
`linux-sleepy-next-<version>-x86_64.pkg.tar.zst`, each with a matching
`-headers` package.

`sleepy-next` applies its series to an unstable base, so `prepare()` **skips**
patches that no longer apply instead of failing the build. A skipped patch is an
inert no-op — see its `PATCH_SOURCES.md` for why that is safe here and which
interdependent groups had to be excluded wholesale.

## Repository layout

| Path | Purpose |
|---|---|
| `sleepy-rc/` | Mainline package — `PKGBUILD`, `config`, `patches/`, `net-tune/`, `docs/` |
| `sleepy-next/` | Preview package — same layout, snapshot base |
| `CHANGELOG.md` | Release history |
| `LESSONS.md` | Incident log |
| `CLAUDE.md` | Maintenance rules |
| `repos/` | Cloned upstream git repos for patch extraction (gitignored) |

## History

Until 2026-09-12 the repository also carried a 7.2 `linux-sleepy` package at the
root, alongside `sleepy-next/`. It was dropped in favour of the single 7.3
package; its `PKGBUILD`, `patches/`, `config`, `disable_configs.py` and
`net-tune/` remain in git history. The `net-tune` service it used to own is now
shipped by both 7.3 packages.

On 2026-10-11 the single `sleepy-next/` package was split: that directory became
`sleepy-rc/` (same series, same patch numbers, renamed package) and `sleepy-next/`
was recreated as the linux-next snapshot preview. The rename was done with
`git mv`, so history is preserved.
