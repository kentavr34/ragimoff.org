# -*- coding: utf-8 -*-
"""Разбивает длинные заголовки разделов на строки почти равной длины.

Зачем. Правило владельца: заголовок и подзаголовок раздела выровнены по
ширине, поля слева и справа одинаковы на всех страницах. В шапке это
работает, потому что заголовок там разбит на строки вручную
(.ph-h1-w1 / .ph-h1-w2) и каждая строка подгоняется отдельно. У разделов
разбивки нет: заголовок переносится сам, его ширина оказывается шириной
длиннейшей строки, и пара не сходится — две попытки свести её алгоритмом
дали 8 пар из 24 против 9 без правок.

Что делает. Заголовок длиннее порога делится по пробелу, ближайшему к
середине по числу знаков, и обе половины оборачиваются в
<span class="sh-line">. Дальше их равняет тот же механизм, что и в шапке.

Чего НЕ делает. Не трогает заголовки короче порога — они и так встают в
строку. Не переносит одиночное слово: строка из одного слова не
выравнивается, а только сужает блок. Не меняет текст — только расставляет
переносы.

    python split_headings.py            # сухой прогон
    python split_headings.py --apply
"""
import io
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).parent
APPLY = '--apply' in sys.argv
TREES = [ROOT, ROOT / 'ru', ROOT / 'en']

H2 = re.compile(r'(<h2 class="sec-h2"[^>]*>)(.*?)(</h2>)', re.S)
MIN_CHARS = 15          # ниже этого заголовок и так встаёт в строку
MIN_WORDS = 2           # два длинных слова тоже делятся: «Samirə / Rəhimova»


def split_text(s):
    """Делит по пробелу, ближайшему к середине по числу знаков.

    По слэшу НЕ делим: «Samirə Rəhimova/» с висящим слэшем на конце строки
    читается как обрыв слова, а не как перечисление двух фамилий.
    """
    words = s.split()
    if len(words) < MIN_WORDS:
        return None
    total = len(s)
    best, best_diff = None, None
    acc = 0
    for i, w in enumerate(words[:-1]):
        acc += len(w) + 1
        diff = abs(acc - (total - acc))
        if best_diff is None or diff < best_diff:
            best, best_diff = i + 1, diff
    if best is None:
        return None
    left = ' '.join(words[:best])
    right = ' '.join(words[best:])
    if not left or not right:
        return None
    return left, right


stat = {'pages': 0, 'split': 0, 'skipped_short': 0, 'skipped_words': 0}
for tree in TREES:
    if not tree.exists():
        continue
    for p in sorted(tree.glob('*.html')):
        raw = p.read_bytes()
        crlf = raw.count(b'\r\n') > raw.count(b'\n') // 2
        t = raw.decode('utf-8').replace('\r\n', '\n')
        touched = 0

        def repl(m):
            global touched
            head, body, tail = m.group(1), m.group(2), m.group(3)
            if 'sh-line' in body:
                return m.group(0)                 # уже разбит
            plain = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', body)).strip()
            if len(plain) < MIN_CHARS:
                stat['skipped_short'] += 1
                return m.group(0)
            if re.search(r'<(?!/?(strong|em|b|i|span)\b)[^>]+>', body):
                return m.group(0)                 # внутри разметка сложнее строки
            parts = split_text(plain)
            if not parts:
                stat['skipped_words'] += 1
                return m.group(0)
            touched += 1
            stat['split'] += 1
            return '%s<span class="sh-line">%s</span> <span class="sh-line">%s</span>%s' % (
                head, parts[0], parts[1], tail)

        new = H2.sub(repl, t)
        if touched:
            stat['pages'] += 1
            if APPLY:
                p.write_bytes((new.replace('\n', '\r\n') if crlf else new).encode('utf-8'))

print('страниц: %d · заголовков разбито: %d' % (stat['pages'], stat['split']))
print('пропущено: коротких %d, из двух слов %d' % (stat['skipped_short'], stat['skipped_words']))
print('ПРИМЕНЕНО' if APPLY else 'сухой прогон — запустить с --apply')
