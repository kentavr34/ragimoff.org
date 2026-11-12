# -*- coding: utf-8 -*-
"""Поиск по библиотеке: в какой книге, в какой главе и в каком абзаце написано (как по картотеке).
Ищет по тексту глав books/<книга>/<язык>/NN.html; регистр и «ё/е» не важны; все слова должны встретиться в одном абзаце.
Запуск: python library_find.py <слова> [--book книга] [--lang az|ru|en] [--max N]
Пример: python library_find.py "чувство вины" детство --lang ru"""
import io, os, re, sys, json, glob, html
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
args = sys.argv[1:]
opt = {"--book": "", "--lang": "", "--max": "30"}
words = []
i = 0
while i < len(args):
    if args[i] in opt and i + 1 < len(args):
        opt[args[i]] = args[i + 1]
        i += 2
    else:
        words += args[i].split()
        i += 1
if not words:
    print(__doc__)
    sys.exit(0)
norm = lambda s: s.lower().replace(u"ё", u"е")
W = [norm(w) for w in words]
found = 0
for pj in sorted(glob.glob(os.path.join(D, "books", "*", "book.json"))):
    P = json.load(io.open(pj, encoding="utf-8"))
    if opt["--book"] and opt["--book"] not in P["id"]:
        continue
    for l in P["langs"]:
        if opt["--lang"] and l != opt["--lang"]:
            continue
        for n, ch in enumerate(P["toc"][l], 1):
            f = os.path.join(D, "books", P["id"], l, "%03d.html" % n)
            if not os.path.isfile(f):
                continue
            raw = io.open(f, encoding="utf-8").read()
            if not all(w in norm(raw) for w in W):
                continue
            for k, par in enumerate(re.findall(r"<(?:p|h3|h4|li|td|blockquote)[^>]*>(.*?)</(?:p|h3|h4|li|td|blockquote)>", raw, flags=re.S), 1):
                t = html.unescape(re.sub(r"<[^>]+>", "", par))
                nt = norm(t)
                if all(w in nt for w in W):
                    found += 1
                    j = max(0, nt.find(W[0]) - 70)
                    print("%s [%s] · глава %d «%s» · абзац %d\n    …%s…\n    read.html?b=%s&c=%d" % (P["t"][l], l, n, ch["t"][:60], k, re.sub(r"\s+", " ", t[j:j + 220]), P["id"], n))
                    if found >= int(opt["--max"]):
                        print("показаны первые %d совпадений" % found)
                        sys.exit(0)
print("совпадений: %d" % found)
