# -*- coding: utf-8 -*-
"""Прототип книжного магазина (12.11.2026): стили раздела SHP, оболочки shop.html и book.html, страницы в проверке.
Повторный запуск ничего не меняет."""
import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(D)

p = "assets/css/site.css"
s = io.open(p, encoding="utf-8").read()
if "SHP: прототип" not in s:
    s += io.open("_agent/lab/shp.css", encoding="utf-8").read()
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
    print("стили SHP добавлены")

p = "_tools/make_shells.py"
s = io.open(p, encoding="utf-8").read()
if "SHOP_MAIN" not in s:
    a = "# индекс консультаций"
    assert s.count(a) == 1
    add = '''# прототип книжного магазина и страницы книги: та же рама, свой сценарий
SHOP_MAIN = """<main id="top" class="pp shp">
  <section class="pp__hero"><div class="wrap" id="shpHero"></div></section>
  <div id="shpBody"></div>
  <section class="sec sec--soc"><div class="wrap"><div class="soc rv"><p class="soc__h" id="socH"></p><ul class="soc__l" id="socList"></ul></div></div></section>
</main>"""
for name, kind in (("shop", "shop"), ("book", "book")):
    h = re.sub(r"<main.*?</main>", lambda m: SHOP_MAIN, src, flags=re.S)
    h = h.replace('<body class="inner">', '<body class="inner" data-kind="%s">' % kind).replace("assets/js/page-program.js", "assets/js/page-shop.js")
    assert "page-shop.js" in h and 'data-kind="%s"' % kind in h, name
    io.open(os.path.join(D, name + ".html"), "w", encoding="utf-8", newline=chr(10)).write(h)
    print("оболочка:", name + ".html")

'''
    s = s.replace(a, add + a)
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
    print("make_shells: магазин добавлен")

p = "_tools/pages_check.py"
s = io.open(p, encoding="utf-8").read()
if "shop.html" not in s:
    a = '    ps = ["index.html", "specialist.html?s=kenan"'
    assert s.count(a) == 1
    s = s.replace(a, '    ps = ["index.html", "shop.html", "book.html?b=klinik", "book.html?b=art-freud-gw02", "specialist.html?s=kenan"')
    a = 'if not pg.startswith(("program", "index")) and'
    assert s.count(a) == 1
    s = s.replace(a, 'if not pg.startswith(("program", "index", "shop", "book")) and')
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
    print("pages_check: страницы магазина добавлены")
