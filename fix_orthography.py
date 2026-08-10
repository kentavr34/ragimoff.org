#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_orthography.py — орфографические решения владельца, зафиксированные 2026-08-10.

Книга годами держала обе формы пяти терминов сразу, и читатель видел разные
написания на соседних страницах. Кенан выбрал по каждому паре одну форму,
разную для азербайджанского и турецкого:

  1. depressiv  — азербайджанский пишет двойное s (depressiv, depressiya,
     antidepressant); турецкий остаётся при своём depresif с одним s.
  2. apnoe      — азербайджанский apnoe/apnoesi; турецкий apne/apnesi.
  3. -ergik     — азербайджанский суффикс -ergik (dopaminergik, GABA-ergik);
     турецкий -erjik.
  4. DDHP/PTSP  — в азербайджанском тексте азербайджанские аббревиатуры,
     в английском ADHD/PTSD. По той же логике русский текст получает
     СДВГ/ПТСР, турецкий — DEHB/TSSB.
  5. 6B82       — AŞIRI QİDALANMA POZUNTUSU (правится в _build_abbreviatur.py,
     канон уже держит это имя).

Пункт 4 нельзя делать слепой заменой: ADHD и PTSD входят в английские имена
шкал, руководств и источников — «Adult ADHD Self-Report Scale», «PTSD
Checklist», «Canadian ADHD Practice Guidelines», строка DSM в шапке карточки.
Там аббревиатура английская по праву. Поэтому каждое вхождение решается по
окружению: рядом английское слово-маркер — не трогаем.

Инструмент идемпотентен: целевые формы не содержат исходных подстрок.

    python fix_orthography.py            # разбор, ничего не пишет
    python fix_orthography.py --apply
"""
from __future__ import annotations
import re, sys, io
from pathlib import Path
from collections import Counter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).parent
BOOK = ROOT / 'klinik-psixiatriya'
DIRS = {'az': BOOK, 'ru': BOOK / 'ru', 'en': BOOK / 'en', 'tr': BOOK / 'tr'}
APPLY = '--apply' in sys.argv

# ── 1–3: простые пары «было → стало», по языкам ─────────────────────────────
# Порядок важен: длинные формы раньше коротких.
PLAIN: dict[str, list[tuple[str, str]]] = {
    'az': [
        # 1. двойное s
        ('ANTİDEPRESANT', 'ANTİDEPRESSANT'), ('Antidepresant', 'Antidepressant'),
        ('antidepresant', 'antidepressant'),
        ('DEPRESİYA', 'DEPRESSİYA'), ('Depresiya', 'Depressiya'), ('depresiya', 'depressiya'),
        ('DEPRESİV', 'DEPRESSİV'), ('Depresiv', 'Depressiv'), ('depresiv', 'depressiv'),
        # 2. apnoe (apnea/apnoea — английские имена, не трогаем)
        ('hipopnesi', 'hipopnoesi'), ('apnesində', 'apnoesində'),
        ('apnesi', 'apnoesi'), ('apneda', 'apnoedə'),
        # 3. -ergik
        ('erjik', 'ergik'),
    ],
    # турецкий уже держит depresif, apne и -erjik — правок не нужно
    'tr': [],
    'ru': [],
    'en': [],
}

# ── 4: аббревиатуры, зависящие от окружения ─────────────────────────────────
ABBR = {
    'az': {'ADHD': 'DDHP', 'PTSD': 'PTSP'},
    'ru': {'ADHD': 'СДВГ', 'PTSD': 'ПТСР'},
    'tr': {'ADHD': 'DEHB', 'PTSD': 'TSSB'},
    'en': {},
}
# Решает СОСЕДНЕЕ слово, а не окно: «Adult ADHD Self-Report Scale» — имя шкалы,
# а «Komorbidlik skrininq (ADHD, autizm)» — азербайджанская проза, даже если
# двумя словами раньше стояло английское «Interview». Окно в 45 символов на
# этом и ошибалось, защищая прозу по случайному соседству.
# «Stress» намеренно не в списке: азербайджанское «Posttravmatik Stress
# Pozuntusu» пишется так же и увело бы защиту не туда.
ENG_LEFT = {
    'Adult', 'Canadian', 'Vanderbilt', 'Complex', 'complex', 'ENIGMA',
    'Administered', 'Clinician-Administered', 'Disorder', 'disorder', 'DBT',
    'ISTSS', 'proposed', 'Treatment', 'Prolonged', 'Processing', 'Exposure',
    'of', 'for', 'with', 'in', 'and', 'the', 'on', 'to', 'about',
}
ENG_RIGHT = {
    'Scale', 'Checklist', 'Guideline', 'Guidelines', 'Rating', 'Diagnostic',
    'Practice', 'Resource', 'Alliance', 'Self-Report', 'Treatment',
    'Prevention', 'Study', 'Symptoms', 'Psychol', 'Oxford', 'Research',
    'symptoms', 'in', 'and', 'a', 'of', 'for', 'with', 'the', 'adults',
    'children', 'severity', 'versus',
}
# «DSM-5-TR: F90.0–F90.2x ADHD» — ярлык классификации, аббревиатура английская
CODE = re.compile(r'^[A-Z]{1,4}\d[\w.–/-]*$')
LEFT_W = re.compile(r'([\w./–-]+)[^\w]*$')
RIGHT_W = re.compile(r'^[^\w]*([\w./–-]+)')
TAG = re.compile(r'<[^>]*>')


def _neighbour(s: str, rx: re.Pattern) -> str:
    m = rx.search(TAG.sub(' ', s))
    return m.group(1).strip('-./–') if m else ''


QUOTED = ('«»', '„“', '““', '“”', '""')
# Страницы-расшифровщики: там левая колонка — сама латинская аббревиатура,
# и заменить её значит лишить строку смысла («СДВГ — синдром дефицита…»).
REGISTRY = {'abbreviatur', 'terminoloji-luget'}


def english_here(text: str, i: int, j: int) -> bool:
    """Стоит ли вхождение внутри английского имени — по соседнему слову."""
    # «ADHD» в кавычках — цитата термина: «DSM-IV (1994) — термин "ADHD"».
    # Заменить значило бы приписать DSM-IV азербайджанскую аббревиатуру.
    if any(text[i - 1:i] == q[0] and text[j:j + 1] == q[1] for q in QUOTED):
        return True
    # «СДВГ (ADHD)» — скобка расшифровывает уже переведённую аббревиатуру;
    # замена дала бы «СДВГ (СДВГ)».
    if text[i - 1:i] == '(' and text[j:j + 1] == ')':
        return True
    left = _neighbour(text[max(0, i - 60):i], LEFT_W)
    right = _neighbour(text[j:j + 60], RIGHT_W)
    return left in ENG_LEFT or CODE.match(left) is not None or right in ENG_RIGHT


def process(text: str, lg: str, stem: str, stat: Counter, keep: Counter) -> str:
    for a, b in PLAIN[lg]:
        n = text.count(a)
        if n:
            stat[f'{a} → {b}'] += n
            text = text.replace(a, b)
    if stem in REGISTRY:
        return text
    # <meta> не трогаем: ключевые слова для поиска пишутся в международной
    # форме — человек ищет «PTSD», а не «PTSP».
    meta = [(m.start(), m.end()) for m in re.finditer(r'<meta[^>]*>', text)]
    for a, b in ABBR[lg].items():
        out, pos = [], 0
        for m in re.finditer(r'\b' + a + r'\b', text):
            out.append(text[pos:m.start()])
            if any(s <= m.start() < e for s, e in meta):
                out.append(a)
                keep[f'{lg}/{a} в <meta>'] += 1
            elif english_here(text, m.start(), m.end()):
                out.append(a)
                keep[f'{lg}/{a} в английском имени'] += 1
            else:
                out.append(b)
                stat[f'{a} → {b}'] += 1
            pos = m.end()
        out.append(text[pos:])
        text = ''.join(out)
    return text


def main() -> int:
    total = 0
    for lg, folder in DIRS.items():
        if not folder.is_dir():
            continue
        stat, keep, files = Counter(), Counter(), 0
        for fp in sorted(folder.glob('*.html')):
            raw = fp.read_bytes().decode('utf-8')
            crlf = raw.count('\r\n') > raw.count('\n') // 2
            t = raw.replace('\r\n', '\n')
            new = process(t, lg, fp.stem, stat, keep)
            if new == t:
                continue
            files += 1
            if APPLY:
                fp.write_bytes((new.replace('\n', '\r\n') if crlf else new).encode('utf-8'))
        if stat or keep:
            print(f'  {lg}: файлов {files}')
            for k, v in stat.most_common():
                print(f'      {k:34} ×{v}')
            for k, v in keep.most_common():
                print(f'      оставлено английским: {k:14} ×{v}')
            total += sum(stat.values())
    print(f'\nзамен {total}')
    print('применено' if APPLY else 'пробный прогон — запустить с --apply')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
