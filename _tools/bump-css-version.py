# -*- coding: utf-8 -*-
"""Сброс кэша CSS: book.css?v=N → v=N+1 во всех страницах сайта (правится в OLD/NEW)."""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLD, NEW = "book.css?v=7", "book.css?v=8"   # ← версии для замены
pat = re.compile(r"(/books/)?book\.css\?v=\d+")
n = 0
for dp, dn, fn in os.walk(ROOT):
    dn[:] = [d for d in dn if not d.startswith(".") and not d.endswith(".bak_20260929")]
    for f in fn:
        if not f.endswith(".html"):
            continue
        fp = os.path.join(dp, f)
        with open(fp, encoding="utf-8", newline="") as fh:
            s = fh.read()
        if OLD not in s:
            continue
        with open(fp, "w", encoding="utf-8", newline="") as fh:
            fh.write(s.replace(OLD, NEW))
        n += 1
print("страниц с %s → %s: %d" % (OLD, NEW, n))
