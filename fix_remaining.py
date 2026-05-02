#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Точечные исправления после fix_all.py"""
import re, glob, os

BASE = r"C:\Users\SAM\Desktop\sayt2\klinik-psixiatriya"

# ─── 1. Исправить h2 в bolme-13 (неверный код 6C72–ni → 6C70–6C7Z) ──────────
f13 = os.path.join(BASE, "bolme-13.html")
with open(f13, encoding='utf-8') as f:
    html = f.read()
html = html.replace(
    '6C72–ni · İMPULS NƏZARƏTİ POZUNTULARI',
    '6C70–6C7Z · İMPULS NƏZARƏTİ POZUNTULARI'
)
with open(f13, 'w', encoding='utf-8') as f:
    f.write(html)
print("bolme-13: h2 исправлен → 6C70–6C7Z")

# ─── 2. Добавить h2 коды для bolme без code_range ────────────────────────────
MANUAL = {
    'bolme-02': ('6A20–6A25', 'ŞİZOFRENİYA VƏ DİGƏR BİRİNCİLİ PSİXOTİK POZUNTULAR'),
    'bolme-17': ('6D50–6D51', 'SÜNI (FAKTİTİOZ) POZUNTULAR'),
    'bolme-21': ('6E20',      'HAMİLƏLİK VƏ DOĞUŞ DÖVRLƏ ƏLAQƏLİ PSİXİ POZUNTULAR'),
    'bolme-ps': ('6E40',      'DİGƏR XƏSTƏLİKLƏRƏ TƏSİR EDƏN PSİXOLOJİ VƏ DAVRANIŞ AMİLLƏRİ'),
}

H2_BOLME_RE = re.compile(r'<h1[^>]*class="h-bolme"[^>]*>')

for slug, (code, title) in MANUAL.items():
    fpath = os.path.join(BASE, f"{slug}.html")
    with open(fpath, encoding='utf-8') as f:
        html = f.read()

    m = H2_BOLME_RE.search(html)
    if not m:
        print(f"  ПРОПУСК {slug}: нет h1.h-bolme")
        continue

    before = html[:m.end()]
    after  = html[m.end():]

    new_heading = f"{code} · {title}"
    pat = re.compile(r'(<h2[^>]*>)(' + re.escape(title) + r')(</h2>)')
    new_after, count = pat.subn(lambda m: m.group(1) + new_heading + m.group(3), after, count=1)

    if count:
        html = before + new_after
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"  {slug}: h2 → '{new_heading}'")
    else:
        # может уже обновлён
        if code in after[:2000]:
            print(f"  {slug}: h2 уже содержит код")
        else:
            print(f"  {slug}: h2 НЕ найден! Ищем первый h2 после h-bolme...")
            # debug
            m2 = re.search(r'<h2[^>]*>([^<]+)</h2>', after)
            if m2:
                print(f"    Первый h2: {repr(m2.group(1)[:80])}")

# ─── 3. Обновить nav-code в сайдбаре для bolme-02, 17, 21, ps ───────────────
# В сайдбаре эти главы сейчас без nav-code (code_range был пустым).
# Нужно добавить nav-code span в соответствующие nav-link

# Паттерн в сайдбаре:
# <a href="bolme-02.html" class="nav-link is-bolme" data-slug="bolme-02">
#     <span>ŞİZOFRENİYA VƏ DİGƏR BİRİNCİLİ PSİXOTİK POZUNTULAR</span>
# </a>
# → добавить: <span class='nav-code'>6A20–6A25</span> перед span с названием

all_html = sorted(glob.glob(os.path.join(BASE, "*.html")))
nav_fixes = 0

for fpath in all_html:
    with open(fpath, encoding='utf-8') as f:
        html = f.read()
    original = html

    for slug, (code, title) in MANUAL.items():
        # ищем nav-link этой главы где нет nav-code
        pat = re.compile(
            r'(<a href="' + slug + r'\.html" class="nav-link is-bolme" data-slug="' + slug + r'">\s*\n\s*)(<span>' + re.escape(title) + r'</span>)',
            re.DOTALL
        )
        def add_code(m, code=code):
            return m.group(1) + f"<span class='nav-code'>{code}</span>\n    " + m.group(2)
        html = pat.sub(add_code, html)

    if html != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html)
        nav_fixes += 1

print(f"\nNav-code добавлен в {nav_fixes} файлов")

# ─── 4. index.html: слить два h1 в один ──────────────────────────────────────
idx = os.path.join(BASE, "index.html")
with open(idx, encoding='utf-8') as f:
    html = f.read()
original = html

# Два отдельных h1 с одним классом
# <h1 id="k-l-i̇-n-i̇-k" class="h-section">K L İ N İ K</h1>
# <h1 id="p-s-i̇-x-i̇-a-t-r-i̇-y-a" class="h-section">P S İ X İ A T R İ Y A</h1>
# → <h1 id="k-l-i̇-n-i̇-k" class="h-section">K L İ N İ K  P S İ X İ A T R İ Y A</h1>

html = re.sub(
    r'<h1[^>]*class="h-section"[^>]*>K L [İI] N [İI] K</h1>\s*\n\s*<h1[^>]*class="h-section"[^>]*>P S [İI] X [İI] A T R [İI] Y A</h1>',
    '<h1 id="k-l-i̇-n-i̇-k" class="h-section">K L İ N İ K  P S İ X İ A T R İ Y A</h1>',
    html
)

if html != original:
    with open(idx, 'w', encoding='utf-8') as f:
        f.write(html)
    print("index.html: h1 объединён")
else:
    print("index.html: паттерн не сработал — проверяю вручную")
    pos = html.find('K L ')
    if pos >= 0:
        print(repr(html[pos-30:pos+120]))

print("\nГотово.")
