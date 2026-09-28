# -*- coding: utf-8 -*-
"""Аудит всех страниц книг Фрейда: издательский/переводческий мусор, пустые главы.
Ищет по абзацам и заголовкам; печатает примеры. Запуск: python _tools/check-freud-junk.py"""
import os, re, sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
BOOKS = ['freud-musa', 'freud-yuxularin-yozumu', 'freud-seksualligin-psixologiyasi',
         'freud-psixoanalizle-tanishliq', 'freud-sevgi-mektublari', 'freud-aforizmlar',
         'freud-medeniyyetin-sancilari']

PATTERNS = [
    (r'^ISBN', 'ISBN'), (r'^İSBN', 'İSBN'), (r'^©', 'копирайт'), (r'^\(c\)', '(c)'),
    (r'^Qanun Nəşriyyatı', 'издательство'), (r'Nəşriyyatı[, ]', 'издательство'),
    (r'^Bakı\b', 'адрес/город'), (r'^Tel(efon)?[:.]', 'телефон'), (r'^Mobil[:.]', 'телефон'),
    (r'^e-?mail', 'e-mail'), (r'^www\.', 'сайт'), (r'^https?://', 'ссылка'),
    (r'info@|@qanun|kitabbul', 'e-mail/водяной знак'),
    (r'facebook\.com|instagram\.com|fb\.com|t\.me/', 'соцсети'),
    (r'^Çapa imzalanmışdır', 'выходные данные'), (r'^Çapa\b', 'типография'),
    (r'^Sifariş', 'типография'), (r'^Tiraj', 'тираж'), (r'^Kağız', 'бумага'),
    (r'^Redaktor', 'редактор'), (r'^Korrektor', 'корректор'), (r'^Tərcümə\b', 'переводчик'),
    (r'^Tercümə\b', 'переводчик'), (r'^Rus dilindən tərcümə', 'переводчик'),
    (r'^MÜNDƏRİCAT$', 'печатное оглавление'), (r'^Mündəricat$', 'печатное оглавление'),
    (r'^Sigmund Freud\b', 'англ. титул'), (r'^Moses and Monotheism$', 'англ. титул'),
    (r'^Die Brautbriefe', 'нем. титул'), (r'^Introduction to Psychoanalysis$', 'англ. титул'),
    (r'^Annotasiya$', 'аннотация'), (r'^Converted Ebook$', 'водяной знак'),
    (r'^Telegram\b', 'водяной знак'), (r'^Спасибо, что скачали', 'водяной знак'),
    (r'электронной библиотек', 'водяной знак'), (r'^Оставить отзыв', 'водяной знак'),
    (r'^Перевод .{0,60}дополнен редакторскими', 'редакторская вставка'),
    (r'^Вводное примечание издателей', 'издательское примечание'),
    (r'^ЛитРес|^Скачать|^Читать$', 'магазин/ссылка'),
]
RE_P = [re.compile(p, re.I) for p, _ in PATTERNS]
RE_T = [re.compile(r'<title>([^<]*)</title>'), re.compile(r'<p>([\s\S]*?)</p>'),
        re.compile(r'<h[1-3][^>]*>([\s\S]*?)</h[1-3]>'), re.compile(r'sub-name">([^<]*)<'),
        re.compile(r'toc-name">([^<]*)<')]

total = 0
pages = 0
for slug in BOOKS:
    for base, dirs, files in os.walk(os.path.join(ROOT, 'books', slug)):
        for f in files:
            if not f.endswith('.html'):
                continue
            pages += 1
            p = os.path.join(base, f)
            h = open(p, encoding='utf-8').read()
            ru = os.sep + 'ru' + os.sep in p
            # «MÜNDƏRİCAT»/«СОДЕРЖАНИЕ» на странице-оглавлении — это наша шапка TOC, не печатный мусор
            h = re.sub(r'<h2 class="toc-title">[\s\S]*?</h2>', ' <TOC> ', h)
            for rx in RE_T:
                for m in rx.findall(h):
                    t = re.sub(r'<[^>]+>', '', m).strip()
                    t = re.sub(r'\s+', ' ', t)
                    for i, (pt, what) in enumerate(PATTERNS):
                        if ru and what in ('англ. титул', 'нем. титул', 'печатное оглавление'):
                            continue          # в русских книгах эти строки — часть текста/библиографии
                        if RE_P[i].search(t):
                            total += 1
                            if total <= 25:
                                print('  %-70s %-18s %s' % (os.path.relpath(p, ROOT), what, t[:80]))
print('страниц проверено: %d | найдено мусорных строк: %d' % (pages, total))
