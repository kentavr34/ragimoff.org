# -*- coding: utf-8 -*-
"""
_tools/fix-stray-main.py — убрать ЛИШНИЙ </main> из собранных страниц книг.

Зачем: в старой разметке тело главы заканчивалось закрывающим </main>. После
пересборки по каркасу концепта оболочка даёт свой </main> ровно один, а чужой
закрывает .bk-main раньше времени: .bk-col и колонка чтения кончаются на тексте,
и пред/след + футер уезжают во всю ширину ПОД сайдбар. В демо
(design_concept/book-chapter.html) футер стоит В КОЛОНКЕ чтения.

Правило простое: настоящий </main> в пересобранной странице один — последний.
Всё, что до него, — остаток старой разметки; такие теги убираем вместе с их
строкой. Файлы с одним </main> не трогаем (идемпотентно).

Запуск:
    python _tools/fix-stray-main.py --dry     # только отчёт
    python _tools/fix-stray-main.py           # починить
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
SKIP_DIRS = ("test", ".bak")          # books/phoenix-era/test — тест владельца, не трогаем


def strip_stray_main(raw):
    """Все </main>, кроме последнего, — вместе с их строкой. Возвращает (текст, сколько)."""
    n = raw.count("</main>")
    if n < 2:
        return raw, 0
    i = raw.rfind("</main>")
    return re.sub(r"[ \t]*</main>[ \t]*\r?\n", "", raw[:i]) + raw[i:], n - 1


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
    ap.add_argument("--dry", action="store_true", help="только отчёт")
    a = ap.parse_args()

    fixed, tags, clean = 0, 0, 0
    for fp in pages():
        with open(fp, encoding="utf-8", newline="") as fh:
            raw = fh.read()
        out, k = strip_stray_main(raw)
        if not k:
            clean += 1
            continue
        fixed += 1
        tags += k
        if not a.dry:
            with open(fp, "w", encoding="utf-8", newline="") as fh:
                fh.write(out)
        print("  %-72s −%d" % (os.path.relpath(fp, ROOT).replace("\\", "/"), k))
    print("страниц починено: %d | убрано </main>: %d | уже в порядке: %d%s"
          % (fixed, tags, clean, "  (dry-run: файлы не изменены)" if a.dry else ""))


if __name__ == "__main__":
    main()
