# -*- coding: utf-8 -*-
"""Третий дожим NEXT (28.11.2026): короткие ячейки таблиц и блоки, не найденные целиком.
Привязка — к соседней ячейке слева (предыдущий блок той же таблицы по выгрузке NEXT): <td>сосед</td><td>было</td> ->
<td>сосед</td><td>стало</td>; замена только при ЕДИНСТВЕННОМ совпадении в копии. Для ячеек без соседа слева (первый столбец)
привязка — к соседу справа. Остальное — в отчёт.
  python _tools/klinik_apply_cells.py <paras.json> <next_dump.json> --lang az [--dry]"""
import glob, html, io, json, os, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(D)
dry = "--dry" in sys.argv
L = sys.argv[sys.argv.index("--lang") + 1]
P = json.load(io.open(sys.argv[1], encoding="utf-8"))
X = json.load(io.open(sys.argv[2], encoding="utf-8"))["paras"]
idx = {p["para_id"]: i for i, p in enumerate(X)}
esc = lambda s: html.escape(s, quote=False)
copies = {"books": glob.glob("books/klinik-psixiatriya/%s/*.html" % L), "read": glob.glob("%s/read/klinik-psixiatriya/*.html" % L)}
T = {f: io.open(f, encoding="utf-8", newline="").read() for fs in copies.values() for f in fs}
orig = dict(T)
TD = r"<td[^>]*>"
done, rep = 0, []
REST = {l.split("\t")[0] for l in io.open("_agent/klinik_rest_%s.tsv" % L, encoding="utf-8").read().splitlines()[1:]}
plain = " ".join(re.sub("<[^>]+>", " ", t) for t in T.values())
for key, v in P.items():
    old, new = (v.get("old") or ""), (v.get("new") or "")
    if key not in REST or old == new or key not in idx or " " in new or not old.strip() and not new.strip():
        continue
    if len(new) >= 12 and esc(new) in plain:
        continue
    i = idx[key]
    pr = X[i - 1]["text"] if i > 0 else None
    nx = X[i + 1]["text"] if i + 1 < len(X) else None
    pats = []
    if pr is not None:
        pats.append((r"(>%s</td>\s*%s)%s(</td>)" % (re.escape(esc(pr)), TD, re.escape(esc(old))), "слева"))
    if nx is not None:
        pats.append((r"(%s)%s(</td>\s*%s%s<)" % (TD, re.escape(esc(old)), TD, re.escape(esc(nx))), "справа"))
    ok = False
    for pat, side in pats:
        for cname, fs in copies.items():
            hits = [(f, m) for f in fs for m in re.finditer(pat, T[f])]
            if len(hits) == 1:
                f, m = hits[0]
                T[f] = T[f][:m.start()] + m.group(1) + esc(new) + m.group(2) + T[f][m.end():]
                ok = True
        if ok:
            break
    if ok:
        done += 1
    else:
        rep.append((key, old[:60], new[:60]))
changed = [f for f in T if T[f] != orig[f]]
if not dry:
    for f in changed:
        io.open(f, "w", encoding="utf-8", newline="").write(T[f])
for r in rep:
    print("  не тронуто:", r[0][-6:], repr(r[1]), "→", repr(r[2]))
print(L, "ячеек исправлено:", done, "| файлов:", len(changed), "(проба)" if dry else "")
