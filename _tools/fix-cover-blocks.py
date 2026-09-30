# -*- coding: utf-8 -*-
"""
_tools/fix-cover-blocks.py — титулы: два дефекта из списка владельца.

1. «Обращение на главной сместилось в конец»: блок `.bk-read--rest` с обращением
   автора (`.author-note`) и карточками-переходами должен идти ДО оглавления —
   в прежней разметке порядок был «титул → обращение → карточки → оглавление».
2. «Автор отображается двумя строками»: у книг без года в титуле подпись
   `.bk-tp__sub` дословно повторяла автора и он выходил дважды. Убираем дубль.

Запуск:
    python _tools/fix-cover-blocks.py --dry
    python _tools/fix-cover-blocks.py
"""
import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOKS = [
    "books/freud-yuxularin-yozumu", "books/freud-musa", "books/freud-psixoanalizle-tanishliq",
    "books/freud-seksualligin-psixologiyasi", "books/freud-sevgi-mektublari",
    "books/freud-aforizmlar", "books/freud-medeniyyetin-sancilari", "books/freud-totem-ve-tabu",
    "books/virus-viny", "books/shizofreniya", "books/phoenix-era", "klinik-psixiatriya",
]
SKIP_DIRS = ("test", ".bak")
SUB = re.compile(r'<p class="bk-tp__sub">(?P<name>[^<]*)</p>\s*')


def fix(raw):
    what = []
    # 1. дубль подписи и автора
    m = re.search(r'<span class="bk-tp__author">(?P<a>[^<]*)</span>', raw)
    s = SUB.search(raw)
    if m and s and s.group("name").strip() and s.group("name").strip() == m.group("a").strip():
        raw = raw[:s.start()] + raw[s.end():]
        what.append("снят дубль подписи")
    # 2. обращение автора — до оглавления
    r = re.search(r'\s*<div class="bk-read bk-read--rest">(?P<body>.*?)</div>\s*'
                  r'(?=<nav class="bk-pn"|<footer class="bk-ft")', raw, re.S)
    if r and 'class="author-note"' in r.group("body"):
        t = raw.find('<section class="bk-toc"')
        if t > 0:
            blk = '<div class="bk-read bk-read--rest">%s</div>\n' % r.group("body")
            raw = raw[:r.start()] + "\n" + raw[r.end():] + "\n"
            t = raw.find('<section class="bk-toc"')
            raw = raw[:t] + blk + "\n      " + raw[t:]
            what.append("обращение перенесено перед оглавлением")
    return raw, what


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    n = 0
    for book in BOOKS:
        for dp, dn, fn in os.walk(os.path.join(ROOT, book)):
            dn[:] = [d for d in dn if not any(x in d for x in SKIP_DIRS)]
            for f in sorted(fn):
                if f != "index.html":
                    continue
                fp = os.path.join(dp, f)
                with open(fp, encoding="utf-8", newline="") as fh:
                    raw = fh.read()
                if 'class="bk bk-cover"' not in raw[:6000]:
                    continue
                out, what = fix(raw)
                if not what:
                    continue
                n += 1
                if not a.dry:
                    with open(fp, "w", encoding="utf-8", newline="") as fh:
                        fh.write(out)
                print("  %-56s %s" % (os.path.relpath(fp, ROOT).replace(os.sep, "/"), ", ".join(what)))
    print("титулов поправлено: %d%s" % (n, "  (dry-run)" if a.dry else ""))


if __name__ == "__main__":
    main()
