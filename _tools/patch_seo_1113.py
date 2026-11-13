# -*- coding: utf-8 -*-
"""Правка сценариев под постоянные языковые адреса (13.11.2026). Повторный запуск ничего не меняет."""
import io, os, re, sys, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(D)
n = 0


def patch(p, pairs):
    global n
    s = io.open(p, encoding="utf-8").read()
    o = s
    for a, b in pairs:
        if b in s:
            continue
        assert s.count(a) == 1, (p, a[:70], s.count(a))
        s = s.replace(a, b)
    if s != o:
        io.open(p + ".new", "w", encoding="utf-8", newline="\n").write(s)
        os.replace(p + ".new", p)
        n += 1
        print("исправлен", p)


SEO = "import { initSeo, switchLang } from './seo.js?v=11131300';\n"
# chrome.js: язык по умолчанию — AZ; смена языка на снимке ведёт на снимок; ссылки — на снимки
patch("assets/js/chrome.js", [
    ("import { PROGRAMS } from './programs.js?v=11130541';\n", "import { PROGRAMS } from './programs.js?v=11130541';\n" + SEO),
    ("  let lang = T[document.documentElement.lang] ? document.documentElement.lang : 'ru';",
     "  let lang = T[document.documentElement.lang] ? document.documentElement.lang : 'az';"),
    ("    const lg = e.target.closest('[data-lang-btn]'); if (lg) { lang = lg.dataset.langBtn; store.set('r11_lang', lang); render(); return; }",
     "    const lg = e.target.closest('[data-lang-btn]'); if (lg) { if (switchLang(lg.dataset.langBtn)) return; lang = lg.dataset.langBtn; store.set('r11_lang', lang); render(); return; }"),
    ("  return { render, watch, get lang() { return lang; } };",
     "  initSeo(() => lang);\n  return { render, watch, get lang() { return lang; } };"),
])
# site.js (главная)
patch("assets/js/site.js", [
    ("import { initLight } from './light.js?v=11130541';\n", "import { initLight } from './light.js?v=11130541';\n" + SEO),
    ("let lang = T[document.documentElement.lang] ? document.documentElement.lang : 'ru';",
     "let lang = T[document.documentElement.lang] ? document.documentElement.lang : 'az';"),
    ("  const lg = e.target.closest('[data-lang-btn]'); if (lg) { lang = lg.dataset.langBtn; store.set('r11_lang', lang); render(); return; }",
     "  const lg = e.target.closest('[data-lang-btn]'); if (lg) { if (switchLang(lg.dataset.langBtn)) return; lang = lg.dataset.langBtn; store.set('r11_lang', lang); render(); return; }"),
    ("render(); cineLoad();", "render(); cineLoad(); initSeo(() => lang);"),
])
# адрес страницы: на снимке параметры лежат в window.__Q (адрес снимка без «?»)
Q = "(location.search || window.__Q || '')"
patch("assets/js/page-program.js", [("new URLSearchParams(location.search).get('p')", "new URLSearchParams(%s).get('p')" % Q)])
patch("assets/js/page-shop.js", [("const bid = new URLSearchParams(location.search).get('b') || '';", "const bid = new URLSearchParams(%s).get('b') || '';" % Q)])
patch("assets/js/page.js", [("const q = new URLSearchParams(location.search);", "const q = new URLSearchParams(%s);" % Q)])
patch("assets/js/reader.js", [("q = new URLSearchParams(location.search), bid", "q = new URLSearchParams(%s), bid" % Q)])

# загрузчик в каждой странице: язык снимка (window.__LANG) → сохранённый выбор → язык браузера (ru/en, иначе az)
BOOT_OLD = "document.documentElement.lang = l || 'ru';"
BOOT_NEW = ("var b = (navigator.language || '').slice(0, 2).toLowerCase();\n"
            "  document.documentElement.lang = window.__LANG || l || (b === 'ru' || b === 'en' ? b : 'az');   /* 13.11: по умолчанию AZ, иначе язык браузера */")
for p in sorted(glob.glob("*.html")):
    s = io.open(p, encoding="utf-8").read()
    if BOOT_OLD in s:
        patch(p, [(BOOT_OLD, BOOT_NEW), ('<html lang="ru"', '<html lang="az"')])
print("изменено файлов:", n)
