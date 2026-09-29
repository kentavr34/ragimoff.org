# -*- coding: utf-8 -*-
"""Сверка AZ↔RU по книгам Фрейда: главы, письма, лекции. Запуск: python _tools/report-freud-az-ru.py"""
import os, re, sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOKS = ['freud-yuxularin-yozumu', 'freud-musa', 'freud-seksualligin-psixologiyasi',
         'freud-psixoanalizle-tanishliq', 'freud-sevgi-mektublari',
         'freud-totem-ve-tabu', 'freud-medeniyyetin-sancilari']

def toc(path):
    if not os.path.exists(path):
        return []
    h = open(path, encoding='utf-8').read()
    return re.findall(r'toc-name">([^<]*)</span>', h)

def paras(path):
    if not os.path.exists(path):
        return 0
    h = open(path, encoding='utf-8').read()
    return len(re.findall(r'<p>', h))

for slug in BOOKS:
    az_dir = os.path.join(ROOT, 'books', slug)
    ru_dir = os.path.join(az_dir, 'ru')
    az, ru = toc(os.path.join(az_dir, 'index.html')), toc(os.path.join(ru_dir, 'index.html'))
    az_pages = len([f for f in os.listdir(az_dir) if re.match(r'^\d{2}-', f)])
    ru_pages = len([d for d in os.listdir(ru_dir) if os.path.isdir(os.path.join(ru_dir, d))]) if os.path.isdir(ru_dir) else 0
    print('== %s: AZ глав %d (страниц %d) | RU глав %d (папок %d)' % (slug, len(az), az_pages, len(ru), ru_pages))
    print('   AZ: %s' % ' / '.join(az[:6]) + (' …' if len(az) > 6 else ''))
    if ru:
        print('   RU: %s' % ' / '.join(ru[:6]) + (' …' if len(ru) > 6 else ''))
