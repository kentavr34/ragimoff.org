#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, io, glob, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = r"C:\Users\SAM\Desktop\sayt2\klinik-psixiatriya"

for fpath in sorted(glob.glob(BASE + r'\bolme-*.html')):
    with open(fpath, encoding='utf-8') as f:
        lines = f.readlines()
    fname = fpath.split('\\')[-1]
    for i, line in enumerate(lines):
        if 'h-disorder' in line:
            block = ''.join(lines[i:i+6])
            has_10  = 'XBT-10:' in block
            has_dsm = 'DSM-5-TR:' in block
            has_11  = 'XBT-11:' in block
            if not has_10 or not has_dsm:
                hid = re.search(r'id="([^"]+)"', line)
                hid = hid.group(1)[:60] if hid else '?'
                missing = []
                if not has_11:  missing.append('XBT-11')
                if not has_10:  missing.append('XBT-10')
                if not has_dsm: missing.append('DSM-5-TR')
                print(f'{fname}:{i+1} MISSING {"+".join(missing)} — [{hid}]')
