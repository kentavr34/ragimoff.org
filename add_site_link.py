#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
add_site_link.py — возврат на основной сайт из бокового меню книги.

Ссылка «← ragimoff.org» в шапке страницы книги есть, но скрыта на узких
экранах правилом `@media (max-width:600px){.hdr-back{display:none}}` — на
телефоне вернуться на основной сайт было нечем. В шапке выезжающего меню
рядом с крестиком при этом пустует место.

Инструмент ставит ссылку туда: слева «← ragimoff.org», справа крестик.
Адрес выбирается по языку издания: русское ведёт на /ru/, английское на
/en/; у турецкого издания книги пары на основном сайте нет, поэтому оно
ведёт на азербайджанскую главную.

    python add_site_link.py            # отчёт
    python add_site_link.py --apply
"""
from __future__ import annotations
import re, sys, io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).parent
BOOK = ROOT / 'klinik-psixiatriya'
APPLY = '--apply' in sys.argv

# язык издания → (адрес на основном сайте, подпись для screen reader)
SITE = {
    'az': ('https://ragimoff.org/', 'Əsas sayta qayıt'),
    'ru': ('https://ragimoff.org/ru/', 'Вернуться на основной сайт'),
    'en': ('https://ragimoff.org/en/', 'Back to the main site'),
    'tr': ('https://ragimoff.org/', 'Ana siteye dön'),
}
HDR = re.compile(r'<div class="sb-hdr">(?!\s*<a class="sb-site")')


def main() -> int:
    total = 0
    for lg, folder in (('az', BOOK), ('ru', BOOK / 'ru'),
                       ('en', BOOK / 'en'), ('tr', BOOK / 'tr')):
        href, title = SITE[lg]
        link = (f'<div class="sb-hdr"><a class="sb-site" href="{href}" '
                f'title="{title}">← ragimoff.org</a>')
        n = 0
        for fp in sorted(folder.glob('*.html')):
            raw = fp.read_bytes().decode('utf-8')
            crlf = raw.count('\r\n') > raw.count('\n') // 2
            t = raw.replace('\r\n', '\n')
            if 'class="sb-hdr"' not in t or 'sb-site' in t:
                continue
            new = HDR.sub(link, t, count=1)
            if new == t:
                continue
            n += 1
            if APPLY:
                fp.write_bytes((new.replace('\n', '\r\n') if crlf else new).encode('utf-8'))
        total += n
        print(f'  {lg}: страниц {n} → {href}')
    print(f'итого {total}')
    print('применено' if APPLY else 'пробный прогон — запустить с --apply')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
