# -*- coding: utf-8 -*-
"""Дожим переноса правок «Клинической психиатрии» на сайт после klinik_apply_paras.py (28.11.2026, NEXT).
Для блоков, чей новый текст ещё не появился ни в одной копии: прежний текст блока (длиной ≥ 12 знаков), стоящий
ЦЕЛЫМ содержимым элемента (>было<), заменяется на новый во всех местах копии (текст + оглавление + содержание).
Короткие (ячейки «✓», «—», пустые) и не найденные целиком — не трогаются, а пишутся в отчёт _agent/klinik_rest_<lang>.tsv.
Многочастные блоки (U+2029) — части становятся соседними элементами того же тега.
  python _tools/klinik_apply_rest.py <paras.json> --lang az [--dry]"""
import glob, html, io, json, os, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(D)
dry = "--dry" in sys.argv
L = sys.argv[sys.argv.index("--lang") + 1]
P = json.load(io.open(sys.argv[1], encoding="utf-8"))
files = glob.glob("books/klinik-psixiatriya/%s/*.html" % L) + glob.glob("%s/read/klinik-psixiatriya/*.html" % L)
T = {f: io.open(f, encoding="utf-8", newline="").read() for f in files}
orig = dict(T)
esc = lambda s: html.escape(s, quote=False)
rep, done = [], 0
for key, v in P.items():
    old, new = (v.get("old") or ""), (v.get("new") or "")
    if old == new:
        continue
    parts = new.split(" ")
    if parts[0] and any(esc(parts[0]) in t or parts[0] in t for t in T.values()) and len(parts[0]) >= 12:
        continue  # уже перенесено
    if len(old.strip()) < 12:
        rep.append((key, "коротко — вручную", old[:80], new[:80]))
        continue
    hit = 0
    for f, t in T.items():
        for o in {old, esc(old)}:
            pat = re.compile(r"(<(td|li|p|h[1-6]|a|span|th)\b[^>]*>)" + re.escape(o) + r"(</\2>)")
            def sub(m):
                tag, op, cl = m.group(2), m.group(1), m.group(3)
                return op + ("%s\n%s" % (cl, op)).join(esc(x) for x in parts) + cl
            t2, n = pat.subn(sub, t)
            if n:
                T[f] = t = t2
                hit += n
    if hit:
        done += 1
    else:
        rep.append((key, "не найдено целым элементом", old[:80], new[:80]))
changed = [f for f in T if T[f] != orig[f]]
if not dry:
    for f in changed:
        io.open(f, "w", encoding="utf-8", newline="").write(T[f])
with io.open("_agent/klinik_rest_%s.tsv" % L, "w", encoding="utf-8") as w:
    w.write("блок\tитог\tбыло\tстало\n")
    for r in rep:
        w.write("\t".join(x.replace("\t", " ").replace("\n", " ") for x in r) + "\n")
print(L, "дожато блоков:", done, "| осталось:", len(rep), "| файлов изменено:", len(changed), "(проба)" if dry else "")
