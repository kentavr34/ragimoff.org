#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Исправляет артефакт Python lowercase: İ → i̇ (U+0069 + U+0307)
В азербайджанском İ в нижнем регистре = простое i (U+0069)
"""
import glob, os

BASE = r"C:\Users\SAM\Desktop\sayt2\klinik-psixiatriya"
BAD  = "i̇"   # i + combining dot above (артефакт Python lower())
GOOD = "i"         # простое i

all_files = sorted(glob.glob(os.path.join(BASE, "bolme-*.html")))
changed = 0
for fpath in all_files:
    with open(fpath, encoding="utf-8") as f:
        html = f.read()
    if BAD in html:
        fixed = html.replace(BAD, GOOD)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(fixed)
        n = html.count(BAD)
        changed += 1
        print(f"  {os.path.basename(fpath)}: исправлено {n} символов i̇→i")

print(f"\nФайлов исправлено: {changed}")
