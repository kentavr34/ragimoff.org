#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GEO (Generative Engine Optimization) — add structured data for AI search engines.
Adds: WebSite, Organization, Service, Course, Book, FAQPage, BreadcrumbList,
      MedicalCondition, Article/BlogPosting, HowTo, Review, Person, EducationalOrganization.
"""
import sys, io, os, glob, re, json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = os.path.dirname(os.path.abspath(__file__))

def nfc(s): return __import__('unicodedata').normalize('NFC', s)
def read_html(fpath):
    with open(fpath, encoding='utf-8') as f:
        return nfc(f.read())
def write_html(fpath, html):
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)

def has_schema(html, schema_type):
    return f'"@type":"{schema_type}"' in html.replace(' ', '')

def insert_before_head_end(html, new_tags):
    """Insert tags before </head>"""
    return html.replace('</head>', new_tags + '\n  </head>', 1)

def get_lang_from_path(fpath):
    """Determine language from file path"""
    rel = os.path.relpath(fpath, ROOT)
    if rel.startswith('en' + os.sep):
        return 'en'
    elif rel.startswith('ru' + os.sep):
        return 'ru'
    return 'az'

def get_base_url(lang):
    """Get base URL for language"""
    if lang == 'en':
        return 'https://ragimoff.org/en/'
    elif lang == 'ru':
        return 'https://ragimoff.org/ru/'
    return 'https://ragimoff.org/'

# ═══════════════════════════════════════════════════════════════════
# OG META NORMALIZATION (idempotent, additive-only)
# ═══════════════════════════════════════════════════════════════════

OG_LOCALES = {'az': 'az_AZ', 'ru': 'ru_RU', 'en': 'en_US'}
OG_IMAGE = 'https://ragimoff.org/images/kenan/photo-portal-crop-removebg-preview.png'

def normalize_og(html, lang, slug, rel_dir):
    """Add missing og:locale / og:image. Never touches the root design etalon."""
    tags = []
    if 'og:locale' not in html:
        locale = OG_LOCALES.get(lang)
        if locale:
            tags.append(f'<meta property="og:locale" content="{locale}" />')
    if 'og:image' not in html and not (lang == 'az' and slug == 'index' and rel_dir == '.'):
        tags.append(f'<meta property="og:image" content="{OG_IMAGE}" />')
    if not tags:
        return html
    return insert_before_head_end(html, '\n'.join(tags))

# ═══════════════════════════════════════════════════════════════════
# SCHEMAS — Language-specific variants
# ═══════════════════════════════════════════════════════════════════

def build_website_schema(lang):
    names = {'az': 'RAGIMOFF Psixologiya Məktəbi', 'ru': 'RAGIMOFF Школа Психологии', 'en': 'RAGIMOFF Psychology School'}
    descs = {
        'az': 'Psixoterapevt, psixoloq, psixiatr — Kənan Rəhimov. 23 il təcrübə. Təhsil, konsultasiya, kitab.',
        'ru': 'Психотерапевт, психолог, психиатр — Кенан Рагимов. 23 года опыта. Обучение, консультации, книга.',
        'en': 'Psychotherapist, psychologist, psychiatrist — Kenan Ragimov. 23 years experience. Education, consultations, textbook.'
    }
    return f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "{names[lang]}",
  "alternateName": "RAGIMOFF Psychology School",
  "url": "{get_base_url(lang)}",
  "description": "{descs[lang]}",
  "inLanguage": "{lang}",
  "publisher": {{
    "@type": "Organization",
    "name": "{names[lang]}",
    "url": "{get_base_url(lang)}",
    "logo": "https://ragimoff.org/favicon.ico"
  }},
  "potentialAction": {{
    "@type": "SearchAction",
    "target": {{
      "@type": "EntryPoint",
      "urlTemplate": "{get_base_url(lang)}?q={{search_term_string}}"
    }},
    "query-input": "required name=search_term_string"
  }}
}}
</script>'''

def build_org_schema(lang):
    names = {'az': 'RAGIMOFF Psixologiya Məktəbi', 'ru': 'RAGIMOFF Школа Психологии', 'en': 'RAGIMOFF Psychology School'}
    descs = {
        'az': 'Psixologiya təhsili, klinik psixoterapiya və psixiatriya kitabı. 23 illik klinik təcrübə.',
        'ru': 'Образование в психологии, клиническая психотерапия и книга по психиатрии. 23 года клинического опыта.',
        'en': 'Psychology education, clinical psychotherapy, and psychiatry textbook. 23 years clinical experience.'
    }
    return f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "{names[lang]}",
  "alternateName": "RAGIMOFF Psychology School",
  "url": "{get_base_url(lang)}",
  "logo": "https://ragimoff.org/favicon.ico",
  "description": "{descs[lang]}",
  "foundingDate": "2003",
  "founder": {{
    "@type": "Person",
    "name": "Kənan Rəhimov"
  }},
  "address": {{
    "@type": "PostalAddress",
    "streetAddress": "Cəfər Cabbarlı küçəsi 40",
    "addressLocality": "Bakı",
    "addressCountry": "AZ"
  }},
  "contactPoint": [
    {{
      "@type": "ContactPoint",
      "telephone": "+994-70-220-03-76",
      "contactType": "customer service",
      "availableLanguage": ["Azerbaijani", "Russian", "English"]
    }},
    {{
      "@type": "ContactPoint",
      "telephone": "+994-77-539-50-09",
      "contactType": "sales",
      "availableLanguage": ["Azerbaijani", "Russian"]
    }}
  ],
  "sameAs": [
    "https://t.me/ragimoff",
    "https://instagram.com/dr.ragimoff",
    "https://www.facebook.com/Ragimoff.az",
    "https://www.youtube.com/@kragimoff",
    "https://www.linkedin.com/in/kenan-ragimov"
  ],
  "knowsAbout": [
    "Psixiatriya", "Psixoterapiya", "KDT", "EMDR", "Depressiya", "OKP", "PTSD",
    "Ailə terapiyası", "Psixologiya təhsili"
  ]
}}
</script>'''

# Service schema for therapy pages (multilingual)
SERVICE_SCHEMAS = {
    'depressiya': {
        'az': {'name': 'Depressiya Müalicəsi', 'desc': 'Klinik depressiyanın diaqnostikası və müalicəsi. KDT, antidepressant seçimi, qısa və uzunmüddətli protokollar.', 'cat': 'Psixoterapiya'},
        'ru': {'name': 'Лечение депрессии', 'desc': 'Диагностика и лечение клинической депрессии. КПТ, подбор антидепрессантов, краткие и долгосрочные протоколы.', 'cat': 'Психотерапия'},
        'en': {'name': 'Depression Treatment', 'desc': 'Diagnosis and treatment of clinical depression. CBT, antidepressant selection, short and long-term protocols.', 'cat': 'Psychotherapy'},
    },
    'panik-ataklar': {
        'az': {'name': 'Panik Atakların Müalicəsi', 'desc': 'Panik pozuntu və agorafobiya müalicəsi. Nəfas texnikaları, kognitiv restrukturlaşdırma, expositions terapiyası.', 'cat': 'Psixoterapiya'},
        'ru': {'name': 'Лечение панических атак', 'desc': 'Лечение панического расстройства и агорафобии. Дыхательные техники, когнитивная реструктуризация, экспозиционная терапия.', 'cat': 'Психотерапия'},
        'en': {'name': 'Panic Attacks Treatment', 'desc': 'Treatment of panic disorder and agoraphobia. Breathing techniques, cognitive restructuring, exposure therapy.', 'cat': 'Psychotherapy'},
    },
    'sosial-fobiya': {
        'az': {'name': 'Sosial Fobiya Müalicəsi', 'desc': 'Sosial həyəcan pozuntusunun müalicəsi. KDT, expositions, sosial bacarıqların təlimi.', 'cat': 'Psixoterapiya'},
        'ru': {'name': 'Лечение социальной фобии', 'desc': 'Лечение социального тревожного расстройства. КПТ, экспозиция, обучение социальным навыкам.', 'cat': 'Психотерапия'},
        'en': {'name': 'Social Phobia Treatment', 'desc': 'Treatment of social anxiety disorder. CBT, exposure, social skills training.', 'cat': 'Psychotherapy'},
    },
    'enurez': {
        'az': {'name': 'Gecə Enurezi Müalicəsi', 'desc': 'Uşaqlarda birincili monosimptomatik gecə enurezinin müalicəsi. Alarm terapiyası, desmopressin, valideyn məsləhəti.', 'cat': 'Uşaq Psixiatriyası'},
        'ru': {'name': 'Лечение ночной энуреза', 'desc': 'Лечение первичного моносимптоматического ночного энуреза у детей. Аларм-терапия, десмопрессин, консультация родителей.', 'cat': 'Детская психиатрия'},
        'en': {'name': 'Nocturnal Enuresis Treatment', 'desc': 'Treatment of primary monosymptomatic nocturnal enuresis in children. Alarm therapy, desmopressin, parent counseling.', 'cat': 'Child Psychiatry'},
    },
    'aile-terapiyasi': {
        'az': {'name': 'Ailə Terapiyası', 'desc': 'Cütlük və ailə münaqişələrinin həlli. Gottman metodu, EFT, kommunikasiya bacarıqları.', 'cat': 'Ailə Psixoterapiyası'},
        'ru': {'name': 'Семейная терапия', 'desc': 'Решение парных и семейных конфликтов. Метод Готтмана, EFT, навыки коммуникации.', 'cat': 'Семейная психотерапия'},
        'en': {'name': 'Family Therapy', 'desc': 'Resolving couples and family conflicts. Gottman method, EFT, communication skills.', 'cat': 'Family Psychotherapy'},
    },
    'aile-terapiyasi-usaq': {
        'az': {'name': 'Ailə-Uşaq Terapiyası', 'desc': 'Valideyn-uşaq münasibətləri, davranış problemləri, emosional çətinliklər.', 'cat': 'Uşaq Psixologiyası'},
        'ru': {'name': 'Семейно-детская терапия', 'desc': 'Родительско-детские отношения, поведенческие проблемы, эмоциональные трудности.', 'cat': 'Детская психология'},
        'en': {'name': 'Child-Parent Therapy', 'desc': 'Parent-child relationships, behavioral problems, emotional difficulties.', 'cat': 'Child Psychology'},
    },
    'xidmetler': {
        'az': {'name': 'Psixoterapiya Xidmətləri', 'desc': 'Fərdi konsultasiya, ailə terapiyası, deprеssiya, panik ataklar, sosial fobiya, enurez müalicəsi.', 'cat': 'Psixoterapiya'},
        'ru': {'name': 'Услуги психотерапии', 'desc': 'Индивидуальные консультации, семейная терапия, депрессия, панические атаки, социальная фобия, энурез.', 'cat': 'Психотерапия'},
        'en': {'name': 'Psychotherapy Services', 'desc': 'Individual counseling, family therapy, depression, panic attacks, social phobia, enuresis treatment.', 'cat': 'Psychotherapy'},
    }
}

# Course schema for education pages (multilingual)
COURSE_SCHEMAS = {
    'program-umumi': {
        'az': {'name': 'Ümumi Psixologiya DPO', 'desc': 'Rəsmi DPO diplom proqramı. 1556 akademik saat, 22 fənn, 5 blok. FRDO qeydiyyatında.', 'level': 'Professional Development', 'cred': 'Diplom'},
        'ru': {'name': 'Общая Психология ДПО', 'desc': 'Официальная программа ДПО с дипломом. 1556 ак. часов, 22 дисциплины, 5 блоков. Реестр ФРДО.', 'level': 'Professional Development', 'cred': 'Диплом'},
        'en': {'name': 'General Psychology DPO', 'desc': 'Official DPO diploma program. 1556 academic hours, 22 disciplines, 5 blocks. FRDO registered.', 'level': 'Professional Development', 'cred': 'Diploma'},
    },
    'program-klinik': {
        'az': {'name': 'Klinik Psixologiya DPO', 'desc': 'Klinik psixologiya DPO proqramı. 2392 saat, DSM-5/ICD-11, KDT, PTSD. 6600 AZN.', 'level': 'Advanced Professional Development', 'cred': 'Diplom'},
        'ru': {'name': 'Клиническая Психология ДПО', 'desc': 'Программа ДПО по клинической психологии. 2392 часа, DSM-5/ICD-11, КПТ, ПТСР. 6600 AZN.', 'level': 'Advanced Professional Development', 'cred': 'Диплом'},
        'en': {'name': 'Clinical Psychology DPO', 'desc': 'Clinical Psychology DPO program. 2392 hours, DSM-5/ICD-11, CBT, PTSD. 6600 AZN.', 'level': 'Advanced Professional Development', 'cred': 'Diploma'},
    },
    'program-praktikum': {
        'az': {'name': 'Psixoterapiya Praktikumu', 'desc': 'Psixoterapiya praktikumu. 864 saat (36 canlı + 36 video × 12 ay), IPAS/BPA sertifikatı, superviziya.', 'level': 'Practicum', 'cred': 'Certificate'},
        'ru': {'name': 'Практикум Психотерапии', 'desc': 'Практикум по психотерапии. 864 часа (36 живых + 36 видео × 12 мес), сертификат IPAS/BPA, супервизия.', 'level': 'Practicum', 'cred': 'Certificate'},
        'en': {'name': 'Psychotherapy Practicum', 'desc': 'Psychotherapy practicum. 864 hours (36 live + 36 video × 12 months), IPAS/BPA certificate, supervision.', 'level': 'Practicum', 'cred': 'Certificate'},
    },
    'tehsil': {
        'az': {'name': 'Psixologiya Təhsil Proqramları', 'desc': 'Ümumi Psixologiya, Klinik Psixologiya DPO, Psixoterapiya Praktikumu, Ailə Terapiyası. Rəsmi diplom + beynəlxalq sertifikat.', 'level': 'Professional Development', 'cred': 'Diplom'},
        'ru': {'name': 'Программы Обучения Психологии', 'desc': 'Общая Психология, Клиническая Психология ДПО, Практикум Психотерапии, Семейная Терапия. Официальный диплом + международный сертификат.', 'level': 'Professional Development', 'cred': 'Диплом'},
        'en': {'name': 'Psychology Education Programs', 'desc': 'General Psychology, Clinical Psychology DPO, Psychotherapy Practicum, Family Therapy. Official diploma + international certificate.', 'level': 'Professional Development', 'cred': 'Diploma'},
    }
}

# Book schema (multilingual)
def build_book_schema(lang):
    names = {'az': 'Klinik Psixiatriya', 'ru': 'Клиническая Психиатрия', 'en': 'Clinical Psychiatry'}
    alts = {'az': 'Clinical Psychiatry Textbook', 'ru': 'Учебник по клинической психиатрии', 'en': 'Clinical Psychiatry Textbook'}
    descs = {
        'az': 'Psixiatrik pozuntuların diaqnostikası və müalicəsi üzrə klinik bələdçi. ICD-11 (XBT-11), DSM-5-TR əsaslı. 22 bölmə, 100-dən çox diaqnoz. 4 dil: AZ, RU, EN, TR.',
        'ru': 'Клиническое руководство по диагностике и лечению психиатрических расстройств. ICD-11 (МКБ-11), DSM-5-TR. 22 раздела, 100+ диагнозов. 4 языка: АЗ, RU, EN, TR.',
        'en': 'Clinical guide to diagnosis and treatment of psychiatric disorders. ICD-11, DSM-5-TR based. 22 chapters, 100+ diagnoses. 4 languages: AZ, RU, EN, TR.'
    }
    return f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Book",
  "name": "{names[lang]}",
  "alternateName": "{alts[lang]}",
  "author": {{
    "@type": "Person",
    "name": "Kənan Rəhimov",
    "url": "https://ragimoff.org/haqqimda.html"
  }},
  "inLanguage": "{lang}",
  "description": "{descs[lang]}",
  "about": [
    "Psixiatriya", "Diaqnostika", "Müalicə", "ICD-11", "DSM-5-TR",
    "Şizofreniya", "Depressiya", "Təşviş", "OKP", "PTSD",
    "Ailə terapiyası", "Uşaq psixiatriyası"
  ],
  "keywords": "psixiatriya, psixiatr, diaqnoz, ICD-11, DSM-5, klinik protokol, XBT-11",
  "url": "https://ragimoff.org/klinik-psixiatriya/",
  "publisher": {{
    "@type": "Organization",
    "name": "RAGIMOFF Psixologiya Məktəbi",
    "url": "https://ragimoff.org/"
  }},
  "datePublished": "2026",
  "bookFormat": "https://schema.org/EBook",
  "isAccessibleForFree": true,
  "workExample": {{
    "@type": "Book",
    "inLanguage": "{lang}",
    "url": "https://ragimoff.org/klinik-psixiatriya/"
  }},
  "translationOfWork": {{
    "@type": "Book",
    "inLanguage": "ru",
    "url": "https://ragimoff.org/klinik-psixiatriya/ru/"
  }},
  "offers": {{
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "AZN",
    "availability": "https://schema.org/InStock",
    "url": "https://ragimoff.org/klinik-psixiatriya/"
  }}
}}
</script>'''

def build_service_schema(slug, lang):
    """Build Service schema for therapy page"""
    s = SERVICE_SCHEMAS.get(slug, {}).get(lang)
    if not s: return ''
    base = get_base_url(lang)
    return f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "{s['name']}",
  "description": "{s['desc']}",
  "serviceType": "{s['cat']}",
  "provider": {{
    "@type": "Organization",
    "name": "RAGIMOFF Psixologiya Məktəbi",
    "url": "https://ragimoff.org/"
  }},
  "areaServed": "AZ",
  "availableChannel": {{
    "@type": "ServiceChannel",
    "serviceUrl": "{base}{slug}.html",
    "servicePhone": "+994-70-220-03-76",
    "servicePostalAddress": {{
      "@type": "PostalAddress",
      "streetAddress": "Cəfər Cabbarlı küçəsi 40",
      "addressLocality": "Bakı",
      "addressCountry": "AZ"
    }}
  }}
}}
</script>'''

def build_course_schema(slug, lang):
    """Build Course schema for education page"""
    c = COURSE_SCHEMAS.get(slug, {}).get(lang)
    if not c: return ''
    return f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Course",
  "name": "{c['name']}",
  "description": "{c['desc']}",
  "provider": {{
    "@type": "Organization",
    "name": "RAGIMOFF Psixologiya Məktəbi",
    "url": "https://ragimoff.org/"
  }},
  "educationalLevel": "{c['level']}",
  "credentialCategory": "{c['cred']}",
  "hasCourseInstance": {{
    "@type": "CourseInstance",
    "courseMode": "online, in-person",
    "duration": "P1Y",
    "inLanguage": "{lang}"
  }}
}}
</script>'''

def build_breadcrumb_schema(url_path, title, lang):
    """Build BreadcrumbList schema"""
    parts = [p for p in url_path.strip('/').split('/') if p]
    home_names = {'az': 'Ana Səhifə', 'ru': 'Главная', 'en': 'Home'}
    items = [
        {"@type": "ListItem", "position": 1, "name": home_names[lang], "item": get_base_url(lang)}
    ]
    pos = 2
    accum = ''
    for p in parts:
        accum += '/' + p
        name = title if p == parts[-1] else p.replace('-', ' ').title()
        items.append({"@type": "ListItem", "position": pos, "name": name, "item": f"https://ragimoff.org{accum}"})
        pos += 1
    return f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": {json.dumps(items, ensure_ascii=False)}
}}
</script>'''

# FAQ schemas for service pages (multilingual)
FAQ_SCHEMAS = {
    'depressiya': {
        'az': [
            ("Depressiya necə diaqnostik olunur?", "DSM-5-TR və ICD-11 (XBT-11) meyarları ilə: 2 həftə davam edən kədər, maraqlılıqsızlıq, enerji azlığı + əlavə simptomlar."),
            ("Antidepressantlar asılılıq yaradır mı?", "Xeyr, SSRİ/SNRI qrupu asılılıq yaramır. Lakin dayandırma sindromu ola bilər, buna görə lenta azaldma tələb olunur."),
            ("Depressiyada psixoterapiya effektivdir mi?", "Bəli, KDT (CBT) — birinci xətt müalicəsidir. Orta ağırlıqda depressiyada dərmanla eyni effekt verir, recidiv riskini azaldır."),
        ],
        'ru': [
            ("Как диагностируется депрессия?", "По критериям DSM-5-TR и ICD-11: подавленное настроение, анедония, снижение энергии в течение 2 недель + дополнительные симптомы."),
            ("Вызывают ли антидепрессанты зависимость?", "Нет, СИОЗС/СИОЗСН не вызывают зависимости. Возможен синдром отмены, поэтому дозировку снижают постепенно."),
            ("Эффективна ли психотерапия при депрессии?", "Да, КПТ (CBT) — первая линия лечения. При депрессии средней тяжести дает тот же эффект, что и лекарства, снижает риск рецидивов."),
        ],
        'en': [
            ("How is depression diagnosed?", "Per DSM-5-TR and ICD-11 criteria: 2 weeks of depressed mood, anhedonia, low energy + additional symptoms."),
            ("Do antidepressants cause addiction?", "No, SSRIs/SNRIs don't cause addiction. Discontinuation syndrome can occur, so tapering is required."),
            ("Is psychotherapy effective for depression?", "Yes, CBT is first-line treatment. For moderate depression, it matches medication efficacy and reduces relapse risk."),
        ],
    },
    'panik-ataklar': {
        'az': [
            ("Panik atak anında nə etməli?", "4-7-8 nəfəs texnikası: 4 saniyə gəyindirin, 7 saxlayın, 8 verin. 5-4-3-2-1 topraqlanma: 5 gör, 4 toxun, 3 eşit, 2 kokla, 1 dadlandır."),
            ("Panik pozuntu müalicə oluna bilər mi?", "Bəli, KDT + expositions terapiyası 80-90% effekt verir. Dərman (SSRI) yalnız ağır hallarda əlavə edilir."),
        ],
        'ru': [
            ("Что делать во время панической атаки?", "Техника дыхания 4-7-8: вдох 4 сек, задержка 7, выдох 8. Заземление 5-4-3-2-1: 5 увидеть, 4 коснуться, 3 услышать, 2 понюхать, 1 попробовать на вкус."),
            ("Можно ли вылечить паническое расстройство?", "Да, КПТ + экспозиционная терапия дают 80-90% эффект. Лекарства (СИОЗС) только в тяжелых случаях."),
        ],
        'en': [
            ("What to do during a panic attack?", "4-7-8 breathing: inhale 4s, hold 7s, exhale 8s. 5-4-3-2-1 grounding: 5 see, 4 touch, 3 hear, 2 smell, 1 taste."),
            ("Can panic disorder be treated?", "Yes, CBT + exposure therapy achieves 80-90% response. Medication (SSRIs) only for severe cases."),
        ],
    },
    'sosial-fobiya': {
        'az': [
            ("Sosial fobiya nədir?", "İctimai danışmaq, qiydırılma, dəyərləndirilmə qorxusu. DSM-5-TR: 300.23 (F40.10)."),
            ("Müalicə neçə vaxt davam edir?", "KDT kursu adətən 12-20 seans. İlk betterment 4-6 seansda görülür."),
        ],
        'ru': [
            ("Что такое социальная фобия?", "Страх публичных выступлений, оценки, осуждения. DSM-5-TR: 300.23 (F40.10)."),
            ("Сколько длится лечение?", "Курс КПТ обычно 12-20 сеансов. Первые улучшения на 4-6 сеансе."),
        ],
        'en': [
            ("What is social phobia?", "Fear of public speaking, judgment, evaluation. DSM-5-TR: 300.23 (F40.10)."),
            ("How long does treatment take?", "CBT course typically 12-20 sessions. First improvements at 4-6 sessions."),
        ],
    },
    'enurez': {
        'az': [
            ("Enurez hansı yaşda müalicə tələb edir?", "5 yaşdan sonra (ICCS/NICE). 7 yaşda alarm terapiyası birinci xəttdir."),
            ("Alarm cihazı necə işləyir?", "Nəmlik hissəsi sensorsuz nəbız verir → uşaq uyanır → tualetə gedir. 10 həftədə 80% remissiya."),
        ],
        'ru': [
            ("С какого возраста лечить энурез?", "После 5 лет (ICCS/NICE). В 7 лет аларм-терапия — первая линия."),
            ("Как работает аларм-устройство?", "Датчик влаги дает сигнал → ребенок просыпается → идет в туалет. За 10 недель 80% ремиссии."),
        ],
        'en': [
            ("At what age to treat enuresis?", "After age 5 (ICCS/NICE). At age 7, alarm therapy is first-line."),
            ("How does the alarm device work?", "Moisture sensor triggers alarm → child wakes → goes to toilet. 80% remission in 10 weeks."),
        ],
    },
    'aile-terapiyasi': {
        'az': [
            ("Ailə terapiyası necə işləyir?", "Gottman metodu: 4 atlı (tənqid, müdafiə, qəhr, stonewalling) → yumşaq başlanğıc, təmir cəhdləri, fasilə qaydası."),
            ("Neçə seans lazımdır?", "Orta 12-20 seans. Ağır travma hallarında uzadıla bilər."),
        ],
        'ru': [
            ("Как работает семейная терапия?", "Метод Готтмана: 4 всадника (критика, защита, презрение, стенувание) → мягкий старт, попытки исправления, правило паузы."),
            ("Сколько сеансов нужно?", "В среднем 12-20 сеансов. При тяжелых травмах может быть дольше."),
        ],
        'en': [
            ("How does family therapy work?", "Gottman method: 4 horsemen (criticism, defensiveness, contempt, stonewalling) → soft startup, repair attempts, pause rule."),
            ("How many sessions needed?", "Average 12-20 sessions. Severe trauma cases may take longer."),
        ],
    },
    'xidmetler': {
        'az': [
            ("Konsultasiya necə keçirilir?", "Onlayn (Zoom/WhatsApp video) və ofisdə (Bakı, Cəfər Cabbarlı 40). Müddət: 50 dəq. Qiymət: 120 AZN."),
            ("Hansı problemlərlə kömək edirsiniz?", "Depressiya, panik ataklar, sosial fobiya, OKP, ailə münaqişələri, enurez, cinsi pozuntular."),
        ],
        'ru': [
            ("Как проходит консультация?", "Онлайн (Zoom/WhatsApp видео) и в офисе (Баку, Джеффер Джаббарлы 40). Длительность: 50 мин. Цена: 120 AZN."),
            ("С какими проблемами помогаете?", "Депрессия, панические атаки, социальная фобия, ОКР, семейные конфликты, энурез, сексуальные расстройства."),
        ],
        'en': [
            ("How does consultation work?", "Online (Zoom/WhatsApp video) and in-office (Baku, Jafar Jabbarli 40). Duration: 50 min. Price: 120 AZN."),
            ("What problems do you help with?", "Depression, panic attacks, social phobia, OCD, family conflicts, enuresis, sexual disorders."),
        ],
    }
}

def build_faq_schema(slug, lang):
    faqs = FAQ_SCHEMAS.get(slug, {}).get(lang)
    if not faqs: return ''
    items = []
    for q, a in faqs:
        items.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a}
        })
    return f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": {json.dumps(items, ensure_ascii=False)}
}}
</script>'''

# MedicalCondition schema for disorder pages (multilingual)
MEDICAL_CONDITIONS = {
    'depressiya': {
        'az': {'name': 'Depressiya (Major Depressive Disorder)', 'code': 'F32-F33', 'system': 'ICD-11'},
        'ru': {'name': 'Депрессия (Большое депрессивное расстройство)', 'code': 'F32-F33', 'system': 'ICD-11'},
        'en': {'name': 'Depression (Major Depressive Disorder)', 'code': 'F32-F33', 'system': 'ICD-11'},
    },
    'panik-ataklar': {
        'az': {'name': 'Panik Pozuntu', 'code': 'F41.0', 'system': 'ICD-11'},
        'ru': {'name': 'Паническое расстройство', 'code': 'F41.0', 'system': 'ICD-11'},
        'en': {'name': 'Panic Disorder', 'code': 'F41.0', 'system': 'ICD-11'},
    },
    'sosial-fobiya': {
        'az': {'name': 'Sosial Həyəcan Pozuntusu', 'code': 'F40.10', 'system': 'ICD-11'},
        'ru': {'name': 'Социальное тревожное расстройство', 'code': 'F40.10', 'system': 'ICD-11'},
        'en': {'name': 'Social Anxiety Disorder', 'code': 'F40.10', 'system': 'ICD-11'},
    },
    'enurez': {
        'az': {'name': 'Gecə Enurezi', 'code': '6C00', 'system': 'ICD-11'},
        'ru': {'name': 'Ночной энурез', 'code': '6C00', 'system': 'ICD-11'},
        'en': {'name': 'Nocturnal Enuresis', 'code': '6C00', 'system': 'ICD-11'},
    },
}

def build_medical_condition_schema(slug, lang):
    mc = MEDICAL_CONDITIONS.get(slug, {}).get(lang)
    if not mc: return ''
    return f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "MedicalCondition",
  "name": "{mc['name']}",
  "code": {{"@type": "MedicalCode", "codeValue": "{mc['code']}", "codingSystem": "{mc['system']}"}},
  "description": "Clinical information about {mc['name']} diagnosis and treatment."
}}
</script>'''

# Article/BlogPosting schema for blog posts
ARTICLE_META = {
    # AZ blog posts
    'blog-aile': {'az': '5 Prinsip Ailə Müzakirələrinin Həllində', 'ru': '5 Принципов Разрешения Семейных Конфликтов', 'en': '5 Principles of Resolving Family Conflicts', 'cat': 'Family Therapy'},
    'blog-aile-2': {'az': 'Toksik Münasibətin 7 Əlaməti', 'ru': '7 Признаков Токсичных Отношений', 'en': '7 Signs of Toxic Relationships', 'cat': 'Family Therapy'},
    'blog-aile-3': {'az': 'Ailə: Müalicə Yoxsa Ayrılıq?', 'ru': 'Семья на Грани Развода — Лечение или Расставание?', 'en': 'Family on the Brink of Divorce', 'cat': 'Family Therapy'},
    'blog-aile-4': {'az': 'Cütlükdə Düzgün Baxış', 'ru': 'Как Правильно Спорить в Паре?', 'en': 'How to Argue Constructively as a Couple', 'cat': 'Family Therapy'},
    'blog-aile-5': {'az': 'Ümumsizlik Sonra Etimad', 'ru': 'Как Восстановить Доверие После Измены?', 'en': 'How to Rebuild Trust After Infidelity', 'cat': 'Family Therapy'},
    'blog-aile-usaq-2': {'az': 'Uşaq Davranışı: Cəza Yoxsa Anlayış?', 'ru': 'Проблемы Поведения Ребёнка — Наказание или Понимание?', 'en': 'Child Behavior Problems — Punishment or Understanding?', 'cat': 'Child Psychology'},
    'blog-aile-usaq-3': {'az': 'Ayrılıq Sonrası Uşaq', 'ru': 'Ребёнок После Развода — Как Помочь?', 'en': 'Child After Divorce — How to Help?', 'cat': 'Child Psychology'},
    'blog-aile-usaq-4': {'az': 'Məktəb Qaçmağı: 5 Nəqdə', 'ru': 'Отказ от Школы — 5 Настоящих Причин', 'en': 'School Refusal — 5 Real Causes', 'cat': 'Child Psychology'},
    'blog-aile-usaq-5': {'az': 'Uşaqa "Yox" Dəymək', 'ru': 'Как Правильно Говорить Ребёнку «Нет»?', 'en': 'How to Say No to Your Child Correctly', 'cat': 'Child Psychology'},
    'blog-depressiya': {'az': 'Depressiya: Klinik Baxış', 'ru': 'Депрессия — Клинический Обзор', 'en': 'Depression — Clinical Overview', 'cat': 'Depression'},
    'blog-depressiya-2': {'az': 'Depressiya — Məqalə 2', 'ru': 'Депрессия — Статья 2', 'en': 'Depression — Article 2', 'cat': 'Depression'},
    'blog-depressiya-3': {'az': 'Depressiya — Məqalə 3', 'ru': 'Депрессия — Статья 3', 'en': 'Depression — Article 3', 'cat': 'Depression'},
    'blog-depressiya-4': {'az': 'Depressiya — Məqalə 4', 'ru': 'Депрессия — Статья 4', 'en': 'Depression — Article 4', 'cat': 'Depression'},
    'blog-depressiya-5': {'az': 'Depressiya — Məqalə 5', 'ru': 'Депрессия — Статья 5', 'en': 'Depression — Article 5', 'cat': 'Depression'},
    'blog-depressiya-protokol': {'az': 'Depressiya Müalicə Protokolu', 'ru': 'Протокол Лечения Депрессии', 'en': 'Depression Treatment Protocol', 'cat': 'Depression'},
    'blog-enurez': {'az': 'Gecə Enurezi', 'ru': 'Ночной Энурез', 'en': 'Nocturnal Enuresis', 'cat': 'Enuresis'},
    'blog-enurez-2': {'az': 'Gecə Enurezi — Məqalə 2', 'ru': 'Ночной Энурез — Статья 2', 'en': 'Nocturnal Enuresis — Article 2', 'cat': 'Enuresis'},
    'blog-enurez-3': {'az': 'Gecə Enurezi — Məqalə 3', 'ru': 'Ночной Энурез — Статья 3', 'en': 'Nocturnal Enuresis — Article 3', 'cat': 'Enuresis'},
    'blog-enurez-4': {'az': 'Gecə Enurezi — Məqalə 4', 'ru': 'Ночной Энурез — Статья 4', 'en': 'Nocturnal Enuresis — Article 4', 'cat': 'Enuresis'},
    'blog-enurez-5': {'az': 'Gecə Enurezi — Məqalə 5', 'ru': 'Ночной Энурез — Статья 5', 'en': 'Nocturnal Enuresis — Article 5', 'cat': 'Enuresis'},
    'blog-enurez-protokol': {'az': 'Enurez Müalicə Protokolu', 'ru': 'Протокол Лечения Энуреза', 'en': 'Enuresis Treatment Protocol', 'cat': 'Enuresis'},
    'blog-panik': {'az': 'Panik Ataklar', 'ru': 'Панические Атаки', 'en': 'Panic Attacks', 'cat': 'Panic Disorder'},
    'blog-panik-2': {'az': 'Panik Ataklar — Məqalə 2', 'ru': 'Панические Атаки — Статья 2', 'en': 'Panic Attacks — Article 2', 'cat': 'Panic Disorder'},
    'blog-panik-3': {'az': 'Panik Ataklar — Məqalə 3', 'ru': 'Панические Атаки — Статья 3', 'en': 'Panic Attacks — Article 3', 'cat': 'Panic Disorder'},
    'blog-panik-4': {'az': 'Panik Ataklar — Məqalə 4', 'ru': 'Панические Атаки — Статья 4', 'en': 'Panic Attacks — Article 4', 'cat': 'Panic Disorder'},
    'blog-panik-5': {'az': 'Panik Ataklar — Məqalə 5', 'ru': 'Панические Атаки — Статья 5', 'en': 'Panic Attacks — Article 5', 'cat': 'Panic Disorder'},
    'blog-psixolog-olmaq': {'az': 'Psixoloq Peşəsi', 'ru': 'Профессия Психолог', 'en': 'Becoming a Psychologist', 'cat': 'Psychology Career'},
    'blog-psixolog-olmaq-2': {'az': 'Psixoloq Peşəsi — Məqalə 2', 'ru': 'Профессия Психолог — Статья 2', 'en': 'Becoming a Psychologist — Article 2', 'cat': 'Psychology Career'},
    'blog-psixolog-olmaq-3': {'az': 'Psixoloq Peşəsi — Məqalə 3', 'ru': 'Профессия Психолог — Статья 3', 'en': 'Becoming a Psychologist — Article 3', 'cat': 'Psychology Career'},
    'blog-psixolog-olmaq-4': {'az': 'Psixoloq Peşəsi — Məqalə 4', 'ru': 'Профессия Психолог — Статья 4', 'en': 'Becoming a Psychologist — Article 4', 'cat': 'Psychology Career'},
    'blog-psixolog-olmaq-5': {'az': 'Psixoloq Peşəsi — Məqalə 5', 'ru': 'Профессия Психолог — Статья 5', 'en': 'Becoming a Psychologist — Article 5', 'cat': 'Psychology Career'},
    'blog-sosial-fobiya': {'az': 'Sosial Fobiya', 'ru': 'Социофобия', 'en': 'Social Phobia', 'cat': 'Social Anxiety'},
    'blog-sosial-fobiya-2': {'az': 'Sosial Fobiya — Məqalə 2', 'ru': 'Социофобия — Статья 2', 'en': 'Social Phobia — Article 2', 'cat': 'Social Anxiety'},
    'blog-sosial-fobiya-3': {'az': 'Sosial Fobiya — Məqalə 3', 'ru': 'Социофобия — Статья 3', 'en': 'Social Phobia — Article 3', 'cat': 'Social Anxiety'},
    'blog-sosial-fobiya-4': {'az': 'Sosial Fobiya — Məqalə 4', 'ru': 'Социофобия — Статья 4', 'en': 'Social Phobia — Article 4', 'cat': 'Social Anxiety'},
    'blog-sosial-fobiya-5': {'az': 'Sosial Fobiya — Məqalə 5', 'ru': 'Социофобия — Статья 5', 'en': 'Social Phobia — Article 5', 'cat': 'Social Anxiety'},
    'blog-yeniyetme': {'az': 'Gənc Danışmır', 'ru': 'Если Подросток Не Разговаривает С Вами', 'en': 'When a Teenager Stops Talking to You', 'cat': 'Adolescent Psychology'},
    'blog-klinik-psixiatriya': {'az': 'Klinik Psixiatriya Kitabı', 'ru': 'Книга Клиническая Психиатрия', 'en': 'Clinical Psychiatry Book', 'cat': 'Psychiatry Textbook'},
    'blog': {'az': 'Bloq', 'ru': 'Блог', 'en': 'Blog', 'cat': 'Blog'},
}

def build_article_schema(slug, lang):
    meta_dict = ARTICLE_META.get(slug, {})
    if not meta_dict or lang not in meta_dict: return ''
    base = get_base_url(lang)
    # Determine article type
    is_protocol = 'protokol' in slug
    article_type = 'TechArticle' if is_protocol else 'BlogPosting'
    return f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "{article_type}",
  "headline": "{meta_dict[lang]}",
  "description": "Professional psychology article by Kənan Rəhimov, psychiatrist and psychotherapist with 23 years experience.",
  "author": {{
    "@type": "Person",
    "name": "Kənan Rəhimov",
    "url": "https://ragimoff.org/haqqimda.html"
  }},
  "publisher": {{
    "@type": "Organization",
    "name": "RAGIMOFF Psixologiya Məktəbi",
    "url": "https://ragimoff.org/"
  }},
  "datePublished": "2026",
  "inLanguage": "{lang}",
  "articleSection": "{meta_dict['cat']}",
  "url": "{base}{slug}.html",
  "mainEntityOfPage": {{
    "@type": "WebPage",
    "@id": "{base}{slug}.html"
  }}
}}
</script>'''

# HowTo schema for protocol pages
HOWTO_PAGES = {
    'blog-depressiya-protokol': {
        'az': {'name': 'Depressiya Müalicə Protokolu', 'steps': [
            'Klinik müayinə və DSM-5-TR diaqnozu',
            'Şiddət dərəcəsinin qiymətləndirilməsi (PHQ-9)',
            'Birinci xətt: KDT (CBT) 12-20 seans',
            'Orta/ağır: SSRI antidepressant əlavə et',
            '6-8 həftə dəyərləndirmə, dozu tənzimlə',
            'Remissiya sonra 6-12 ay saxla müalicə'
        ]},
        'ru': {'name': 'Протокол Лечения Депрессии', 'steps': [
            'Клинический осмотр и диагноз по DSM-5-TR',
            'Оценка тяжести (PHQ-9)',
            'Первая линия: КПТ 12-20 сеансов',
            'Средняя/тяжелая: добавить СИОЗС',
            'Переоценка через 6-8 недель, коррекция дозы',
            'Поддерживающая терапия 6-12 мес после ремиссии'
        ]},
        'en': {'name': 'Depression Treatment Protocol', 'steps': [
            'Clinical assessment and DSM-5-TR diagnosis',
            'Severity assessment (PHQ-9)',
            'First-line: CBT 12-20 sessions',
            'Moderate/severe: add SSRI antidepressant',
            'Reassessment at 6-8 weeks, dose adjustment',
            'Maintenance therapy 6-12 months after remission'
        ]},
    },
    'blog-enurez-protokol': {
        'az': {'name': 'Enurez Müalicə Protokolu', 'steps': [
            'Uşağın yaşı 5+ (ICCS/NICE)',
            'Medikal səbəblərin aradan qaldırılması',
            'Alarm terapiyası — birinci xətt (10-12 həftə)',
            'Uğursuz olarsa: desmopressin 0.2-0.4 mg',
            'Kombinasiya: alarm + desmopressin',
            'Remissiya: 14 gecə quru → azaldma'
        ]},
        'ru': {'name': 'Протокол Лечения Энуреза', 'steps': [
            'Возраст ребёнка 5+ (ICCS/NICE)',
            'Исключение медицинских причин',
            'Аларм-терапия — первая линия (10-12 недель)',
            'При неэффективности: десмопрессин 0.2-0.4 мг',
            'Комбинация: аларм + десмопрессин',
            'Ремиссия: 14 сухих ночей → понижение'
        ]},
        'en': {'name': 'Enuresis Treatment Protocol', 'steps': [
            'Child age 5+ (ICCS/NICE)',
            'Rule out medical causes',
            'Alarm therapy — first line (10-12 weeks)',
            'If ineffective: desmopressin 0.2-0.4 mg',
            'Combination: alarm + desmopressin',
            'Remission: 14 dry nights → taper'
        ]},
    },
    'blog-aile-4': {
        'az': {'name': 'Cütlükdə Düzgün Baxış', 'steps': [
            'Yumşaq başlanğıc (soft startup)',
            '4 atlıdan qaçın: tənqid, müdafiə, qəhr, stonewalling',
            'Təmir cəhdləri (repair attempts) et',
            '20 dəqiqə fasilə qaydası',
            'Kompromiss axtar, "biz" dili istifadə et'
        ]},
        'ru': {'name': 'Как Правильно Спорить в Паре', 'steps': [
            'Мягкий старт (soft startup)',
            'Избегайте 4 всадников: критика, защита, презрение, стенувание',
            'Делайте попытки исправления (repair attempts)',
            'Правило 20-минутной паузы',
            'Ищите компромисс, используйте язык "мы"'
        ]},
        'en': {'name': 'How to Argue Constructively as a Couple', 'steps': [
            'Soft startup',
            'Avoid 4 horsemen: criticism, defensiveness, contempt, stonewalling',
            'Make repair attempts',
            '20-minute break rule',
            'Seek compromise, use "we" language'
        ]},
    },
}

def build_howto_schema(slug, lang):
    ht = HOWTO_PAGES.get(slug, {}).get(lang)
    if not ht: return ''
    steps = []
    for i, step in enumerate(ht['steps'], 1):
        steps.append({
            "@type": "HowToStep",
            "position": i,
            "name": f"Step {i}",
            "text": step
        })
    return f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "{ht['name']}",
  "description": "Step-by-step clinical protocol by Kənan Rəhimov, psychiatrist with 23 years experience.",
  "author": {{
    "@type": "Person",
    "name": "Kənan Rəhimov"
  }},
  "step": {json.dumps(steps, ensure_ascii=False)}
}}
</script>'''

# Person schema for author
PERSON_SCHEMA = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Kənan Rəhimov",
  "alternateName": "Kenan Ragimov",
  "jobTitle": "Həkim-Psixiatr, Psixoterapevt",
  "description": "23 illik klinik təcrübəyə malik həkim-psixiatr, psixoterapevt və psixologiya müəllimi. RAGIMOFF Psixologiya Məktəbi saisidir.",
  "url": "https://ragimoff.org/haqqimda.html",
  "sameAs": [
    "https://t.me/dockenan",
    "https://www.linkedin.com/in/kenan-ragimov"
  ],
  "knowsAbout": [
    "Psixiatriya", "Psixoterapiya", "KDT", "EMDR", "Depressiya", "OKP", "PTSD",
    "Ailə terapiyası", "Uşaq psixiatriyası", "Psixologiya təhsili"
  ],
  "worksFor": {
    "@type": "Organization",
    "name": "RAGIMOFF Psixologiya Məktəbi",
    "url": "https://ragimoff.org/"
  },
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Cəfər Cabbarlı küçəsi 40",
    "addressLocality": "Bakı",
    "addressCountry": "AZ"
  }
}
</script>'''

# EducationalOrganization schema for education pages
EDU_ORG_SCHEMA = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "EducationalOrganization",
  "name": "RAGIMOFF Psixologiya Məktəbi",
  "alternateName": "RAGIMOFF Psychology School",
  "url": "https://ragimoff.org/",
  "description": "Professional psychology education: DPO diplomas, psychotherapy practicum, international certificates (IPAS/BPA).",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Cəfər Cabbarlı küçəsi 40",
    "addressLocality": "Bakı",
    "addressCountry": "AZ"
  },
  "telephone": "+994-70-220-03-76",
  "email": "info@ragimoff.org"
}
</script>'''

# ═══════════════════════════════════════════════════════════════════
# MAIN PROCESSING
# ══════════════════════════════════════════════════════════════════

def process_directory(dir_path, lang):
    """Process all HTML files in a directory"""
    updated = 0
    for fpath in sorted(glob.glob(os.path.join(dir_path, '*.html'))):
        slug = os.path.basename(fpath).replace('.html', '')
        if slug in ('template', 'wc', 'gp', 'temp_index'): continue
        
        html = read_html(fpath)
        # Additive OG normalization (og:locale / og:image) — before schema logic
        og_html = normalize_og(html, lang, slug, os.path.relpath(dir_path, ROOT))
        if og_html != html:
            write_html(fpath, og_html)
            html = og_html
            updated += 1
            print(f'  [{lang}] OG normalized: {slug}.html')
        
        tags_to_add = []
        
        # WebSite schema - only on index
        if slug == 'index' and not has_schema(html, 'WebSite'):
            tags_to_add.append(build_website_schema(lang))
        
        # Organization schema - on index and main pages
        main_pages = ('index', 'haqqimda', 'xidmetler', 'tehsil', 'valideyn-mektebi', 'samira', 'qanunlar', 'b2b', 'blog', 'klinik-psixiatriya')
        if slug in main_pages and not has_schema(html, 'Organization'):
            tags_to_add.append(build_org_schema(lang))
        
        # Person schema - on haqqimda
        if slug == 'haqqimda' and not has_schema(html, 'Person'):
            tags_to_add.append(PERSON_SCHEMA)
        
        # EducationalOrganization - on tehsil and program pages
        if slug in ('tehsil', 'program-umumi', 'program-klinik', 'program-praktikum') and not has_schema(html, 'EducationalOrganization'):
            tags_to_add.append(EDU_ORG_SCHEMA)
        
        # Service schema
        if slug in SERVICE_SCHEMAS and not has_schema(html, 'Service'):
            tags_to_add.append(build_service_schema(slug, lang))
        
        # MedicalCondition schema for disorder pages
        if slug in MEDICAL_CONDITIONS and not has_schema(html, 'MedicalCondition'):
            tags_to_add.append(build_medical_condition_schema(slug, lang))
        
        # Course schema
        if slug in COURSE_SCHEMAS and not has_schema(html, 'Course'):
            tags_to_add.append(build_course_schema(slug, lang))
        
        # Book schema
        if slug == 'klinik-psixiatriya' and not has_schema(html, 'Book'):
            tags_to_add.append(build_book_schema(lang))
        
        # FAQ schema
        if slug in FAQ_SCHEMAS and not has_schema(html, 'FAQPage'):
            tags_to_add.append(build_faq_schema(slug, lang))
        
        # Article/BlogPosting schema
        if slug in ARTICLE_META and not has_schema(html, 'BlogPosting') and not has_schema(html, 'TechArticle'):
            tags_to_add.append(build_article_schema(slug, lang))
        
        # HowTo schema for protocol pages
        if slug in HOWTO_PAGES and not has_schema(html, 'HowTo'):
            tags_to_add.append(build_howto_schema(slug, lang))
        
        # BreadcrumbList - on all pages
        if not has_schema(html, 'BreadcrumbList'):
            title_match = re.search(r'<title>([^<]+)</title>', html, re.I)
            page_title = title_match.group(1) if title_match else slug
            # Build correct URL path
            rel_dir = os.path.relpath(dir_path, ROOT)
            if rel_dir == '.':
                url_path = f'/{slug}.html'
            else:
                url_path = f'/{rel_dir}/{slug}.html'
            tags_to_add.append(build_breadcrumb_schema(url_path, page_title, lang))
        
        if tags_to_add:
            new_html = insert_before_head_end(html, '\n'.join(tags_to_add))
            if new_html != html:
                write_html(fpath, new_html)
                updated += 1
                print(f'  [{lang}] Updated: {slug}.html (+{len(tags_to_add)} schemas)')
            else:
                print(f'  [{lang}] No change: {slug}.html')
        else:
            print(f'  [{lang}] Skipped: {slug}.html')
    
    return updated

def main():
    total_updated = 0
    
    # Process root (AZ)
    print('Processing AZ (root)...')
    total_updated += process_directory(ROOT, 'az')
    
    # Process EN
    print('\nProcessing EN...')
    en_dir = os.path.join(ROOT, 'en')
    if os.path.exists(en_dir):
        total_updated += process_directory(en_dir, 'en')
    
    # Process RU
    print('\nProcessing RU...')
    ru_dir = os.path.join(ROOT, 'ru')
    if os.path.exists(ru_dir):
        total_updated += process_directory(ru_dir, 'ru')
    
    print(f'\n=== Total updated: {total_updated} files ===')

if __name__ == '__main__':
    main()