#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RAGIMOFF /67 — генератор главной по новой дизайн-системе.
Контент отделён от шаблона: TEXTS + DATA -> HTML.
Запуск: python build.py
"""
import html
import pathlib

OUT = pathlib.Path(__file__).resolve().parents[1]
BASE = "/67"
SITE = "https://ragimoff.org"

LANGS = ["az", "ru", "en"]

TEXTS = {
"az": {
  "lang_name": "AZ", "html_lang": "az",
  "nav": ["Mütəxəssislər", "Kitablar", "Təhsil", "Konsultasiya", "Bloq", "Əlaqə"],
  "nav_href": ["/az/mutexessisler/index.html", "/books/", "/az/telim/index.html", "/az/konsultasiya/index.html", "/az/bloq/index.html", "/az/elaqe/index.html"],
  "cta": "Qeydiyyat",
  "hero_badge": "IPAS Ambassador · BAPPs · ADA",
  "hero_h1": "Psixologiya<br><em>Məktəbi</em>",
  "hero_sub": "23 il klinik təcrübə. Rəsmi diplom. Beynəlxalq sertifikat. Azərbaycan dilində.",
  "hero_btn1": "Təhsil proqramları",
  "hero_btn2": "Konsultasiya",
  "hero_note": "Kənan Rəhimov — klinik psixoloq, psixoterapevt, IPAS ambassadoru",
  "marquee": ["Rəsmi Əlavə Təhsil diplomu", "IPAS sertifikatı", "Klinik psixologiya", "Psixoterapiya praktikumu", "Psixoanaliz", "Psixodiaqnostika", "Ailə terapiyası", "Korporativ təlimlər"],
  "stats": [("23+", "il klinik təcrübə"), ("3000+", "pasient"), ("2000+", "HR məzunu"), ("11", "beynəlxalq sertifikat")],
  "lib_eyebrow": "Açıq kitabxana",
  "lib_h2": "Freyd azərbaycan dilində. İlk dəfə. Pulsuz.",
  "lib_text": "Ziqmund Freydin 24 kitabı orijinal alman dilindən azərbaycan dilinə tərcümə edilib. Tələbə, praktik və ya sadəcə oxucu — hamı üçün açıqdır. Onlayn oxuyun, yükləyin, lazım olsa çap versiyasını sifariş edin.",
  "lib_nums": [("24", "Freyd kitabı"), ("4", "dil"), ("0 ₼", "oxumaq üçün")],
  "lib_btn": "Kitabxananı aç",
  "lib_note": "Bütün kolleksiya: 94 cild — Freyd, Kənan Rəhimov, Samirə Rəhimova.",
  "tb_eyebrow": "Dərslik",
  "tb_h2": "«Klinik Psixiatriya» — müəllifi özü",
  "tb_text": "384 səhifə. DSM-5, ICD-11, beynəlxalq protokollar və konsensus. 4 dildə. Rəsmi dərslik — və onu pulsuz oxumaq mümkündür.",
  "tb_meta": ["384 səhifə", "4 dil", "2024", "Pulsuz oxu"],
  "tb_btn1": "Pulsuz oxu",
  "tb_btn2": "Çap versiyası",
  "film_eyebrow": "Təcrübədən",
  "film_h2": "«Səbinənin draması»",
  "film_text": "Real hadisənin ekranlaşdırılması. 31 dəqiqə. Şərhsiz.",
  "film_btn": "İzlə",
  "prog_eyebrow": "Təhsil",
  "prog_h2": "6 tədris proqramı",
  "prog_lead": "Rəsmi diplom, praktika və beynəlxalq sertifikat. Qiymətlər və müddətlər — açıq.",
  "prog_more": "Proqram",
  "prog_reg": "Qeydiyyat",
  "prog_start": "Başlanğıc", "prog_dur": "Müddət", "prog_price": "Tam qiymət", "prog_pre": "Öncədən", "prog_month": "Aylıq",
  "timeline_eyebrow": "Dossier",
  "timeline_h2": "1994 → 2026",
  "timeline": [
    ("1994–2001", "Azərbaycan Dövlət Tibb Universiteti. Həkim-psixiatr, internatura."),
    ("2001–2003", "Sankt-Peterburq: B.D. Karvasarski, V.D. Vid. Bexterev institutu — qırmızı diplom."),
    ("2003–2008", "«Regional Psixologiya Mərkəzi» — direktor. TV və radio."),
    ("2008", "GTC və «HR Məktəbi». 2000+ məzun. 2019-dan dövlət sertifikatı."),
    ("2012", "Ragimoff HK Ltd — Honq-Konq. Kino və biznes."),
    ("2017", "Ragimoff LP — Şotlandiya. «Garnet», «Jobiman»."),
    ("2020", "ICD-11 azərbaycan dilinə. «Ümumi psixoterapiya» kitabı."),
    ("2021–2022", "Karvasarski institutu və SPb DPO nümayəndəliyi. IPAS ambassadoru."),
  ],
  "ipas_qr": "IPAS reyestrində yoxla",
  "myth_eyebrow": "Miflər və faktlar",
  "myth_h2": "Nə deyirlər — və həqiqətdə nədir",
  "myth_lead": "Mənbə göstərilir. Yoxlaya bilərsiniz.",
  "myth_label": "MİF", "myth_fact": "Fakt:",
  "myths": [
    ("«Melipramin oyanma refleksini formalaşdırır»", "Əslində: yataq islatmaya qarşı refleks yaratmır — sidik ifrazını gecikdirir, bu isə dərmanın yan təsiridir. Kardiotoksikdir, ölüm halları məlumdur. Uşaq enurezində tövsiyə olunmur.", "Mənbə: «Klinik Psixiatriya», enurez bölməsi"),
    ("«Enurezin enurezində istifadə oluna bilər»", "Əslində: Azərbaycan Respublikası Səhiyyə Nazirliyinin sənədləri pediatriyada gecə enurezi üçün tövsiyə etmir.", "Mənbə: Səhiyyə Nazirliyinin PDF sənədi"),
    ("«Akupunktur enurezi müalicə edir»", "Əslində: kognitiv sfera və davranışa sübut edilmiş təsiri yoxdur. Psixoloji pozuntunun müalicəsində effektivliyi təsdiqlənməyib.", "Mənbə: beynəlxalq protokollar və konsensus"),
  ],
  "cons_eyebrow": "Konsultasiya",
  "cons_h2": "Üç format. Bir məqsəd.",
  "cons_lead": "Şəxsi terapiya, cüt terapiya və ya superviziya — hansının sizə uyğun olduğunu bilmirsinizsə, bir sətirdə izah edirik.",
  "cons": [
    ("Fərdi", "Kənan Rəhimov / Samirə Rəhimova", "Şəxsi terapiya, depressiya, panik, fobiya, enurez."),
    ("İki mütəxəssis", "Kənan + Samirə", "Ailə və cüt terapiyası, mürəkkəb hallar."),
    ("Superviziya", "Kənan Rəhimov", "Psixologiya tələbələri və praktik mütəxəssislər üçün."),
  ],
  "cons_btn": "Ətraflı",
  "books_eyebrow": "Kitablar",
  "books_h2": "Oxu — pulsuz. İstəsən — çap.",
  "books": [
    ("Klinik Psixiatriya", "384 səh., 4 dil", "28 ₼", "/books/covers/klinik.jpg"),
    ("Günahkarlıq virusu", "224 səh.", "22 ₼", "/books/covers/guilt.jpg"),
    ("Şizofreniya. Cinnət pandemiyası", "312 səh.", "26 ₼", "/books/covers/pandemic.jpg"),
    ("Feniks erası", "288 səh.", "24 ₼", "/books/covers/phoenix.jpg"),
  ],
  "book_read": "Pulsuz oxu",
  "book_order": "Sifariş",
  "biz_eyebrow": "Biznes və HR",
  "biz_h2": "HR Məktəbi — 2008-dən",
  "biz_text": "2000-dən çox HR məzunu, 3000-dən çox təlim iştirakçısı. MG, Unibank, DNS Computers. 2019-dan dövlət sertifikatı.",
  "biz_nums": [("2008", "təsis ili"), ("2000+", "HR məzunu"), ("3000+", "təlim iştirakçısı")],
  "biz_btn": "Korporativ proqramlar",
  "events_eyebrow": "Business Party",
  "events_h2": "2015–2016. Üç məkan.",
  "events": [
    ("2015", "JW Marriott Absheron", "«Kommunikasiya»"),
    ("2015", "Kempinski Badamdar", "«2016 biznes imkanları»"),
    ("2016", "Fairmont Flame Towers", "«Made in Italy»"),
  ],
  "tg_h2": "Davamı — Telegram-da",
  "tg_text": "Suallar, canlı yayımlar, klinik halların təhlili. Dil seçin.",
  "tg_az": "Azərbaycanca", "tg_ru": "Rusca",
  "blog_eyebrow": "Bloq",
  "blog_h2": "Protokollar, rəylər deyil",
  "blog": [
    ("Klinik protokol", "Psixogen depressiyanın müalicəsi", "17 illik klinik təcrübə. Protokol · 18 dəq", "/az/bloq/depressiya-protokol.html", "/images/blog/depressiya/protokol-cover.jpg"),
    ("Klinik protokol", "Gecə enurezi — modifikasiya edilmiş protokol", "10 həftəlik proqram. n=240, 80% remissiya. · 14 dəq", "/az/bloq/enurez-protokol.html", "/images/blog/enurez/protokol-cover.jpg"),
    ("Klinik psixologiya", "KDT depressiyada necə işləyir?", "Üçbucaq, avtomatik düşüncələr, davranış aktivləşməsi. · 11 dəq", "/az/bloq/depressiya-2.html", "/images/blog/depressiya/art2-cover.jpg"),
  ],
  "blog_read": "Oxu",
  "foot_desc": "Peşəkar Psixologiya Məktəbi. Klinik təcrübə, rəsmi təhsil, beynəlxalq sertifikat.",
  "foot_cols": [
    ("Terapiya", ["Ailə terapiyası", "Gecə enurezi", "Panik ataklar", "Depressiya", "Sosial fobiya"]),
    ("Təhsil", ["Ümumi psixologiya", "Klinik psixologiya", "Psixoterapiya praktikumu", "Psixoanaliz", "Psixodiaqnostika"]),
    ("Əlaqə", ["+994 70 220 03 76", "info@ragimoff.org", "Bakı, Cəfər Cabbarlı 40", "Caspian Business Center"]),
  ],
  "foot_rights": "© 2026 RAGIMOFF. Bütün hüquqlar qorunur.",
  "foot_note": "Peşəkar nüfuzun ünvanı.",
  "prose_note": "Qiymətlər və proqram şərtləri dəyişməz deyil — aktual məlumat üçün əlaqə saxlayın.",
},
"ru": {
  "lang_name": "RU", "html_lang": "ru",
  "nav": ["Специалисты", "Книги", "Обучение", "Консультации", "Блог", "Контакты"],
  "nav_href": ["/ru/mutexessisler/index.html", "/books/", "/ru/telim/index.html", "/ru/konsultasiya/index.html", "/ru/bloq/index.html", "/ru/elaqe/index.html"],
  "cta": "Записаться",
  "hero_badge": "IPAS Ambassador · BAPPs · ADA",
  "hero_h1": "Школа<br><em>психологии</em>",
  "hero_sub": "23 года клинической практики. Официальный диплом. Международный сертификат. На азербайджанском.",
  "hero_btn1": "Программы обучения",
  "hero_btn2": "Консультация",
  "hero_note": "Кенан Рагимов — клинический психолог, психотерапевт, амбассадор IPAS",
  "marquee": ["Официальный диплом ДПО", "Сертификат IPAS", "Клиническая психология", "Практикум психотерапии", "Психоанализ", "Психодиагностика", "Семейная терапия", "Корпоративные тренинги"],
  "stats": [("23+", "года практики"), ("3000+", "пациентов"), ("2000+", "выпускников HR"), ("11", "международных сертификатов")],
  "lib_eyebrow": "Открытая библиотека",
  "lib_h2": "Фрейд на азербайджанском. Впервые. Бесплатно.",
  "lib_text": "24 книги Зигмунда Фрейда переведены с оригинального немецкого на азербайджанский. Для студента, практика и любого читателя. Читайте онлайн, скачивайте, при желании закажите печатную версию.",
  "lib_nums": [("24", "книги Фрейда"), ("4", "языка"), ("0 ₼", "за чтение")],
  "lib_btn": "Открыть библиотеку",
  "lib_note": "Вся коллекция: 94 тома — Фрейд, Кенан Рагимов, Самира Рагимова.",
  "tb_eyebrow": "Учебник",
  "tb_h2": "«Клиническая психиатрия» — автор он же",
  "tb_text": "384 страницы. DSM-5, ICD-11, международные протоколы и консенсус. 4 языка. Официальный учебник — и его можно читать бесплатно.",
  "tb_meta": ["384 страницы", "4 языка", "2024", "Читать бесплатно"],
  "tb_btn1": "Читать бесплатно",
  "tb_btn2": "Печатная версия",
  "film_eyebrow": "Из практики",
  "film_h2": "«Драма Сабины»",
  "film_text": "Экранизация реального случая. 31 минута. Без комментариев.",
  "film_btn": "Смотреть",
  "prog_eyebrow": "Обучение",
  "prog_h2": "6 программ обучения",
  "prog_lead": "Официальный диплом, практика и международный сертификат. Цены и сроки — открыто.",
  "prog_more": "Программа",
  "prog_reg": "Записаться",
  "prog_start": "Старт", "prog_dur": "Срок", "prog_price": "Полная цена", "prog_pre": "При оплате вперёд", "prog_month": "В месяц",
  "timeline_eyebrow": "Досье",
  "timeline_h2": "1994 → 2026",
  "timeline": [
    ("1994–2001", "Азербайджанский медицинский университет. Врач-психиатр, интернатура."),
    ("2001–2003", "Санкт-Петербург: Б.Д. Карвасарский, В.Д. Вид. Институт Бехтерева — красный диплом."),
    ("2003–2008", "«Региональный психологический центр» — директор. ТВ и радио."),
    ("2008", "GTC и «HR Школа». 2000+ выпускников. С 2019 — государственный сертификат."),
    ("2012", "Ragimoff HK Ltd — Гонконг. Кино и бизнес."),
    ("2017", "Ragimoff LP — Шотландия. «Garnet», «Jobiman»."),
    ("2020", "ICD-11 на азербайджанский. Книга «Общая психотерапия»."),
    ("2021–2022", "Институт Карвасарского и представительство СПб ДПО. Амбассадор IPAS."),
  ],
  "ipas_qr": "Проверить в реестре IPAS",
  "myth_eyebrow": "Мифы и факты",
  "myth_h2": "Что говорят — и что на самом деле",
  "myth_lead": "Источник указан. Можно проверить.",
  "myth_label": "МИФ", "myth_fact": "Факт:",
  "myths": [
    ("«Мелипрамин формирует рефлекс пробуждения»", "На самом деле: рефлекс не формирует — вызывает задержку мочеиспускания как побочный эффект. Кардиотоксичен, известны случаи смерти. При энурезе у детей не рекомендован.", "Источник: «Клиническая психиатрия», раздел об энурезе"),
    ("«Энурезин можно применять при энурезе»", "На самом деле: документы Министерства здравоохранения АР не рекомендуют его в педиатрии для лечения ночного энуреза.", "Источник: PDF Министерства здравоохранения АР"),
    ("«Акупунктура лечит энурез»", "На самом деле: доказанного влияния на когнитивную сферу и поведение нет. Эффективность при психологическом расстройстве не подтверждена.", "Источник: международные протоколы и консенсус"),
  ],
  "cons_eyebrow": "Консультации",
  "cons_h2": "Три формата. Одна цель.",
  "cons_lead": "Личная терапия, парная или супервизия — если не знаете, что выбрать, объясним одной строкой.",
  "cons": [
    ("Индивидуально", "Кенан Рагимов / Самира Рагимова", "Личная терапия, депрессия, паника, фобия, энурез."),
    ("Два специалиста", "Кенан + Самира", "Семейная и парная терапия, сложные случаи."),
    ("Супервизия", "Кенан Рагимов", "Для студентов-психологов и практикующих специалистов."),
  ],
  "cons_btn": "Подробнее",
  "books_eyebrow": "Книги",
  "books_h2": "Читай — бесплатно. Хочешь — в печати.",
  "books": [
    ("Клиническая психиатрия", "384 с., 4 языка", "28 ₼", "/books/covers/klinik.jpg"),
    ("Вирус вины", "224 с.", "22 ₼", "/books/covers/guilt.jpg"),
    ("Шизофрения. Пандемия безумия", "312 с.", "26 ₼", "/books/covers/pandemic.jpg"),
    ("Эра Феникса", "288 с.", "24 ₼", "/books/covers/phoenix.jpg"),
  ],
  "book_read": "Читать бесплатно",
  "book_order": "Заказать",
  "biz_eyebrow": "Бизнес и HR",
  "biz_h2": "HR Школа — с 2008 года",
  "biz_text": "Более 2000 выпускников HR, более 3000 участников тренингов. MG, Unibank, DNS Computers. С 2019 — государственный сертификат.",
  "biz_nums": [("2008", "год основания"), ("2000+", "выпускников HR"), ("3000+", "участников тренингов")],
  "biz_btn": "Корпоративные программы",
  "events_eyebrow": "Business Party",
  "events_h2": "2015–2016. Три площадки.",
  "events": [
    ("2015", "JW Marriott Absheron", "«Коммуникация»"),
    ("2015", "Kempinski Badamdar", "«Возможности бизнеса в 2016»"),
    ("2016", "Fairmont Flame Towers", "«Made in Italy»"),
  ],
  "tg_h2": "Продолжение — в Telegram",
  "tg_text": "Вопросы, эфиры, разбор клинических случаев. Выберите язык.",
  "tg_az": "На азербайджанском", "tg_ru": "На русском",
  "blog_eyebrow": "Блог",
  "blog_h2": "Протоколы, а не мнения",
  "blog": [
    ("Клинический протокол", "Лечение психогенной депрессии", "17 лет клинической практики. Протокол · 18 мин", "/ru/bloq/depressiya-protokol.html", "/images/blog/depressiya/protokol-cover.jpg"),
    ("Клинический протокол", "Ночной энурез — модифицированный протокол", "10-недельная программа. n=240, 80% ремиссия. · 14 мин", "/ru/bloq/enurez-protokol.html", "/images/blog/enurez/protokol-cover.jpg"),
    ("Клиническая психология", "Как КПТ работает при депрессии", "Треугольник, автоматические мысли, поведенческая активация. · 11 мин", "/ru/bloq/depressiya-2.html", "/images/blog/depressiya/art2-cover.jpg"),
  ],
  "blog_read": "Читать",
  "foot_desc": "Профессиональная школа психологии. Клиническая практика, официальное образование, международный сертификат.",
  "foot_cols": [
    ("Терапия", ["Семейная терапия", "Ночной энурез", "Панические атаки", "Депрессия", "Социальная фобия"]),
    ("Обучение", ["Общая психология", "Клиническая психология", "Практикум психотерапии", "Психоанализ", "Психодиагностика"]),
    ("Контакты", ["+994 70 220 03 76", "info@ragimoff.org", "Баку, Джафар Джаббарлы 40", "Caspian Business Center"]),
  ],
  "foot_rights": "© 2026 RAGIMOFF. Все права защищены.",
  "foot_note": "Адрес профессиональной репутации.",
  "prose_note": "Цены и условия программ могут меняться — уточняйте актуальную информацию.",
},
"en": {
  "lang_name": "EN", "html_lang": "en",
  "nav": ["Specialists", "Books", "Training", "Consultations", "Blog", "Contact"],
  "nav_href": ["/en/mutexessisler/index.html", "/books/", "/en/telim/index.html", "/en/konsultasiya/index.html", "/en/bloq/index.html", "/en/elaqe/index.html"],
  "cta": "Book now",
  "hero_badge": "IPAS Ambassador · BAPPs · ADA",
  "hero_h1": "School of<br><em>Psychology</em>",
  "hero_sub": "23 years of clinical practice. Official diploma. International certificate. In Azerbaijani.",
  "hero_btn1": "Training programs",
  "hero_btn2": "Consultation",
  "hero_note": "Kenan Ragimov — clinical psychologist, psychotherapist, IPAS Ambassador",
  "marquee": ["Official CPD diploma", "IPAS certificate", "Clinical psychology", "Psychotherapy practicum", "Psychoanalysis", "Psychodiagnostics", "Family therapy", "Corporate training"],
  "stats": [("23+", "years of practice"), ("3000+", "patients"), ("2000+", "HR graduates"), ("11", "international certificates")],
  "lib_eyebrow": "Open library",
  "lib_h2": "Freud in Azerbaijani. First time. Free.",
  "lib_text": "24 books by Sigmund Freud translated from the original German into Azerbaijani. For students, practitioners and any reader. Read online, download, or order a printed copy.",
  "lib_nums": [("24", "Freud books"), ("4", "languages"), ("0 ₼", "to read")],
  "lib_btn": "Open the library",
  "lib_note": "Full collection: 94 volumes — Freud, Kenan Ragimov, Samira Ragimova.",
  "tb_eyebrow": "Textbook",
  "tb_h2": "“Clinical Psychiatry” — by the author",
  "tb_text": "384 pages. DSM-5, ICD-11, international protocols and consensus. 4 languages. The official textbook — free to read.",
  "tb_meta": ["384 pages", "4 languages", "2024", "Free to read"],
  "tb_btn1": "Read free",
  "tb_btn2": "Printed edition",
  "film_eyebrow": "From practice",
  "film_h2": "“Sabina's Drama”",
  "film_text": "A real case, dramatised. 31 minutes. No commentary.",
  "film_btn": "Watch",
  "prog_eyebrow": "Training",
  "prog_h2": "6 training programs",
  "prog_lead": "Official diploma, practice and international certificate. Prices and dates — open.",
  "prog_more": "Program",
  "prog_reg": "Enroll",
  "prog_start": "Start", "prog_dur": "Duration", "prog_price": "Full price", "prog_pre": "Prepaid", "prog_month": "Monthly",
  "timeline_eyebrow": "Dossier",
  "timeline_h2": "1994 → 2026",
  "timeline": [
    ("1994–2001", "Azerbaijan Medical University. Psychiatrist, internship."),
    ("2001–2003", "St Petersburg: B.D. Karvasarsky, V.D. Vid. Bekhterev Institute — honours diploma."),
    ("2003–2008", "Regional Psychology Center — director. TV and radio."),
    ("2008", "GTC and HR School. 2000+ graduates. State certificate since 2019."),
    ("2012", "Ragimoff HK Ltd — Hong Kong. Film and business."),
    ("2017", "Ragimoff LP — Scotland. Garnet, Jobiman."),
    ("2020", "ICD-11 into Azerbaijani. “General Psychotherapy” book."),
    ("2021–2022", "Karvasarsky Institute and St Petersburg CPD representative office. IPAS Ambassador."),
  ],
  "ipas_qr": "Verify in the IPAS registry",
  "myth_eyebrow": "Myths and facts",
  "myth_h2": "What they say — and what is true",
  "myth_lead": "The source is given. You can verify it.",
  "myth_label": "MYTH", "myth_fact": "Fact:",
  "myths": [
    ("“Melipramine builds an awakening reflex”", "In fact: it does not build a reflex — it delays urination as a side effect. Cardiotoxic; deaths are known. Not recommended for childhood enuresis.", "Source: “Clinical Psychiatry”, enuresis section"),
    ("“Enurexin can be used for enuresis”", "In fact: documents of the Ministry of Health of Azerbaijan do not recommend it in paediatrics for nocturnal enuresis.", "Source: Ministry of Health PDF"),
    ("“Acupuncture cures enuresis”", "In fact: there is no proven effect on cognition or behaviour. Efficacy in a psychological disorder is not confirmed.", "Source: international protocols and consensus"),
  ],
  "cons_eyebrow": "Consultations",
  "cons_h2": "Three formats. One goal.",
  "cons_lead": "Individual therapy, couples therapy or supervision — if you don't know what to choose, we explain in one line.",
  "cons": [
    ("Individual", "Kenan Ragimov / Samira Ragimova", "Personal therapy, depression, panic, phobia, enuresis."),
    ("Two specialists", "Kenan + Samira", "Family and couples therapy, complex cases."),
    ("Supervision", "Kenan Ragimov", "For psychology students and practising specialists."),
  ],
  "cons_btn": "Details",
  "books_eyebrow": "Books",
  "books_h2": "Read free. Order print if you prefer.",
  "books": [
    ("Clinical Psychiatry", "384 pp., 4 languages", "28 ₼", "/books/covers/klinik.jpg"),
    ("The Guilt Virus", "224 pp.", "22 ₼", "/books/covers/guilt.jpg"),
    ("Schizophrenia. Pandemic of Madness", "312 pp.", "26 ₼", "/books/covers/pandemic.jpg"),
    ("The Phoenix Era", "288 pp.", "24 ₼", "/books/covers/phoenix.jpg"),
  ],
  "book_read": "Read free",
  "book_order": "Order",
  "biz_eyebrow": "Business & HR",
  "biz_h2": "HR School — since 2008",
  "biz_text": "2000+ HR graduates, 3000+ training participants. MG, Unibank, DNS Computers. State certificate since 2019.",
  "biz_nums": [("2008", "founded"), ("2000+", "HR graduates"), ("3000+", "training participants")],
  "biz_btn": "Corporate programs",
  "events_eyebrow": "Business Party",
  "events_h2": "2015–2016. Three venues.",
  "events": [
    ("2015", "JW Marriott Absheron", "“Communication”"),
    ("2015", "Kempinski Badamdar", "“Business opportunities 2016”"),
    ("2016", "Fairmont Flame Towers", "“Made in Italy”"),
  ],
  "tg_h2": "Continue on Telegram",
  "tg_text": "Questions, live streams, clinical case reviews. Choose your language.",
  "tg_az": "In Azerbaijani", "tg_ru": "In Russian",
  "blog_eyebrow": "Blog",
  "blog_h2": "Protocols, not opinions",
  "blog": [
    ("Clinical protocol", "Treating psychogenic depression", "17 years of clinical practice. Protocol · 18 min", "/en/bloq/depressiya-protokol.html", "/images/blog/depressiya/protokol-cover.jpg"),
    ("Clinical protocol", "Nocturnal enuresis — modified protocol", "10-week program. n=240, 80% remission. · 14 min", "/en/bloq/enurez-protokol.html", "/images/blog/enurez/protokol-cover.jpg"),
    ("Clinical psychology", "How CBT works in depression", "Triangle, automatic thoughts, behavioural activation. · 11 min", "/en/bloq/depressiya-2.html", "/images/blog/depressiya/art2-cover.jpg"),
  ],
  "blog_read": "Read",
  "foot_desc": "Professional School of Psychology. Clinical practice, official education, international certificate.",
  "foot_cols": [
    ("Therapy", ["Family therapy", "Nocturnal enuresis", "Panic attacks", "Depression", "Social phobia"]),
    ("Training", ["General psychology", "Clinical psychology", "Psychotherapy practicum", "Psychoanalysis", "Psychodiagnostics"]),
    ("Contact", ["+994 70 220 03 76", "info@ragimoff.org", "Baku, Jafar Jabbarli 40", "Caspian Business Center"]),
  ],
  "foot_rights": "© 2026 RAGIMOFF. All rights reserved.",
  "foot_note": "The address of professional reputation.",
  "prose_note": "Prices and program terms may change — please confirm current details.",
},
}

PROGRAMS = [
  ("Ümumi Psixologiya", "Rəsmi Əlavə Təhsil diplomu. Psixoloq kimi hüquqi fəaliyyətin başlanğıcı.", "1 il — 6+6 ay", "4 200 ₼", "3 800 ₼", "200 ₼/ay", False),
  ("Klinik Psixologiya", "Mürəkkəb klinik hallar, öz mərkəziniz üçün tam hüquqi status. IPAS sertifikatı.", "1 il — 6+6 ay", "6 600 ₼", "6 000 ₼", "300 ₼/ay", True),
  ("Psixoterapiya Praktikumu", "Psixoloq + pasiyent rollarında canlı məşqlər, real keyslərin superviziyası.", "1 il — praktika", "3 600 ₼", "3 000 ₼", "175 ₼/ay", False),
  ("Ailə Terapiyası", "Cütlük terapiyası və valideyn-övlad münasibətləri. 3 ay + 6 ay superviziya.", "3 ay + 6 ay", "900 ₼", "800 ₼", "300 ₼/ay", False),
  ("Psixoanaliz", "3 aylıq nəzəri təlim və 6 aylıq superviziya. Tədrisçi — Kənan Rəhimov.", "3 ay + 6 ay", "900 ₼", "800 ₼", "300 ₼/ay", False),
  ("Psixodiaqnostika", "ÜST və ICD standartları üzrə diaqnozun əsaslandırılması.", "3 ay + 6 ay", "900 ₼", "800 ₼", "300 ₼/ay", False),
]

PROGRAMS_RU = [
  ("Общая психология", "Официальный диплом ДПО. Начало легальной практики психолога.", "1 год — 6+6 мес.", "4 200 ₼", "3 800 ₼", "200 ₼/мес.", False),
  ("Клиническая психология", "Сложные клинические случаи, полный правовой статус для своего центра. Сертификат IPAS.", "1 год — 6+6 мес.", "6 600 ₼", "6 000 ₼", "300 ₼/мес.", True),
  ("Практикум психотерапии", "Живые упражнения в ролях психолога и пациента, супервизия реальных кейсов.", "1 год — практика", "3 600 ₼", "3 000 ₼", "175 ₼/мес.", False),
  ("Семейная терапия", "Парная терапия и детско-родительские отношения. 3 мес. + 6 мес. супервизии.", "3 мес. + 6 мес.", "900 ₼", "800 ₼", "300 ₼/мес.", False),
  ("Психоанализ", "3 месяца теории и 6 месяцев супервизии. Преподаёт Кенан Рагимов.", "3 мес. + 6 мес.", "900 ₼", "800 ₼", "300 ₼/мес.", False),
  ("Психодиагностика", "Обоснование диагноза по стандартам ВОЗ и ICD.", "3 мес. + 6 мес.", "900 ₼", "800 ₼", "300 ₼/мес.", False),
]

PROGRAMS_EN = [
  ("General Psychology", "Official CPD diploma. The start of lawful psychological practice.", "1 year — 6+6 months", "4 200 ₼", "3 800 ₼", "200 ₼/mo", False),
  ("Clinical Psychology", "Complex clinical cases, full legal status for your own centre. IPAS certificate.", "1 year — 6+6 months", "6 600 ₼", "6 000 ₼", "300 ₼/mo", True),
  ("Psychotherapy Practicum", "Live exercises as psychologist and patient, supervision of real cases.", "1 year — practice", "3 600 ₼", "3 000 ₼", "175 ₼/mo", False),
  ("Family Therapy", "Couples therapy and parent-child relationships. 3 months + 6 months supervision.", "3 mo + 6 mo", "900 ₼", "800 ₼", "300 ₼/mo", False),
  ("Psychoanalysis", "3 months of theory and 6 months of supervision. Taught by Kenan Ragimov.", "3 mo + 6 mo", "900 ₼", "800 ₼", "300 ₼/mo", False),
  ("Psychodiagnostics", "Justifying diagnosis under WHO and ICD standards.", "3 mo + 6 mo", "900 ₼", "800 ₼", "300 ₼/mo", False),
]

PROG_BY_LANG = {"az": PROGRAMS, "ru": PROGRAMS_RU, "en": PROGRAMS_EN}


def esc(s):
    return html.escape(str(s), quote=True)


def header(t, lang):
    nav = "".join(
        f'<a href="{h}">{esc(n)}</a>'
        for n, h in zip(t["nav"], t["nav_href"])
    )
    langs = "".join(
        f'<a href="../{l}/index.html" class="{"is-on" if l == lang else ""}" lang="{l}">{l.upper()}</a>'
        for l in LANGS
    )
    mob_langs = "".join(
        f'<a href="../{l}/index.html" class="{"is-on" if l == lang else ""}" lang="{l}">{l.upper()}</a>'
        for l in LANGS
    )
    mob_nav = "".join(f'<a class="mob__big" href="{h}">{esc(n)}</a>' for n, h in zip(t["nav"], t["nav_href"]))
    return f"""
<header class="head" data-head>
  <div class="head__in">
    <a class="logo" href="index.html" aria-label="RAGIMOFF">
      <span class="logo__mark">R.</span><span>RAGIMOFF</span>
    </a>
    <nav class="nav" aria-label="Main">{nav}</nav>
    <div class="head__right">
      <div class="langs" aria-label="Language">{langs}</div>
      <button class="icon-btn" type="button" data-theme-toggle aria-label="Theme">
        <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M21 12.8A9 9 0 1 1 11.2 3 7 7 0 0 0 21 12.8z"/></svg>
      </button>
      <a class="btn btn--primary btn--sm" href="{t['nav_href'][5]}">{esc(t['cta'])}</a>
      <button class="icon-btn burger" type="button" data-burger aria-label="Menu" aria-expanded="false">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
      </button>
    </div>
  </div>
</header>
<div class="mob" data-mob>
  <div class="mob__in">
    {mob_nav}
    <div class="mob__langs">{mob_langs}</div>
  </div>
</div>
"""


def hero(t):
    return f"""
<section class="hero" id="top">
  <div class="hero__bg" aria-hidden="true"></div>
  <div class="hero__grid" aria-hidden="true"></div>
  <div class="hero__glow" aria-hidden="true"></div>
  <div class="wrap hero__in">
    <div class="hero__copy reveal">
      <span class="badge badge--accent">{esc(t['hero_badge'])}</span>
      <h1>{t['hero_h1']}</h1>
      <p class="hero__sub">{esc(t['hero_sub'])}</p>
      <div class="hero__cta">
        <a class="btn btn--primary btn--lg" href="{t['nav_href'][2]}">{esc(t['hero_btn1'])}</a>
        <a class="btn btn--line btn--lg" href="{t['nav_href'][3]}">{esc(t['hero_btn2'])}</a>
      </div>
      <p class="hero__note">{esc(t['hero_note'])}</p>
    </div>
    <div class="hero__person reveal">
      <div class="hero__ring" aria-hidden="true"></div>
      <img src="/images/kenan/kenan-removebg-preview.png" alt="Kenan Ragimov" width="420" height="620" loading="eager">
      <div class="hero__badges">
        <span class="badge">IPAS</span><span class="badge">BAPPs</span><span class="badge">ADA</span>
      </div>
    </div>
  </div>
</section>
"""


def marquee(t):
    items = "".join(f"<span>{esc(x)}</span>" for x in t["marquee"])
    return f'<div class="marquee" aria-hidden="true"><div class="marquee__track">{items}{items}</div></div>'


def stats(t):
    items = "".join(
        f'<div class="stat reveal"><span class="stat__num">{esc(n)}</span><span class="stat__label">{esc(l)}</span></div>'
        for n, l in t["stats"]
    )
    return f'<section class="section section--tight"><div class="wrap"><div class="stats">{items}</div></div></section>'


def library(t):
    nums = "".join(
        f'<div class="stat"><span class="stat__num" style="font-size:clamp(26px,3vw,38px)">{esc(n)}</span><span class="stat__label">{esc(l)}</span></div>'
        for n, l in t["lib_nums"]
    )
    shelf = "".join(
        f'<img src="/books/covers/{f}" alt="" loading="lazy">'
        for f in ["freud.jpg", "klinik.jpg", "guilt.jpg", "pandemic.jpg", "phoenix.jpg", "freud-gw01.jpg", "freud-gw02.jpg", "freud-gw03.jpg"]
    )
    return f"""
<section class="section" id="library">
  <div class="wrap library">
    <div class="reveal">
      <span class="eyebrow">{esc(t['lib_eyebrow'])}</span>
      <h2 style="margin:var(--r1) 0">{esc(t['lib_h2'])}</h2>
      <p class="lead">{esc(t['lib_text'])}</p>
      <p style="font-size:13px;color:var(--text-faint);margin-top:var(--r1)">{esc(t['lib_note'])}</p>
      <a class="btn btn--primary" style="margin-top:var(--r2)" href="/books/">{esc(t['lib_btn'])}</a>
    </div>
    <div class="library__panel reveal">
      <div class="library__nums">{nums}</div>
      <div class="library__shelf">{shelf}</div>
    </div>
  </div>
</section>
"""


def textbook(t):
    meta = "".join(f'<span class="badge">{esc(x)}</span>' for x in t["tb_meta"])
    return f"""
<section class="section">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">{esc(t['tb_eyebrow'])}</span>
      <h2 style="margin:var(--r1) 0">{esc(t['tb_h2'])}</h2>
      <p class="lead">{esc(t['tb_text'])}</p>
      <div style="display:flex;flex-wrap:wrap;gap:8px;margin:var(--r2) 0">{meta}</div>
      <div style="display:flex;gap:10px;flex-wrap:wrap">
        <a class="btn btn--primary" href="/books/">{esc(t['tb_btn1'])}</a>
        <a class="btn btn--line" href="/books/">{esc(t['tb_btn2'])}</a>
      </div>
    </div>
    <div class="reveal" style="display:grid;place-items:center">
      <img src="/books/covers/klinik.jpg" alt="Clinical Psychiatry" style="width:min(100%,360px);border-radius:14px;box-shadow:var(--shadow)" loading="lazy">
    </div>
  </div>
</section>
"""


def film(t):
    return f"""
<section class="section" id="film">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">{esc(t['film_eyebrow'])}</span>
      <h2 style="margin:var(--r1) 0">{esc(t['film_h2'])}</h2>
      <p class="lead">{esc(t['film_text'])}</p>
      <a class="btn btn--line" style="margin-top:var(--r2)" href="https://youtu.be/rb68nHEF9-o" target="_blank" rel="noopener">{esc(t['film_btn'])}</a>
    </div>
    <div class="video reveal" data-video="rb68nHEF9-o" data-title="Sabina's Drama" role="button" tabindex="0">
      <img src="https://i.ytimg.com/vi/rb68nHEF9-o/maxresdefault.jpg" alt="" loading="lazy">
      <div class="video__play"><span>▶</span></div>
      <div class="video__cap">31:46 · 2013</div>
    </div>
  </div>
</section>
"""


def programs(t, lang):
    rows = ""
    for name, desc, dur, full, pre, month, featured in PROG_BY_LANG[lang]:
        cls = "program program--featured" if featured else "program"
        rows += f"""
    <article class="{cls} reveal">
      <h3 class="program__name">{esc(name)}</h3>
      <p class="program__desc">{esc(desc)}</p>
      <div class="program__rows">
        <div class="program__row"><span>{esc(t['prog_dur'])}</span><span>{esc(dur)}</span></div>
        <div class="program__row"><span>{esc(t['prog_price'])}</span><span>{esc(full)}</span></div>
        <div class="program__row"><span>{esc(t['prog_pre'])}</span><span>{esc(pre)}</span></div>
        <div class="program__row"><span>{esc(t['prog_month'])}</span><span>{esc(month)}</span></div>
      </div>
      <div class="program__price"><b>{esc(pre)}</b><small>{esc(t['prog_pre'])}</small></div>
      <div class="program__actions">
        <a class="btn btn--primary btn--sm" href="{t['nav_href'][5]}">{esc(t['prog_reg'])}</a>
        <a class="btn btn--line btn--sm" href="{t['nav_href'][2]}">{esc(t['prog_more'])}</a>
      </div>
    </article>"""
    return f"""
<section class="section" id="programs">
  <div class="wrap">
    <div class="sec-head reveal">
      <span class="eyebrow">{esc(t['prog_eyebrow'])}</span>
      <h2>{esc(t['prog_h2'])}</h2>
      <p class="lead">{esc(t['prog_lead'])}</p>
    </div>
    <div class="grid-3">{rows}</div>
  </div>
</section>
"""


def timeline(t):
    items = "".join(
        f'<div class="timeline__item reveal"><span class="timeline__year">{esc(y)}</span><p class="timeline__text">{esc(x)}</p></div>'
        for y, x in t["timeline"]
    )
    return f"""
<section class="section" id="dossier">
  <div class="wrap split" style="align-items:start">
    <div class="reveal">
      <span class="eyebrow">{esc(t['timeline_eyebrow'])}</span>
      <h2 style="margin:var(--r1) 0">{esc(t['timeline_h2'])}</h2>
      <p class="lead">{esc(t['hero_note'])}</p>
      <a class="btn btn--line" style="margin-top:var(--r2)" href="https://intpas.com/student/13iu21e3az001/" target="_blank" rel="noopener">{esc(t['ipas_qr'])} ↗</a>
    </div>
    <div class="timeline">{items}</div>
  </div>
</section>
"""


def myths(t):
    cards = "".join(
        f"""<details class="myth reveal">
      <summary data-label="{esc(t['myth_label'])}">{esc(q)}</summary>
      <div class="myth__body">
        <p class="myth__fact"><b>{esc(t['myth_fact'])}</b> {esc(a)}</p>
        <p class="myth__src">{esc(src)}</p>
      </div>
    </details>"""
        for q, a, src in t["myths"]
    )
    return f"""
<section class="section" id="myths">
  <div class="wrap">
    <div class="sec-head reveal">
      <span class="eyebrow">{esc(t['myth_eyebrow'])}</span>
      <h2>{esc(t['myth_h2'])}</h2>
      <p class="lead">{esc(t['myth_lead'])}</p>
    </div>
    <div class="grid-3" style="align-items:start">{cards}</div>
  </div>
</section>
"""


def consultations(t):
    cards = "".join(
        f"""<article class="card reveal">
      <span class="badge badge--accent">{esc(k)}</span>
      <h3 class="card__title">{esc(who)}</h3>
      <p class="card__text">{esc(what)}</p>
      <div class="card__actions"><a class="btn btn--line btn--sm" href="{t['nav_href'][3]}">{esc(t['cons_btn'])}</a></div>
    </article>"""
        for k, who, what in t["cons"]
    )
    return f"""
<section class="section" id="consultations">
  <div class="wrap">
    <div class="sec-head reveal">
      <span class="eyebrow">{esc(t['cons_eyebrow'])}</span>
      <h2>{esc(t['cons_h2'])}</h2>
      <p class="lead">{esc(t['cons_lead'])}</p>
    </div>
    <div class="grid-3">{cards}</div>
  </div>
</section>
"""


def books(t):
    cards = "".join(
        f"""<article class="book reveal">
      <div class="book__cover"><img src="{esc(img)}" alt="{esc(title)}" loading="lazy"></div>
      <h3 class="book__title">{esc(title)}</h3>
      <div class="book__meta"><span>{esc(meta)}</span><span>{esc(price)}</span></div>
      <div class="book__actions">
        <a class="btn btn--primary btn--sm" href="/books/">{esc(t['book_read'])}</a>
        <a class="btn btn--line btn--sm" href="/books/">{esc(t['book_order'])}</a>
      </div>
    </article>"""
        for title, meta, price, img in t["books"]
    )
    return f"""
<section class="section" id="books">
  <div class="wrap">
    <div class="sec-head reveal">
      <span class="eyebrow">{esc(t['books_eyebrow'])}</span>
      <h2>{esc(t['books_h2'])}</h2>
    </div>
    <div class="grid-4">{cards}</div>
  </div>
</section>
"""


def business(t):
    nums = "".join(
        f'<div class="stat"><span class="stat__num" style="font-size:clamp(24px,2.6vw,34px)">{esc(n)}</span><span class="stat__label">{esc(l)}</span></div>'
        for n, l in t["biz_nums"]
    )
    return f"""
<section class="section" id="business">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">{esc(t['biz_eyebrow'])}</span>
      <h2 style="margin:var(--r1) 0">{esc(t['biz_h2'])}</h2>
      <p class="lead">{esc(t['biz_text'])}</p>
      <div class="library__nums" style="margin:var(--r2) 0">{nums}</div>
      <a class="btn btn--primary" href="/{t['html_lang']}/korporativ/index.html">{esc(t['biz_btn'])}</a>
    </div>
    <div class="video reveal" data-video="1JMEVec4F1c" data-title="Unibank Team Building" role="button" tabindex="0">
      <img src="https://i.ytimg.com/vi/1JMEVec4F1c/maxresdefault.jpg" alt="" loading="lazy">
      <div class="video__play"><span>▶</span></div>
      <div class="video__cap">Unibank · Team Building · 2013</div>
    </div>
  </div>
</section>
"""


def events(t):
    cards = "".join(
        f'<article class="event reveal"><span class="event__year">{esc(y)}</span><span class="event__place">{esc(place)}</span><span class="event__theme">{esc(theme)}</span></article>'
        for y, place, theme in t["events"]
    )
    return f"""
<section class="section" id="events">
  <div class="wrap">
    <div class="sec-head reveal">
      <span class="eyebrow">{esc(t['events_eyebrow'])}</span>
      <h2>{esc(t['events_h2'])}</h2>
    </div>
    <div class="grid-3">{cards}</div>
    <div class="grid-3" style="margin-top:var(--r2)">
      <a class="video reveal" href="https://youtu.be/HDSnAVA1-tw" target="_blank" rel="noopener">
        <img src="https://i.ytimg.com/vi/HDSnAVA1-tw/maxresdefault.jpg" alt="" loading="lazy">
        <div class="video__play"><span>▶</span></div><div class="video__cap">JW Marriott · 2015</div>
      </a>
      <a class="video reveal" href="https://youtu.be/kEk6B3kNEoE" target="_blank" rel="noopener">
        <img src="https://i.ytimg.com/vi/kEk6B3kNEoE/maxresdefault.jpg" alt="" loading="lazy">
        <div class="video__play"><span>▶</span></div><div class="video__cap">Kempinski · 2015</div>
      </a>
      <a class="video reveal" href="https://youtu.be/06Qm8uzTwvs" target="_blank" rel="noopener">
        <img src="https://i.ytimg.com/vi/06Qm8uzTwvs/maxresdefault.jpg" alt="" loading="lazy">
        <div class="video__play"><span>▶</span></div><div class="video__cap">Flame Towers · 2016</div>
      </a>
    </div>
  </div>
</section>
"""


def telegram(t):
    return f"""
<section class="section" id="telegram">
  <div class="wrap">
    <div class="tg reveal">
      <div>
        <h2 style="font-size:var(--step-4)">{esc(t['tg_h2'])}</h2>
        <p class="lead" style="margin-top:8px">{esc(t['tg_text'])}</p>
      </div>
      <div class="tg__links">
        <a class="tg__link" href="https://t.me/ragimoff" target="_blank" rel="noopener">✈ {esc(t['tg_az'])}</a>
        <a class="tg__link" href="https://t.me/doctor_ragimoff" target="_blank" rel="noopener">✈ {esc(t['tg_ru'])}</a>
      </div>
    </div>
  </div>
</section>
"""


def blog(t):
    cards = "".join(
        f"""<article class="card reveal">
      <a href="{esc(href)}" style="display:block;border-radius:var(--radius-sm);overflow:hidden;aspect-ratio:16/9">
        <img src="{esc(img)}" alt="" style="width:100%;height:100%;object-fit:cover" loading="lazy">
      </a>
      <span class="badge">{esc(cat)}</span>
      <h3 class="card__title" style="font-size:var(--step-2)">{esc(title)}</h3>
      <p class="card__text">{esc(desc)}</p>
      <div class="card__actions"><a class="btn btn--ghost" href="{esc(href)}">{esc(t['blog_read'])} →</a></div>
    </article>"""
        for cat, title, desc, href, img in t["blog"]
    )
    return f"""
<section class="section" id="blog">
  <div class="wrap">
    <div class="sec-head reveal">
      <span class="eyebrow">{esc(t['blog_eyebrow'])}</span>
      <h2>{esc(t['blog_h2'])}</h2>
    </div>
    <div class="grid-3">{cards}</div>
  </div>
</section>
"""


def footer(t, lang):
    cols = ""
    for title, links in t["foot_cols"]:
        items = "".join(f"<li><a href=\"{'tel:+994702200376' if l.startswith('+994') else ('mailto:'+l if '@' in l else t['nav_href'][5])}\">{esc(l)}</a></li>" for l in links)
        cols += f'<div><h4>{esc(title)}</h4><ul>{items}</ul></div>'
    return f"""
<footer class="foot">
  <div class="wrap">
    <div class="foot__grid">
      <div class="foot__brand">
        <div class="foot__word">RAGIMOFF.</div>
        <p class="foot__desc">{esc(t['foot_desc'])}</p>
        <p style="font-size:12px;color:var(--text-faint)">{esc(t['foot_note'])}</p>
      </div>
      {cols}
    </div>
    <div class="foot__bottom">
      <span>{esc(t['foot_rights'])}</span>
      <span>{esc(t['prose_note'])}</span>
    </div>
  </div>
</footer>
<a class="wa" href="https://wa.me/994702200376" target="_blank" rel="noopener" aria-label="WhatsApp">WA</a>
"""


def page(lang):
    t = TEXTS[lang]
    alt = "".join(
        f'<link rel="alternate" hreflang="{l}" href="{SITE}{BASE}/{l}/">' for l in LANGS
    )
    return f"""<!DOCTYPE html>
<html lang="{t['html_lang']}" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RAGIMOFF — {esc(t['hero_h1'].replace('<br>',' ').replace('<em>','').replace('</em>',''))}</title>
<meta name="description" content="{esc(t['hero_sub'])}">
<link rel="canonical" href="{SITE}{BASE}/{lang}/">
{alt}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Manrope:wght@400;500;600;700&family=Alegreya:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{BASE}/assets/css/tokens.css">
<link rel="stylesheet" href="{BASE}/assets/css/base.css">
<link rel="stylesheet" href="{BASE}/assets/css/components.css">
<link rel="stylesheet" href="{BASE}/assets/css/patterns.css">
<script defer src="{BASE}/assets/js/main.js"></script>
</head>
<body>
<a class="sr-only" href="#main">Skip to content</a>
{header(t, lang)}
<main id="main">
{hero(t)}
{marquee(t)}
{stats(t)}
{library(t)}
{textbook(t)}
{film(t)}
{programs(t, lang)}
{timeline(t)}
{myths(t)}
{consultations(t)}
{books(t)}
{business(t)}
{events(t)}
{telegram(t)}
{blog(t)}
</main>
{footer(t, lang)}
</body>
</html>
"""


def main():
    for lang in LANGS:
        d = OUT / lang
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(page(lang), encoding="utf-8")
        print("built", d / "index.html")
    # root redirect
    (OUT / "index.html").write_text(
        """<!DOCTYPE html><html lang="az"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>RAGIMOFF</title>
<script>location.replace('az/index.html')</script>
</head><body><a href="az/index.html">AZ</a> · <a href="ru/index.html">RU</a> · <a href="en/index.html">EN</a></body></html>""",
        encoding="utf-8",
    )
    print("built", OUT / "index.html")


if __name__ == "__main__":
    main()
