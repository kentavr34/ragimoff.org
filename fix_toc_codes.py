#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_toc_codes.py — коды в оглавлении берутся из канона, а не из прошлого.

ЧТО БЫЛО НЕ ТАК (2026-08-10)
============================
Страницу `mundericat.html` собрали до того, как коды DSM в книге перевели
с ICD-9-CM на ICD-10-CM, и с тех пор не пересобирали. В дереве DSM-5-TR
осталась смесь двух поколений: у расстройств уже стоят F-коды, а рядом
доживают обрубки ICD-9 — `319`, `296.`, `303.`, `309.`, `301.`, `316`.
Заголовки глав там же несут числовые диапазоны DSM-IV (299–319, 296–301,
296–300), которые вдобавок перекрывают друг друга и на узком экране
налезают на название главы.

Всего 25 кодов в дереве DSM и по 6 в деревьях XBT-11 и XBT-10 расходились
с `_codes_canon.json` — а канон и есть источник шапок карточек, то есть
оглавление противоречило самим карточкам.

ЧТО ДЕЛАЕТ
==========
Три дерева классификаций встроены в боковое меню КАЖДОЙ страницы книги,
а не только в оглавление, поэтому обход идёт по всем страницам.

Переписывает код каждого пункта значением из канона и
пересчитывает диапазон главы. Для XBT-11 и XBT-10 диапазон главы — это
официальный блок классификации, он остаётся как есть; для DSM-5-TR
официальных блоков не существует, поэтому диапазон выводится из кодов
самих расстройств главы: от наименьшего к наибольшему.

    python fix_toc_codes.py            # отчёт
    python fix_toc_codes.py --apply
"""
from __future__ import annotations
import re, sys, io, json, html as H
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).parent
BOOK = ROOT / 'klinik-psixiatriya'
LANGS = {'az': BOOK, 'ru': BOOK / 'ru', 'en': BOOK / 'en', 'tr': BOOK / 'tr'}
APPLY = '--apply' in sys.argv
FIELD = {'icd': 'icd11_shown', 'dsm': 'dsm_code', 'icd10': 'icd10_code'}
# Деревья встречаются в двух видах разметки: боковое меню (cls-tree,
# nav-code / sub-code) и основной список на странице оглавления
# (cls-panel, tc-range / sc). Обрабатываются оба.
TREE = re.compile(r'<div class="(?:cls-tree|cls-panel)" data-cls="(\w+)"[\s\S]*?'
                  r'(?=<div class="(?:cls-tree|cls-panel)" data-cls=|<script)')
SUB = re.compile(r'(<a href="([0-9A-Z]{4})\.html"[^>]*>\s*<span class="(?:sub-code|sc)">)([^<]*)(</span>)')
CHAP = re.compile(r'<div class="(?:nav-item nav-has-sub|toc-ch)">[\s\S]*?'
                  r'(?=<div class="(?:nav-item nav-has-sub|toc-ch)">|$)')
NAVCODE = re.compile(r'(<span class="(?:nav-code|tc-range)">)([^<]*)(</span>)')


def sort_key(code: str) -> tuple:
    """Порядок кодов вида F06.1, G47.33, N94.3 — по букве, затем по числу."""
    m = re.match(r'([A-Z])(\d+)(?:\.(\d+))?', code.strip())
    if not m:
        return ('Z', 999, 999)
    return (m.group(1), int(m.group(2)), int(m.group(3) or 0))


def span(codes: list[str]) -> str:
    """Диапазон главы по кодам её расстройств.

    Группируем по букве: «F32–N94» читалось бы как «и всё, что между», а
    между F и N лежат чужие классы. Правильно — «F32–F34 · N94»."""
    flat: list[str] = []
    for c in codes:
        flat += re.findall(r'[A-Z]\d+(?:\.\w+)?', c)
    if not flat:
        return '—'
    by_letter: dict[str, list[str]] = {}
    for c in flat:
        by_letter.setdefault(c[0], []).append(c.split('.')[0])
    parts = []
    for letter in sorted(by_letter):
        group = by_letter[letter]
        lo = min(group, key=sort_key)
        hi = max(group, key=sort_key)
        parts.append(lo if lo == hi else f'{lo}–{hi}')
    return ' · '.join(parts)


def main() -> int:
    canon = {r['code']: r for r in
             json.loads((ROOT / '_codes_canon.json').read_text(encoding='utf-8'))
             ['header_source']['rows']}
    stat = {'sub': 0, 'chap': 0, 'files': 0}
    for lg, folder in LANGS.items():
      for fp in sorted(folder.glob('*.html')):
        if 'cls-tree' not in fp.read_text(encoding='utf-8', errors='ignore'):
            continue
        raw = fp.read_bytes().decode('utf-8')
        crlf = raw.count('\r\n') > raw.count('\n') // 2
        t = raw.replace('\r\n', '\n')
        subs = chaps = 0

        def fix_tree(m: re.Match) -> str:
            nonlocal subs, chaps
            cls, tree = m.group(1), m.group(0)
            field = FIELD.get(cls)
            if not field:
                return tree

            def fix_sub(s: re.Match) -> str:
                nonlocal subs
                want = str(canon.get(s.group(2), {}).get(field, '')).strip()
                if not want or want == H.unescape(s.group(3)).strip():
                    return s.group(0)
                subs += 1
                return s.group(1) + H.escape(want) + s.group(4)

            tree = SUB.sub(fix_sub, tree)
            if cls != 'dsm':          # у XBT-11 и XBT-10 диапазон главы официальный
                return tree

            def fix_chap(c: re.Match) -> str:
                nonlocal chaps
                block = c.group(0)
                kids = [H.unescape(x) for x in
                        re.findall(r'<span class="(?:sub-code|sc)">([^<]*)</span>', block)]
                new = span(kids)

                def put(n: re.Match) -> str:
                    nonlocal chaps
                    if n.group(2).strip() == new:
                        return n.group(0)
                    chaps += 1
                    return n.group(1) + new + n.group(3)

                return NAVCODE.sub(put, block, count=1)

            return CHAP.sub(fix_chap, tree)

        new = TREE.sub(fix_tree, t)
        if new == t:
            continue
        stat['sub'] += subs; stat['chap'] += chaps; stat['files'] += 1
        if APPLY:
            fp.write_bytes((new.replace('\n', '\r\n') if crlf else new).encode('utf-8'))
    print(f'итого: файлов {stat["files"]}, кодов {stat["sub"]}, глав {stat["chap"]}')
    print('применено' if APPLY else 'пробный прогон — запустить с --apply')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
