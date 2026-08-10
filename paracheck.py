#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
paracheck.py — ищет потерянные, удвоенные и усохшие абзацы в переводах.

Зачем. `checkup.py` считает h2/h3/h4/li/table/tr по всей карточке — и абзац
`<p>` в этот счёт не входит вовсе, а раздел там не различается. Поэтому
пропавший абзац перевода невидим, а перенос блока из §5 в §8 взаимно
сокращается и тоже не замечается.

Две проверки, разные по строгости:

  СЧЁТ.  Число блоков (`p`, `li`, `tr`, `h3`, `h4`) сверяется ПО РАЗДЕЛАМ,
         а не по карточке. Расхождение означает потерянный или лишний блок
         и является жёстким сигналом.

  ОБЪЁМ. Когда счёт сошёлся, блоки сопоставляются попарно по порядку и
         сравнивается длина. Языки естественно различаются по многословности,
         поэтому эталон берётся не с потолка: для каждой пары языков считается
         СВОЙ типичный коэффициент по всей книге (медиана), и тревога поднимается
         только на блоках, выпадающих из него в разы. Так ловится абзац,
         переведённый одной строкой вместо пяти.

Дополнительно ищутся два вида брака, не зависящие от языка:
  * два одинаковых блока подряд — след копирования;
  * пустой блок.

    python paracheck.py            # отчёт
    python paracheck.py --card 6A05
    python paracheck.py --ratio    # показать коэффициенты многословности
"""
from __future__ import annotations
import re, sys, io, html as H
from pathlib import Path
from statistics import median

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).parent
BOOK = ROOT / 'klinik-psixiatriya'
DIRS = {'az': BOOK, 'ru': BOOK / 'ru', 'en': BOOK / 'en', 'tr': BOOK / 'tr'}
ONE = sys.argv[sys.argv.index('--card') + 1] if '--card' in sys.argv else None
SHOW_RATIO = '--ratio' in sys.argv

BLOCKS = ('p', 'li', 'tr', 'h3', 'h4')
LOOSE = re.compile(r'<(?![a-zA-Z/!?])')
# Разделы карточки: якорь вида id="6a05-3-epidemiologiya" одинаков во всех языках
SEC = re.compile(r'<h2 id="[^"]*?-(\d+)-[^"]*"')


def body(raw: str) -> str:
    m = re.search(r'<main[\s\S]*</main>', raw)
    if not m:
        return ''
    s = re.sub(r'<(script|style|nav|aside)[\s\S]*?</\1>', ' ', m.group(0))
    return LOOSE.sub('&lt;', s)


def sections(raw: str) -> dict[str, str]:
    """Разрезает карточку по номерам разделов §1…§11."""
    b = body(raw)
    marks = [(m.start(), m.group(1)) for m in SEC.finditer(b)]
    out = {}
    for i, (pos, num) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else len(b)
        out[num] = b[pos:end]
    return out


def blocks(sec: str) -> dict[str, list[str]]:
    """Текст каждого блока раздела, по типам."""
    out = {}
    for tag in BLOCKS:
        vals = []
        for m in re.finditer(rf'<{tag}\b[^>]*>([\s\S]*?)</{tag}>', sec, re.I):
            txt = re.sub(r'\s+', ' ', H.unescape(re.sub(r'<[^>]*>', ' ', m.group(1)))).strip()
            vals.append(txt)
        out[tag] = vals
    return out


def cards() -> list[str]:
    return [p.stem for p in sorted(BOOK.glob('*.html'))
            if re.fullmatch(r'[0-9A-Z]{4}', p.stem) and (ONE is None or p.stem == ONE)]


def main() -> int:
    codes = cards()
    counts, lengths, dup, empty = [], [], [], []
    ratios = {lg: [] for lg in ('ru', 'en', 'tr')}
    pairs = []          # (карточка, раздел, тег, номер, длина az, длина lg, lg, текст)

    for c in codes:
        base_raw = (BOOK / f'{c}.html').read_text(encoding='utf-8', errors='ignore')
        base = sections(base_raw)
        for lg in ('ru', 'en', 'tr'):
            fp = DIRS[lg] / f'{c}.html'
            if not fp.exists():
                continue
            other = sections(fp.read_text(encoding='utf-8', errors='ignore'))
            for num in sorted(base, key=int):
                if num not in other:
                    continue
                a, b = blocks(base[num]), blocks(other[num])
                for tag in BLOCKS:
                    if len(a[tag]) != len(b[tag]):
                        counts.append((c, lg, num, tag, len(a[tag]), len(b[tag])))
                        continue
                    for i, (x, y) in enumerate(zip(a[tag], b[tag])):
                        if len(x) >= 60 and len(y) >= 1:
                            ratios[lg].append(len(y) / len(x))
                            pairs.append((c, num, tag, i, len(x), len(y), lg, x))

    # брак, не зависящий от языка
    for lg, d in DIRS.items():
        for c in codes:
            fp = d / f'{c}.html'
            if not fp.exists():
                continue
            for num, sec in sections(fp.read_text(encoding='utf-8', errors='ignore')).items():
                bl = blocks(sec)
                for tag in BLOCKS:
                    seq = bl[tag]
                    for i in range(1, len(seq)):
                        if seq[i] and seq[i] == seq[i - 1] and len(seq[i]) > 40:
                            dup.append((lg, c, num, tag, seq[i][:60]))
                    if tag in ('p', 'li'):
                        empty += [(lg, c, num, tag) for x in seq if not x]

    med = {lg: median(v) if v else 1.0 for lg, v in ratios.items()}
    for c, num, tag, i, la, lb, lg, txt in pairs:
        r = (lb / la) / med[lg]
        if r < 0.60 or r > 1.75:
            lengths.append((c, lg, num, tag, i, la, lb, round(r, 2), txt[:70]))

    print('=' * 72)
    print(f'СВЕРКА АБЗАЦЕВ — {len(codes)} карточек × 3 перевода')
    print('=' * 72)
    if SHOW_RATIO:
        for lg in ('ru', 'en', 'tr'):
            print(f'  многословность {lg}/az: медиана {med[lg]:.2f} по {len(ratios[lg])} блокам')
    print(f'  сопоставлено блоков: {len(pairs)}')
    print(f'  расхождений в числе блоков: {len(counts)}')
    for c, lg, num, tag, x, y in counts[:25]:
        print(f'      {c} §{num} {lg}: <{tag}> az={x} {lg}={y}')
    print(f'  блоков с подозрительной длиной: {len(lengths)}')
    for c, lg, num, tag, i, la, lb, r, txt in lengths[:25]:
        print(f'      {c} §{num} {lg} <{tag}>#{i}: {la}→{lb} симв. (×{r} к норме) — {txt}')
    print(f'  одинаковых блоков подряд: {len(dup)}')
    for lg, c, num, tag, txt in dup[:12]:
        print(f'      {lg}/{c} §{num} <{tag}>: {txt}')
    print(f'  пустых блоков: {len(empty)}')
    for lg, c, num, tag in empty[:12]:
        print(f'      {lg}/{c} §{num} <{tag}>')
    return 1 if (counts or dup or empty) else 0


if __name__ == '__main__':
    raise SystemExit(main())
