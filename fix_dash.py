# -*- coding: utf-8 -*-
"""
fix_dash.py — тире и регистр после жирной метки.

Два разных дефекта:

1. **Короткое тире вместо длинного.** В книге метка отделяется длинным тире
   («<strong>Метка</strong> — пояснение»), но в 436 местах стоит короткое
   «–». Это однозначная ошибка набора, чинится во всех четырёх языках.

2. **Регистр пояснения.** После тире то заглавная, то строчная — причём
   и в азербайджанском мастере (367 против 397). Значит, это авторская
   непоследовательность, а не дефект перевода, и навязывать своё правило
   я не вправе. Что можно сделать честно — заставить переводы следовать
   мастеру: если на той же позиции у az строчная, а у перевода заглавная,
   регистр переводу выравнивается. Языки перестают спорить друг с другом.

Позиции, где число меток разошлось, пропускаются целиком.

    python fix_dash.py            # отчёт
    python fix_dash.py --apply
"""
from __future__ import annotations
import re, sys, io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).parent
BOOK = ROOT / 'klinik-psixiatriya'
DIRS = {'az': BOOK, 'ru': BOOK / 'ru', 'en': BOOK / 'en', 'tr': BOOK / 'tr'}
CARD = re.compile(r'(6[A-E][0-9A-Z]{2}|7[AB][0-9A-Z]{2}|8A05|HA[0-9A-Z]{2}|GA34)')
APPLY = '--apply' in sys.argv
LABEL = re.compile(r'</strong>\s*—\s*(\w)')
UPPER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯÇĞİÖŞÜƏ'
# метка-аббревиатура или имя собственное — регистр не трогаем
KEEP = re.compile(r'^(?:[A-ZА-ЯЁ]{2,}|[A-ZА-ЯЁ]\.|[A-ZА-ЯЁ][a-zа-яё]+\s+[A-ZА-ЯЁ])')


def body(fp: Path):
    raw = fp.read_bytes().decode('utf-8')
    crlf = raw.count('\r\n') > raw.count('\n') // 2
    t = raw.replace('\r\n', '\n')
    m = re.search(r'<main[\s\S]*?</main>', t, re.I)
    return raw, crlf, t, m


def save(fp: Path, t: str, crlf: bool):
    fp.write_bytes((t.replace('\n', '\r\n') if crlf else t).encode('utf-8'))


def main() -> int:
    dashes = 0
    # 1. короткое тире → длинное
    for lg, d in DIRS.items():
        for fp in sorted(d.glob('*.html')):
            raw, crlf, t, m = body(fp)
            if not m:
                continue
            b, k = re.subn(r'(</strong>\s*)–(\s)', r'\1—\2', m.group(0))
            if not k:
                continue
            dashes += k
            if APPLY:
                save(fp, t[:m.start()] + b + t[m.end():], crlf)

    # 2. регистр по мастеру
    codes = sorted({p.stem for p in BOOK.glob('*.html') if CARD.fullmatch(p.stem)})
    fixed, skew = 0, 0
    for c in codes:
        _, _, _, ma = body(BOOK / f'{c}.html')
        if not ma:
            continue
        az = [x.group(1) for x in LABEL.finditer(ma.group(0))]
        az_tail = [ma.group(0)[x.end(1):x.end(1) + 24] for x in LABEL.finditer(ma.group(0))]
        for lg in ('ru', 'en', 'tr'):
            fp = DIRS[lg] / f'{c}.html'
            if not fp.exists():
                continue
            raw, crlf, t, m = body(fp)
            if not m:
                continue
            b = m.group(0)
            hits = list(LABEL.finditer(b))
            if len(hits) != len(az):
                skew += 1
                continue
            out, shift, n = b, 0, 0
            for i, x in enumerate(hits):
                ch, want = x.group(1), az[i]
                if (ch in UPPER) == (want in UPPER):
                    continue
                after = b[x.end(1):x.end(1) + 24]
                if KEEP.match(ch + after):
                    continue
                pos = x.start(1) + shift
                out = out[:pos] + (ch.lower() if want not in UPPER else ch.upper()) + out[pos + 1:]
                n += 1
            if n and APPLY:
                save(fp, t[:m.start()] + out + t[m.end():], crlf)
            fixed += n
    print(f'короткое тире → длинное: {dashes}')
    print(f'регистр выровнен по мастеру: {fixed}; карточек с расхождением числа меток: {skew}')
    print('применено' if APPLY else 'пробный прогон — запустить с --apply')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
