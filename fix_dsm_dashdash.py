#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix all remaining DSM-5-TR "— —" entries that should have real codes.
"""
import sys, io, os, unicodedata

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r"C:\Users\SAM\Desktop\sayt2\klinik-psixiatriya"

FIXES = [

    # ── bolme-06: 6B22 Olfactory reference disorder ───────────────────────────
    # DSM-5-TR: Other specified OC-related disorder (olfactory reference syndrome) = 300.3
    ('bolme-06.html',
     '<div class="xbt-line"><span class="xbt-lbl">DSM-5-TR:</span> — — olfactory reference syndrome</div>',
     '<div class="xbt-line"><span class="xbt-lbl">DSM-5-TR:</span> <span class="icd">300.3</span> — Other specified obsessive-compulsive and related disorder (olfactory reference syndrome)</div>'),

    # ── bolme-07: 6B42 Prolonged grief disorder ───────────────────────────────
    # Added to DSM-5-TR in 2022 revision with code 296.99
    ('bolme-07.html',
     '<div class="xbt-line"><span class="xbt-lbl">DSM-5-TR:</span> — — prolonged grief disorder</div>',
     '<div class="xbt-line"><span class="xbt-lbl">DSM-5-TR:</span> <span class="icd">296.99</span> — Prolonged grief disorder (added in DSM-5-TR 2022)</div>'),

    # ── bolme-11: 6C21 Body integrity dysphoria ───────────────────────────────
    # Not in DSM-5-TR; coded under Other specified OC-related disorder = 300.3
    ('bolme-11.html',
     '<div class="xbt-line"><span class="xbt-lbl">DSM-5-TR:</span> — — body integrity dysphoria</div>',
     '<div class="xbt-line"><span class="xbt-lbl">DSM-5-TR:</span> <span class="icd">300.3</span> — Other specified obsessive-compulsive and related disorder (body integrity dysphoria)</div>'),

    # ── bolme-13: 6C73 Compulsive sexual behaviour disorder ───────────────────
    # Not in DSM-5-TR; coded under Other specified disruptive/impulse-control disorder = 312.89
    ('bolme-13.html',
     '<div class="xbt-line"><span class="xbt-lbl">DSM-5-TR:</span> — — Compulsive sexual behaviour disorder</div>',
     '<div class="xbt-line"><span class="xbt-lbl">DSM-5-TR:</span> <span class="icd">312.89</span> — Other specified disruptive, impulse-control, and conduct disorder (compulsive sexual behaviour)</div>'),

    # ── bolme-16: 6D36 Paedophilic disorder — THIS IS A REAL ERROR ───────────
    # Pedophilic disorder IS in DSM-5-TR with code 302.2 — not "other specified"
    ('bolme-16.html',
     '<div class="xbt-line"><span class="xbt-lbl">DSM-5-TR:</span> — — other specified paraphilic disorder</div>',
     '<div class="xbt-line"><span class="xbt-lbl">DSM-5-TR:</span> <span class="icd">302.2</span> — Pedophilic disorder</div>'),

    # ── bolme-20: 6D70 Dementia — general principles ──────────────────────────
    # Major neurocognitive disorder (unspecified etiology) = 294.10
    ('bolme-20.html',
     '<div class="xbt-line"><span class="xbt-lbl">DSM-5-TR:</span> — — mild neurocognitive disorder</div>',
     '<div class="xbt-line"><span class="xbt-lbl">DSM-5-TR:</span> <span class="icd">294.10</span> — Major neurocognitive disorder (unspecified etiology)</div>'),

    # ── bolme-15: 6D10.0 Severity — dimensional tool → closest formal code ────
    # DSM-5-TR categorical: Personality disorder, unspecified = 301.9
    ('bolme-15.html',
     '<div class="xbt-line"><span class="xbt-lbl">DSM-5-TR:</span> — — Severity assessed via Level of Personality Functioning Scale (LPFS, Section III AMPD)</div>',
     '<div class="xbt-line"><span class="xbt-lbl">DSM-5-TR:</span> <span class="icd">301.9</span> — Personality disorder, unspecified (severity assessed via LPFS, AMPD Section III)</div>'),

    # ── bolme-15: 6D10.1 Trait domains — dimensional tool → closest formal code
    ('bolme-15.html',
     '<div class="xbt-line"><span class="xbt-lbl">DSM-5-TR:</span> — — Trait domains assessed via AMPD (Section III); no formal categorical code</div>',
     '<div class="xbt-line"><span class="xbt-lbl">DSM-5-TR:</span> <span class="icd">301.9</span> — Personality disorder, unspecified (trait domains coded via AMPD, Section III)</div>'),

    # ── bolme-02: 6A25 Symptom rating scales — truly no equivalent ────────────
    # Dimensional assessment tool — keep informative note, but add closest code
    ('bolme-02.html',
     '<div class="xbt-line"><span class="xbt-lbl">DSM-5-TR:</span> — — No direct equivalent (dimensional assessment; see PANSS / clinician-rated dimensions)</div>',
     '<div class="xbt-line"><span class="xbt-lbl">DSM-5-TR:</span> <span class="icd">298.9</span> — Unspecified schizophrenia spectrum and other psychotic disorder (dimensional rating via PANSS / clinician-rated dimensions)</div>'),

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
        print(f'  OK {fname}: {old[60:100].strip()}')
        total += 1
    else:
        print(f'  MISS {fname}: {old[60:100].strip()}')

written = 0
for fname, html in file_data.items():
    fpath = os.path.join(BASE, fname)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)
    written += 1
    print(f'  >> {fname} written')

print(f'\nDone. {total} fixes in {written} files.')
