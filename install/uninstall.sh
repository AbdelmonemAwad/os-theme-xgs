#!/bin/sh
#-
# SPDX-License-Identifier: BSD-2-Clause
# Copyright (c) 2026 Abdelmonem Awad <eg2@live.com>
#
# Remove XGS Silicon. A GUI left on a theme that is gone would draw OPNsense's stylesheets with a
# missing logo, so when one of the three is the GUI's theme, OPNsense's own takes its place first.
set -u
/usr/local/bin/php -r '
require_once "/usr/local/opnsense/mvc/script/load_phalcon.php";
$config = \OPNsense\Core\Config::getInstance();
$root = $config->object();
if (isset($root->theme) && in_array((string)$root->theme, ["xgs", "xgs-dark", "xgs-auto"], true)) {
    $root->theme = "opnsense";
    $config->save();
    echo "GUI theme: opnsense\n";
}
'
DST=/usr/local/opnsense/www/themes
rm -rf "${DST:?}/xgs" "${DST:?}/xgs-dark" "${DST:?}/xgs-auto"
echo "removed xgs, xgs-dark and xgs-auto"
