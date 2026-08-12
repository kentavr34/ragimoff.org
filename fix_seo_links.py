#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fix_seo_links.py — canonical и hreflang по всему сайту. Кенан 2026-08-12.

Зачем. Аудит 12 августа нашёл три вещи:
  • 131 страница азербайджанского дерева книги имела canonical на ОДНУ чужую
    страницу — `02-6A2-sizofreniya-spektri.html`. Для поиска это значит:
    «вся азербайджанская книга — дубликат главы про шизофрению»;
  • 107 страниц веток ru/ и en/ корневого сайта не имели canonical вовсе;
  • все 644 страницы книги не имели hreflang, то есть четыре языковых дерева
    для поиска были четырьмя不 связанными сайтами.

Что делает:
  • canonical — всегда на саму страницу (абсолютный адрес);
  • hreflang — на те языки, где файл РЕАЛЬНО существует, плюс x-default на аз.;
  • страницы-перенаправления (meta refresh) не трогает: у них canonical
    законно ведёт на цель;
  • `index.html` в корне — эталон дизайна, по правилу проекта не трогаем;
  • служебные `template.html`, `wc.html` пропускает.

Идемпотентен: повторный прогон даёт ноль изменений.

    python fix_seo_links.py            # показать
    python fix_seo_links.py --apply
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
BASE = 'https://ragimoff.org/'
SKIP_DIRS = {'.git', 'node_modules', 'graphify-out', '__pycache__', '.claude',
             '_supplements', 'backend', 'images', 'partials'}
SKIP_FILES = {'index.html', 'template.html', 'wc.html'}   # index.html — эталон

BOOK = 'klinik-psixiatriya'
SITE_LANGS = ['az', 'ru', 'en']
BOOK_LANGS = ['az', 'ru', 'en', 'tr']


def variants(path: str) -> dict[str, str]:
    """Пути этой же страницы на других языках — только существующие файлы."""
    out: dict[str, str] = {}
    if path.startswith(BOOK + '/'):
        tail = path[len(BOOK) + 1:]
        parts = tail.split('/')
        name = parts[-1] if parts[0] in ('ru', 'en', 'tr') else tail
        for lang in BOOK_LANGS:
            cand = '{}/{}'.format(BOOK, name) if lang == 'az' else '{}/{}/{}'.format(BOOK, lang, name)
            if (ROOT / cand).is_file():
                out[lang] = cand
    else:
        parts = path.split('/')
        name = parts[-1] if parts[0] in ('ru', 'en') else path
        for lang in SITE_LANGS:
            cand = name if lang == 'az' else '{}/{}'.format(lang, name)
            if (ROOT / cand).is_file():
                out[lang] = cand
    return out


def build_block(path: str) -> str:
    lines = ['  <link rel="canonical" href="{}{}" />'.format(BASE, path)]
    v = variants(path)
    if len(v) > 1:
        for lang in (BOOK_LANGS if path.startswith(BOOK + '/') else SITE_LANGS):
            if lang in v:
                lines.append('  <link rel="alternate" hreflang="{}" href="{}{}" />'.format(
                    lang, BASE, v[lang]))
        if 'az' in v:
            lines.append('  <link rel="alternate" hreflang="x-default" href="{}{}" />'.format(
                BASE, v['az']))
    return '\n'.join(lines)


# Порядок атрибутов в этих тегах в проекте разный: где-то rel впереди, где-то
# href. Поэтому ловим любой <link>, а решаем по его содержимому.
RX_LINK = re.compile(r'[ \t]*<link\b[^>]*>\s*\n?', re.I)


def _drop_old(head: str) -> str:
    def repl(m):
        tag = m.group(0)
        if re.search(r'rel=["\']canonical["\']', tag, re.I):
            return ''
        if re.search(r'rel=["\']alternate["\']', tag, re.I) and 'hreflang=' in tag.lower():
            return ''
        return tag
    return RX_LINK.sub(repl, head)


def process(path: str, text: str) -> str | None:
    head_end = text.find('</head>')
    if head_end == -1:
        return None
    head, rest = text[:head_end], text[head_end:]
    if re.search(r'http-equiv=["\']refresh["\']', head, re.I):
        return None                       # страница-перенаправление
    new_head = _drop_old(head)
    # После удаления старых тегов остаются пустые строки; без этого повторный
    # прогон каждый раз добавлял бы ещё одну и скрипт не был бы идемпотентен.
    new_head = new_head.rstrip() + '\n'
    block = build_block(path)
    new_head += block + '\n'
    out = new_head + rest
    return out if out != text else None


def main(apply: bool = False) -> None:
    changed = skipped = same = 0
    samples = []
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        rel = Path(dp).relative_to(ROOT)
        for f in sorted(fn):
            if not f.endswith('.html'):
                continue
            path = (rel / f).as_posix()
            if path in SKIP_FILES or f in SKIP_FILES and rel.as_posix() == '.':
                skipped += 1
                continue
            p = Path(dp) / f
            raw = p.read_bytes()
            crlf = raw.count(b'\r\n') > raw.count(b'\n') // 2
            t = raw.decode('utf-8', 'replace').replace('\r\n', '\n')
            new = process(path, t)
            if new is None:
                same += 1
                continue
            changed += 1
            if len(samples) < 5:
                samples.append(path)
            if apply:
                p.write_bytes((new.replace('\n', '\r\n') if crlf else new).encode('utf-8'))
    print('изменено {}, без изменений {}, пропущено {}'.format(changed, same, skipped))
    for s in samples:
        print('   напр. ' + s)
    if not apply:
        print('пробный прогон — запустить с --apply')


if __name__ == '__main__':
    main('--apply' in sys.argv)
