#!/bin/bash
# Create the swapfile that zswap fronts, and make it persistent.
#
# Run as root. Idempotent: re-running against an existing, active swapfile is
# a no-op, and re-running against a stale one repairs it.
#
# This box has no free partition (the NVMe is a single root filesystem), so the
# backing store is a file. That is fine for SWAP -- and it is the reason zswap
# was chosen over zram: zswap's drain writes back to the entry's own swap
# device, so any real device will do. zram's backing_dev would NOT have
# accepted a file (backing_dev_store() rejects anything that is not S_ISBLK),
# which is why zram's writeback was a dead end here.
#
# Size: 16 GiB. The pool in front of it is capped at max_pool_percent (20% of
# RAM = 6.4 GB compressed, ~19 GB uncompressed at 3:1), so in normal operation
# this file receives only entries the shrinker has already decided are cold.
# It is overflow, not the primary tier.
set -euo pipefail

SWAPFILE=/swapfile
SIZE=16G
PRI=100

[ "$(id -u)" -eq 0 ] || { echo "must run as root" >&2; exit 1; }

if [ ! -f "$SWAPFILE" ]; then
    echo "creating $SWAPFILE ($SIZE)"
    # fallocate is fine on ext4; mkswap+swapon below will reject it if the
    # extents came out unwritten. Fall back to a real write if that happens.
    fallocate -l "$SIZE" "$SWAPFILE" || dd if=/dev/zero of="$SWAPFILE" bs=1M count=16384 status=progress
    chmod 600 "$SWAPFILE"
    mkswap "$SWAPFILE"
else
    echo "$SWAPFILE already exists, leaving it alone"
fi

# /etc/fstab may not end in a newline -- appending blindly concatenates onto
# the last entry and breaks parsing. Force one first. (This was hit for real.)
if ! grep -q "^${SWAPFILE}[[:space:]]" /etc/fstab; then
    echo "adding $SWAPFILE to /etc/fstab"
    [ -n "$(tail -c1 /etc/fstab)" ] && echo >> /etc/fstab
    printf '%s none swap defaults,pri=%s 0 0\n' "$SWAPFILE" "$PRI" >> /etc/fstab
fi

systemctl daemon-reload

if ! swapon --show=NAME --noheadings | grep -qx "$SWAPFILE"; then
    echo "activating $SWAPFILE at priority $PRI"
    swapon "$SWAPFILE" -p "$PRI"
else
    echo "$SWAPFILE already active"
fi

echo
echo "=== verify ==="
swapon --show
findmnt --verify --tab-file /etc/fstab 2>&1 | tail -2
