# -*- coding: utf-8 -*-
"""Перенос правок «Клинической психиатрии» AZ из базы истины на сайт по блокам (17.11.2026).
Вход — paras.json из kp_diff_json.py ({ключ: {old, new, edits}}). Правится каждая копия книги отдельно:
books/klinik-psixiatriya/az/*.html и az/read/klinik-psixiatriya/*.html.
В каждой копии: (1) весь текст блока «old» найден ровно один раз — заменяется на «new»;
(2) иначе — каждая правка блока (было→стало), если «было» длиной ≥6 знаков встречается в копии ровно один раз;
«стало» уже есть — пропуск; иначе — в отчёт _agent/klinik_paras_report.tsv без правки. Ничего не угадывает.
  python _tools/klinik_apply_paras.py <paras.json> [--dry]"""
import glob, html, io, json, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(D)
dry = "--dry" in sys.argv
LANG = sys.argv[sys.argv.index("--lang") + 1] if "--lang" in sys.argv else "az"
P = json.load(io.open(sys.argv[1], encoding="utf-8"))
COPIES = {"books": "books/klinik-psixiatriya/%s/*.html" % LANG, "read": "%s/read/klinik-psixiatriya/*.html" % LANG}


def variants(t):
    v = [t, html.escape(t, quote=False)]
    return [x for i, x in enumerate(v) if x and x not in v[:i]]


rep, stat, changed_all = [], {}, []
for cname, pat in COPIES.items():
    files = {f: io.open(f, encoding="utf-8").read() for f in sorted(glob.glob(pat))}
    orig = dict(files)

    def count(s):
        return [(f, files[f].count(s)) for f in files if s in files[f]]

    # одинаковые блоки (одна запись литературы в нескольких главах): сколько раз текст «old» стоит в базе
    same = {}
    for b in P.values():
        same.setdefault(b["old"], set()).add(b["new"])
    group_n = {}
    for b in P.values():
        group_n[b["old"]] = group_n.get(b["old"], 0) + 1
    done_groups = set()
    for key, b in P.items():
        old, new = b["old"].replace(" ", "\n"), b["new"].replace(" ", "\n")
        res = None
        if b["old"] in done_groups:
            res = "блок целиком (повтор записи)"
        n_db = group_n[b["old"]] if len(same[b["old"]]) == 1 else 1
        for o, n in zip(variants(old), variants(new)):
            if res or len(o) < 6:
                continue
            h = count(o)
            tot = sum(c for _, c in h)
            if tot == 1 or (tot == n_db and n_db > 1):
                for f, _ in h:
                    files[f] = files[f].replace(o, n)
                res = "блок целиком"
                if n_db > 1:
                    done_groups.add(b["old"])
                break
        if res is None:
            ok, miss = 0, 0
            for eo, en in b["edits"]:
                done = False
                for o, n in zip(variants(eo), variants(en)):
                    if len(o) < 6:
                        continue
                    h = count(o)
                    if sum(c for _, c in h) == 1:
                        f = h[0][0]; files[f] = files[f].replace(o, n, 1); done = True; break
                if done:
                    ok += 1
                elif len(en) >= 6 and any(count(x) for x in variants(en)):
                    ok += 1
                else:
                    miss += 1
            if ok and not miss:
                res = "по правкам"
            elif any(count(x) for x in variants(new) if len(x) >= 6):
                res = "уже есть"
            else:
                res = "НЕ ПЕРЕНЕСЕНО (%d из %d правок)" % (miss, ok + miss) if ok + miss else "НЕ НАЙДЕНО"
        k = cname + ": " + res.split(" (")[0]
        stat[k] = stat.get(k, 0) + 1
        rep.append((cname, key.split(":")[-1], res, old[:150].replace("\t", " ").replace("\n", " "), new[:150].replace("\t", " ").replace("\n", " ")))
    changed = [f for f in files if files[f] != orig[f]]
    changed_all += changed
    if not dry:
        for f in changed:
            io.open(f + ".new", "w", encoding="utf-8", newline="\n").write(files[f])
            os.replace(f + ".new", f)
os.makedirs("_agent", exist_ok=True)
io.open("_agent/klinik_paras_report.tsv", "w", encoding="utf-8").write(
    "копия\tблок\tитог\tбыло\tстало\n" + "\n".join("\t".join(x) for x in rep) + "\n")
print("блоков:", len(P), "|", stat, "| файлов изменено:", len(changed_all), "(проба)" if dry else "")
