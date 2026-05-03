#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Replace all Azerbaijani-language descriptions in XBT-11 and XBT-10 lines
with correct English international names across all klinik-psixiatriya files.
"""
import sys, io, os, unicodedata, glob

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r"C:\Users\SAM\Desktop\sayt2\klinik-psixiatriya"

# Each tuple: (filename, old_line_content, new_line_content)
# old/new = exact content of the full <div class="xbt-line">...</div> line
FIXES = [

    # ══════════════════════════════════════════════════════════════════════
    # bolme-02.html — Schizophrenia spectrum
    # ══════════════════════════════════════════════════════════════════════
    ('bolme-02.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A20</span> — Şizofreniya</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A20</span> — Schizophrenia</div>'),
    ('bolme-02.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F20</span> — Şizofreniya</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F20</span> — Schizophrenia</div>'),
    ('bolme-02.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A21</span> — Şizoaffektiv pozuntu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A21</span> — Schizoaffective disorder</div>'),
    ('bolme-02.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F25</span> — Şizoaffektiv pozuntu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F25</span> — Schizoaffective disorders</div>'),
    ('bolme-02.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A22</span> — Şizotipik pozuntu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A22</span> — Schizotypal disorder</div>'),
    ('bolme-02.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A23</span> — Kəskin və keçici psixotik pozuntu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A23</span> — Acute and transient psychotic disorder</div>'),
    ('bolme-02.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F23</span> — Kəskin və keçici psixotik pozuntu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F23</span> — Acute and transient psychotic disorders</div>'),
    # Two occurrences of F22 — same old text, replace_all handles both
    ('bolme-02.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F22</span> — Xroniki sayıqlama pozuntusu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F22</span> — Persistent delusional disorders</div>'),
    # "Sayiqlama pozuntusu" entry (line 1215, uses 6A22 code — keep code, fix name)
    ('bolme-02.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A22</span> — Sayiqlama pozuntusu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A22</span> — Delusional disorder</div>'),

    # ══════════════════════════════════════════════════════════════════════
    # bolme-04.html — Mood disorders
    # ══════════════════════════════════════════════════════════════════════
    ('bolme-04.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A60</span> — Depressiv pozuntular</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A60</span> — Depressive disorders</div>'),
    ('bolme-04.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F32</span> — Depressiv epizod</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F32</span> — Depressive episode</div>'),
    ('bolme-04.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A70</span> — Bipolyar i pozuntu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A70</span> — Bipolar type I disorder</div>'),
    ('bolme-04.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F31</span> — Bipolyar affektiv pozuntu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F31</span> — Bipolar affective disorder</div>'),
    ('bolme-04.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A71</span> — Bipolyar ii pozuntu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A71</span> — Bipolar type II disorder</div>'),
    ('bolme-04.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F31.8</span> — Digər bipolyar affektiv pozuntular</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F31.8</span> — Other bipolar affective disorders</div>'),
    ('bolme-04.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A72</span> — Siklotimik pozuntu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A72</span> — Cyclothymic disorder</div>'),
    ('bolme-04.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F34.0</span> — Siklotimiya</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F34.0</span> — Cyclothymia</div>'),
    ('bolme-04.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A62</span> — Distimik pozuntu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A62</span> — Dysthymic disorder</div>'),
    ('bolme-04.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F34.1</span> — Distimiya</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F34.1</span> — Dysthymia</div>'),
    ('bolme-04.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A73</span> — Qarişiq depressiv və təşviş pozuntusu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A73</span> — Mixed depressive and anxiety disorder</div>'),
    ('bolme-04.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F41.2</span> — Qarışıq təşviş və depressiv pozuntu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F41.2</span> — Mixed anxiety and depressive disorder</div>'),
    ('bolme-04.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A80</span> — Əhval pozuntularinin simptom təzahürləri</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6A80</span> — Symptom presentations of mood episodes</div>'),

    # ══════════════════════════════════════════════════════════════════════
    # bolme-05.html — Anxiety disorders
    # ══════════════════════════════════════════════════════════════════════
    ('bolme-05.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F40</span> (fobik), <span class="icd">F41</span> (digər təşviş) — Neyrotik, stress və somatoform pozuntular qrupunda</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F40</span> (phobic), <span class="icd">F41</span> (other anxiety) — Neurotic, stress-related and somatoform disorders</div>'),
    ('bolme-05.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B00</span> — Generalizə olunmuş təşviş pozuntusu (GTP)</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B00</span> — Generalised anxiety disorder</div>'),
    ('bolme-05.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F41.1</span> — Generalizə olunmuş təşviş pozuntusu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F41.1</span> — Generalised anxiety disorder</div>'),
    ('bolme-05.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B03</span> — Panik pozuntusu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B03</span> — Panic disorder</div>'),
    ('bolme-05.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F41.0</span> — Panik pozuntusu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F41.0</span> — Panic disorder</div>'),
    ('bolme-05.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B02</span> — Aqorafobiya</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B02</span> — Agoraphobia</div>'),
    ('bolme-05.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F40.0</span> — Aqorafobiya</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F40.0</span> — Agoraphobia</div>'),
    ('bolme-05.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B04</span> — Spesifik fobiya</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B04</span> — Specific phobia</div>'),
    ('bolme-05.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F40.2</span> — Spesifik (izolə edilmiş) fobiyalar</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F40.2</span> — Specific (isolated) phobias</div>'),
    ('bolme-05.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B01</span> — Sosial təşviş pozuntusu (sosial fobiya)</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B01</span> — Social anxiety disorder (social phobia)</div>'),
    ('bolme-05.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F40.1</span> — Sosial fobiyalar</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F40.1</span> — Social phobias</div>'),
    ('bolme-05.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B05</span> — Ayrilma təşvişi pozuntusu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B05</span> — Separation anxiety disorder</div>'),
    ('bolme-05.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F93.0</span> — Uşaqlıq dövrünün ayrılıq təşvişi pozuntusu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F93.0</span> — Separation anxiety disorder of childhood</div>'),
    ('bolme-05.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B06</span> — Selektiv mutizm</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B06</span> — Selective mutism</div>'),
    ('bolme-05.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F94.0</span> — Elektiv mutizm</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F94.0</span> — Elective mutism</div>'),

    # ══════════════════════════════════════════════════════════════════════
    # bolme-06.html — OCD and related
    # ══════════════════════════════════════════════════════════════════════
    ('bolme-06.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F42</span> (OKP); <span class="icd">F45.2</span> (hipoxondriya); <span class="icd">F63.3</span> (trixotillomaniya) — Ayrı-ayrı bölmələrdə</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F42</span> (OCD); <span class="icd">F45.2</span> (hypochondriasis); <span class="icd">F63.3</span> (trichotillomania) — In separate sections</div>'),
    ('bolme-06.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B20</span> — Obsessiv-kompulsiv pozuntu (OKP)</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B20</span> — Obsessive-compulsive disorder</div>'),
    ('bolme-06.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F42</span> — Obsessiv-kompulsiv pozuntu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F42</span> — Obsessive-compulsive disorder</div>'),
    ('bolme-06.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B21</span> — Bədən dismorfik pozuntusu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B21</span> — Body dysmorphic disorder</div>'),
    ('bolme-06.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F45.2</span> — Hipokondrik pozuntu (BDP)</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F45.2</span> — Hypochondriacal disorder (BDD)</div>'),
    ('bolme-06.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B22</span> — Olfaktiv referans pozuntusu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B22</span> — Olfactory reference disorder</div>'),
    ('bolme-06.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B23</span> — Hipoxondriya</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B23</span> — Hypochondriasis</div>'),
    ('bolme-06.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F45.2</span> — Hipokondrik pozuntu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F45.2</span> — Hypochondriacal disorder</div>'),
    ('bolme-06.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B24</span> — Yiğma pozuntusu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B24</span> — Hoarding disorder</div>'),
    ('bolme-06.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F63.9</span> — Vərdiş və impuls pozuntusu, dəqiqləşdirilməmiş</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F63.9</span> — Habit and impulse disorder, unspecified</div>'),
    ('bolme-06.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B25</span> — Bədənə yönəlik repetitiv davraniş pozuntulari</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B25</span> — Body-focused repetitive behaviour disorders</div>'),
    ('bolme-06.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F63.3</span> — Trikotillomaniya</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F63.3</span> — Trichotillomania</div>'),

    # ══════════════════════════════════════════════════════════════════════
    # bolme-07.html — Trauma and stress-related
    # ══════════════════════════════════════════════════════════════════════
    ('bolme-07.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F43</span> — Ağır stress reaksiyası və uyğunlaşma pozuntusu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F43</span> — Reaction to severe stress and adjustment disorders</div>'),
    ('bolme-07.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B40</span> — Posttravmatik stress pozuntusu (PTSP)</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B40</span> — Post-traumatic stress disorder</div>'),
    ('bolme-07.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F43.1</span> — Travma sonrası stress pozuntusu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F43.1</span> — Post-traumatic stress disorder</div>'),
    ('bolme-07.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B41</span> — Kompleks posttravmatik stress pozuntusu (KPTSP)</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B41</span> — Complex post-traumatic stress disorder</div>'),
    ('bolme-07.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F43.10</span> — Kompleks TSSP</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F43.10</span> — Complex PTSD</div>'),
    ('bolme-07.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B42</span> — Uzadilmiş kədər pozuntusu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B42</span> — Prolonged grief disorder</div>'),
    ('bolme-07.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F43.8</span> — Uzunmüddətli kədər</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F43.8</span> — Prolonged grief</div>'),
    ('bolme-07.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B43</span> — Uyğunlaşma pozuntusu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B43</span> — Adjustment disorder</div>'),
    ('bolme-07.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F43.20</span> — Uyğunlaşma pozuntuları</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F43.20</span> — Adjustment disorders</div>'),
    ('bolme-07.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B44</span> — Reaktiv bağliliğ və dezinhibisiyali sosial əlaqə pozuntusu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B44</span> — Reactive attachment disorder and disinhibited social engagement disorder</div>'),

    # ══════════════════════════════════════════════════════════════════════
    # bolme-08.html — Dissociative disorders
    # ══════════════════════════════════════════════════════════════════════
    ('bolme-08.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F44</span> — Dissosiativ [konversiya] pozuntular</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F44</span> — Dissociative [conversion] disorders</div>'),
    ('bolme-08.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B60</span> — Dissosiativ neyroloji simptom pozuntusu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B60</span> — Dissociative neurological symptom disorder</div>'),
    ('bolme-08.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F44</span> — Dissosiativ pozuntu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F44</span> — Dissociative disorder</div>'),
    ('bolme-08.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B61</span> — Dissosiativ amneziya</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B61</span> — Dissociative amnesia</div>'),
    ('bolme-08.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F44.0</span> — Dissosiativ amneziya</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F44.0</span> — Dissociative amnesia</div>'),
    ('bolme-08.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B62</span> — Fuga hali (dissosiativ fuqa)</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B62</span> — Dissociative fugue</div>'),
    ('bolme-08.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F44.3</span> — Trans və posessiya pozuntuları</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F44.3</span> — Trance and possession disorders</div>'),
    ('bolme-08.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B63</span> — Trans pozuntusu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B63</span> — Trance disorder</div>'),
    ('bolme-08.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B64</span> — Özü-özlərindən ayrilma pozuntusu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B64</span> — Depersonalisation-derealisation disorder</div>'),
    ('bolme-08.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F44.81</span> — Multipl şəxsiyyət pozuntusu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F44.81</span> — Multiple personality disorder</div>'),
    ('bolme-08.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B65</span> — Dissosiativ identiklik pozuntusu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B65</span> — Dissociative identity disorder</div>'),
    ('bolme-08.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B66</span> — Qismən dissosiativ identiklik pozuntusu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B66</span> — Partial dissociative identity disorder</div>'),
    ('bolme-08.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F48.1</span> — Depersonalizasiya-derealizasiya sindromu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F48.1</span> — Depersonalisation-derealisation syndrome</div>'),

    # ══════════════════════════════════════════════════════════════════════
    # bolme-09.html — Feeding and eating disorders
    # ══════════════════════════════════════════════════════════════════════
    ('bolme-09.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F50</span> — Yemə pozuntuları</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F50</span> — Eating disorders</div>'),
    ('bolme-09.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B80</span> — Nevrotik anoreksiya</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B80</span> — Anorexia nervosa</div>'),
    ('bolme-09.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F50.0</span> — Nevrotik anoreksiya</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F50.0</span> — Anorexia nervosa</div>'),
    ('bolme-09.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B81</span> — Nevrotik bulimiya</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B81</span> — Bulimia nervosa</div>'),
    ('bolme-09.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F50.2</span> — Nevrotik bulimiya</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F50.2</span> — Bulimia nervosa</div>'),
    ('bolme-09.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B82</span> — Dövri yeməklə yeyinmə pozuntusu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B82</span> — Binge eating disorder</div>'),
    ('bolme-09.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F50.8</span> — Digər yemə pozuntuları</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F50.8</span> — Other eating disorders</div>'),
    ('bolme-09.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B83</span> — Qaçinma/məhdudlaşdirma qida qəbulu pozuntusu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B83</span> — Avoidant-restrictive food intake disorder</div>'),
    ('bolme-09.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B84</span> — Pika</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B84</span> — Pica</div>'),
    ('bolme-09.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F98.3</span> — Uşaqlıqda qeyri-qida maddələrin yenilməsi</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F98.3</span> — Pica of infancy and childhood</div>'),
    ('bolme-09.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B85</span> — Ruminasiya-requrqitasiya pozuntusu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6B85</span> — Rumination-regurgitation disorder</div>'),
    ('bolme-09.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F98.2</span> — Erkən uşaqlıqda yemək tərpədilməsi</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F98.2</span> — Feeding disorder of infancy and early childhood</div>'),

    # ══════════════════════════════════════════════════════════════════════
    # bolme-10.html — Elimination disorders
    # ══════════════════════════════════════════════════════════════════════
    ('bolme-10.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6C00</span> — Enurez</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6C00</span> — Enuresis</div>'),
    ('bolme-10.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6C01</span> — Enkoprez</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6C01</span> — Encopresis</div>'),

    # ══════════════════════════════════════════════════════════════════════
    # bolme-11.html — Somatic / bodily distress
    # ══════════════════════════════════════════════════════════════════════
    ('bolme-11.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F45</span> — Somatoform pozuntular</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F45</span> — Somatoform disorders</div>'),
    ('bolme-11.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6C20</span> — Bədən disstres pozuntusu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6C20</span> — Bodily distress disorder</div>'),
    ('bolme-11.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F45.0</span> — Somatizasiya pozuntusu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F45.0</span> — Somatisation disorder</div>'),
    ('bolme-11.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6C21</span> — Bədən bütövlüyünü qavrama pozuntusu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6C21</span> — Body integrity dysphoria</div>'),
    ('bolme-11.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F45.1</span> — Fərqlənməyən somatoform pozuntu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F45.1</span> — Undifferentiated somatoform disorder</div>'),

    # ══════════════════════════════════════════════════════════════════════
    # bolme-12.html — Substance-related
    # ══════════════════════════════════════════════════════════════════════
    ('bolme-12.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6C40</span> — Alkohol istifadəsi və asililiq pozuntusu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6C40</span> — Disorders due to use of alcohol</div>'),
    ('bolme-12.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6C45</span> — Opioid istifadəsi və asililiq pozuntusu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6C45</span> — Disorders due to use of opioids</div>'),
    ('bolme-12.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6C43</span> — Kannabis istifadəsi və asililiq pozuntusu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6C43</span> — Disorders due to use of cannabis</div>'),
    ('bolme-12.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6C44</span> — Stimulyant istifadəsi</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6C44</span> — Disorders due to use of stimulants</div>'),
    ('bolme-12.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6C48</span> — Nikotin asililiği</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6C48</span> — Disorders due to use of nicotine</div>'),
    ('bolme-12.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6C90</span> — Qumar və video-oyun asililiq pozuntusu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6C90</span> — Gambling disorder or gaming disorder</div>'),

    # ══════════════════════════════════════════════════════════════════════
    # bolme-13.html — Impulse control
    # ══════════════════════════════════════════════════════════════════════
    ('bolme-13.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F63</span> — Vərdiş və impuls pozuntuları</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F63</span> — Habit and impulse disorders</div>'),
    ('bolme-13.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6C72</span> — Piromaniya</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6C72</span> — Pyromania</div>'),
    ('bolme-13.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F63.8</span> — Digər vərdiş və impuls pozuntuları</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F63.8</span> — Other habit and impulse disorders</div>'),
    ('bolme-13.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6C71</span> — Kleptomaniya</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6C71</span> — Kleptomania</div>'),
    ('bolme-13.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6C73</span> — Kompulsiv cinsi davraniş pozuntusu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6C73</span> — Compulsive sexual behaviour disorder</div>'),
    ('bolme-13.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F63.8</span> — İmpuls nəzarəti pozuntusu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F63.8</span> — Impulse control disorder</div>'),
    ('bolme-13.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6C70</span> — İntermittent eksplosiv pozuntu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6C70</span> — Intermittent explosive disorder</div>'),

    # ══════════════════════════════════════════════════════════════════════
    # bolme-14.html — Disruptive behaviour
    # ══════════════════════════════════════════════════════════════════════
    ('bolme-14.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F91</span> — Davranış pozuntuları</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F91</span> — Conduct disorders</div>'),
    ('bolme-14.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6C91</span> — Oppozisiya-etiraz pozuntusu (OEP)</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6C91</span> — Oppositional defiant disorder</div>'),
    ('bolme-14.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F91.3</span> — Opozisiya-etiraz pozuntusu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F91.3</span> — Oppositional defiant disorder</div>'),
    ('bolme-14.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6C90</span> — Davraniş-dissosial pozuntu (DDP)</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6C90</span> — Conduct-dissocial disorder</div>'),

    # ══════════════════════════════════════════════════════════════════════
    # bolme-15.html — Personality disorders
    # ══════════════════════════════════════════════════════════════════════
    ('bolme-15.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F60</span> – <span class="icd">F62</span> — Şəxsiyyət pozuntuları</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F60</span> – <span class="icd">F62</span> — Disorders of adult personality and behaviour</div>'),
    ('bolme-15.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> 10 spesifik tip — Paranoid, şizoid, şizotipal, antisosial, emosional qeyri-sabit (impulsiv/bpd), dissosiativ, anankast, narahatlıqdan qaçan, asılı, başqası. hər birinin konkret diaqnostik meyarları.</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> 10 specific types — Paranoid, schizoid, schizotypal, antisocial, emotionally unstable (impulsive/BPD), dissocial, anankastic, anxious-avoidant, dependent, other. Each with specific diagnostic criteria.</div>'),
    ('bolme-15.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6D10</span> — Şəxsiyyət pozuntusu — ümumi meyarlar</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6D10</span> — Personality disorder — general criteria</div>'),
    ('bolme-15.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F60</span> — Spesifik şəxsiyyət pozuntuları</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F60</span> — Specific personality disorders</div>'),
    ('bolme-15.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6D10</span> — Şəxsiyyət pozuntusunun şiddət dərəcəsi</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6D10</span> — Severity of personality disorder</div>'),
    ('bolme-15.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6D11</span> — Şəxsiyyət xüsusiyyət domenləri</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6D11</span> — Personality trait domains</div>'),
    ('bolme-15.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6D11</span> — Sərhəd nümunəsi (borderline pattern)</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6D11</span> — Borderline pattern qualifier</div>'),
    ('bolme-15.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F60.3</span> — Emosional qeyri-sabit şəxsiyyət pozuntusu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F60.3</span> — Emotionally unstable personality disorder</div>'),
    ('bolme-15.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6D10</span> — Antisosial/dissosial nümunəsi</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6D10</span> — Antisocial/dissocial pattern</div>'),

    # ══════════════════════════════════════════════════════════════════════
    # bolme-16.html — Paraphilic disorders
    # ══════════════════════════════════════════════════════════════════════
    ('bolme-16.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F65</span> — Cinsi üstünlük pozuntuları</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F65</span> — Disorders of sexual preference</div>'),
    ('bolme-16.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6D36</span> — Pedofilik pozuntu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6D36</span> — Paedophilic disorder</div>'),
    ('bolme-16.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F65.9</span> — Cinsi seçim pozuntusu, dəqiqləşdirilməmiş</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F65.9</span> — Disorder of sexual preference, unspecified</div>'),

    # ══════════════════════════════════════════════════════════════════════
    # bolme-17.html — Factitious disorders
    # ══════════════════════════════════════════════════════════════════════
    ('bolme-17.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6D50</span> — Özünə uyğulanmiş süni pozuntu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6D50</span> — Factitious disorder imposed on self</div>'),
    ('bolme-17.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6D51</span> — Başqasina uyğulanmiş süni pozuntu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6D51</span> — Factitious disorder imposed on another</div>'),
    ('bolme-17.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F68</span>.A — Başqasına süni xəstəlik yaratma</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F68</span>.A — Fabricated or induced illness</div>'),

    # ══════════════════════════════════════════════════════════════════════
    # bolme-18.html — Sleep-wake disorders
    # ══════════════════════════════════════════════════════════════════════
    ('bolme-18.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">7A00</span> – <span class="icd">7B2Z</span> — Sleep-wake disorders (ayrı fəsil)</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">7A00</span> – <span class="icd">7B2Z</span> — Sleep-wake disorders (separate chapter)</div>'),
    ('bolme-18.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F51</span> (qeyri-üzvi yuxu pozuntuları, F bölməsi); G47 (üzvi yuxu pozuntuları)</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F51</span> (non-organic sleep disorders, F section); G47 (organic sleep disorders)</div>'),
    ('bolme-18.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">7A60</span> — Yuxu-bağli tənəffüs pozuntulari</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">7A60</span> — Sleep-related breathing disorders</div>'),
    ('bolme-18.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">7A80</span> — Hərəkət-bağli yuxu pozuntulari</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">7A80</span> — Sleep-related movement disorders</div>'),

    # ══════════════════════════════════════════════════════════════════════
    # bolme-19.html — Sexual health / gender dysphoria
    # ══════════════════════════════════════════════════════════════════════
    ('bolme-19.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">HA00</span> – <span class="icd">HA8Z</span> — Conditions related to sexual health (ayrı fəsil — fəsil 17)</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">HA00</span> – <span class="icd">HA8Z</span> — Conditions related to sexual health (separate chapter — chapter 17)</div>'),
    ('bolme-19.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F52</span> (cinsi disfunksiyalar — psixiatriya bölməsində); <span class="icd">F64</span> (cinsiyyət identifikasiyası pozuntuları)</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F52</span> (sexual dysfunctions — psychiatry section); <span class="icd">F64</span> (gender identity disorders)</div>'),

    # ══════════════════════════════════════════════════════════════════════
    # bolme-20.html — Neurocognitive disorders
    # ══════════════════════════════════════════════════════════════════════
    ('bolme-20.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F00</span> – <span class="icd">F03</span> (demensiya), <span class="icd">F04</span> – <span class="icd">F09</span> (organik)</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F00</span> – <span class="icd">F03</span> (dementia), <span class="icd">F04</span> – <span class="icd">F09</span> (organic)</div>'),
    ('bolme-20.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F00</span> — Alzheimer xəstəliyində demensiya</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F00</span> — Dementia in Alzheimer\'s disease</div>'),
    ('bolme-20.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6D71</span> — Yüngül neyrokoqnitiv pozuntu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6D71</span> — Mild neurocognitive disorder</div>'),
    ('bolme-20.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6D70</span> — Demensiya — ümumi prinsiplər</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6D70</span> — Dementia — general principles</div>'),
    ('bolme-20.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F06.7</span> — Yüngül koqnitiv pozuntu</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F06.7</span> — Mild cognitive disorder</div>'),
    ('bolme-20.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6D70</span> — Alzheimer xəstəliyindən demensiya</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6D70</span> — Dementia due to Alzheimer\'s disease</div>'),

    # ══════════════════════════════════════════════════════════════════════
    # bolme-21.html — Peripartum disorders
    # ══════════════════════════════════════════════════════════════════════
    ('bolme-21.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F53</span> — Puerperium ilə əlaqəli psixi pozuntular (<span class="icd">F53.0</span> – <span class="icd">F53.1</span>)</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F53</span> — Mental and behavioural disorders associated with the puerperium (<span class="icd">F53.0</span> – <span class="icd">F53.1</span>)</div>'),
    ('bolme-21.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6E20</span> — Doğuşdan sonraki depressiya (PPD)</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6E20</span> — Postpartum depression (PPD)</div>'),
    ('bolme-21.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F53.0</span> — Yüngül puerperiya psixi pozuntuları</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F53.0</span> — Mild mental and behavioural disorders associated with the puerperium</div>'),
    ('bolme-21.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6E21</span> — Doğuşdan sonraki psixoz (PPP)</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">6E21</span> — Postpartum psychosis (PPP)</div>'),
    ('bolme-21.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F53.1</span> — Ağır puerperiya psixotik pozuntular</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-11:</span> <span class="icd">F53.1</span> — Severe mental and behavioural disorders associated with the puerperium</div>'),

    # ══════════════════════════════════════════════════════════════════════
    # bolme-22.html — Secondary mental disorders
    # ══════════════════════════════════════════════════════════════════════
    ('bolme-22.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F06</span> – <span class="icd">F09</span> — Üzvi, o cümlədən simptomatik psixi pozuntular</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F06</span> – <span class="icd">F09</span> — Organic, including symptomatic, mental disorders</div>'),

    # ══════════════════════════════════════════════════════════════════════
    # bolme-03.html — Catatonia
    # ══════════════════════════════════════════════════════════════════════
    ('bolme-03.html',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F06.1</span> (üzvi katatonik pozuntu); <span class="icd">F20.2</span> (katatonik şizofreniya – ləğv); <span class="icd">F30</span> – <span class="icd">F33</span> (affektiv pozuntularda katatonik xüsusiyyətlər)</div>',
     '<div class="xbt-line"><span class="xbt-lbl">XBT-10:</span> <span class="icd">F06.1</span> (organic catatonic disorder); <span class="icd">F20.2</span> (catatonic schizophrenia — abolished); <span class="icd">F30</span> – <span class="icd">F33</span> (catatonic features in affective disorders)</div>'),
]

# ── Run all fixes ─────────────────────────────────────────────────────────────
total_files = 0
total_fixes = 0
file_counts = {}

for fname, old, new in FIXES:
    fpath = os.path.join(BASE, fname)
    if fname not in file_counts:
        # First time seeing this file — read it
        with open(fpath, encoding='utf-8') as f:
            html = f.read()
        file_counts[fname] = {'html': unicodedata.normalize('NFC', html), 'fixes': 0}

    html = file_counts[fname]['html']
    if old in html:
        file_counts[fname]['html'] = html.replace(old, new)  # replace first occurrence
        file_counts[fname]['fixes'] += 1
        print(f'  ✓ {fname}: ...{old[50:100]}...')
    else:
        print(f'  ✗ NOT FOUND {fname}: {old[30:100]}')

# Write all changed files
for fname, data in file_counts.items():
    if data['fixes'] > 0:
        fpath = os.path.join(BASE, fname)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(data['html'])
        print(f'\n  >> {fname}: {data["fixes"]} fix(es) written')
        total_files += 1
        total_fixes += data['fixes']

print(f'\nDone. {total_files} files, {total_fixes} total fixes.')
