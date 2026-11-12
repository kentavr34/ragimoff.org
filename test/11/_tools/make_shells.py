# -*- coding: utf-8 -*-
"""Оболочки внутренних страниц: рама (шапка, подвал, окно просмотра, кнопка WhatsApp) берётся из program.html — один источник.
Запуск: python make_shells.py — пересоздаёт specialist/consult/contact/corporate/law/blog/article.html и индексы разделов."""
import io, os, re, json, glob, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SHELLS = {"specialist": ("spec", ""), "consult": ("cons", ""), "contact": ("page", "contact"), "corporate": ("page", "corporate"),
          "blog": ("blog", ""), "article": ("post", "")}
CONS = ["panik-ataklar", "depressiya", "sosial-fobiya", "enurez", "aile-terapiyasi", "tesvis-pozuntulari", "okp", "aile-usaq-terapiyasi", "valideyn-mektebi"]
MAIN = """<main id="top" class="pp pg">
  <section class="pp__hero"><div class="wrap pg__hero" id="pgHero"></div></section>
  <div id="pgBlocks"></div>
  <section class="sec" id="reg"><div class="wrap"><header class="sh"><h2 class="sh__h rv" id="regH"></h2><p class="sh__s rv" id="regS"></p></header><div class="reg" id="regBox"></div></div></section>
  <section class="sec sec--soc"><div class="wrap"><nav class="pp__other rv" id="ppOther"></nav><div class="soc rv"><p class="soc__h" id="socH"></p><ul class="soc__l" id="socList"></ul></div></div></section>
</main>"""
LB = '<div class="lb" id="lb" aria-hidden="true"><button type="button" class="lb__x" aria-label="×">×</button><button type="button" class="lb__a lb__a--p" id="lbPrev" aria-label="←">‹</button><button type="button" class="lb__a lb__a--n" id="lbNext" aria-label="→">›</button><figure><img id="lbImg" alt=""><figcaption id="lbCap"></figcaption></figure></div>'

src = io.open(os.path.join(D, "program.html"), encoding="utf-8").read()
assert src.count("<main") == 1 and 'page-program.js' in src
for name, (kind, slug) in SHELLS.items():
    h = re.sub(r"<main.*?</main>", lambda m: MAIN, src, flags=re.S)
    h = h.replace('<body class="inner">', '<body class="inner" data-kind="%s"%s>' % (kind, ' data-slug="%s"' % slug if slug else ""))
    h = re.sub(r'<div class="lb" id="lb".*?</div>\n', lambda m: LB + "\n", h, flags=re.S)
    h = h.replace("assets/js/page-program.js", "assets/js/page.js")
    assert 'data-kind="%s"' % kind in h and "page.js" in h and 'id="lbPrev"' in h, name
    io.open(os.path.join(D, name + ".html"), "w", encoding="utf-8", newline="\n").write(h)
    print("оболочка:", name + ".html")

# прототип книжного магазина и страницы книги: та же рама, свой сценарий
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

# страница теста для студентов: рама сайта + прежний движок /test/quiz.js (слаг теста — в data-test)
TEST_MAIN = """<main id="top" class="pp">
  <section class="pp__hero"><div class="wrap tst">
    <a class="pp__back" id="tstBack" href="index.html#edu"></a>
    <p class="pp__kind">Test</p>
    <h1 class="pp__t">Sistemli ailə terapiyası</h1>
    <div id="test-app"><p class="t-who">Yüklənir…</p></div>
  </div></section>
  <section class="sec sec--soc"><div class="wrap"><div class="soc rv"><p class="soc__h" id="socH"></p><ul class="soc__l" id="socList"></ul></div></div></section>
</main>"""
h = re.sub(r"<main.*?</main>", lambda m: TEST_MAIN, src, flags=re.S)
h = h.replace('<body class="inner">', '<body class="inner" data-kind="test" data-test="sistemli-aile-terapiyasi">').replace("assets/js/page-program.js", "assets/js/page-test.js")
h = h.replace("</body>", '<script src="/test/quiz.js"></script>' + chr(10) + "</body>")
assert "page-test.js" in h and "/test/quiz.js" in h and 'data-test="sistemli-aile-terapiyasi"' in h
io.open(os.path.join(D, "test.html"), "w", encoding="utf-8", newline=chr(10)).write(h)
print("оболочка: test.html")

# индекс консультаций: названия для нижней навигации
for lang in ("ru", "az", "en"):
    items = []
    for s in CONS:
        fn = os.path.join(D, "data", "cons", "%s.%s.json" % (s, lang))
        if os.path.isfile(fn):
            items.append({"slug": s, "title": json.load(io.open(fn, encoding="utf-8"))["title"]})
    json.dump({"items": items}, io.open(os.path.join(D, "data", "cons", "index.%s.json" % lang), "w", encoding="utf-8"), ensure_ascii=False)
    print("индекс консультаций", lang, len(items))
