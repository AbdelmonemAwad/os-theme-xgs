#!/bin/sh
#-
# SPDX-License-Identifier: BSD-2-Clause
# Copyright (c) 2026 Abdelmonem Awad <eg2@live.com>
#
# Compile both themes' stylesheets into build/css, as OPNsense ships its own: compressed, no source
# maps, and no byte-order mark - the CSS is UTF-8, as the pages are. The dark theme reads Bootstrap
# and the shared XGS Silicon files from the light theme's directory, as OPNsense's dark theme reads
# them from `opnsense`.
#
#   sh tools/build-css.sh          (npm install first: the Sass compiler is a development dependency)
set -e
cd "$(dirname "$0")/.."
T=src/opnsense/www/themes
SASS="npx --no-install sass --no-source-map --no-charset --style=compressed --quiet"

for f in main dashboard opnsense-bootgrid bootstrap-dialog; do
    $SASS "$T/xgs/assets/stylesheets/$f.scss" "$T/xgs/build/css/$f.css"
done
for f in main dashboard opnsense-bootgrid bootstrap-dialog bootstrap-select dns-overview; do
    $SASS --load-path="$T/xgs/assets/stylesheets" "$T/xgs-dark/assets/stylesheets/$f.scss" "$T/xgs-dark/build/css/$f.css"
done
echo "built: $(ls $T/xgs/build/css | wc -l | tr -d ' ') light, $(ls $T/xgs-dark/build/css | wc -l | tr -d ' ') dark"
