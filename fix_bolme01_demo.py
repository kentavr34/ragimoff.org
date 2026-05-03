#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DEMO-düzəliş: bolme-01.html + bolme-02.html
Standart: XBT-11, XBT-10, DSM-5-TR — kod — İngilis adı
"""
import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = r"C:\Users\SAM\Desktop\sayt2\klinik-psixiatriya"

# ═══════════════════════════════════════════════════════════════
# bolme-01.html — bütün xbt-line sətirləri
# ═══════════════════════════════════════════════════════════════

BOLME01 = [
    # ── Bölmə başlığı (chapter header) ──────────────────────────
    # XBT-11: azərbaycanca adı → ingilis adı
    ('<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A00</span> – <span class="icd">6A0Z</span> — Neyroinkişaf pozuntuları (neurodevelopmental disorders)</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A00</span> – <span class="icd">6A0Z</span> — Neurodevelopmental disorders</div>'),

    # XBT-10: azərbaycanca qeyd → ingilis
    ('<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F70</span> – <span class="icd">F89</span>, <span class="icd">F90</span> – <span class="icd">F98</span> (qismən, dağınıq olaraq)</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F70</span> – <span class="icd">F89</span>, <span class="icd">F90</span> – <span class="icd">F98</span> — Childhood-onset mental disorders (multiple chapters)</div>'),

    # DSM-5-TR chapter: kod yoxdur → — — əlavə edilir
    ('<div class="xbt-line"><span class="xbt-lbl">DSM-5-TR:</span> Neurodevelopmental disorders</div>',
     '<div class="xbt-line"><span class="xbt-lbl">DSM-5-TR:</span> — — Neurodevelopmental disorders</div>'),

    # ── 6A00 İntellektual inkişaf pozuntusu ─────────────────────
    ('<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A00</span> — İntellektual inkişaf pozuntusu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A00</span> — Disorders of intellectual development</div>'),

    ('<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F70</span> – <span class="icd">F79</span> — Zehni gerililik</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F70</span> – <span class="icd">F79</span> — Mental retardation</div>'),

    # DSM-5-TR 319 artıq ingilis dilindədir ✓

    # ── 6A01 İnkişaf nitq və dil pozuntuları ────────────────────
    ('<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A01</span> — İnkişaf nitq və dil pozuntulari</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A01</span> — Developmental speech or language disorders</div>'),

    ('<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F80</span> — Nitqin spesifik inkişaf pozuntuları</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F80</span> — Specific developmental disorders of speech and language</div>'),

    # ── 6A02 Autizm spektri pozuntusu ───────────────────────────
    ('<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A02</span> — Autizm spektri pozuntusu (ASP)</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A02</span> — Autism spectrum disorder</div>'),

    ('<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F84.0</span> — Uşaqlıq autizmi</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F84.0</span> — Childhood autism</div>'),

    # ── 6A03 İnkişaf öyrənmə pozuntusu ─────────────────────────
    # Kod SƏHV idi (6A04 yerinə 6A03 olmalı) + azərbaycanca ad
    ('<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A04</span> — İnkişaf öyrənmə pozuntusu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A03</span> — Developmental learning disorder</div>'),

    # XBT-10 SƏHV idi (F90 yerinə F81 olmalı) + azərbaycanca ad
    ('<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F90</span> — Hiperkinetik pozuntular</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F81</span> — Specific developmental disorders of scholastic skills</div>'),

    # DSM-5-TR SƏHV idi (314.01 DDHP yerinə 315.00 öyrənmə olmalı)
    ('<div class="xbt-line"><span class="xbt-lbl">DSM-5-TR:</span> 314.01 — Attention-deficit/hyperactivity disorder</div>',
     '<div class="xbt-line"><span class="xbt-lbl">DSM-5-TR:</span> 315.00 — Specific learning disorder</div>'),

    # ── 6A04 İnkişaf hərəki koordinasiya pozuntusu ──────────────
    # Kod SƏHV idi (6A05 yerinə 6A04 olmalı) + azərbaycanca ad
    ('<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A05</span> — İnkişaf hərəki koordinasiya pozuntusu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A04</span> — Developmental motor coordination disorder</div>'),

    ('<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F82</span> — Hərəkət koordinasiyasının spesifik pozuntusu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F82</span> — Specific developmental disorder of motor function</div>'),

    # DSM-5-TR 315.4 artıq ingilis dilindədir ✓

    # ── 6A05 Diqqət defisiti və hiperaktivlik pozuntusu (DDHP) ──
    ('<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A05</span> — Diqqət defisiti və hiperaktivlik pozuntusu (DDHP)</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A05</span> — Attention deficit hyperactivity disorder</div>'),

    # XBT-10 F90 (DDHP üçün doğrudur, ancaq ad azərbaycancadır)
    # Qeyd: Bu bolme-01-də yeganə F90 sətridir ki, 6A05-ə aiddir;
    # artıq F81 ilə əvəz etdikdən sonra digər F90 → bu biri qalır
    ('<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F90</span> — Hiperkinetik pozuntular</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F90</span> — Hyperkinetic disorders</div>'),

    # ── 6A06 Stereotipik hərəkət pozuntusu ─────────────────────
    ('<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A06</span> — Stereotipik hərəkət pozuntusu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A06</span> — Stereotyped movement disorder</div>'),

    ('<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F98.4</span> — Stereotipik hərəkət pozuntusu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F98.4</span> — Stereotyped movement disorders</div>'),

    # ── 6A07 Tikli pozuntular və Tourette sindromu ───────────────
    ('<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A07</span> — Tikli pozuntular və Tourette sindromu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A07</span> — Tic disorders or Tourette syndrome</div>'),

    # XBT-10 F95.0-F95.9 artıq ingilis dilindədir ✓
    # DSM-5-TR artıq ingilis dilindədir ✓
]

# ═══════════════════════════════════════════════════════════════
# bolme-02.html — yalnız DSM-5-TR chapter header
# ═══════════════════════════════════════════════════════════════

BOLME02 = [
    ('<div class="xbt-line"><span class="xbt-lbl">DSM-5-TR:</span> Schizophrenia spectrum and other psychotic disorders</div>',
     '<div class="xbt-line"><span class="xbt-lbl">DSM-5-TR:</span> — — Schizophrenia spectrum and other psychotic disorders</div>'),
]


import unicodedata

def apply_changes(fpath, changes):
    with open(fpath, encoding='utf-8') as f:
        html = f.read()
    # İ (I + combining dot) → İ (U+0130 precomposed) — artifact from fix_xbt_style.py
    html = unicodedata.normalize('NFC', html)
    orig = html
    ok = []
    miss = []
    for old, new in changes:
        if old in html:
            html = html.replace(old, new, 1)
            ok.append(old[:70])
        else:
            miss.append(old[:70])
    if html != orig:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html)
    return ok, miss


p1 = os.path.join(BASE, 'bolme-01.html')
p2 = os.path.join(BASE, 'bolme-02.html')

print('=== bolme-01.html ===')
ok1, miss1 = apply_changes(p1, BOLME01)
for s in ok1:
    print(f'  ✓ {s}')
for s in miss1:
    print(f'  ✗ NOT FOUND: {s}')

print(f'\n=== bolme-02.html ===')
ok2, miss2 = apply_changes(p2, BOLME02)
for s in ok2:
    print(f'  ✓ {s}')
for s in miss2:
    print(f'  ✗ NOT FOUND: {s}')

print(f'\nbolme-01: {len(ok1)} dəyişdi, {len(miss1)} tapılmadı')
print(f'bolme-02: {len(ok2)} dəyişdi, {len(miss2)} tapılmadı')
