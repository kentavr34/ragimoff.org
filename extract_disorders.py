#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extract all h-disorder headings with ICD codes from all bolme-*.html files.
"""
import sys, io, os, glob, re, unicodedata

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r"C:\Users\SAM\Desktop\sayt2\klinik-psixiatriya"

def nfc(s): return unicodedata.normalize('NFC', s)
def strip_tags(s): return re.sub(r'<[^>]+>', '', s).strip()

results = []

for fpath in sorted(glob.glob(os.path.join(BASE, 'bolme-*.html'))):
    fname = os.path.basename(fpath).replace('.html','')
    with open(fpath, encoding='utf-8') as f:
        html = f.read()
    html = nfc(html)

    for m in re.finditer(
        r'<h1[^>]+class="h-disorder"[^>]*>(.*?)</h1>',
        html, re.DOTALL | re.IGNORECASE
    ):
        raw = m.group(1)
        # Extract ICD code from <span class="icd">...</span>
        code_m = re.search(r'class="icd">([^<]+)<', raw)
        code = code_m.group(1).strip() if code_m else ''
        title = strip_tags(raw).strip()
        # Remove code from beginning of title if present
        title_clean = re.sub(r'^' + re.escape(code) + r'\s*', '', title).strip()
        results.append((fname, code, title_clean))

print(f"{'Page':<14} {'Code':<10} {'AZ Heading'}")
print('-' * 90)
for page, code, title in results:
    print(f"{page:<14} {code:<10} {title[:65]}")

print(f'\nTotal: {len(results)} disorders')
