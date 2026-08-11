#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_meta.py — приводит служебные данные страницы в согласие с самой страницей.

Две вещи, которых не видно при чтении книги, потому что они живут в <head>:
вкладка браузера, карточка при пересылке ссылки и то, что забирает поисковик.

  ЗАГОЛОВОК ВКЛАДКИ. В карточках расстройств <title> и <og:title> остались
        со СТАРЫМИ, доканоническими именами: «SINGLE EPISODE DEPRESIVE
        DISORDER» (с одной s), «LIGHT NEUROCOGNITIVE DISORDER» вместо MILD,
        «AVERSION/RESTRICTIVE» вместо AVOIDANT-RESTRICTIVE, русское «ОДИН
        ЭПИЗОД» против «ЕДИНИЧНЫЙ ЭПИЗОД» в <h1>. Расхождений 79 из 416.
        Направление правки не выбирается: в ТОМ ЖЕ файле <meta description>
        и og:description уже несут каноническое имя — страница сама знает
        верный ответ, разошёлся только заголовок. Источник — тот же
        `_codes_canon.json`, из которого build_headers.py собирает <h1>.

        В азербайджанском мастере таких расхождений два, и оба — дефекты
        (6C20, 6C41); значит правило книги «title совпадает с h1», а 77
        расхождений в переводах — снос, а не замысел.

  ЯЗЫК ДОКУМЕНТА. Все 411 переведённых страниц объявляли в структурированных
        данных `"inLanguage": "az"` — то есть сообщали поисковику и
        экранному диктору, что русская, английская и турецкая книги написаны
        по-азербайджански. Значение берётся по папке страницы.

    python fix_meta.py --dry
    python fix_meta.py
"""
from __future__ import annotations
import json, re, sys, io, html as H
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).parent
BOOK = ROOT / 'klinik-psixiatriya'
CANON = ROOT / '_codes_canon.json'
DIRS = {'az': BOOK, 'ru': BOOK / 'ru', 'en': BOOK / 'en', 'tr': BOOK / 'tr'}
DRY = '--dry' in sys.argv

SUFFIX = {'az': 'KLİNİK PSİXİATRİYA', 'ru': 'КЛИНИЧЕСКАЯ ПСИХИАТРИЯ',
          'en': 'CLINICAL PSYCHIATRY', 'tr': 'KLİNİK PSİKİYATRİ'}


def canon_titles() -> dict:
    """код → {язык: каноническое имя} — тот же источник, что и у <h1>."""
    data = json.loads(CANON.read_text(encoding='utf-8'))
    return {r['code']: r['title'] for r in data['header_source']['rows']}


def h1_of(t: str) -> str:
    m = re.search(r'<h1[^>]*>([\s\S]*?)</h1>', t)
    return re.sub(r'\s+', ' ', H.unescape(re.sub(r'<[^>]*>', ' ', m.group(1)))).strip() if m else ''


def main() -> int:
    titles = canon_titles()
    changed_t, changed_l, files = 0, 0, 0
    report = []

    for lg, d in DIRS.items():
        for fp in sorted(d.glob('*.html')):
            raw = fp.read_bytes()
            crlf = raw.count(b'\r\n') > raw.count(b'\n') // 2
            t = raw.decode('utf-8').replace('\r\n', '\n')
            orig = t

            # 1. заголовок вкладки — только у карточек расстройств: у страниц
            #    глав и вводных <title> намеренно короче <h1>
            if re.fullmatch(r'[0-9A-Z]{4}', fp.stem) and fp.stem in titles:
                want = titles[fp.stem].get(lg) or ''
                cur = h1_of(t)
                if want and cur and want != cur:
                    # канон и страница разошлись — это забота build_headers.py
                    want = cur
                if want:
                    full = H.escape(want, quote=False) + ' | ' + SUFFIX[lg]
                    t2 = re.sub(r'<title>[^<]*</title>', '<title>' + full + '</title>', t)
                    t2 = re.sub(r'(<meta property="og:title" content=")[^"]*(")',
                                lambda m: m.group(1) + H.escape(full, quote=True) + m.group(2), t2)
                    if t2 != t:
                        changed_t += 1
                        report.append(f'  {lg}/{fp.stem}: {want[:62]}')
                        t = t2

            # 2. язык документа в структурированных данных
            t2 = re.sub(r'("inLanguage":\s*")[a-z-]+(")',
                        lambda m: m.group(1) + lg + m.group(2), t)
            if t2 != t:
                changed_l += 1
                t = t2

            if t != orig:
                files += 1
                if not DRY:
                    fp.write_bytes((t.replace('\n', '\r\n') if crlf else t).encode('utf-8'))

    print('=' * 72)
    print('СЛУЖЕБНЫЕ ДАННЫЕ СТРАНИЦ')
    print('=' * 72)
    print(f'  заголовок вкладки приведён к имени из канона: {changed_t}')
    for line in report[:40]:
        print(line)
    if len(report) > 40:
        print(f'      …ещё {len(report) - 40}')
    print(f'  язык документа исправлен: {changed_l}')
    print(f'  файлов затронуто: {files}' + ('  (пробный прогон)' if DRY else ''))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
