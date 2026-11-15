# -*- coding: utf-8 -*-
"""В какой книге сайта лежит текст правок базы (имена книг базы и сайта расходятся).
  python _tools/find_book_of_text.py <diffs.json> <slug> [<slug> …]"""
import io, sys, json, glob, re, html, os, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
E = json.load(open(sys.argv[1], encoding="utf-8"))
T = {}
for f in glob.glob(os.path.join("books", "freud-*", "az", "*.html")):
    bk = os.path.normpath(f).split(os.sep)[1]
    T[f] = (bk, " ".join(html.unescape(re.sub(r"<[^>]+>", "", open(f, encoding="utf-8").read())).split()))
Q = re.compile("[„“”«»\"]")
for b in sys.argv[2:]:
    tot = collections.Counter()
    for e in [x for x in E if x["book"] == b][:8]:
        frag = Q.sub("", " ".join(e["new"].split()))[20:60]
        for f, (bk, t) in T.items():
            if frag and frag in Q.sub("", t): tot[bk] += 1
    print(b, "→", tot.most_common(3))
