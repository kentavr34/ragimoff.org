#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive update:
1. Remove ABBREVIATURALAR table from mugeddime.html
2. Rebuild abbreviatur.html as TERMİNOLOJİ LÜĞƏT with merged table
3. Update nav label "Abbreviaturalar" -> "TERMİNOLOJİ LÜĞƏT" in all files
4. Update ALL_PAGES: abbreviatur title -> "TERMİNOLOJİ LÜĞƏT", giris title -> "Kitab Haqqında"
5. Remove "giris" nav entry from all HTML files
6. Update giris.html H1 and title
"""
import sys, io, os, glob, unicodedata

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r"C:\Users\SAM\Desktop\sayt2\klinik-psixiatriya"

def nfc(s): return unicodedata.normalize('NFC', s)

# ── NEW TABLE CONTENT (merged from both sources, deduplicated, corrected) ──

NEW_TABLE_ROWS = [
    # Abbreviatura | Azərbaycanca tam adı | İngilis dilində
    ("AAP",      "Atipik (İkinci Nəsil) Antipsixotiklər",                              "Atypical / Second-Generation Antipsychotics (AAP/SGA)"),
    ("ACT",      "Qəbul və Öhdəlik Terapiyası",                                        "Acceptance and Commitment Therapy (ACT)"),
    ("AİP",      "Alkoqol İstifadəsi Pozuntusu",                                       "Alcohol Use Disorder (AUD)"),
    ("ANO",      "Nevrotik Anoreksiya",                                                 "Anorexia Nervosa (AN)"),
    ("ARFİD",    "Qaçınmalı/Məhdudlaşdırıcı Qida Qəbulu Pozuntusu",                   "Avoidant/Restrictive Food Intake Disorder (ARFID)"),
    ("ASP",      "Autizm Spektri Pozuntusu",                                            "Autism Spectrum Disorder (ASD)"),
    ("BDP",      "Bədən Dismorfik Pozuntusu",                                           "Body Dysmorphic Disorder (BDD)"),
    ("BİİP",     "Bipolyar II Pozuntu",                                                 "Bipolar II Disorder (BD-II)"),
    ("BİP",      "Bipolyar I Pozuntu",                                                  "Bipolar I Disorder (BD-I)"),
    ("BKİ",      "Bədən Kütlə İndeksi",                                                "Body Mass Index (BMI)"),
    ("BNO",      "Nevrotik Bulimiya",                                                   "Bulimia Nervosa (BN)"),
    ("BP",       "Bipolyar Pozuntu (ümumi)",                                            "Bipolar Disorder (BD)"),
    ("BPRS",     "Qısa Psixiatrik Reytinq Şkalası",                                    "Brief Psychiatric Rating Scale (BPRS)"),
    ("BZD",      "Benzodiazepin",                                                       "Benzodiazepine (BZD)"),
    ("CAPS",     "TSSP üçün Klinik İdarəolunan PTSD Şkalası",                          "Clinician-Administered PTSD Scale (CAPS)"),
    ("CGI",      "Klinik Qlobal Qiymətləndirmə",                                       "Clinical Global Impression (CGI)"),
    ("CPAP",     "Davamlı Müsbət Hava Yolu Təzyiqi",                                   "Continuous Positive Airway Pressure (CPAP)"),
    ("DBT",      "Dialektik Davranış Terapiyası",                                       "Dialectical Behaviour Therapy (DBT)"),
    ("DDHP",     "Diqqət Defisiti və Hiperaktivlik Pozuntusu",                         "Attention-Deficit/Hyperactivity Disorder (ADHD)"),
    ("DPT",      "Dinamik Psixoterapiya",                                               "Dynamic Psychotherapy (DPT)"),
    ("DSM-5-TR", "Psixi Pozuntuların Diaqnostik və Statistik Təlimatı, 5-ci nəşr, Mətn Yeniləməsi", "Diagnostic and Statistical Manual of Mental Disorders, 5th Edition, Text Revision (DSM-5-TR)"),
    ("DSP",      "Dissosiativ Şəxsiyyət Pozuntusu",                                    "Dissociative Identity Disorder (DID)"),
    ("EEG",      "Elektroensefaloqrafiya",                                              "Electroencephalography (EEG)"),
    ("EFT",      "Emosional Fokuslu Terapiya",                                          "Emotion-Focused Therapy (EFT)"),
    ("EKT",      "Elektrokonvulsiv Terapiya",                                           "Electroconvulsive Therapy (ECT)"),
    ("EMDR",     "Göz Hərəkəti ilə Həssaslaşdırma və Yenidən İşləmə",                 "Eye Movement Desensitization and Reprocessing (EMDR)"),
    ("GAD-7",    "Generalizə Olunmuş Təşviş Şkalası-7",                                "Generalized Anxiety Disorder Scale-7 (GAD-7)"),
    ("GAP",      "Generalizə Olunmuş Təşviş Pozuntusu",                                "Generalized Anxiety Disorder (GAD)"),
    ("HARS",     "Hamilton Narahatlıq Reytinq Şkalası",                                "Hamilton Anxiety Rating Scale (HARS)"),
    ("HBS",      "Huzursuz Bacaq Sindromu",                                             "Restless Legs Syndrome (RLS)"),
    ("HDRS",     "Hamilton Depressiya Reytinq Şkalası",                                "Hamilton Depression Rating Scale (HDRS/HAM-D)"),
    ("IPA",      "Beynəlxalq Psixoanalitik Assosiasiya",                               "International Psychoanalytic Association (IPA)"),
    ("IPAS",     "Beynəlxalq Psixoterapiya Assosiasiyası",                             "International Psychotherapy Association (IPAS)"),
    ("İİP",      "İntellektual İnkişaf Pozuntusu",                                     "Intellectual Developmental Disorder (IDD)"),
    ("KDT",      "Koqnitiv Davranış Terapiyası",                                       "Cognitive Behavioural Therapy (CBT)"),
    ("KDT-İ",    "İnsomnia üçün Koqnitiv Davranış Terapiyası",                         "Cognitive Behavioural Therapy for Insomnia (CBT-I)"),
    ("KTSSP",    "Kompleks Travma Sonrası Stress Pozuntusu",                            "Complex Post-Traumatic Stress Disorder (cPTSD)"),
    ("Li",       "Litium",                                                              "Lithium (Li)"),
    ("MAOİ",     "Monoaminooksidaza İnhibitorları",                                    "Monoamine Oxidase Inhibitors (MAOI)"),
    ("MBT",      "Mentalizasiyaya Əsaslanan Terapiya",                                 "Mentalization-Based Treatment (MBT)"),
    ("MDP",      "Major Depressiv Pozuntu",                                             "Major Depressive Disorder (MDD)"),
    ("MI",       "Motivasional Müsahibə",                                               "Motivational Interviewing (MI)"),
    ("MINI",     "Mini Beynəlxalq Nöropsixiatrik Müsahibə",                            "Mini International Neuropsychiatric Interview (MINI)"),
    ("MMSE",     "Mini Ruhi Vəziyyət Müayinəsi",                                       "Mini-Mental State Examination (MMSE)"),
    ("MoKQ",     "Monreal Koqnitiv Qiymətləndirməsi",                                  "Montreal Cognitive Assessment (MoCA)"),
    ("MRI",      "Maqnit Rezonans Tomoqrafiyası",                                      "Magnetic Resonance Imaging (MRI)"),
    ("MSLT",     "Çoxlu Yuxu Latensiyası Testi",                                       "Multiple Sleep Latency Test (MSLT)"),
    ("NİPNİ",    "Bexterev adına Psixonevroloji Elmi-Tədqiqat İnstitutu",             "V.M. Bekhterev Psychoneurological Research Institute (NIPNI)"),
    ("NKP",      "Neyrokoqnitiv Pozuntu",                                               "Neurocognitive Disorder (NCD)"),
    ("NREM",     "Sürətli Olmayan Göz Hərəkəti (yuxu fazası)",                         "Non-Rapid Eye Movement (NREM)"),
    ("OİP",      "Opioid İstifadəsi Pozuntusu",                                        "Opioid Use Disorder (OUD)"),
    ("OKP",      "Obsessiv-Kompulsiv Pozuntu",                                          "Obsessive-Compulsive Disorder (OCD)"),
    ("OSA",      "Obstruktiv Yuxu Apnoesi",                                             "Obstructive Sleep Apnea (OSA)"),
    ("PANSS",    "Müsbət və Mənfi Simptom Şkalası",                                    "Positive and Negative Syndrome Scale (PANSS)"),
    ("PDE5",     "Fosfodiesteraz-5 inhibitoru",                                         "Phosphodiesterase-5 Inhibitor (PDE5i)"),
    ("PHQ-9",    "Pasiyent Sağlamlıq Sorğusu-9",                                       "Patient Health Questionnaire-9 (PHQ-9)"),
    ("PSQ",      "Polisomnoqrafiya",                                                    "Polysomnography (PSG)"),
    ("RBD",      "REM Yuxu Davranış Pozuntusu",                                        "REM Sleep Behaviour Disorder (RBD)"),
    ("REM",      "Sürətli Göz Hərəkəti (yuxu fazası)",                                 "Rapid Eye Movement (REM)"),
    ("SCID",     "DSM üzrə Struktur Klinik Müsahibə",                                  "Structured Clinical Interview for DSM (SCID)"),
    ("SİUSİ",    "Serotoninin Seçici Geri-Alınma İnhibitorları",                       "Selective Serotonin Reuptake Inhibitors (SSRI)"),
    ("SNP",      "Sosial Narahatlıq Pozuntusu",                                         "Social Anxiety Disorder (SAD)"),
    ("SNRİ",     "Serotonin-Noradrenalin Geri-Alınma İnhibitorları",                   "Serotonin-Norepinephrine Reuptake Inhibitors (SNRI)"),
    ("SSD",      "Somatik Simptom Pozuntusu",                                           "Somatic Symptom Disorder (SSD)"),
    ("TİP",      "Tipik (Birinci Nəsil) Antipsixotiklər",                              "First-Generation Antipsychotics (FGA)"),
    ("TMS",      "Transkranial Maqnit Stimulyasiya",                                   "Transcranial Magnetic Stimulation (TMS)"),
    ("TSSP",     "Travma Sonrası Stress Pozuntusu",                                     "Post-Traumatic Stress Disorder (PTSD)"),
    ("TsAD",     "Trisiklik Antidepressantlar",                                         "Tricyclic Antidepressants (TCA)"),
    ("TYP",      "Tıxanma ilə Yemə Pozuntusu",                                         "Binge Eating Disorder (BED)"),
    ("ÜST",      "Ümumdünya Səhiyyə Təşkilatı",                                        "World Health Organization (WHO)"),
    ("VPA",      "Valproat turşusu",                                                    "Valproic Acid (VPA)"),
    ("WPATH",    "Transseksual Sağlamlığı üçün Dünya Peşəkarlar Assosiasiyası",        "World Professional Association for Transgender Health (WPATH)"),
    ("XAP",      "Xəstəlik Həyəcanı Pozuntusu",                                        "Illness Anxiety Disorder (IAD)"),
    ("XBT-10",   "Xəstəliklərin Beynəlxalq Təsnifatı, 10-cu nəşr",                    "International Classification of Diseases, 10th Revision (ICD-10)"),
    ("XBT-11",   "Xəstəliklərin Beynəlxalq Təsnifatı, 11-ci nəşr",                    "International Classification of Diseases, 11th Revision (ICD-11)"),
    ("Y-BOCS",   "Yel-Braun Obsessiv-Kompulsiv Şkalası",                               "Yale-Brown Obsessive Compulsive Scale (Y-BOCS)"),
    ("YMRS",     "Yanq Maniya Reytinq Şkalası",                                        "Young Mania Rating Scale (YMRS)"),
]

def build_table():
    rows = ['<tr><th>Abbreviatura</th><th>Azərbaycanca tam adı</th><th>İngilis dilində</th></tr>']
    for abbr, az, en in NEW_TABLE_ROWS:
        rows.append(f'<tr><td>{abbr}</td><td>{az}</td><td>{en}</td></tr>')
    return '\n'.join(rows)

NEW_SECTION = (
    '<h1 id="terminoloji-lüğət" class="h-section">TERMİNOLOJİ LÜĞƏT</h1>\n'
    '<p>Bu lüğətdə kitabda istifadə edilən abbreviaturalar, onların azərbaycanca tam adı '
    'və ingilis dilindəki qarşılıqları verilmişdir. Abbreviaturalar əlifba sırası ilə düzülmüşdür.</p>\n'
    '<div class="tbl-wrap"><table>\n'
    + build_table() +
    '\n</table></div>\n'
    '<hr>'
)

# ════════════════════════════════════════════════════════
# STEP 1 — Remove ABBREVIATURALAR block from mugeddime.html
# ════════════════════════════════════════════════════════
mug_path = os.path.join(BASE, 'mugeddime.html')
with open(mug_path, encoding='utf-8') as f:
    mug = f.read()
mug = nfc(mug)

# The block starts at <h2 id="abbreviaturalar-lüğəti̇" and ends with </table></div>\n<hr>\n
# followed by <h2 id="oxucuya-müraciət"
import re

# Remove from the ABBREVIATURALAR h2 through the <hr> (inclusive), leaving the next <h2> intact
mug_new = re.sub(
    r'<h2[^>]+id="[^"]*abbreviaturalar[^"]*"[^>]*>.*?<hr>(\s*)',
    r'\1',
    mug,
    count=1,
    flags=re.DOTALL
)

if mug_new != mug:
    with open(mug_path, 'w', encoding='utf-8') as f:
        f.write(mug_new)
    print('OK mugeddime.html — ABBREVIATURALAR block removed')
else:
    print('MISS mugeddime.html — pattern not found')

# ════════════════════════════════════════════════════════
# STEP 2 — Rebuild abbreviatur.html
# ════════════════════════════════════════════════════════
abbr_path = os.path.join(BASE, 'abbreviatur.html')
with open(abbr_path, encoding='utf-8') as f:
    abbr = f.read()
abbr = nfc(abbr)

# Update <title>
abbr = abbr.replace(
    'Abbreviaturalar | KLİNİK PSİXİATRİYA',
    'TERMİNOLOJİ LÜĞƏT | KLİNİK PSİXİATRİYA',
    1
)
# Update <meta description>
abbr = abbr.replace(
    'content="Klinik Psixiatriya — Abbreviaturalar"',
    'content="Klinik Psixiatriya — Terminoloji Lüğət"',
    1
)

# Replace main content: from the old h2 through <hr> (just before <nav class="page-nav">)
abbr_new = re.sub(
    r'<h2[^>]+id="[^"]*abbrevi[^"]*"[^>]*>.*?<hr>',
    nfc(NEW_SECTION),
    abbr,
    count=1,
    flags=re.DOTALL
)

if abbr_new != abbr:
    with open(abbr_path, 'w', encoding='utf-8') as f:
        f.write(abbr_new)
    print(f'OK abbreviatur.html — rebuilt as TERMİNOLOJİ LÜĞƏT ({len(NEW_TABLE_ROWS)} rows)')
else:
    print('MISS abbreviatur.html — main content pattern not found')

# ════════════════════════════════════════════════════════
# STEP 3, 4, 5 — Update ALL HTML files
# ════════════════════════════════════════════════════════
GIRIS_NAV_BLOCK = nfc(
    '<div class="nav-item" data-slug="giris">\n'
    '  <a href="giris.html" class="nav-link" data-slug="giris">\n'
    '    <span>Giriş</span>\n'
    '  </a>\n'
    '</div>\n'
)

all_html = sorted(glob.glob(os.path.join(BASE, '*.html')))
nav_updated = 0
giris_removed = 0
allpages_abbr_updated = 0
allpages_giris_updated = 0

for fpath in all_html:
    fname = os.path.basename(fpath)
    with open(fpath, encoding='utf-8') as f:
        html = f.read()
    html = nfc(html)
    original = html

    # 3 — nav label
    if nfc('<span>Abbreviaturalar</span>') in html:
        html = html.replace(nfc('<span>Abbreviaturalar</span>'), nfc('<span>TERMİNOLOJİ LÜĞƏT</span>'), 1)
        nav_updated += 1

    # 4a — ALL_PAGES abbreviatur title
    if '"slug": "abbreviatur", "title": "Abbreviaturalar"' in html:
        html = html.replace(
            '"slug": "abbreviatur", "title": "Abbreviaturalar"',
            '"slug": "abbreviatur", "title": "TERMİNOLOJİ L\\u00dcG\\u018eT"',
            1
        )
        allpages_abbr_updated += 1

    # 4b — ALL_PAGES giris title (update to "Kitab Haqqında" so search shows correct name)
    if '"slug": "giris", "title": "Giri\\u015f"' in html:
        html = html.replace(
            '"slug": "giris", "title": "Giri\\u015f"',
            '"slug": "giris", "title": "Kitab Haqq\\u0131nda"',
            1
        )
        allpages_giris_updated += 1

    # 5 — remove giris nav entry
    if GIRIS_NAV_BLOCK in html:
        html = html.replace(GIRIS_NAV_BLOCK, '', 1)
        giris_removed += 1

    if html != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html)

print(f'Nav "TERMİNOLOJİ LÜĞƏT" updated: {nav_updated} files')
print(f'ALL_PAGES abbreviatur title updated: {allpages_abbr_updated} files')
print(f'ALL_PAGES giris title updated: {allpages_giris_updated} files')
print(f'Giris nav entry removed: {giris_removed} files')

# ════════════════════════════════════════════════════════
# STEP 6 — Update giris.html heading and title
# ════════════════════════════════════════════════════════
giris_path = os.path.join(BASE, 'giris.html')
with open(giris_path, encoding='utf-8') as f:
    giris = f.read()
giris = nfc(giris)

# Title tag
giris_new = giris.replace(
    'Giriş | KLİNİK PSİXİATRİYA',
    'Kitab Haqqında | KLİNİK PSİXİATRİYA',
    1
)
# H1 heading — the id might have dotted İ
giris_new = re.sub(
    r'<h1[^>]+id="[^"]*giri[^"]*"[^>]*>GİRİŞ</h1>',
    '<h1 id="kitab-haqqinda" class="h-section">Kitab Haqqında</h1>',
    giris_new,
    count=1,
    flags=re.IGNORECASE
)

if giris_new != giris:
    with open(giris_path, 'w', encoding='utf-8') as f:
        f.write(giris_new)
    print('OK giris.html — H1 and title updated')
else:
    print('MISS giris.html — pattern not found')

print('\nDone.')
