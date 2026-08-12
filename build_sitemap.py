#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_sitemap.py — карта сайта из того, что реально лежит на диске.
Кенан 2026-08-12.

Прежняя sitemap.xml была от 29 апреля: 159 адресов, из них в книгу вели три.
Книга — 645 страниц на четырёх языках — в карту не попадала вовсе.

Что делает: обходит все .html, отбрасывает служебное и перенаправления,
пишет карту с языковыми альтернативами (hreflang) — той же связкой, что
проставляет fix_seo_links.py. Приоритеты и частоту обновления ставит по
разделу: главная выше, карточки книги ниже, но все в индексе.

Идемпотентен: два прогона подряд дают одинаковый файл.

    python build_sitemap.py            # показать сводку
    python build_sitemap.py --apply
"""
from __future__ import annotations

import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / 'sitemap.xml'
BASE = 'https://ragimoff.org/'
SKIP_DIRS = {'.git', 'node_modules', 'graphify-out', '__pycache__', '.claude',
             '_supplements', 'backend', 'images', '_partials', 'partials'}
SKIP_FILES = {'template.html', 'wc.html', 'gp.html'}
BOOK = 'klinik-psixiatriya'


def priority(path: str) -> tuple[str, str]:
    """(приоритет, частота) по месту страницы в сайте."""
    if path == 'index.html':
        return '1.0', 'weekly'
    if path in ('ru/index.html', 'en/index.html'):
        return '0.9', 'weekly'
    if path == 'klinik-psixiatriya.html':
        return '0.9', 'weekly'
    if path.startswith(BOOK + '/'):
        name = path.split('/')[-1]
        if re.match(r'^\d\d-', name):
            return '0.7', 'monthly'          # страницы глав
        if re.match(r'^[0-9A-Z]{4}\.html$', name):
            return '0.6', 'monthly'          # карточки расстройств
        return '0.5', 'monthly'              # справочники, приложения
    if path.startswith('blog'):
        return '0.6', 'monthly'
    return '0.8', 'monthly'


def variants(path: str) -> dict[str, str]:
    out: dict[str, str] = {}
    if path.startswith(BOOK + '/'):
        tail = path[len(BOOK) + 1:]
        parts = tail.split('/')
        name = parts[-1] if parts[0] in ('ru', 'en', 'tr') else tail
        for lang in ('az', 'ru', 'en', 'tr'):
            cand = '{}/{}'.format(BOOK, name) if lang == 'az' else '{}/{}/{}'.format(BOOK, lang, name)
            if (ROOT / cand).is_file():
                out[lang] = cand
    else:
        parts = path.split('/')
        name = parts[-1] if parts[0] in ('ru', 'en') else path
        for lang in ('az', 'ru', 'en'):
            cand = name if lang == 'az' else '{}/{}'.format(lang, name)
            if (ROOT / cand).is_file():
                out[lang] = cand
    return out


def collect() -> list[str]:
    pages = []
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        rel = Path(dp).relative_to(ROOT)
        for f in sorted(fn):
            if not f.endswith('.html') or f in SKIP_FILES:
                continue
            path = (rel / f).as_posix()
            t = (Path(dp) / f).read_text(encoding='utf-8', errors='replace')
            head = t[:t.find('</head>')] if '</head>' in t else t[:4000]
            if re.search(r'http-equiv=["\']refresh["\']', head, re.I):
                continue                      # перенаправления в карту не идут
            if re.search(r'<meta[^>]+noindex', head, re.I):
                continue
            pages.append(path)
    return sorted(pages)


def url_of(path: str) -> str:
    return BASE if path == 'index.html' else BASE + path


def main(apply: bool = False) -> None:
    pages = collect()
    today = time.strftime('%Y-%m-%d')
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
             '        xmlns:xhtml="http://www.w3.org/1999/xhtml">',
             '',
             '  <!-- Собрано build_sitemap.py {} — по файлам на диске -->'.format(today),
             '']
    for path in pages:
        prio, freq = priority(path)
        lines.append('  <url>')
        lines.append('    <loc>{}</loc>'.format(url_of(path)))
        v = variants(path)
        if len(v) > 1:
            for lang in ('az', 'ru', 'en', 'tr'):
                if lang in v:
                    lines.append('    <xhtml:link rel="alternate" hreflang="{}" href="{}"/>'.format(
                        lang, url_of(v[lang])))
            if 'az' in v:
                lines.append('    <xhtml:link rel="alternate" hreflang="x-default" href="{}"/>'.format(
                    url_of(v['az'])))
        lines.append('    <lastmod>{}</lastmod>'.format(today))
        lines.append('    <changefreq>{}</changefreq>'.format(freq))
        lines.append('    <priority>{}</priority>'.format(prio))
        lines.append('  </url>')
    lines.append('')
    lines.append('</urlset>')
    xml = '\n'.join(lines) + '\n'

    book = len([p for p in pages if p.startswith(BOOK + '/')])
    print('страниц в карте: {} (книга {}, сайт {})'.format(len(pages), book, len(pages) - book))
    if apply:
        OUT.write_text(xml, encoding='utf-8')
        print('записано: {} ({:.0f} КБ)'.format(OUT, len(xml) / 1024))
    else:
        print('пробный прогон — запустить с --apply')


if __name__ == '__main__':
    main('--apply' in sys.argv)
