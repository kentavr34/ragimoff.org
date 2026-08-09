#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
remove_duzelis.py — снимает виджет «Düzəliş et» со страниц книги.

Виджет состоял из двух частей:
  * плавающая кнопка внизу страницы — её рисует duzelis.js, подключённый
    в <head> блоком <!-- DUZELIS-WIDGET -->;
  * колонка «Düzəlt» с кнопкой ✎ в каждой строке справочных таблиц
    (abbreviatur и terminoloji-luget, 8 страниц, 2007 кнопок).

Убирается и то, и другое. Сами duzelis.js / duzelis.css остаются в
репозитории, и admin-corrections.html — страница разбора предложений —
не затрагивается: она виджетом не пользуется.

    python remove_duzelis.py            # отчёт
    python remove_duzelis.py --apply
"""
from __future__ import annotations
import re, sys, io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).parent
BOOK = ROOT / 'klinik-psixiatriya'
APPLY = '--apply' in sys.argv
KEEP = {'admin-corrections'}

# подключение виджета в <head>
HEAD = re.compile(r'[ \t]*<!-- DUZELIS-WIDGET -->\s*'
                  r'(?:<link rel="stylesheet" href="duzelis\.css">\s*)?'
                  r'(?:<script src="duzelis\.js" defer></script>\s*)?', re.I)
# правило, двигавшее кнопку в центр низа
FAB_CSS = re.compile(r'/\* «Düzəliş et»[^*]*\*/\s*\.dzl-fab\{[^}]*\}\s*')
# колонка с кнопкой правки в справочных таблицах
CELL = re.compile(r'<td class="rasmi-cell">(?:(?!</td>)[\s\S])*?</td>')
TH = re.compile(r'<th[^>]*>\s*(?:Düzəlt|Düzelt|Исправить|Correct)\s*</th>')


def main() -> int:
    stat = {'head': 0, 'css': 0, 'cells': 0, 'th': 0, 'files': 0}
    for fp in sorted(BOOK.rglob('*.html')):
        if fp.stem in KEEP:
            continue
        raw = fp.read_bytes().decode('utf-8')
        crlf = raw.count('\r\n') > raw.count('\n') // 2
        t = raw.replace('\r\n', '\n')
        t, a = HEAD.subn('', t)
        t, b = FAB_CSS.subn('', t)
        t, c = CELL.subn('', t)
        t, d = TH.subn('', t)
        if not (a or b or c or d):
            continue
        stat['head'] += a; stat['css'] += b; stat['cells'] += c; stat['th'] += d
        stat['files'] += 1
        if APPLY:
            fp.write_bytes((t.replace('\n', '\r\n') if crlf else t).encode('utf-8'))
    print(f'страниц затронуто: {stat["files"]}')
    print(f'  подключений виджета снято: {stat["head"]}')
    print(f'  правил .dzl-fab снято:     {stat["css"]}')
    print(f'  кнопок ✎ в таблицах:       {stat["cells"]}')
    print(f'  заголовков колонки:        {stat["th"]}')
    print('применено' if APPLY else 'пробный прогон — запустить с --apply')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
