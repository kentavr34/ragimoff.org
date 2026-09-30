# -*- coding: utf-8 -*-
"""
_tools/build-aforizmlar.py — «Aforizmlər»: 178 высказываний → 12 тематических рубрик.

Владелец: «в оглавлении всего 1 пункт — разделить афоризмы на группы по темам
и сделать нормальное оглавление — 10–12 рубрик». Годов и подписей в источнике
нет, поэтому рубрики тематические (см. _tools/configs/freud-aforizmlar-themes.json).

Что делает:
  · берёт 178 высказываний ИЗ GIT как есть (`<p class="afo-item">…</p>`) — текст не
    переписывается и не перенабирается, меняется только группировка;
  · собирает 12 страниц-рубрик по каркасу концепта (шапка, рейка, заголовок,
    высказывания, пред/след), нумерация 01…12 как у глав;
  · обновляет титул (index.html): оглавление из 12 строк + рейка;
  · старый единственный файл 01-aforizmlar.html становится редиректом на титул
    (страница-дубль не нужна, но старые ссылки/закладки продолжают работать).

Запуск:
    python _tools/build-aforizmlar.py --dry
    python _tools/build-aforizmlar.py                  # исходник берётся из HEAD
    python _tools/build-aforizmlar.py --base f4f7374    # или из конкретного коммита
"""
import argparse
import html
import io
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = "books/freud-aforizmlar"
SITE = "https://ragimoff.org/" + BOOK + "/"
CONF = os.path.join(ROOT, "_tools", "configs", "freud-aforizmlar-themes.json")
BOOK_TITLE = "Aforizmlər"
BOOK_AUTHOR = "Ziqmund Freyd"
TOTAL = 178

FONTS = ('<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;'
         '0,400;0,500;1,400&family=IBM+Plex+Mono:wght@400;500&family=Literata:ital,opsz,wght;'
         '0,7..72,300..700;1,7..72,300..700&family=Montserrat:wght@300;400;500&display=swap" rel="stylesheet">')
KEYWORDS = ("psixoterapevt, psixoloq, psixiatr, həkim, Kənan Rəhimov, Bakı, psixologiya, "
            "psixoterapiya, depressiya, həyəcan, fobiya, OKP, PTSD")


def git_show(rel, base):
    r = subprocess.run(["git", "show", "%s:%s" % (base, rel)], cwd=ROOT,
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.stdout if r.returncode == 0 else None


def ui_rows(themes, current=None):
    """Строки рейки: безномерной титул + 12 рубрик."""
    out = ['        <a class="bk-row bk-row--front%s" href="index.html">'
           '<span class="bk-row__n"></span><span class="bk-row__t">Ana səhifə</span></a>' %
           (" is-on" if current == "index" else ""),
           '        <div class="bk-sb__sep" role="presentation"></div>']
    for i, t in enumerate(themes, 1):
        cls = "bk-row is-on" if current == t["slug"] else "bk-row"
        out.append('        <a class="%s" href="%02d-%s.html"><span class="bk-row__n">%02d</span>'
                   '<span class="bk-row__t">%s</span></a>'
                   % (cls, i, t["slug"], i, html.escape(t["title"])))
    return "\n".join(out)


def head_html(page_title, desc, url, rubric_note="", jsonld_name=None):
    return """<!doctype html>
<html lang="az" data-langs="az" data-lang-url-az="%(url)s" data-lang-avail="az">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="theme-color" content="#07090E">
<meta name="description" content="%(desc)s">
<meta name="keywords" content="%(kw)s">
<meta name="robots" content="index, follow">
<title>%(title)s</title>
<link rel="canonical" href="%(url)s">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:type" content="website">
<meta property="og:url" content="%(url)s">
<meta property="og:locale" content="az_AZ">
<script type="application/ld+json">{"@context":"https://schema.org","@type":"Book",
"name":"%(book)s","inLanguage":"az",
"author":{"@type":"Person","name":"%(author)s"},
"about":"%(about)s",
"url":"%(url)s",
"keywords":"Freyd, psixoanaliz, aforizmlər, psixologiya%(rubric)s"}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
%(fonts)s
<link rel="stylesheet" href="/books/book.css?v=9">
<link rel="stylesheet" href="/books/book-content.css?v=2">
</head>
""" % {"title": html.escape(page_title), "desc": html.escape(desc), "url": url,
       "kw": KEYWORDS, "book": BOOK_TITLE, "author": BOOK_AUTHOR,
       "about": jsonld_name or desc, "rubric": rubric_note, "fonts": FONTS}


def pn_html(prev, nxt, themes):
    """Блок пред/след: как у остальных глав книги (см. rebuild-concept.py)."""
    def block(item, side):
        direction = "Əvvəlki" if side == "prev" else "Növbəti"
        if item:
            return ('          <a class="bk-pn__a" href="%s">\n'
                    '            <span class="bk-pn__dir">%s</span>\n'
                    '            <span class="bk-pn__t">%s</span>\n'
                    '          </a>' % (item["href"], direction, html.escape(item["title"])))
        return ('          <span class="bk-pn__a" aria-disabled="true">\n'
                '            <span class="bk-pn__dir">%s</span>\n'
                '            <span class="bk-pn__t">—</span>\n'
                '          </span>' % direction)
    return """      <nav class="bk-pn" aria-label="Fəsil keçidi / Переход между главами">
        <p class="bk-pn__up"><a href="index.html">Kitabın mündəricatı</a></p>
        <div class="bk-pn__grid">
%s
%s
        </div>
      </nav>
""" % (block(prev, "prev"), block(nxt, "next"))


def crumb():
    return """      <nav class="bk-crumb" aria-label="Naviqasiya">
        <a href="index.html">%(book)s</a>
        <span class="bk-crumb__sep" aria-hidden="true">/</span>
      </nav>
""" % {"book": BOOK_TITLE}


def chead(num, title):
    return """      <header class="bk-chead">
        <p class="bk-chead__top">
          <span class="bk-chead__n">%02d</span>
          <span class="bk-chead__rule" role="presentation"></span>
        </p>
        <h1 class="bk-chead__h1">%s</h1>
      </header>
""" % (num, html.escape(title))


def redirect_html(target, title):
    return """<!DOCTYPE html>
<html lang="az"><head>
<meta charset="UTF-8">
<meta http-equiv="refresh" content="0;url=%(t)s">
<link rel="canonical" href="%(t)s">
<meta name="robots" content="noindex, follow">
<title>Aforizmlər — mündəricat</title>
<style>abbr[title]{ text-decoration: underline dotted; text-underline-offset: 2px; cursor: help; }</style>
</head><body>
<p>Bu səhifə köçürülüb. <a href="%(t)s">%(n)s</a></p>
<script>window.location.replace("%(t)s");</script>
</body></html>
""" % {"t": target, "n": title}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--base", default="HEAD", help="коммит, из которого берём 178 высказываний")
    a = ap.parse_args()

    conf = json.load(io.open(CONF, encoding="utf-8"))
    themes = conf["themes"]

    src = git_show("%s/%s" % (BOOK, conf["source"]), a.base)
    if not src:
        print("!! не читается %s из %s" % (conf["source"], a.base))
        return 1
    raw_items = re.findall(r'<p class="afo-item">(.*?)</p>', src, re.S)
    if len(raw_items) != TOTAL:
        print("!! высказываний в источнике %d, ожидалось %d — укажите --base с полной версией"
              % (len(raw_items), TOTAL))
        return 1
    # контроль: каждая позиция ровно в одной рубрике
    seen = [i for t in themes for i in t["items"]]
    assert sorted(seen) == list(range(1, TOTAL + 1)), "рубрики не покрывают 1..178"

    # каркас берём из собранной страницы: шапка/рейка/подвал/модал/скрипты
    body_at = src.find('<body')
    nav_at = src.find('<nav class="bk-sb__nav" aria-label="Mündəricat">')
    nav_end = src.find("</nav>", nav_at) + len("</nav>")
    hdr = src[body_at:nav_at]                     # <body> + шапка + начало рейки
    tail = src[src.find('      <footer class="bk-ft">'):]

    written = []
    for i, t in enumerate(themes, 1):
        num = "%02d-%s" % (i, t["slug"])
        fname = num + ".html"
        prev = {"href": "%02d-%s.html" % (i - 1, themes[i - 2]["slug"]), "title": themes[i - 2]["title"]} if i > 1 else None
        nxt = {"href": "%02d-%s.html" % (i + 1, themes[i]["slug"]), "title": themes[i]["title"]} if i < len(themes) else None
        body = "\n\n".join('<p class="afo-item">%s</p>' % raw_items[k - 1] for k in t["items"])
        page = (head_html("%s | %s" % (t["title"], BOOK_TITLE.upper()),
                          "%s — Ziqmund Freydin aforizmləri və əsərlərindən çıxarışlar." % t["title"],
                          SITE + fname, " · " + t["title"], jsonld_name=t["title"])
                + hdr
                + ("<nav class=\"bk-sb__nav\" aria-label=\"Mündəricat\">\n%s\n      </nav>\n" % ui_rows(themes, t["slug"]))
                + "    </aside>\n  <main class=\"bk-main\">\n    <div class=\"bk-col\">\n"
                + crumb() + chead(i, t["title"])
                + '      <div class="bk-read">\n%s\n      </div>\n' % body
                + pn_html(prev, nxt, themes)
                + tail)
        path = os.path.join(ROOT, BOOK, fname)
        if not a.dry:
            with io.open(path, "w", encoding="utf-8", newline="\r\n") as fh:
                fh.write(page)
        written.append(fname)
        print("  %-46s высказываний: %2d" % (fname, len(t["items"])))

    # титул: новая рейка и оглавление из 12 строк
    cover_path = os.path.join(ROOT, BOOK, "index.html")
    cover = io.open(cover_path, encoding="utf-8").read()          # строки → \n
    cover = re.sub(r'(<nav class="bk-sb__nav" aria-label="Mündəricat">\r?\n).*?(\r?\n      </nav>)',
                   lambda m: m.group(1) + ui_rows(themes, "index") + m.group(2), cover, flags=re.S)
    rows = []
    for i, t in enumerate(themes, 1):
        rows.append('          <li class="bk-toc__row"><a class="bk-toc__a" href="%02d-%s.html">'
                    '<span class="bk-toc__n">%02d</span><span class="bk-toc__t">%s</span></a></li>'
                    % (i, t["slug"], i, html.escape(t["title"])))
    cover = re.sub(r'(<ol class="bk-toc__list">\r?\n).*?(\r?\n        </ol>)',
                   lambda m: m.group(1) + "\n".join(rows) + m.group(2), cover, flags=re.S)
    cover = cover.replace('<span class="bk-label">1 fəsil</span>',
                          '<span class="bk-label">%d fəsil</span>' % len(themes), 1)
    if not a.dry:
        with io.open(cover_path, "w", encoding="utf-8", newline="\r\n") as fh:
            fh.write(cover)
    print("  index.html — оглавление: %d строк" % len(themes))

    # старая единственная страница — редирект на титул
    red_path = os.path.join(ROOT, BOOK, "01-aforizmlar.html")
    if not a.dry:
        with io.open(red_path, "w", encoding="utf-8", newline="\r\n") as fh:
            fh.write(redirect_html("index.html", "Kitabın mündəricatı"))
    print("  01-aforizmlar.html → redirect на index.html")
    print("итого страниц-рубрик: %d%s" % (len(themes), "  (dry-run)" if a.dry else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
