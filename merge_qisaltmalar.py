#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Merge QISALTMALAR tables from index.html and elave-acde.html
into TERMİNOLOJİ LÜĞƏT (abbreviatur.html).
Remove source tables from both pages.
"""
import sys, io, os, re, unicodedata

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r"C:\Users\SAM\Desktop\sayt2\klinik-psixiatriya"

def nfc(s): return unicodedata.normalize('NFC', s)

# ── FULL MERGED TABLE (existing 77 + 52 new from QISALTMALAR) ──────────────
# Columns: abbreviatura | azərbaycanca | ingilis
ROWS = [
    ("AAP",          "Atipik (İkinci Nəsil) Antipsixotiklər",                                  "Atypical / Second-Generation Antipsychotics (AAP/SGA)"),
    ("AACAP",        "Amerika Uşaq və Yeniyetmə Psixiatriyası Akademiyası",                    "American Academy of Child & Adolescent Psychiatry (AACAP)"),
    ("ACE",          "Mənfi Uşaqlıq Təcrübələri",                                              "Adverse Childhood Experiences (ACE)"),
    ("ACT",          "Qəbul və Öhdəlik Terapiyası",                                            "Acceptance and Commitment Therapy (ACT)"),
    ("AİP",          "Alkoqol İstifadəsi Pozuntusu",                                           "Alcohol Use Disorder (AUD)"),
    ("ANO",          "Nevrotik Anoreksiya",                                                     "Anorexia Nervosa (AN)"),
    ("APA",          "Amerika Psixiatrik Birliyi",                                             "American Psychiatric Association (APA)"),
    ("ARFİD",        "Qaçınmalı/Məhdudlaşdırıcı Qida Qəbulu Pozuntusu",                       "Avoidant/Restrictive Food Intake Disorder (ARFID)"),
    ("ASP",          "Autizm Spektri Pozuntusu",                                               "Autism Spectrum Disorder (ASD)"),
    ("ASPD",         "Antisosial Şəxsiyyət Pozuntusu",                                        "Antisocial Personality Disorder (ASPD)"),
    ("BDD (6B21)",   "Bədən Dismorfik Pozuntusu (XBT-11 kodu; AZ ixtisarı: BDP)",            "Body Dysmorphic Disorder (BDD / ICD-11: 6B21)"),
    ("BDD (6C20)",   "Bədən Sıxıntı Pozuntusu (XBT-11 kodu)",                                "Bodily Distress Disorder (BDD / ICD-11: 6C20)"),
    ("BDP",          "Bədən Dismorfik Pozuntusu",                                              "Body Dysmorphic Disorder (BDD)"),
    ("BİİP",         "Bipolyar II Pozuntu",                                                    "Bipolar II Disorder (BD-II)"),
    ("BİP",          "Bipolyar I Pozuntu",                                                     "Bipolar I Disorder (BD-I)"),
    ("BKİ",          "Bədən Kütlə İndeksi",                                                   "Body Mass Index (BMI)"),
    ("BNO",          "Nevrotik Bulimiya",                                                      "Bulimia Nervosa (BN)"),
    ("BP",           "Bipolyar Pozuntu (ümumi)",                                               "Bipolar Disorder (BD)"),
    ("BPD",          "Sərhəd Şəxsiyyət Pozuntusu (ingilis ixtisarı)",                        "Borderline Personality Disorder (BPD)"),
    ("BPRS",         "Qısa Psixiatrik Reytinq Şkalası",                                       "Brief Psychiatric Rating Scale (BPRS)"),
    ("BZD",          "Benzodiazepin",                                                          "Benzodiazepine (BZD)"),
    ("CAPS",         "TSSP üçün Klinik İdarəolunan PTSD Şkalası",                             "Clinician-Administered PTSD Scale (CAPS)"),
    ("CAT",          "Koqnitiv Analitik Terapiya",                                             "Cognitive Analytic Therapy (CAT)"),
    ("CDDG",         "Klinik Təsvirlər və Diaqnostik Tələblər (ÜST, XBT-10, 1992)",          "Clinical Descriptions and Diagnostic Guidelines (WHO/ICD-10, 1992)"),
    ("CD",           "Davranış Pozuntusu",                                                     "Conduct Disorder (CD)"),
    ("CGI",          "Klinik Qlobal Qiymətləndirmə",                                          "Clinical Global Impression (CGI)"),
    ("CPAP",         "Davamlı Müsbət Hava Yolu Təzyiqi",                                      "Continuous Positive Airway Pressure (CPAP)"),
    ("CSBD",         "Kompulsiv Cinsi Davranış Pozuntusu",                                    "Compulsive Sexual Behaviour Disorder (CSBD)"),
    ("DBT",          "Dialektik Davranış Terapiyası",                                         "Dialectical Behaviour Therapy (DBT)"),
    ("DDHP",         "Diqqət Defisiti və Hiperaktivlik Pozuntusu",                            "Attention-Deficit/Hyperactivity Disorder (ADHD)"),
    ("DMDD",         "Disruptiv Əhval Disrequlasiya Pozuntusu (DSM-5)",                       "Disruptive Mood Dysregulation Disorder (DMDD)"),
    ("DPT",          "Dinamik Psixoterapiya",                                                  "Dynamic Psychotherapy (DPT)"),
    ("DPDR",         "Depersonalizasiya-Derealizasiya Pozuntusu",                             "Depersonalization-Derealization Disorder (DPDR/DPD)"),
    ("DSM-5-TR",     "Psixi Pozuntuların Diaqnostik və Statistik Təlimatı, 5-ci nəşr, Mətn Yeniləməsi", "Diagnostic and Statistical Manual of Mental Disorders, 5th Edition, Text Revision (DSM-5-TR)"),
    ("DSP",          "Dissosiativ Şəxsiyyət Pozuntusu",                                       "Dissociative Identity Disorder (DID)"),
    ("EBM",          "Sübutlara Əsaslanan Tibb",                                              "Evidence-Based Medicine (EBM)"),
    ("EEG",          "Elektroensefaloqrafiya",                                                 "Electroencephalography (EEG)"),
    ("EFT",          "Emosional Fokuslu Terapiya",                                             "Emotion-Focused Therapy (EFT)"),
    ("EKT",          "Elektrokonvulsiv Terapiya",                                              "Electroconvulsive Therapy (ECT)"),
    ("EMDR",         "Göz Hərəkəti ilə Həssaslaşdırma və Yenidən İşləmə",                    "Eye Movement Desensitization and Reprocessing (EMDR)"),
    ("EPDS",         "Edinburq Doğuşdan Sonrakı Depressiya Şkalası",                          "Edinburgh Postnatal Depression Scale (EPDS)"),
    ("EPM",          "Eksperimental-Psixoloji Müayinə",                                       "Experimental Psychological Examination (EPM)"),
    ("FBT",          "Ailə Əsaslı Müalicə",                                                   "Family-Based Treatment (FBT)"),
    ("FDIA",         "Başqasına Tətbiq Edilmiş Süni Pozuntu",                                 "Factitious Disorder Imposed on Another (FDIA)"),
    ("FDIS",         "Özünə Tətbiq Edilmiş Süni Pozuntu",                                    "Factitious Disorder Imposed on Self (FDIS)"),
    ("FII",          "Uydurulmuş/Törədilmiş Xəstəlik",                                       "Fabricated or Induced Illness (FII)"),
    ("GAD-7",        "Generalizə Olunmuş Təşviş Şkalası-7",                                   "Generalized Anxiety Disorder Scale-7 (GAD-7)"),
    ("GAP",          "Generalizə Olunmuş Təşviş Pozuntusu",                                   "Generalized Anxiety Disorder (GAD)"),
    ("HAND",         "HIV ilə Əlaqəli Neyrokoqnitiv Pozuntu",                                "HIV-Associated Neurocognitive Disorder (HAND)"),
    ("HARS",         "Hamilton Narahatlıq Reytinq Şkalası",                                   "Hamilton Anxiety Rating Scale (HARS)"),
    ("HBS",          "Huzursuz Bacaq Sindromu",                                               "Restless Legs Syndrome (RLS)"),
    ("HDRS",         "Hamilton Depressiya Reytinq Şkalası",                                   "Hamilton Depression Rating Scale (HDRS/HAM-D)"),
    ("HPA",          "Hipotalamus-Hipofiz-Böyrəküstü Vəzi Oxu",                              "Hypothalamic-Pituitary-Adrenal Axis (HPA)"),
    ("IACAPAP",      "Uşaq və Yeniyetmə Psixiatriyası Beynəlxalq Assosiasiyası",            "International Assoc. for Child & Adolescent Psychiatry and Allied Professions (IACAPAP)"),
    ("IED",          "İntermittent Eksplosiv Pozuntu",                                         "Intermittent Explosive Disorder (IED)"),
    ("IPA",          "Beynəlxalq Psixoanalitik Assosiasiya",                                  "International Psychoanalytic Association (IPA)"),
    ("IPA",          "Beynəlxalq Psixogeriatrik Assosiasiya",                                 "International Psychogeriatric Association (IPA)"),
    ("IPAS",         "Beynəlxalq Psixoterapiya Assosiasiyası",                                "International Psychotherapy Association (IPAS)"),
    ("ISBD",         "Bipolyar Pozuntular üzrə Beynəlxalq Cəmiyyət",                        "International Society for Bipolar Disorders (ISBD)"),
    ("ISSTD",        "Travma və Dissosiasiya Tədqiqatı üzrə Beynəlxalq Cəmiyyət",           "International Society for the Study of Trauma and Dissociation (ISSTD)"),
    ("ISTSS",        "Travmatik Stress Tədqiqatları üçün Beynəlxalq Cəmiyyət",              "International Society for Traumatic Stress Studies (ISTSS)"),
    ("İİP",          "İntellektual İnkişaf Pozuntusu",                                        "Intellectual Developmental Disorder (IDD)"),
    ("İPT",          "Şəxslərarası Terapiya",                                                 "Interpersonal Therapy (IPT)"),
    ("KDT",          "Koqnitiv Davranış Terapiyası",                                          "Cognitive Behavioural Therapy (CBT)"),
    ("KDT-İ",        "İnsomnia üçün Koqnitiv Davranış Terapiyası",                           "Cognitive Behavioural Therapy for Insomnia (CBT-I)"),
    ("KTSSP",        "Kompleks Travma Sonrası Stress Pozuntusu",                              "Complex Post-Traumatic Stress Disorder (cPTSD)"),
    ("KTTD",         "Klinik Təsvirlər və Diaqnostik Tələblər (ÜST, XBT-11, 2024)",         "Clinical Descriptions and Diagnostic Guidelines (WHO/ICD-11, 2024)"),
    ("Li",           "Litium",                                                                 "Lithium (Li)"),
    ("MAOİ",         "Monoaminooksidaza İnhibitorları",                                       "Monoamine Oxidase Inhibitors (MAOI)"),
    ("MBT",          "Mentalizasiyaya Əsaslanan Terapiya",                                    "Mentalization-Based Treatment (MBT)"),
    ("MCI",          "Yüngül Koqnitiv Pozuntu",                                               "Mild Cognitive Impairment (MCI)"),
    ("MDP",          "Major Depressiv Pozuntu",                                                "Major Depressive Disorder (MDD)"),
    ("MDMA",         "3,4-metilendioksimetamfetamin (maddə)",                                 "3,4-Methylenedioxymethamphetamine (MDMA)"),
    ("MDQ",          "Əhval Pozuntusu Sorğusu",                                               "Mood Disorder Questionnaire (MDQ)"),
    ("mhGAP",        "Ruhi Sağlamlıq Boşluğu Fəaliyyət Proqramı (ÜST)",                     "Mental Health Gap Action Programme (mhGAP, WHO)"),
    ("MI",           "Motivasional Müsahibə",                                                  "Motivational Interviewing (MI)"),
    ("MINI",         "Mini Beynəlxalq Nöropsixiatrik Müsahibə",                              "Mini International Neuropsychiatric Interview (MINI)"),
    ("MMPI",         "Minnesota Çoxfazalı Şəxsiyyət İnventarı",                             "Minnesota Multiphasic Personality Inventory (MMPI)"),
    ("MMSE",         "Mini Ruhi Vəziyyət Müayinəsi",                                         "Mini-Mental State Examination (MMSE)"),
    ("MNN",          "Beynəlxalq Patentləşdirilməmiş Ad",                                    "International Nonproprietary Name (INN/MNN)"),
    ("MoKQ",         "Monreal Koqnitiv Qiymətləndirməsi",                                    "Montreal Cognitive Assessment (MoCA)"),
    ("MRI",          "Maqnit Rezonans Tomoqrafiyası",                                         "Magnetic Resonance Imaging (MRI)"),
    ("MS",           "Multipl Skleroz",                                                        "Multiple Sclerosis (MS)"),
    ("MST",          "Multisistem Terapiyası",                                                 "Multisystemic Therapy (MST)"),
    ("MSLT",         "Çoxlu Yuxu Latensiyası Testi",                                          "Multiple Sleep Latency Test (MSLT)"),
    ("NİPNİ",        "Bexterev adına Psixonevroloji Elmi-Tədqiqat İnstitutu",               "V.M. Bekhterev Psychoneurological Research Institute (NIPNI)"),
    ("NICE",         "Milli Sağlamlıq və Klinik Mükəmməllik İnstitutu (Böyük Britaniya)",  "National Institute for Health and Care Excellence (NICE, UK)"),
    ("NKP",          "Neyrokoqnitiv Pozuntu",                                                  "Neurocognitive Disorder (NCD)"),
    ("NMS",          "Neyroleptik Maliqn Sindromu",                                           "Neuroleptic Malignant Syndrome (NMS)"),
    ("NREM",         "Sürətli Olmayan Göz Hərəkəti (yuxu fazası)",                           "Non-Rapid Eye Movement (NREM)"),
    ("OCRD",         "Obsessiv-Kompulsiv və Əlaqəli Pozuntular",                             "Obsessive-Compulsive and Related Disorders (OCRD)"),
    ("ODD",          "Oppozisiya-Etiraz Pozuntusu",                                           "Oppositional Defiant Disorder (ODD)"),
    ("OİP",          "Opioid İstifadəsi Pozuntusu",                                          "Opioid Use Disorder (OUD)"),
    ("OKP",          "Obsessiv-Kompulsiv Pozuntu",                                             "Obsessive-Compulsive Disorder (OCD)"),
    ("OSA",          "Obstruktiv Yuxu Apnoesi",                                               "Obstructive Sleep Apnea (OSA)"),
    ("PANSS",        "Müsbət və Mənfi Simptom Şkalası",                                      "Positive and Negative Syndrome Scale (PANSS)"),
    ("PCL-5",        "PTSD Yoxlama Siyahısı (DSM-5)",                                        "PTSD Checklist for DSM-5 (PCL-5)"),
    ("PDE5",         "Fosfodiesteraz-5 inhibitoru",                                           "Phosphodiesterase-5 Inhibitor (PDE5i)"),
    ("PGD",          "Uzanmış Kədər Pozuntusu",                                               "Prolonged Grief Disorder (PGD)"),
    ("PHQ-9",        "Pasiyent Sağlamlıq Sorğusu-9",                                         "Patient Health Questionnaire-9 (PHQ-9)"),
    ("PMT",          "Valideyn Davranış Terapiyası",                                          "Parent Management Training (PMT)"),
    ("PNES",         "Psixogen Qeyri-Epileptik Tutmalar",                                    "Psychogenic Non-Epileptic Seizures (PNES)"),
    ("PSQ",          "Polisomnoqrafiya",                                                       "Polysomnography (PSG)"),
    ("RBD",          "REM Yuxu Davranış Pozuntusu",                                          "REM Sleep Behaviour Disorder (RBD)"),
    ("REM",          "Sürətli Göz Hərəkəti (yuxu fazası)",                                   "Rapid Eye Movement (REM)"),
    ("SCID",         "DSM üzrə Struktur Klinik Müsahibə",                                   "Structured Clinical Interview for DSM (SCID)"),
    ("SİUSİ",        "Serotoninin Seçici Geri-Alınma İnhibitorları",                         "Selective Serotonin Reuptake Inhibitors (SSRI)"),
    ("SNP",          "Sosial Narahatlıq Pozuntusu",                                           "Social Anxiety Disorder (SAD)"),
    ("SNRİ",         "Serotonin-Noradrenalin Geri-Alınma İnhibitorları",                     "Serotonin-Norepinephrine Reuptake Inhibitors (SNRI)"),
    ("SSD",          "Somatik Simptom Pozuntusu",                                             "Somatic Symptom Disorder (SSD)"),
    ("SSRİ",         "Serotoninin Seçici Geri-Alınma İnhibitorları (ingilis ixtisarı)",      "Selective Serotonin Reuptake Inhibitors (SSRI) — bax: SİUSİ"),
    ("TBZ",          "Travmatik Beyin Zədəsi",                                                "Traumatic Brain Injury (TBI/TBZ)"),
    ("TF-KDT",       "Travmaya Yönəldilmiş Koqnitiv Davranış Terapiyası",                    "Trauma-Focused Cognitive Behavioural Therapy (TF-CBT)"),
    ("TFP",          "Köçürülmə Fokuslu Psixoterapiya",                                      "Transference-Focused Psychotherapy (TFP)"),
    ("TİP",          "Tipik (Birinci Nəsil) Antipsixotiklər",                                "First-Generation Antipsychotics (FGA)"),
    ("TMS",          "Transkranial Maqnit Stimulyasiya",                                      "Transcranial Magnetic Stimulation (TMS)"),
    ("TSSP",         "Travma Sonrası Stress Pozuntusu",                                       "Post-Traumatic Stress Disorder (PTSD)"),
    ("TsAD",         "Trisiklik Antidepressantlar",                                           "Tricyclic Antidepressants (TCA)"),
    ("TYP",          "Tıxanma ilə Yemə Pozuntusu",                                           "Binge Eating Disorder (BED)"),
    ("ÜST",          "Ümumdünya Səhiyyə Təşkilatı",                                          "World Health Organization (WHO)"),
    ("VPA",          "Valproat turşusu",                                                       "Valproic Acid (VPA)"),
    ("WFSBP",        "Bioloji Psixiatriya Cəmiyyətlərinin Dünya Federasiyası",              "World Federation of Societies of Biological Psychiatry (WFSBP)"),
    ("WPA",          "Dünya Psixiatrik Assosiasiyası",                                        "World Psychiatric Association (WPA)"),
    ("WPATH",        "Transseksual Sağlamlığı üçün Dünya Peşəkarlar Assosiasiyası",         "World Professional Association for Transgender Health (WPATH)"),
    ("XAP",          "Xəstəlik Həyəcanı Pozuntusu",                                          "Illness Anxiety Disorder (IAD)"),
    ("XBT-10",       "Xəstəliklərin Beynəlxalq Təsnifatı, 10-cu nəşr",                      "International Classification of Diseases, 10th Revision (ICD-10)"),
    ("XBT-11",       "Xəstəliklərin Beynəlxalq Təsnifatı, 11-ci nəşr",                      "International Classification of Diseases, 11th Revision (ICD-11)"),
    ("Y-BOCS",       "Yel-Braun Obsessiv-Kompulsiv Şkalası",                                 "Yale-Brown Obsessive Compulsive Scale (Y-BOCS)"),
    ("YMRS",         "Yanq Maniya Reytinq Şkalası",                                          "Young Mania Rating Scale (YMRS)"),
]

def build_table():
    rows = ['<tr><th>Abbreviatura</th><th>Azərbaycanca tam adı</th><th>İngilis dilində</th></tr>']
    for abbr, az, en in ROWS:
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
# STEP 1 — Update abbreviatur.html
# ════════════════════════════════════════════════════════
abbr_path = os.path.join(BASE, 'abbreviatur.html')
with open(abbr_path, encoding='utf-8') as f:
    abbr = f.read()
abbr = nfc(abbr)

abbr_new = re.sub(
    r'<h1[^>]+id="terminoloji[^"]*"[^>]*>TERMİNOLOJİ LÜĞƏT</h1>.*?<hr>',
    nfc(NEW_SECTION),
    abbr,
    count=1,
    flags=re.DOTALL
)
if abbr_new != abbr:
    with open(abbr_path, 'w', encoding='utf-8') as f:
        f.write(abbr_new)
    print(f'OK abbreviatur.html — {len(ROWS)} entries')
else:
    print('MISS abbreviatur.html')

# ════════════════════════════════════════════════════════
# STEP 2 — Remove QISALTMALAR from index.html
# ════════════════════════════════════════════════════════
idx_path = os.path.join(BASE, 'index.html')
with open(idx_path, encoding='utf-8') as f:
    idx = f.read()
idx = nfc(idx)

# Remove <hr> + <h2 id="qisaltmalar"> ... </table></div> + <hr>
idx_new = re.sub(
    r'<hr>\s*<h2[^>]+id="qisaltmalar"[^>]*>.*?</table></div>\s*<hr>',
    '',
    idx,
    count=1,
    flags=re.DOTALL
)
if idx_new != idx:
    with open(idx_path, 'w', encoding='utf-8') as f:
        f.write(idx_new)
    print('OK index.html — QISALTMALAR removed')
else:
    print('MISS index.html')

# ════════════════════════════════════════════════════════
# STEP 3 — Remove QISALTMALAR from elave-acde.html
# ════════════════════════════════════════════════════════
ea_path = os.path.join(BASE, 'elave-acde.html')
with open(ea_path, encoding='utf-8') as f:
    ea = f.read()
ea = nfc(ea)

# Remove <hr> + <h1 id="qisaltmalar-..."> ... </table></div>
# (the <hr> before ÜMUMİ MƏNBƏLƏR stays)
ea_new = re.sub(
    r'<hr>\s*<h1[^>]+id="[^"]*qisaltmalar[^"]*"[^>]*>.*?</table></div>',
    '',
    ea,
    count=1,
    flags=re.DOTALL
)
if ea_new != ea:
    with open(ea_path, 'w', encoding='utf-8') as f:
        f.write(ea_new)
    print('OK elave-acde.html — QISALTMALAR VƏ AKRONİMLƏR removed')
else:
    print('MISS elave-acde.html')

print(f'\nDone. Total entries in TERMİNOLOJİ LÜĞƏT: {len(ROWS)}')
