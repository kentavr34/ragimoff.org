#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Исправить номера глав внутри файлов bolme-20, bolme-21, bolme-22
чтобы h1 совпадал с реальным порядком в сайдбаре.
"""
import os

BASE = r"C:\Users\SAM\Desktop\sayt2\klinik-psixiatriya"

FIXES = [
    # (файл, старый h1, новый h1, старый id, новый id)
    (
        "bolme-20.html",
        '<h1 id="bölmə-18" class="h-bolme">BÖLMƏ 18</h1>',
        '<h1 id="bölmə-20" class="h-bolme">BÖLMƏ 20</h1>',
    ),
    (
        "bolme-21.html",
        '<h1 id="bölmə-19" class="h-bolme">BÖLMƏ 19</h1>',
        '<h1 id="bölmə-21" class="h-bolme">BÖLMƏ 21</h1>',
    ),
    (
        "bolme-22.html",
        '<h1 id="bölmə-21" class="h-bolme">BÖLMƏ 21</h1>',
        '<h1 id="bölmə-22" class="h-bolme">BÖLMƏ 22</h1>',
    ),
]

for fname, old, new in FIXES:
    fpath = os.path.join(BASE, fname)
    with open(fpath, encoding='utf-8') as f:
        html = f.read()
    if old in html:
        html = html.replace(old, new, 1)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"{fname}: исправлено")
    else:
        print(f"{fname}: паттерн не найден — проверяю что есть:")
        import re
        m = re.search(r'<h1[^>]*class="h-bolme"[^>]*>[^<]+</h1>', html)
        if m: print(f"  найдено: {m.group()}")
