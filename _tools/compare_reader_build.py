# -*- coding: utf-8 -*-
"""_tools/compare_reader_build.py — сверка пересобранной читалки с живой (04.11.2026). Только чтение.

    python _tools/compare_reader_build.py <корень копии сайта> <slug> [az ru en] [--live <корень сайта>]

Для каждого языка сравнивает books/<slug>/[<lang>/]:
  · index.html (читалка): главы пословно (по позиции, а при перестановке — по содержимому), якоря #chN,
    data-title, оглавление (.rd-contents / .rd-toc), части, ссылки внутри глав, атрибуты <html>, head
    (link/meta/title), подключённые стили и скрипты, титул, набор HTML-тегов в тексте;
  · заглушки NN-*.html: имена файлов, текст .bk-read пословно, h1, адрес перенаправления, hreflang,
    canonical, title, стили.
Код возврата 1, если в тексте глав читалки есть расхождения (слова) — остальное печатается как отличия разметки.
"""
import difflib
import os
import re
import sys

from bs4 import BeautifulSoup

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH_RX = re.compile(r'\d\d-.*\.html$')


def soup(p):
    return BeautifulSoup(open(p, encoding='utf-8').read(), 'html.parser')


def words(s):
    return re.sub(r'\s+', ' ', s).strip().split(' ')


def chap_text(art):
    a = BeautifulSoup(str(art), 'html.parser')
    for x in a.select('.rd-chap__n, .rd-orn, .rd-chap__part'):
        x.decompose()
    return a.get_text(' ')


def reader_info(p):
    s = soup(p)
    info = {'chapters': [(a.get('id'), a.get('data-title'), chap_text(a)) for a in s.select('article.rd-chap')],
            'toc': [(a.get('href'), re.sub(r'\s+', ' ', a.get_text(' ')).strip()) for a in s.select('.rd-contents a')],
            'parts': [t.get_text(' ').strip() for t in s.select('.rd-contents .toc-part')],
            'links': sorted(set(a.get('href') for a in s.select('article.rd-chap a[href]'))),
            'html_attrs': dict(s.html.attrs) if s.html else {},
            'head_links': [(tuple(l.get('rel') or []), l.get('hreflang'), l.get('href')) for l in s.select('head link')],
            'meta': [(m.get('name') or m.get('property'), m.get('content')) for m in s.select('head meta')],
            'title': s.title.get_text() if s.title else '',
            'scripts': [x.get('src') for x in s.select('script[src]')],
            'styles': [l.get('href') for l in s.select('link[rel=stylesheet]')],
            'cover': re.sub(r'\s+', ' ', s.select_one('#rd-title').get_text(' ')).strip() if s.select_one('#rd-title') else '',
            'tags': {}}
    for a in s.select('article.rd-chap'):
        for t in a.find_all(True):
            info['tags'][t.name] = info['tags'].get(t.name, 0) + 1
    return info


def stub_info(p):
    s = soup(p)
    body, h1, meta = s.select_one('.bk-read'), s.select_one('.bk-chead__h1'), s.select_one('meta[http-equiv=refresh]')
    return {'text': body.get_text(' ') if body else None,
            'h1': h1.get_text(' ').strip() if h1 else None,
            'redirect': meta.get('content') if meta else None,
            'html_attrs': dict(s.html.attrs) if s.html else {},
            'hreflang': [(l.get('hreflang'), l.get('href')) for l in s.select('link[rel=alternate]')],
            'canonical': [l.get('href') for l in s.select('link[rel=canonical]')],
            'title': s.title.get_text() if s.title else '',
            'styles': [l.get('href') for l in s.select('link[rel=stylesheet]')]}


def wdiff(a, b, label, limit=6):
    wa, wb = words(a), words(b)
    if wa == wb:
        return 0
    n = 0
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, wa, wb, autojunk=False).get_opcodes():
        if tag == 'equal':
            continue
        n += max(i2 - i1, j2 - j1)
        if limit > 0:
            print(f'    {label}: {tag} live={" ".join(wa[i1:i2])[:140]!r} | new={" ".join(wb[j1:j2])[:140]!r}')
            limit -= 1
    return n


def compare_lang(new_root, live_root, slug, lang):
    sub = '' if lang == 'az' else lang
    nd, ld = os.path.join(new_root, 'books', slug, sub), os.path.join(live_root, 'books', slug, sub)
    print(f'=== {slug} / {lang}')
    ni, li = reader_info(os.path.join(nd, 'index.html')), reader_info(os.path.join(ld, 'index.html'))
    lc, nc = li['chapters'], ni['chapters']
    print(f'  главы читалки: live {len(lc)} / new {len(nc)}')
    # по позиции; при перестановке глав — по содержимому (текст той же главы ищем на другом месте)
    by_text = {}
    for k, c in enumerate(nc):
        by_text.setdefault(' '.join(words(c[2])), []).append(k)
    nwords, moved = 0, []
    for k in range(max(len(lc), len(nc))):
        a = lc[k] if k < len(lc) else ('', '', '')
        b = nc[k] if k < len(nc) else ('', '', '')
        if words(a[2]) == words(b[2]):
            if a[1] != b[1]:
                print(f'  data-title {k + 1}: live {a[1]!r} / new {b[1]!r}')
            continue
        same = by_text.get(' '.join(words(a[2])))
        if same:
            moved.append((k + 1, same[0] + 1))
            continue
        nwords += wdiff(a[2], b[2], f'гл.{k + 1}')
    if moved:
        print('  главы переставлены (текст тот же): ' + ', '.join(f'live #ch{a} → new #ch{b}' for a, b in moved))
    print(f'  расхождений слов в тексте глав: {nwords}')
    if li['toc'] != ni['toc']:
        lt, nt = li['toc'], ni['toc']
        print(f'  оглавление читалки: live {len(lt)} / new {len(nt)} пунктов; отличия:')
        for k in range(max(len(lt), len(nt))):
            a, b = (lt[k] if k < len(lt) else None), (nt[k] if k < len(nt) else None)
            if a != b:
                print(f'    {k}: live {a} / new {b}')
    else:
        print(f'  оглавление читалки: совпадает ({len(li["toc"])} пунктов)')
    if li['parts'] != ni['parts']:
        print(f'  части: live {li["parts"]} / new {ni["parts"]}')
    for key in ('links', 'html_attrs', 'head_links', 'meta', 'title', 'scripts', 'styles', 'cover', 'tags'):
        if li[key] != ni[key]:
            print(f'  {key}: live {li[key]} / new {ni[key]}')
    lf, nf = sorted(f for f in os.listdir(ld) if CH_RX.match(f)), sorted(f for f in os.listdir(nd) if CH_RX.match(f))
    if lf != nf:
        print(f'  имена заглушек: только live {sorted(set(lf) - set(nf))}; только new {sorted(set(nf) - set(lf))}')
    sw, attrs_diff, redirects, titles = 0, {}, 0, 0
    for f in sorted(set(lf) & set(nf)):
        a, b = stub_info(os.path.join(ld, f)), stub_info(os.path.join(nd, f))
        if a['text'] is None or b['text'] is None:
            print(f'  {f}: нет .bk-read: live={a["text"] is None} new={b["text"] is None}')
            continue
        sw += wdiff(a['text'], b['text'], f'заглушка {f}', limit=0)
        if a['redirect'] != b['redirect']:
            redirects += 1
            print(f'  {f}: redirect live {a["redirect"]} / new {b["redirect"]}')
        if a['title'] != b['title']:
            titles += 1
        for key in ('html_attrs', 'hreflang', 'canonical', 'styles'):
            if a[key] != b[key]:
                attrs_diff.setdefault(key, (f, a[key], b[key]))
    print(f'  заглушки: общих {len(set(lf) & set(nf))}, расхождений слов в тексте {sw}, перенаправления изменены {redirects}, '
          f'title изменён {titles}, отличия шапки: {sorted(attrs_diff) or "нет"}')
    for key, (f, x, y) in sorted(attrs_diff.items()):
        print(f'    пример {f} {key}: live {x} / new {y}')
    return nwords


def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
    argv = sys.argv[1:]
    live = SITE
    if '--live' in argv:
        i = argv.index('--live')
        live = os.path.abspath(argv[i + 1])
        del argv[i:i + 2]
    if len(argv) < 2:
        sys.exit(__doc__)
    new_root, slug = os.path.abspath(argv[0]), argv[1]
    total = sum(compare_lang(new_root, live, slug, lang) for lang in (argv[2:] or ['az', 'ru', 'en']))
    print('ИТОГО расхождений слов в тексте глав читалки:', total)
    sys.exit(1 if total else 0)


if __name__ == '__main__':
    main()
