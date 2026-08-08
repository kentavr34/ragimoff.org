# -*- coding: utf-8 -*-
"""Восстанавливает разделитель после </strong>, потерянный в переводах.

ОСТОРОЖНО: «нет пробела после </strong>» — само по себе НЕ дефект.
В азербайджанском и турецком падежный аффикс законно приклеивается к
закрывающему тегу: «<strong>uşaq istismarı</strong>dır», «<strong>tek
kategori</strong>nda», «<strong>overdiagnosis</strong>-'den». То же с
английским множественным «<strong>qualifier</strong>s:» и со скобкой
«<strong>...</strong>)». Широкое правило дало 663 «дефекта», из которых
большинство — законная типографика. Поэтому чиним только два случая:

1. Пробел есть, знака препинания нет, а у az на той же позиции разделитель
   есть — значит при переводе он потерялся.
2. Пробела нет вовсе, и следующий символ — заглавная буква или цифра
   («</strong>2+ core features», «</strong>The effect of...»), либо для
   русского — любая кириллическая буква (в русском аффиксы к тегу не
   приклеиваются: «</strong>это», «</strong>объединены»).

    python fix_strong.py          # только отчёт
    python fix_strong.py --apply
"""
import re, sys, io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
B = Path('klinik-psixiatriya')
DIRS = {'az': B, 'ru': B / 'ru', 'en': B / 'en', 'tr': B / 'tr'}
CARD = re.compile(r'(6[A-E][0-9A-Z]{2}|7[AB][0-9A-Z]{2}|8A05|HA[0-9A-Z]{2}|GA34)')
APPLY = '--apply' in sys.argv
SAMPLES = []

# знак сразу после </strong>, при котором вмешиваться не надо
OK_AFTER = re.compile(r'^\s*([—–:;,.\)\]\}»”"\'’\-…/%]|&[mn]dash;|$)')
# разделитель, который имеет смысл переносить из az
CARRY = re.compile(r'^\s*([—–:;,])')
CLOSE = re.compile(r'^\s*</')
UPPER = re.compile(r'[A-ZÀ-ÖØ-ÞĞİÖŞÜÇƏА-ЯЁ0-9]')
CYR = re.compile(r'[А-Яа-яЁё]')


def scan(text):
    m = re.search(r'<main[\s\S]*?</main>', text, re.I)
    body = m.group(0) if m else text
    out = []
    for mm in re.finditer(r'</strong>', body):
        tail = body[mm.end():mm.end() + 12]
        if CLOSE.match(tail):
            out.append(None)
        else:
            s = CARRY.match(tail)
            out.append(s.group(1) if s else ('ok' if OK_AFTER.match(tail) else ''))
    return out, m


def main():
    codes = sorted({p.stem for p in B.glob('*.html') if CARD.fullmatch(p.stem)})
    total, per_lang, skew = 0, {'ru': 0, 'en': 0, 'tr': 0}, []
    for c in codes:
        az_sep, _ = scan((B / f'{c}.html').read_text(encoding='utf-8', errors='ignore'))
        for lg in ('ru', 'en', 'tr'):
            fp = DIRS[lg] / f'{c}.html'
            if not fp.exists():
                continue
            raw = fp.read_bytes().decode('utf-8')
            crlf = raw.count('\r\n') > raw.count('\n') // 2
            t = raw.replace('\r\n', '\n')
            lg_sep, m = scan(t)
            aligned = len(lg_sep) == len(az_sep)
            if not aligned:
                skew.append(f'{lg}/{c}')
            body = m.group(0) if m else t
            fixes = []
            for i, mm in enumerate(re.finditer(r'</strong>', body)):
                if lg_sep[i] in (None, 'ok') or lg_sep[i] != '':
                    continue
                nxt = body[mm.end():mm.end() + 1]
                carry = az_sep[i] if (aligned and az_sep[i] not in (None, '', 'ok')) else None
                if nxt.isspace():
                    if not carry:
                        continue                       # случай 1
                    sep = carry
                else:
                    if not (UPPER.match(nxt) or (lg == 'ru' and CYR.match(nxt))):
                        continue                       # аффикс — не трогаем
                    sep = carry or '—'                 # случай 2
                fixes.append((mm.end(), sep))
                if len(SAMPLES) < 16:
                    SAMPLES.append(f'{lg}/{c} «{sep}» ...'
                                   + re.sub(r'\s+', ' ', body[max(0, mm.start() - 46):mm.end() + 46]))
            if not fixes:
                continue
            for pos, sep in reversed(fixes):
                body = body[:pos] + (f' {sep} ' if sep in '—–' else f'{sep} ') + body[pos:].lstrip()
                # «Фармакотерапия первой линии.</strong> — ...» — точка внутри
                # жирного перед разделителем лишняя
                head = pos - len('</strong>')
                if body[:head].endswith('.') and not body[:head].endswith('..'):
                    body = body[:head - 1] + body[head:]
            total += len(fixes)
            per_lang[lg] += len(fixes)
            if APPLY:
                t = t[:m.start()] + body + t[m.end():]
                fp.write_bytes((t.replace('\n', '\r\n') if crlf else t).encode('utf-8'))
    for x in SAMPLES:
        print('  ', x)
    print(f'\nвосстановлено разделителей: {total}  (ru {per_lang["ru"]}, '
          f'en {per_lang["en"]}, tr {per_lang["tr"]})')
    if skew:
        print(f'карточек с расхождением числа <strong>: {len(skew)} — {", ".join(skew)}')
    print('применено' if APPLY else 'пробный прогон — запустить с --apply')


if __name__ == '__main__':
    main()
