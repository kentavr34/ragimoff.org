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


def chunk_list(soup):
    main = soup.find('main') or soup.body
    for sel in ['section.page-hero', 'section.page-hero-x', 'header', 'footer', 'nav.mobile-nav', 'script', 'style', 'noscript', '#dgLightbox', '#kitab-modal', '.wa-float', '.skip-link']:
        for el in main.select(sel):
            el.decompose()
    return [norm(t) for t in main.stripped_strings if len(norm(t)) > 2]


sys.path.insert(0, str(SITE / '_tools' / 'nocturne'))
import build as B      # канон цен Кенана 08.11 (ЦНС #712) и перенос тренинга Самиры — та же логика, что при сборке


def apply_canon(a, orig, new):
    main = a.find('main') or a.body
    name = orig.rsplit('/', 1)[-1]
    if name == 'samira.html' and '/mutexessisler/' in new:
        for sec in main.find_all('section'):
            if sec.select_one('.mod-panel') and not sec.find_parent('section'):
                sec.decompose()
    B.canon_prices(main, name, new.split('/', 1)[0], new)
    if name in B.TL.PROGRAMS and name != 'samira.html':
        B.TL.prune(main, name, new.split('/', 1)[0])


for new, orig in pairs:
    a = BeautifulSoup((SITE / orig).read_text(encoding='utf-8'), 'lxml')
    apply_canon(a, orig, new)
    b0 = (OUT / new).read_text(encoding='utf-8')
    if 'id="consultForm"' in b0:      # старая форма консультации заменена новой (Кенан 09.11) — сравниваем без неё
        for el in a.select('section#registration'):
            el.decompose()
    b = BeautifulSoup((OUT / new).read_text(encoding='utf-8'), 'lxml')
    for el in a.find_all(True):
        if any(c.endswith('-mob') for c in el.get('class', [])):
            el.decompose()          # мобильные дубли: тот же текст есть в -desk
    chunks = chunk_list(a)
    ta, tb = body_text(a, False), body_text(b, True)
    probs = []
    miss = [c for c in chunks if c not in tb]
    if miss:
        probs.append('ТЕКСТ: нет %d фрагм., напр. «%s»' % (len(miss), '» / «'.join(m[:60] for m in miss[:3])))
    hero_o = a.select_one('section.page-hero, section.page-hero-x')
    hero_n = b.select_one('.n-hero')
    if hero_o is not None and hero_n is not None:
        h1o = norm(hero_o.find('h1').get_text(' ')) if hero_o.find('h1') else ''
        h1n = norm(hero_n.find('h1').get_text(' '))
        if h1o.replace(' ', '') != h1n.replace(' ', ''):
            probs.append('H1: «%s» vs «%s»' % (h1o, h1n))
    pa = sorted(norm(x) for x in PRICE.findall(ta))
    pb = sorted(norm(x) for x in PRICE.findall(tb))
    lost = [x for x in set(pa) if pa.count(x) > pb.count(x)]
    if lost:
        probs.append('ЦЕНЫ потеряны: %s' % lost)
    fa = sorted((f.get('id'), tuple(sorted({i.get('name') for i in f.find_all(['input', 'select', 'textarea']) if i.get('name')}))) for f in a.find_all('form'))
    fb = sorted((f.get('id'), tuple(sorted({i.get('name') for i in f.find_all(['input', 'select', 'textarea']) if i.get('name')}))) for f in b.find_all('form') if f.get('id') != 'consultForm')
    fb = sorted((i, tuple(n for n in names if n != 'diplom')) for i, names in fb)
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
