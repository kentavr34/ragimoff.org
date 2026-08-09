#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_sidebar.py — одно и то же боковое меню на всех страницах книги.

ЧТО БЫЛО НЕ ТАК (2026-08-09)
============================
В книге сосуществовали две генерации бокового меню:

  107 страниц на язык — полное меню: 60 ссылок, у глав раскрыты
      подпункты с расстройствами;
   27 страниц на язык — короткое: 29 ссылок, без подпунктов, плюс
      заголовок «📋 Mündəricat» в шапке меню;
    3 страницы — 28 ссылок.

В короткую группу попали главная и «Müqəddimə» — те самые страницы,
на которых Кенан и заметил, что меню выглядит иначе. Причина: их
переписывает `_rebuild_book_nav.py`, а он собирает подпункты, читая
страницы глав `01-…`—`23-…`; после разбиения книги на карточки эти
страницы стали редиректами, читать в них нечего — меню и вышло куцым.

Отдельно: `const CURRENT` на 532 страницах равнялся `'bolme-02'` —
копия, оставшаяся от одной страницы. Скрипт подсветки активного пункта
сравнивает `data-slug` ссылки с `CURRENT`, поэтому активный пункт не
подсвечивался НИ НА ОДНОЙ странице. В полном меню вдобавок не было
самого атрибута `data-slug`.

ЧТО ДЕЛАЕТ
==========
Берёт полное меню (самый распространённый вариант в каждом языке),
проставляет каждой ссылке `data-slug` по её href и раскладывает по всем
страницам книги этого языка. Каждой странице выставляет свой `CURRENT`.

    python fix_sidebar.py            # отчёт
    python fix_sidebar.py --apply
"""
from __future__ import annotations
import re, sys, io, hashlib
from pathlib import Path
from collections import Counter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).parent
BOOK = ROOT / 'klinik-psixiatriya'
LANGS = {'az': BOOK, 'ru': BOOK / 'ru', 'en': BOOK / 'en', 'tr': BOOK / 'tr'}
APPLY = '--apply' in sys.argv

ASIDE = re.compile(r'<aside class="sidebar"[\s\S]*?</aside>')
LINK = re.compile(r'<a href="([^"#?]+)\.html"([^>]*)class="(nav-link[^"]*|nav-sub-link)"([^>]*)>')
CURRENT = re.compile(r'''(const CURRENT\s*=\s*)["'][^"']*["']''')


def canonical(folder: Path) -> str | None:
    """Самый распространённый вариант полного меню в языке."""
    seen: Counter[str] = Counter()
    store: dict[str, str] = {}
    for fp in sorted(folder.glob('*.html')):
        m = ASIDE.search(fp.read_text(encoding='utf-8', errors='ignore'))
        if not m or len(re.findall(r'class="nav-link', m.group(0))) < 60:
            continue
        key = hashlib.md5(re.sub(r'\s+', ' ', m.group(0)).encode()).hexdigest()
        seen[key] += 1
        store.setdefault(key, m.group(0))
    if not seen:
        return None
    return store[seen.most_common(1)[0][0]]


def with_slugs(aside: str) -> tuple[str, int]:
    """Вернуть data-slug каждой ссылке — по нему скрипт метит активный пункт."""
    n = 0

    def rep(m: re.Match) -> str:
        nonlocal n
        href, a, cls, b = m.groups()
        if 'data-slug' in a + b:
            return m.group(0)
        n += 1
        return f'<a href="{href}.html"{a}class="{cls}" data-slug="{href}"{b}>'

    return LINK.sub(rep, aside), n


def main() -> int:
    total = {'aside': 0, 'slug': 0, 'current': 0}
    for lg, folder in LANGS.items():
        base = canonical(folder)
        if not base:
            print(f'  {lg}: полное меню не найдено')
            continue
        base, slugs = with_slugs(base)
        links = len(re.findall(r'class="nav-link', base))
        touched = 0
        for fp in sorted(folder.glob('*.html')):
            raw = fp.read_bytes().decode('utf-8')
            crlf = raw.count('\r\n') > raw.count('\n') // 2
            t = raw.replace('\r\n', '\n')
            m = ASIDE.search(t)
            if not m:
                continue
            new = t[:m.start()] + base + t[m.end():]
            new, c = CURRENT.subn(lambda x, s=fp.stem: x.group(1) + f'"{s}"', new)
            if new == t:
                continue
            touched += 1
            total['current'] += c
            if APPLY:
                fp.write_bytes((new.replace('\n', '\r\n') if crlf else new).encode('utf-8'))
        total['aside'] += touched
        total['slug'] += slugs
        print(f'  {lg}: меню {links} ссылок, data-slug добавлен {slugs} ссылкам, '
              f'страниц выровнено {touched}')
    print(f'итого страниц {total["aside"]}, CURRENT выставлен {total["current"]} раз')
    print('применено' if APPLY else 'пробный прогон — запустить с --apply')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
