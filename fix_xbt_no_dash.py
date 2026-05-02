#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Доп. правка: sentence case для xbt-line строк без em-dash
(напр: DSM-5-TR: Anxiety Disorders → Anxiety disorders)
"""
import re, glob, os

BASE = r"C:\Users\SAM\Desktop\sayt2\klinik-psixiatriya"

def sentence_case(text):
    if not text:
        return text
    words = text.split()
    result = []
    for i, word in enumerate(words):
        if word.isupper() and len(word) >= 2:
            result.append(word)  # ALL CAPS — аббревиатуры
        elif i == 0:
            low = word.lower()
            result.append(low[0].upper() + low[1:])
        else:
            result.append(word.lower())
    return ' '.join(result)

# Паттерн: xbt-line где нет — но есть текст после </span>
PATTERN = re.compile(
    r'(<div class="xbt-line"><span class="xbt-lbl">[^<]+</span>)\s+([^<\-][^<]*?)(</div>)'
)

def fix_no_dash_line(m):
    before = m.group(1)
    text   = m.group(2).strip()
    after  = m.group(3)
    # Пропускаем строки с тире (уже обработаны)
    if '—' in text or '–' in text:
        return m.group(0)
    fixed = sentence_case(text)
    if fixed == text:
        return m.group(0)
    return before + " " + fixed + after

all_files = sorted(glob.glob(os.path.join(BASE, "bolme-*.html")))
changed = 0
for fpath in all_files:
    with open(fpath, encoding="utf-8") as f:
        html = f.read()
    orig = html
    html = PATTERN.sub(fix_no_dash_line, html)
    if html != orig:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(html)
        changed += 1
        print(f"  OK: {os.path.basename(fpath)}")

print(f"\nИзменено: {changed} файлов")
