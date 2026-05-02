#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Исправить неверные nav-code в сайдбарах всех файлов"""
import glob, os

BASE = r"C:\Users\SAM\Desktop\sayt2\klinik-psixiatriya"

FIXES = [
    ("6C72–ni",   "6C70–6C7Z"),   # bolme-13
    ("6D10.0–2",  "6D10–6D1Z"),   # bolme-15
]

all_html = sorted(glob.glob(os.path.join(BASE, "*.html")))
total = 0

for fpath in all_html:
    with open(fpath, encoding='utf-8') as f:
        html = f.read()
    original = html
    for bad, good in FIXES:
        html = html.replace(bad, good)
    if html != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html)
        total += 1

print(f"Исправлено в {total} файлах")
