#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Уточняет DSM-5-TR коды глав: вместо диапазонов — конкретные коды.
Формат: DSM-5-TR: [295], [297], [298] — Chapter name
"""
import sys, io, os, unicodedata

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r"C:\Users\SAM\Desktop\sayt2\klinik-psixiatriya"

def icd(*codes):
    """Render list of codes as <span class="icd">XXX</span>, ..."""
    return ', '.join(f'<span class="icd">{c}</span>' for c in codes)

def fix(fpath, old_suffix, new_content):
    with open(fpath, encoding='utf-8') as f:
        html = f.read()
    html = unicodedata.normalize('NFC', html)
    tag = '<div class="xbt-line"><span class="xbt-lbl">DSM-5-TR:</span> '
    old = tag + old_suffix + '</div>'
    new = tag + new_content + '</div>'
    if old in html:
        html = html.replace(old, new, 1)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html)
        fname = os.path.basename(fpath)
        print(f'  ✓ {fname}: DSM-5-TR: {new_content[:90]}')
        return True
    else:
        fname = os.path.basename(fpath)
        print(f'  ✗ NOT FOUND in {fname}: {old_suffix[:70]}')
        return False

B = BASE + '\\'

# ── bolme-01: Neurodevelopmental disorders ───────────────────────────────────
# 299=ASD, 307=Tics+Stereotypy, 314=ADHD, 315=Learning/Speech/DCD, 317-319=ID
fix(B+'bolme-01.html',
    icd('299','307','314','315','317','318','319') + ' — Neurodevelopmental disorders',
    icd('299','307','314','315','317','318','319') + ' — Neurodevelopmental disorders')

# ── bolme-02: Schizophrenia spectrum ─────────────────────────────────────────
# 295=Schizophrenia/Schizophreniform/Schizoaffective
# 297=Delusional Disorder
# 298=Brief Psychotic/Unspecified Schizophrenia Spectrum
fix(B+'bolme-02.html',
    icd('295') + ' – ' + icd('298') + ' — Schizophrenia spectrum and other psychotic disorders',
    icd('295','297','298') + ' — Schizophrenia spectrum and other psychotic disorders')

# ── bolme-04: Depressive + Bipolar ───────────────────────────────────────────
# 296=MDD+Bipolar I/II (both share 296.xx in DSM-5)
# 300=Persistent Depressive Disorder (300.4=Dysthymia)
# 301=Cyclothymia (301.13)
fix(B+'bolme-04.html',
    icd('296') + ' – ' + icd('301') + ' — Depressive disorders and bipolar and related disorders',
    icd('296','300','301') + ' — Depressive disorders and bipolar and related disorders')

# ── bolme-05: Anxiety disorders ──────────────────────────────────────────────
# 300=GAD, Panic, Agoraphobia, Specific/Social Phobia (all 300.0x-300.2x)
# 309=Separation Anxiety Disorder (309.21)
# 312=Selective Mutism (312.23)
fix(B+'bolme-05.html',
    icd('300') + ' – ' + icd('312') + ' — Anxiety disorders',
    icd('300','309','312') + ' — Anxiety disorders')

# ── bolme-06: OCD and related disorders ──────────────────────────────────────
# 300=OCD (300.3), BDD (300.7), Illness Anxiety (300.7), Hoarding (300.3)
# 312=Trichotillomania (312.39)
fix(B+'bolme-06.html',
    icd('300') + ' – ' + icd('312') + ' — Obsessive-compulsive and related disorders',
    icd('300','312') + ' — Obsessive-compulsive and related disorders')

# ── bolme-07: Trauma- and stressor-related disorders ─────────────────────────
# 308=Acute Stress Disorder (308.3)
# 309=PTSD (309.81), Adjustment Disorder (309.0–309.9)
fix(B+'bolme-07.html',
    icd('308') + ' – ' + icd('309') + ' — Trauma- and stressor-related disorders',
    icd('308','309') + ' — Trauma- and stressor-related disorders')

# ── bolme-08: Dissociative disorders ─────────────────────────────────────────
# 300=Dissociative Amnesia (300.12), DID (300.14), OSDD (300.15),
#     Depersonalization/Derealization (300.6), FND/Conversion (300.11)
# All 300.xx — single code base
fix(B+'bolme-08.html',
    icd('300') + ' — Dissociative disorders',
    icd('300') + ' — Dissociative disorders')

# ── bolme-09: Feeding and eating disorders ────────────────────────────────────
# 307=AN (307.1), Bulimia (307.51), BED (307.51), ARFID (307.59),
#     Pica (307.52), Rumination (307.53) — all 307.xx
fix(B+'bolme-09.html',
    icd('307') + ' — Feeding and eating disorders',
    icd('307') + ' — Feeding and eating disorders')

# ── bolme-10: Elimination disorders ──────────────────────────────────────────
# 307=Enuresis (307.6), Encopresis (307.7) — both 307.xx
fix(B+'bolme-10.html',
    icd('307') + ' — Elimination disorders',
    icd('307') + ' — Elimination disorders')

# ── bolme-11: Somatic symptom and related disorders ──────────────────────────
# 300=SSD (300.82), FND/Conversion (300.11), Illness Anxiety (300.7),
#     Factitious Disorder (300.19)
# 316=Psychological Factors Affecting Medical Condition
fix(B+'bolme-11.html',
    icd('300') + ' – ' + icd('316') + ' — Somatic symptom and related disorders',
    icd('300','316') + ' — Somatic symptom and related disorders')

# ── bolme-12: Substance-related and addictive disorders ──────────────────────
# 291=Alcohol-Induced Mental Disorders (291.0–291.9)
# 292=Other Substance-Induced Mental Disorders (292.xx)
# 303=Alcohol Use Disorder (303.90 moderate/severe)
# 304=Substance Use Disorders moderate/severe (304.00 Opioid, 304.10 Sedative,
#     304.30 Cannabis, 304.40 Stimulant)
# 305=Substance Use Disorders mild (305.00 Alcohol, 305.20 Cannabis, etc.)
# 312=Gambling Disorder (312.31)
fix(B+'bolme-12.html',
    icd('291') + ' – ' + icd('312') + ' — Substance-related and addictive disorders',
    icd('291','292','303','304','305','312') + ' — Substance-related and addictive disorders')

# ── bolme-13: Disruptive, impulse-control (IED, kleptomania, pyromania, CSBD) ─
# 312=IED (312.34), Kleptomania (312.32), Pyromania (312.33)
# 313=ODD (313.81)
fix(B+'bolme-13.html',
    icd('312') + ' – ' + icd('313') + ' — Disruptive, impulse-control, and conduct disorders',
    icd('312','313') + ' — Disruptive, impulse-control, and conduct disorders')

# ── bolme-14: Disruptive (conduct disorder, ODD) ─────────────────────────────
# 312=Conduct Disorder (312.81, 312.82)
# 313=ODD (313.81)
fix(B+'bolme-14.html',
    icd('312') + ' – ' + icd('313') + ' — Disruptive, impulse-control, and conduct disorders',
    icd('312','313') + ' — Disruptive, impulse-control, and conduct disorders')

# ── bolme-15: Personality disorders ──────────────────────────────────────────
# 301=All 10 PD types (301.0 Paranoid, 301.20 Schizoid, 301.22 Schizotypal,
#     301.50 Histrionic, 301.81 Narcissistic, 301.83 BPD, 301.82 Avoidant,
#     301.6 Dependent, 301.4 OCPD, 301.7 ASPD)
fix(B+'bolme-15.html',
    icd('301') + ' — Personality disorders (categorical model; alternative model — Appendix B)',
    icd('301') + ' — Personality disorders (categorical model; alternative model — Appendix B)')

# ── bolme-16: Paraphilic disorders ───────────────────────────────────────────
# 302=Voyeurism (302.82), Exhibitionism (302.4), Frotteurism (302.89),
#     Pedophilia (302.2), Sexual Masochism (302.83), Sadism (302.84),
#     Fetishism (302.81), Transvestism (302.3)
fix(B+'bolme-16.html',
    icd('302') + ' — Paraphilic disorders',
    icd('302') + ' — Paraphilic disorders')

# ── bolme-18: Sleep-wake disorders ───────────────────────────────────────────
# 307=Insomnia (307.42), Hypersomnolence (307.44), Circadian (307.45),
#     Non-REM Arousal (307.46), Nightmare (307.47)
# 327=OSA (327.23), Central Sleep Apnea (327.21), Hypoventilation (327.24),
#     REM Sleep Behavior (327.42)
# 333=Restless Legs Syndrome (333.94)
# 347=Narcolepsy (347.00)
fix(B+'bolme-18.html',
    icd('307') + ' – ' + icd('347') + ' — Sleep-wake disorders',
    icd('307','327','333','347') + ' — Sleep-wake disorders')

# ── bolme-19: Sexual dysfunctions + gender dysphoria ─────────────────────────
# 302=Female Sexual Interest/Arousal (302.72), Female Orgasmic (302.73),
#     Delayed Ejaculation (302.74), Premature Ejaculation (302.75),
#     Genito-Pelvic Pain (302.76), Male Hypoactive (302.71),
#     Erectile Disorder (302.72), Gender Dysphoria in adults (302.85),
#     Gender Dysphoria in children (302.6)
fix(B+'bolme-19.html',
    icd('302') + ' — Sexual dysfunctions and gender dysphoria',
    icd('302') + ' — Sexual dysfunctions and gender dysphoria')

# ── bolme-20: Neurocognitive disorders ───────────────────────────────────────
# 290=Vascular NCD (290.40), NCD due to prion/HIV etc. (290.xx)
# 294=NCD due to another medical condition (294.10, 294.11)
# 331=Major NCD due to Alzheimer's (331.0), FTD (331.19),
#     Lewy Body (331.0), Parkinson's (331.82), Mild NCD (331.83)
fix(B+'bolme-20.html',
    icd('290') + ' – ' + icd('331') + ' — Neurocognitive disorders (major and mild)',
    icd('290','294','331') + ' — Neurocognitive disorders (major and mild)')

# ── bolme-22: Mental disorder due to another medical condition ───────────────
# 293=Psychotic (293.81), Bipolar-type (293.83), Depressive-type (293.83),
#     Anxiety (293.84), OCD-type (293.84), Neurocognitive (293.89),
#     Catatonia (293.89), Other specified (293.89)
fix(B+'bolme-22.html',
    icd('293') + ' — Mental disorder due to another medical condition',
    icd('293') + ' — Mental disorder due to another medical condition')

print('\nDone.')
