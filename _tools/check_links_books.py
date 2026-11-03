# -*- coding: utf-8 -*-
"""_tools/check_links_books.py — внутренние ссылки и якоря страниц книг (03.11.2026). Только чтение.

Проверяет во всех .html заданных каталогов:
  · <a href> на файлы сайта (относительные и от корня; каталог → index.html): файл существует;
  · якорь #id: id есть в целевой странице (страницы-перенаправления с meta refresh якорями не проверяются);
  · <link rel=canonical|alternate href="https://ragimoff.org/...">: файл есть;
  · data-lang-url-*="/..." — файл есть.
Внешние http(s), mailto, tel, javascript, data — пропускаются; ссылки на не-HTML (css/js/img/json) — только наличие файла.

    python _tools/check_links_books.py                         # klinik-psixiatriya, books/{phoenix-era,virus-viny,shizofreniya}, каталоги книг
    python _tools/check_links_books.py klinik-psixiatriya      # свой список каталогов/файлов
Код возврата 1, если есть битые ссылки/якоря.
"""
import collections
import html as H
import os
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://ragimoff.org'
DEFAULT = ['klinik-psixiatriya', 'books/phoenix-era', 'books/virus-viny', 'books/shizofreniya',
           'books/index.html', 'books/ru/index.html', 'books/en/index.html']
_ids = {}
_redir = {}
A_RX = re.compile(r'<a\s[^>]*?href\s*=\s*"([^"]*)"', re.I)
LINK_RX = re.compile(r'<link\s[^>]*?rel="(canonical|alternate)"[^>]*?href="([^"]*)"', re.I)
LANG_RX = re.compile(r'data-lang-url-[a-z]+="([^"]*)"')
ID_RX = re.compile(r'\sid\s*=\s*"([^"]+)"')


def read(p):
    with open(p, encoding='utf-8', errors='replace') as f:
        return f.read()


def ids_of(p):
    if p not in _ids:
        s = read(p)
        _ids[p] = set(H.unescape(x) for x in ID_RX.findall(s))
        _redir[p] = bool(re.search(r'http-equiv="refresh"', s[:3000], re.I))
    return _ids[p]


def resolve(cur, href):
    """→ (путь к файлу | None, якорь) или (None, None), если ссылка внешняя/служебная."""
    h = H.unescape(href.strip())
    if not h or re.match(r'^(mailto:|tel:|javascript:|data:|#$)', h, re.I):
        return None, None
    if h.startswith(BASE):
        h = h[len(BASE):] or '/'
    if re.match(r'^[a-z][a-z0-9+.-]*:', h, re.I) or h.startswith('//'):
        return None, None
    u = urlsplit(h)
    path, frag = unquote(u.path), unquote(u.fragment)
    if not path:
        return cur, frag
    if path.startswith('/'):
        p = os.path.join(ROOT, path.lstrip('/'))
    else:
        p = os.path.normpath(os.path.join(os.path.dirname(cur), path))
    if os.path.isdir(p):
        p = os.path.join(p, 'index.html')
    return os.path.normpath(p), frag


def check(files):
    total = 0
    bad = collections.Counter()
    where = collections.defaultdict(list)
    for f in files:
        s = read(f)
        items = [('a', h) for h in A_RX.findall(s)] + [('link', h) for _, h in LINK_RX.findall(s)] + [('lang', h) for h in LANG_RX.findall(s)]
        for kind, h in items:
            p, frag = resolve(f, h)
            if p is None:
                continue
            total += 1
            if not os.path.isfile(p):
                key = ('нет файла', os.path.relpath(p, ROOT).replace('\\', '/'))
                bad[key] += 1
                where[key].append(os.path.relpath(f, ROOT).replace('\\', '/'))
                continue
            if frag and p.endswith('.html'):
                ids = ids_of(p)
                if frag not in ids and not _redir.get(p):
                    key = ('нет якоря', os.path.relpath(p, ROOT).replace('\\', '/') + '#' + frag)
                    bad[key] += 1
                    where[key].append(os.path.relpath(f, ROOT).replace('\\', '/'))
    return total, bad, where


def main():
    targets = sys.argv[1:] or DEFAULT
    files = []
    for t in targets:
        p = os.path.join(ROOT, t)
        if os.path.isfile(p):
            files.append(p)
        else:
            for dp, dn, fn in os.walk(p):
                dn[:] = [d for d in dn if not d.startswith('_backup')]
                files += [os.path.join(dp, x) for x in fn if x.endswith('.html')]
    files = sorted(set(files))
    total, bad, where = check(files)
    print('страниц: %d | проверено ссылок/якорей: %d | битых: %d (уникальных целей: %d)' % (len(files), total, sum(bad.values()), len(bad)))
    for (kind, tgt), n in bad.most_common(40):
        print('  %-11s %-70s x%-4d напр. %s' % (kind, tgt, n, where[(kind, tgt)][0]))
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
