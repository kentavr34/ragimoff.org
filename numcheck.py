#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
numcheck.py — сверяет числовые утверждения книги между четырьмя языками.

Зачем. Проценты, дозы, возрасты и объёмы выборок — это факты. Если в
азербайджанском стоит 3,05%, а в русском 3,5%, читатель получит разные книги,
и ни одна проверка структуры этого не заметит.

Почему нельзя сравнивать голые числа. Пробовали — четыре раза подряд ошибался
инструмент, а не книга:
  * «2018, 2024» склеивалось в одно число, когда убирали пробелы;
  * английское «800,000» читалось как «800», потому что запятая там разряд,
    а не дробь;
  * «§10.1» и код «F90.0» выглядели десятичными дробями;
  * турецкий пишет «%20», а не «20%», и диапазон «%10–20» отдавал 10 там,
    где азербайджанский «10–20%» отдавал 20.

Отсюда правило: сверяем только числа, **привязанные к единице измерения**.
Единица — это якорь, который отличает факт от нумерации. Номера подразделов,
коды XBT и пункты списков единиц не имеют и в сравнение не попадают.

Что сверяется:
  проценты      3,05% · 10–20% · %20 (турецкая запись) · 25,7 %
  дозы          20 mg · 0,5–2 mg · 150 mkq · 10 ml
  выборки       n = 597 · n=18 932
  частота       25–50/100 000

Каждое значение приводится к единому виду с учётом языка: десятичный знак,
разделитель разрядов, положение знака процента, вид тире в диапазоне.

    python numcheck.py              # отчёт по расхождениям
    python numcheck.py --card 6A05  # разбор одной карточки
    python numcheck.py --verbose    # показать, что именно извлечено
"""
from __future__ import annotations
import re, sys, io, html as H
from pathlib import Path
from collections import Counter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).parent
BOOK = ROOT / 'klinik-psixiatriya'
DIRS = {'az': BOOK, 'ru': BOOK / 'ru', 'en': BOOK / 'en', 'tr': BOOK / 'tr'}
ONE = sys.argv[sys.argv.index('--card') + 1] if '--card' in sys.argv else None
VERBOSE = '--verbose' in sys.argv

# ── извлечение видимого текста ──────────────────────────────────────────────
# «<32 həftə», «< 110 pg/ml» — в книге таких мест много, и наивное вырезание
# тегов съедает всё до следующего «>». Сначала обезвреживаем одиночные «<».
LOOSE = re.compile(r'<(?![a-zA-Z/!?])')


def visible(raw: str) -> str:
    m = re.search(r'<main[\s\S]*</main>', raw)
    if not m:
        return ''
    s = re.sub(r'<(script|style|nav|aside)[\s\S]*?</\1>', ' ', m.group(0))
    # список литературы не сверяем: тома, страницы и годы там своя вселенная
    s = re.sub(r'<ol class="ref-list"[^>]*>[\s\S]*?</ol>', ' ', s)
    return re.sub(r'\s+', ' ', H.unescape(re.sub(r'<[^>]*>', ' ', LOOSE.sub('&lt;', s))))


# ── запись числа своя в каждом языке ───────────────────────────────────────
# Разряды: азербайджанский и русский отбивают пробелом, английский запятой,
# турецкий точкой. Дробь: везде запятая, кроме английского. Поэтому шаблон
# числа строится под язык, а не один на всех — на этом ломались прошлые
# попытки, когда «800,000» читалось как «800».
SPACE = "[" + chr(32) + chr(0xa0) + chr(0x2009) + chr(0x202f) + "]"
NUM = {
    'az': r"BSd{1,3}(?:" + SPACE + r"BSd{3})+|BSd+(?:,BSd+)?",
    'ru': r"BSd{1,3}(?:" + SPACE + r"BSd{3})+|BSd+(?:,BSd+)?",
    'en': r"\d{1,3}(?:[,\s]\d{3})+|\d+(?:\.\d+)?",
    'tr': r"\d{1,3}(?:[\.\s]\d{3})+|\d+(?:,\d+)?",
}
NUM = {k: v.replace("BS", chr(92)) for k, v in NUM.items()}
# Диапазон в книге пишется коротким тире «–». Длинное «—» — знак препинания:
# «n>34 000 — 3,9%» это не диапазон, а пояснение, и принимать его за диапазон
# значит получить бессмысленное «34000-3.9».
DASH = "[" + chr(0x2013) + "-]"


def norm(tok: str, lg: str) -> str:
    """«18 932» · «18,932» · «18.932» → «18932»; «3,05» · «3.05» → «3.05»."""
    tok = re.sub(SPACE, "", tok)
    if lg == 'en':
        tok = tok.replace(",", "")
    elif lg == 'tr':
        if re.fullmatch(r"BSd{1,3}(?:BS.BSd{3})+".replace("BS", chr(92)), tok):
            tok = tok.replace(".", "")
        tok = tok.replace(",", ".")
    else:
        tok = tok.replace(",", ".")
    if "." in tok:
        tok = tok.rstrip("0").rstrip(".")
    return tok or "0"


def rng(txt: str, lg: str) -> str:
    parts = [x.strip() for x in re.split(DASH, txt) if x.strip()]
    return "-".join(norm(x, lg) for x in parts)


# Одна и та же единица пишется по-разному: азербайджанское «q» — это грамм,
# «mkq» — микрограмм; русские «г» и «мкг»; турецкое «gr»; английские «g», «µg».
UNIT = {
    # азербайджанский пишет миллиграмм как «mq», русский как «мг»
    'mg': 'mg', 'mq': 'mg', 'мг': 'mg',
    'q': 'g', 'g': 'g', 'gr': 'g', 'г': 'g',
    'mkq': 'ug', 'mcg': 'ug', 'µg': 'ug', 'ug': 'ug', 'мкг': 'ug',
    'ml': 'ml', 'мл': 'ml', 'mL': 'ml',
    'iu': 'iu', 'ме': 'iu',
    'mmol': 'mmol', 'ммоль': 'mmol',
    'ng': 'ng', 'нг': 'ng', 'pg': 'pg', 'пг': 'pg',
}
# «(?![.])» отсекает русское «2021 г.» — это год, а не граммы
UNIT_RX = "(" + "|".join(sorted(UNIT, key=len, reverse=True)) + r")\b"
# Класс «возраст» намеренно не сверяется: «22 yaşa qədər», «до 22 лет»,
# «by age 22» — конструкции слишком разные, и класс давал только шум.


def facts(s: str, lg: str) -> Counter:
    out = Counter()
    N = NUM[lg]
    # NUM содержит альтернативу «A|B», поэтому при подстановке её ОБЯЗАТЕЛЬНО
    # оборачивать в (?:…). Без этого диапазон цеплялся не к тому варианту:
    # «5–15%» давало 15, а турецкое «%5–15» давало 5.
    SPX = r"BSs*".replace("BS", chr(92))
    # Граница слова обязательна: без неё азербайджанское «α1 300–800»
    # читалось как разряды «1 300», потому что тысячи там отбиты пробелом.
    VAL = "(?<!\\w)((?:" + N + ")(?:" + SPX + DASH + SPX + "(?:" + N + "))?)"
    SP = r"BSs*".replace("BS", chr(92))

    # процент бывает записан и словом: аз. «51,4 faiz», тур. «yüzde»,
    # рус. «процентов», англ. «percent»
    WORD = {'az': "%|faiz", 'tr': "%|y" + chr(0xfc) + "zde",
            'ru': "%|" + chr(0x43f) + chr(0x440) + chr(0x43e) + chr(0x446) + chr(0x435) + chr(0x43d) + "[" + chr(0x442) + chr(0x43e) + "]",
            'en': "%|per ?cent"}[lg]
    for m in re.finditer(VAL + SP + "(?:" + WORD + ")", s):
        out["%" + rng(m.group(1), lg)] += 1
    # диапазон словами: рус. «от 43 до 45 процентов», англ. «43 to 45 percent»
    # Диапазон, записанный словами. Грамматика своя в каждом языке, и знак
    # процента у турецкого стоит перед КАЖДЫМ числом: «%15,4 ila %51,4».
    WB = "(?<!\\w)"
    WORD_RANGE = {
        'ru': WB + "((?:" + N + "))" + " " + chr(0x434) + chr(0x43e) + " " + "((?:" + N + "))" + SP + "(?:" + WORD + ")",
        'en': WB + "((?:" + N + ")) (?:to|and) ((?:" + N + "))" + SP + "(?:" + WORD + ")",
        'az': WB + "((?:" + N + ")) il" + chr(0x259) + " ((?:" + N + "))" + SP + "(?:" + WORD + ")",
        'tr': WB + "%((?:" + N + ")) ila %((?:" + N + "))",
    }[lg]
    for m in re.finditer(WORD_RANGE, s):
        out["%" + norm(m.group(1), lg) + "-" + norm(m.group(2), lg)] += 1
        out["%" + norm(m.group(2), lg)] -= 1
        if lg == 'tr':
            out["%" + norm(m.group(1), lg)] -= 1
    # «%20» — турецкая запись. В остальных языках «…50–80% 1 ildə» дало бы
    # ложный «%1»: процент относится к прошлому числу, а «1» к следующему слову.
    if lg == 'tr':
        for m in re.finditer("%" + SP + VAL, s):
            out["%" + rng(m.group(1), lg)] += 1
    for m in re.finditer(VAL + SP + UNIT_RX, s, re.I):
        u = m.group(2).lower()
        # русское «2021 г.» — это год, а не граммы: точка после «г» выдаёт его
        if lg == 'ru' and u == chr(0x433) and s[m.end():m.end() + 1] == '.':
            continue
        out[rng(m.group(1), lg) + " " + UNIT[u]] += 1
    for m in re.finditer(r"BSbnBSs*=BSs*".replace("BS", chr(92)) + "((?:" + N + "))", s, re.I):
        out["n=" + norm(m.group(1), lg)] += 1
    for m in re.finditer(VAL + SP + "(?:/|per)" + SP + "((?:" + N + "))", s, re.I):
        base = norm(m.group(2), lg)
        if base in ("100000", "10000", "1000", "1000000"):
            out[rng(m.group(1), lg) + "/" + base] += 1
    return out


def cards() -> list[str]:
    return [p.stem for p in sorted(BOOK.glob('*.html'))
            if re.fullmatch(r'[0-9A-Z]{4}', p.stem) and (ONE is None or p.stem == ONE)]


def main() -> int:
    codes = cards()
    rows, checked = [], 0
    for c in codes:
        base = facts(visible((BOOK / f'{c}.html').read_text(encoding='utf-8', errors='ignore')), 'az')
        checked += sum(base.values())
        if VERBOSE:
            print(f'  {c} az: ' + ', '.join(f'{k}×{v}' for k, v in sorted(base.items())))
        for lg in ('ru', 'en', 'tr'):
            fp = DIRS[lg] / f'{c}.html'
            if not fp.exists():
                continue
            other = facts(visible(fp.read_text(encoding='utf-8', errors='ignore')), lg)
            miss, extra = base - other, other - base
            if miss or extra:
                rows.append((c, lg, sorted(miss.elements()), sorted(extra.elements())))
    print('=' * 72)
    print(f'ЧИСЛОВАЯ СВЕРКА — {len(codes)} карточек × 4 языка')
    print('=' * 72)
    print(f'  фактов с единицей измерения в азербайджанском мастере: {checked}')
    print(f'  карточек×языков с расхождением: {len(rows)} из {len(codes) * 3}')
    for c, lg, miss, extra in rows:
        print(f'\n  {c} / {lg}')
        if miss:
            print(f'      нет в переводе : {", ".join(miss[:12])}')
        if extra:
            print(f'      лишнее         : {", ".join(extra[:12])}')
    return 1 if rows else 0


if __name__ == '__main__':
    raise SystemExit(main())
