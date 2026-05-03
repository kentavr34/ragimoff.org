#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wraps all bare DSM-5-TR codes in <span class="icd"> tags.
Handles: single codes (295.90, 319, 300.xx), ranges (307.20–307.23).
"""
import sys, io, os, re, unicodedata, glob

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r"C:\Users\SAM\Desktop\sayt2\klinik-psixiatriya"

# Pattern: DSM-5-TR:</span> CODE — ...
# CODE can be:  digits with optional .digits/x  e.g. 319, 295.90, 296.2x, 300.xx, 309.xx
# Range:        CODE–CODE  (en-dash)
CODE_PAT = r'[\d][\d]*(?:\.[\dx]+)?'
RANGE_PAT = rf'({CODE_PAT})(–)({CODE_PAT})'
SINGLE_PAT = rf'({CODE_PAT})'

TAG = '<span class="xbt-lbl">DSM-5-TR:</span> '

def wrap(code):
    return f'<span class="icd">{code}</span>'

def fix_line(line):
    if TAG not in line:
        return line
    # Split at the tag
    pre, rest = line.split(TAG, 1)
    # rest looks like: CODE — ... or CODE–CODE — ...
    # Try range first
    m = re.match(rf'^({CODE_PAT})(–)({CODE_PAT})( — .*)$', rest)
    if m:
        new_rest = wrap(m.group(1)) + ' – ' + wrap(m.group(3)) + m.group(4)
        return pre + TAG + new_rest
    # Try single code
    m = re.match(rf'^({CODE_PAT})( — .*)$', rest)
    if m:
        new_rest = wrap(m.group(1)) + m.group(2)
        return pre + TAG + new_rest
    return line

total_files = 0
total_fixes = 0

for fpath in sorted(glob.glob(BASE + r'\*.html')):
    with open(fpath, encoding='utf-8') as f:
        html = f.read()
    html = unicodedata.normalize('NFC', html)

    lines = html.split('\n')
    new_lines = []
    file_fixes = 0
    for line in lines:
        new_line = fix_line(line)
        if new_line != line:
            file_fixes += 1
        new_lines.append(new_line)

    if file_fixes > 0:
        new_html = '\n'.join(new_lines)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_html)
        print(f'  {os.path.basename(fpath)}: {file_fixes} fix(es)')
        total_files += 1
        total_fixes += file_fixes

print(f'\nDone. {total_files} files, {total_fixes} total fixes.')
