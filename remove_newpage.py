#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import glob, os

BASE = r"C:\Users\SAM\Desktop\sayt2\klinik-psixiatriya"
all_files = sorted(glob.glob(os.path.join(BASE, "*.html")))

# Literal: <p>\newpage</p>  (backslash + newpage)
target = "<p>\x5cnewpage</p>"

changed = 0
total_removed = 0
for fpath in all_files:
    with open(fpath, encoding="utf-8") as f:
        html = f.read()
    count = html.count(target)
    if count:
        new_html = html.replace(target + "\n", "").replace(target, "")
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(new_html)
        changed += 1
        total_removed += count
        print(f"  {os.path.basename(fpath)}: убрано {count}")

print(f"\nИтого: {total_removed} удалено из {changed} файлов")
