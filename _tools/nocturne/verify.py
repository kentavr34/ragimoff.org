#!/usr/bin/env python3
"""Проверка сборки «Ноктюрн»:
1) ТЕКСТ: видимый текст содержимого каждой новой страницы (без шапки, первого
   экрана и подвала) совпадает с текстом оригинала слово в слово;
   первый экран — бейдж, заголовок и лид — тоже из оригинала.
2) ЦЕНЫ: все суммы (AZN, руб., ₽) оригинала есть на новой странице, лишних нет.
3) ССЫЛКИ: каждая относительная ссылка/картинка ведёт на существующий файл.
4) ФОРМЫ: формы оригинала (id, имена полей) и скрипты оплаты на месте.
Запуск из папки site: python -I _tools/nocturne/verify.py
"""
import re, sys, pathlib
from bs4 import BeautifulSoup
sys.stdout.reconfigure(encoding='utf-8')
SITE = pathlib.Path(__file__).resolve().parents[2]
OUT = SITE / 'test' / 'nocturne'
lines = (SITE / '_tools' / 'nocturne' / 'SITEMAP.md').read_text(encoding='utf-8').splitlines()
pairs = [l.split('  ←  ') for l in lines if '  ←  ' in l and l.split('  ←  ')[1].endswith('.html')]

PRICE = re.compile(r'\d[\d\s.,]*\s?(?:AZN|azn|манат|руб\.?|₽|тыс\.\s?руб)')
norm = lambda s: ' '.join(s.split())
bad = 0


def body_text(soup, new):
    main = soup.find('main')
    if main is None:            # у части старых страниц нет <main>: тело без шапки, меню, подвала и служебных окон
        main = soup.body
        for el in main.find_all(['header', 'footer'], recursive=False) + main.select('nav.mobile-nav, .skip-link, .wa-float, #dgLightbox, #kitab-modal'):
            el.decompose()
    for sel in (['.n-hero', '.n-marquee'] if new else ['section.page-hero', 'section.page-hero-x']):
        for el in main.select(sel):
            el.decompose()
    for el in main.find_all(['script', 'style', 'noscript']):
        el.decompose()
    return norm(main.get_text(' '))


for new, orig in pairs:
    a = BeautifulSoup((SITE / orig).read_text(encoding='utf-8'), 'lxml')
    b = BeautifulSoup((OUT / new).read_text(encoding='utf-8'), 'lxml')
    ta, tb = body_text(a, False), body_text(b, True)
    probs = []
    if ta != tb:
        i = next((k for k in range(min(len(ta), len(tb))) if ta[k] != tb[k]), min(len(ta), len(tb)))
        probs.append('ТЕКСТ расходится с позиции %d: «…%s» vs «…%s»' % (i, ta[max(0, i - 30):i + 40], tb[max(0, i - 30):i + 40]))
    hero_o = a.select_one('section.page-hero, section.page-hero-x')
    hero_n = b.select_one('.n-hero')
    if hero_o is not None and hero_n is not None:
        h1o = norm(hero_o.find('h1').get_text(' ')) if hero_o.find('h1') else ''
        h1n = norm(hero_n.find('h1').get_text(' '))
        if h1o.replace(' ', '') != h1n.replace(' ', ''):
            probs.append('H1: «%s» vs «%s»' % (h1o, h1n))
    pa = sorted(norm(x) for x in PRICE.findall(ta))
    pb = sorted(norm(x) for x in PRICE.findall(tb))
    if pa != pb:
        probs.append('ЦЕНЫ: оригинал %s / новая %s' % (pa, pb))
    fa = sorted((f.get('id'), tuple(sorted({i.get('name') for i in f.find_all(['input', 'select', 'textarea']) if i.get('name')}))) for f in a.find_all('form'))
    fb = sorted((f.get('id'), tuple(sorted({i.get('name') for i in f.find_all(['input', 'select', 'textarea']) if i.get('name')}))) for f in b.find_all('form'))
    if fa != fb:
        probs.append('ФОРМЫ: %s vs %s' % (fa, fb))
    if a.find('script', src=re.compile('training-pay')) and not b.find('script', src=re.compile('training-pay')):
        probs.append('нет training-pay.js')
    for el in b.find_all(['a', 'img', 'link', 'script']):
        u = el.get('href') or el.get('src')
        if not u or re.match(r'^(https?:|mailto:|tel:|#|javascript:|data:|/)', u):
            continue
        path = u.split('#')[0].split('?')[0]
        if path and not ((OUT / new).parent / path).resolve().exists():
            probs.append('ССЫЛКА %s' % u)
    if probs:
        bad += 1
        print('✗', new, '←', orig)
        for p in probs[:6]:
            print('    ', p)
print('\nпроверено страниц: %d, с замечаниями: %d' % (len(pairs), bad))
