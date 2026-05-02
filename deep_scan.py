#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Глубокая проверка DOCX на артефакты, лишние символы, шаблонный мусор."""
import zipfile, re

DOCX = r"D:\BOOKS\FINAL\kp_new\KLINIK_PSIXIATRIYA.docx"

with zipfile.ZipFile(DOCX) as z:
    with z.open("word/document.xml") as f:
        xml = f.read().decode("utf-8")

paras_raw = re.split(r'</w:p>', xml)
paragraphs = []
for p in paras_raw:
    t = re.sub(r'<[^>]+>', '', p)
    t = re.sub(r'\s+', ' ', t).strip()
    if len(t) > 3:
        paragraphs.append(t)

issues = []

def report(category, para, note=""):
    issues.append((category, para[:140], note))

for i, p in enumerate(paragraphs):

    # 1. Markdown/программные артефакты
    if re.search(r'^#{1,6}\s+\w', p):
        report("MARKDOWN заголовок", p, "# ## ###...")
    if re.search(r'^\*{1,3}\w|\w\*{1,3}$', p):
        report("MARKDOWN жирный/курсив", p, "* ** ***")
    if re.search(r'^\s*[-*]\s+\w', p) and len(p) < 10:
        report("MARKDOWN список", p, "- * bullet")
    if re.search(r'```|~~~|<code>|<pre>', p, re.I):
        report("КОД блок", p, "``` ~~~")
    if re.search(r'\$\{|\{\{|\}\}|<%|%>', p):
        report("ШАБЛОН формула", p, "${} {{}} <%>")
    if re.search(r'<\s*[a-z]+\s*/?>', p, re.I) and not re.search(r'XBT|DSM|ICD', p):
        report("HTML тег", p, "<tag>")

    # 2. Странные символы
    if re.search(r'\\n|\\t|\\r', p):
        report("ESCAPE символ", p, r"\n \t \r")
    if re.search(r'\[PLACEHOLDER\]|\[TODO\]|\[INSERT\]|\[XXX\]|\[TBD\]|\[\.\.\.\]', p, re.I):
        report("PLACEHOLDER", p, "[TODO] [INSERT]")
    if re.search(r'_{3,}|={3,}|\*{3,}', p):
        report("РАЗДЕЛИТЕЛЬ артефакт", p, "___ === ***")
    if re.search(r'\bnewpage\b|\bpagebreak\b|\x0c', p, re.I):
        report("РАЗРЫВ страницы", p, "newpage")
    if p.count('→') > 3 or p.count('←') > 3:
        report("СТРЕЛКИ (много)", p, f"→{p.count('→')} ←{p.count('←')}")

    # 3. Программные формулы не по теме
    if re.search(r'font-size|font-family|color:|padding:|margin:|display:|border:', p, re.I):
        report("CSS стиль", p, "CSS свойство")
    if re.search(r'class=|id=|href=|src=|style=', p, re.I):
        report("HTML атрибут", p, "class= id= href=")
    if re.search(r'function\s*\(|var\s+\w+\s*=|const\s+\w+|console\.log|document\.', p):
        report("JavaScript", p, "JS код")

    # 4. Бессмысленные повторы символов
    if re.search(r'\.{4,}|,{3,}|!{3,}|\?{3,}', p):
        report("ПОВТОР знаков", p, ".... ,,, !!!!")

    # 5. Подозрительно короткие "параграфы" с одним символом
    if len(p.strip()) == 1 and p.strip() not in '-–—·•':
        report("ОДИНОЧНЫЙ символ", p, "одинокий знак")

    # 6. Смешение языков внутри одного предложения (не библиография)
    if re.search(r'[А-Яа-я]{3,}', p) and 'Post-sovet' not in p and 'MDB' not in p and '(' not in p:
        report("КИРИЛЛИЦА (не цитата)", p, "кирилл вне скобок")

print("=" * 70)
print(f"НАЙДЕНО ПОТЕНЦИАЛЬНЫХ ПРОБЛЕМ: {len(issues)}")
print("=" * 70)

# Группируем по категории
from collections import defaultdict
by_cat = defaultdict(list)
for cat, para, note in issues:
    by_cat[cat].append((para, note))

for cat, items in sorted(by_cat.items()):
    print(f"\n▶ {cat} ({len(items)} шт.):")
    for para, note in items[:8]:  # max 8 на категорию
        print(f"   {para[:120]}")
    if len(items) > 8:
        print(f"   ... ещё {len(items)-8}")
