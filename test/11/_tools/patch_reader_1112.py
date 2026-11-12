# -*- coding: utf-8 -*-
"""Единая читалка библиотеки (12.11.2026): стили раздела RDR, оболочка read.html, ссылки «Читать» из магазина,
страница в проверке. Повторный запуск ничего не меняет."""
import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(D)


def rep(s, a, b):
    assert s.count(a) == 1, "ожидалось 1: " + a[:70]
    return s.replace(a, b)


p = "assets/css/site.css"
s = io.open(p, encoding="utf-8").read()
if "RDR: единая читалка" not in s:
    s += io.open("_agent/lab/rdr.css", encoding="utf-8").read()
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
    print("стили RDR добавлены")

p = "_tools/make_shells.py"
s = io.open(p, encoding="utf-8").read()
if "READ_MAIN" not in s:
    a = "# индекс консультаций"
    add = '''# единая читалка библиотеки: одна страница на все книги и языки (текст — books/<книга>/<язык>/NN.html)
READ_MAIN = """<main id="top" class="pp rdr">
  <div class="rdr__prog" id="rdProg"></div>
  <div class="rdr__bar" id="rdBar"></div>
  <section class="pp__hero"><div class="wrap">
    <div id="rdTitle"></div>
    <article class="rdr__chap" id="rdChap" hidden></article>
    <nav class="rdr__pager" id="rdPager" hidden><button type="button" id="rdPrev"><i></i><span></span></button><button type="button" id="rdNext"><i></i><span></span></button></nav>
  </div></section>
  <aside class="rdr__toc" id="rdToc"><div class="rdr__toch"><h2 id="rdTocT"></h2><button type="button" id="rdTocX">×</button></div><ol id="rdTocL"></ol></aside>
  <div class="rdr__scrim" id="rdScrim"></div>
  <div class="rdr__pop" id="rdPop" hidden></div>
</main>"""
h = re.sub(r"<main.*?</main>", lambda m: READ_MAIN, src, flags=re.S)
h = h.replace('<body class="inner">', '<body class="inner" data-kind="read">').replace("assets/js/page-program.js", "assets/js/reader.js")
assert "reader.js" in h and 'data-kind="read"' in h
io.open(os.path.join(D, "read.html"), "w", encoding="utf-8", newline=chr(10)).write(h)
print("оболочка: read.html")

'''
    s = rep(s, a, add + a)
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
    print("make_shells: читалка добавлена")

# магазин: «Читать» открывает книгу в новой читалке, если её текст есть в библиотеке
p = "_tools/build_shop.py"
s = io.open(p, encoding="utf-8").read()
if "LIB = " not in s:
    s = rep(s, "AZ_PRICE = {}", '''AZ_PRICE = {}
LIB = set(os.listdir(os.path.join(D, "books"))) if os.path.isdir(os.path.join(D, "books")) else set()      # книги, перенесённые в библиотеку
LIB_ID = {"guilt": "virus-viny", "pandemic": "shizofreniya", "phoenix": "phoenix-era"}''')
    s = rep(s, '        if lang == "az":\n            AZ_PRICE[it["id"]] = it["price"]', '''        lib = LIB_ID.get(it["id"], it["id"])
        if lib in LIB:
            it["read_new"] = "read.html?b=" + lib               # единая читалка новой системы
        if lang == "az":
            AZ_PRICE[it["id"]] = it["price"]''')
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
    print("build_shop: адрес новой читалки")
p = "assets/js/page-shop.js"
s = io.open(p, encoding="utf-8").read()
if "read_new" not in s:
    s = rep(s, '${it.read ? `<a class="btn" href="${esc(it.href)}">${esc(d.u.read)}</a>`', '${it.read ? `<a class="btn" href="${esc(it.read_new || it.href)}">${esc(d.u.read)}</a>`')
    s = rep(s, "book3d(it, lang, it.read ? esc(it.href) : '#')", "book3d(it, lang, it.read ? esc(it.read_new || it.href) : '#')")
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
    print("page-shop: кнопка «Читать» ведёт в новую читалку")

p = "_tools/pages_check.py"
s = io.open(p, encoding="utf-8").read()
if "read.html" not in s:
    s = rep(s, '    ps = ["index.html", "test.html", "shop.html",', '    ps = ["index.html", "test.html", "read.html?b=virus-viny", "read.html?b=virus-viny&c=3", "read.html?b=freud-gw02&c=2", "shop.html",')
    s = s.replace('pg.startswith(("program", "index", "shop", "book", "test")) and', 'pg.startswith(("program", "index", "shop", "book", "test", "read")) and')
    s = s.replace('not pg.startswith(("shop", "book", "test")):', 'not pg.startswith(("shop", "book", "test", "read")):')
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
    print("pages_check: читалка добавлена")
