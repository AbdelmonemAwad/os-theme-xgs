#!/usr/bin/env python3
#-
# SPDX-License-Identifier: BSD-2-Clause
# Copyright (c) 2026 Abdelmonem Awad <eg2@live.com>
#
"""
Draw the README's palettes from the tokens themselves, so the colours shown are the colours built.

    python3 tools/readme-art.py           write docs/images/palette-light.svg and palette-dark.svg
    python3 tools/readme-art.py --check   fail when either is not what the tokens say
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
STYLES = os.path.join(ROOT, 'src', 'opnsense', 'www', 'themes')
OUT = os.path.join(ROOT, 'docs', 'images')

# The swatches, in the order the README explains them.
SWATCHES = [
    ('ground', 'xgs-ground'), ('surface', 'xgs-surface'), ('line', 'xgs-line'), ('text', 'xgs-text'),
    ('muted', 'xgs-muted'), ('carbon', 'xgs-carbon'), ('copper', 'xgs-copper-text'),
    ('signal', 'xgs-signal'), ('up', 'xgs-up'), ('caution', 'xgs-caution'), ('down', 'xgs-down'),
]


def tokens(theme):
    with open(os.path.join(STYLES, theme, 'assets', 'stylesheets', '_xgs-tokens.scss'), encoding='utf-8') as handle:
        text = handle.read()
    return dict(re.findall(r'^\$([\w-]+):\s*(#[0-9A-Fa-f]{6})\s*;', text, re.M))


def svg(theme, title, ground, ink, muted, line):
    t = tokens(theme)
    w, cell, gap, top = 1200, 96, 12, 64
    cols = 6
    rows = (len(SWATCHES) + cols - 1) // cols
    h = top + rows * (cell + 56) + 24
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" '
           'role="img" aria-label="%s">' % (w, h, w, h, title),
           '<rect width="%d" height="%d" rx="14" fill="%s"/>' % (w, h, ground),
           '<text x="32" y="42" font-family="IBM Plex Sans, Segoe UI, Arial, sans-serif" font-size="18" '
           'font-weight="600" fill="%s">%s</text>' % (ink, title)]
    cw = (w - 64 - gap * (cols - 1)) / cols
    for i, (name, key) in enumerate(SWATCHES):
        x = 32 + (i % cols) * (cw + gap)
        y = top + (i // cols) * (cell + 56)
        hexv = t[key].upper()
        out.append('<rect x="%.1f" y="%d" width="%.1f" height="%d" rx="10" fill="%s" stroke="%s"/>'
                   % (x, y, cw, cell - 30, hexv, line))
        out.append('<text x="%.1f" y="%d" font-family="IBM Plex Sans, Segoe UI, Arial, sans-serif" '
                   'font-size="15" font-weight="600" fill="%s">%s</text>' % (x, y + cell - 8, ink, name))
        out.append('<text x="%.1f" y="%d" font-family="IBM Plex Mono, Consolas, monospace" font-size="13" '
                   'fill="%s">%s</text>' % (x, y + cell + 12, muted, hexv))
    out.append('</svg>')
    return '\n'.join(out) + '\n'


def drawings():
    light, dark = tokens('xgs'), tokens('xgs-dark')
    return {
        'palette-light.svg': svg('xgs', 'Light - xgs', light['xgs-ground'], light['xgs-text'],
                                 light['xgs-muted'], light['xgs-line']),
        'palette-dark.svg': svg('xgs-dark', 'Dark - xgs-dark', dark['xgs-ground'], dark['xgs-text'],
                                dark['xgs-muted'], dark['xgs-line']),
    }


def main(argv):
    stale = []
    for name, text in drawings().items():
        path = os.path.join(OUT, name)
        if '--check' in argv:
            try:
                with open(path, encoding='utf-8') as handle:
                    if handle.read() != text:
                        stale.append(name)
            except OSError:
                stale.append(name)
        else:
            os.makedirs(OUT, exist_ok=True)
            with open(path, 'w', encoding='utf-8', newline='\n') as handle:
                handle.write(text)
            print('wrote docs/images/' + name)
    if stale:
        sys.exit('not what the tokens say: %s - run python3 tools/readme-art.py' % ', '.join(stale))
    if '--check' in argv:
        print('the palettes are what the tokens say')


if __name__ == '__main__':
    main(sys.argv)
