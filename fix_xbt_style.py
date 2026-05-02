#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Унификация форматирования XBT-линий и заголовков глав.
Правила:
  1. H2 заголовки глав: CODE – CODE · TITLE (пробелы вокруг en-dash)
  2. XBT диапазоны: код1</span> – <span class="icd">код2</span>
  3. Имена после — : sentence case (первая буква заглавная, остальные строчные)
  4. Аббревиатуры в скобках: (Gtp) → (GTP)
"""
import re, glob, os

BASE = r"C:\Users\SAM\Desktop\sayt2\klinik-psixiatriya"

# Правильные имена собственные — сохраняем регистр
PROPER_NOUNS = {
    "alzheimer", "parkinson", "tourette", "lewy", "korsakoff",
    "huntington", "pick", "freud", "briquet", "asperger",
    "stevens-johnson", "creutzfeldt-jakob", "rett", "prader-willi",
    "angelman", "klinefelter", "wilson", "wernicke"
}

def fix_abbrev_parens(text):
    """(Gtp) → (GTP), (Asp) → (ASP) и т.д."""
    def upper_paren(m):
        inner = m.group(1)
        # Аббревиатура: 2-6 букв, смешанный регистр (не ALL CAPS уже)
        if 2 <= len(inner) <= 7 and inner.isalpha() and not inner.isupper():
            return "(" + inner.upper() + ")"
        return m.group(0)
    return re.sub(r'\(([A-ZÇĞİÖŞÜa-zçğıöşü]{2,7})\)', upper_paren, text)

def sentence_case_name(text):
    """Преобразует имя к sentence case, сохраняет собственные имена и ALL-CAPS."""
    if not text:
        return text
    words = text.split()
    result = []
    for i, word in enumerate(words):
        # Скобки с аббревиатурой — уже обработаны выше, оставляем
        if word.startswith('(') and word.endswith(')'):
            result.append(word)
            continue
        # Слово в квадратных скобках — оставляем
        if word.startswith('[') and word.endswith(']'):
            result.append(word)
            continue
        # ALL CAPS слово (аббревиатура: XBT, ICD, DSM, CBT и т.д.)
        if word.isupper() and len(word) >= 2:
            result.append(word)
            continue
        # Проверяем собственное имя
        clean = word.strip('.,;:!?()')
        if clean.lower() in PROPER_NOUNS:
            result.append(clean[0].upper() + clean[1:].lower() + word[len(clean):])
            continue
        # Первое слово — заглавная первая буква
        if i == 0:
            lower = word.lower()
            result.append(lower[0].upper() + lower[1:] if lower else word)
        else:
            result.append(word.lower())
    return ' '.join(result)

def process_xbt_name(after_dash):
    """Обрабатывает имя после — в xbt-line."""
    after_dash = fix_abbrev_parens(after_dash)
    after_dash = sentence_case_name(after_dash)
    return after_dash

def fix_icd_ranges(html):
    """Добавляет пробелы вокруг en-dash между кодами в span.icd."""
    # </span>–<span class="icd"> → </span> – <span class="icd">
    html = re.sub(
        r'(</span>)\s*–\s*(<span class="icd">)',
        r'\1 – \2',
        html
    )
    # Дефис вместо en-dash
    html = re.sub(
        r'(</span>)\s*-\s*(<span class="icd">)',
        r'\1 – \2',
        html
    )
    return html

def fix_trailing_code_no_span(html):
    """
    XBT-11 chapter line: <span class="icd">6A00</span>–6A0Z —
    → <span class="icd">6A00</span> – <span class="icd">6A0Z</span> —
    """
    pattern = re.compile(
        r'(<span class="icd">)([^<]+)(</span>)\s*–\s*([A-Z0-9]{3,6})\s*(—)',
    )
    def replacer(m):
        return f'{m.group(1)}{m.group(2)}{m.group(3)} – <span class="icd">{m.group(4)}</span> {m.group(5)}'
    return pattern.sub(replacer, html)

def fix_h2_dash(html):
    """H2 заголовки: 6A00–6A0Z · → 6A00 – 6A0Z ·"""
    # Паттерн: код–код·  (с потенциально разными типами кодов)
    pattern = re.compile(
        r'(<h2[^>]*>)([A-Z0-9]{2,5})–([A-Z0-9]{3,6})\s*·'
    )
    def h2_fix(m):
        return f'{m.group(1)}{m.group(2)} – {m.group(3)} ·'
    return pattern.sub(h2_fix, html)

def fix_xbt_names_case(html):
    """
    Применяет sentence case к именам после — в xbt-line дивах.
    Только строки с <div class="xbt-line">
    """
    def fix_line(m):
        before = m.group(1)  # всё до финального —
        dash = " — "
        name = m.group(2)    # имя после —
        name = process_xbt_name(name)
        return before + dash + name + m.group(3)

    # Паттерн: xbt-line ... — NAME</div>
    pattern = re.compile(
        r'(<div class="xbt-line">.*?)\s*—\s*([^<\n][^<\n]*?)(</div>)',
        re.DOTALL
    )
    return pattern.sub(fix_line, html)

# ─── Основной цикл ────────────────────────────────────────────────────────────
all_files = sorted(glob.glob(os.path.join(BASE, "bolme-*.html")))

stats = {
    "h2_dash": 0,
    "icd_range": 0,
    "trailing_span": 0,
    "name_case": 0,
    "files": 0
}

for fpath in all_files:
    fname = os.path.basename(fpath)
    with open(fpath, encoding="utf-8") as f:
        html = f.read()
    orig = html

    # Фиксируем H2 тире
    h2_fixed = fix_h2_dash(html)
    if h2_fixed != html:
        stats["h2_dash"] += html.count("–") - h2_fixed.count("–") + 1
        html = h2_fixed

    # Фиксируем trailing code без span
    ts_fixed = fix_trailing_code_no_span(html)
    if ts_fixed != html:
        stats["trailing_span"] += 1
        html = ts_fixed

    # Фиксируем диапазоны между span.icd
    icd_fixed = fix_icd_ranges(html)
    if icd_fixed != html:
        stats["icd_range"] += 1
        html = icd_fixed

    # Sentence case имён в xbt-line
    case_fixed = fix_xbt_names_case(html)
    if case_fixed != html:
        stats["name_case"] += 1
        html = case_fixed

    if html != orig:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(html)
        stats["files"] += 1
        print(f"  OK: {fname}")

print(f"""
Изменено файлов: {stats['files']} из {len(all_files)}
  H2 тире исправлено:     {stats['h2_dash']}
  Trailing span добавлен: {stats['trailing_span']}
  ICD диапазоны:          {stats['icd_range']}
  Sentence case имён:     {stats['name_case']}
""")
