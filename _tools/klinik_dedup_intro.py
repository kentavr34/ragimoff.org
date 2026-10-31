"""Klinik Psixiatriya: убрать дубли во вводной части (Кенан 31.10.2026).
1) «Müqəddimə» начиналась со встроенного оглавления из ~90 заголовков (nav.page-toc) — тот же список уже есть
   в боковом меню; на страницах болезней короткая строка разделов остаётся.
2) «Kitab haqqında» — старая отдельная редакция тем, которые есть в «Müqəddimə» (Bu kitab haqqında, Niyə XBT-11,
   struktur, istifadə qaydası, məsuliyyət, təşəkkürlər): убрана из бокового меню и карточек главной;
   страница не удалена — перенаправляет на «Müqəddimə» (старые ссылки работают).
Идемпотентно. usage: python _tools/klinik_dedup_intro.py"""
import glob
import os
import re

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'klinik-psixiatriya')
ROW = re.compile(r'[ \t]*<a class="bk-row bk-row--sub" href="kitab-haqqinda\.html">.*?</a>\n?')
CARD = re.compile(r'<a href="kitab-haqqinda\.html" class="home-card">.*?</a>')
TOC = re.compile(r'<nav class="page-toc">.*?</nav>\n?', re.S)
stat = {'rows': 0, 'cards': 0, 'toc': 0, 'redirect': 0}

for d in ['', 'ru', 'en', 'tr']:
    base = os.path.join(ROOT, d)
    for f in glob.glob(os.path.join(base, '*.html')):
        s = open(f, encoding='utf-8').read()
        n = s
        if os.path.basename(f) != 'kitab-haqqinda.html':
            n, k = ROW.subn('', n); stat['rows'] += k
        if os.path.basename(f) == 'index.html':
            n, k = CARD.subn('', n); stat['cards'] += k
        if os.path.basename(f) == 'mugeddime.html':
            n, k = TOC.subn('', n, count=1); stat['toc'] += k
        if os.path.basename(f) == 'kitab-haqqinda.html' and 'data-rd-redirect' not in n:
            n = n.replace('<head>', '<head><meta http-equiv="refresh" content="0; url=mugeddime.html" data-rd-redirect>'
                                    '<script>location.replace("mugeddime.html")</script>', 1)
            n = re.sub(r'<link rel="canonical" href="([^"]*)kitab-haqqinda\.html">', r'<link rel="canonical" href="\1mugeddime.html">', n)
            stat['redirect'] += 1
        if n != s:
            open(f, 'w', encoding='utf-8', newline='').write(n)
print(stat)
