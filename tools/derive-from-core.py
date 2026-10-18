#!/usr/bin/env python3
#-
# SPDX-License-Identifier: BSD-2-Clause
# Copyright (c) 2026 Abdelmonem Awad <eg2@live.com>
#
"""
Derive the two themes' stylesheets from OPNsense's own, so that XGS Silicon follows OPNsense when
its themes change.

    python3 tools/derive-from-core.py <core>/src/opnsense/www/themes [<commit>]

The light theme `xgs` starts from OPNsense's `opnsense`, and the dark theme `xgs-dark` from
`opnsense-dark`: every stylesheet is copied as OPNsense has it, then changed in three places only.

  1. main.scss loads XGS Silicon's tokens and fonts where OPNsense declares its own fonts,
     and `_xgs.scss` last, so that what this theme changes is in one file and wins.
  2. dashboard.scss loads the tokens, and `_xgs-dashboard.scss` last.
  3. Paths that name OPNsense's theme directory name this theme's.

What is never touched: `config/colors.scss`, the tokens, `_xgs*.scss` - this theme's own files -
and `bootstrap/`, which is Bootstrap 3 as OPNsense ships it (the dark theme reads the light one's,
as OPNsense's dark theme reads `opnsense`'s). OPNsense's licence (BSD-2-Clause, Deciso B.V.) stays
beside the files that came from it.
"""

import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
THEMES = os.path.join(HERE, '..', 'src', 'opnsense', 'www', 'themes')
OURS = ('config/colors.scss', '_xgs-tokens.scss', '_xgs-fonts.scss', '_xgs.scss', '_xgs-dashboard.scss')
PAIRS = (('opnsense', 'xgs'), ('opnsense-dark', 'xgs-dark'))


def edit_main(text):
    # OPNsense's three @font-face blocks for Source Sans Pro sit between the colours and Bootstrap.
    start = text.index('@font-face')
    end = text.index('// Core variables and mixins')
    text = text[:start] + '// XGS Silicon: the tokens (Bootstrap\'s variables among them) and the fonts.\n' \
        '@import "xgs-tokens";\n@import "xgs-fonts";\n\n' + text[end:]
    return text.rstrip('\n') + '\n\n// XGS Silicon: everything this theme changes, last, so that it wins.\n@import "xgs";\n'


def edit_dashboard(text):
    text = text.replace('@import "config/colors";', '@import "config/colors";\n@import "xgs-tokens";', 1)
    return text.rstrip('\n') + '\n\n// XGS Silicon: the widgets.\n@import "xgs-dashboard";\n'


def derive(core, commit):
    for theirs, ours in PAIRS:
        src = os.path.join(core, theirs, 'assets', 'stylesheets')
        dst = os.path.join(THEMES, ours, 'assets', 'stylesheets')
        for root, _dirs, files in os.walk(src):
            for name in files:
                rel = os.path.relpath(os.path.join(root, name), src).replace(os.sep, '/')
                if rel in OURS:
                    continue
                with open(os.path.join(root, name), encoding='utf-8') as handle:
                    text = handle.read()
                if rel == 'main.scss':
                    text = edit_main(text)
                elif rel == 'dashboard.scss':
                    text = edit_dashboard(text)
                text = text.replace('/ui/themes/%s/' % theirs, '/ui/themes/%s/' % ours)
                if theirs == 'opnsense-dark':
                    text = text.replace('/ui/themes/opnsense/', '/ui/themes/xgs/')
                out = os.path.join(dst, rel)
                os.makedirs(os.path.dirname(out), exist_ok=True)
                with open(out, 'w', encoding='utf-8', newline='\n') as handle:
                    handle.write(text)
        shutil.copy(os.path.join(core, 'opnsense', 'LICENSE'), os.path.join(THEMES, ours, 'LICENSE'))
    if commit:
        with open(os.path.join(THEMES, 'xgs', 'BASE'), 'w', encoding='utf-8', newline='\n') as handle:
            handle.write('OPNsense core %s\n' % commit)
    print('derived from %s%s' % (core, ' at ' + commit if commit else ''))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('usage: derive-from-core.py <core>/src/opnsense/www/themes [<commit>]')
    derive(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else '')
