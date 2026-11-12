# -*- coding: utf-8 -*-
"""Сверка языков: у каждой страницы на ru / az / en должен быть один и тот же состав —
те же блоки в том же порядке и то же число элементов в каждом. Правило владельца (12.11.2026):
«все предложения 1:1 должны быть». Дополнительно ловит чужие письменности (иероглифы) в тексте.
Запуск: python parity_check.py [фильтр]   → печатает расхождения, код возврата 1 при их наличии."""
import io, os, sys, json, glob, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FLT = sys.argv[1] if len(sys.argv) > 1 else ""
LANGS = ("ru", "az", "en")
ALIEN = re.compile(u"[぀-ヿ㐀-鿿가-힯؀-ۿ֐-׿]")


def shape(d):
    out = []
    for b in d.get("blocks", []):
        n = ""
        for k in ("items", "rows", "p", "btns", "ids"):
            if isinstance(b.get(k), list):
                n += "%s%d " % (k, len(b[k]))
                if k == "items":
                    sub = [len(x.get("list", [])) for x in b[k] if isinstance(x, dict) and "list" in x]
                    if sub:
                        n += "list%s " % sub
        out.append("%s %s" % (b["type"], n.strip()))
    return out


def strings(o, acc):
    if isinstance(o, str):
        acc.append(o)
    elif isinstance(o, dict):
        for v in o.values():
            strings(v, acc)
    elif isinstance(o, list):
        for v in o:
            strings(v, acc)


bad = 0
pages = sorted(set(re.sub(r"\.(ru|az|en)\.json$", "", f) for f in glob.glob(os.path.join(D, "data", "*", "*.json"))))
for p in pages:
    name = os.path.relpath(p, os.path.join(D, "data")).replace(os.sep, "/")
    if FLT and FLT not in name:
        continue
    docs = {}
    for l in LANGS:
        fn = "%s.%s.json" % (p, l)
        if os.path.exists(fn):
            docs[l] = json.load(io.open(fn, encoding="utf-8"))
    miss = [l for l in LANGS if l not in docs]
    if miss:
        print("%s: нет языка %s" % (name, ",".join(miss)))
        bad += 1
    for l, d in docs.items():
        acc = []
        strings(d, acc)
        for s in acc:
            m = ALIEN.search(s)
            if m:
                print("%s.%s: чужая письменность «%s» — …%s…" % (name, l, m.group(0), s[max(0, m.start() - 30):m.end() + 30]))
                bad += 1
    if name.endswith("/index"):
        ns = dict((l, len(d.get("items", []))) for l, d in docs.items())
        if len(set(ns.values())) > 1:
            print("%s: число элементов %s" % (name, ns))
            bad += 1
        continue
    sh = dict((l, shape(d)) for l, d in docs.items())
    base = sh.get("ru") or list(sh.values())[0]
    for l, s in sh.items():
        if s != base:
            bad += 1
            print("%s: %s отличается от ru (блоков %d против %d)" % (name, l, len(s), len(base)))
            for i in range(max(len(s), len(base))):
                a = base[i] if i < len(base) else "—"
                b = s[i] if i < len(s) else "—"
                if a != b:
                    print("     %2d  ru: %-34s %s: %s" % (i, a, l, b))
print("расхождений:", bad)
sys.exit(1 if bad else 0)
