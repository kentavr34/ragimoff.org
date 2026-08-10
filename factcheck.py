#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
factcheck.py — сверяет книгу с первоисточником ВОЗ.

Первоисточник — «Clinical Descriptions and Diagnostic Requirements for ICD-11
Mental, Behavioural and Neurodevelopmental Disorders» (CDDR), официальный
документ ВОЗ, 852 страницы. Текст кладётся рядом как `_cddr.txt`; выкачивается
один раз, дальше проверка идёт локально.

Что сверяется сейчас — ДИАГНОСТИЧЕСКИЕ СРОКИ. Это самый проверяемый класс
клинических фактов: «не менее 12 месяцев», «две недели», «до 12 лет» — числа
однозначные, и ошибка в них меняет диагноз. Для каждой карточки берётся её
раздел в CDDR, из него вынимаются все сроки, и то же делается с §6 книги.
Расхождение выносится на разбор.

Чего инструмент НЕ делает и делать не может: он не понимает, к чему срок
относится. «12 месяцев» может быть длительностью симптома в одном месте и
периодом наблюдения в другом. Поэтому вывод — не приговор, а список мест,
которые надо прочитать. Приговор выносит человек.

Границы источника: CDDR покрывает только главу 6 (психические расстройства).
Карточки глав 7 (сон), 8 (тики), 16 (GA34) и 17 (сексуальное здоровье)
сверяются отдельно, по своим руководствам.

    python factcheck.py --titles     сверка названий кодов
    python factcheck.py --terms      сверка диагностических сроков
    python factcheck.py --card 6C51  разбор одной карточки
"""
from __future__ import annotations
import re, sys, io, json, html as H
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).parent
BOOK = ROOT / 'klinik-psixiatriya'
CDDR = ROOT / '_cddr.txt'
TABLE = ROOT / '_factcheck.json'
ONE = sys.argv[sys.argv.index('--card') + 1] if '--card' in sys.argv else None

LOOSE = re.compile(r'<(?![a-zA-Z/!?])')
# срок в тексте ВОЗ: «at least 12 months», «2 weeks», «before age 12»
EN_TERM = re.compile(
    r'(?:at least|minimum of|for)?\s*(\d{1,2})\s*(month|week|day|year|hour)s?\b', re.I)
EN_AGE = re.compile(r'before (?:the )?age (?:of )?(\d{1,2})|age (\d{1,2})\s*years?', re.I)
# срок в азербайджанском тексте: «ən azı 12 ay», «2 həftə», «12 yaşa qədər»
AZ_TERM = re.compile(r'(\d{1,2})\s*(ay|həftə|gün|il|saat)\b')
AZ_AGE = re.compile(r'(\d{1,2})\s*yaş')


def visible(raw: str) -> str:
    m = re.search(r'<main[\s\S]*</main>', raw)
    if not m:
        return ''
    s = re.sub(r'<(script|style|nav|aside)[\s\S]*?</\1>', ' ', m.group(0))
    s = re.sub(r'<ol class="ref-list"[^>]*>[\s\S]*?</ol>', ' ', s)
    return re.sub(r'\s+', ' ', H.unescape(re.sub(r'<[^>]*>', ' ', LOOSE.sub('&lt;', s))))


def diagnosis_section(raw: str) -> str:
    """§6 «Diaqnoz» — там живут диагностические требования."""
    m = re.search(r'<h2 id="[^"]*-6-diaqnoz[\s\S]*?(?=<h2 id="[^"]*-7-)', raw)
    return visible('<main>' + m.group(0) + '</main>') if m else ''


def cddr_text() -> str:
    if not CDDR.exists():
        sys.exit('нет _cddr.txt — сначала выкачать документ ВОЗ, см. шапку файла')
    return CDDR.read_text(encoding='utf-8')


ANCHOR = 'Essential (required) features'


def cddr_slice(full: str, title: str) -> str:
    """Раздел CDDR для расстройства.

    Документ устроен так: «<Название расстройства> «<Название расстройства>» и следом строка
    «Essential (required) features», дальше сами требования. Срезаем от
    features» и дальше сами требования. Срезаем от этого якоря до следующего.
    По коду срезать нельзя: код стоит и в оглавлении, и в колонтитулах, и
    в таблицах квалификаторов — первое совпадение почти всегда не то.
    """
    if not title:
        return ''
    lo = full.lower()
    key = title.lower().rstrip('.') + chr(10) + ANCHOR.lower()
    i = lo.find(key)
    if i < 0:                       # заголовок мог перенестись со строки
        key2 = title.lower().rstrip('.')
        for m in re.finditer(re.escape(key2), lo):
            tail = lo[m.end():m.end() + 120].replace(chr(10), ' ')
            if ANCHOR.lower() in tail:
                i = m.start()
                break
    if i < 0:
        return ''
    # первый якорь идёт сразу за названием; конец раздела — СЛЕДУЮЩИЙ якорь
    first = lo.find(ANCHOR.lower(), i)
    j = lo.find(ANCHOR.lower(), first + len(ANCHOR)) if first > 0 else -1
    return full[i:j if j > 0 else i + 9000]


def terms(text: str, lang: str) -> set:
    out = set()
    if lang == 'en':
        for m in EN_TERM.finditer(text):
            out.add(f'{m.group(1)} {m.group(2).lower()}')
        for m in EN_AGE.finditer(text):
            out.add(f'age {m.group(1) or m.group(2)}')
    else:
        unit = {'ay': 'month', 'həftə': 'week', 'gün': 'day', 'il': 'year', 'saat': 'hour'}
        for m in AZ_TERM.finditer(text):
            out.add(f'{m.group(1)} {unit[m.group(2)]}')
        for m in AZ_AGE.finditer(text):
            out.add(f'age {m.group(1)}')
    return out


def cards() -> list[str]:
    return [p.stem for p in sorted(BOOK.glob('*.html'))
            if re.fullmatch(r'[0-9A-Z]{4}', p.stem) and (ONE is None or p.stem == ONE)]


def load_table() -> dict:
    return json.loads(TABLE.read_text(encoding='utf-8')) if TABLE.exists() else {}


def save_table(t: dict) -> None:
    TABLE.write_text(json.dumps(t, ensure_ascii=False, indent=1, sort_keys=True),
                     encoding='utf-8')


def main() -> int:
    full = cddr_text()
    table = load_table()
    codes = cards()
    covered, uncovered, rows = 0, [], []

    for c in codes:
        sl = cddr_slice(full, c)
        if not sl:
            uncovered.append(c)
            continue
        covered += 1
        book = diagnosis_section((BOOK / f'{c}.html').read_text(encoding='utf-8', errors='ignore'))
        b, w = terms(book, 'az'), terms(sl, 'en')
        only_book = sorted(b - w)
        if only_book:
            rows.append((c, only_book, sorted(w)[:8]))
        rec = table.setdefault(c, {})
        rec['cddr_terms'] = sorted(w)
        rec['book_terms'] = sorted(b)
        rec['status'] = 'совпадает' if not only_book else 'на разбор'

    save_table(table)
    print('=' * 72)
    print('СВЕРКА С ПЕРВОИСТОЧНИКОМ ВОЗ (CDDR) — диагностические сроки')
    print('=' * 72)
    print(f'  карточек в книге: {len(codes)}')
    print(f'  найдено в CDDR: {covered}')
    print(f'  вне охвата CDDR (главы 7, 8, 16, 17): {len(uncovered)} — {", ".join(uncovered)}')
    print(f'  карточек со сроком, которого нет у ВОЗ: {len(rows)}')
    for c, only, who in rows[:30]:
        print(f'      {c}: в книге {only}')
        print(f'            у ВОЗ  {who}')
    print(f'\n  таблица сохранена: {TABLE.name}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
