# SITE-STRUCTURE — структура сайта ragimoff.org

Машинный паспорт сайта: какие страницы существуют, из каких блоков состоят,
что обязано быть на каждом типе страницы и какие проверки обязана проходить
каждая страница. Пересобирается скриптом `_tools/site-structure-build.py`
(раздел «Страницы» снимается с дерева), проверяется скриптом
`_tools/site-structure-check.py` по живой копии сайта. Человекочитаемая
проекция — `SITE-STRUCTURE.md`; стандарт дизайна — `DESIGN-STANDARDS.md`,
стандарт пары «заголовок ↔ подзаголовок» — `DESIGN-STANDARD.md`.

## 1. Языки и каталоги

| язык | каталог | роль |
|---|---|---|
| AZ | `/` | основная версия; страницы раздела психиатрии и служебные — только здесь |
| RU | `/ru/` | русская версия; полный набор, кроме служебных |
| EN | `/en/` | английская версия; полный набор, кроме служебных |

## 2. Каркас страницы (порядок сверху вниз)

| # | блок | класс/маркер | обязателен | роль |
|---|---|---|---|---|
| 1 | Шапка | `header .site-header / .desktop-nav / .mobile-nav` | да | логотип, меню разделов, поиск (#site-si), переключатель языков (.lang-drop / .mobile-lang-row), кнопка записи |
| 2 | Блок героя | `.page-hero (главные) / .page-hero-x (внутренние) / .pg-hero` | да | метка (.badge/.ph-badge), H1, лид (.hero-lead/.ph-sub), поиск (.hero-search-wrap/.ph-search-wrap), фото (.photo-col — не на всех страницах) |
| 3 | Секции | `section[class], .sec-header + содержимое` | да, ≥1 | смысловые блоки страницы; шапка блока (.sec-header) = бейдж + H2 + подзаголовок |
| 4 | Подвал | `footer .footer-links` | да | навигация по разделам, контакты, языковой ряд, копирайт |
| 5 | Мобильное меню | `.mobile-nav` | да | выдвижное меню; закрыто вне экрана и не считается за горизонтальную прокрутку |

## 3. Типы страниц и обязательные блоки

### home — Главная (az/ru/en)

Витрина: герой с портретом автора, полоса цифр, экосистема, направления, статьи, книги, форма связи.
Герой — самый длинный на сайте: H1 в одну строку на десктопе, лид в две.

Обязательные блоки: `.page-hero`, `.stats-strip`, `h2`, `.footer-links`.

### page — Внутренняя страница (раздел, услуга, программа, статья раздела)

Всё, что не главная и не блог: страницы услуг, программы, раздел психиатрии, юридические,
служебные. Единый герой `.page-hero-x` с меткой, H1, лидом и поиском.
Раздел психиатрии (`klinik-psixiatriya/`) ведёт свой герой (`pg-hero`) и в этот файл не входит.

Обязательные блоки: `.page-hero-x`, `section`, `h2`, `.footer-links`.

### blog-index — Индекс блога

Список статей с фильтром по темам.

Обязательные блоки: `.page-hero-x`, `.filter-inner`, `h2`, `.footer-links`.

### blog-article — Статья блога

Текстовая страница: герой, тело статьи (.article-body), блок «читать также», подвал.
Внутри статьи подзаголовки ведут себя по карточному правилу (16/12), а не 48/32.

Обязательные блоки: `.page-hero-x`, `.article-body`, `h2`, `.footer-links`.

### template — Служебные шаблоны

`template.html`, `temp_index.html` — заготовки для копирования. Из проверок структуры
исключены (могут не иметь H1), но не должны попадать в sitemap и в навигацию.

Обязательные блоки: .

### test — Тестовые страницы

`test-wave-elements.html` — стенд проверки волн. Из проверок структуры исключены,
в навигацию и sitemap не входят.

Обязательные блоки: .

### redirect — Страница-редирект

`klinik-psixiatriya.html` — точка входа в раздел психиатрии: `<meta http-equiv="refresh">`
уводит в `/klinik-psixiatriya/`. Ни шапки, ни героя, ни подвала у неё нет по устройству —
проверки структуры к типу не применяются (исключён из правил в `site-structure-check.py`).

Обязательные блоки: .

## 4. Проверки, которые обязана проходить каждая страница

| код | класс | проверка | норма | где мерить |
|---|---|---|---|---|
| `hero-height` | a | высота блока героя — одна на всех страницах (все страницы с героем) | десктоп 1440: 520 px ± 1; телефон 390: одна величина на всех страницах (слоты H1/лида/фото) ± 1 | `node _tools/hero-survey.js --width <ш> --jobs 4 --require-fit 0 --list pages.txt --out out.json` |
| `hero-grid` | a | сетка героя: метка / H1 / лид / поиск на одних и тех же высотах | десктоп: метка 88, H1 154, лид 304, поиск 419; телефон: метка 32, лид после фото, поиск прижат, 25 px под поиском | `node _tools/hero-survey.js` |
| `hero-photo` | a | пропорции фото героя | десктоп: верх 50 от грани блока, низ = низ блока; телефон: портрет 70–85 % ширины колонки, пропорция кадра 0,952 сохранена, лицо не обрезано | `node _tools/hero-lines.js 390 <страницы>` |
| `hero-lines` | a | деление H1 и лида на строки | по словам, без переносов по слогам; 2 строки, при необходимости 3; text-wrap: balance; перекос (макс/мин ширина строки) ≤ 1,3 | `node _tools/hero-lines.js 390 <страницы>` |
| `spacing` | c | шкала интервалов и пустые полосы | верх блока → метка 88/48/32; шапка блока → содержимое 48/32; поиск → низ героя 50/25; пустая полоса между блоками > 160 px — дефект | `node _tools/site-audit.js --width 1440,390 --light-width 390` |
| `font-roles` | d | роли гарнитур по классам элементов | дисплей Cormorant Garamond — H1/H2/H3; чтение Literata — абзацы и лиды; интерфейс Montserrat — навигация, кнопки, поля; метаданные IBM Plex Mono — бейджи, метки, подписи | `node _tools/site-audit.js --width 1440` |
| `contrast` | b | контраст текста к фону | ≥ 4,5:1 обычный текст; ≥ 3:1 крупный (≥ 24 px или ≥ 18,66 px при весе ≥ 700) | `node _tools/site-audit.js --width 1440` |
| `h-scroll` | e | горизонтальная прокрутка и вылеты за вьюпорт | scrollWidth ≤ clientWidth + 1 на 390 и 1440; ни один видимый элемент не выходит за вьюпорт | `node _tools/site-audit.js --width 390,1440` |
| `links` | f | ссылки и навигация | все внутренние ссылки и якоря разрешаются; нет пустых href ("", "#"); переключатель языков ведёт на существующие страницы | `node _tools/site-audit.js --static-only` |
| `lang` | g | язык версии и регистр | основной текст — на языке версии; иноязычное только в скобках/кавычках; термины — по реестру CASE-REGISTER.tsv | `_tools/site-structure-check.py --lang` |
| `structure` | f | обязательные блоки типа страницы и метаданные | шапка, герой нужного класса, ≥1 секция, подвал, ровно один H1, <title>, lang атрибута версии | `_tools/site-structure-check.py` |

## 5. Страницы

| страница | язык | тип | герой | назначение |
|---|---|---|---|---|
| `aile-terapiyasi-usaq.html` | az | page | `page-hero-x` | детская и подростковая семейная терапия |
| `aile-terapiyasi.html` | az | page | `page-hero-x` | семейная терапия: направления и форматы работы |
| `b2b.html` | az | page | `page-hero-x` | корпоративным клиентам: программы для организаций |
| `blog-aile-2.html` | az | blog-article | `page-hero-x` | Toksik Münasibətin 7 Əlaməti |
| `blog-aile-3.html` | az | blog-article | `page-hero-x` | Boşanma Astanasında Ailə — Müalicə vs Ayrılıq |
| `blog-aile-4.html` | az | blog-article | `page-hero-x` | Cütlüklər Necə Düzgün Mübahisə Etməlidir? |
| `blog-aile-5.html` | az | blog-article | `page-hero-x` | Etibar İtirildikdə Onu Necə Qaytarmaq Olar? |
| `blog-aile-usaq-2.html` | az | blog-article | `page-hero-x` | Uşaq Davranış Problemləri — Əmr-Cəza vs Anlama |
| `blog-aile-usaq-3.html` | az | blog-article | `page-hero-x` | Boşanma Sonrası Uşaq — Necə Kömək Etmək Olar? |
| `blog-aile-usaq-4.html` | az | blog-article | `page-hero-x` | Məktəbdən İmtina — 5 Əsl Səbəb |
| `blog-aile-usaq-5.html` | az | blog-article | `page-hero-x` | Uşağa 'Yox' Demək — Sağlam Sərhəd Necə Qurulur? |
| `blog-aile.html` | az | blog-article | `page-hero-x` | Ailə Münaqişəsini Həll Etmənin 5 Prinsipi |
| `blog-depressiya-2.html` | az | blog-article | `page-hero-x` | KDT Depressiyada Necə İşləyir? |
| `blog-depressiya-3.html` | az | blog-article | `page-hero-x` | Antidepressantlar — Faktlar və Miflər |
| `blog-depressiya-4.html` | az | blog-article | `page-hero-x` | Postpartum Depressiya — Tanımaq və Müalicə |
| `blog-depressiya-5.html` | az | blog-article | `page-hero-x` | Mövsümi Depressiya (SAD) və İşıq Terapiyası |
| `blog-depressiya-protokol.html` | az | blog-article | `page-hero-x` | Psixogen Depressiyanın Müalicəsi |
| `blog-depressiya.html` | az | blog-article | `page-hero-x` | Depressiya Kədərdən Necə Fərqlənir? |
| `blog-enurez-2.html` | az | blog-article | `page-hero-x` | BMGE — Birincili Monosimptomatik Gecə Enurezi: Tam Bələdçi |
| `blog-enurez-3.html` | az | blog-article | `page-hero-x` | Alarm Cihazı Necə İşləyir? — Beynəlxalq Protokol |
| `blog-enurez-4.html` | az | blog-article | `page-hero-x` | Desmopressin və İmipramin — Enurezdə Dərmanlar |
| `blog-enurez-5.html` | az | blog-article | `page-hero-x` | Valideynlər Üçün 7 Praktik Məsləhət |
| `blog-enurez-protokol.html` | az | blog-article | `page-hero-x` | Uşaqlarda Gecə Enurezinin Müalicəsi |
| `blog-enurez.html` | az | blog-article | `page-hero-x` | Uşağınız Gecələr Yatağı Isladırsa — 5 Yanlış İnanc |
| `blog-klinik-psixiatriya.html` | az | blog-article | `page-hero-x` | Klinik Psixiatriya — XBT-11 Əsaslı Diaqnostika Rəhbərliyi |
| `blog-panik-2.html` | az | blog-article | `page-hero-x` | Panik Atak Anında Beyində Nə Baş Verir? |
| `blog-panik-3.html` | az | blog-article | `page-hero-x` | Agorafobiya — Panik Atakdan Sosial Təcridə |
| `blog-panik-4.html` | az | blog-article | `page-hero-x` | KDT Panik Pozğunluqda Necə İşləyir? |
| `blog-panik-5.html` | az | blog-article | `page-hero-x` | Panik Ataklarla Bağlı 7 Mif və Elmi Cavablar |
| `blog-panik.html` | az | blog-article | `page-hero-x` | Panik Atak Anında Nə Etməli? |
| `blog-psixolog-olmaq-2.html` | az | blog-article | `page-hero-x` | Klinik vs Ümumi Psixologiya — Fərq və Seçim |
| `blog-psixolog-olmaq-3.html` | az | blog-article | `page-hero-x` | Yeni Psixoloq Üçün İlk Müştəri Necə Alınır? |
| `blog-psixolog-olmaq-4.html` | az | blog-article | `page-hero-x` | Süpervizyon — Psixoloqun Davamlı Müəllimi |
| `blog-psixolog-olmaq-5.html` | az | blog-article | `page-hero-x` | Psixoloqun Özünüqayğısı — Burnoutdan Qorunma |
| `blog-psixolog-olmaq.html` | az | blog-article | `page-hero-x` | Yaxşı Psixoloq Heç Vaxt İşsiz Qalmır — Niyə? |
| `blog-sosial-fobiya-2.html` | az | blog-article | `page-hero-x` | İctimai Çıxış Qorxusu — KDT və Ekspozisiya |
| `blog-sosial-fobiya-3.html` | az | blog-article | `page-hero-x` | Qızarma və Tərləmə — Sosial Reaksiyalar |
| `blog-sosial-fobiya-4.html` | az | blog-article | `page-hero-x` | Sosial Anksiyete vs İntrovertlik — Fərq Nədə? |
| `blog-sosial-fobiya-5.html` | az | blog-article | `page-hero-x` | Sosial Mediada Anksiyete — Yeni Forma |
| `blog-sosial-fobiya.html` | az | blog-article | `page-hero-x` | Sosial Fobiya — Sadəcə Utancaqlıq Deyil |
| `blog-yeniyetme.html` | az | blog-article | `page-hero-x` | Yeniyetməniz Sizinlə Danışmırsa — Səbəb Siz Deyilsiniz |
| `blog.html` | az | blog-index | `page-hero-x` | индекс статей блога с фильтром по темам |
| `depressiya.html` | az | page | `page-hero-x` | депрессия: раздел направления |
| `enurez.html` | az | page | `page-hero-x` | энурез: раздел направления |
| `haqqimda.html` | az | page | `page-hero-x` | о специалисте: биография, квалификации, подход |
| `index.html` | az | home | `page-hero` | витрина: герой с портретом, цифры, экосистема, направления, статьи, книги, форма |
| `klinik-psixiatriya.html` | az | redirect | — | редирект в раздел «Клиническая психиатрия» |
| `panik-ataklar.html` | az | page | `page-hero-x` | панические атаки: раздел направления |
| `program-klinik.html` | az | page | `page-hero-x` | программа «Клиническая психология» |
| `program-praktikum.html` | az | page | `page-hero-x` | программу «Практикум» |
| `program-umumi.html` | az | page | `page-hero-x` | программа «Общая психология» |
| `qanunlar.html` | az | page | `page-hero-x` | нормативная база: законы и стандарты профессии |
| `samira.html` | az | page | `page-hero-x` | авторский метод SAMİRA: протокол и обоснование |
| `sosial-fobiya.html` | az | page | `page-hero-x` | социальная фобия: раздел направления |
| `tehsil.html` | az | page | `page-hero-x` | программа обучения: институт ДПО, модули, цены, форма записи |
| `temp_index.html` | az | template | `page-hero` | служебная заготовка главной (не индексируется) |
| `template.html` | az | template | — | служебный шаблон страницы (не индексируется) |
| `test-wave-elements.html` | az | test | `page-hero` | тестовый стенд элементов (не индексируется) |
| `valideyn-mektebi.html` | az | page | `page-hero-x` | родительская школа: курс для родителей |
| `xidmetler.html` | az | page | `page-hero-x` | каталог услуг: индивидуальная, семейная, подростковая терапия |
| `ru/aile-terapiyasi-usaq.html` | ru | page | `page-hero-x` | детская и подростковая семейная терапия |
| `ru/aile-terapiyasi.html` | ru | page | `page-hero-x` | семейная терапия: направления и форматы работы |
| `ru/b2b.html` | ru | page | `page-hero-x` | корпоративным клиентам: программы для организаций |
| `ru/blog-aile-2.html` | ru | blog-article | `page-hero-x` | 7 признаков токсичных отношений |
| `ru/blog-aile-3.html` | ru | blog-article | `page-hero-x` | Семья на грани развода — лечение или расставание? |
| `ru/blog-aile-4.html` | ru | blog-article | `page-hero-x` | Как правильно спорить в паре? |
| `ru/blog-aile-5.html` | ru | blog-article | `page-hero-x` | Как восстановить доверие после измены? |
| `ru/blog-aile-usaq-2.html` | ru | blog-article | `page-hero-x` | Проблемы поведения ребёнка — наказание или понимание? |
| `ru/blog-aile-usaq-3.html` | ru | blog-article | `page-hero-x` | Ребёнок после развода — как помочь? |
| `ru/blog-aile-usaq-4.html` | ru | blog-article | `page-hero-x` | Отказ от школы — 5 настоящих причин |
| `ru/blog-aile-usaq-5.html` | ru | blog-article | `page-hero-x` | Сказать ребёнку «нет» — как выстроить здоровые границы? |
| `ru/blog-aile.html` | ru | blog-article | `page-hero-x` | 5 принципов разрешения семейных конфликтов |
| `ru/blog-depressiya-2.html` | ru | blog-article | `page-hero-x` | Как работает КПТ при депрессии? |
| `ru/blog-depressiya-3.html` | ru | blog-article | `page-hero-x` | Антидепрессанты — факты и мифы |
| `ru/blog-depressiya-4.html` | ru | blog-article | `page-hero-x` | Послеродовая депрессия — распознать и лечить |
| `ru/blog-depressiya-5.html` | ru | blog-article | `page-hero-x` | Сезонная депрессия (SAD) и световая терапия |
| `ru/blog-depressiya-protokol.html` | ru | blog-article | `page-hero-x` | Лечение психогенной депрессии |
| `ru/blog-depressiya.html` | ru | blog-article | `page-hero-x` | Чем депрессия отличается от грусти? |
| `ru/blog-enurez-2.html` | ru | blog-article | `page-hero-x` | ПМНЭ — Первичный моносимптоматический ночной энурез: полное руководство |
| `ru/blog-enurez-3.html` | ru | blog-article | `page-hero-x` | Как работает сигнализатор энуреза? — Международный протокол |
| `ru/blog-enurez-4.html` | ru | blog-article | `page-hero-x` | Десмопрессин и имипрамин — препараты при энурезе |
| `ru/blog-enurez-5.html` | ru | blog-article | `page-hero-x` | 7 практических советов для родителей |
| `ru/blog-enurez-protokol.html` | ru | blog-article | `page-hero-x` | Лечение ночного энуреза у детей |
| `ru/blog-enurez.html` | ru | blog-article | `page-hero-x` | Ребёнок мочится в постель ночью — 5 ложных убеждений |
| `ru/blog-panik-2.html` | ru | blog-article | `page-hero-x` | Что происходит в мозге во время панической атаки? |
| `ru/blog-panik-3.html` | ru | blog-article | `page-hero-x` | Агорафобия — от панических атак к социальной изоляции |
| `ru/blog-panik-4.html` | ru | blog-article | `page-hero-x` | Как работает КПТ при паническом расстройстве? |
| `ru/blog-panik-5.html` | ru | blog-article | `page-hero-x` | 7 мифов о панических атаках и научные ответы |
| `ru/blog-panik.html` | ru | blog-article | `page-hero-x` | Что делать во время панической атаки? |
| `ru/blog-psixolog-olmaq-2.html` | ru | blog-article | `page-hero-x` | Клиническая vs общая психология — разница и выбор |
| `ru/blog-psixolog-olmaq-3.html` | ru | blog-article | `page-hero-x` | Как новому психологу найти первых клиентов? |
| `ru/blog-psixolog-olmaq-4.html` | ru | blog-article | `page-hero-x` | Супервизия — постоянный учитель психолога |
| `ru/blog-psixolog-olmaq-5.html` | ru | blog-article | `page-hero-x` | Забота о себе для психолога — защита от выгорания |
| `ru/blog-psixolog-olmaq.html` | ru | blog-article | `page-hero-x` | Хороший психолог никогда не остаётся без работы — почему? |
| `ru/blog-sosial-fobiya-2.html` | ru | blog-article | `page-hero-x` | Страх публичных выступлений — КПТ и экспозиция |
| `ru/blog-sosial-fobiya-3.html` | ru | blog-article | `page-hero-x` | Покраснение и потливость — социальные реакции |
| `ru/blog-sosial-fobiya-4.html` | ru | blog-article | `page-hero-x` | Социальная тревога vs интроверсия — в чём разница? |
| `ru/blog-sosial-fobiya-5.html` | ru | blog-article | `page-hero-x` | Тревога в социальных сетях — новая форма |
| `ru/blog-sosial-fobiya.html` | ru | blog-article | `page-hero-x` | Социофобия — это не просто застенчивость |
| `ru/blog-yeniyetme.html` | ru | blog-article | `page-hero-x` | Ваш подросток не разговаривает с вами — это не ваша вина |
| `ru/blog.html` | ru | blog-index | `page-hero-x` | индекс статей блога с фильтром по темам |
| `ru/depressiya.html` | ru | page | `page-hero-x` | депрессия: раздел направления |
| `ru/enurez.html` | ru | page | `page-hero-x` | энурез: раздел направления |
| `ru/haqqimda.html` | ru | page | `page-hero-x` | о специалисте: биография, квалификации, подход |
| `ru/index.html` | ru | home | `page-hero` | витрина: герой с портретом, цифры, экосистема, направления, статьи, книги, форма |
| `ru/panik-ataklar.html` | ru | page | `page-hero-x` | панические атаки: раздел направления |
| `ru/program-klinik.html` | ru | page | `page-hero-x` | программа «Клиническая психология» |
| `ru/program-praktikum.html` | ru | page | `page-hero-x` | программу «Практикум» |
| `ru/program-umumi.html` | ru | page | `page-hero-x` | программа «Общая психология» |
| `ru/qanunlar.html` | ru | page | `page-hero-x` | нормативная база: законы и стандарты профессии |
| `ru/samira.html` | ru | page | `page-hero-x` | авторский метод SAMİRA: протокол и обоснование |
| `ru/sosial-fobiya.html` | ru | page | `page-hero-x` | социальная фобия: раздел направления |
| `ru/tehsil.html` | ru | page | `page-hero-x` | программа обучения: институт ДПО, модули, цены, форма записи |
| `ru/template.html` | ru | template | — | служебный шаблон страницы (не индексируется) |
| `ru/valideyn-mektebi.html` | ru | page | `page-hero-x` | родительская школа: курс для родителей |
| `ru/xidmetler.html` | ru | page | `page-hero-x` | каталог услуг: индивидуальная, семейная, подростковая терапия |
| `en/aile-terapiyasi-usaq.html` | en | page | `page-hero-x` | детская и подростковая семейная терапия |
| `en/aile-terapiyasi.html` | en | page | `page-hero-x` | семейная терапия: направления и форматы работы |
| `en/b2b.html` | en | page | `page-hero-x` | корпоративным клиентам: программы для организаций |
| `en/blog-aile-2.html` | en | blog-article | `page-hero-x` | 7 Signs of a Toxic Relationship |
| `en/blog-aile-3.html` | en | blog-article | `page-hero-x` | Family on the Brink of Divorce — Therapy or Separation? |
| `en/blog-aile-4.html` | en | blog-article | `page-hero-x` | How to Argue Constructively as a Couple? |
| `en/blog-aile-5.html` | en | blog-article | `page-hero-x` | How to Rebuild Trust After Infidelity? |
| `en/blog-aile-usaq-2.html` | en | blog-article | `page-hero-x` | Child Behavior Problems — Punishment or Understanding? |
| `en/blog-aile-usaq-3.html` | en | blog-article | `page-hero-x` | A Child After Divorce — How to Help? |
| `en/blog-aile-usaq-4.html` | en | blog-article | `page-hero-x` | School Refusal — 5 Real Causes |
| `en/blog-aile-usaq-5.html` | en | blog-article | `page-hero-x` | Saying "No" to a Child — How to Build Healthy Boundaries? |
| `en/blog-aile.html` | en | blog-article | `page-hero-x` | 5 Principles of Resolving Family Conflicts |
| `en/blog-depressiya-2.html` | en | blog-article | `page-hero-x` | How Does CBT Work for Depression? |
| `en/blog-depressiya-3.html` | en | blog-article | `page-hero-x` | Antidepressants — Facts and Myths |
| `en/blog-depressiya-4.html` | en | blog-article | `page-hero-x` | Postpartum Depression — Recognition and Treatment |
| `en/blog-depressiya-5.html` | en | blog-article | `page-hero-x` | Seasonal Depression (SAD) and Light Therapy |
| `en/blog-depressiya-protokol.html` | en | blog-article | `page-hero-x` | Treatment of Psychogenic Depression |
| `en/blog-depressiya.html` | en | blog-article | `page-hero-x` | How Does Depression Differ from Sadness? |
| `en/blog-enurez-2.html` | en | blog-article | `page-hero-x` | PMNE — Primary Monosymptomatic Nocturnal Enuresis: Complete Guide |
| `en/blog-enurez-3.html` | en | blog-article | `page-hero-x` | How Does the Enuresis Alarm Work? — International Protocol |
| `en/blog-enurez-4.html` | en | blog-article | `page-hero-x` | Desmopressin and Imipramine — Medications for Enuresis |
| `en/blog-enurez-5.html` | en | blog-article | `page-hero-x` | 7 Practical Tips for Parents |
| `en/blog-enurez-protokol.html` | en | blog-article | `page-hero-x` | Nocturnal Enuresis in Children — Modified Alarm Therapy Protocol |
| `en/blog-enurez.html` | en | blog-article | `page-hero-x` | Child Wets the Bed at Night — 5 False Beliefs |
| `en/blog-panik-2.html` | en | blog-article | `page-hero-x` | What Happens in the Brain During a Panic Attack? |
| `en/blog-panik-3.html` | en | blog-article | `page-hero-x` | Agoraphobia — From Panic Attacks to Social Isolation |
| `en/blog-panik-4.html` | en | blog-article | `page-hero-x` | How Does CBT Work for Panic Disorder? |
| `en/blog-panik-5.html` | en | blog-article | `page-hero-x` | 7 Myths About Panic Attacks and Scientific Answers |
| `en/blog-panik.html` | en | blog-article | `page-hero-x` | What to Do During a Panic Attack? |
| `en/blog-psixolog-olmaq-2.html` | en | blog-article | `page-hero-x` | Clinical vs General Psychology — Differences and Choice |
| `en/blog-psixolog-olmaq-3.html` | en | blog-article | `page-hero-x` | How Can a New Psychologist Find Their First Clients? |
| `en/blog-psixolog-olmaq-4.html` | en | blog-article | `page-hero-x` | Supervision — The Psychologist's Permanent Teacher |
| `en/blog-psixolog-olmaq-5.html` | en | blog-article | `page-hero-x` | Self-Care for Psychologists — Protection Against Burnout |
| `en/blog-psixolog-olmaq.html` | en | blog-article | `page-hero-x` | A Good Psychologist Never Runs Out of Work — Why? |
| `en/blog-sosial-fobiya-2.html` | en | blog-article | `page-hero-x` | Fear of Public Speaking — CBT and Exposure |
| `en/blog-sosial-fobiya-3.html` | en | blog-article | `page-hero-x` | Blushing and Sweating — Social Physical Reactions |
| `en/blog-sosial-fobiya-4.html` | en | blog-article | `page-hero-x` | Social Anxiety vs Introversion — What Is the Difference? |
| `en/blog-sosial-fobiya-5.html` | en | blog-article | `page-hero-x` | Social Media Anxiety — A New Form |
| `en/blog-sosial-fobiya.html` | en | blog-article | `page-hero-x` | Social Phobia Is Not Just Shyness |
| `en/blog-yeniyetme.html` | en | blog-article | `page-hero-x` | Your Teenager Won't Talk to You — It's Not Your Fault |
| `en/blog.html` | en | blog-index | `page-hero-x` | индекс статей блога с фильтром по темам |
| `en/depressiya.html` | en | page | `page-hero-x` | депрессия: раздел направления |
| `en/enurez.html` | en | page | `page-hero-x` | энурез: раздел направления |
| `en/haqqimda.html` | en | page | `page-hero-x` | о специалисте: биография, квалификации, подход |
| `en/index.html` | en | home | `page-hero` | витрина: герой с портретом, цифры, экосистема, направления, статьи, книги, форма |
| `en/panik-ataklar.html` | en | page | `page-hero-x` | панические атаки: раздел направления |
| `en/program-klinik.html` | en | page | `page-hero-x` | программа «Клиническая психология» |
| `en/program-praktikum.html` | en | page | `page-hero-x` | программу «Практикум» |
| `en/program-umumi.html` | en | page | `page-hero-x` | программа «Общая психология» |
| `en/qanunlar.html` | en | page | `page-hero-x` | нормативная база: законы и стандарты профессии |
| `en/samira.html` | en | page | `page-hero-x` | авторский метод SAMİRA: протокол и обоснование |
| `en/sosial-fobiya.html` | en | page | `page-hero-x` | социальная фобия: раздел направления |
| `en/tehsil.html` | en | page | `page-hero-x` | программа обучения: институт ДПО, модули, цены, форма записи |
| `en/valideyn-mektebi.html` | en | page | `page-hero-x` | родительская школа: курс для родителей |
| `en/xidmetler.html` | en | page | `page-hero-x` | каталог услуг: индивидуальная, семейная, подростковая терапия |

Файл сгенерирован; раздел «Страницы» пересобирается `python _tools/site-structure-build.py`,
проверяется `python _tools/site-structure-check.py --base http://127.0.0.1:8765`.
