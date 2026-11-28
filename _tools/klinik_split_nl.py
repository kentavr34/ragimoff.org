# -*- coding: utf-8 -*-
"""NEXT 28.11.2026: многочастные блоки базы (части через U+2029) при переносе на сайт стали одним элементом с переводом строки
внутри (<li>часть1\nчасть2</li>). Разбивает такие <li>/<p>/<td> (без вложенных тегов) на соседние элементы того же тега.
Трогает только элементы, изменённые в рабочей копии относительно git HEAD (чтобы не задеть прежнюю вёрстку).
  python _tools/klinik_split_nl.py [--dry]"""
import glob, io, os, re, subprocess, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(D)
dry = "--dry" in sys.argv
PAT = re.compile(r"(<(li|p|td)\b[^>]*>)([^<]*\n[^<]*)(</\2>)")
files = glob.glob("books/klinik-psixiatriya/*/*.html") + glob.glob("*/read/klinik-psixiatriya/*.html")
tot = 0
for f in files:
    t = io.open(f, encoding="utf-8", newline="").read()
    rel = f.replace(os.sep, "/")
    try:
        head = subprocess.run(["git", "show", "HEAD:" + rel], capture_output=True, encoding="utf-8").stdout
    except Exception:
        head = ""
    n = 0

    def sub(m):
        global n
        if m.group(0) in head:      # было так и до переноса — не трогаем
            return m.group(0)
        parts = [x.strip() for x in m.group(3).split("\n") if x.strip()]
        if len(parts) < 2:
            return m.group(0)
        n += 1
        return ("%s\n%s" % (m.group(4), m.group(1))).join(parts).join([m.group(1), m.group(4)])
    t2 = PAT.sub(sub, t)
    if t2 != t:
        tot += n
        print(f, "разбито элементов:", n)
        if not dry:
            io.open(f, "w", encoding="utf-8", newline="").write(t2)
print("всего:", tot, "(проба)" if dry else "")
