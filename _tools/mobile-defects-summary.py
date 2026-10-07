#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""mobile-defects-summary.py — сводка обмера `_tools/mobile-defects.js`.

Читает один или два JSON-файла (до/после) и печатает:
  1) счёт по классам дефектов (штук / страниц);
  2) TSV-таблицу «страница | язык | класс | элемент | было | стало»;
  3) краткие примеры по каждому классу.

Запуск:
  python _tools/mobile-defects-summary.py --before before_390.json --after after_390.json
  python _tools/mobile-defects-summary.py --before before_390.json --tsv out.tsv
"""
import argparse
import collections
import json
import os
import sys

CLASSES = ['gap', 'inset', 'overf', 'photo', 'align', 'size', 'stick']
CLS_RU = {
    'gap': 'GAP пустая полоса',
    'inset': 'INSET прижато к грани',
    'overf': 'OVERF переполнение',
    'photo': 'PHOTO прямоугольник фото',
    'align': 'ALIGN разъезд/наезд',
    'size': 'SIZE пропорции',
    'stick': 'STICK наложение',
}


def lang_of(path):
    if path.startswith('ru/'):
        return 'ru'
    if path.startswith('en/'):
        return 'en'
    return 'az'


def load(path):
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    return {r['file']: r for r in data if 'file' in r}


def item_key(it):
    """Ключ сопоставления записей до/после — класс + элемент + подкласс."""
    cls = it.get('cls') or it.get('slot') or ''
    el = it.get('el') or it.get('a') or ''
    sub = it.get('src') or it.get('txt') or it.get('where') or ''
    return (cls, el, str(sub)[:40])


def describe(it):
    c = it.get('cls')
    if c == 'smallimg':
        return 'img %s — %s px, доля %s' % (it.get('src', ''), it.get('w'), it.get('share'))
    if c == 'bigh':
        return '%s %s px (порог %s)' % (it.get('el'), it.get('fs'), it.get('lim'))
    if c == 'lowbtn':
        return '%s — высота %s (норма 44)' % (it.get('el'), it.get('h'))
    if c == 'lineh':
        return '%s кегль %s, строка %s (x%s) — %s' % (it.get('role', ''), it.get('fs'), it.get('lh'), it.get('ratio'), (it.get('txt') or '')[:26])
    if c == 'mix':
        return '%s — text-align %s' % (it.get('el'), it.get('ta'))
    if c == 'overlap':
        return '%s ∩ %s' % (it.get('a'), it.get('b'))
    if it.get('ringA') is not None:
        return '%s край %s' % (it.get('src'), it.get('ringA'))
    if it.get('src'):
        return '%s' % it.get('src')
    return (it.get('el') or '') + ' ' + (it.get('txt') or '')


def short(it):
    c = it.get('cls')
    if c == 'viewport':
        return 'вылет за вьюпорт: %s w=%s cw=%s %s' % (it.get('el'), it.get('w'), it.get('cw'), it.get('src', ''))
    if c == 'clipped':
        return 'обрезан текст: %s («%s») %s→%s' % (it.get('el'), (it.get('txt') or '')[:24], it.get('cw'), it.get('sw'))
    if c == 'wider':
        return 'текст шире контейнера: %s («%s») %s→%s' % (it.get('el'), (it.get('txt') or '')[:24], it.get('cw'), it.get('sw'))
    if c == 'strip-over-hero':
        return 'полоса цифр накрывает герой на %s px' % it.get('overlap')
    if c in ('fixed-over-text', 'header-over-text'):
        return '%s (%s) перекрывает текст: %s' % (it.get('el'), it.get('pos'), it.get('sample'))
    if it.get('h') is not None and it.get('where') is not None:
        return 'полоса %s px (%s→%s), выше: %s, ниже: %s' % (it.get('h'), it.get('t'), it.get('b'), (it.get('above') or '')[:26], (it.get('below') or '')[:26])
    if it.get('insetL') is not None:
        return 'инсет L=%s T=%s в %s (паддинг %s)' % (it.get('insetL'), it.get('insetT'), it.get('panel'), it.get('pad'))
    return describe(it)


def counts(data):
    cnt = collections.Counter()
    pages = collections.Counter()
    for f, r in data.items():
        if 'error' in r:
            continue
        for k in CLASSES:
            n = len(r.get(k, []))
            if n:
                cnt[k] += n
                pages[k] += 1
    return cnt, pages


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--before', required=True)
    ap.add_argument('--after')
    ap.add_argument('--tsv')
    ap.add_argument('--examples', type=int, default=6)
    args = ap.parse_args()

    before = load(args.before)
    after = load(args.after) if args.after else None

    print('страниц в замере: %d' % len(before))
    bad = [f for f, r in before.items() if 'error' in r]
    if bad:
        print('ошибки замера: %s' % ', '.join(bad))

    for label, data in (('ДО', before), ('ПОСЛЕ', after) if after else ('ДО', before),):
        if data is None:
            continue
        cnt, pages = counts(data)
        print('\n── %s ──' % label)
        total = 0
        for k in CLASSES:
            total += cnt[k]
            print('  %-6s %5d шт / %3d стр   %s' % (k, cnt[k], pages[k], CLS_RU[k]))
        print('  ИТОГО  %5d шт' % total)

    if after:
        print('\n── ИСЧЕЗЛО ПОСЛЕ ПРАВОК (по страницам) ──')
        for f in sorted(before, key=lambda x: (lang_of(x), x)):
            b, a = before[f], after.get(f, {})
            if 'error' in b:
                continue
            gone, left = [], []
            bset = {}
            for k in CLASSES:
                for it in b.get(k, []):
                    bset.setdefault(k, []).append(it)
            for k in CLASSES:
                aset = [item_key(x) for x in a.get(k, [])] if 'error' not in a else []
                for it in bset.get(k, []):
                    if item_key(it) in aset:
                        left.append((k, it))
                    else:
                        gone.append((k, it))
            if gone:
                print('%s [%s]: снято %d' % (f, lang_of(f), len(gone)))
                for k, it in gone[:args.examples]:
                    print('    %-6s %s' % (k, short(it)))

    if args.tsv:
        rows = ['страница\tязык\tкласс\tэлемент\tбыло\tстало']
        for f in sorted(before, key=lambda x: (lang_of(x), x)):
            b, a = before[f], (after.get(f, {}) if after else {})
            for k in CLASSES:
                aset = {}
                if after and 'error' not in a:
                    for it in a.get(k, []):
                        aset[item_key(it)] = it
                for it in b.get(k, []):
                    key = item_key(it)
                    was = short(it)
                    now = 'исправлено' if (after and key not in aset) else ('без изменений' if after else '')
                    if after and key in aset:
                        continue
                    rows.append('%s\t%s\t%s\t%s\t%s\t%s' % (f, lang_of(f), k, describe(it), was, now))
        with open(args.tsv, 'w', encoding='utf-8') as fh:
            fh.write('\n'.join(rows) + '\n')
        print('\nTSV: %s (%d строк)' % (args.tsv, len(rows) - 1))


if __name__ == '__main__':
    main()
