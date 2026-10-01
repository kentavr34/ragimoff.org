# -*- coding: utf-8 -*-
"""_tools/fix-book-chrome-i18n.py — язык служебных подписей в книгах (aria-label).

Замер 2026-09-30 (все книги: books/** + klinik-psixiatriya/**):
  * aria-label="Aç / bağla" (азербайджанский) стоял 3973 раза на русских,
    3973 на английских и 3973 на турецких страницах — подпись кнопки раскрытия
    подменю была чужого языка;
  * "Naviqasiya" (аз.) — 310 раз в ru/, 201 в en/, 136 в tr/;
  * "Fəsil keçidi / Переход между главами" (смесь языков) — 309 в ru/, 200 в en/,
    136 в tr/;
  * "Bağla / Закрыть" (аз.+рус. вперемешку) — 182 в ru/, 66 в en/;
  * "Futermenü" (аз.) — 183 в ru/, 67 в en/.

Скрипт приводит служебные подписи к языку страницы. Таблица ниже — единый
реестр: ключ → строка на язык; варианты написания любого языка сводятся к
ключу, поэтому идемпотентно.

Запуск:
    python _tools/fix-book-chrome-i18n.py --dry
    python _tools/fix-book-chrome-i18n.py
"""
from __future__ import annotations

import argparse
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ключ → {язык: строка}
LABELS = {
    "toggle": {  # кнопка раскрытия/закрытия подменю (▶)
        "az": "Aç / bağla", "ru": "Открыть / закрыть",
        "en": "Open / close", "tr": "Aç / kapat",
    },
    "crumb": {   # навигация-хлебные крошки
        "az": "Naviqasiya", "ru": "Навигация", "en": "Navigation", "tr": "Gezinti",
    },
    "pn": {      # переход между главами
        "az": "Fəsil keçidi", "ru": "Переход между главами",
        "en": "Chapter navigation", "tr": "Bölüm geçişi",
    },
    "close": {   # закрыть рейку/модал
        "az": "Bağla", "ru": "Закрыть", "en": "Close", "tr": "Kapat",
    },
    "footer": {  # меню подвала
        "az": "Futermenü", "ru": "Меню подвала", "en": "Footer menu", "tr": "Alt menü",
    },
    "langs": {   # группа языковых кнопок
        "az": "Dil", "ru": "Язык", "en": "Language", "tr": "Dil",
    },
    "contents": {  # оглавление (nav / бургер)
        "az": "Mündəricat", "ru": "Оглавление", "en": "Contents", "tr": "İçindekiler",
    },
    "search": {  # поиск по книгам
        "az": "Kitab axtarışı", "ru": "Поиск книг", "en": "Search books", "tr": "Kitap arama",
    },
}

VARIANT_TO_KEY = {}
for key, langs in LABELS.items():
    for lang, val in langs.items():
        VARIANT_TO_KEY[val] = key
# прочие написания, встречающиеся в книге
VARIANT_TO_KEY.update({
    "Открыть/закрыть": "toggle",
    "Fəsil keçidi / Переход между главами": "pn",
    "Bağla / Закрыть": "close",
    "Открыть / Закрыть": "toggle",
    "Open / Close": "toggle",
    "Содержание": "contents",
})


def lang_of(path):
    p = path.replace(os.sep, "/")
    parts = p.split("/")
    if "klinik-psixiatriya" in parts:
        i = parts.index("klinik-psixiatriya")
        rest = parts[i + 1:]
        return rest[0] if rest and rest[0] in ("ru", "en", "tr") else "az"
    for L in ("ru", "en", "tr"):
        if L in parts:
            return L
    return "az"


ARIA_RE = re.compile(r'(aria-label=")([^"]*)(")')


def fix_file(path, dry=False):
    lang = lang_of(path)
    s = open(path, encoding="utf-8", newline="").read()
    n = [0]

    def repl(m):
        key = VARIANT_TO_KEY.get(m.group(2))
        if not key:
            return m.group(0)
        target = LABELS[key][lang]
        if target == m.group(2):
            return m.group(0)
        n[0] += 1
        return m.group(1) + target + m.group(3)

    out = ARIA_RE.sub(repl, s)
    if n[0] and not dry:
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(out)
    return n[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    files = sorted(glob.glob(os.path.join(ROOT, "books", "**", "*.html"), recursive=True)) + \
            sorted(glob.glob(os.path.join(ROOT, "klinik-psixiatriya", "**", "*.html"), recursive=True))
    total, changed = 0, 0
    for f in files:
        if ".bak" in f:
            continue
        c = fix_file(f, dry=args.dry)
        if c:
            changed += 1
            total += c
    print("[%s] подписей исправлено: %d в %d файлах" % ("DRY" if args.dry else "OK", total, changed))


if __name__ == "__main__":
    main()
