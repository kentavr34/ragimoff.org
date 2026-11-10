#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RAGIMOFF /67 — генератор главной по новой дизайн-системе.
Контент отделён от шаблона: TEXTS + DATA -> HTML.
Запуск: python build.py
"""
import html
import pathlib

OUT = pathlib.Path(__file__).resolve().parents[1]
BASE = "/68"
SITE = "https://ragimoff.org"

LANGS = ["az", "ru", "en"]

TEXTS = {
"az": {
  "lang_name": "AZ", "html_lang": "az",
  "nav": ["Mütəxəssislər", "Kitablar", "Təhsil", "Konsultasiya", "Bloq", "Əlaqə"],
  "nav_href": ["/az/mutexessisler/index.html", "/books/", "/az/telim/index.html", "/az/konsultasiya/index.html", "/az/bloq/index.html", "/az/elaqe/index.html"],
  "cta": "Qeydiyyat",
  "hero_badge": "IPAS Ambassador · BAPPs · ADA",
  "hero_query": "Doctor Ragimoff",
  "hero_strong": "Psixologiya Məktəbi",
  "hero_h1": "Psixologiya<br><em>Məktəbi</em>",
  "hero_sub": "İyirmi üç ildir klinik praktikadayam. Rəsmi diplom, beynəlxalq sertifikat — və bütün bunlar Azərbaycan dilində.",
  "hero_btn1": "Təhsil proqramları",
  "hero_btn2": "Konsultasiya",
  "hero_note": "Kənan Rəhimov — klinik psixoloq, psixoterapevt, IPAS ambassadoru",
  "spec_eyebrow": "Mütəxəssislər",
  "spec_h2": "İki mütəxəssis, bir məktəb",
  "spec_lead": "Biri klinik psixiatriya dərsliyinin müəllifidir, digəri ailə terapiyası modullarını aparır. Eyni məktəbin iki fərqli baxışı — buna görə mürəkkəb hallarda ikinci rəy almaq mümkündür.",
  "spec_more": "Ətraflı",
  "spec": [
    ("Kənan Rəhimov", "Klinik psixoloq, psixoterapevt, IPAS ambassadoru",
     "RAGIMOFF Psixologiya Məktəbinin təsiscisi, «Klinik Psixiatriya» sorğu kitabının müəllifi. 23 il klinik təcrübə, 2008-dən HR Məktəbinin rəhbəri.",
     "/images/kenan/kenan-removebg-preview.png", "/az/mutexessisler/kenan-rehimov.html"),
    ("Samirə Rəhimova", "Ailə terapevti",
     "Cütlüklər, valideyn və uşaq əlaqəsi, çətin yeniyetmələr. Ailə terapiyası modullarını aparır.",
     "/images/samira/samira-portret.jpg", "/az/mutexessisler/samire-rehimova.html"),
  ],
  "ment_eyebrow": "Formalaşma",
  "ment_h2": "Kimin məktəbini keçib",
  "ment_lead": "2001–2003-cü illər, Sankt-Peterburq, V.M. Bexterev adına Psixonevrologiya İnstitutu. Qırmızı diplom — və dərslikləri bu gün də Rusiyada və ondan kənarda psixoterapevt hazırlayan iki insan.",
  "ment": [
    ("Viktor Davidoviç Vida", "2001–2002", "Tibb elmləri doktoru, professor, V.M. Bexterev adına Psixiatriya və Nevrologiya Milli Tədqiqat Mərkəzinin baş elmi işçisi. Rusiyada ilk diplomlu psixoanalitik — Alman Psixoanaliz Akademiyası, Berlin və Münhen. «Şizofreniyanın psixoterapiyası» monoqrafiyasının müəllifi. Psixoanalitik hazırlığa rəhbərlik edib."),
    ("Boris Dmitriyeviç Karvasarski", "2001–2003", "Tibb elmləri doktoru, professor, RF əməkdar elm xadimi. Rusiya Federasiyası Səhiyyə Nazirliyinin baş psixoterapevti, Leninqrad psixoterapiya məktəbinin yaradıcısı. «Psixoterapiya» dərsliyinin və «Psixoterapevtik ensiklopediya»nın baş redaktoru, 215 elmi işin müəllifi. Psixoterapiya üzrə hazırlığa rəhbərlik edib."),
  ],
  "ment_note": "Karvasarskinin rəhbərliyi altında 100-dən çox namizədlik və 27 doktorluq dissertasiyası müdafiə olunub. Hər iki rəhbərin dərslikləri bu gün də psixoterapevt hazırlığının əsasını təşkil edir.",
  "freud_eyebrow": "İlk dəfə Azərbaycanda",
  "freud_h2": "Freyd — doğma dilinizdə",
  "freud_lead": "Alman orijinalından tərcümə edilib: əsərlər, mühazirələr, məktublar, klinik qeydlər. Təkrar nəşrlər deyil — mətnlərin özü.",
  "freud_text": "Oxumaq üçün heç nə yükləmək lazım deyil: brauzerdə açılır, axtarış işləyir, oxuduğunuz yer yadda qalır. Tələbələrə ən çox çatışmayan şey məhz bu idi — fundamental mətnlər olmadan peşəkar təhsil mümkün deyil.",
  "freud_btn": "Kitabxanaya keç",
  "own_eyebrow": "Müəllif kitabları",
  "own_h2": "Hər kitab — bir istiqamətin sübutu",
  "own_lead": "Dörd kitab və dörd istiqamət. Hər biri universitet dərsliyi səviyyəsində yazılıb; bu gün onların analoqu yoxdur.",
  "own_note": "Üç dildə nəşr olunub, «Klinik Psixiatriya» həm də türk dilindədir. Dillərin sayı artmaqda davam edir.",
  "own": [
    ("Klinik Psixiatriya", "Əlavə peşə təhsili · Psixoterapiya praktikumu · Psixodiaqnostika", "/books/covers/klinik.jpg"),
    ("Feniks erası", "Ailə terapiyası · Münasibətlər", "/books/covers/phoenix.jpg"),
    ("Günahkarlıq virusu", "Maarifləndirmə · Koqnitiv terapiya — yalançı qənaətlə qarşı mübarizə", "/books/covers/guilt.jpg"),
    ("Şizofreniya. Cinnət pandemiyası", "Maarifləndirmə · Klinik psixiatriya", "/books/covers/pandemic.jpg"),
  ],
  "tb2_eyebrow": "Hazırlanır",
  "tb2_h2": "«Ümumi psixoterapiya»",
  "tb2_text": "Rus dilində cild artıq hazırdır, azərbaycan dilində versiyası hazırlanır. Psixoterapevt hazırlığının əsas kursu — bir cilddə.",
  "tb2_note": "Kitab çıxan kimi kitabxanada açılacaq.",
  "case_eyebrow": "Təcrübədən",
  "case_h2": "«Səbinənin draması»",
  "case_lead": "Real terapiya işinin ekranlaşdırılması. Şərhsiz, müdaxiləsiz — yalnız iş gedir.",
  "case_text": "31 dəqiqə. Peşəkar auditoriya və tələbələr üçün açıqdır.",
  "marquee": ["Rəsmi Əlavə Təhsil diplomu", "IPAS sertifikatı", "Klinik psixologiya", "Psixoterapiya praktikumu", "Psixoanaliz", "Psixodiaqnostika", "Ailə terapiyası", "Korporativ təlimlər"],
  "stats": [("23+", "il klinik təcrübə"), ("3000+", "pasient"), ("2000+", "HR məzunu"), ("11", "beynəlxalq sertifikat")],
  "lib_eyebrow": "Açıq kitabxana",
  "lib_h2": "Freyd azərbaycan dilində. İlk dəfə. Pulsuz.",
  "lib_text": "Ziqmund Freydin 24 kitabı orijinal alman dilindən azərbaycan dilinə tərcümə edilib. Tələbə, praktik və ya sadəcə oxucu — hamı üçün açıqdır. Onlayn oxuyun, yükləyin, lazım olsa çap versiyasını sifariş edin.",
  "lib_nums": [("24", "Freyd kitabı"), ("4", "dil"), ("0 ₼", "oxumaq üçün")],
  "lib_btn": "Kitabxananı aç",
  "lib_note": "Bütün kolleksiya: 94 cild — Freyd, Kənan Rəhimov, Samirə Rəhimova.",
  "tb_eyebrow": "Əsas əsər",
  "tb_h2": "«Klinik Psixiatriya» — dünyada analoqu olmayan dərslik",
  "tb_text": "820 səhifə (B5 çap), DSM-5 və ICD-11, beynəlxalq protokollar və konsensus. Bu gün dünyada belə bir dərslik yoxdur: həm klinik həkim, həm tələbə, həm də psixoterapiya metodunu seçən oxucu üçün eyni dərəcədə işləkdir. Dörd dilə çevrilib — azərbaycan, rus, ingilis və türk. Azərbaycan dilində rəsmi dərslikdir və hamı üçün açıqdır. Ayrıca vəzifəsi var: elmi olmayan fikirləri və mifləri ayırmaq, düzgün müalicədən yayındıran yanlış təsəvvürləri aradan qaldırmaq.",
  "tb_meta": ["820 səhifə · B5", "4 dil", "DSM-5 · ICD-11", "Pulsuz oxu"],
  "tb_btn1": "Aç və bax",
  "tb_btn2": "Çap versiyası",
  "film_eyebrow": "Təcrübədən",
  "film_h2": "«Səbinənin draması»",
  "film_text": "Real hadisənin ekranlaşdırılması. 31 dəqiqə. Şərhsiz.",
  "film_btn": "İzlə",
  "prog_eyebrow": "Təhsil",
  "prog_g_dpo": "Diplomlu əlavə peşə təhsili",
  "prog_g_spec": "Praktikum və ixtisaslaşmalar",
  "prog_h2": "Altı tədris proqramı",
  "prog_lead": "Rəsmi nümunəli diplom, canlı praktika və beynəlxalq sertifikat. Müddətlər və qiymətlər «zəng edib dəqiqləşdirin» demədən açıq göstərilib.",
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
  "myth_lead": "Hər izah mənbəyə istinadla verilir. Özünüz yoxlayın: dərsliyi açın və göstərilən bölməni oxuyun.",
  "myth_label": "MİF", "myth_fact": "Fakt:",
  "myths": [
    ("Depressiya", "«Depressiya sadəcə pis əhvaldır, özü keçər»", "Əslində: depressiya diaqnoz qoyulan xəstəlikdir — beyin kimyası, yuxu, iştaha və iş qabiliyyəti dəyişir. Orta hesabla 6–8 ay davam edir və müalicəsiz təkrarlanır. Psixoterapiya və dərman eyni dərəcədə sübut edilmiş üsuldur.", "Mənbə: «Klinik Psixiatriya», depressiya bölməsi", "#textbook", "Kitaba bax →"),
    ("Sosial fobiya", "«Bu sadəcə utancaqlıqdır, özünü ələ al»", "Əslində: sosial fobiya utancaqlıq deyil — insan danışmaqdan, yeməkdən, telefonla danışmaqdan çəkinir, bədən reaksiyaları başlayır və həyat daralır. KBT ilə nəticə ölçülür: simptomlar azalır, yox olmasa da idarə olunur.", "Mənbə: «Klinik Psixiatriya» + «Virus günahı»", "#ownbooks", "Virus günahına bax →"),
    ("Gecə enurezi", "«Uşaq tənbəldir, qəsdən edir»", "Əslində: gecə enurezi uşağın iradəsindən asılı deyil — yetkinləşmə, irsiyyət və yuxu dövrləri iştirak edir. Cəza vəziyyəti ağırlaşdırır. Sübut edilmiş yol: rejim, siqnal aparatı, davranış terapiyası.", "Mənbə: «Klinik Psixiatriya», enurez bölməsi", "#textbook", "Kitaba bax →"),
    ("Panik atak", "«Panik atak ürək tutmasıdır, ölürəm»", "Əslində: panik atak təhlükəli deyil, ölümlə nəticələnmir. Döyüntü, boğulma və ölüm qorxusu adrenalin dalğasıdır və 10–20 dəqiqədə səngəyir. Əsas zərər — qaçma davranışı və gözləmə qorxusudur, terapiya məhz onu hədəfləyir.", "Mənbə: «Klinik Psixiatriya», anksiyete pozuntuları", "#textbook", "Kitaba bax →"),
    ("Psixoterapiya", "«Söhbət etmək xəstəliyi müalicə etmir»", "Əslində: psixoterapiyanın effektivliyi yüzlərlə randomizə edilmiş tədqiqatda ölçülüb və dərman müalicəsi ilə müqayisə edilir. Əsas şərt — protokola uyğun aparılması və effektin ölçülməsi.", "Mənbə: beynəlxalq protokollar və konsensus", "#programs", "Proqramlara bax →"),
  ],
  "cons_eyebrow": "Konsultasiya",
  "cons_h2": "Üç format, bir məqsəd",
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
    ("Klinik Psixiatriya", "820 səh. (B5), 4 dil", "28 ₼", "/books/covers/klinik.jpg"),
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
  "foot_note": "Təhsili öz dərsliklərinə və mənbə mətnlərə söykənən məktəb.",
  "prose_note": "Qiymətlər və proqram şərtləri dəyişməz deyil — aktual məlumat üçün əlaqə saxlayın.",
},
"ru": {
  "lang_name": "RU", "html_lang": "ru",
  "nav": ["Специалисты", "Книги", "Обучение", "Консультации", "Блог", "Контакты"],
  "nav_href": ["/ru/mutexessisler/index.html", "/books/", "/ru/telim/index.html", "/ru/konsultasiya/index.html", "/ru/bloq/index.html", "/ru/elaqe/index.html"],
  "cta": "Записаться",
  "hero_badge": "IPAS Ambassador · BAPPs · ADA",
  "hero_query": "Doctor Ragimoff",
  "hero_strong": "Школа психологии",
  "hero_h1": "Школа<br><em>психологии</em>",
  "hero_sub": "Двадцать три года в клинической практике. Официальный диплом, международный сертификат — и всё это на азербайджанском языке.",
  "hero_btn1": "Программы обучения",
  "hero_btn2": "Консультация",
  "hero_note": "Кенан Рагимов — клинический психолог, психотерапевт, амбассадор IPAS",
  "spec_eyebrow": "Специалисты",
  "spec_h2": "Двое специалистов, одна школа",
  "spec_lead": "Один — автор учебника по клинической психиатрии, вторая ведёт модули семейной терапии. Две линии одной школы — поэтому в сложных случаях можно получить второе мнение.",
  "spec_more": "Подробнее",
  "spec": [
    ("Кенан Рагимов", "Клинический психолог, психотерапевт, амбассадор IPAS",
     "Основатель Школы психологии RAGIMOFF, автор справочника «Клиническая психиатрия». 23 года клинической практики, с 2008 года руководит Школой HR.",
     "/images/kenan/kenan-removebg-preview.png", "/ru/mutexessisler/kenan-rehimov.html"),
    ("Самира Рагимова", "Семейный терапевт",
     "Пары, связь родителя с ребёнком, трудные подростки. Ведёт модули семейной терапии.",
     "/images/samira/samira-portret.jpg", "/ru/mutexessisler/samire-rehimova.html"),
  ],
  "ment_eyebrow": "Становление",
  "ment_h2": "У кого прошёл школу",
  "ment_lead": "2001–2003 годы, Санкт-Петербург, Институт психоневрологии имени В. М. Бехтерева. Красный диплом — и два человека, чьи учебники до сих пор готовят психотерапевтов в России и за её пределами.",
  "ment": [
    ("Виктор Давыдович Вида", "2001–2002", "Доктор медицинских наук, профессор, главный научный сотрудник НМИЦ психиатрии и неврологии имени В. М. Бехтерева. Первый в России дипломированный психоаналитик — Немецкая академия психоанализа, Берлин и Мюнхен. Автор монографии «Психотерапия шизофрении». Руководил психоаналитической подготовкой."),
    ("Борис Дмитриевич Карвасарский", "2001–2003", "Доктор медицинских наук, профессор, заслуженный деятель науки РФ. Главный психотерапевт Министерства здравоохранения Российской Федерации, создатель Ленинградской школы психотерапии. Главный редактор учебника «Психотерапия» и «Психотерапевтической энциклопедии», автор 215 научных работ. Руководил подготовкой по психотерапии."),
  ],
  "ment_note": "Под руководством Карвасарского защищено более 100 кандидатских и 27 докторских диссертаций. Оба руководителя — авторы учебников, по которым учатся психотерапевты до сих пор.",
  "freud_eyebrow": "Впервые в Азербайджане",
  "freud_h2": "Фрейд — на родном языке",
  "freud_lead": "Переведено с немецкого оригинала: труды, лекции, переписка, клинические записи. Не пересказы и не хрестоматии — сами тексты.",
  "freud_text": "Читать можно прямо в браузере: ничего не нужно скачивать, поиск работает, место чтения сохраняется. Это то, чего студентам не хватало больше всего — без фундаментальных текстов профессиональное образование невозможно.",
  "freud_btn": "Перейти в библиотеку",
  "own_eyebrow": "Книги автора",
  "own_h2": "Каждая книга — доказательство направления",
  "own_lead": "Четыре книги и четыре направления. Каждая написана на уровне университетского учебника; на сегодня аналогов в мире нет.",
  "own_note": "Изданы на трёх языках, «Клиническая психиатрия» — ещё и на турецком. Список языков продолжает расти.",
  "own": [
    ("Клиническая психиатрия", "ДПО · Практикум по психотерапии · Психодиагностика", "/books/covers/klinik.jpg"),
    ("Эра Феникса", "Семейная терапия · Взаимоотношения", "/books/covers/phoenix.jpg"),
    ("Вирус вины", "Просвещение · Когнитивная терапия — борьба с ложными установками", "/books/covers/guilt.jpg"),
    ("Шизофрения. Пандемия безумия", "Просвещение · Клиническая психиатрия", "/books/covers/pandemic.jpg"),
  ],
  "tb2_eyebrow": "Готовится",
  "tb2_h2": "«Общая психотерапия»",
  "tb2_text": "Том на русском языке уже собран; азербайджанское издание готовится. Базовый курс подготовки психотерапевта уложен в один том.",
  "tb2_note": "Как только книга выйдет, она откроется в библиотеке — там же, где Фрейд.",
  "case_eyebrow": "Из практики",
  "case_h2": "«Драма Сабины»",
  "case_lead": "Экранизация настоящей терапевтической работы. Без комментариев и монтажных подсказок — на экране идёт только работа.",
  "case_text": "31 минута. Открыто для профессиональной аудитории и студентов.",
  "marquee": ["Официальный диплом ДПО", "Сертификат IPAS", "Клиническая психология", "Практикум психотерапии", "Психоанализ", "Психодиагностика", "Семейная терапия", "Корпоративные тренинги"],
  "stats": [("23+", "года практики"), ("3000+", "пациентов"), ("2000+", "выпускников HR"), ("11", "международных сертификатов")],
  "lib_eyebrow": "Открытая библиотека",
  "lib_h2": "Фрейд на азербайджанском. Впервые. Бесплатно.",
  "lib_text": "24 книги Зигмунда Фрейда переведены с немецкого оригинала на азербайджанский. Для студента, практика и просто читателя. Читайте онлайн, скачивайте, при желании закажите печатное издание.",
  "lib_nums": [("24", "книги Фрейда"), ("4", "языка"), ("0 ₼", "за чтение")],
  "lib_btn": "Открыть библиотеку",
  "lib_note": "Вся коллекция: 94 тома — Фрейд, Кенан Рагимов, Самира Рагимова.",
  "tb_eyebrow": "Главный труд",
  "tb_h2": "«Клиническая психиатрия» — учебник без аналогов в мире",
  "tb_text": "820 страниц в печати (формат B5), DSM-5 и ICD-11, международные протоколы и консенсус. Такого учебника сегодня в мире нет: он одинаково рабочий и для клинициста, и для студента, и для того, кто выбирает метод терапии. Переведён на четыре языка — азербайджанский, русский, английский и турецкий. В азербайджанском это официальный учебник, и он открыт каждому. У него есть отдельная задача: отделять научное от ненаучного и снимать мифы и заблуждения, которые уводят от правильного лечения.",
  "tb_meta": ["820 страниц · B5", "4 языка", "DSM-5 · ICD-11", "Читать бесплатно"],
  "tb_btn1": "Открыть и посмотреть",
  "tb_btn2": "Печатная версия",
  "film_eyebrow": "Из практики",
  "film_h2": "«Драма Сабины»",
  "film_text": "Экранизация реального случая. 31 минута. Без комментариев.",
  "film_btn": "Смотреть",
  "prog_eyebrow": "Обучение",
  "prog_g_dpo": "ДПО с дипломом",
  "prog_g_spec": "Практикум и специализации",
  "prog_h2": "Шесть программ обучения",
  "prog_lead": "Диплом установленного образца, живая практика и международный сертификат. Сроки и цены указаны без «уточняйте по телефону».",
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
  "myth_lead": "Каждый разбор — со ссылкой на источник. Проверьте сами: возьмите учебник и откройте названный раздел.",
  "myth_label": "МИФ", "myth_fact": "Факт:",
  "myths": [
    ("Депрессия", "«Депрессия — это просто плохое настроение, само пройдёт»", "На самом деле: депрессия — диагностируемое заболевание, меняются биохимия мозга, сон, аппетит и работоспособность. В среднем длится 6–8 месяцев и без лечения повторяется. Психотерапия и медикаменты — равно доказанные методы.", "Источник: «Клиническая психиатрия», раздел о депрессии", "#textbook", "Посмотреть в книге →"),
    ("Социальная фобия", "«Это просто стеснительность, возьми себя в руки»", "На самом деле: социальная фобия — не стеснительность. Человек избегает говорить, есть, звонить, включаются телесные реакции, жизнь сужается. Эффект КПТ измерим: симптомы снижаются и становятся управляемыми.", "Источник: «Клиническая психиатрия» + «Вирус вины»", "#ownbooks", "Посмотреть «Вирус вины» →"),
    ("Ночной энурез", "«Ребёнок ленится, делает это назло»", "На самом деле: ночной энурез не зависит от воли ребёнка — участвуют созревание, наследственность и фазы сна. Наказание ухудшает состояние. Доказанный путь: режим, сигнальный аппарат, поведенческая терапия.", "Источник: «Клиническая психиатрия», раздел об энурезе", "#textbook", "Посмотреть в книге →"),
    ("Паническая атака", "«Паническая атака — это инфаркт, я умираю»", "На самом деле: паническая атака не опасна и не приводит к смерти. Сердцебиение, нехватка воздуха и страх смерти — это волна адреналина, она стихает за 10–20 минут. Главный вред — избегание и страх ожидания; именно их и снимает терапия.", "Источник: «Клиническая психиатрия», тревожные расстройства", "#textbook", "Посмотреть в книге →"),
    ("Психотерапия", "«Разговоры болезнь не лечат»", "На самом деле: эффективность психотерапии измерена в сотнях рандомизированных исследований и сопоставима с медикаментозным лечением. Условие — работа по протоколу и измерение результата.", "Источник: международные протоколы и консенсус", "#programs", "Посмотреть программы →"),
  ],
  "cons_eyebrow": "Консультации",
  "cons_h2": "Три формата, одна цель",
  "cons_lead": "Личная терапия, парная или супервизия — если не знаете, что выбрать, объясним одной строкой.",
  "cons": [
    ("Индивидуально", "Кенан Рагимов / Самира Рагимова", "Личная терапия, депрессия, паника, фобия, энурез."),
    ("Два специалиста", "Кенан + Самира", "Семейная и парная терапия, сложные случаи."),
    ("Супервизия", "Кенан Рагимов", "Для студентов-психологов и практикующих специалистов."),
  ],
  "cons_btn": "Подробнее",
  "books_eyebrow": "Книги",
  "books_h2": "Читайте бесплатно, в печати — по желанию",
  "books": [
    ("Клиническая психиатрия", "820 с. (B5), 4 языка", "28 ₼", "/books/covers/klinik.jpg"),
    ("Вирус вины", "224 с.", "22 ₼", "/books/covers/guilt.jpg"),
    ("Шизофрения. Пандемия безумия", "312 с.", "26 ₼", "/books/covers/pandemic.jpg"),
    ("Эра Феникса", "288 с.", "24 ₼", "/books/covers/phoenix.jpg"),
  ],
  "book_read": "Читать бесплатно",
  "book_order": "Заказать",
  "biz_eyebrow": "Бизнес и HR",
  "biz_h2": "HR Школа — с 2008 года",
  "biz_text": "Более 2000 выпускников программы HR и более 3000 участников тренингов. MG, Unibank, DNS Computers. С 2019 года — государственный сертификат.",
  "biz_nums": [("2008", "год основания"), ("2000+", "выпускников HR"), ("3000+", "участников тренингов")],
  "biz_btn": "Корпоративные программы",
  "events_eyebrow": "Business Party",
  "events_h2": "2015–2016: три площадки",
  "events": [
    ("2015", "JW Marriott Absheron", "«Коммуникация»"),
    ("2015", "Kempinski Badamdar", "«Возможности бизнеса в 2016»"),
    ("2016", "Fairmont Flame Towers", "«Made in Italy»"),
  ],
  "tg_h2": "Продолжение — в Telegram",
  "tg_text": "Ответы на вопросы, эфиры, разбор клинических случаев. Выберите язык канала.",
  "tg_az": "На азербайджанском", "tg_ru": "На русском",
  "blog_eyebrow": "Блог",
  "blog_h2": "Протоколы, а не мнения",
  "blog": [
    ("Клинический протокол", "Лечение психогенной депрессии", "17 лет клинической практики. Протокол · 18 мин", "/ru/bloq/depressiya-protokol.html", "/images/blog/depressiya/protokol-cover.jpg"),
    ("Клинический протокол", "Ночной энурез — модифицированный протокол", "10-недельная программа. n=240, 80% ремиссия. · 14 мин", "/ru/bloq/enurez-protokol.html", "/images/blog/enurez/protokol-cover.jpg"),
    ("Клиническая психология", "Как КПТ работает при депрессии", "Треугольник, автоматические мысли, поведенческая активация. · 11 мин", "/ru/bloq/depressiya-2.html", "/images/blog/depressiya/art2-cover.jpg"),
  ],
  "blog_read": "Читать",
  "foot_desc": "Профессиональная школа психологии. Клиническая практика, официальное образование, международная сертификация.",
  "foot_cols": [
    ("Терапия", ["Семейная терапия", "Ночной энурез", "Панические атаки", "Депрессия", "Социальная фобия"]),
    ("Обучение", ["Общая психология", "Клиническая психология", "Практикум психотерапии", "Психоанализ", "Психодиагностика"]),
    ("Контакты", ["+994 70 220 03 76", "info@ragimoff.org", "Баку, Джафар Джаббарлы 40", "Caspian Business Center"]),
  ],
  "foot_rights": "© 2026 RAGIMOFF. Все права защищены.",
  "foot_note": "Школа, где обучение опирается на собственные учебники и первоисточники.",
  "prose_note": "Цены и условия программ могут меняться — уточняйте актуальную информацию.",
},
"en": {
  "lang_name": "EN", "html_lang": "en",
  "nav": ["Specialists", "Books", "Training", "Consultations", "Blog", "Contact"],
  "nav_href": ["/en/mutexessisler/index.html", "/books/", "/en/telim/index.html", "/en/konsultasiya/index.html", "/en/bloq/index.html", "/en/elaqe/index.html"],
  "cta": "Book now",
  "hero_badge": "IPAS Ambassador · BAPPs · ADA",
  "hero_query": "Doctor Ragimoff",
  "hero_strong": "School of Psychology",
  "hero_h1": "School of<br><em>Psychology</em>",
  "hero_sub": "Twenty-three years in clinical practice. An official diploma and an international certificate — all of it in Azerbaijani.",
  "hero_btn1": "Training programs",
  "hero_btn2": "Consultation",
  "hero_note": "Kenan Ragimov — clinical psychologist, psychotherapist, IPAS Ambassador",
  "spec_eyebrow": "Specialists",
  "spec_h2": "Two specialists, one school",
  "spec_lead": "One is the author of the clinical psychiatry textbook, the other runs the family therapy modules. Two lines of one school — which is why a second opinion is available in complex cases.",
  "spec_more": "Learn more",
  "spec": [
    ("Kenan Ragimov", "Clinical psychologist, psychotherapist, IPAS Ambassador",
     "Founder of the RAGIMOFF Psychology School, author of the reference book “Clinical Psychiatry”. 23 years of clinical practice, has led the HR School since 2008.",
     "/images/kenan/kenan-removebg-preview.png", "/en/mutexessisler/kenan-rehimov.html"),
    ("Samira Ragimova", "Family therapist",
     "Couples, the parent–child bond, difficult teenagers. Leads the family therapy modules.",
     "/images/samira/samira-portret.jpg", "/en/mutexessisler/samire-rehimova.html"),
  ],
  "ment_eyebrow": "Formation",
  "ment_h2": "Whose school he came through",
  "ment_lead": "2001–2003, Saint Petersburg, the Bekhterev Institute of Psychoneurology. Graduated with distinction — under two men whose textbooks still train psychotherapists in Russia and beyond.",
  "ment": [
    ("Viktor Davydovich Vida", "2001–2002", "Doctor of Medical Sciences, professor, chief researcher at the Bekhterev National Medical Research Centre for Psychiatry and Neurology. The first certified psychoanalyst in Russia — German Academy of Psychoanalysis, Berlin and Munich. Author of the monograph “Psychotherapy of Schizophrenia”. Supervised the psychoanalytic training."),
    ("Boris Dmitrievich Karvasarsky", "2001–2003", "Doctor of Medical Sciences, professor, Honoured Scientist of the Russian Federation. Chief Psychotherapist of the Ministry of Health of the Russian Federation, founder of the Leningrad school of psychotherapy. Editor-in-chief of the textbook “Psychotherapy” and of the “Psychotherapeutic Encyclopaedia”; author of 215 scientific works. Supervised the psychotherapy training."),
  ],
  "ment_note": "Both supervisors' textbooks still form the basis of psychotherapy training today.",
  "freud_eyebrow": "First time in Azerbaijan",
  "freud_h2": "Freud — in your own language",
  "freud_lead": "Translated from the German originals: works, lectures, correspondence, clinical notes. Not retellings and not anthologies — the texts themselves.",
  "freud_text": "It opens in the browser: nothing to download, search works, your place is saved. This is what students lacked most — without fundamental texts a professional education is impossible.",
  "freud_btn": "Go to the library",
  "own_eyebrow": "Books by the author",
  "own_h2": "Every book proves its field",
  "own_lead": "Four books and four fields. Each is written at university textbook level; today nothing comparable exists.",
  "own_note": "Published in three languages. “Clinical Psychiatry” is also out in Turkish; more languages are being added.",
  "own": [
    ("Clinical Psychiatry", "CPD · Psychotherapy practicum · Psychodiagnostics", "/books/covers/klinik.jpg"),
    ("The Phoenix Era", "Family therapy · Relationships", "/books/covers/phoenix.jpg"),
    ("The Guilt Virus", "Public education · Cognitive therapy — against false beliefs", "/books/covers/guilt.jpg"),
    ("Schizophrenia. Pandemic of Madness", "Public education · Clinical psychiatry", "/books/covers/pandemic.jpg"),
  ],
  "tb2_eyebrow": "In preparation",
  "tb2_h2": "“General Psychotherapy”",
  "tb2_text": "The Russian volume is finished; the Azerbaijani edition is in preparation. The core course of psychotherapist training — in a single volume.",
  "tb2_note": "The book will open in the library as soon as it is published.",
  "case_eyebrow": "From practice",
  "case_h2": "“Sabina's Drama”",
  "case_lead": "A filmed record of real therapeutic work. No commentary, no directorial hints — only the work itself.",
  "case_text": "31 minutes. Open to a professional audience and students.",
  "marquee": ["Official CPD diploma", "IPAS certificate", "Clinical psychology", "Psychotherapy practicum", "Psychoanalysis", "Psychodiagnostics", "Family therapy", "Corporate training"],
  "stats": [("23+", "years of practice"), ("3000+", "patients"), ("2000+", "HR graduates"), ("11", "international certificates")],
  "lib_eyebrow": "Open library",
  "lib_h2": "Freud in Azerbaijani. First time. Free.",
  "lib_text": "24 books by Sigmund Freud translated from the original German into Azerbaijani. For students, practitioners and any reader. Read online, download, or order a printed copy.",
  "lib_nums": [("24", "Freud books"), ("4", "languages"), ("0 ₼", "to read")],
  "lib_btn": "Open the library",
  "lib_note": "Full collection: 94 volumes — Freud, Kenan Ragimov, Samira Ragimova.",
  "tb_eyebrow": "The principal work",
  "tb_h2": "“Clinical Psychiatry” — a textbook with no equivalent",
  "tb_text": "820 pages in print (B5 format), DSM-5 and ICD-11, international protocols and consensus. No such textbook exists in the world today: it works equally well for the clinician, the student and anyone choosing a method of therapy. It has been translated into four languages — Azerbaijani, Russian, English and Turkish. In Azerbaijani it is the official textbook, and it is open to everyone. It carries a further task: separating the scientific from the unscientific and clearing away the myths and misconceptions that divert people from proper treatment.",
  "tb_meta": ["820 pages · B5", "4 languages", "DSM-5 · ICD-11", "Free to read"],
  "tb_btn1": "Open and look inside",
  "tb_btn2": "Printed edition",
  "film_eyebrow": "From practice",
  "film_h2": "“Sabina's Drama”",
  "film_text": "A real case, dramatised. 31 minutes. No commentary.",
  "film_btn": "Watch",
  "prog_eyebrow": "Training",
  "prog_g_dpo": "CPD with diploma",
  "prog_g_spec": "Practicum and specialisations",
  "prog_h2": "Six training programmes",
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
  "myth_lead": "Every explanation cites its source. Check it yourself: open the textbook and read the section named.",
  "myth_label": "MYTH", "myth_fact": "Fact:",
  "myths": [
    ("Depression", "“Depression is just a bad mood — it will pass”", "In fact: depression is a diagnosable illness — brain chemistry, sleep, appetite and capacity to work all change. It lasts six to eight months on average and recurs without treatment. Psychotherapy and medication are equally evidenced methods.", "Source: “Clinical Psychiatry”, the depression section", "#textbook", "Open the book →"),
    ("Social phobia", "“It is just shyness — pull yourself together”", "In fact: social phobia is not shyness. The person avoids speaking, eating, making calls; physical reactions set in and life narrows. The effect of CBT is measurable: symptoms fall and become manageable.", "Source: “Clinical Psychiatry” + “The Virus of Guilt”", "#ownbooks", "See “The Virus of Guilt” →"),
    ("Nocturnal enuresis", "“The child is lazy and does it on purpose”", "In fact: nocturnal enuresis is not a matter of the child’s will — maturation, heredity and sleep phases are involved. Punishment makes it worse. The evidenced path: routine, alarm device, behavioural therapy.", "Source: “Clinical Psychiatry”, the enuresis section", "#textbook", "Open the book →"),
    ("Panic attack", "“A panic attack is a heart attack — I am dying”", "In fact: a panic attack is not dangerous and does not cause death. Racing heart, breathlessness and fear of dying are a wave of adrenaline that subsides within ten to twenty minutes. The real damage is avoidance and anticipatory fear — and that is what therapy removes.", "Source: “Clinical Psychiatry”, anxiety disorders", "#textbook", "Open the book →"),
    ("Psychotherapy", "“Talking does not cure illness”", "In fact: the effectiveness of psychotherapy has been measured in hundreds of randomised trials and is comparable to medication. The condition is working to protocol and measuring the result.", "Source: international protocols and consensus", "#programs", "See the programmes →"),
  ],
  "cons_eyebrow": "Consultations",
  "cons_h2": "Three formats, one goal",
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
    ("Clinical Psychiatry", "820 pp. (B5), 4 languages", "28 ₼", "/books/covers/klinik.jpg"),
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
  "foot_note": "A school whose teaching rests on its own textbooks and source texts.",
  "prose_note": "Prices and program terms may change — please confirm current details.",
},
}

PROGRAMS = [
  # (название обучения, документ/часы, пояснение, срок, полная цена, со скидкой, в месяц, выделенная, группа)
  ("Ümumi Psixologiya", "Diplom · 1 556 saat", "AR qanunvericiliyinə uyğun FRDO dövlət reyestrinə daxil edilən rəsmi Əlavə Təhsil diplomu. Psixoloq kimi hüquqi fəaliyyətin başlanğıcı.", "1 il — 6+6 ay", "4 200 ₼", "3 800 ₼", "200 ₼/ay", False, "dpo"),
  ("Klinik Psixologiya", "Diplom · 1 528 saat", "Mürəkkəb klinik hallar üzərində müstəqil işləmək hüququ. Öz mərkəzinizi açmaq üçün tam hüquqi status. Beynəlxalq IPAS sertifikatı ilə birgə.", "1 il — 6+6 ay", "6 600 ₼", "6 000 ₼", "300 ₼/ay", True, "dpo"),
  ("Psixoterapiya Praktikumu", "IPAS/BPA sertifikatı · 864 saat", "Psixoloq və pasiyent rollarında canlı məşqlər, real keyslərin superviziyası, konsilium formatı. QR-kodla yoxlanılan beynəlxalq sertifikat.", "1 il — praktika", "3 600 ₼", "3 000 ₼", "175 ₼/ay", False, "spec"),
  ("Ailə Terapiyası", "IPAS sertifikatı · 2 modul", "Cütlük terapiyası və valideyn-övlad münasibətləri. Ali təhsil tələb olunmur — psixologiya təhsili olanlara daha geniş imkanlar. Məzunlar mərkəzimizdə məsləhətçilik xidməti göstərə bilər.", "3 ay + 6 ay superviziya", "900 ₼", "800 ₼", "300 ₼/ay", False, "spec"),
  ("Psixoanaliz", "IPAS sertifikatı", "Təlim öz kitabxanamıza söykənir: Freydin 24 kitabı doğma dilinizdə, alman orijinalından. Oxu, müzakirə, superviziya.", "3 ay + 6 ay", "900 ₼", "800 ₼", "300 ₼/ay", False, "spec"),
  ("Psixodiaqnostika", "IPAS sertifikatı", "ÜST standartları üzrə diaqnozun əsaslandırılması — praktik vərdişə çevrilir. «Klinik Psixiatriya» dərsliyi ilə birlikdə.", "3 ay + 6 ay", "900 ₼", "800 ₼", "300 ₼/ay", False, "spec"),
]

PROGRAMS_RU = [
  ("Общая психология", "Диплом · 1 556 часов", "Официальный диплом Дополнительного образования, вносимый в государственный реестр ФРДО по законодательству АР. Начало правовой деятельности психолога.", "1 год — 6+6 мес.", "4 200 ₼", "3 800 ₼", "200 ₼/мес.", False, "dpo"),
  ("Клиническая психология", "Диплом · 1 528 часов", "Право самостоятельной работы со сложными клиническими случаями. Полный правовой статус для открытия своего центра. Вместе с международным сертификатом IPAS.", "1 год — 6+6 мес.", "6 600 ₼", "6 000 ₼", "300 ₼/мес.", True, "dpo"),
  ("Практикум психотерапии", "Сертификат IPAS/BPA · 864 часа", "Живые упражнения в ролях психолога и пациента, супервизия реальных кейсов, консилиум. Международный сертификат с проверкой по QR.", "1 год — практика", "3 600 ₼", "3 000 ₼", "175 ₼/мес.", False, "spec"),
  ("Семейная терапия", "Сертификат IPAS · 2 модуля", "Парная терапия и детско-родительские отношения. Высшее образование не требуется — с психологическим образованием больше возможностей. Выпускники могут консультировать в нашем центре.", "3 мес. + 6 мес. супервизии", "900 ₼", "800 ₼", "300 ₼/мес.", False, "spec"),
  ("Психоанализ", "Сертификат IPAS", "Обучение опирается на нашу библиотеку: 24 книги Фрейда на родном языке, с немецкого оригинала. Чтение, разбор, супервизия.", "3 мес. + 6 мес.", "900 ₼", "800 ₼", "300 ₼/мес.", False, "spec"),
  ("Психодиагностика", "Сертификат IPAS", "Обоснование диагноза по стандартам ВОЗ — до уровня устойчивого навыка. Вместе с учебником «Клиническая психиатрия».", "3 мес. + 6 мес.", "900 ₼", "800 ₼", "300 ₼/мес.", False, "spec"),
]

PROGRAMS_EN = [
  ("General Psychology", "Diploma · 1,556 hours", "The official Further Education diploma entered in the state FRDO register under Azerbaijani law. The starting point of lawful practice as a psychologist.", "1 year — 6+6 months", "4 200 ₼", "3 800 ₼", "200 ₼/mo", False, "dpo"),
  ("Clinical Psychology", "Diploma · 1,528 hours", "The right to work independently with complex clinical cases. Full legal status to open your own centre. Together with the international IPAS certificate.", "1 year — 6+6 months", "6 600 ₼", "6 000 ₼", "300 ₼/mo", True, "dpo"),
  ("Psychotherapy Practicum", "IPAS/BPA certificate · 864 hours", "Live exercises as psychologist and patient, supervision of real cases, case conference format. An international certificate verified by QR code.", "1 year — practice", "3 600 ₼", "3 000 ₼", "175 ₼/mo", False, "spec"),
  ("Family Therapy", "IPAS certificate · 2 modules", "Couples therapy and parent-child relationships. No university degree required — a psychology background opens more options. Graduates may counsel at our centre.", "3 mo + 6 mo supervision", "900 ₼", "800 ₼", "300 ₼/mo", False, "spec"),
  ("Psychoanalysis", "IPAS certificate", "The course rests on our library: 24 volumes of Freud in your own language, from the German originals. Reading, analysis, supervision.", "3 mo + 6 mo", "900 ₼", "800 ₼", "300 ₼/mo", False, "spec"),
  ("Psychodiagnostics", "IPAS certificate", "Justifying a diagnosis under WHO standards, down to a durable skill. Together with the “Clinical Psychiatry” textbook.", "3 mo + 6 mo", "900 ₼", "800 ₼", "300 ₼/mo", False, "spec"),
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
    """Первый экран — скраб 90 кадров видео по скроллу.
    Кадры лежат в /images/hero-home/{d,m}/f000..f089.webp, движок в main.js.
    Фазы (номера кадров): касание → поисковая строка, печать имени, заголовок."""
    marks = "19,23,23,35,37"
    # посимвольная выдача сильного слова (для анимации --i)
    strong = t.get("hero_strong", "Psixologiya Məktəbi")
    letters = "".join(
        f'<span style="--i:{i}">{esc(ch) if ch != " " else "&nbsp;"}</span>'
        for i, ch in enumerate(strong)
    )
    return f"""
<section class="cine cine-v" id="main-content" data-cine>
  <div class="cine__stick">
    <div class="cine__frame" data-frames="90"
         data-fsrc="/images/hero-home/d/f{{i}}.webp"
         data-msrc="/images/hero-home/m/f{{i}}.webp"
         data-marks="{marks}">
      <img class="cine__img" src="/images/hero-home/d/f000.webp" alt="" fetchpriority="high">
      <canvas class="cine__cv" aria-hidden="true"></canvas>
      <div class="cine__search" aria-hidden="true">
        <svg viewBox="0 0 24 24" width="22" height="22"><circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M15.5 15.5 21 21" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>
        <span class="cine__q" data-q="{esc(t.get('hero_query', 'Doctor Ragimoff'))}"></span><i class="cine__caret"></i>
      </div>
    </div>
    <div class="cine__shade" aria-hidden="true"></div>
    <div class="wrap cine__beat cine__b1">
      <span class="eyebrow">{esc(t['hero_badge'])}</span>
      <h1 class="cine__h1">
        <span class="cine__hand">{esc(t.get('hero_query', 'Doctor Ragimoff'))}</span>
        <span class="cine__strong" aria-label="{esc(strong)}">{letters}</span>
      </h1>
      <div class="cine__cta">
        <a class="btn btn--primary btn--lg" href="{t['nav_href'][2]}">{esc(t['hero_btn1'])}</a>
        <a class="btn btn--line btn--lg" href="{t['nav_href'][3]}">{esc(t['hero_btn2'])}</a>
      </div>
      <p class="cine__lead">{esc(t['hero_note'])}</p>
    </div>
    <div class="cine__cue" aria-hidden="true"><i></i></div>
    <div class="cine__out" aria-hidden="true"></div>
  </div>
</section>
"""


def specialists(t):
    cards = "".join(
        f"""<article class="person reveal">
      <div class="person__photo"><img src="{img}" alt="{esc(name)}" loading="lazy"></div>
      <div class="person__body">
        <h3 class="person__name">{esc(name)}</h3>
        <p class="person__role">{esc(role)}</p>
        <p class="person__text">{esc(d)}</p>
        <a class="btn btn--line btn--sm" href="{href}">{esc(t['spec_more'])}</a>
      </div>
    </article>"""
        for name, role, d, img, href in t["spec"]
    )
    return f"""
<section class="section" id="specialists">
  <div class="wrap">
    <div class="sec-head reveal">
      <span class="eyebrow">{esc(t['spec_eyebrow'])}</span>
      <h2>{esc(t['spec_h2'])}</h2>
      <p class="lead">{esc(t['spec_lead'])}</p>
    </div>
    <div class="people">{cards}</div>
  </div>
</section>
"""


def mentors(t):
    rows = "".join(
        f"""<div class="mentor reveal">
      <h3 class="mentor__name">{esc(n)}</h3>
      <span class="mentor__years">{esc(y)}</span>
      <p class="mentor__text">{esc(d)}</p>
    </div>"""
        for n, y, d in t["ment"]
    )
    return f"""
<section class="section section--tight" id="formation">
  <div class="wrap split" style="align-items:start">
    <div class="reveal">
      <span class="eyebrow">{esc(t['ment_eyebrow'])}</span>
      <h2 style="margin:var(--r1) 0">{esc(t['ment_h2'])}</h2>
      <p class="lead">{esc(t['ment_lead'])}</p>
      <p class="note-line">{esc(t['ment_note'])}</p>
    </div>
    <div class="mentors">{rows}</div>
  </div>
</section>
"""


def freud(t):
    shelf = "".join(
        f'<a class="shelf__item" href="/books/"><img src="/books/covers/{f}" alt="" loading="lazy"></a>'
        for f in ["freud.jpg", "art-freud-gw01.jpg", "art-freud-aforizmlar.jpg",
                  "art-freud-koka.jpg", "art-freud-fliesse-mektublari.jpg",
                  "art-freud-sevgi-mektublari.jpg", "art-freud-yung-mektublari.jpg",
                  "art-freud-zweig-mektublari.jpg"]
    )
    return f"""
<section class="section" id="freud">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">{esc(t['freud_eyebrow'])}</span>
      <h2 style="margin:var(--r1) 0">{esc(t['freud_h2'])}</h2>
      <p class="lead">{esc(t['freud_lead'])}</p>
      <p class="note-line">{esc(t['freud_text'])}</p>
      <a class="btn btn--primary" style="margin-top:var(--r2)" href="/books/">{esc(t['freud_btn'])}</a>
    </div>
    <div class="shelf reveal">{shelf}</div>
  </div>
</section>
"""


def own_books(t):
    cards = "".join(
        f"""<a class="bookcard reveal" href="/books/">
      <span class="bookcard__cover"><img src="{cover}" alt="" loading="lazy"></span>
      <span class="bookcard__meta"><b>{esc(title)}</b><small>{esc(sub)}</small></span>
    </a>"""
        for title, sub, cover in t["own"]
    )
    return f"""
<section class="section section--tight" id="ownbooks">
  <div class="wrap">
    <div class="sec-head reveal">
      <span class="eyebrow">{esc(t['own_eyebrow'])}</span>
      <h2>{esc(t['own_h2'])}</h2>
      <p class="lead">{esc(t['own_lead'])}</p>
    </div>
    <div class="bookrow">{cards}</div>
    <p class="note-line reveal">{esc(t['own_note'])}</p>
  </div>
</section>
"""


def upcoming(t):
    return f"""
<section class="section section--tight" id="upcoming">
  <div class="wrap">
    <div class="upcoming reveal">
      <div>
        <span class="eyebrow">{esc(t['tb2_eyebrow'])}</span>
        <h2 style="margin:var(--r1) 0">{esc(t['tb2_h2'])}</h2>
        <p class="lead">{esc(t['tb2_text'])}</p>
        <p class="note-line">{esc(t['tb2_note'])}</p>
      </div>
      <div class="upcoming__mark" aria-hidden="true">{esc(t['tb2_h2'].strip('«»“”'))}</div>
    </div>
  </div>
</section>
"""


def marquee(t):
    """Бегущая строка — как в эталоне (замер: высота 122 px, буквы 68 px,
    курсив Cormorant 300, золотые точки между словами, 90s linear).
    Кенан: «у тебя какой-то зависшая во времени полосочка. А там конкретно идёт
    полоса, крупные буквы, читаемые, не микро какие-то.»"""
    items = "".join(
        f"<span>{esc(x)}</span><i aria-hidden=\"true\"></i>" for x in t["marquee"]
    )
    return (f'<div class="marquee" aria-hidden="true">'
            f'<div class="marquee__track">{items}{items}</div></div>')


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
<section class="section section--ucl" id="textbook">
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
    def card(name, doc, desc, dur, full, pre, month, featured):
        cls = "program program--featured" if featured else "program"
        return f"""
    <article class="{cls} reveal">
      <h3 class="program__name">{esc(name)}</h3>
      <p class="program__doc">{esc(doc)}</p>
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

    dpo = [p for p in PROG_BY_LANG[lang] if p[8] == "dpo"]
    spec = [p for p in PROG_BY_LANG[lang] if p[8] != "dpo"]
    groups = ""
    for label, rows_src in ((t["prog_g_dpo"], dpo), (t["prog_g_spec"], spec)):
        cards = "".join(card(*p[:8]) for p in rows_src)
        groups += f"""
    <h3 class="program__group reveal">{esc(label)}</h3>
    <div class="grid-2">{cards}</div>"""

    return f"""
<section class="section" id="programs">
  <div class="wrap">
    <div class="sec-head reveal">
      <span class="eyebrow">{esc(t['prog_eyebrow'])}</span>
      <h2>{esc(t['prog_h2'])}</h2>
      <p class="lead">{esc(t['prog_lead'])}</p>
    </div>
    {groups}
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
    """Разрушение мифов — отдельный крупный блок (Кенан 10.11.2026).

    Было: три узкие полоски в сетке из трёх, мрачно и мимо.
    Кенан: «Взять наиболее популярные, связанные с депрессией, социальной фобией,
    ночным энурезом... привести со ссылкой именно на страницу книги, именно на
    этот раздел, чтобы человек кликал и переходил на страницу этой книги, и смог
    там ознакомиться с другими мифами и со структурой терапии.»

    Стало: каждый миф — широкая строка с темой слева, разбором справа и ссылкой
    в конец. Темы идут от самых частых обращений."""
    rows = ""
    for topic, q, a, src, href, link in t["myths"]:
        rows += f"""
    <article class="mythrow reveal">
      <div class="mythrow__topic">
        <span class="mythrow__topic-name">{esc(topic)}</span>
        <span class="mythrow__label">{esc(t['myth_label'])}</span>
      </div>
      <div class="mythrow__body">
        <p class="mythrow__q">{esc(q)}</p>
        <p class="mythrow__a"><b>{esc(t['myth_fact'])}</b> {esc(a)}</p>
        <p class="mythrow__src">{esc(src)}
          <a class="mythrow__link" href="{href}">{esc(link)}</a></p>
      </div>
    </article>"""
    return f"""
<section class="section section--myths" id="myths">
  <div class="wrap">
    <div class="sec-head reveal">
      <span class="eyebrow">{esc(t['myth_eyebrow'])}</span>
      <h2>{esc(t['myth_h2'])}</h2>
      <p class="lead">{esc(t['myth_lead'])}</p>
    </div>
    <div class="mythlist">{rows}</div>
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
        <p class="foot__desc">{esc(t['foot_desc'])}</p>
        <p style="font-size:12px;color:var(--text-faint)">{esc(t['foot_note'])}</p>
      </div>
      {cols}
    </div>
    <div class="foot__mark reveal" aria-hidden="true">RAGIMOFF.</div>
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
<link rel="stylesheet" href="{BASE}/assets/css/fonts.css">
<link rel="stylesheet" href="{BASE}/assets/css/tokens.css">
<link rel="stylesheet" href="{BASE}/assets/css/base.css">
<link rel="stylesheet" href="{BASE}/assets/css/components.css">
<link rel="stylesheet" href="{BASE}/assets/css/patterns.css">
<link rel="stylesheet" href="{BASE}/assets/css/hero.css">
<script defer src="{BASE}/assets/js/main.js"></script>
</head>
<body>
<a class="sr-only" href="#main">Skip to content</a>
{header(t, lang)}
<main id="main">
{hero(t)}
{marquee(t)}
{textbook(t)}
{mentors(t)}
{freud(t)}
{specialists(t)}
{own_books(t)}
{upcoming(t)}
{consultations(t)}
{film(t)}
{programs(t, lang)}
{business(t)}
{myths(t)}
{timeline(t)}
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
