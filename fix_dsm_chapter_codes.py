#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Добавляет DSM-5-TR коды к заголовкам глав во всех bolme-файлах.
Формат: DSM-5-TR: [CODE] – [CODE] — Chapter name
Codes взяты из фактических кодов расстройств в каждом bolme-файле.
"""
import sys, io, os, unicodedata

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = r"C:\Users\SAM\Desktop\sayt2\klinik-psixiatriya"

def fix(fpath, old, new):
    with open(fpath, encoding='utf-8') as f:
        html = f.read()
    html = unicodedata.normalize('NFC', html)
    if old in html:
        html = html.replace(old, new, 1)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html)
        return True
    return False

def p(fpath, old_suffix, new_content):
    """Replace chapter DSM line: suffix = everything after 'DSM-5-TR:</span> '"""
    tag = '<div class="xbt-line"><span class="xbt-lbl">DSM-5-TR:</span> '
    old = tag + old_suffix + '</div>'
    new = tag + new_content + '</div>'
    ok = fix(fpath, old, new)
    fname = os.path.basename(fpath)
    if ok:
        print(f'  ✓ {fname}: {new_content[:80]}')
    else:
        print(f'  ✗ NOT FOUND in {fname}: {old_suffix[:60]}')

B = BASE + '\\'

# ── bolme-01: Neurodevelopmental disorders ───────────────────────────────────
# Codes in book: 299.00 (ASD), 307.3/307.20-23 (tics/stereotypy),
#                314.01 (ADHD), 315.00/315.4/315.39 (learning/coord),
#                319 (ID)  → range 299–319
p(B+'bolme-01.html',
  'Neurodevelopmental disorders',
  '<span class="icd">299</span> – <span class="icd">319</span> — Neurodevelopmental disorders')

# ── bolme-02: Schizophrenia spectrum ─────────────────────────────────────────
# Codes in book: 295.90 (schiz), 295.70 (schizoaff), 297.1 (delus), 298.8 (brief)
# User confirmed: 295 – 298
p(B+'bolme-02.html',
  'Schizophrenia spectrum and other psychotic disorders',
  '<span class="icd">295</span> – <span class="icd">298</span> — Schizophrenia spectrum and other psychotic disorders')

# ── bolme-04: Depressive + Bipolar ───────────────────────────────────────────
# Codes: 296.2x (MDD), 296.xx (Bipolar I), 296.89 (Bipolar II),
#        301.13 (Cyclothymia), 300.4 (Dysthymia)  → range 296–301
p(B+'bolme-04.html',
  'Depressive disorders + bipolar and related disorders',
  '<span class="icd">296</span> – <span class="icd">301</span> — Depressive disorders and bipolar and related disorders')

# ── bolme-05: Anxiety disorders ──────────────────────────────────────────────
# Codes: 300.02 (GAD), 300.01 (panic), 300.22 (agoraphobia),
#        300.29 (specific phobia), 300.23 (social anxiety),
#        309.21 (separation anxiety), 312.23 (selective mutism)  → 300–312
p(B+'bolme-05.html',
  'Anxiety disorders',
  '<span class="icd">300</span> – <span class="icd">312</span> — Anxiety disorders')

# ── bolme-06: OCD and related ────────────────────────────────────────────────
# Codes: 300.3 (OCD), 300.7 (BDD, Illness anxiety, Hoarding), 312.39 (Trichotillomania)
# → range 300–312
p(B+'bolme-06.html',
  'Obsessive-compulsive and related disorders',
  '<span class="icd">300</span> – <span class="icd">312</span> — Obsessive-compulsive and related disorders')

# ── bolme-07: Trauma and stressor-related ────────────────────────────────────
# Codes: 308.3 (Acute Stress), 309.81 (PTSD), 309.xx (Adjustment)  → 308–309
p(B+'bolme-07.html',
  'Trauma- and stressor-related disorders',
  '<span class="icd">308</span> – <span class="icd">309</span> — Trauma- and stressor-related disorders')

# ── bolme-08: Dissociative disorders ─────────────────────────────────────────
# Codes: 300.11 (FND), 300.12 (Dissoc. amnesia), 300.14 (DID), 300.15 (OSDD)
# All 300.xx → single range: 300
p(B+'bolme-08.html',
  'Dissociative disorders',
  '<span class="icd">300</span> — Dissociative disorders')

# ── bolme-09: Feeding and eating disorders ────────────────────────────────────
# Codes: 307.1 (AN), 307.51 (BN/BED), 307.52 (Pica), 307.53 (Rumination), 307.59 (ARFID)
# All 307.xx → single range: 307
p(B+'bolme-09.html',
  'Feeding and eating disorders',
  '<span class="icd">307</span> — Feeding and eating disorders')

# ── bolme-10: Elimination disorders ──────────────────────────────────────────
# Codes: 307.6 (Enuresis), 307.7 (Encopresis) — all 307.xx → 307
p(B+'bolme-10.html',
  'Elimination disorders',
  '<span class="icd">307</span> — Elimination disorders')

# ── bolme-11: Somatic symptom and related ────────────────────────────────────
# Codes: 300.82 (SSD), 300.11 (FND/Conversion), 300.7 (Illness Anxiety), 316 (Psych Factors)
# → range 300–316
p(B+'bolme-11.html',
  'Somatic symptom and related disorders',
  '<span class="icd">300</span> – <span class="icd">316</span> — Somatic symptom and related disorders')

# ── bolme-12: Substance-related and addictive ────────────────────────────────
# Codes: 291.xx (alcohol-induced), 292.xx (substance-induced),
#        303.90 (Alcohol UD), 304.xx (moderate/severe UD), 305.xx (mild UD),
#        312.31 (Gambling) → range 291–312
p(B+'bolme-12.html',
  'Substance-related and addictive disorders',
  '<span class="icd">291</span> – <span class="icd">312</span> — Substance-related and addictive disorders')

# ── bolme-13: Disruptive, impulse-control ────────────────────────────────────
# Codes: 312.34 (IED), 312.32 (Kleptomania), 312.33 (Pyromania) → 312–313
p(B+'bolme-13.html',
  'Disruptive, impulse-control, and conduct disorders',
  '<span class="icd">312</span> – <span class="icd">313</span> — Disruptive, impulse-control, and conduct disorders')

# ── bolme-14: Disruptive (conduct + ODD) ─────────────────────────────────────
# Codes: 312.8x (Conduct disorder), 313.81 (ODD) → 312–313
p(B+'bolme-14.html',
  'Disruptive, impulse-control, and conduct disorders',
  '<span class="icd">312</span> – <span class="icd">313</span> — Disruptive, impulse-control, and conduct disorders')

# ── bolme-15: Personality disorders ──────────────────────────────────────────
# Codes: 301.xx (all 10 PD types), 301.83 (BPD) → 301
p(B+'bolme-15.html',
  'Personality disorders (ana mətn: 10 kateqorial tip; alternativ model: əlavə B)',
  '<span class="icd">301</span> — Personality disorders (categorical model; alternative model — Appendix B)')

# ── bolme-16: Paraphilic disorders ───────────────────────────────────────────
# Codes: 302.82 (Voyeurism), 302.4 (Exhibitionism), 302.89 (Frotteurism) → 302
p(B+'bolme-16.html',
  'Paraphilic disorders',
  '<span class="icd">302</span> — Paraphilic disorders')

# ── bolme-18: Sleep-wake disorders ───────────────────────────────────────────
# Codes: 307.42 (Insomnia), 307.44 (Hypersomnolence), 307.45 (Circadian),
#        327.23 (OSA), 327.42 (REM Sleep Behavior), 347.00 (Narcolepsy) → 307–347
p(B+'bolme-18.html',
  'Sleep-wake disorders',
  '<span class="icd">307</span> – <span class="icd">347</span> — Sleep-wake disorders')

# ── bolme-19: Sexual dysfunctions + gender dysphoria ─────────────────────────
# Sexual codes: 302.71–302.76 (all 302.xx); Gender: 302.6, 302.85 → 302
p(B+'bolme-19.html',
  'Sexual dysfunctions; gender dysphoria',
  '<span class="icd">302</span> — Sexual dysfunctions and gender dysphoria')

# ── bolme-20: Neurocognitive disorders ───────────────────────────────────────
# Codes: 290.40 (Vascular NCD), 294.10–294.11 (NCD unspec.),
#        331.0 (Alzheimer's major), 331.83 (Mild NCD) → 290–331
p(B+'bolme-20.html',
  'Neurocognitive disorders (major + mild)',
  '<span class="icd">290</span> – <span class="icd">331</span> — Neurocognitive disorders (major and mild)')

# ── bolme-22: Mental disorder due to another medical condition ───────────────
# Codes: 293.81 (psychotic), 293.82 (hallucinatory), 293.83 (mood),
#        293.84 (anxiety), 293.89 (catatonic/other) → 293
p(B+'bolme-22.html',
  'Mental disorder due to another medical condition',
  '<span class="icd">293</span> — Mental disorder due to another medical condition')

print('\nDone.')
