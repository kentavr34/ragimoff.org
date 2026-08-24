# -*- coding: utf-8 -*-
"""Возвращает разделам единый вертикальный ритм.

Правило владельца: «отступ сверху над кнопкой, от кнопки до заголовка, от
заголовка до подзаголовка — одна и та же единица на всех страницах, тогда
страницы выглядят клонами».

Ритм задан переменными в gtc.css и работает сам:

    бейдж → заголовок      --s-gap-tag-hero   30px
    заголовок → подзаголовок --s-gap-title     16px
    подзаголовок → контент   --s-gap-sub       30px

Но 71 раздел перебил его вручную: заголовки с margin-bottom:8px и
margin-top:16px, бейджи с margin-bottom:16px или 20px. Каждый такой
inline-стиль сильнее переменной, поэтому разделы стояли с разным шагом,
и разница видна при переходе между страницами.

Скрипт убирает из inline-стиля ТОЛЬКО вертикальные margin у трёх классов.
Всё остальное в том же атрибуте остаётся: text-align:left у описаний
(это не подзаголовок, у него своя раскладка), color, display.

    python fix_rhythm.py              # сухой прогон
    python fix_rhythm.py --apply
"""
import io
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).parent
APPLY = '--apply' in sys.argv
TREES = [ROOT, ROOT / 'ru', ROOT / 'en']

TAG = re.compile(
    r'<(?P<tag>\w+)(?P<pre>[^>]*\bclass="(?:badge|sec-h2|sec-sub|svc-h2|svc-sub)[^"]*"[^>]*)>')
MARGIN = re.compile(r'\s*margin-(?:top|bottom)\s*:\s*[^;"]+;?', re.I)


def clean_style(m):
    pre = m.group('pre')
    sm = re.search(r'\bstyle="([^"]*)"', pre)
    if not sm or not MARGIN.search(sm.group(1)):
        return m.group(0)
    rest = MARGIN.sub('', sm.group(1)).strip().strip(';')
    new = pre[:sm.start()] + (' style="%s"' % rest if rest else '') + pre[sm.end():]
    new = re.sub(r'\s+', ' ', new).rstrip()
    clean_style.n += 1
    return '<%s%s>' % (m.group('tag'), (' ' + new.lstrip()) if new.strip() else '')


clean_style.n = 0
pages = 0
for tree in TREES:
    if not tree.exists():
        continue
    for p in sorted(tree.glob('*.html')):
        raw = p.read_bytes()
        crlf = raw.count(b'\r\n') > raw.count(b'\n') // 2
        t = raw.decode('utf-8').replace('\r\n', '\n')
        before = clean_style.n
        new = TAG.sub(clean_style, t)
        if clean_style.n > before:
            pages += 1
            if APPLY:
                p.write_bytes((new.replace('\n', '\r\n') if crlf else new).encode('utf-8'))

print('страниц: %d · снято ручных отступов: %d' % (pages, clean_style.n))
print('ПРИМЕНЕНО' if APPLY else 'сухой прогон — запустить с --apply')
