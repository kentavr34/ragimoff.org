#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Читаем DOCX, извлекаем заголовки и параграфы первого уровня,
ищем кириллицу и сравниваем с текущим сайтом.
"""
import zipfile, re, os

DOCX = r"D:\BOOKS\FINAL\kp_new\KLINIK_PSIXIATRIYA.docx"

# DOCX — это ZIP с XML внутри
with zipfile.ZipFile(DOCX) as z:
    with z.open("word/document.xml") as f:
        xml = f.read().decode("utf-8")

# Удалить XML-теги, оставить текст
text_clean = re.sub(r'<[^>]+>', ' ', xml)
text_clean = re.sub(r'\s+', ' ', text_clean).strip()

# Разбить по параграфам через </w:p>
paras_raw = re.split(r'</w:p>', xml)

paragraphs = []
for p in paras_raw:
    t = re.sub(r'<[^>]+>', '', p)
    t = re.sub(r'\s+', ' ', t).strip()
    if t:
        paragraphs.append(t)

# ─── Кириллица ──────────────────────────────────────────────────────────────
CYR = re.compile(r'[А-Яа-яЁё]{2,}')

print("=" * 70)
print("КИРИЛЛИЦА В ТЕКСТЕ:")
print("=" * 70)
cyr_found = []
for i, p in enumerate(paragraphs):
    matches = CYR.findall(p)
    if matches:
        cyr_found.append((i, p[:120], matches))

if cyr_found:
    for i, snippet, matches in cyr_found[:60]:
        print(f"  [{i:04d}] {snippet}")
        print(f"         → кирилл: {matches}")
        print()
else:
    print("  Кириллица не найдена.")

# ─── Заголовки бölmə ─────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("ЗАГОЛОВКИ BÖLMƏ / БОЛМƏ:")
print("=" * 70)
BOLME = re.compile(r'BÖLM[ƏE]\s*\d+', re.IGNORECASE)
for i, p in enumerate(paragraphs):
    if BOLME.search(p):
        print(f"  [{i:04d}] {p[:140]}")

# ─── Сохранить весь текст для ручной проверки ────────────────────────────────
out = r"D:\BOOKS\FINAL\kp_new\extracted_text.txt"
with open(out, 'w', encoding='utf-8') as f:
    for i, p in enumerate(paragraphs):
        if len(p) > 3:
            f.write(f"[{i:04d}] {p}\n")

print(f"\nПолный текст сохранён: {out}")
print(f"Всего параграфов: {len(paragraphs)}")
