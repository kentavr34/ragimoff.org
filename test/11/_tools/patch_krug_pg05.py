# -*- coding: utf-8 -*-
"""Пятый круг критика (12.11.2026): система книг в едином стандарте. Повторный запуск ничего не меняет.
 • Паспорт книги (books/<книга>/book.json) — один источник адреса, названия и обложки для каталога, страницы книги и читалки.
 • Обложки лежат внутри новой версии (assets/img/books/covers), а не берутся со старого сайта.
 • Каталог: адрес книги = имя её папки в библиотеке; название — из паспорта."""
import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(D)


def rep(s, a, b, n=1):
    assert s.count(a) == n, "ожидалось %d, найдено %d: %s" % (n, s.count(a), a[:70])
    return s.replace(a, b)


def patch(p, pairs, mark):
    s = io.open(p, encoding="utf-8").read()
    if mark in s:
        return
    for a, b in pairs:
        s = rep(s, a, b)
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
    print("изменён", p)


# сборщики: паспорт проходит через libcommon.finish
patch("_tools/build_library.py", [
    ("from bs4 import BeautifulSoup", "from bs4 import BeautifulSoup\nsys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\nimport libcommon"),
    ('    wrote += write(os.path.join(OUT, bdir, "book.json"), json.dumps(passport,', '    libcommon.finish(passport)\n    wrote += write(os.path.join(OUT, bdir, "book.json"), json.dumps(passport,'),
    ('"langs": passport["langs"], "cover": passport["cover"],', '"langs": passport["langs"], "cover": passport["cover"], "coverKey": passport.get("coverKey", ""),')], "libcommon")
patch("_tools/build_library_legacy.py", [
    ("from bs4 import BeautifulSoup", "from bs4 import BeautifulSoup\nsys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\nimport libcommon"),
    ('    wrote += write(os.path.join(OUT, b, "book.json"), json.dumps(P,', '    libcommon.finish(P)\n    wrote += write(os.path.join(OUT, b, "book.json"), json.dumps(P,')], "libcommon")
patch("_tools/build_klinik.py", [
    ("from bs4 import BeautifulSoup", "from bs4 import BeautifulSoup\nsys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\nimport libcommon"),
    ('    wrote += write(os.path.join(OUT, "book.json"), json.dumps(P,', '    libcommon.finish(P)\n    wrote += write(os.path.join(OUT, "book.json"), json.dumps(P,')], "libcommon")

# каталог: адрес и название из библиотеки, обложка внутри новой версии
patch("_tools/build_shop.py", [
    ("from bs4 import BeautifulSoup", "from bs4 import BeautifulSoup\nsys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\nimport libcommon"),
    ('FACTS_FOR = {0: "klinik", 2: "phoenix", 3: "guilt", 4: "pandemic"}', 'FACTS_FOR = {0: "klinik-psixiatriya", 2: "phoenix-era", 3: "virus-viny", 4: "shizofreniya"}'),
    ('    if base in ("klinik", "guilt", "pandemic", "phoenix"):\n        return base', '    if base in libcommon.OWN_BY_KEY:\n        return libcommon.OWN_BY_KEY[base]                       # адрес книги = имя её папки в библиотеке'),
    ('LIB_ID = {"klinik": "klinik-psixiatriya", "guilt": "virus-viny", "pandemic": "shizofreniya", "phoenix": "phoenix-era"}', 'LIB_ID = {}'),
    ('        if lib in LIB:\n', '''        if it["id"] in libcommon.OWN:
            it["cov"] = libcommon.OWN[it["id"]]                  # готовая обложка: assets/img/books/covers/<cov>-<язык>.jpg
            it["img"] = ""
        else:
            it["img"] = libcommon.local_cover(it["img"])
        pj = os.path.join(D, "books", lib, "book.json")
        if os.path.isfile(pj):                                  # название книги — из её паспорта (один источник)
            PT = json.load(io.open(pj, encoding="utf-8"))["t"]
            it["t"] = PT.get(lang) or it["t"]
        if lib in LIB:
''')], "libcommon")

patch("assets/js/page-shop.js", [
    ("const OWN = ['klinik', 'guilt', 'pandemic', 'phoenix'];                 /* у этих книг готовая обложка с названием на трёх языках */\n", "import { fixImg } from './blocks.js?v=11121254';\n"),
    ("const cover = (it, lang, big) => OWN.includes(it.id)\n  ? `<img src=\"assets/img/books/covers/${it.id}-${lang}.jpg\"", "const cover = (it, lang, big) => it.cov\n  ? `<img src=\"assets/img/books/covers/${it.cov}-${lang}.jpg\""),
    ("background-image:url('${esc(it.img)}')", "background-image:url('${esc(fixImg(it.img))}')"),
    ("class=\"shp__obj${OWN.includes(it.id) ? '' : ' shp__obj--tex'}\"", "class=\"shp__obj${it.cov ? '' : ' shp__obj--tex'}\"")], "it.cov")

patch("_tools/pages_check.py", [('"book.html?b=klinik",', '"book.html?b=klinik-psixiatriya",')], "book.html?b=klinik-psixiatriya")
