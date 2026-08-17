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
# Защита имён собственных была СЛЕПА К ДИАКРИТИКЕ: набор строчных не включал
# ö ü ş ğ ı ç ə å é, и «Strömgren E.» под правило имени не подпадал — скрипт
# понижал фамилию до «strömgren». Дефект уже правился однажды и вернулся при
# следующем прогоне; поймал его сторож regress.py. 2026-08-17
_UP = 'A-ZА-ЯЁÄÖÜÅÉÈÇŞĞİÆØƏ'
_LO = 'a-zа-яёäöüåéèçşğıəæø'
KEEP = re.compile(r'^(?:[%s]{2,}|[%s]\.|[%s][%s]+\s+[%s])' % (_UP, _UP, _UP, _LO, _UP))


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

    # 1б. ДЕФИС-МИНУС в роли тире. Правило 1 чинит короткое тире «–», но не
    # дефис «-»: в 28 местах (24 в английском, 4 в турецком) между пробелами
    # стоял именно он — «Scales - PHQ-9», «Personality - anxiety sensitivity».
    # Условия узкие, чтобы не задеть законный дефис: по бокам пробелы, слева
    # буква или скобка, справа буква или цифра, и обе стороны — не число
    # (диапазоны вида «10 - 20» тоже тире, но их правит другое правило).
    hyphens = 0
    for lg, d in DIRS.items():
        for fp in sorted(d.glob('*.html')):
            raw2, crlf2, t2, m2 = body(fp)
            if not m2:
                continue
            b, k = re.subn(r'(?<=[A-Za-zА-Яа-яƏəÇçĞğİıÖöŞşÜü\)\]]) - (?=[A-Za-zА-Яа-яƏəÇçĞğİıÖöŞşÜü“"«(])',
                           ' — ', m2.group(0))
            if not k:
                continue
            hyphens += k
            if APPLY:
                save(fp, t2[:m2.start()] + b + t2[m2.end():], crlf2)
    print(f'дефис-минус в роли тире → длинное тире: {hyphens}')

    # 2. регистр по мастеру
    codes = sorted({p.stem for p in BOOK.glob('*.html') if CARD.fullmatch(p.stem)})
    fixed, skew = 0, 0
    for c in codes:
        _, _, _, ma = body(BOOK / f'{c}.html')
        if not ma:
            continue
        az = [x.group(1) for x in LABEL.finditer(ma.group(0))]
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
                if KEEP.match(ch + after) or not want.isalpha() or not ch.isalpha():
                    # аббревиатура, имя собственное или цифра с любой стороны —
                    # регистр здесь не наша забота
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
