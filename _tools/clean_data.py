# -*- coding: utf-8 -*-
"""Чистка данных внутренних страниц: в строках остаются только strong, em, b, i, a, br, sup, sub. Статьи блога (prose) не трогаются."""
import re, glob, io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
n = 0
for f in glob.glob(os.path.join(D, "data", "*", "*.json")):
    if os.sep + "blog" + os.sep in f:
        continue
    s = io.open(f, encoding="utf-8").read()
    t = re.sub(r"</?(span|div|p|small|u|font)(\s[^>]*)?>", "", s)
    if t != s:
        io.open(f, "w", encoding="utf-8", newline="\n").write(t)
        n += 1
        print("очищен", os.path.relpath(f, D))
print("очищено файлов:", n)
