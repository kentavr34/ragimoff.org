# -*- coding: utf-8 -*-
"""Карта сайта sitemap.xml: все страницы новой системы. Запуск из корня сайта: python _tools/build_sitemap.py"""
import io, os, re, sys, json, glob, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(D)
B = "https://ragimoff.org/"
slugs = lambda sec: sorted(set(os.path.basename(f).split(".")[0] for f in glob.glob("data/%s/*.json" % sec)))
u = ["", "shop.html", "blog.html", "contact.html", "corporate.html", "test.html"]
m = re.search(r"order:\s*\[([^\]]*)\]", io.open("assets/js/programs.js", encoding="utf-8").read())
u += ["program.html?p=" + s for s in re.findall(r"'([\w-]+)'", m.group(1))]
u += ["specialist.html?s=" + s for s in slugs("spec")]
u += ["consult.html?c=" + s for s in slugs("cons") if s != "index"]
u += ["article.html?a=" + s for s in slugs("blog") if s != "index"]
for b in json.load(io.open("books/index.json", encoding="utf-8"))["books"]:
    u += ["book.html?b=" + b["id"], "read.html?b=" + b["id"]]
P = json.load(io.open("books/klinik-psixiatriya/book.json", encoding="utf-8"))
u += ["read.html?b=klinik-psixiatriya&amp;p=" + x["id"] for x in P["toc"]["az"]]
day = datetime.date.today().isoformat()
x = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join("<url><loc>%s%s</loc><lastmod>%s</lastmod></url>\n" % (B, a, day) for a in u) + "</urlset>\n"
io.open("sitemap.xml", "w", encoding="utf-8", newline="\n").write(x)
print("адресов в карте сайта:", len(u))
