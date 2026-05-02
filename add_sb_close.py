#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import glob, os, re

BASE = r"C:\Users\SAM\Desktop\sayt2\klinik-psixiatriya"

OLD = '<div class="sb-hdr"><h3>📋 Mündəricat</h3></div>'
NEW = '<div class="sb-hdr"><h3>📋 Mündəricat</h3><button class="sb-close" onclick="toggleSb()" aria-label="Bağla">✕</button></div>'

files = sorted(glob.glob(os.path.join(BASE, "*.html")))
updated = 0
for fpath in files:
    with open(fpath, encoding='utf-8') as f:
        html = f.read()
    if OLD in html:
        html = html.replace(OLD, NEW, 1)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html)
        updated += 1

print(f"Обновлено: {updated} файлов")
