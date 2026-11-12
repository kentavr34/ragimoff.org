# -*- coding: utf-8 -*-
"""Переход 12.11.2026, стражи и простановка версии под корень сайта. Повторный запуск ничего не меняет.
 • страж структуры знает служебные файлы корня и временную страницу заказа книг в books/;
 • stamp.py пишет через временный файл с заменой (index.html бывает занят сервером предпросмотра)."""
import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(D)


def rep(s, a, b):
    assert s.count(a) == 1, "ожидалось 1, найдено %d: %s" % (s.count(a), a[:80])
    return s.replace(a, b)


def save(p, s):
    t = p + ".new"
    io.open(t, "w", encoding="utf-8", newline="\n").write(s)
    os.replace(t, p)


p = "_tools/structure_check.py"
s = io.open(p, encoding="utf-8").read()
if "ROOT_SERVICE" not in s:
    s = rep(s, '"README.md": "описание проекта", "FILE_MAP.md": "карта файлов (собирается этим стражем)", ".gitignore": "что не публикуется"}',
            '"README.md": "описание проекта", "FILE_MAP.md": "карта файлов (собирается этим стражем)", ".gitignore": "что не публикуется",\n'
            '              "404.html": "страница «не найдено»: переводит прежние адреса сайта на новые", "CLAUDE.md": "вводная для агента"}\n'
            '# служебные файлы корня: домен, значки, приложение, поисковики, переход с прежнего сайта\n'
            'ROOT_SERVICE = {"CNAME": "домен ragimoff.org", ".nojekyll": "публиковать как есть", "robots.txt": "правила для поисковиков", "sitemap.xml": "карта сайта (build_sitemap.py)",\n'
            '                "sw.js": "снимает сохранённые копии прежнего сайта с устройств", "favicon.ico": "значок", "app.webmanifest": "описание приложения", "site.webmanifest": "описание приложения",\n'
            '                "browserconfig.xml": "значки для Windows", "indexnow_key.txt": "ключ оповещения поисковиков", "_lang-switch.js": "нужен странице заказа книг (временно)"}\n'
            'ROOT_FILES.update(ROOT_SERVICE)\n'
            'ROOT_FILES.update(dict((n, "значок") for n in os.listdir(".") if n.startswith("apple-touch-icon") and n.endswith(".png")))')
    s = rep(s, '"vendor": "сторонние библиотеки", "sketch": "наброски"}',
            '"vendor": "сторонние библиотеки", "sketch": "наброски",\n'
            '             "payment": "страницы возврата после оплаты (адреса записаны на сервере оплаты)", "test": "действующий тест: aile.html и его движок quiz.js",\n'
            '             "app": "приложение для Android", "favicons": "значки", ".well-known": "подтверждение приложения", ".claude": "настройки агента", ".git": "история"}\n'
            '# в books/ временно остаётся прежняя страница заказа и корзина (до переноса заказа в новую систему) — это не книги\n'
            'BOOKS_ORDER = {"ru", "en", "covers"}')
    s = rep(s, 'books = sorted(d for d in os.listdir("books") if os.path.isdir(os.path.join("books", d))) if os.path.isdir("books") else []',
            'books = sorted(d for d in os.listdir("books") if os.path.isdir(os.path.join("books", d)) and d not in BOOKS_ORDER) if os.path.isdir("books") else []')
    save(p, s)
    print("страж структуры: корень сайта")

p = "_tools/stamp.py"
s = io.open(p, encoding="utf-8").read()
if "def _save" not in s:
    s = s.replace("import io, re, time\n", "import io, re, time, os as _os\n\n\ndef _save(p, t):\n    n = p + '.new'\n    io.open(n, 'w', encoding='utf-8', newline='\\n').write(t)\n    _os.replace(n, p)\n\n", 1)
    import re
    s = re.sub(r"io\.open\((\w+), 'w', encoding='utf-8', newline='\\n'\)\.write\((\w+)\)", r"_save(\1, \2)", s)
    s = s.replace("Запуск из test/11 перед публикацией", "Запуск из корня сайта перед публикацией")
    save(p, s)
    print("stamp.py: запись через замену")
