#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
xrefcheck.py — проверяет отсылки внутри текста книги.

`checkup.py` проверяет ссылки разметки: `href` и якоря. Но книга ссылается на
себя и словами — «развёрнутая тема §10», «см. Əlavə B», «(6B41)». Такая
отсылка не является ссылкой для браузера, поэтому её никто не проверял: раздел
мог быть перенумерован, приложение переименовано, карточка получить другой код,
и текст молча указывал бы в пустоту.

Что проверяется:

  РАЗДЕЛ.   «§10», «§ 7.2» — существует ли раздел с таким номером в этой же
            карточке. Ссылка на §12 в карточке из одиннадцати разделов — брак.

  КОД.      «(6B41)», «6A05» в прозе — существует ли карточка с таким кодом
            или знает ли его канон. Подкоды (6A00.0) и остаточные (6C5Y, 6C5Z)
            законны и сверяются по базовому коду.

  ПРИЛОЖЕНИЕ. «Əlavə B» · «Приложение Б» · «Appendix B» · «Ek B» — существует
            ли такое приложение.

  ПАРАЛЛЕЛЬНОСТЬ. Набор отсылок карточки сверяется между четырьмя языками.
            Если азербайджанский отсылает к §10, а русский нет — перевод
            потерял отсылку, даже когда обе фразы по отдельности верны.

    python xrefcheck.py
    python xrefcheck.py --card 6A05
"""
from __future__ import annotations
import re, sys, io, json, html as H
from pathlib import Path
from collections import Counter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).parent
BOOK = ROOT / 'klinik-psixiatriya'
DIRS = {'az': BOOK, 'ru': BOOK / 'ru', 'en': BOOK / 'en', 'tr': BOOK / 'tr'}
ONE = sys.argv[sys.argv.index('--card') + 1] if '--card' in sys.argv else None

LOOSE = re.compile(r'<(?![a-zA-Z/!?])')
SEC_ID = re.compile(r'<h2 id="[^"]*?-(\d+)-[^"]*"')
# «§10», «§ 7.2», «§§ 4–5»
SEC_REF = re.compile(r'§\s*(\d{1,2})')
# код XBT-11: цифра, буква, две буквы-или-цифры; далее необязательный подкод
CODE_REF = re.compile(r'(?<![\w.])([0-9][A-Z][0-9A-Z]{2})(?:\.[0-9A-Z]{1,2})?(?![\w])')
# Русский склоняет: «в Приложении Б». Турецкий приклеивает падеж: «Ek B'de».
APPX = re.compile(r'(?:Əlavə|Приложени[еий]|Appendix|Ek)\s+([A-ZА-Я])(?![\wа-яa-z])')


def visible(raw: str) -> str:
    m = re.search(r'<main[\s\S]*</main>', raw)
    if not m:
        return ''
    s = re.sub(r'<(script|style|nav|aside)[\s\S]*?</\1>', ' ', m.group(0))
    # список литературы отсылок не содержит, зато полон кодов и цифр
    s = re.sub(r'<ol class="ref-list"[^>]*>[\s\S]*?</ol>', ' ', s)
    return re.sub(r'\s+', ' ', H.unescape(re.sub(r'<[^>]*>', ' ', LOOSE.sub('&lt;', s))))


def known_codes() -> set[str]:
    """Коды, о которых книга знает: карточки плюс всё, что перечисляет канон."""
    codes = {p.stem for p in BOOK.glob('*.html') if re.fullmatch(r'[0-9A-Z]{4}', p.stem)}
    canon = ROOT / '_codes_canon.json'
    if canon.exists():
        blob = canon.read_text(encoding='utf-8')
        codes |= set(re.findall(r'\b[0-9][A-Z][0-9A-Z]{2}\b', blob))
    return codes


def appendices() -> set[str]:
    """Буквы существующих приложений — из заголовков страниц elave-*."""
    out = set()
    for fp in BOOK.glob('elave-*.html'):
        for m in re.finditer(r'(?:Əlavə|ƏLAVƏ)\s+([A-ZА-Я])', fp.read_text(encoding='utf-8', errors='ignore')):
            out.add(m.group(1))
    return out


def refs(raw: str) -> tuple[Counter, Counter, Counter, set]:
    v = visible(raw)
    secs = Counter(SEC_REF.findall(v))
    codes = Counter(CODE_REF.findall(v))
    appx = Counter(APPX.findall(v))
    own = {m.group(1) for m in SEC_ID.finditer(raw)}
    return secs, codes, appx, own


def cards() -> list[str]:
    return [p.stem for p in sorted(BOOK.glob('*.html'))
            if re.fullmatch(r'[0-9A-Z]{4}', p.stem) and (ONE is None or p.stem == ONE)]


def main() -> int:
    codes_ok, appx_ok = known_codes(), appendices()
    bad_sec, bad_code, bad_appx, parity = [], [], [], []
    no_card = set()
    total = 0

    for c in cards():
        prof = {}
        for lg, d in DIRS.items():
            fp = d / f'{c}.html'
            if not fp.exists():
                continue
            raw = fp.read_text(encoding='utf-8', errors='ignore')
            s, k, a, own = refs(raw)
            prof[lg] = (s, k, a)
            total += sum(s.values()) + sum(k.values()) + sum(a.values())
            for num, n in s.items():
                if num not in own:
                    bad_sec.append((lg, c, num, sorted(own, key=int)))
            for code, n in k.items():
                # Коды на Y и Z — остаточные и границы диапазонов XBT-11
                # («6A00–6A0Z», «6C5Y digər dəqiqləşdirilmiş»), они законны
                # по построению и своей карточки иметь не должны.
                if code.endswith(('Y', 'Z')) or code in codes_ok:
                    continue
                no_card.add((code, c))
            for letter, n in a.items():
                if appx_ok and letter not in appx_ok:
                    bad_appx.append((lg, c, letter, sorted(appx_ok)))
        if 'az' in prof:
            for idx, name in ((0, '§'), (2, 'приложение')):
                base = prof['az'][idx]
                for lg in ('ru', 'en', 'tr'):
                    if lg not in prof:
                        continue
                    miss = base - prof[lg][idx]
                    extra = prof[lg][idx] - base
                    if miss or extra:
                        parity.append((c, lg, name, sorted(miss.elements()), sorted(extra.elements())))

    print('=' * 72)
    print('ПРОВЕРКА ОТСЫЛОК В ТЕКСТЕ')
    print('=' * 72)
    print(f'  отсылок найдено: {total}')
    print(f'  ссылок на несуществующий раздел: {len(bad_sec)}')
    for lg, c, num, own in bad_sec[:15]:
        print(f'      {lg}/{c}: §{num}, а разделы {own[0]}…{own[-1]}')
    print(f'  ссылок на неизвестный код: {len(bad_code)}')
    codes_no_card = sorted({x[0] for x in no_card})
    print(f'  кодов XBT-11 без своей карточки (не ошибка, но проверить факт): '
          f'{len(codes_no_card)}')
    if codes_no_card:
        print('      ' + ', '.join(codes_no_card))
    print(f'  ссылок на несуществующее приложение: {len(bad_appx)}')
    for lg, c, letter, ok in bad_appx[:10]:
        print(f'      {lg}/{c}: «{letter}», а есть {ok}')
    print(f'  отсылок, потерянных или добавленных в переводе: {len(parity)}')
    for c, lg, name, miss, extra in parity[:20]:
        print(f'      {c}/{lg} {name}: нет {miss} · лишние {extra}')
    return 1 if (bad_sec or bad_code or bad_appx or parity) else 0


if __name__ == '__main__':
    raise SystemExit(main())
