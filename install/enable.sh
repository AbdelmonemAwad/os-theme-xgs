#!/bin/sh
#-
# SPDX-License-Identifier: BSD-2-Clause
# Copyright (c) 2026 Abdelmonem Awad <eg2@live.com>
#
# Make one of the three the GUI's theme, as System: Settings: General: Theme does - xgs-auto unless
# another is named. xgs-image-builder runs this at an image's first boot.
#
#   sh install/enable.sh [xgs | xgs-dark | xgs-auto]
set -u
THEME=${1:-xgs-auto}
case "$THEME" in
    xgs|xgs-dark|xgs-auto) ;;
    *) echo "usage: enable.sh [xgs | xgs-dark | xgs-auto]" >&2; exit 1 ;;
esac
[ -d "/usr/local/opnsense/www/themes/$THEME" ] || { echo "$THEME is not installed: run install/install.sh first" >&2; exit 1; }

/usr/local/bin/php -r '
require_once "/usr/local/opnsense/mvc/script/load_phalcon.php";
$config = \OPNsense\Core\Config::getInstance();
$config->object()->system->theme = $argv[1];
$config->save();
echo "GUI theme: " . $argv[1] . "\n";
' "$THEME"
