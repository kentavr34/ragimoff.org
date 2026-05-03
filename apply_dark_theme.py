#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add <link rel="stylesheet" href="gtc-dark.css"> to all main site HTML pages,
directly after the <link rel="stylesheet" href="gtc.css"> line.
"""
import sys, io, os, glob, unicodedata

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = r"C:\Users\SAM\Desktop\sayt2"

def nfc(s): return unicodedata.normalize('NFC', s)

added = 0
skipped = 0

for fpath in sorted(glob.glob(os.path.join(ROOT, '*.html'))):
    slug = os.path.basename(fpath).replace('.html', '')
    if slug == 'template':
        continue

    with open(fpath, encoding='utf-8') as f:
        html = nfc(f.read())

    # Skip if already has dark theme
    if 'gtc-dark.css' in html:
        skipped += 1
        continue

    # Insert after gtc.css link
    if 'href="gtc.css"' in html:
        html = html.replace(
            'href="gtc.css"',
            'href="gtc.css"',
            1
        )
        # Find the full link tag and insert after it
        import re
        html = re.sub(
            r'(<link[^>]+href="gtc\.css"[^>]*/>)',
            r'\1\n    <link rel="stylesheet" href="gtc-dark.css" />',
            html, count=1
        )
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html)
        added += 1
    else:
        print(f'  WARNING: no gtc.css found in {slug}.html')

print(f'Dark theme link added: {added} pages, skipped: {skipped}')
