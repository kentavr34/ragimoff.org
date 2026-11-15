# -*- coding: utf-8 -*-
"""Перенос правок базы истины (truth.edit_log) в тексты книг сайта (15.11.2026).
Вход: JSON-список {book, lang, para, old, new, why} (выгрузка edit_log). Для каждой правки берётся отличающийся кусок
(общее начало/конец отрезаны, края расширены до границ слов) и заменяется в файлах books/<book>/<lang>/ — только если
«было» встречается во всей книге этого языка РОВНО один раз и «стало» ещё нет. Иначе — в отчёт, без правки.
  python _tools/apply_db_edits.py <edits.json> [--dry]"""
import io, os, re, sys, json, glob, html
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
E = json.load(open(sys.argv[1], encoding="utf-8")); DRY = "--dry" in sys.argv

def diff_piece(o, n, ctx=12):
    i = 0
    while i < min(len(o), len(n)) and o[i] == n[i]: i += 1
    j = 0
    while j < min(len(o), len(n)) - i and o[-1 - j] == n[-1 - j]: j += 1
    a, bo, bn = max(0, i - ctx), len(o) - j, len(n) - j
    while a > 0 and o[a - 1] not in " \n": a -= 1
    eo, en = min(len(o), bo + ctx), min(len(n), bn + ctx)
    while eo < len(o) and o[eo] not in " \n.,;:": eo += 1; en += 1
    return o[a:eo], n[a:min(en, len(n))]

def variants(s):  # текст в HTML может быть с сущностями
    yield s
    yield html.escape(s, quote=False)
    yield s.replace(" ", "&nbsp;")

rep = []
for e in E:
    files = sorted(glob.glob(os.path.join(D, "books", e["book"], e["lang"], "*.html")))
    old, new = diff_piece(e["old"] or "", e["new"] or "")
    hit = None
    for vo, vn in zip(variants(old), variants(new)):
        cnt = [(f, io.open(f, encoding="utf-8").read().count(vo)) for f in files]
        tot = sum(c for _, c in cnt)
        if tot == 1:
            hit = (next(f for f, c in cnt if c), vo, vn); break
    if not hit:
        already = any(new in html.unescape(io.open(f, encoding="utf-8").read()) for f in files)
        rep.append((e["book"], e["lang"], e["para"], "уже на сайте" if already else "не найдено однозначно", old[:70])); continue
    f, vo, vn = hit
    if not DRY:
        t = io.open(f, encoding="utf-8").read().replace(vo, vn)
        io.open(f, "w", encoding="utf-8", newline="").write(t)
    rep.append((e["book"], e["lang"], e["para"], "применено", os.path.basename(f) + ": " + vo[:40] + " → " + vn[:40]))
for r in rep: print(" | ".join(r))
print("итог:", {s: sum(1 for r in rep if r[3] == s) for s in set(r[3] for r in rep)})
