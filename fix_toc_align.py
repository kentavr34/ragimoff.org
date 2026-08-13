#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fix_toc_align.py — оглавление: код и название по одной вертикали.

Кенан 2026-08-13: «в оглавлении заголовки глав и заголовки страниц — у них не
одинаковый отступ слева, и это искажает структуру».

Так и было. Строка главы и строка карточки верстались по-разному:

    заголовок главы   display:flex,  .tc-range{min-width:4.6rem}  gap .7rem
    строка карточки   display:grid,  колонка 5.4rem               gap .6rem

У flex-элемента min-width — это только нижняя граница: длинный диапазон
«6C00–6C0Z» растягивал колонку и уводил название главы вправо, а короткий
«6C20» оставлял её узкой и уводил влево. Название карточки при этом стояло
на жёстких 7 rem. Совпадения не было ни при какой длине кода.

На мобильном (≤720px) всё то же самое, но зеркально: там заголовку задали
фиксированные 5.4rem, а строке карточки — 4.6rem, и вдобавок правило зоны
нажатия WCAG (44px) переводило обе в display:flex, обнуляя grid-колонки.

Правка: у заголовка и у строки одна и та же сетка «колонка кода | название»,
одинаковый gap и одинаковый левый отступ — на обоих брейкпойнтах:

    рабочий стол   5.4rem + gap .6rem + padding-left 1rem   → название на 7.0rem
    мобильный      5.4rem + gap .5rem + padding-left .8rem  → название на 6.7rem

Колонка фиксированная, а длинный код (ICD-10 «F90.0–F90.2, F63.3 / F42.4»)
переносится внутри неё — раньше он вылезал на название.

Идемпотентен: правила ищутся по точной старой записи, второй прогон даёт 0.

    python fix_toc_align.py            # показать
    python fix_toc_align.py --apply
"""
from __future__ import annotations

import io
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).parent / 'klinik-psixiatriya'

PAIRS = [
    # ── рабочий стол ────────────────────────────────────────────────────────
    # заголовок главы: flex → та же сетка, что у строк карточек
    ('.toc-ch>a,.toc-ch .tc-head{display:flex;align-items:baseline;gap:.7rem;padding:.8rem 1rem;',
     '.toc-ch>a,.toc-ch .tc-head{display:grid;grid-template-columns:5.4rem 1fr;'
     'align-items:baseline;gap:.6rem;padding:.8rem 1rem;'),
    # колонка кода больше не растягивается содержимым — длинный код переносится
    ('.toc-ch .tc-range{color:var(--gold);font-family:var(--mono,monospace);'
     'min-width:4.6rem;font-variant-numeric:tabular-nums}',
     '.toc-ch .tc-range{color:var(--gold);font-family:var(--mono,monospace);'
     'min-width:0;white-space:normal;overflow-wrap:anywhere;font-variant-numeric:tabular-nums}'),
    ('.tc-head .tc-range{color:var(--gold);font-family:var(--mono,monospace);min-width:5rem}',
     '.tc-head .tc-range{color:var(--gold);font-family:var(--mono,monospace);'
     'min-width:0;white-space:normal;overflow-wrap:anywhere}'),
    # ── мобильный (≤720px) ──────────────────────────────────────────────────
    # правило зоны нажатия WCAG переводило обе строки в flex и гасило сетку
    ('.nav-link,.nav-sub-link,.d-nav a,.toc-ch>a,.page-toc a{min-height:44px;'
     'display:flex;align-items:center}',
     '.nav-link,.nav-sub-link,.d-nav a,.page-toc a{min-height:44px;'
     'display:flex;align-items:center}\n'
     '  .toc-ch>a{min-height:44px;display:grid;grid-template-columns:5.4rem 1fr;'
     'gap:.5rem;align-items:center}'),
    ('.tc-list>a,.toc-preview .toc-ch>a{min-height:44px;display:flex;align-items:center}',
     '.tc-list>a,.toc-preview .toc-ch>a{min-height:44px;display:grid;'
     'grid-template-columns:5.4rem 1fr;gap:.5rem;align-items:center}'),
    # ширину колонке задаёт сетка, а не сам элемент
    ('.toc-ch .tc-range{flex:0 0 5.4rem;width:5.4rem;font-size:.8rem;'
     'white-space:normal;overflow-wrap:anywhere}',
     '.toc-ch .tc-range{font-size:.8rem;white-space:normal;overflow-wrap:anywhere}'),
    # строка карточки: 4.6rem → 5.4rem, как у заголовка.
    # Заодно поднята специфичность. Селектор был `.toc-ch .tc-list a` — ровно
    # такой же, как у настольного правила ниже по файлу, и при равенстве
    # побеждало то, что позже. Мобильное правило не применялось никогда:
    # ни gap, ни размер шрифта, ни отступы. Заголовок при этом брал gap из
    # правила зоны нажатия WCAG (две категории специфичности) и уезжал влево
    # на 0,1rem. `.toc-preview` в начале селектора возвращает правилу силу.
    ('.tc-list a{font-size:.82rem;grid-template-columns:4.6rem 1fr;gap:.5rem;padding:.45rem .8rem}',
     '.toc-preview .toc-ch .tc-list a{font-size:.82rem;grid-template-columns:5.4rem 1fr;'
     'gap:.5rem;padding:.45rem .8rem}'),
    # повторный проход по уже поправленным файлам первой версии инструмента
    ('.tc-list a{font-size:.82rem;grid-template-columns:5.4rem 1fr;gap:.5rem;padding:.45rem .8rem}',
     '.toc-preview .toc-ch .tc-list a{font-size:.82rem;grid-template-columns:5.4rem 1fr;'
     'gap:.5rem;padding:.45rem .8rem}'),
    # ── единая горизонталь на обеих ширинах ────────────────────────────────
    # Блок @media стоит в файле ВЫШЕ настольных правил, поэтому при равной
    # специфичности выигрывает настольное — мобильные отступы не применялись
    # вовсе. Вместо гонки за специфичностью убираем расхождение: колонка,
    # gap и левый отступ одинаковы на любой ширине, а мобильная компактность
    # остаётся в вертикальных отступах и размере шрифта.
    ('.toc-ch>a{min-height:44px;display:grid;grid-template-columns:5.4rem 1fr;'
     'gap:.5rem;align-items:center}',
     '.toc-ch>a{min-height:44px;display:grid;grid-template-columns:5.4rem 1fr;'
     'gap:.6rem;align-items:center}'),
    ('.tc-list>a,.toc-preview .toc-ch>a{min-height:44px;display:grid;'
     'grid-template-columns:5.4rem 1fr;gap:.5rem;align-items:center}',
     '.tc-list>a,.toc-preview .toc-ch>a{min-height:44px;display:grid;'
     'grid-template-columns:5.4rem 1fr;gap:.6rem;align-items:center}'),
    ('.toc-ch>a,.toc-ch .tc-head{font-size:.84rem;padding:.65rem .8rem;gap:.5rem;'
     'align-items:flex-start}',
     '.toc-ch>a,.toc-ch .tc-head{font-size:.84rem;padding:.65rem 1rem;gap:.6rem;'
     'align-items:flex-start}'),
    ('.toc-preview .toc-ch .tc-list a{font-size:.82rem;grid-template-columns:5.4rem 1fr;'
     'gap:.5rem;padding:.45rem .8rem}',
     '.toc-preview .toc-ch .tc-list a{font-size:.82rem;grid-template-columns:5.4rem 1fr;'
     'gap:.6rem;padding:.45rem 1rem}'),
]


def main(apply: bool = False) -> int:
    files = sorted(set(list(ROOT.glob('*.html')) + list(ROOT.glob('*/*.html'))))
    touched, total = 0, 0
    for p in files:
        raw = p.read_bytes()
        crlf = raw.count(b'\r\n') > raw.count(b'\n') // 2
        t = raw.decode('utf-8', 'replace').replace('\r\n', '\n')
        n = 0
        for old, new in PAIRS:
            # Готовая запись содержит старую как хвост («.toc-preview .toc-ch
            # .tc-list a» включает «.tc-list a»), поэтому без этой проверки
            # каждый прогон дописывал бы префикс заново.
            if new in t:
                continue
            if old in t:
                n += t.count(old)
                t = t.replace(old, new)
        if n:
            touched += 1
            total += n
            if apply:
                p.write_bytes((t.replace('\n', '\r\n') if crlf else t).encode('utf-8'))
    print('файлов: {}, правок: {}'.format(touched, total))
    print('применено' if apply else 'пробный прогон — запустить с --apply')
    return 0


if __name__ == '__main__':
    raise SystemExit(main('--apply' in sys.argv))
