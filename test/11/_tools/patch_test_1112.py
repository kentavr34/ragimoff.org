# -*- coding: utf-8 -*-
"""Страница теста для студентов в новой системе (12.11.2026): test.html — та же рама, темы и шрифты, что у всего сайта.
Движок теста — прежний /test/quiz.js (вопросы и проверка на сервере, результаты в админке) — не меняется;
прежняя страница /test/aile.html остаётся на месте. Повторный запуск ничего не меняет."""
import io, os, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(D)

p = "assets/css/site.css"
s = io.open(p, encoding="utf-8").read()
if "TST: страница теста" not in s:
    s += io.open("_agent/lab/tst.css", encoding="utf-8").read()
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
    print("стили TST добавлены")

js = "assets/js/page-test.js"
if not os.path.exists(js):
    io.open(js, "w", encoding="utf-8", newline="\n").write(
        "/* test/11 — страница теста: рама сайта (шапка, меню, темы, подвал). Сам тест ведёт прежний сценарий /test/quiz.js. */\n"
        "import { initChrome } from './chrome.js?v=11121014';\n"
        "const page = initChrome({ onRender(t, L) { const b = document.querySelector('#tstBack'); if (b) { b.textContent = '← ' + t.nav.edu; b.href = 'index.html#edu'; } const hc = document.querySelector('#headCta'); if (hc) hc.href = L.form || 'index.html#reg'; } });\n"
        "page.watch();\n")
    print("сценарий page-test.js создан")

p = "_tools/make_shells.py"
s = io.open(p, encoding="utf-8").read()
if "TEST_MAIN" not in s:
    a = "# индекс консультаций"
    assert s.count(a) == 1
    add = '''# страница теста для студентов: рама сайта + прежний движок /test/quiz.js (слаг теста — в data-test)
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

'''
    s = s.replace(a, add + a)
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
    print("make_shells: тест добавлен")

p = "assets/js/content.js"
s = io.open(p, encoding="utf-8").read()
if "L.tests = 'test.html'" not in s:
    assert s.count("L.tests = '/test/aile.html';") == 1 and s.count("'program.html?p=general#law', '/test/aile.html']") == 1
    s = s.replace("L.tests = '/test/aile.html';", "L.tests = 'test.html';").replace("'program.html?p=general#law', '/test/aile.html']", "'program.html?p=general#law', 'test.html']")
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
    print("ссылка «Тесты» ведёт на test.html")

p = "_tools/pages_check.py"
s = io.open(p, encoding="utf-8").read()
if '"test.html"' not in s:
    a = '    ps = ["index.html", "shop.html",'
    assert s.count(a) == 1
    s = s.replace(a, '    ps = ["index.html", "test.html", "shop.html",')
    s = s.replace('pg.startswith(("program", "index", "shop", "book")) and', 'pg.startswith(("program", "index", "shop", "book", "test")) and')
    s = s.replace('not pg.startswith(("shop", "book")):', 'not pg.startswith(("shop", "book", "test")):')
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
    print("pages_check: test.html добавлен")
