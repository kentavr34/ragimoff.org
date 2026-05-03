#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BİRİNCİLİ → İLKİN: bulk replacement across all klinik-psixiatriya HTML files.
"""
import sys, io, os, unicodedata, glob as globmod

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = r"C:\Users\SAM\Desktop\sayt2\klinik-psixiatriya"

def apply_changes(fpath, changes):
    with open(fpath, encoding='utf-8') as f:
        html = f.read()
    html = unicodedata.normalize('NFC', html)
    orig = html
    ok = []
    miss = []
    for old, new in changes:
        if old in html:
            n = html.count(old)
            html = html.replace(old, new)
            ok.append((old[:70], n))
        else:
            miss.append(old[:70])
    if html != orig:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html)
    return ok, miss

# ── 1. Sidebar — ALL files ───────────────────────────────────────────────────
ALL_FILES = [
    # Chapter title (line 87)
    ('<span>ŞİZOFRENİYA VƏ DİGƏR BİRİNCİLİ PSİXOTİK POZUNTULAR</span>',
     '<span>ŞİZOFRENİYA VƏ DİGƏR İLKİN PSİXOTİK POZUNTULAR</span>'),
    # 6A25 sub-link display text
    ('<span class="sub-name">BİRİNCİLİ PSİXOTİK POZUNTULARIN SİMPTOM DOMENLƏRİ (',
     '<span class="sub-name">İLKİN PSİXOTİK POZUNTULARIN SİMPTOM DOMENLƏRİ ('),
    # 6A25 href — NFC variant (bolme-01..22, bolme-ps)
    ('href="bolme-02.html#6a25-birincili-psixotik-pozuntularin-simptom-domenləri-6a25"',
     'href="bolme-02.html#6a25-ilkin-psixotik-pozuntularin-simptom-domenləri-6a25"'),
    # 6A25 href — dotted-i variant (abbreviatur, elave-*, giris*, index, mugeddime, yekun)
    # i̇ = i + combining dot above (stays after NFC since no precomposed form)
    ('href="bolme-02.html#6a25-bi̇ri̇nci̇li̇-psi̇xoti̇k-pozuntularin-si̇mptom-domenləri̇-6a25"',
     'href="bolme-02.html#6a25-ilkin-psixotik-pozuntularin-simptom-domenləri-6a25"'),
]

# ── 2. bolme-02.html — heading + body text ───────────────────────────────────
BOLME02 = [
    # H2 heading id + text
    ('<h2 id="şizofreniya-və-digər-birincili-psixotik-pozuntular" class="">6A20 – 6A25 \xb7 ŞİZOFRENİYA VƏ DİGƏR BİRİNCİLİ PSİXOTİK POZUNTULAR</h2>',
     '<h2 id="şizofreniya-və-digər-ilkin-psixotik-pozuntular" class="">6A20 – 6A25 \xb7 ŞİZOFRENİYA VƏ DİGƏR İLKİN PSİXOTİK POZUNTULAR</h2>'),
    # Body text — bold lowercase
    ('<strong>birincili psixotik pozuntular</strong>',
     '<strong>ilkin psixotik pozuntular</strong>'),
    # Body text — plain lowercase
    ('XBT-11 birincili psixotik pozuntuların',
     'XBT-11 ilkin psixotik pozuntuların'),
    # H1 disorder heading (6A25) — id and text
    ('<h1 id="6a25-birincili-psixotik-pozuntularin-simptom-domenləri-6a25" class="h-disorder"><span class="icd">6A25</span> BİRİNCİLİ PSİXOTİK POZUNTULARIN SİMPTOM DOMENLƏRİ (<span class="icd">6A25</span>)</h1>',
     '<h1 id="6a25-ilkin-psixotik-pozuntularin-simptom-domenləri-6a25" class="h-disorder"><span class="icd">6A25</span> İLKİN PSİXOTİK POZUNTULARIN SİMPTOM DOMENLƏRİ (<span class="icd">6A25</span>)</h1>'),
    # Line 1323 body — "hər bir birincili psixotik pozuntu"
    ('hər bir birincili psixotik pozuntu',
     'hər bir ilkin psixotik pozuntu'),
]

# ── 3. bolme-22.html — differential diagnosis body text ─────────────────────
BOLME22 = [
    # Line 363: "birincili psixi pozuntunun"
    ('birincili psixi pozuntunun',
     'ilkin psixi pozuntunun'),
    # Line 387: "birincili psixozdan fərqli"
    ('birincili psixozdan fərqli',
     'ilkin psixozdan fərqli'),
    # Line 434: "birincili psixi pozuntu kimi"
    ('birincili psixi pozuntu kimi',
     'ilkin psixi pozuntu kimi'),
    # Line 508: table header
    ('<th>Birincili psixoz</th>',
     '<th>İlkin psixoz</th>'),
]

# ── Run ───────────────────────────────────────────────────────────────────────

all_html = sorted(globmod.glob(os.path.join(BASE, '*.html')))
total_files = 0
total_changes = 0

for fpath in all_html:
    fname = os.path.basename(fpath)
    changes = list(ALL_FILES)
    if fname == 'bolme-02.html':
        changes += BOLME02
    if fname == 'bolme-22.html':
        changes += BOLME22

    ok, miss = apply_changes(fpath, changes)
    if ok:
        total_files += 1
        for s, n in ok:
            total_changes += n
            print(f'  [{n}] {fname}: {s}')
    if miss:
        for s in miss:
            # Only report misses for bolme-02/22 specific changes
            if fname in ('bolme-02.html', 'bolme-22.html'):
                print(f'  ✗ NOT FOUND in {fname}: {s}')

print(f'\nИтог: {total_files} файлов изменено, {total_changes} замен.')
