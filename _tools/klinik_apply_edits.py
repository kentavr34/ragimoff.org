# -*- coding: utf-8 -*-
"""Перенос правок «Клинической психиатрии» из базы истины на сайт (13.11.2026).
Сайт книги собран до ночной вычитки и до исправления фактов 13.11; отдельного сборщика сайта из печати у этой книги нет
(читалка с деревьями классификаций). Поэтому каждая правка журнала (edit_log: было → стало) переносится в текст глав
books/klinik-psixiatriya/<язык>/*.html точечно: «было» найдено ровно один раз — заменяется; «стало» уже есть — пропуск;
не найдено или найдено несколько раз — в отчёт (_agent/klinik_edits_report.tsv), без правки.
  python _tools/klinik_apply_edits.py <edits.tsv> [--dry]"""
import csv, glob, html, io, os, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(D)
dry = "--dry" in sys.argv
rows = list(csv.DictReader(io.open(sys.argv[1], encoding="utf-8"), delimiter="\t"))
files = {}
for lang in ("az", "ru", "en", "tr"):
    for f in sorted(glob.glob("books/klinik-psixiatriya/%s/*.html" % lang)):
        files[f] = io.open(f, encoding="utf-8").read()
orig = dict(files)
rep, stat = [], {}


def variants(t):
    v = [t, html.escape(t, quote=False)]
    return [x for i, x in enumerate(v) if x and x not in v[:i]]


for r in rows:
    lang, old, new = r["lang"], r["old_text"], r["new_text"]
    fs = [f for f in files if f.startswith("books/klinik-psixiatriya/%s/" % lang)]
    done = False
    for o, n in zip(variants(old), variants(new)) if html.escape(old, quote=False) != old else [(old, new)]:
        hits = [(f, files[f].count(o)) for f in fs if o in files[f]]
        total = sum(c for _, c in hits)
        if total == 1:
            f = hits[0][0]
            files[f] = files[f].replace(o, n, 1)
            res = "применено"
            done = True
            break
        if total > 1:
            res = "несколько мест (%d)" % total
            break
    else:
        res = "уже есть" if any(n in files[f] for f in fs for n in variants(new)) else "не найдено"
    if not done and res == "не найдено" and any(x in files[f] for f in fs for x in variants(new)):
        res = "уже есть"
    stat[res.split(" (")[0]] = stat.get(res.split(" (")[0], 0) + 1
    rep.append((lang, r["version_id"], r["edit_id"], res, old[:120].replace("\t", " ").replace("\n", " "), new[:120].replace("\t", " ").replace("\n", " ")))
changed = [f for f in files if files[f] != orig[f]]
if not dry:
    for f in changed:
        io.open(f + ".new", "w", encoding="utf-8", newline="\n").write(files[f])
        os.replace(f + ".new", f)
os.makedirs("_agent", exist_ok=True)
io.open("_agent/klinik_edits_report.tsv", "w", encoding="utf-8").write("язык\tверсия\tправка\tитог\tбыло\tстало\n" + "\n".join("\t".join(x) for x in rep) + "\n")
print("правок:", len(rows), "|", stat, "| файлов изменено:", len(changed), "(проба)" if dry else "")
