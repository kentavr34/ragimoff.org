# -*- coding: utf-8 -*-
"""
_tools/fix-toc-groups.py — строки оглавления БЕЗ целевой страницы → заголовки групп.

В оглавлении книг есть структурные элементы (части и разделы), у которых нет
отдельной страницы. Пересборщик рисовал их как обычные строки со ссылкой-обёрткой
<span class="bk-toc__a" aria-disabled="true">: href нет, но строка выглядит и
ведёт себя как ссылка (наведение подсвечивает) — владелец читает это как
«ссылка не кликается».

Теперь такие строки — заголовки групп: <span class="bk-toc__g">, тише по цвету и
кеглю, без подсветки и без курсора-указателя.

Запуск:
    python _tools/fix-toc-groups.py --dry
    python _tools/fix-toc-groups.py
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

ROW = re.compile(
    r'<li class="bk-toc__row bk-toc__row--front">\s*'
    r'<span class="bk-toc__a" aria-disabled="true">\s*'
    r'<span class="bk-toc__n">\s*</span>\s*'
    r'<span class="bk-toc__t">(?P<name>.*?)</span>\s*'
    r'</span>\s*</li>', re.S)


def fix_list(text):
    """Возвращает (новый текст, число переделанных строк-групп)."""
    n = 0

    def rep(m):
        nonlocal n
        n += 1
        return ('<li class="bk-toc__row bk-toc__row--group">'
                '<span class="bk-toc__g">%s</span></li>' % m.group("name"))

    return ROW.sub(rep, text), n


def pages():
    for book in BOOKS:
        base = os.path.join(ROOT, book)
        for dp, dn, fn in os.walk(base):
            dn[:] = [d for d in dn if not any(s in d for s in SKIP_DIRS)]
            for f in sorted(fn):
                if f.endswith(".html"):
                    yield os.path.join(dp, f)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    files = groups = 0
    for fp in pages():
        with open(fp, encoding="utf-8", newline="") as fh:
            raw = fh.read()
        out, n = fix_list(raw)
        if not n:
            continue
        files += 1
        groups += n
        if not a.dry:
            with open(fp, "w", encoding="utf-8", newline="") as fh:
                fh.write(out)
        print("  %-60s групп: %d" % (os.path.relpath(fp, ROOT).replace(os.sep, "/"), n))
    print("файлов: %d | строк-групп оформлено: %d%s"
          % (files, groups, "  (dry-run)" if a.dry else ""))


if __name__ == "__main__":
    main()
