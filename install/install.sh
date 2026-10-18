#!/bin/sh
#-
# SPDX-License-Identifier: BSD-2-Clause
# Copyright (c) 2026 Abdelmonem Awad <eg2@live.com>
#
# Install XGS Silicon: the three themes, into OPNsense's own theme directory.
#
#   xgs        light
#   xgs-dark   dark
#   xgs-auto   whichever of the two the browser's own setting asks for, switching when it changes
#
# Choosing one stays the owner's - System: Settings: General: Theme - or install/enable.sh from a
# shell; an image from xgs-image-builder chooses xgs-auto at its first boot. Only build/ goes onto the
# appliance: assets/ is the source the stylesheets are compiled from (tools/build-css.sh).
set -eu
SRC=$(cd "$(dirname "$0")/.." && pwd)/src/opnsense/www/themes
DST=/usr/local/opnsense/www/themes
[ -d "$DST" ] || { echo "no $DST: this is not OPNsense" >&2; exit 1; }

for t in xgs xgs-dark xgs-auto; do
    rm -rf "${DST:?}/$t"
    mkdir -p "$DST/$t"
    cp -R "$SRC/$t/build" "$DST/$t/"
    cp "$SRC/$t/LICENSE" "$DST/$t/"
done
# xgs-auto shares the light theme's stylesheets, fonts and images, as OPNsense's opnsense-auto
# shares opnsense's; its own is the switcher in build/js.
for d in css fonts images; do
    ln -sfn "../../xgs/build/$d" "$DST/xgs-auto/build/$d"
done
chown -R root:wheel "$DST/xgs" "$DST/xgs-dark" "$DST/xgs-auto"

# The right-to-left layout (opnsense-rtl) writes a mirrored copy of every theme's stylesheets; it
# does so at every boot, and now, so that Arabic has these at once.
if [ -f /root/opnsense-rtl/apply_rtl.py ]; then
    /usr/local/bin/python3 /root/opnsense-rtl/apply_rtl.py > /dev/null 2>&1 || true
fi
echo "installed xgs, xgs-dark and xgs-auto - choose one in System: Settings: General, or run install/enable.sh"
