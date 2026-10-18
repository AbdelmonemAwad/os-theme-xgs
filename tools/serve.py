#!/usr/bin/env python3
#-
# SPDX-License-Identifier: BSD-2-Clause
# Copyright (c) 2026 Abdelmonem Awad <eg2@live.com>
#
"""
Serve the themes at /ui/themes/ on localhost, as an appliance serves them, so that a page of a
running OPNsense can be looked at with these stylesheets before anything is installed: the page's
own <link> elements are pointed here from the browser's console, and nothing on the appliance
changes. The stylesheets name their fonts as /ui/themes/xgs/build/fonts/..., which resolves here.

    python3 tools/serve.py [port] [pages] [appliance]    (8765 unless given)

With a directory of saved pages - a page of the GUI saved from the browser with its scripts taken
out, and what it loads from /ui/ beside it under the same paths - /pages/<name>.html shows that page
with one of the themes: ?theme=xgs, xgs-dark or xgs-auto, and ?dir=rtl for right to left with the
mirrored stylesheets opnsense-rtl writes (*.rtl.css, when they have been made). Saved pages carry an
appliance's names and addresses, so they stay on the machine that saved them, never in a repository.
"""

import functools
import http.server
import os
import re
import sys
import urllib.parse
import urllib.request

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src', 'opnsense', 'www')
PAGES = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else ''
# With an appliance's address as well, what a saved page loads from /ui/ and has no copy of yet is
# fetched from that appliance once and kept beside the pages: OPNsense's icon font and its other
# stylesheets, which are static files.
UPSTREAM = sys.argv[3].rstrip('/') if len(sys.argv) > 3 else ''


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        url = urllib.parse.urlsplit(self.path)
        if PAGES and url.path.startswith('/pages/'):
            return self.page(url)
        if PAGES and url.path.startswith('/ui/') and (not url.path.startswith('/ui/themes/xgs')
                                                      or url.path.endswith('.rtl.css')):
            # What a saved page loads from the appliance besides the theme, and the mirrored
            # stylesheets opnsense-rtl made of the theme's: their copies beside the pages.
            local = os.path.join(PAGES, url.path.lstrip('/'))
            if not os.path.isfile(local) and UPSTREAM and '..' not in url.path:
                try:
                    with urllib.request.urlopen(UPSTREAM + url.path, timeout=15) as answer:
                        body = answer.read()
                    os.makedirs(os.path.dirname(local), exist_ok=True)
                    with open(local, 'wb') as handle:
                        handle.write(body)
                except (OSError, ValueError):
                    pass
            if os.path.isfile(local):
                return self.send_file(local)
        return super().do_GET()

    def page(self, url):
        query = urllib.parse.parse_qs(url.query)
        theme = query.get('theme', ['xgs'])[0]
        if theme not in ('xgs', 'xgs-dark', 'xgs-auto'):
            theme = 'xgs'
        name = os.path.basename(url.path)
        try:
            with open(os.path.join(PAGES, name), encoding='utf-8') as handle:
                text = handle.read()
        except OSError:
            return self.send_error(404)
        text = re.sub(r'/ui/themes/[^/"]+/', '/ui/themes/%s/' % theme, text)
        if query.get('dir', [''])[0] == 'rtl':
            text = re.sub(r'<html[^>]*>', '<html lang="ar" dir="rtl">', text, count=1)
            text = re.sub(r'(/ui/themes/[^"?]+?)\.css', r'\1.rtl.css', text)
        if theme == 'xgs-auto':
            text = text.replace('</head>', '<script src="/ui/themes/xgs-auto/build/js/theme.js"></script></head>', 1)
        body = text.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_file(self, local):
        with open(local, 'rb') as handle:
            body = handle.read()
        self.send_response(200)
        self.send_header('Content-Type', self.guess_type(local))
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def translate_path(self, path):
        # /ui/themes/<theme>/... is src/opnsense/www/themes/<theme>/...; xgs-auto's shared parts
        # are the light theme's, as the installer links them.
        path = path.split('?', 1)[0]
        if path.startswith('/ui/'):
            path = path[3:]
        for part in ('css', 'fonts', 'images'):
            path = path.replace('/themes/xgs-auto/build/%s/' % part, '/themes/xgs/build/%s/' % part)
        return super().translate_path(path)

    def end_headers(self):
        # A page of the appliance loads these from another origin: fonts need the header to be used.
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    handler = functools.partial(Handler, directory=os.path.abspath(ROOT))
    http.server.ThreadingHTTPServer(('127.0.0.1', port), handler).serve_forever()
