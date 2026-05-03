#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Терминологические правки:
  1. İkincili → İkinci dərəcəli (все файлы, все контексты)
  2. Anksiyete → Təşviş (все Азербайджанские контексты)
  3. Оставшиеся birincili в body-тексте → ilkin
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
    for old, new in changes:
        if old in html:
            n = html.count(old)
            html = html.replace(old, new)
            ok.append((old[:70], n))
    if html != orig:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html)
    return ok

# ── 1. İkincili → İkinci dərəcəli  (ALL files) ──────────────────────────────
# Порядок: более специфичные формы первыми
IKINCILI_ALL = [
    # UPPERCASE headings
    ('İKİNCİLİ PSİXOTİK POZUNTULAR',          'İKİNCİ DƏRƏCƏLİ PSİXOTİK POZUNTULAR'),
    ('İKİNCİLİ',                               'İKİNCİ DƏRƏCƏLİ'),
    # H3 headings (Title Case) — h3 id anchors also updated below
    ('İkincili Psixoz',                        'İkinci Dərəcəli Psixoz'),
    ('İkincili Depressiya',                    'İkinci Dərəcəli Depressiya'),
    ('İkincili Manik/Hipomanik Sindrom',       'İkinci Dərəcəli Manik/Hipomanik Sindrom'),
    ('İkincili Anksiyete Sindromu',            'İkinci Dərəcəli Anksiyete Sindromu'),
    ('İkincili Şəxsiyyət Dəyişikliyi',        'İkinci Dərəcəli Şəxsiyyət Dəyişikliyi'),
    # Body text — sentence case
    ('İkincili psixi sindromlar',              'İkinci dərəcəli psixi sindromlar'),
    ('İkincili psixoz',                        'İkinci dərəcəli psixoz'),
    ('İkincili psixiatrik simptomlar',         'İkinci dərəcəli psixiatrik simptomlar'),
    ('İkincili psixiatrik sindrom',            'İkinci dərəcəli psixiatrik sindrom'),
    # Generic — covers remaining uppercase-start instances
    ('İkincili',                               'İkinci dərəcəli'),
    # Lowercase — all remaining forms
    ('ikincili katatoniya',                    'ikinci dərəcəli katatoniya'),
    ('ikincili psixi sindromlar',              'ikinci dərəcəli psixi sindromlar'),
    ('ikincili enurez',                        'ikinci dərəcəli enurez'),
    ('ikincili tibbi müayinə',                 'ikinci dərəcəli tibbi müayinə'),
    ('ikincili formalardır',                   'ikinci dərəcəli formalardır'),
    ('ikincilidir',                            'ikinci dərəcəlidir'),
    ('ikincili',                               'ikinci dərəcəli'),
    # Anchor IDs — bolme-22 h3 sections
    ('id="ikincili-psixoz-6e61"',
     'id="ikinci-dərəcəli-psixoz-6e61"'),
    ('id="ikincili-depressiya-6e62"',
     'id="ikinci-dərəcəli-depressiya-6e62"'),
    ('id="ikincili-manikhipomanik-sindrom-6e63"',
     'id="ikinci-dərəcəli-manikhipomanik-sindrom-6e63"'),
    ('id="ikincili-anksiyete-sindromu-6e64"',
     'id="ikinci-dərəcəli-anksiyete-sindromu-6e64"'),
    ('id="ikincili-şəxsiyyət-dəyişikliyi-6e65"',
     'id="ikinci-dərəcəli-şəxsiyyət-dəyişikliyi-6e65"'),
    ('id="ikincili-psixi-və-davraniş-sindromlari"',
     'id="ikinci-dərəcəli-psixi-və-davraniş-sindromlari"'),
]

# ── 2. Anksiyete → Təşviş  (ALL files, Azerbaijani context only) ─────────────
# Note: "anxiety" (English) is not affected; "anksiyete" is purely Azerbaijani
ANKSIYETE_ALL = [
    # Inflected forms first (to avoid double-match)
    ('anksiyetesi',                            'təşvişi'),
    ('Anksiyetesi',                            'Təşvişi'),
    # Compounds
    ('Anksiyete Sindromu',                     'Təşviş Sindromu'),
    ('anksiyete sindromu',                     'təşviş sindromu'),
    ('Anksiyete sindromu',                     'Təşviş sindromu'),
    ('Anksiyete pozuntuları',                  'Təşviş pozuntuları'),
    ('anksiyete pozuntuları',                  'təşviş pozuntuları'),
    ('Anksiyete pozuntusu',                    'Təşviş pozuntusu'),
    ('anksiyete pozuntusu',                    'təşviş pozuntusu'),
    # Standalone (covers remaining occurrences)
    ('Anksiyete',                              'Təşviş'),
    ('anksiyete',                              'təşviş'),
    # H2 anchor in bolme-21
    ('id="doğuşdan-sonrakı-anksiyete"',
     'id="doğuşdan-sonrakı-təşviş"'),
    # bolme-22 updated anchor (after İkincili→İkinci dərəcəli)
    ('id="ikinci-dərəcəli-anksiyete-sindromu-6e64"',
     'id="ikinci-dərəcəli-təşviş-sindromu-6e64"'),
]

# ── 3. Remaining birincili body text  (targeted per file) ────────────────────
BIRINCILI_BODY = {
    'bolme-02.html': [
        # line 1323: "Hər bir birincili psixotik pozuntu"
        ('Hər bir birincili psixotik pozuntu',
         'Hər bir ilkin psixotik pozuntu'),
    ],
    'bolme-10.html': [
        # line 374: primary/secondary enuresis types
        ('<strong>Birincili:</strong>',   '<strong>İlkin:</strong>'),
        ('<strong>İkincili:</strong>',    '<strong>İkinci dərəcəli:</strong>'),
        # line 377
        ('İkincili enurez:',              'İkinci dərəcəli enurez:'),
    ],
    'bolme-18.html': [
        # line 382: "sadəcə "ikincili" deyil"
        ('"ikincili"',                   '"ikinci dərəcəli"'),
        # line 386: "Birincili" və "ikincili"
        ('"Birincili" və "ikincili"',    '"İlkin" və "ikinci dərəcəli"'),
    ],
    'bolme-19.html': [
        # line 447: primary erectile dysfunction
        ('<strong>Birincili</strong>',    '<strong>İlkin</strong>'),
        # line 448: secondary (will be caught by global İkincili rule)
    ],
}


# ── Run ───────────────────────────────────────────────────────────────────────

all_html = sorted(globmod.glob(os.path.join(BASE, '*.html')))
grand_total = 0

for fpath in all_html:
    fname = os.path.basename(fpath)
    changes = list(IKINCILI_ALL) + list(ANKSIYETE_ALL)
    if fname in BIRINCILI_BODY:
        changes += BIRINCILI_BODY[fname]

    ok = apply_changes(fpath, changes)
    if ok:
        for s, n in ok:
            grand_total += n
            print(f'  [{n}] {fname}: {s}')

print(f'\nИтог: {grand_total} замен.')
