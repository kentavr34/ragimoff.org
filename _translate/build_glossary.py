#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build translator glossaries (AZ->EN, AZ->RU) from local terminology sources:
   - klinik-psixiatriya/abbreviatur.html (trilingual tables — synced with 994 term DB)
   - _codes_map.json (official ICD-11 EN titles)
   - TYPOGRAPHY.md §0b (verified AZ<->RU disorder names)
Outputs: _translate/glossary_en.md, _translate/glossary_ru.md
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent

def strip(s):
    s = re.sub(r'<[^>]+>', '', s)
    return re.sub(r'\s+', ' ', s).strip()

def tables(path):
    t = path.read_text(encoding='utf-8')
    out = []
    for tb in re.findall(r'<table[^>]*>(.*?)</table>', t, re.S):
        rows = []
        for r in re.findall(r'<tr[^>]*>(.*?)</tr>', tb, re.S):
            cells = [strip(c) for c in re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', r, re.S)]
            rows.append(cells)
        out.append(rows)
    return out

abbr_tables = tables(ROOT / 'klinik-psixiatriya' / 'abbreviatur.html')
# table indexes (see structure): 1 = AZ form -> EN equivalent (Kod),
# 3 = Kod | AZ | EN(ICD-11) | RU(МКБ-11), 4 = AZ | RU | EN clinical terms
tri = [r for r in abbr_tables[3][1:] if len(r) >= 4]
terms = [r for r in abbr_tables[4][1:] if len(r) >= 3]
azen = [r for r in abbr_tables[1][1:] if len(r) >= 2]
abbrs = [r for r in abbr_tables[2][1:] if len(r) >= 2]

codes = json.loads((ROOT / '_codes_map.json').read_text(encoding='utf-8'))

# TYPOGRAPHY.md §0b table: | code | AZ | RU |
typ = (ROOT / 'TYPOGRAPHY.md').read_text(encoding='utf-8')
sec = re.search(r'## 0b\..*?(?=\n## )', typ, re.S).group(0)
typ_rows = []
for line in sec.splitlines():
    m = re.match(r'\|\s*\**([0-9A-Z]{2,4}[0-9A-Z.–-]*)\**\s*\|([^|]+)\|([^|]+)\|', line)
    if m and m.group(1) not in ('Kod', '---'):
        typ_rows.append((m.group(1).strip(), m.group(2).strip(), m.group(3).strip()))

RULES_EN = """# Glossary AZ -> EN (Klinik Psixiatriya)
Style: professional psychiatric register; ICD-11 (WHO 2024) and DSM-5-TR official terminology.
Core rules:
- pasiyent -> patient; psixi pozuntu -> mental disorder; XBT-11 -> ICD-11; UST -> WHO; DSM-5 stays DSM-5.
- Klinik tezahurler -> Clinical manifestations; Vahid diaqnostik meyarlar -> Unified diagnostic criteria;
  Instrumental muayineler -> Instrumental investigations; Muayine ve qiymetlendirme -> Examination and assessment;
  Mualice -> Treatment; Proqnoz -> Prognosis; Menbeler -> Sources; Metodikalar -> Methods;
  Mif ve yanlis inanclar -> Myths and misconceptions; Terminoloji luget -> Terminology glossary.
- Disorder names MUST match official ICD-11 titles (table below). DSM-5-TR names where DSM is referenced.
- AZ abbreviation pattern `AZ-abbr (EN-abbr — full name)` becomes plain EN: `EN-abbr (full name)` on first use, then EN-abbr.
- Do not translate: drug INNs stay in English INN form; scale acronyms (PHQ-9, GAD-7, ADOS-2...) stay as-is.

## Disorder names (code | AZ | EN)
"""

RULES_RU = """# Glossary AZ -> RU (Klinik Psixiatriya)
Стиль: профессиональный психиатрический регистр; терминология официального перевода МКБ-11 (РФ 2022) и DSM-5-TR (рус. издание).
Базовые правила:
- pasiyent -> пациент; psixi pozuntu -> психическое расстройство; XBT-11 -> МКБ-11; ÜST -> ВОЗ; DSM-5 остаётся DSM-5.
- Klinik təzahürlər -> Клинические проявления; Vahid diaqnostik meyarlar -> Единые диагностические критерии;
  İnstrumental müayinələr -> Инструментальные исследования; Müayinə və qiymətləndirmə -> Обследование и оценка;
  Müalicə -> Лечение; Proqnoz -> Прогноз; Mənbələr -> Источники; Metodikalar -> Методики;
  Mif və yanlış inanclar -> Мифы и заблуждения; Terminoloji lüğət -> Терминологический словарь.
- Названия расстройств СТРОГО по таблице ниже (МКБ-11 РФ 2022).
- Паттерн `АЗ-аббр (EN-аббр — полное название)` в русском: `РУ-аббревиатура (EN-аббр)`, напр. ОКР (OCD), ПТСР (PTSD), КПТ (CBT).
- МНН препаратов — русские МНН (сертралин, флуоксетин...); акронимы шкал (PHQ-9, GAD-7...) не переводить.

## Названия расстройств (код | AZ | RU)
"""

def w(path, rules, rows3, extra):
    lines = [rules]
    for r in rows3:
        lines.append(f"| {r[0]} | {r[1]} | {r[2]} |")
    lines.append(extra)
    path.write_text("\n".join(lines) + "\n", encoding='utf-8')
    print(path.name, len(rows3), 'disorder rows')

# EN glossary rows: prefer trilingual table EN col; fallback _codes_map en11
en_rows, seen = [], set()
for r in tri:
    if r[2]:
        en_rows.append((r[0], r[1], r[2])); seen.add(r[0])
for code, d in sorted(codes.items()):
    if code not in seen and d.get('en11'):
        en_rows.append((code, d.get('name_az', ''), d['en11']))

extra_en = "\n## Clinical terms (AZ | EN)\n" + "\n".join(
    f"| {r[0]} | {r[2]} |" for r in terms if len(r) >= 3 and r[2]) + \
    "\n\n## Fixed equivalents (AZ form | EN)\n" + "\n".join(
    f"| {r[0]} | {r[1]} |" for r in azen if r[1]) + \
    "\n\n## Abbreviations used in the book (AZ abbr | AZ full)\n" + "\n".join(
    f"| {r[0]} | {r[1]} |" for r in abbrs)

ru_rows, seen = [], set()
for r in tri:
    if r[3]:
        ru_rows.append((r[0], r[1], r[3])); seen.add(r[0])
for code, az, ru in typ_rows:
    if code not in seen and ru:
        ru_rows.append((code, az, ru))

extra_ru = "\n## Клинические термины (AZ | RU)\n" + "\n".join(
    f"| {r[0]} | {r[1]} |" for r in terms if len(r) >= 2 and r[1]) + \
    "\n\n## Аббревиатуры книги (AZ abbr | AZ полное)\n" + "\n".join(
    f"| {r[0]} | {r[1]} |" for r in abbrs)

w(OUT / 'glossary_en.md', RULES_EN, en_rows, extra_en)
w(OUT / 'glossary_ru.md', RULES_RU, ru_rows, extra_ru)
