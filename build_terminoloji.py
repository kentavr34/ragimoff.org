#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rebuild abbreviatur.html as full TERMİNOLOJİ LÜĞƏT with three sections:
  1. Abbreviaturalar  — AZ | RU | EN  (129 entries)
  2. Pozuntular       — Kod | AZ | EN | RU | Rəsmi (✓/✗/—)
  3. Terminlər        — AZ | RU | EN
"""
import sys, io, os, re, unicodedata

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r"C:\Users\SAM\Desktop\sayt2\klinik-psixiatriya"
def nfc(s): return unicodedata.normalize('NFC', s)

# ════════════════════════════════════════════════════════════════════
# TABLE 1 — ABBREVIATURALAR  (AZ | RU | EN)
# ════════════════════════════════════════════════════════════════════
ABBR = [
    # abbr | AZ tam adı | RU tam adı | EN tam adı
    ("AAP",       "Atipik (İkinci Nəsil) Antipsixotiklər",                     "Атипичные антипсихотики",                                                "Atypical / Second-Generation Antipsychotics (AAP/SGA)"),
    ("AACAP",     "Amerika Uşaq və Yeniyetmə Psixiatriyası Akademiyası",       "Американская академия детской и подростковой психиатрии",                "American Academy of Child & Adolescent Psychiatry (AACAP)"),
    ("ACE",       "Mənfi Uşaqlıq Təcrübələri",                                 "Неблагоприятный детский опыт",                                           "Adverse Childhood Experiences (ACE)"),
    ("ACT",       "Qəbul və Öhdəlik Terapiyası",                               "Терапия принятия и ответственности (ТПО)",                               "Acceptance and Commitment Therapy (ACT)"),
    ("AİP",       "Alkoqol İstifadəsi Pozuntusu",                              "Расстройство употребления алкоголя (РУА)",                               "Alcohol Use Disorder (AUD)"),
    ("ANO",       "Nevrotik Anoreksiya",                                        "Нервная анорексия (НА)",                                                 "Anorexia Nervosa (AN)"),
    ("APA",       "Amerika Psixiatrik Birliyi",                                 "Американская психиатрическая ассоциация (АПА)",                          "American Psychiatric Association (APA)"),
    ("ARFİD",     "Qaçınmalı/Məhdudlaşdırıcı Qida Qəbulu Pozuntusu",          "Расстройство избегающего/ограниченного употребления пищи",               "Avoidant/Restrictive Food Intake Disorder (ARFID)"),
    ("ASP",       "Autizm Spektri Pozuntusu",                                  "Расстройство аутистического спектра (РАС)",                              "Autism Spectrum Disorder (ASD)"),
    ("ASPD",      "Antisosial Şəxsiyyət Pozuntusu",                           "Антисоциальное расстройство личности",                                   "Antisocial Personality Disorder (ASPD)"),
    ("BDD (6B21)","Bədən Dismorfik Pozuntusu (XBT-11: 6B21)",                 "Дисморфическое расстройство тела / дисморфофобия (МКБ-11: 6B21)",        "Body Dysmorphic Disorder (ICD-11: 6B21)"),
    ("BDD (6C20)","Bədən Sıxıntı Pozuntusu (XBT-11: 6C20)",                   "Расстройство телесного дистресса (МКБ-11: 6C20)",                        "Bodily Distress Disorder (ICD-11: 6C20)"),
    ("BDP",       "Bədən Dismorfik Pozuntusu",                                 "Дисморфическое расстройство тела",                                       "Body Dysmorphic Disorder (BDD)"),
    ("BİİP",      "Bipolyar II Pozuntu",                                       "Биполярное расстройство II типа",                                        "Bipolar II Disorder (BD-II)"),
    ("BİP",       "Bipolyar I Pozuntu",                                        "Биполярное расстройство I типа",                                         "Bipolar I Disorder (BD-I)"),
    ("BKİ",       "Bədən Kütlə İndeksi",                                      "Индекс массы тела (ИМТ)",                                                "Body Mass Index (BMI)"),
    ("BNO",       "Nevrotik Bulimiya",                                         "Нервная булимия (НБ)",                                                   "Bulimia Nervosa (BN)"),
    ("BP",        "Bipolyar Pozuntu (ümumi)",                                  "Биполярное расстройство (БР)",                                           "Bipolar Disorder (BD)"),
    ("BPD",       "Sərhəd Şəxsiyyət Pozuntusu (ingilis ixtisarı)",            "Пограничное расстройство личности (ПРЛ)",                                "Borderline Personality Disorder (BPD)"),
    ("BPRS",      "Qısa Psixiatrik Reytinq Şkalası",                          "Краткая психиатрическая оценочная шкала",                                "Brief Psychiatric Rating Scale (BPRS)"),
    ("BZD",       "Benzodiazepin",                                             "Бензодиазепин (БЗД)",                                                    "Benzodiazepine (BZD)"),
    ("CAPS",      "TSSP üçün Klinik İdarəolunan PTSD Şkalası",                "Клинически вводимая шкала ПТСР",                                         "Clinician-Administered PTSD Scale (CAPS)"),
    ("CAT",       "Koqnitiv Analitik Terapiya",                                "Когнитивно-аналитическая терапия (КАТ)",                                 "Cognitive Analytic Therapy (CAT)"),
    ("CDDG",      "Klinik Təsvirlər və Diaqnostik Tələblər (XBT-10, 1992)",   "Клинические описания и диагностические указания (МКБ-10, ВОЗ, 1992)",    "Clinical Descriptions and Diagnostic Guidelines (ICD-10, 1992)"),
    ("CD",        "Davranış Pozuntusu",                                        "Расстройство поведения",                                                 "Conduct Disorder (CD)"),
    ("CGI",       "Klinik Qlobal Qiymətləndirmə",                             "Шкала общего клинического впечатления",                                  "Clinical Global Impression (CGI)"),
    ("CPAP",      "Davamlı Müsbət Hava Yolu Təzyiqi",                         "Постоянное положительное давление в дыхательных путях (СИПАП)",          "Continuous Positive Airway Pressure (CPAP)"),
    ("CSBD",      "Kompulsiv Cinsi Davranış Pozuntusu",                        "Компульсивное сексуальное расстройство поведения",                       "Compulsive Sexual Behaviour Disorder (CSBD)"),
    ("DBT",       "Dialektik Davranış Terapiyası",                             "Диалектическая поведенческая терапия (ДПТ)",                             "Dialectical Behaviour Therapy (DBT)"),
    ("DDHP",      "Diqqət Defisiti və Hiperaktivlik Pozuntusu",                "Синдром дефицита внимания и гиперактивности (СДВГ)",                     "Attention-Deficit/Hyperactivity Disorder (ADHD)"),
    ("DMDD",      "Disruptiv Əhval Disrequlasiya Pozuntusu (DSM-5)",          "Деструктивное расстройство дисрегуляции настроения",                     "Disruptive Mood Dysregulation Disorder (DMDD)"),
    ("DPT",       "Dinamik Psixoterapiya",                                     "Динамическая психотерапия",                                              "Dynamic Psychotherapy (DPT)"),
    ("DPDR",      "Depersonalizasiya-Derealizasiya Pozuntusu",                 "Расстройство деперсонализации/дереализации",                             "Depersonalization-Derealization Disorder (DPDR)"),
    ("DSM-5-TR",  "Psixi Pozuntuların Diaqnostik və Statistik Təlimatı, 5-ci nəşr, Mətn Yeniləməsi", "Диагностическое и статистическое руководство по психическим расстройствам, 5-е изд., текстовая ревизия (ДСМ-5-ТР)", "Diagnostic and Statistical Manual of Mental Disorders, 5th Edition, Text Revision (DSM-5-TR)"),
    ("DSP",       "Dissosiativ Şəxsiyyət Pozuntusu",                           "Диссоциативное расстройство идентичности (ДРИ)",                         "Dissociative Identity Disorder (DID)"),
    ("EBM",       "Sübutlara Əsaslanan Tibb",                                  "Доказательная медицина (ДМ)",                                            "Evidence-Based Medicine (EBM)"),
    ("EEG",       "Elektroensefaloqrafiya",                                    "Электроэнцефалография (ЭЭГ)",                                            "Electroencephalography (EEG)"),
    ("EFT",       "Emosional Fokuslu Terapiya",                                "Эмоционально-фокусированная терапия (ЭФТ)",                              "Emotion-Focused Therapy (EFT)"),
    ("EKT",       "Elektrokonvulsiv Terapiya",                                 "Электросудорожная терапия (ЭСТ)",                                        "Electroconvulsive Therapy (ECT)"),
    ("EMDR",      "Göz Hərəkəti ilə Həssaslaşdırma və Yenidən İşləmə",       "Десенсибилизация и переработка движениями глаз (ДПДГ)",                  "Eye Movement Desensitization and Reprocessing (EMDR)"),
    ("EPDS",      "Edinburq Doğuşdan Sonrakı Depressiya Şkalası",              "Эдинбургская шкала послеродовой депрессии",                              "Edinburgh Postnatal Depression Scale (EPDS)"),
    ("EPM",       "Eksperimental-Psixoloji Müayinə",                           "Экспериментально-психологическое исследование (ЭПИ)",                    "Experimental Psychological Examination (EPM)"),
    ("FBT",       "Ailə Əsaslı Müalicə",                                      "Семейная терапия / Семейное лечение",                                    "Family-Based Treatment (FBT)"),
    ("FDIA",      "Başqasına Tətbiq Edilmiş Süni Pozuntu",                     "Искусственное расстройство, обращённое на другого",                      "Factitious Disorder Imposed on Another (FDIA)"),
    ("FDIS",      "Özünə Tətbiq Edilmiş Süni Pozuntu",                        "Искусственное расстройство, обращённое на себя",                         "Factitious Disorder Imposed on Self (FDIS)"),
    ("FII",       "Uydurulmuş/Törədilmiş Xəstəlik",                           "Сфабрикованная или индуцированная болезнь",                              "Fabricated or Induced Illness (FII)"),
    ("GAD-7",     "Generalizə Olunmuş Təşviş Şkalası-7",                      "Шкала генерализованного тревожного расстройства-7",                      "Generalized Anxiety Disorder Scale-7 (GAD-7)"),
    ("GAP",       "Generalizə Olunmuş Təşviş Pozuntusu",                       "Генерализованное тревожное расстройство (ГТР)",                          "Generalized Anxiety Disorder (GAD)"),
    ("HAND",      "HIV ilə Əlaqəli Neyrokoqnitiv Pozuntu",                    "ВИЧ-ассоциированное нейрокогнитивное расстройство",                      "HIV-Associated Neurocognitive Disorder (HAND)"),
    ("HARS",      "Hamilton Narahatlıq Reytinq Şkalası",                       "Шкала тревоги Гамильтона (HARS/ШТГ)",                                   "Hamilton Anxiety Rating Scale (HARS)"),
    ("HBS",       "Huzursuz Bacaq Sindromu",                                   "Синдром беспокойных ног (СБН)",                                          "Restless Legs Syndrome (RLS)"),
    ("HDRS",      "Hamilton Depressiya Reytinq Şkalası",                       "Шкала депрессии Гамильтона (HDRS/ШДГ)",                                 "Hamilton Depression Rating Scale (HDRS/HAM-D)"),
    ("HPA",       "Hipotalamus-Hipofiz-Böyrəküstü Vəzi Oxu",                  "Гипоталамо-гипофизарно-надпочечниковая ось (ГГН-ось)",                   "Hypothalamic-Pituitary-Adrenal Axis (HPA)"),
    ("IACAPAP",   "Uşaq və Yeniyetmə Psixiatriyası Beynəlxalq Assosiasiyası","Международная ассоциация детской и подростковой психиатрии",             "International Assoc. for Child & Adolescent Psychiatry (IACAPAP)"),
    ("IED",       "İntermittent Eksplosiv Pozuntu",                            "Интермиттирующее эксплозивное расстройство",                             "Intermittent Explosive Disorder (IED)"),
    ("IPA",       "Beynəlxalq Psixoanalitik Assosiasiya",                      "Международная психоаналитическая ассоциация (МПА)",                      "International Psychoanalytic Association (IPA)"),
    ("IPA",       "Beynəlxalq Psixogeriatrik Assosiasiya",                     "Международная психогериатрическая ассоциация",                           "International Psychogeriatric Association (IPA)"),
    ("IPAS",      "Beynəlxalq Psixoterapiya Assosiasiyası",                    "Международная ассоциация психотерапии",                                  "International Psychotherapy Association (IPAS)"),
    ("ISBD",      "Bipolyar Pozuntular üzrə Beynəlxalq Cəmiyyət",            "Международное общество биполярных расстройств",                          "International Society for Bipolar Disorders (ISBD)"),
    ("ISSTD",     "Travma və Dissosiasiya Tədqiqatı üzrə Beynəlxalq Cəmiyyət","Международное общество исследования травмы и диссоциации",              "International Society for the Study of Trauma and Dissociation (ISSTD)"),
    ("ISTSS",     "Travmatik Stress Tədqiqatları üçün Beynəlxalq Cəmiyyət",  "Международное общество по изучению травматического стресса",             "International Society for Traumatic Stress Studies (ISTSS)"),
    ("İİP",       "İntellektual İnkişaf Pozuntusu",                            "Расстройство интеллектуального развития (РИР)",                          "Intellectual Developmental Disorder (IDD)"),
    ("İPT",       "Şəxslərarası Terapiya",                                     "Интерперсональная терапия (ИПТ)",                                        "Interpersonal Therapy (IPT)"),
    ("KDT",       "Koqnitiv Davranış Terapiyası",                              "Когнитивно-поведенческая терапия (КПТ)",                                 "Cognitive Behavioural Therapy (CBT)"),
    ("KDT-İ",     "İnsomnia üçün Koqnitiv Davranış Terapiyası",               "КПТ при инсомнии (КПТ-И)",                                               "Cognitive Behavioural Therapy for Insomnia (CBT-I)"),
    ("KTSSP",     "Kompleks Travma Sonrası Stress Pozuntusu",                  "Комплексное ПТСР (К-ПТСР)",                                              "Complex Post-Traumatic Stress Disorder (cPTSD)"),
    ("KTTD",      "Klinik Təsvirlər və Diaqnostik Tələblər (ÜST, XBT-11, 2024)", "Клинические описания и диагностические требования (МКБ-11, ВОЗ, 2024)", "Clinical Descriptions and Diagnostic Guidelines (ICD-11, WHO, 2024)"),
    ("Li",        "Litium",                                                    "Литий (Ли)",                                                             "Lithium (Li)"),
    ("MAOİ",      "Monoaminooksidaza İnhibitorları",                           "Ингибиторы моноаминоксидазы (ИМАО)",                                     "Monoamine Oxidase Inhibitors (MAOI)"),
    ("MBT",       "Mentalizasiyaya Əsaslanan Terapiya",                        "Ментализационная терапия (МТ)",                                          "Mentalization-Based Treatment (MBT)"),
    ("MCI",       "Yüngül Koqnitiv Pozuntu",                                   "Лёгкое когнитивное расстройство (ЛКР)",                                  "Mild Cognitive Impairment (MCI)"),
    ("MDP",       "Major Depressiv Pozuntu",                                   "Большое депрессивное расстройство (БДР)",                                "Major Depressive Disorder (MDD)"),
    ("MDMA",      "3,4-metilendioksimetamfetamin (maddə)",                     "3,4-метилендиоксиметамфетамин (МДМА)",                                   "3,4-Methylenedioxymethamphetamine (MDMA)"),
    ("MDQ",       "Əhval Pozuntusu Sorğusu",                                   "Опросник расстройств настроения (ОРН)",                                  "Mood Disorder Questionnaire (MDQ)"),
    ("mhGAP",     "Ruhi Sağlamlıq Boşluğu Fəaliyyət Proqramı (ÜST)",         "Программа ликвидации разрыва в области психического здоровья (ВОЗ)",      "Mental Health Gap Action Programme (mhGAP, WHO)"),
    ("MI",        "Motivasional Müsahibə",                                     "Мотивационное интервьюирование (МИ)",                                    "Motivational Interviewing (MI)"),
    ("MINI",      "Mini Beynəlxalq Nöropsixiatrik Müsahibə",                  "Международное мини-нейропсихиатрическое интервью",                        "Mini International Neuropsychiatric Interview (MINI)"),
    ("MMPI",      "Minnesota Çoxfazalı Şəxsiyyət İnventarı",                 "Миннесотский многоаспектный личностный опросник (ММPI)",                 "Minnesota Multiphasic Personality Inventory (MMPI)"),
    ("MMSE",      "Mini Ruhi Vəziyyət Müayinəsi",                             "Краткое исследование психического состояния (КИПС/MMSE)",                "Mini-Mental State Examination (MMSE)"),
    ("MNN",       "Beynəlxalq Patentləşdirilməmiş Ad",                        "Международное непатентованное наименование (МНН)",                       "International Nonproprietary Name (INN/MNN)"),
    ("MoKQ",      "Monreal Koqnitiv Qiymətləndirməsi",                        "Монреальская когнитивная оценка (МоКА/MoCA)",                            "Montreal Cognitive Assessment (MoCA)"),
    ("MRI",       "Maqnit Rezonans Tomoqrafiyası",                             "Магнитно-резонансная томография (МРТ)",                                  "Magnetic Resonance Imaging (MRI)"),
    ("MS",        "Multipl Skleroz",                                           "Рассеянный склероз (РС)",                                                "Multiple Sclerosis (MS)"),
    ("MST",       "Multisistem Terapiyası",                                    "Мультисистемная терапия (МСТ)",                                          "Multisystemic Therapy (MST)"),
    ("MSLT",      "Çoxlu Yuxu Latensiyası Testi",                             "Тест множественной латентности сна (ТМЛС)",                              "Multiple Sleep Latency Test (MSLT)"),
    ("NİPNİ",     "Bexterev adına Psixonevroloji Elmi-Tədqiqat İnstitutu",   "НИПНИ им. В.М. Бехтерева",                                              "V.M. Bekhterev Psychoneurological Research Institute (NIPNI)"),
    ("NICE",      "Milli Sağlamlıq və Klinik Mükəmməllik İnstitutu (Böyük Britaniya)", "Национальный институт здравоохранения и клинического совершенства (Великобритания)", "National Institute for Health and Care Excellence (NICE, UK)"),
    ("NKP",       "Neyrokoqnitiv Pozuntu",                                     "Нейрокогнитивное расстройство (НКР)",                                    "Neurocognitive Disorder (NCD)"),
    ("NMS",       "Neyroleptik Maliqn Sindromu",                               "Злокачественный нейролептический синдром (ЗНС)",                         "Neuroleptic Malignant Syndrome (NMS)"),
    ("NREM",      "Sürətli Olmayan Göz Hərəkəti (yuxu fazası)",               "Сон без быстрых движений глаз (NREM)",                                   "Non-Rapid Eye Movement (NREM)"),
    ("OCRD",      "Obsessiv-Kompulsiv və Əlaqəli Pozuntular",                  "Обсессивно-компульсивные и связанные расстройства",                      "Obsessive-Compulsive and Related Disorders (OCRD)"),
    ("ODD",       "Oppozisiya-Etiraz Pozuntusu",                               "Оппозиционно-вызывающее расстройство (ОВР)",                             "Oppositional Defiant Disorder (ODD)"),
    ("OİP",       "Opioid İstifadəsi Pozuntusu",                              "Расстройство употребления опиоидов",                                     "Opioid Use Disorder (OUD)"),
    ("OKP",       "Obsessiv-Kompulsiv Pozuntu",                                "Обсессивно-компульсивное расстройство (ОКР)",                            "Obsessive-Compulsive Disorder (OCD)"),
    ("OSA",       "Obstruktiv Yuxu Apnoesi",                                   "Обструктивное апноэ сна (ОАС)",                                          "Obstructive Sleep Apnea (OSA)"),
    ("PANSS",     "Müsbət və Mənfi Simptom Şkalası",                          "Шкала позитивных и негативных синдромов (PANSS/ШПНС)",                  "Positive and Negative Syndrome Scale (PANSS)"),
    ("PCL-5",     "PTSD Yoxlama Siyahısı (DSM-5)",                            "Контрольный перечень симптомов ПТСР (PCL-5)",                            "PTSD Checklist for DSM-5 (PCL-5)"),
    ("PDE5",      "Fosfodiesteraz-5 inhibitoru",                               "Ингибитор фосфодиэстеразы-5 (иФДЭ-5)",                                  "Phosphodiesterase-5 Inhibitor (PDE5i)"),
    ("PGD",       "Uzanmış Kədər Pozuntusu",                                   "Пролонгированное расстройство горя (ПРГ)",                               "Prolonged Grief Disorder (PGD)"),
    ("PHQ-9",     "Pasiyent Sağlamlıq Sorğusu-9",                             "Опросник здоровья пациента-9 (PHQ-9)",                                   "Patient Health Questionnaire-9 (PHQ-9)"),
    ("PMT",       "Valideyn Davranış Terapiyası",                              "Тренинг родительских навыков (ТРН)",                                     "Parent Management Training (PMT)"),
    ("PNES",      "Psixogen Qeyri-Epileptik Tutmalar",                         "Психогенные неэпилептические приступы (ПНЭП)",                           "Psychogenic Non-Epileptic Seizures (PNES)"),
    ("PSQ",       "Polisomnoqrafiya",                                           "Полисомнография (ПСГ)",                                                  "Polysomnography (PSG)"),
    ("RBD",       "REM Yuxu Davranış Pozuntusu",                               "Расстройство поведения в фазе быстрого сна (РПБС)",                      "REM Sleep Behaviour Disorder (RBD)"),
    ("REM",       "Sürətli Göz Hərəkəti (yuxu fazası)",                        "Быстрые движения глаз (БДГ/REM)",                                        "Rapid Eye Movement (REM)"),
    ("SCID",      "DSM üzrə Struktur Klinik Müsahibə",                        "Структурированное клиническое интервью для DSM (СКИД)",                  "Structured Clinical Interview for DSM (SCID)"),
    ("SİUSİ",     "Serotoninin Seçici Geri-Alınma İnhibitorları",              "Селективные ингибиторы обратного захвата серотонина (СИОЗС)",            "Selective Serotonin Reuptake Inhibitors (SSRI)"),
    ("SNP",       "Sosial Narahatlıq Pozuntusu",                               "Социальное тревожное расстройство (СТР)",                                "Social Anxiety Disorder (SAD)"),
    ("SNRİ",      "Serotonin-Noradrenalin Geri-Alınma İnhibitorları",         "Ингибиторы обратного захвата серотонина и норадреналина (ИОЗСН)",        "Serotonin-Norepinephrine Reuptake Inhibitors (SNRI)"),
    ("SSD",       "Somatik Simptom Pozuntusu",                                 "Соматическое симптомное расстройство (ССР)",                             "Somatic Symptom Disorder (SSD)"),
    ("SSRİ",      "Serotoninin Seçici Geri-Alınma İnhibitorları (ing. ixt.)", "СИОЗС — см. SİUSİ",                                                     "SSRI — see SİUSİ"),
    ("TBZ",       "Travmatik Beyin Zədəsi",                                    "Черепно-мозговая травма (ЧМТ)",                                          "Traumatic Brain Injury (TBI/TBZ)"),
    ("TF-KDT",    "Travmaya Yönəldilmiş Koqnitiv Davranış Terapiyası",        "КПТ, ориентированная на травму (Т-КПТ)",                                 "Trauma-Focused Cognitive Behavioural Therapy (TF-CBT)"),
    ("TFP",       "Köçürülmə Fokuslu Psixoterapiya",                           "Терапия, фокусированная на переносе (ТФП)",                              "Transference-Focused Psychotherapy (TFP)"),
    ("TİP",       "Tipik (Birinci Nəsil) Antipsixotiklər",                    "Типичные (первого поколения) антипсихотики (АПП-I)",                     "First-Generation Antipsychotics (FGA)"),
    ("TMS",       "Transkranial Maqnit Stimulyasiya",                          "Транскраниальная магнитная стимуляция (ТМС)",                            "Transcranial Magnetic Stimulation (TMS)"),
    ("TSSP",      "Travma Sonrası Stress Pozuntusu",                           "Посттравматическое стрессовое расстройство (ПТСР)",                      "Post-Traumatic Stress Disorder (PTSD)"),
    ("TsAD",      "Trisiklik Antidepressantlar",                               "Трициклические антидепрессанты (ТЦА)",                                   "Tricyclic Antidepressants (TCA)"),
    ("TYP",       "Tıxanma ilə Yemə Pozuntusu",                               "Расстройство переедания / приступообразное переедание",                  "Binge Eating Disorder (BED)"),
    ("ÜST",       "Ümumdünya Səhiyyə Təşkilatı",                              "Всемирная организация здравоохранения (ВОЗ)",                            "World Health Organization (WHO)"),
    ("VPA",       "Valproat turşusu",                                          "Вальпроевая кислота (ВК)",                                               "Valproic Acid (VPA)"),
    ("WFSBP",     "Bioloji Psixiatriya Cəmiyyətlərinin Dünya Federasiyası",   "Всемирная федерация обществ биологической психиатрии (ВФОБП)",           "World Federation of Societies of Biological Psychiatry (WFSBP)"),
    ("WPA",       "Dünya Psixiatrik Assosiasiyası",                            "Всемирная психиатрическая ассоциация (ВПА)",                             "World Psychiatric Association (WPA)"),
    ("WPATH",     "Transseksual Sağlamlığı üçün Dünya Peşəkarlar Assosiasiyası","Всемирная профессиональная ассоциация по трансгендерному здоровью",   "World Professional Association for Transgender Health (WPATH)"),
    ("XAP",       "Xəstəlik Həyəcanı Pozuntusu",                              "Тревожное расстройство болезни (тревога о здоровье)",                   "Illness Anxiety Disorder (IAD)"),
    ("XBT-10",    "Xəstəliklərin Beynəlxalq Təsnifatı, 10-cu nəşr",          "Международная классификация болезней, 10-й пересмотр (МКБ-10)",          "International Classification of Diseases, 10th Revision (ICD-10)"),
    ("XBT-11",    "Xəstəliklərin Beynəlxalq Təsnifatı, 11-ci nəşr",          "Международная классификация болезней, 11-й пересмотр (МКБ-11)",          "International Classification of Diseases, 11th Revision (ICD-11)"),
    ("Y-BOCS",    "Yel-Braun Obsessiv-Kompulsiv Şkalası",                      "Шкала обсессий и компульсий Йеля-Брауна (Й-BOCS)",                      "Yale-Brown Obsessive Compulsive Scale (Y-BOCS)"),
    ("YMRS",      "Yanq Maniya Reytinq Şkalası",                               "Шкала мании Янга (YMRS/ШМЯ)",                                           "Young Mania Rating Scale (YMRS)"),
]

# ════════════════════════════════════════════════════════════════════
# TABLE 2 — POZUNTULAR  (Kod | AZ | EN | RU | Rəsmi ✓/✗/—)
# Rəsmi column: — = pending verification against AZ MoH / AzPA sources
# ════════════════════════════════════════════════════════════════════
POZUNTULAR = [
    # kod | AZ (saytda) | EN (ICD-11 official) | RU (МКБ-11) | rəsmi
    ("6A00",    "İntellektual İnkişaf Pozuntusu",                        "Intellectual Developmental Disorder (IDD)",                         "Расстройство интеллектуального развития",                  "—"),
    ("6A01",    "İnkişaf Nitq və Dil Pozuntuları",                       "Developmental Speech or Language Disorder",                         "Расстройство развития речи или языка",                     "—"),
    ("6A02",    "Autizm Spektri Pozuntusu (ASP)",                        "Autism Spectrum Disorder (ASD)",                                    "Расстройство аутистического спектра (РАС)",                "—"),
    ("6A03",    "İnkişaf Öyrənmə Pozuntusu",                             "Developmental Learning Disorder",                                   "Расстройство развития обучения",                           "—"),
    ("6A04",    "İnkişaf Hərəki Koordinasiya Pozuntusu",                 "Developmental Motor Coordination Disorder (DCD)",                   "Расстройство двигательной координации",                    "—"),
    ("6A05",    "Diqqət Defisiti və Hiperaktivlik Pozuntusu (DDHP)",     "Attention-Deficit/Hyperactivity Disorder (ADHD)",                   "Синдром дефицита внимания и гиперактивности (СДВГ)",       "—"),
    ("6A06",    "Stereotipik Hərəkət Pozuntusu",                         "Stereotyped Movement Disorder",                                     "Стереотипное двигательное расстройство",                   "—"),
    ("6A07",    "Tikli Pozuntular və Tourette Sindromu",                  "Tourette Syndrome and Other Tic Disorders",                         "Синдром Туретта и тикозные расстройства",                  "—"),
    ("6A20",    "Şizofreniya",                                            "Schizophrenia",                                                     "Шизофрения",                                               "—"),
    ("6A21",    "Şizoaffektiv Pozuntu",                                   "Schizoaffective Disorder",                                          "Шизоаффективное расстройство",                             "—"),
    ("6A22",    "Şizotipik Pozuntu",                                      "Schizotypal Disorder",                                              "Шизотипическое расстройство",                              "—"),
    ("6A24",    "Sayıqlama Pozuntusu",                                    "Delusional Disorder",                                               "Бредовое расстройство",                                    "—"),
    ("6A23",    "Kəskin və Keçici Psixotik Pozuntu",                     "Acute and Transient Psychotic Disorder",                            "Острое и транзиторное психотическое расстройство",         "—"),
    ("6A25",    "İlkin Psixotik Pozuntuların Simptom Domenləri",         "Symptom Domains of Primary Psychotic Disorders",                    "Симптоматические домены первичных психотических расстройств","—"),
    ("6A40",    "Katatoniya",                                             "Catatonia",                                                         "Кататония",                                                "—"),
    ("6A60",    "Depressiv Pozuntular (ümumi)",                           "Depressive Disorders",                                              "Депрессивные расстройства",                                "—"),
    ("6A62",    "Distimik Pozuntu",                                       "Dysthymic Disorder (Persistent Depressive Disorder)",               "Дистимическое расстройство",                               "—"),
    ("6A70",    "Bipolyar I Pozuntu",                                     "Bipolar I Disorder",                                                "Биполярное расстройство I типа",                           "—"),
    ("6A71",    "Bipolyar II Pozuntu",                                    "Bipolar II Disorder",                                               "Биполярное расстройство II типа",                          "—"),
    ("6A72",    "Siklotimik Pozuntu",                                     "Cyclothymic Disorder",                                              "Циклотимическое расстройство",                             "—"),
    ("6A73",    "Qarışıq Depressiv və Təşviş Pozuntusu",                 "Mixed Depressive and Anxiety Disorder",                             "Смешанное депрессивно-тревожное расстройство",            "—"),
    ("6B00",    "Generalizə Olunmuş Təşviş Pozuntusu",                   "Generalized Anxiety Disorder (GAD)",                                "Генерализованное тревожное расстройство (ГТР)",            "—"),
    ("6B01",    "Sosial Təşviş Pozuntusu (Sosial Fobiya)",               "Social Anxiety Disorder (Social Phobia)",                           "Социальное тревожное расстройство (социальная фобия)",     "—"),
    ("6B02",    "Aqorafobiya",                                            "Agoraphobia",                                                       "Агорафобия",                                               "—"),
    ("6B03",    "Panik Pozuntu",                                          "Panic Disorder",                                                    "Паническое расстройство",                                  "—"),
    ("6B04",    "Spesifik Fobiya",                                        "Specific Phobia",                                                   "Специфическая фобия",                                      "—"),
    ("6B05",    "Ayrılma Təşviş Pozuntusu",                              "Separation Anxiety Disorder",                                       "Расстройство тревоги разлучения",                          "—"),
    ("6B06",    "Selektiv Mutizm",                                        "Selective Mutism",                                                  "Избирательный мутизм",                                     "—"),
    ("6B20",    "Obsessiv-Kompulsiv Pozuntu (OKP)",                       "Obsessive-Compulsive Disorder (OCD)",                               "Обсессивно-компульсивное расстройство (ОКР)",              "—"),
    ("6B21",    "Bədən Dismorfik Pozuntusu",                              "Body Dysmorphic Disorder (BDD)",                                    "Дисморфическое расстройство тела / дисморфофобия",         "—"),
    ("6B22",    "Olfaktiv Referans Pozuntusu",                            "Olfactory Reference Disorder",                                      "Обонятельное референтное расстройство",                    "—"),
    ("6B23",    "Hipoxondriya (Xəstəlik Həyəcanı)",                      "Hypochondriasis / Health Anxiety Disorder",                         "Ипохондрия / тревога о здоровье",                          "—"),
    ("6B24",    "Yığma Pozuntusu",                                        "Hoarding Disorder",                                                 "Расстройство накопительства",                              "—"),
    ("6B25",    "Bədənə Yönəlik Repetitiv Davranış Pozuntuları",         "Body-Focused Repetitive Behaviour Disorders (BFRBDs)",              "Повторяющееся поведение, направленное на тело",            "—"),
    ("6B40",    "Posttravmatik Stress Pozuntusu (PTSP)",                  "Post-Traumatic Stress Disorder (PTSD)",                             "Посттравматическое стрессовое расстройство (ПТСР)",        "—"),
    ("6B41",    "Kompleks Posttravmatik Stress Pozuntusu (KPTSP)",        "Complex PTSD (cPTSD)",                                              "Комплексное ПТСР (К-ПТСР)",                                "—"),
    ("6B42",    "Uzanmış Kədər Pozuntusu",                               "Prolonged Grief Disorder (PGD)",                                    "Пролонгированное расстройство горя",                       "—"),
    ("6B43",    "Uyğunlaşma Pozuntusu",                                   "Adjustment Disorder",                                               "Расстройство адаптации",                                   "—"),
    ("6B4Z",    "Digər Stress Əlaqəli Pozuntular",                        "Other Stress-Related Disorders",                                    "Другие расстройства, связанные со стрессом",               "—"),
    ("6B60",    "Dissosiativ Nevroloji Simptom Pozuntusu",                "Dissociative Neurological Symptom Disorder",                        "Диссоциативное расстройство неврологических симптомов",    "—"),
    ("6B61",    "Dissosiativ Amneziya",                                   "Dissociative Amnesia",                                              "Диссоциативная амнезия",                                   "—"),
    ("6B62",    "Dissosiativ Fuqa",                                       "Dissociative Fugue",                                                "Диссоциативная фуга",                                      "—"),
    ("6B63",    "Trans Pozuntusu",                                        "Trance Disorder",                                                   "Трансовое расстройство",                                   "—"),
    ("6B64",    "Depersonalizasiya-Derealizasiya Pozuntusu",              "Depersonalization-Derealization Disorder",                          "Расстройство деперсонализации/дереализации",               "—"),
    ("6B65",    "Dissosiativ Şəxsiyyət Pozuntusu",                       "Dissociative Identity Disorder (DID)",                              "Диссоциативное расстройство идентичности (ДРИ)",           "—"),
    ("6B66",    "Qismən Dissosiativ Şəxsiyyət Pozuntusu",                "Partial Dissociative Identity Disorder",                            "Частичное диссоциативное расстройство идентичности",       "—"),
    ("6B80",    "Nevrotik Anoreksiya",                                    "Anorexia Nervosa",                                                  "Нервная анорексия",                                        "—"),
    ("6B81",    "Nevrotik Bulimiya",                                      "Bulimia Nervosa",                                                   "Нервная булимия",                                          "—"),
    ("6B82",    "Dövrü Yeyinmə Pozuntusu (BED)",                         "Binge Eating Disorder (BED)",                                       "Расстройство переедания (приступообразное переедание)",     "—"),
    ("6B83",    "Qaçınma/Məhdudlaşdırıcı Qida Qəbulu Pozuntusu (ARFİD)","Avoidant/Restrictive Food Intake Disorder (ARFID)",                 "Расстройство избегающего/ограниченного употребления пищи", "—"),
    ("6B84",    "Pika",                                                   "Pica",                                                              "Пика",                                                     "—"),
    ("6B85",    "Ruminasiya Pozuntusu",                                   "Rumination Disorder",                                               "Расстройство руминации",                                   "—"),
    ("6C00",    "Enurez",                                                 "Enuresis",                                                          "Энурез",                                                   "—"),
    ("6C01",    "Enkoprez",                                               "Encopresis",                                                        "Энкопрез",                                                 "—"),
    ("6C20",    "Bədən Disstres Pozuntusu",                              "Bodily Distress Disorder",                                          "Расстройство телесного дистресса",                         "—"),
    ("6C21",    "Bədən Bütövlüyünü Qavrama Pozuntusu",                   "Body Integrity Dysphoria",                                          "Дисфория целостности тела (апотемнофилия)",                "—"),
    ("6C40",    "Alkohol İstifadəsi və Asılılıq Pozuntusu",              "Alcohol Dependence / Alcohol Use Disorder",                         "Расстройство употребления алкоголя / алкогольная зависимость","—"),
    ("6C43",    "Kannabis İstifadəsi və Asılılıq Pozuntusu",             "Cannabis Dependence / Cannabis Use Disorder",                       "Расстройство употребления каннабиса",                      "—"),
    ("6C44",    "Stimulyant İstifadəsi Pozuntusu",                       "Stimulant Use Disorder",                                            "Расстройство употребления стимуляторов",                   "—"),
    ("6C45",    "Opioid İstifadəsi və Asılılıq Pozuntusu",               "Opioid Dependence / Opioid Use Disorder",                           "Расстройство употребления опиоидов / опиоидная зависимость","—"),
    ("6C4A",    "Sedativ, Hipnotik və Anksiolotik İstifadə Pozuntusu",   "Sedative, Hypnotic or Anxiolytic Use Disorder",                     "Расстройство употребления седативных/снотворных/анксиолитиков","—"),
    ("6C48",    "Nikotin Asılılığı",                                      "Nicotine Dependence",                                               "Никотиновая зависимость",                                  "—"),
    ("6C50",    "Qumar və Video-Oyun Asılılıq Pozuntusu",                "Gaming Disorder / Gambling Disorder",                               "Расстройство игровой деятельности (азартные игры / видеоигры)","—"),
    ("6C70",    "Epizodik Eksplosiv Pozuntu",                             "Intermittent Explosive Disorder (IED)",                             "Интермиттирующее эксплозивное расстройство",               "—"),
    ("6C71",    "Kleptomoniya",                                           "Kleptomania",                                                       "Клептомания",                                              "—"),
    ("6C72",    "Piromoniya",                                             "Pyromania",                                                         "Пиромания",                                                "—"),
    ("6C73",    "Kompulsiv Cinsi Davranış Pozuntusu",                     "Compulsive Sexual Behaviour Disorder (CSBD)",                       "Компульсивное сексуальное расстройство поведения",         "—"),
    ("6C90",    "Davranış-Dissosial Pozuntu",                             "Conduct-Dissocial Disorder",                                        "Расстройство поведения (диссоциальное)",                   "—"),
    ("6C91",    "Oppozisiya-Etiraz Pozuntusu (OEP)",                     "Oppositional Defiant Disorder (ODD)",                               "Оппозиционно-вызывающее расстройство (ОВР)",               "—"),
    ("6D10",    "Şəxsiyyət Pozuntusu — Ümumi Meyarlar",                 "Personality Disorder (General Criteria)",                           "Расстройство личности (общие критерии)",                   "—"),
    ("6D10.0",  "Şəxsiyyət Pozuntusunun Şiddət Dərəcəsi",               "Severity of Personality Disorder",                                  "Степень тяжести расстройства личности",                    "—"),
    ("6D10.1",  "Şəxsiyyət Xüsusiyyət Domenləri (AMPD)",                "Personality Trait Domain Specifiers",                               "Домены черт личности (AMPD)",                              "—"),
    ("6D11",    "Sərhəd Nümuməsi (Borderline pattern)",                  "Borderline Pattern Qualifier",                                      "Пограничный паттерн (ПРЛ)",                                "—"),
    ("6D10.2",  "Antisosial/Dissosial Nümuməsi",                         "Antisocial/Dissocial Pattern Qualifier",                            "Антисоциальный/диссоциальный паттерн",                     "—"),
    ("6D31–33", "Ekshibisionizm, Vuayerizm, Frottürizm",                 "Exhibitionistic, Voyeuristic, Frotteuristic Disorder",              "Эксгибиционизм, вуайеризм, фроттюризм",                   "—"),
    ("6D36",    "Pedofilik Pozuntu",                                      "Paedophilic Disorder",                                              "Педофилическое расстройство",                              "—"),
    ("6D3Z",    "Digər Parafilik Pozuntular",                             "Other Paraphilic Disorders",                                        "Другие парафилические расстройства",                       "—"),
    ("6D50",    "Özünə Uyğulanmış Süni Pozuntu",                        "Factitious Disorder Imposed on Self (FDIS)",                        "Искусственное расстройство, обращённое на себя",           "—"),
    ("6D51",    "Başqasına Uyğulanmış Süni Pozuntu",                    "Factitious Disorder Imposed on Another (FDIA)",                     "Искусственное расстройство, обращённое на другого",        "—"),
    ("6D70",    "Demensiya — Ümumi Prinsiplər",                          "Dementia / Major Neurocognitive Disorder (General)",                "Деменция / большое нейрокогнитивное расстройство (общее)", "—"),
    ("6D70",    "Alzheimer Xəstəliyindən Demensiya",                     "Dementia Due to Alzheimer Disease",                                 "Деменция при болезни Альцгеймера",                         "—"),
    ("6D7Z",    "Digər Demensiya Formaları",                              "Other Forms of Dementia",                                           "Другие формы деменции",                                    "—"),
    ("6D71",    "Yüngül Neyrokoqnitiv Pozuntu",                          "Mild Neurocognitive Disorder",                                      "Лёгкое нейрокогнитивное расстройство",                     "—"),
    ("6D75",    "Deliriyum",                                              "Delirium",                                                          "Делирий",                                                  "—"),
    ("6E20",    "Hamiləlik Dövründə Psixi Pozuntular",                   "Mental Disorders During Pregnancy",                                 "Психические расстройства во время беременности",           "—"),
    ("6E20.0",  "Erkən Doğuşdan Sonrakı Emosional Reaksiya (Baby blues)","Early Postpartum Emotional Response (Baby Blues)",                 "Ранняя послеродовая эмоциональная реакция (беби-блюз)",    "—"),
    ("6E20",    "Doğuşdan Sonrakı Depressiya (PPD)",                     "Postpartum Depression (PPD)",                                       "Послеродовая депрессия (ПРД)",                             "—"),
    ("6E21",    "Doğuşdan Sonrakı Psixoz (PPP)",                         "Postpartum Psychosis (PPP)",                                        "Послеродовой психоз (ПРП)",                                "—"),
    ("6E20",    "Doğuşdan Sonrakı Təşviş, OKP, PTSP",                   "Postpartum Anxiety, OCD, PTSD",                                     "Послеродовые тревожность, ОКР, ПТСР",                      "—"),
]

# ════════════════════════════════════════════════════════════════════
# TABLE 3 — TERMİNLƏR  (AZ | RU | EN)
# ════════════════════════════════════════════════════════════════════
TERMINLER = [
    # AZ | RU | EN
    ("Affekt (Duyğu tonusu)",          "Аффект",                                       "Affect"),
    ("Affektiv pozuntu",               "Аффективное расстройство",                     "Affective disorder"),
    ("Aqressivlik",                    "Агрессивность",                                "Aggressiveness"),
    ("Akathiziya",                     "Акатизия",                                     "Akathisia"),
    ("Ambivalentlik",                  "Амбивалентность",                              "Ambivalence"),
    ("Amneziya",                       "Амнезия",                                      "Amnesia"),
    ("Anhedonia",                      "Ангедония",                                    "Anhedonia"),
    ("Anksioliz",                      "Анксиолиз",                                    "Anxiolysis"),
    ("Antisosial davranış",            "Антисоциальное поведение",                     "Antisocial behaviour"),
    ("Assosiasiya pozuntusu",          "Расстройство ассоциаций",                      "Association disturbance"),
    ("Autopsixik dezorientasiya",      "Аутопсихическая дезориентация",                "Autopsychic disorientation"),
    ("Bioritm",                        "Биоритм",                                      "Biorhythm"),
    ("Davranış terapiyası",            "Поведенческая терапия",                        "Behaviour therapy"),
    ("Dekompensasiya",                 "Декомпенсация",                                "Decompensation"),
    ("Deluziya (Sayıqlama)",           "Бред / Делюзия",                               "Delusion"),
    ("Depersonalizasiya",              "Деперсонализация",                             "Depersonalization"),
    ("Derealizasiya",                  "Дереализация",                                 "Derealization"),
    ("Diaqnostik meyar",               "Диагностический критерий",                     "Diagnostic criterion"),
    ("Dinamika (klinik)",              "Динамика (клиническая)",                       "Clinical dynamics"),
    ("Dissosiasiya",                   "Диссоциация",                                  "Dissociation"),
    ("Düşüncə pozuntusu (formal)",     "Формальное расстройство мышления",             "Formal thought disorder"),
    ("Dysforiya",                      "Дисфория",                                     "Dysphoria"),
    ("Ehtiyatlı proqnoz",              "Осторожный прогноз",                           "Guarded prognosis"),
    ("Ekstremal stress",               "Экстремальный стресс",                         "Extreme stress"),
    ("Emosional labillik",             "Эмоциональная лабильность",                    "Emotional lability"),
    ("Empati",                         "Эмпатия",                                      "Empathy"),
    ("Epizod (psixiatrik)",            "Эпизод (психиатрический)",                     "Episode (psychiatric)"),
    ("Erkən müdaxilə",                 "Раннее вмешательство",                         "Early intervention"),
    ("Etioloji amil",                  "Этиологический фактор",                        "Aetiological factor"),
    ("Exzitasiya (həyəcan)",           "Экзитация (возбуждение)",                      "Excitation / Agitation"),
    ("Fobiya",                         "Фобия",                                        "Phobia"),
    ("Funksional pozuntu",             "Функциональное расстройство",                  "Functional disorder"),
    ("Hallusinasiya",                  "Галлюцинация",                                 "Hallucination"),
    ("Həyəcan (Əhval)",                "Тревога",                                      "Anxiety"),
    ("Hipertimiyanın",                 "Гипертимия",                                   "Hyperthymia"),
    ("Hipomaniya",                     "Гипомания",                                    "Hypomania"),
    ("İmpuls",                         "Импульс",                                      "Impulse"),
    ("İmpuls nəzarəti",                "Контроль импульсов",                           "Impulse control"),
    ("İnsomnia",                       "Инсомния / бессонница",                        "Insomnia"),
    ("İnteqrasiya (psixoterapevtik)",  "Интеграция (психотерапевтическая)",            "Integration (psychotherapeutic)"),
    ("Katatoniya",                     "Кататония",                                    "Catatonia"),
    ("Klinik müsahibə",                "Клиническое интервью",                         "Clinical interview"),
    ("Klinik remissiya",               "Клиническая ремиссия",                         "Clinical remission"),
    ("Komorbidlik",                    "Коморбидность",                                "Comorbidity"),
    ("Kompulsiya",                     "Компульсия",                                   "Compulsion"),
    ("Konversiya",                     "Конверсия",                                    "Conversion"),
    ("Kriz müdaxiləsi",                "Кризисное вмешательство",                      "Crisis intervention"),
    ("Maniya",                         "Мания",                                        "Mania"),
    ("Mentalizasiya",                  "Ментализация",                                 "Mentalisation"),
    ("Mənfi simptomlar",               "Негативные симптомы",                          "Negative symptoms"),
    ("Müşayiət edən xəstəlik",         "Сопутствующее заболевание",                    "Comorbid condition"),
    ("Müsbət simptomlar",              "Позитивные симптомы",                          "Positive symptoms"),
    ("Neyrobiologiya",                 "Нейробиология",                                "Neurobiology"),
    ("Neyrotransmitter",               "Нейротрансмиттер",                             "Neurotransmitter"),
    ("Obsessiya",                      "Обсессия",                                     "Obsession"),
    ("Paranoya",                       "Паранойя",                                     "Paranoia"),
    ("Patogenez",                      "Патогенез",                                    "Pathogenesis"),
    ("Prevalensiya",                   "Распространённость (превалентность)",          "Prevalence"),
    ("Prodromal dövr",                 "Продромальный период",                         "Prodromal period"),
    ("Psixomotor ləngimə",             "Психомоторная заторможенность",                "Psychomotor retardation"),
    ("Psixomotor həyəcanlanma",        "Психомоторное возбуждение",                    "Psychomotor agitation"),
    ("Psixoz",                         "Психоз",                                       "Psychosis"),
    ("Qavrayış",                       "Восприятие",                                   "Perception"),
    ("Qeyri-ixtiyari hərəkət",         "Непроизвольное движение",                      "Involuntary movement"),
    ("Recidiv / Qayıdış",              "Рецидив / возврат симптомов",                  "Relapse / recurrence"),
    ("Remissiya",                      "Ремиссия",                                     "Remission"),
    ("Rezilyentlik",                   "Резильентность / устойчивость",                "Resilience"),
    ("Rituallar (kompulsiv)",          "Ритуалы (компульсивные)",                      "Rituals (compulsive)"),
    ("Sosial funksionallıq",           "Социальное функционирование",                  "Social functioning"),
    ("Somatizasiya",                   "Соматизация",                                  "Somatisation"),
    ("Stresor",                        "Стрессор",                                     "Stressor"),
    ("Suisid (özünəqəsd)",             "Суицид",                                       "Suicide"),
    ("Suisidal ideya",                 "Суицидальные мысли / идеация",                 "Suicidal ideation"),
    ("Şüur pozuntusu",                 "Нарушение сознания",                           "Disturbance of consciousness"),
    ("Terapevtik alyans",              "Терапевтический альянс",                       "Therapeutic alliance"),
    ("Travma",                         "Травма",                                       "Trauma"),
    ("Vulnerabillik",                  "Уязвимость / предрасположенность",             "Vulnerability"),
    ("Xronik gedişat",                 "Хроническое течение",                          "Chronic course"),
    ("Yaddaş",                         "Память",                                       "Memory"),
    ("Yanaşı diaqnoz",                 "Коморбидный диагноз",                          "Comorbid diagnosis"),
]

# ════════════════════════════════════════════════════════════════════
# BUILD HTML
# ════════════════════════════════════════════════════════════════════
def abbr_table():
    rows = ['<tr><th>Abbreviatura</th><th>Azərbaycanca tam adı</th><th>Русский эквивалент</th><th>English equivalent</th></tr>']
    for a, az, ru, en in ABBR:
        rows.append(f'<tr><td>{a}</td><td>{az}</td><td>{ru}</td><td>{en}</td></tr>')
    return '\n'.join(rows)

def pozuntu_table():
    rows = ['<tr><th>Kod</th><th>Azərbaycanca (saytda)</th><th>English (ICD-11)</th><th>Русский (МКБ-11)</th><th class="col-rasmi">Rəsmi AZ</th></tr>']
    for k, az, en, ru, rasmi in POZUNTULAR:
        rasmi_cell = f'<td class="rasmi-cell">{rasmi}</td>'
        rows.append(f'<tr><td class="kod-cell">{k}</td><td>{az}</td><td>{en}</td><td>{ru}</td>{rasmi_cell}</tr>')
    return '\n'.join(rows)

def termin_table():
    rows = ['<tr><th>Azərbaycan dili</th><th>Русский язык</th><th>English</th></tr>']
    for az, ru, en in TERMINLER:
        rows.append(f'<tr><td>{az}</td><td>{ru}</td><td>{en}</td></tr>')
    return '\n'.join(rows)

NEW_CONTENT = f'''\
<h1 id="terminoloji-lüğət" class="h-section">TERMİNOLOJİ LÜĞƏT</h1>
<p>Bu səhifədə kitabda istifadə edilən <strong>abbreviaturalar</strong>, <strong>psixiatrik pozuntu adları</strong> və <strong>klinik terminlər</strong> üç dildə — azərbaycanca, rusca və ingiliscə — verilmişdir.</p>

<h2 id="abbreviaturalar">Abbreviaturalar</h2>
<p>Əlifba sırası ilə. Sütunlar: abbreviatura · azərbaycanca · rusca · ingiliscə.</p>
<div class="tbl-wrap"><table>
{abbr_table()}
</table></div>
<hr>

<h2 id="pozuntular-lüğəti">Psixiatrik Pozuntular — 3 Dildə</h2>
<p>XBT-11 kodları üzrə bütün pozuntular. Sonuncu sütun — Rəsmi AZ — Azərbaycan Səhiyyə Nazirliyi / AzPA mənbələri ilə müqayisə üçün nəzərdə tutulmuşdur (<span style="color:#2a9d5c">✓</span> uyğun, <span style="color:#e63946">✗</span> fərqli, — yoxlanılmayıb).</p>
<div class="tbl-wrap"><table>
{pozuntu_table()}
</table></div>
<hr>

<h2 id="terminler-lüğəti">Klinik Terminlər — 3 Dildə</h2>
<p>Psixiatriyada istifadə olunan əsas klinik terminlər.</p>
<div class="tbl-wrap"><table>
{termin_table()}
</table></div>
<hr>'''

# ════════════════════════════════════════════════════════════════════
# WRITE TO abbreviatur.html
# ════════════════════════════════════════════════════════════════════
abbr_path = os.path.join(BASE, 'abbreviatur.html')
with open(abbr_path, encoding='utf-8') as f:
    html = f.read()
html = nfc(html)

html_new = re.sub(
    r'<h1[^>]+id="terminoloji[^"]*"[^>]*>TERMİNOLOJİ LÜĞƏT</h1>.*?<hr>(?=\s*<nav class="page-nav")',
    nfc(NEW_CONTENT),
    html,
    count=1,
    flags=re.DOTALL
)

if html_new != html:
    with open(abbr_path, 'w', encoding='utf-8') as f:
        f.write(html_new)
    print(f'OK abbreviatur.html rebuilt:')
    print(f'  Abbreviaturalar: {len(ABBR)} entries (4 columns: AZ+RU+EN)')
    print(f'  Pozuntular:      {len(POZUNTULAR)} entries (4 columns + Rəsmi)')
    print(f'  Terminlər:       {len(TERMINLER)} entries (3 columns: AZ+RU+EN)')
else:
    print('MISS — pattern not found')
