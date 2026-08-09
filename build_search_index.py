#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_search_index.py — индекс полнотекстового поиска книги.

ЧТО БЫЛО НЕ ТАК (обнаружено 2026-08-09)
=======================================
Прежняя версия индексировала страницы `bolme-*.html` — структуру книги ДО
разбиения на карточки по расстройствам, и держала абсолютный путь на
`C:\\Users\\SAM\\Desktop\\sayt2`, которого больше нет. После реорганизации её
не запускали, страницы `bolme-*` опустели, и в индексе осталось 0 карточек
из 104: поиск по книге не находил ни одного расстройства. При этом 137
страниц книги грузят этот индекс.

ЧТО ДЕЛАЕТ СЕЙЧАС
=================
Обходит изданные карточки и справочные страницы азербайджанского издания,
берёт каждый заголовок с якорем и текст до следующего заголовка. Коды
XBT-11 / XBT-10 / DSM-5-TR из шапки карточки попадают в поле `codes` —
поиск по «6A02» или «F84.0» должен находить карточку.

Схема записи (её ждёт обработчик поиска в шапке страниц):
    {page, id, title, codes, icd, text, sub}
`goTo(page, id)` открывает `page.html#id`.

    python build_search_index.py            # отчёт
    python build_search_index.py --apply
"""
from __future__ import annotations
import re, sys, io, json, html as H
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).parent
BOOK = ROOT / 'klinik-psixiatriya'
OUT = BOOK / 'search-index.json'
APPLY = '--apply' in sys.argv

CARD = re.compile(r'^[0-9A-Z]{4}$')
LOOSE = re.compile(r'<(?![a-zA-Z/!?])')          # «<» перед не-буквой — это текст
HEAD = re.compile(r'<h([1-4])\b([^>]*)>([\s\S]*?)</h\1>', re.I)
SNIPPET = 420

# страницы без кода расстройства, которые тоже стоит искать
EXTRA = ('abbreviatur', 'terminoloji-luget', 'mundericat', 'kitab-haqqinda',
         'mugeddime', 'melumat', 'yekun', 'elave-acde', 'elave-skalalar')


def visible(fragment: str) -> str:
    fragment = re.sub(r'<(script|style)\b[\s\S]*?</\1>', ' ', fragment, flags=re.I)
    fragment = re.sub(r'<nav[\s\S]*?</nav>', ' ', fragment, flags=re.I)
    return re.sub(r'\s+', ' ', H.unescape(re.sub(r'<[^>]*>', ' ', LOOSE.sub('&lt;', fragment)))).strip()


def page_codes(main: str) -> str:
    """Коды из шапки карточки: XBT-11, XBT-10, DSM-5-TR."""
    codes = re.findall(r'<span class="dh-code">([^<]{1,16})</span>', main)
    return ' '.join(dict.fromkeys(H.unescape(c).strip() for c in codes))


def build() -> list[dict]:
    entries: list[dict] = []
    pages = sorted(p for p in BOOK.glob('*.html')
                   if CARD.fullmatch(p.stem) or p.stem in EXTRA)
    for fp in pages:
        t = fp.read_text(encoding='utf-8', errors='ignore')
        m = re.search(r'<main[\s\S]*?</main>', t, re.I)
        if not m:
            continue
        main = m.group(0)
        h1 = re.search(r'<h1[^>]*>([\s\S]*?)</h1>', main, re.I)
        sub = visible(h1.group(1)) if h1 else fp.stem
        codes = page_codes(main)
        heads = [(mm.start(), mm.end(), mm.group(2), visible(mm.group(3)))
                 for mm in HEAD.finditer(main)]
        # заголовок страницы — отдельной записью, чтобы карточка находилась по имени
        entries.append({'page': fp.stem, 'id': '', 'title': sub, 'codes': codes,
                        'icd': codes, 'text': visible(main[:1400])[:SNIPPET], 'sub': sub})
        for i, (s, e, attrs, title) in enumerate(heads):
            hid = re.search(r'id="([^"]+)"', attrs)
            if not hid or not title:
                continue
            body = main[e:heads[i + 1][0]] if i + 1 < len(heads) else main[e:]
            entries.append({'page': fp.stem, 'id': hid.group(1), 'title': title,
                            'codes': codes, 'icd': codes,
                            'text': visible(body)[:SNIPPET], 'sub': sub})
    return entries


def main() -> int:
    entries = build()
    cards = len({e['page'] for e in entries if CARD.fullmatch(e['page'])})
    print(f'записей {len(entries)}, страниц {len({e["page"] for e in entries})}, '
          f'карточек {cards} из {sum(1 for p in BOOK.glob("*.html") if CARD.fullmatch(p.stem))}')
    if APPLY:
        OUT.write_text(json.dumps(entries, ensure_ascii=False, separators=(',', ':')),
                       encoding='utf-8')
        print(f'записано {OUT} — {OUT.stat().st_size // 1024} кб')
    else:
        print('пробный прогон — запустить с --apply')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
