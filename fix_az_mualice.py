# -*- coding: utf-8 -*-
"""Единая структура раздела «Müalicə» в азербайджанском дереве.

Как было. В §8 жили три блока об одном и том же: «8.1 Ümumi prinsiplər»
перечисляла линии терапии, отдельный блок «Müalicə metodikaları» без
номера повторял те же методы подробнее, «Mənbə-spesifik dəqiqləşdirmələr»
стояла между ними и обрывала мысль. Читатель проходил КДТ дважды и не
понимал, где основной текст, а где уточнение.

Как стало. Один порядок на все карточки:
    8.1 …               общие принципы и линии терапии (как было)
    8.2 …               прочие содержательные подразделы карточки
    8.N Müalicə metodikaları        — методы подробно, ПОСЛЕ линий
    8.N+1 Mənbələr arasında fərqlər — расхождения источников, последними
Нумерация сквозная: подраздел без номера в нумерованном разделе выглядит
как чужой кусок.

Скрипт не переписывает содержание — он расставляет части в единый порядок
и нумерует. Содержательное слияние повторов делается чтением, карточка за
карточкой; здесь задаётся каркас, в котором повтор становится виден.

    python fix_az_mualice.py            # сухой прогон
    python fix_az_mualice.py --apply
"""
import io
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).parent / 'klinik-psixiatriya'
APPLY = '--apply' in sys.argv

H3 = re.compile(r'<h3[^>]*>(.*?)</h3>', re.S)
NUM = re.compile(r'^\s*8\.\d+\s*')
METOD = 'Müalicə metodikaları'
MENBE = 'Mənbə-spesifik dəqiqləşdirmələr'
MENBE_NEW = 'Mənbələr arasında fərqlər'


def split_blocks(chunk):
    """Раскладывает §8 на вступление и блоки, начинающиеся с <h3>."""
    marks = [m.start() for m in H3.finditer(chunk)]
    if not marks:
        return chunk, []
    head = chunk[:marks[0]]
    blocks = []
    for a, b in zip(marks, marks[1:] + [len(chunk)]):
        blocks.append(chunk[a:b])
    return head, blocks


def title_of(block):
    m = H3.search(block)
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', m.group(1))).strip() if m else ''


def rebuild(chunk):
    head, blocks = split_blocks(chunk)
    if not blocks:
        return chunk, 0
    main, metod, menbe = [], [], []
    for b in blocks:
        t = title_of(b)
        if METOD in t:
            metod.append(b)
        elif MENBE in t or MENBE_NEW in t:
            menbe.append(b)
        else:
            main.append(b)
    ordered = main + metod + menbe
    if not ordered:
        return chunk, 0

    changed = 0
    out = []
    for i, b in enumerate(ordered, 1):
        t = title_of(b)
        bare = NUM.sub('', t).strip()
        if MENBE in bare:
            bare = MENBE_NEW          # «уточнения по источнику» → «различия между источниками»
        want = '8.%d %s' % (i, bare)
        if t != want:
            changed += 1
            b = H3.sub(lambda m, w=want: '<h3>%s</h3>' % w, b, count=1)
        out.append(b)
    return head + ''.join(out), changed


total_cards = total_h3 = 0
moved = 0
for p in sorted(ROOT.glob('*.html')):
    raw = p.read_bytes()
    crlf = raw.count(b'\r\n') > raw.count(b'\n') // 2
    t = raw.decode('utf-8').replace('\r\n', '\n')
    m8 = re.search(r'<h2 id="[^"]*-8-[^"]*"', t)
    if not m8:
        continue
    i = m8.start()
    m9 = re.search(r'<h2 id="[^"]*-9-[^"]*"', t[i:])
    j = i + m9.start() if m9 else len(t)
    chunk = t[i:j]
    new, changed = rebuild(chunk)
    if new != chunk:
        total_cards += 1
        total_h3 += changed
        if METOD in chunk and chunk.find(METOD) < chunk.find(MENBE) if MENBE in chunk else False:
            pass
        if APPLY:
            t = t[:i] + new + t[j:]
            p.write_bytes((t.replace('\n', '\r\n') if crlf else t).encode('utf-8'))

print('карточек затронуто: %d · заголовков перенумеровано: %d' % (total_cards, total_h3))
print('ПРИМЕНЕНО' if APPLY else 'сухой прогон — запустить с --apply')
