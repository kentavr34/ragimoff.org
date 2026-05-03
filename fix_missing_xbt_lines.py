#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adds missing XBT-10 and DSM-5-TR lines to disorder sections.
Each fix: (filename, old_str, new_str)
"""
import sys, io, os, unicodedata

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r"C:\Users\SAM\Desktop\sayt2\klinik-psixiatriya"

def icd(*codes):
    return ', '.join(f'<span class="icd">{c}</span>' for c in codes)

def xbt10(code, name):
    return f'<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">{code}</span> — {name}</div>'

def dsm(code, name):
    return f'<div class="xbt-line"><span class="xbt-lbl">DSM-5-TR:</span> <span class="icd">{code}</span> — {name}</div>'

def xbt11(code, name):
    return f'<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">{code}</span> — {name}</div>'

# Each tuple: (file, old_str, new_str)
FIXES = [

    # ── bolme-03: Catatonia ────────────────────────────────────────────────────
    ('bolme-03.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A40</span> — Catatonia</div>\n<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F06.1</span> (organic catatonic disorder); <span class="icd">F20.2</span> (catatonic schizophrenia — abolished); <span class="icd">F30</span> – <span class="icd">F33</span> (catatonic features in affective disorders)</div>\n<hr>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A40</span> — Catatonia</div>\n'
     + '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F06.1</span> (organic catatonic disorder); <span class="icd">F20.2</span> (catatonic schizophrenia — abolished); <span class="icd">F30</span> – <span class="icd">F33</span> (catatonic features in affective disorders)</div>\n'
     + dsm('293.89', 'Catatonia (associated with another mental disorder / due to another medical condition)') + '\n'
     + '<hr>'),

    # ── bolme-10: Enuresis ────────────────────────────────────────────────────
    ('bolme-10.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6C00</span> — Enuresis</div>\n<hr>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6C00</span> — Enuresis</div>\n'
     + xbt10('F98.0', 'Enuresis (non-organic)') + '\n'
     + dsm('307.6', 'Enuresis') + '\n'
     + '<hr>'),

    # ── bolme-10: Encopresis ─────────────────────────────────────────────────
    ('bolme-10.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6C01</span> — Encopresis</div>\n<hr>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6C01</span> — Encopresis</div>\n'
     + xbt10('F98.1', 'Encopresis (non-organic)') + '\n'
     + dsm('307.7', 'Encopresis') + '\n'
     + '<hr>'),

    # ── bolme-17: Factitious on self ──────────────────────────────────────────
    ('bolme-17.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6D50</span> — Factitious disorder imposed on self</div>\n<hr>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6D50</span> — Factitious disorder imposed on self</div>\n'
     + xbt10('F68.1', 'Intentional production or feigning of symptoms or disabilities [factitious disorder]') + '\n'
     + dsm('300.19', 'Factitious disorder imposed on self') + '\n'
     + '<hr>'),

    # ── bolme-20: Mild neurocognitive disorder ────────────────────────────────
    ('bolme-20.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6D71</span> — Mild neurocognitive disorder</div>\n<hr>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6D71</span> — Mild neurocognitive disorder</div>\n'
     + xbt10('F06.7', 'Mild cognitive disorder') + '\n'
     + dsm('331.83', 'Mild neurocognitive disorder') + '\n'
     + '<hr>'),

    # ── bolme-20: Alzheimer dementia ─────────────────────────────────────────
    ('bolme-20.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6D70</span> — Dementia due to Alzheimer\'s disease</div>\n<hr>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6D70</span> — Dementia due to Alzheimer\'s disease</div>\n'
     + xbt10('F00', 'Dementia in Alzheimer\'s disease') + '\n'
     + dsm('331.0', 'Major neurocognitive disorder due to Alzheimer\'s disease') + '\n'
     + '<hr>'),

    # ── bolme-20: Other dementia forms ────────────────────────────────────────
    ('bolme-20.html',
     '<h1 id="6d7z-digər-demensiya-formalari" class="h-disorder">6D7Z DİGƏR DEMENSİYA FORMALARI</h1>\n<hr>',
     '<h1 id="6d7z-digər-demensiya-formalari" class="h-disorder">6D7Z DİGƏR DEMENSİYA FORMALARI</h1>\n'
     + xbt11('6D80', 'Dementia due to other medical conditions') + '\n'
     + xbt10('F01', 'Vascular dementia') + '\n'
     + dsm('290', 'Vascular dementia / Other specified neurocognitive disorders') + '\n'
     + '<hr>'),

    # ── bolme-21: 6E20 prenatal (hamiləlik dövründə) ──────────────────────────
    ('bolme-21.html',
     '<h1 id="6e20-hamiləlik-dövründə-psixi-pozuntular" class="h-disorder"><span class="icd">6E20</span> HAMİLƏLİK DÖVRÜNDƏ PSİXİ POZUNTULAR</h1>\n<hr>',
     '<h1 id="6e20-hamiləlik-dövründə-psixi-pozuntular" class="h-disorder"><span class="icd">6E20</span> HAMİLƏLİK DÖVRÜNDƏ PSİXİ POZUNTULAR</h1>\n'
     + xbt11('6E20', 'Mental or behavioural disorders associated with pregnancy, childbirth or the puerperium') + '\n'
     + xbt10('F53', 'Mental and behavioural disorders associated with the puerperium') + '\n'
     + dsm('296', 'Peripartum onset specifier (applied to MDD and bipolar disorders)') + '\n'
     + '<hr>'),

    # ── bolme-21: 6E20.0 Baby blues ───────────────────────────────────────────
    ('bolme-21.html',
     '<h1 id="6e200-erkən-doğuşdan-sonraki-emosional-reaksiya-baby-blues" class="h-disorder"><span class="icd">6E20.0</span> ERKƏN DOĞUŞDAN SONRAKI EMOSIONAL REAKSİYA (&quot;Baby blues&quot;)</h1>\n<hr>',
     '<h1 id="6e200-erkən-doğuşdan-sonraki-emosional-reaksiya-baby-blues" class="h-disorder"><span class="icd">6E20.0</span> ERKƏN DOĞUŞDAN SONRAKI EMOSIONAL REAKSİYA (&quot;Baby blues&quot;)</h1>\n'
     + xbt11('6E20.0', 'Postpartum mood disturbance (baby blues) — normal transient reaction, not a disorder') + '\n'
     + xbt10('F53.0', 'Mild mental and behavioural disorders associated with the puerperium') + '\n'
     + '<div class="xbt-line"><span class="xbt-lbl">DSM-5-TR:</span> — — Not a DSM-5-TR diagnosis (normal transient postpartum reaction)</div>\n'
     + '<hr>'),

    # ── bolme-21: 6E20 PPD — fix DSM-5-TR line ────────────────────────────────
    ('bolme-21.html',
     '<div class="xbt-line"><span class="xbt-lbl">DSM-5-TR:</span> — — postpartum depression / specifier</div>',
     dsm('296.xx', 'Major depressive disorder with peripartum onset specifier')),

    # ── bolme-21: 6E21 — fix wrong XBT-11 label on F53.1 → XBT-10 ─────────────
    ('bolme-21.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">F53.1</span> — Severe mental and behavioural disorders associated with the puerperium</div>',
     xbt10('F53.1', 'Severe mental and behavioural disorders associated with the puerperium')),

    # ── bolme-21: 6E20 postpartum anxiety/OCD/PTSD ────────────────────────────
    ('bolme-21.html',
     '<h1 id="6e20-doğuşdan-sonraki-təşviş-okp-ptsp" class="h-disorder"><span class="icd">6E20</span> DOĞUŞDAN SONRAKI TƏŞVİŞ, OKP, PTSP</h1>\n<hr>',
     '<h1 id="6e20-doğuşdan-sonraki-təşviş-okp-ptsp" class="h-disorder"><span class="icd">6E20</span> DOĞUŞDAN SONRAKI TƏŞVİŞ, OKP, PTSP</h1>\n'
     + xbt11('6E20', 'Mental or behavioural disorders associated with pregnancy, childbirth or the puerperium') + '\n'
     + '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F40</span>–<span class="icd">F41</span> (anxiety), <span class="icd">F42</span> (OCD), <span class="icd">F43.1</span> (PTSD) — with postpartum onset</div>\n'
     + '<div class="xbt-line"><span class="xbt-lbl">DSM-5-TR:</span> <span class="icd">300</span>, <span class="icd">309.81</span> — Anxiety/OCD/PTSD with peripartum onset specifier</div>\n'
     + '<hr>'),

    # ── bolme-21: 6E2Z Azerbaijan context section ─────────────────────────────
    ('bolme-21.html',
     '<h1 id="6e2z-azərbaycan-konteksti-və-ümumi-müalicə-prinsipləri" class="h-disorder">6E2Z AZƏRBAYCAN KONTEKSTİ VƏ ÜMUMİ MÜALİCƏ PRİNSİPLƏRİ</h1>\n<hr>',
     '<h1 id="6e2z-azərbaycan-konteksti-və-ümumi-müalicə-prinsipləri" class="h-disorder">6E2Z AZƏRBAYCAN KONTEKSTİ VƏ ÜMUMİ MÜALİCƏ PRİNSİPLƏRİ</h1>\n'
     + xbt11('6E2Z', 'Other specified mental or behavioural disorders associated with pregnancy, childbirth or the puerperium') + '\n'
     + xbt10('F53.8', 'Other mental and behavioural disorders associated with the puerperium') + '\n'
     + '<div class="xbt-line"><span class="xbt-lbl">DSM-5-TR:</span> — — No direct equivalent (clinical context section)</div>\n'
     + '<hr>'),

    # ── bolme-04: 6A8Z mood symptom presentations ─────────────────────────────
    ('bolme-04.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A80</span> — Symptom presentations of mood episodes</div>\n<hr>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A80</span> — Symptom presentations of mood episodes</div>\n'
     + xbt10('F30', 'Manic episode (symptom specifiers)') + '\n'
     + dsm('296', 'Mood episode specifiers (severity, psychotic features, course)') + '\n'
     + '<hr>'),

    # ── bolme-07: 6B4Z other stress-related ───────────────────────────────────
    ('bolme-07.html',
     '<h1 id="6b4z-digər-stress-əlaqəli-pozuntular" class="h-disorder">6B4Z DİGƏR STRESS ƏLAQƏLİ POZUNTULAR</h1>\n<hr>',
     '<h1 id="6b4z-digər-stress-əlaqəli-pozuntular" class="h-disorder">6B4Z DİGƏR STRESS ƏLAQƏLİ POZUNTULAR</h1>\n'
     + xbt11('6B4Z', 'Unspecified disorder specifically associated with stress') + '\n'
     + xbt10('F43.9', 'Reaction to severe stress, unspecified') + '\n'
     + dsm('309.9', 'Adjustment disorder, unspecified') + '\n'
     + '<hr>'),

    # ── bolme-15: 6D10.0 personality disorder severity ───────────────────────
    ('bolme-15.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6D10</span> — Severity of personality disorder</div>\n<hr>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6D10</span> — Severity of personality disorder</div>\n'
     + xbt10('F60.9', 'Personality disorder, unspecified (no severity specifier in ICD-10)') + '\n'
     + '<div class="xbt-line"><span class="xbt-lbl">DSM-5-TR:</span> — — Severity assessed via Level of Personality Functioning Scale (LPFS, Section III AMPD)</div>\n'
     + '<hr>'),

    # ── bolme-15: 6D10.1 personality trait domains ───────────────────────────
    ('bolme-15.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6D11</span> — Personality trait domains</div>\n<hr>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6D11</span> — Personality trait domains</div>\n'
     + '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F60</span>–<span class="icd">F69</span> — Personality disorders (categorical types; no trait domain specifier in ICD-10)</div>\n'
     + '<div class="xbt-line"><span class="xbt-lbl">DSM-5-TR:</span> — — Trait domains assessed via AMPD (Section III); no formal categorical code</div>\n'
     + '<hr>'),

    # ── bolme-15: 6D10 ICD-10→ICD-11 conversion table section ───────────────
    ('bolme-15.html',
     '<h1 id="6d10-xbt-10-kateqoriyalarinin-xbt-11-ə-çevrilməsi" class="h-disorder"><span class="icd">6D10</span> XBT-10 KATEQORİYALARININ XBT-11-Ə ÇEVRİLMƏSİ</h1>\n<p><strong>Klinik istifadə üçün çevirici cədvəl</strong></p>\n<hr>',
     '<h1 id="6d10-xbt-10-kateqoriyalarinin-xbt-11-ə-çevrilməsi" class="h-disorder"><span class="icd">6D10</span> XBT-10 KATEQORİYALARININ XBT-11-Ə ÇEVRİLMƏSİ</h1>\n'
     + '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F60</span>–<span class="icd">F69</span> — Personality disorders (see conversion table below)</div>\n'
     + '<div class="xbt-line"><span class="xbt-lbl">DSM-5-TR:</span> <span class="icd">301.x</span> — Personality disorders (DSM-5-TR Section II categorical)</div>\n'
     + '<p><strong>Klinik istifadə üçün çevirici cədvəl</strong></p>\n<hr>'),

    # ── bolme-16: 6D3Z other paraphilic disorders ────────────────────────────
    ('bolme-16.html',
     '<h1 id="6d3z-digər-parafilik-pozuntular" class="h-disorder">6D3Z DİGƏR PARAFİLİK POZUNTULAR</h1>\n<hr>',
     '<h1 id="6d3z-digər-parafilik-pozuntular" class="h-disorder">6D3Z DİGƏR PARAFİLİK POZUNTULAR</h1>\n'
     + xbt11('6D3Z', 'Other specified paraphilic disorder') + '\n'
     + xbt10('F65.8', 'Other disorders of sexual preference') + '\n'
     + dsm('302.89', 'Other specified paraphilic disorder') + '\n'
     + '<hr>'),

    # ── bolme-12: Gaming disorder DSM-5-TR — update to mention gaming status ──
    ('bolme-12.html',
     '<div class="xbt-line"><span class="xbt-lbl">DSM-5-TR:</span> <span class="icd">312.31</span> — Gambling disorder</div>\n<hr>',
     '<div class="xbt-line"><span class="xbt-lbl">DSM-5-TR:</span> <span class="icd">312.31</span> — Gambling disorder / Gaming disorder (Internet Gaming Disorder — Section III, condition for further study; not formally coded)</div>\n'
     + '<hr>'),

]

total = 0
file_data = {}

for fname, old, new in FIXES:
    fpath = os.path.join(BASE, fname)
    if fname not in file_data:
        with open(fpath, encoding='utf-8') as f:
            html = f.read()
        file_data[fname] = unicodedata.normalize('NFC', html)

    html = file_data[fname]
    old_n = unicodedata.normalize('NFC', old)
    new_n = unicodedata.normalize('NFC', new)

    if old_n in html:
        file_data[fname] = html.replace(old_n, new_n, 1)
        print(f'  OK {fname}: {old[:70].strip()}')
        total += 1
    else:
        print(f'  MISS {fname}: {old[:70].strip()}')

# Write files
written = 0
for fname, html in file_data.items():
    fpath = os.path.join(BASE, fname)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)
    written += 1
    print(f'  >> {fname} written')

print(f'\nDone. {total} fixes in {written} files.')
