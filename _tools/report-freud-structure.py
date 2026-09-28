# -*- coding: utf-8 -*-
"""Таблица-доказательство «стр. PDF — как напечатано — что стоит на сайте».
Читает построенные оглавления книг и печатные PDF; печатает строки таблицы.
Запуск: python _tools/report-freud-structure.py [slug]"""
import os, re, sys
import pymupdf

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDFDIR = 'D:/Документы/ZFreud/azerbaycan_freud/books/'

BOOKS = [
    ('freud-musa', 'Musa və təkallahlılıq.pdf'),
    ('freud-yuxularin-yozumu', 'Yuxuların yozumu.pdf'),
    ('freud-seksualligin-psixologiyasi', 'Seksuallığın psixologiyası.pdf'),
    ('freud-psixoanalizle-tanishliq', 'Psixoanalizlə ilkin tanışlıq.pdf'),
    ('freud-sevgi-mektublari', 'Sevgi məktubları.pdf'),
]

FOLD = str.maketrans({'İ': 'i', 'I': 'i', 'ı': 'i', 'Ə': 'e', 'ə': 'e', 'Ö': 'o', 'ö': 'o',
                      'Ü': 'u', 'ü': 'u', 'Ç': 'c', 'ç': 'c', 'Ş': 's', 'ş': 's', 'Ğ': 'g', 'ğ': 'g',
                      'Ё': 'е', 'ё': 'е'})

ROMAN = re.compile(r'^((I|II|III|IV|V|VI|VII|VIII|IX|X)[.)]?|\d{1,2}[.)])\s+', re.I)

def key(s):
    s = ROMAN.sub('', s.strip())
    s = s.translate(FOLD).lower()
    s = re.sub(r'(?<=[a-z])\d+', '', s)        # OCR-огрехи вида «Narsisizm9»
    return re.sub(r'\s+', ' ', re.sub(r"[’'«»\"`.,:;!?()\[\]{}—–\-]", ' ', s)).strip()

def pdf_lines(doc):
    """все строки PDF с номером страницы"""
    out = []
    for pno in range(doc.page_count):
        for blk in doc[pno].get_text('dict')['blocks']:
            if blk.get('type') != 0:
                continue
            for ln in blk['lines']:
                t = ''.join(sp['text'] for sp in ln['spans']).strip()
                if t:
                    out.append((pno + 1, re.sub(r'\s+', ' ', t)))
    return out

only = sys.argv[1] if len(sys.argv) > 1 else None
seen = set()
for slug, pdf in BOOKS:
    if slug in seen or (only and slug != only):
        continue
    seen.add(slug)
    index = open(os.path.join(ROOT, 'books', slug, 'index.html'), encoding='utf-8').read()
    toc = re.findall(r'toc-name">([^<]*)</span>', index)
    doc = pymupdf.open(PDFDIR + pdf)
    lines = pdf_lines(doc)
    print('\n### %s  (%s)' % (slug, pdf))
    for t in toc:
        k = key(t)
        page, printed, exact = '?', '', False
        best = ('', -1, '')                       # (текст, длина ключа, страница)
        for pno, txt in lines:
            kt = key(txt)
            if kt == k:
                page, printed, exact = pno, txt, True
                break
            if len(txt) < 90 and len(kt) >= 10:
                if k.startswith(kt) and len(kt) > best[1]:
                    best = (txt, len(kt), pno)
                elif kt.startswith(k) and len(k) > best[1]:
                    best = (txt, len(k), pno)
        if not exact and best[1] > 0:
            printed, page = best[0], best[2]
        print('  стр.%-5s %s | %-76s | %s' % (page, '' if exact else '~', (printed or '—')[:76], t[:76]))
    doc.close()
