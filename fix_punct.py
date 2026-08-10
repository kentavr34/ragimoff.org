# -*- coding: utf-8 -*-
"""Восстанавливает точку в конце пункта там, где перевод её потерял.

Пункты списков в книге заканчиваются точкой. В переводах она местами
пропала — и это видно только при сверке с другими языками: сам по себе
пункт без точки выглядит нормально.

Решение принимается по большинству: если на этой же позиции у двух и более
языков точка есть, а у одного нет — добавляем. Пункты, кончающиеся на «:»,
«;», «?», «!», «)» или на код МКБ, не трогаем. Позиции, где языки разошлись
по числу пунктов, пропускаются целиком.

    python fix_punct.py           # отчёт
    python fix_punct.py --apply
"""
from __future__ import annotations
import re, sys, io, html as H
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).parent
BOOK = ROOT / 'klinik-psixiatriya'
LANGS = ('az', 'ru', 'en', 'tr')
DIRS = {'az': BOOK, 'ru': BOOK / 'ru', 'en': BOOK / 'en', 'tr': BOOK / 'tr'}
CARD = re.compile(r'(6[A-E][0-9A-Z]{2}|7[AB][0-9A-Z]{2}|8A05|HA[0-9A-Z]{2}|GA34)')
APPLY = '--apply' in sys.argv
OKEND = ':;?!)»”"\'’…»'


def items(fp: Path):
    """(список текстов <li> внутри <main> без списка литературы, тело, срез)."""
    t = fp.read_bytes().decode('utf-8').replace('\r\n', '\n')
    m = re.search(r'<main[\s\S]*?</main>', t, re.I)
    if not m:
        return None, None, None, t
    body = m.group(0)
    r = re.search(r'<ol class="ref-list"[^>]*>[\s\S]*?</ol>', body)
    cut = r.start() if r else len(body)
    out = []
    for li in re.finditer(r'<li>([\s\S]*?)</li>', body):
        if li.start() >= cut:
            break
        txt = re.sub(r'\s+', ' ', H.unescape(re.sub(r'<[^>]*>', '', li.group(1)))).strip()
        out.append((li, txt))
    return out, body, m, t


def main() -> int:
    codes = sorted({p.stem for p in BOOK.glob('*.html') if CARD.fullmatch(p.stem)})
    total, per = 0, {l: 0 for l in LANGS}
    samples = []
    for c in codes:
        data = {}
        for lg in LANGS:
            fp = DIRS[lg] / f'{c}.html'
            if fp.exists():
                data[lg] = items(fp) + (fp,)
        if len(data) < 3 or len({len(v[0] or []) for v in data.values()}) > 1:
            continue
        n = len(next(iter(data.values()))[0])
        for i in range(n):
            ends = {lg: (data[lg][0][i][1][-1:] if data[lg][0][i][1] else '') for lg in data}
            dots = [lg for lg, e in ends.items() if e == '.']
            if len(dots) < 2:
                continue
            for lg, e in ends.items():
                if e == '.' or not data[lg][0][i][1] or e in OKEND:
                    continue
                if not re.search(r'[\wа-яА-ЯёЁəƏıİöÖüÜşŞçÇğĞ»”)]$', data[lg][0][i][1]):
                    continue
                data[lg][0][i] = (data[lg][0][i][0], data[lg][0][i][1], True)
                per[lg] += 1
                total += 1
                if len(samples) < 12:
                    samples.append(f'{lg}/{c}: …{data[lg][0][i][1][-58:]}')
        if not APPLY:
            continue
        for lg in data:
            lis, body, m, t, fp = data[lg]
            marked = [(li, txt) for li, txt, *rest in lis if rest and rest[0]]
            if not marked:
                continue
            for li, _ in reversed(marked):
                inner = li.group(1)
                body = body[:li.start(1)] + inner.rstrip() + '.' + body[li.end(1):]
            t = t[:m.start()] + body + t[m.end():]
            raw = fp.read_bytes().decode('utf-8')
            crlf = raw.count('\r\n') > raw.count('\n') // 2
            fp.write_bytes((t.replace('\n', '\r\n') if crlf else t).encode('utf-8'))
    for s in samples:
        print('  ', s)
    print(f'\nпропущенных точек: {total} — ' + ', '.join(f'{l} {per[l]}' for l in LANGS))
    print('применено' if APPLY else 'пробный прогон — запустить с --apply')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
