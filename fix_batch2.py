#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch fix:
1. index.html — remove "Növbəti addım" instruction paragraph
2. index.html — bottom nav "Giriş" → "Kitab haqqında"
3. giris.html — H1 → "KİTAB HAQQINDA"; remove H2 "Bu kitab haqqında"
4. All HTML — nav label "Titul + Önsöz" → "Önsöz"
5. All HTML — ALL_PAGES index title → "Önsöz"
6. abbreviatur.html — fill Rəsmi column with verification results
"""
import sys, io, os, glob, re, unicodedata

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r"C:\Users\SAM\Desktop\sayt2\klinik-psixiatriya"
def nfc(s): return unicodedata.normalize('NFC', s)

# ════════════════════════════════════════════════════════
# STEP 1 + 2 — index.html
# ════════════════════════════════════════════════════════
idx_path = os.path.join(BASE, 'index.html')
with open(idx_path, encoding='utf-8') as f:
    idx = f.read()
idx = nfc(idx)

# Remove instruction paragraph
idx = re.sub(
    r'<p>\s*<em>\s*Növbəti addım:.*?</em>\s*</p>\s*',
    '',
    idx, count=1, flags=re.DOTALL
)

# Bottom nav: "Giriş" → "Kitab haqqında"
idx = idx.replace(
    '<span class="pnav-title">Giriş</span>',
    '<span class="pnav-title">Kitab haqqında</span>',
    1
)

with open(idx_path, 'w', encoding='utf-8') as f:
    f.write(idx)
print('OK index.html — instruction removed, bottom nav fixed')

# ════════════════════════════════════════════════════════
# STEP 3 — giris.html
# ════════════════════════════════════════════════════════
giris_path = os.path.join(BASE, 'giris.html')
with open(giris_path, encoding='utf-8') as f:
    giris = f.read()
giris = nfc(giris)

# H1 → uppercase
giris = giris.replace(
    '<h1 id="kitab-haqqinda" class="h-section">Kitab Haqqında</h1>',
    '<h1 id="kitab-haqqinda" class="h-section">KİTAB HAQQINDA</h1>',
    1
)

# Remove H2 "Bu kitab haqqında"
giris = re.sub(
    r'<h2[^>]*id="bu-kitab-haqqında"[^>]*>Bu kitab haqqında</h2>\s*',
    '',
    giris, count=1
)

with open(giris_path, 'w', encoding='utf-8') as f:
    f.write(giris)
print('OK giris.html — H1 → KİTAB HAQQINDA, Bu kitab haqqında removed')

# ════════════════════════════════════════════════════════
# STEP 4 + 5 — All HTML files: nav label + ALL_PAGES
# ════════════════════════════════════════════════════════
nav_updated = 0
allpages_updated = 0

for fpath in sorted(glob.glob(os.path.join(BASE, '*.html'))):
    with open(fpath, encoding='utf-8') as f:
        html = f.read()
    html = nfc(html)
    original = html

    # Nav label
    html = html.replace(
        nfc('<span>Titul + Önsöz</span>'),
        nfc('<span>Önsöz</span>'),
        1
    )

    # ALL_PAGES: index title
    # JSON has: "slug": "index", "title": "Titul + Önsöz"
    html = html.replace(
        '"slug": "index", "title": "Titul + \\u00d6ns\\u00f6z"',
        '"slug": "index", "title": "\\u00d6ns\\u00f6z"',
        1
    )

    if html != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html)
        nav_updated += 1

print(f'OK nav + ALL_PAGES "Önsöz": {nav_updated} files')

# ════════════════════════════════════════════════════════
# STEP 6 — abbreviatur.html: fill Rəsmi column
# ════════════════════════════════════════════════════════
# Verification results: (kod_fragment_in_AZ_cell, rasmi_html)
# ✓ = green check, ✗ official_name = red cross + official term, — = pending

OK  = '<span style="color:#2a9d5c;font-weight:700">✓</span>'
def NO(term): return f'<span style="color:#e63946;font-weight:700">✗</span> <em>{term}</em>'

RASMI = {
    # kod: rasmi_html
    # ✓ confirmed matches
    '6A02': OK,   # Autizm Spektri Pozuntusu
    '6A20': OK,   # Şizofreniya
    '6A21': OK,   # Şizoaffektiv Pozuntu
    '6A22': OK,   # Şizotipik Pozuntu
    '6A24': OK,   # Sayıqlama Pozuntusu
    '6A40': OK,   # Katatoniya
    '6B02': OK,   # Aqorafobiya
    '6B04': OK,   # Spesifik Fobiya
    '6B20': OK,   # OKP
    '6B40': OK,   # PTSP
    '6B41': OK,   # Kompleks PTSP
    '6B61': OK,   # Dissosiativ Amneziya
    '6B65': OK,   # Dissosiativ Şəxsiyyət Pozuntusu
    '6C00': OK,   # Enurez
    '6C01': OK,   # Enkoprez
    '6C48': OK,   # Nikotin Asılılığı
    '6D10': OK,   # Şəxsiyyət Pozuntusu
    '6D70-demensiya-ümumi': OK,  # Demensiya (ümumi)
    '6D70-alzheimer': OK,         # Alzheimer Demensiyası
    '6E20-ppd': OK,   # Doğuşdan Sonrakı Depressiya
    # ✗ confirmed differences
    '6A05': NO('Diqqət çatışmazlığı və hiperaktivlik pozuntusu (DÇHP)'),
    '6A62': NO('Distimiya'),
    '6A70': NO('Bipolyar pozuntu, I tip'),
    '6A71': NO('Bipolyar pozuntu, II tip'),
    '6A72': NO('Tsiklotimiya / Siklotimiya'),
    '6B00': NO('Generalizə edilmiş həyəcan pozuntusu'),
    '6B01': NO('Sosial fobiya (XBT-10: F40.1)'),
    '6B03': NO('Epizodik paroksizmal həyəcan (XBT-10: F41.0)'),
    '6B21': NO('Dismorfofobiya (XBT-10: F45.2)'),
    '6B23': NO('İpoxondrik pozuntu (XBT-10: F45.2)'),
    '6B42': NO('Uzanmış hüzn pozuntusu'),
    '6B43': NO('Adaptasiya pozuntusu'),
    '6B60': NO('Dissosiativ (konversiya) pozuntu (XBT-10: F44)'),
    '6B80': NO('Nevrogen anoreksiya (XBT-10: F50.0)'),
    '6B81': NO('Nevrogen bulimiya (XBT-10: F50.2)'),
    '6C20': NO('Somatikləşmiş / somatoform pozuntu (XBT-10: F45)'),
    '6C40': NO('Alkoqoldan asılılıq sindromu (XBT-10: F10.2)'),
    '6C71': NO('Kleptomaniya'),
    '6C72': NO('Piromaniya'),
    '6D11': NO('Sərhəd şəxsiyyət pozuntusu'),
    '6D75': NO('Deliriy'),
}

abbr_path = os.path.join(BASE, 'abbreviatur.html')
with open(abbr_path, encoding='utf-8') as f:
    abbr = f.read()
abbr = nfc(abbr)

# The pozuntular table rows look like:
# <tr><td class="kod-cell">6A00</td><td>...</td><td>...</td><td>...</td><td class="rasmi-cell">—</td></tr>
# We need to replace the rasmi-cell content based on the kod.

def replace_rasmi(html, kod, rasmi_html):
    # Match the row that starts with this kod
    pattern = (
        r'(<tr><td class="kod-cell">' + re.escape(kod) + r'</td>'
        r'.*?<td class="rasmi-cell">)([^<]*)(</td></tr>)'
    )
    replacement = r'\g<1>' + rasmi_html + r'\3'
    new_html, n = re.subn(pattern, replacement, html, count=1, flags=re.DOTALL)
    return new_html, n

updated_rows = 0

# Handle simple code-based replacements
simple_codes = {k: v for k, v in RASMI.items() if '-' not in k}
for kod, rasmi_html in simple_codes.items():
    abbr, n = replace_rasmi(abbr, kod, nfc(rasmi_html))
    if n:
        updated_rows += 1

# Handle special multi-row codes (6D70, 6E20 have multiple rows)
# 6D70 row 1: "Demensiya — Ümumi Prinsiplər"
abbr = re.sub(
    r'(<tr><td class="kod-cell">6D70</td><td>Demensiya — Ümumi.*?<td class="rasmi-cell">)(—)(</td></tr>)',
    r'\g<1>' + nfc(OK) + r'\3',
    abbr, count=1, flags=re.DOTALL
)
# 6D70 row 2: "Alzheimer"
abbr = re.sub(
    r'(<tr><td class="kod-cell">6D70</td><td>Alzheimer.*?<td class="rasmi-cell">)(—)(</td></tr>)',
    r'\g<1>' + nfc(OK) + r'\3',
    abbr, count=1, flags=re.DOTALL
)
# 6E20 PPD row
abbr = re.sub(
    r'(<tr><td class="kod-cell">6E20</td><td>Doğuşdan Sonrakı Depressiya.*?<td class="rasmi-cell">)(—)(</td></tr>)',
    r'\g<1>' + nfc(OK) + r'\3',
    abbr, count=1, flags=re.DOTALL
)

with open(abbr_path, 'w', encoding='utf-8') as f:
    f.write(abbr)
print(f'OK abbreviatur.html — Rəsmi column filled ({updated_rows} simple codes updated)')
print('\nDone.')
