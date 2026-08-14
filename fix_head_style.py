#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fix_head_style.py — две шапки: оглавления и карточки расстройства.

Кенан 2026-08-14: «стиль оформления заголовков — не очень, всё равно
искажается»; «код диагноза мелким шрифтом, не выравнен по середине ячейки».

**Оглавление.** После выравнивания колонка кода стала ровно 5.4rem — и этого
не хватило: замер в браузере показал, что диапазон вида «6A60–6A7Z» требует
106 px, то есть переносился на две строки. Переносились 20 заголовков глав
из 23, строка распухала вдвое, и вместо порядка получался разнобой.

Ширина нужна разная, потому что классификации разные: у МКБ-11 самый длинный
код 106 px, у DSM-раздела — 155 px («F01–F05 · G30–G31»), у МКБ-10 — 102 px.
Панели помечены `data-cls`, поэтому каждой задаётся своя `--tc-col`, а сетка
берёт её через переменную. Заголовок главы и строка карточки внутри одной
панели пользуются одним значением — вертикаль сохраняется.

**Шапка карточки.** Код диагноза стоял тем же кеглем, что и ярлык над ним
(.74rem), и прижимался к базовой линии соседнего заголовка, а не к середине
ячейки. Ярлыки разной длины («XBT-11» против «DSM-5-TR») при выравнивании
влево давали рваный правый край. Теперь: код крупнее ярлыка, столбик
выровнен по центру и по вертикали середины ячейки.

Идемпотентен: правила ищутся по точной старой записи, второй прогон даёт 0.

    python fix_head_style.py            # показать
    python fix_head_style.py --apply
"""
from __future__ import annotations

import io
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).parent / 'klinik-psixiatriya'

# ширины замерены в браузере: самый длинный код каждой классификации + запас
VARS = ('.toc-ch{--tc-col:5.4rem}'
        '.cls-panel[data-cls="icd"] .toc-ch{--tc-col:7rem}'
        '.cls-panel[data-cls="dsm"] .toc-ch{--tc-col:10.1rem}'
        '.cls-panel[data-cls="icd10"] .toc-ch{--tc-col:6.8rem}')

PAIRS = [
    # ── оглавление: ширина колонки кода — своя у каждой классификации ──────
    ('.toc-ch>a,.toc-ch .tc-head{display:grid;grid-template-columns:5.4rem 1fr;'
     'align-items:baseline;gap:.6rem;padding:.8rem 1rem;',
     VARS + '.toc-ch>a,.toc-ch .tc-head{display:grid;grid-template-columns:var(--tc-col) 1fr;'
     'align-items:baseline;gap:.6rem;padding:.8rem 1rem;'),
    ('.toc-ch .tc-list a{display:grid;grid-template-columns:5.4rem 1fr',
     '.toc-ch .tc-list a{display:grid;grid-template-columns:var(--tc-col) 1fr'),
    ('.toc-ch>a{min-height:44px;display:grid;grid-template-columns:5.4rem 1fr;'
     'gap:.6rem;align-items:center}',
     '.toc-ch>a{min-height:44px;display:grid;grid-template-columns:var(--tc-col) 1fr;'
     'gap:.6rem;align-items:center}'),
    ('.tc-list>a,.toc-preview .toc-ch>a{min-height:44px;display:grid;'
     'grid-template-columns:5.4rem 1fr;gap:.6rem;align-items:center}',
     '.tc-list>a,.toc-preview .toc-ch>a{min-height:44px;display:grid;'
     'grid-template-columns:var(--tc-col) 1fr;gap:.6rem;align-items:center}'),
    ('.toc-preview .toc-ch .tc-list a{font-size:.82rem;grid-template-columns:5.4rem 1fr;'
     'gap:.6rem;padding:.45rem 1rem}',
     '.toc-preview .toc-ch .tc-list a{font-size:.82rem;grid-template-columns:var(--tc-col) 1fr;'
     'gap:.6rem;padding:.45rem 1rem}'),
    # ── шапка карточки: три колонки — ярлык | код | название ───────────────
    # Ярлык и код стояли стопкой в одной ячейке. Длина у них разная, кегль
    # разный — при выравнивании влево, по центру и вправо край одинаково
    # оставался рваным: это лесенка, а не колонка. Решение Кенана 2026-08-14:
    # у ярлыка и у кода своя вертикаль, строка классификации — одна строка.
    # Разметку выдаёт build_headers.py, он переведён на три ячейки там же.
    ('table.dh .dh-meta{white-space:nowrap;vertical-align:baseline;padding:.24rem .9rem .24rem 0}',
     'table.dh .dh-lbl-c{white-space:nowrap;vertical-align:baseline;text-align:left;'
     'padding:.24rem .8rem .24rem 0}'
     'table.dh .dh-code-c{white-space:nowrap;vertical-align:baseline;text-align:left;'
     'padding:.24rem .9rem .24rem 0}'),
    ('table.dh .dh-meta{white-space:nowrap;vertical-align:middle;text-align:center;'
     'padding:.24rem .9rem .24rem 0}',
     'table.dh .dh-lbl-c{white-space:nowrap;vertical-align:baseline;text-align:left;'
     'padding:.24rem .8rem .24rem 0}'
     'table.dh .dh-code-c{white-space:nowrap;vertical-align:baseline;text-align:left;'
     'padding:.24rem .9rem .24rem 0}'),
    ('table.dh .dh-lbl{display:block;', 'table.dh .dh-lbl{display:inline-block;'),
    ('table.dh .dh-meta{padding-right:.7rem}',
     'table.dh .dh-lbl-c{padding-right:.6rem}table.dh .dh-code-c{padding-right:.7rem}'),
    ('table.dh .dh-code{display:block;font-family:var(--mono,monospace);font-weight:700;'
     'color:var(--gold);font-size:.74rem;line-height:1.25;margin-top:.1rem}',
     'table.dh .dh-code{display:inline-block;font-family:var(--mono,monospace);font-weight:700;'
     'color:var(--gold);font-size:.95rem;line-height:1.2;margin-top:0}'),
    ('table.dh .dh-code{display:block;font-family:var(--mono,monospace);font-weight:700;'
     'color:var(--gold);font-size:.95rem;line-height:1.2;margin-top:.06rem}',
     'table.dh .dh-code{display:inline-block;font-family:var(--mono,monospace);font-weight:700;'
     'color:var(--gold);font-size:.95rem;line-height:1.2;margin-top:0}'),
    ('table.dh .dh-lbl,table.dh .dh-code{font-size:.72rem}',
     'table.dh .dh-lbl{font-size:.7rem}table.dh .dh-code{font-size:.86rem}'),
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
