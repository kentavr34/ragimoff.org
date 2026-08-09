#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_code_table.py — трёхъязычная таблица кодов МКБ-11 в переводах.

Таблица «Psixi pozuntular» устроена так: Kod | Azərbaycanca (на сайте) |
English (ICD-11) | Русский (МКБ-11). Три языковые колонки — это её смысл:
читатель сверяет, как одно и то же расстройство названо в трёх изданиях.
Заголовки колонок это прямо и говорят, на каждом языке.

Что нашлось 2026-08-09: в русском, английском и турецком изданиях все три
колонки перевели на язык читателя. Сравнивать стало не с чем — в
английском издании колонка «Russian (ICD-11)» содержит английский текст.
Хуже того, набор строк там остался старый, до разбиения книги на карточки:
89 строк против 103, и коды разъехались с названиями —

    6A70 «Биполярное расстройство I типа»   (6A70 — депрессивный эпизод)
    6A71 «Биполярное расстройство II типа»  (6A71 — рекуррентная депрессия)
    6B83 «Расстройство руминации»           (6B83 — ARFID)
    6B84 «ARFID»                            (6B84 — пика)

Азербайджанская таблица верна: её 103 кода совпадают с карточками книги.
Инструмент переносит её строки в три перевода, оставляя каждому изданию
свою шапку и свою подпись кнопки правки.

    python fix_code_table.py            # отчёт
    python fix_code_table.py --apply
"""
from __future__ import annotations
import re, sys, io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).parent
BOOK = ROOT / 'klinik-psixiatriya'
PAGES = ('abbreviatur.html', 'terminoloji-luget.html')
APPLY = '--apply' in sys.argv
BTN = {'ru': 'Исправить', 'en': 'Correct', 'tr': 'Düzelt'}
TABLE = re.compile(r'<table[\s\S]*?</table>')


def code_table(html: str):
    """Таблица, у которой есть колонка кода и больше 50 строк."""
    for m in TABLE.finditer(html):
        if 'kod-cell' in m.group(0) and len(re.findall(r'<tr>', m.group(0))) > 50:
            return m
    return None


def main() -> int:
    src = code_table((BOOK / 'abbreviatur.html').read_text(encoding='utf-8', errors='ignore'))
    if not src:
        print('азербайджанская таблица не найдена')
        return 1
    rows = re.findall(r'<tr>[\s\S]*?</tr>', src.group(0))[1:]
    print(f'эталон: {len(rows)} строк из азербайджанского издания')

    for lg in ('ru', 'en', 'tr'):
        for page in PAGES:
            fp = BOOK / lg / page
            if not fp.exists():
                continue
            raw = fp.read_bytes().decode('utf-8')
            crlf = raw.count('\r\n') > raw.count('\n') // 2
            t = raw.replace('\r\n', '\n')
            tb = code_table(t)
            if not tb:
                print(f'  {lg}/{page}: таблица не найдена')
                continue
            body = tb.group(0)
            old = re.findall(r'<tr>[\s\S]*?</tr>', body)
            header = old[0]
            # подпись кнопки — своя в каждом издании
            new_rows = [re.sub(r'(✎\s*)[^<]*(</button>)', r'\g<1>' + BTN[lg] + r'\2', r)
                        for r in rows]
            new = body[:body.index(old[0])] + header + ''.join(new_rows) \
                + body[body.rindex(old[-1]) + len(old[-1]):]
            print(f'  {lg}/{page}: {len(old) - 1} → {len(new_rows)} строк')
            if APPLY:
                t = t[:tb.start()] + new + t[tb.end():]
                fp.write_bytes((t.replace('\n', '\r\n') if crlf else t).encode('utf-8'))
    print('применено' if APPLY else 'пробный прогон — запустить с --apply')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
