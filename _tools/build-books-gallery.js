/* =====================================================================
   RAGIMOFF · _tools/build-books-gallery.js — книжная галерея на трёх языках
   Собирает books/index.html (AZ), books/ru/index.html (RU), books/en/index.html (EN)
   из одного источника данных. Названия книг — только из самих книг (файлы/страницы),
   ничего не выдумываем. Запуск: node _tools/build-books-gallery.js
   ===================================================================== */
const fs = require('fs');
const path = require('path');

const OUT = path.resolve(__dirname, '..', 'books');
const SITE = 'https://ragimoff.org';

const UI = {
  az: {
    lang: 'az',
    title: 'Kitablar — RAGIMOFF',
    desc: 'RAGIMOFF kitabları: Klinik Psixiatriya, Günahkarlıq Virusu, Şizofreniya, Feniks Erası. Elektron oxu və sifariş.',
    h1: 'Kitablar',
    free: 'Pulsuz',
    authors: {"kenan":"Kənan Rəhimov","samira":"Samirə Rüstəmova / Rəhimova","freud":"Ziqmund Freyd"},
    filterAll: "Bütün müəlliflər",
    filterLabel: "Müəllif",
    searchPh: 'Ad, müəllif və ya il üzrə axtarış…',
    searchAria: 'Kitab axtarışı',
    count: (n) => n + ' kitab',
    read: 'Oxu',
    order: 'Sifariş et',
    modalTitle: 'Kitabın sifarişi',
    bookLabel: 'Kitab',
    nameLabel: 'Ad Soyad',
    namePh: 'Adınız və soyadınız',
    phoneLabel: 'Mobil nömrə',
    submit: 'Sifariş et',
    sending: 'Göndərilir…',
    ok: 'Təşəkkür edirik!<br>Sifarişiniz qeydə alındı — tezliklə sizinlə əlaqə saxlayacağıq.',
    empty: 'Heç nə tapılmadı',
    close: 'Bağla',
    fill: 'Zəhmət olmasa Ad Soyad və Telefon daxil edin.',
    nav: { home: 'Ana Səhifə', edu: 'Təhsil', books: 'Kitablar', blog: 'Blog' },
    footer: { tag: 'Peşəkar nüfuzun ünvanı', ebook: 'Elektron kitab', blog: 'Bloq' },
    href: { home: '/', edu: '/tehsil.html', books: '/books/', blog: '/blog.html' },
  },
  ru: {
    lang: 'ru',
    title: 'Книги — RAGIMOFF',
    desc: 'Книги RAGIMOFF: Клиническая психиатрия, Вирус вины, Шизофрения, Эра Феникса. Чтение онлайн и заказ.',
    h1: 'Книги',
    free: 'Бесплатно',
    authors: {"kenan":"Кенан Рагимов","samira":"Самира Рустамова / Рагимова","freud":"Зигмунд Фрейд"},
    filterAll: "Все авторы",
    filterLabel: "Автор",
    searchPh: 'Поиск по названию, автору или году…',
    searchAria: 'Поиск книг',
    count: (n) => n + ' книг',
    read: 'Читать',
    order: 'Заказать',
    modalTitle: 'Заказ книги',
    bookLabel: 'Книга',
    nameLabel: 'Имя и фамилия',
    namePh: 'Ваше имя и фамилия',
    phoneLabel: 'Мобильный телефон',
    submit: 'Заказать',
    sending: 'Отправляем…',
    ok: 'Спасибо!<br>Заказ принят — мы скоро свяжемся с вами.',
    empty: 'Ничего не найдено',
    close: 'Закрыть',
    fill: 'Пожалуйста, укажите имя и телефон.',
    nav: { home: 'Главная', edu: 'Обучение', books: 'Книги', blog: 'Блог' },
    footer: { tag: 'Адрес профессиональной репутации', ebook: 'Электронная книга', blog: 'Блог' },
    href: { home: '/ru/', edu: '/ru/tehsil.html', books: '/books/ru/', blog: '/ru/blog.html' },
  },
  en: {
    lang: 'en',
    title: 'Books — RAGIMOFF',
    desc: 'RAGIMOFF books: Clinical Psychiatry, The Guilt Virus, Schizophrenia, Phoenix Era. Read online and order.',
    h1: 'Books',
    free: 'Free',
    authors: {"kenan":"Kenan Ragimov","samira":"Samira Rustamova / Ragimova","freud":"Sigmund Freud"},
    filterAll: "All authors",
    filterLabel: "Author",
    searchPh: 'Search by title, author or year…',
    searchAria: 'Search books',
    count: (n) => n + ' books',
    read: 'Read',
    order: 'Order',
    modalTitle: 'Order the book',
    bookLabel: 'Book',
    nameLabel: 'Full name',
    namePh: 'Your full name',
    phoneLabel: 'Mobile phone',
    submit: 'Order',
    sending: 'Sending…',
    ok: 'Thank you!<br>Your order has been received — we will contact you soon.',
    empty: 'Nothing found',
    close: 'Close',
    fill: 'Please enter your name and phone number.',
    nav: { home: 'Home', edu: 'Education', books: 'Books', blog: 'Blog' },
    footer: { tag: 'The address of professional reputation', ebook: 'E-book', blog: 'Blog' },
    href: { home: '/en/', edu: '/en/tehsil.html', books: '/books/en/', blog: '/en/blog.html' },
  },
};

/* Названия — из самих книг: страницы книги психиатрии (4 языка), DOCX «Вина»,
   DOCX «Cinnat/Schizophrenia», страницы «Эры Феникса». Годы и цены — от владельца. */
const BOOKS = [
  {
    id: 'klinik',
    authorKey: 'kenan',
    cover: 'klinik.jpg',
    coverTitle: { az: 'Klinik<br>Psixiatriya', ru: 'Клиническая<br>психиатрия', en: 'Clinical<br>Psychiatry' },
    coverAuthor: { az: 'KƏNAN RƏHİMOV', ru: 'КЕНАН РАГИМОВ', en: 'KENAN RAGIMOV' },
    year: '2026',
    title: { az: 'Klinik Psixiatriya', ru: 'Клиническая психиатрия', en: 'Clinical Psychiatry' },
    meta: {
      az: 'Kənan Rəhimov · 2026 · AZ RU EN TR',
      ru: 'Кенан Рагимов · 2026 · AZ RU EN TR',
      en: 'Kenan Ragimov · 2026 · AZ RU EN TR',
    },
    price: '100 ₼',
    read: { az: '/klinik-psixiatriya/', ru: '/klinik-psixiatriya/ru/', en: '/klinik-psixiatriya/en/' },
  },
  {
    id: 'guilt',
    authorKey: 'kenan',
    cover: 'guilt.jpg',
    coverTitle: { az: 'Günahkarlıq<br>Virusu', ru: 'Вирус<br>вины', en: 'The Guilt<br>Virus' },
    coverAuthor: { az: 'KƏNAN RƏHİMOV', ru: 'КЕНАН РАГИМОВ', en: 'KENAN RAGIMOV' },
    year: '2024',
    title: { az: 'Günahkarlıq Virusu', ru: 'Вирус вины', en: 'The Guilt Virus' },
    meta: {
      az: 'Kənan Rəhimov · 2024 · AZ RU EN',
      ru: 'Кенан Рагимов · 2024 · AZ RU EN',
      en: 'Kenan Ragimov · 2024 · AZ RU EN',
    },
    price: '30 ₼',
    read: { az: '/books/virus-viny/', ru: '/books/virus-viny/ru/', en: '/books/virus-viny/en/' },
  },
  {
    id: 'schizo',
    authorKey: 'kenan',
    cover: 'pandemic.jpg',
    coverTitle: { az: 'Şizofreniya<br>Cinnət Pandemiyası', ru: 'Шизофрения<br>Пандемия безумия', en: 'Schizophrenia<br>A Pandemic of Madness' },
    coverAuthor: { az: 'KƏNAN RƏHİMOV', ru: 'КЕНАН РАГИМОВ', en: 'KENAN RAGIMOV' },
    year: '2026',
    title: { az: 'Şizofreniya. Cinnət pandemiyası', ru: 'Шизофрения. Пандемия безумия', en: 'Schizophrenia. A Pandemic of Madness' },
    meta: {
      az: 'Kənan Rəhimov · 2026 · AZ RU EN',
      ru: 'Кенан Рагимов · 2026 · AZ RU EN',
      en: 'Kenan Ragimov · 2026 · AZ RU EN',
    },
    price: '30 ₼',
    read: { az: '/books/shizofreniya/', ru: '/books/shizofreniya/ru/', en: '/books/shizofreniya/en/' },
  },
  {
    id: 'phoenix',
    authorKey: 'samira',
    cover: 'phoenix.jpg',
    coverTitle: { az: 'Feniks<br>Erası', ru: 'Эра<br>Феникса', en: 'Phoenix<br>Era' },
    coverAuthor: { az: 'SAMİRƏ RÜSTƏMOVA / RƏHİMOVA', ru: 'САМИРА РУСТАМОВА / РАГИМОВА', en: 'SAMIRA RUSTAMOVA / RAGIMOVA' },
    year: '2026',
    title: { az: 'Feniks Erası', ru: 'Эра Феникса', en: 'Feniks Erası' },
    meta: {
      az: 'Samirə Rüstəmova / Rəhimova · 2026 · AZ RU',
      ru: 'Самира Рустамова / Рагимова · 2026 · AZ RU',
      en: 'Samira Rustamova / Ragimova · 2026 · AZ RU',
    },
    price: '50 ₼',
    read: { az: '/books/phoenix-era/', ru: '/books/phoenix-era/ru/', en: null },
  },
  {
    id: 'freud-yuxularin-yozumu',
    authorKey: 'freud',
    cover: 'freud-yuxularin-yozumu.jpg',
    coverTitle: { az: 'Yuxuların<br>yozumu', ru: 'Толкование<br>сновидений', en: 'The Interpretation<br>of Dreams' },
    coverAuthor: { az: 'ZIQMUND FREYD', ru: 'ЗИГМУНД ФРЕЙД', en: 'SIGMUND FREUD' },
    year: '1900',
    title: { az: 'Yuxuların yozumu', ru: 'Толкование сновидений', en: 'The Interpretation of Dreams' },
    meta: {
      az: 'Ziqmund Freyd · 1900 · AZ RU',
      ru: 'Зигмунд Фрейд · 1900 · AZ RU',
      en: 'Sigmund Freud · 1900 · AZ RU',
    },
    price: null,                                  /* только чтение, без заказа */
    langs: ['az', 'ru'],
    read: { az: '/books/freud-yuxularin-yozumu/', ru: '/books/freud-yuxularin-yozumu/ru/', en: null },
  },
  {
    id: 'freud-musa',
    authorKey: 'freud',
    cover: 'freud-musa.jpg',
    coverTitle: { az: 'Musa və<br>təkallahlılıq', ru: 'Человек<br>Моисей', en: 'Moses and<br>Monotheism' },
    coverAuthor: { az: 'ZIQMUND FREYD', ru: 'ЗИГМУНД ФРЕЙД', en: 'SIGMUND FREUD' },
    year: '1939',
    title: { az: 'Musa və təkallahlılıq', ru: 'Человек Моисей и монотеистическая религия', en: 'Moses and Monotheism' },
    meta: {
      az: 'Ziqmund Freyd · 1939 · AZ RU',
      ru: 'Зигмунд Фрейд · 1939 · AZ RU',
      en: 'Sigmund Freud · 1939 · AZ RU',
    },
    price: null,                                  /* только чтение, без заказа */
    langs: ['az', 'ru'],
    read: { az: '/books/freud-musa/', ru: '/books/freud-musa/ru/', en: null },
  },
  {
    /* Наш перевод: введение и четыре статьи. Печатного издания нет — EPUB собран
       из переведённых частей; на сайте книга только на азербайджанском.
       Обложку-иллюстрацию владелец добавит позже (текст карточки уже верен). */
    id: 'freud-totem-ve-tabu',
    authorKey: 'freud',
    cover: 'freud-totem-ve-tabu.jpg',
    coverTitle: { az: 'Totem və<br>Tabu', ru: 'Тотем и<br>табу', en: 'Totem and<br>Taboo' },
    coverAuthor: { az: 'ZIQMUND FREYD', ru: 'ЗИГМУНД ФРЕЙД', en: 'SIGMUND FREUD' },
    year: '1913',
    title: { az: 'Totem və Tabu', ru: 'Тотем и табу', en: 'Totem and Taboo' },
    meta: {
      az: 'Ziqmund Freyd \u00b7 1913 \u00b7 AZ',
      ru: 'Зигмунд Фрейд \u00b7 1913 \u00b7 AZ',
      en: 'Sigmund Freud \u00b7 1913 \u00b7 AZ',
    },
    price: null,
    langs: ['az'],
    read: { az: '/books/freud-totem-ve-tabu/', ru: null, en: null },
  },
  {
    id: 'freud-psixoanalizle-tanishliq',
    authorKey: 'freud',
    cover: 'freud-psixoanalizle-tanishliq.jpg',
    coverTitle: { az: 'Psixoanalizlə<br>ilkin tanışlıq', ru: 'Введение<br>в психоанализ', en: 'Introduction<br>to Psychoanalysis' },
    coverAuthor: { az: 'ZIQMUND FREYD', ru: 'ЗИГМУНД ФРЕЙД', en: 'SIGMUND FREUD' },
    year: '1917',
    title: { az: 'Psixoanalizlə ilkin tanışlıq', ru: 'Введение в психоанализ. Лекции', en: 'Introduction to Psychoanalysis' },
    meta: {
      az: 'Ziqmund Freyd · 1917 · AZ RU',
      ru: 'Зигмунд Фрейд · 1917 · AZ RU',
      en: 'Sigmund Freud · 1917 · AZ RU',
    },
    price: null,                                  /* только чтение, без заказа */
    langs: ['az', 'ru'],
    read: { az: '/books/freud-psixoanalizle-tanishliq/', ru: '/books/freud-psixoanalizle-tanishliq/ru/', en: null },
  },
  {
    id: 'freud-seksualligin-psixologiyasi',
    authorKey: 'freud',
    cover: 'freud-seksualligin-psixologiyasi.jpg',
    coverTitle: { az: 'Seksuallığın<br>psixologiyası', ru: 'Три очерка<br>по теории', en: 'Three Essays on<br>Sexual Theory' },
    coverAuthor: { az: 'ZIQMUND FREYD', ru: 'ЗИГМУНД ФРЕЙД', en: 'SIGMUND FREUD' },
    year: '1905',
    title: { az: 'Seksuallığın psixologiyası', ru: 'Три очерка по теории сексуальности', en: 'Three Essays on the Theory of Sexuality' },
    meta: {
      az: 'Ziqmund Freyd · 1905 · AZ RU',
      ru: 'Зигмунд Фрейд · 1905 · AZ RU',
      en: 'Sigmund Freud · 1905 · AZ RU',
    },
    price: null,                                  /* только чтение, без заказа */
    langs: ['az', 'ru'],
    read: { az: '/books/freud-seksualligin-psixologiyasi/', ru: '/books/freud-seksualligin-psixologiyasi/ru/', en: null },
  },
  {
    id: 'freud-sevgi-mektublari',
    authorKey: 'freud',
    cover: 'freud-sevgi-mektublari.jpg',
    coverTitle: { az: 'Sevgi<br>məktubları', ru: 'Письма<br>Марте', en: 'Letters to<br>Martha' },
    coverAuthor: { az: 'ZIQMUND FREYD', ru: 'ЗИГМУНД ФРЕЙД', en: 'SIGMUND FREUD' },
    /* интервал — по фактическим датам писем в книге (первое 10.06.1882, последнее 20.09.1912),
       а не по годам печатного тома «Die Brautbriefe» (1882–1886): решение владельца 29.09.2026 */
    year: '1882–1912',
    title: { az: 'Sevgi məktubları (1882–1912)', ru: 'Письма Марте Бернайс (1882–1912)', en: 'Letters to Martha Bernays (1882–1912)' },
    meta: {
      az: 'Ziqmund Freyd · 1882–1912 · AZ RU',
      ru: 'Зигмунд Фрейд · 1882–1912 · AZ RU',
      en: 'Sigmund Freud · 1882–1912 · AZ RU',
    },
    price: null,                                  /* только чтение, без заказа */
    langs: ['az', 'ru'],
    read: { az: '/books/freud-sevgi-mektublari/', ru: '/books/freud-sevgi-mektublari/ru/', en: null },
  },
  {
    id: 'freud-aforizmlar',
    authorKey: 'freud',
    cover: 'freud-aforizmlar.jpg',
    coverTitle: { az: 'Aforizmlər', ru: 'Афоризмы', en: 'Aphorisms' },
    coverAuthor: { az: 'ZIQMUND FREYD', ru: 'ЗИГМУНД ФРЕЙД', en: 'SIGMUND FREUD' },
    /* года у сборника нет (решение владельца 29.09.2026): 2014/2015 — год печатного
       издания Qanun, а не год первой публикации; бейдж обложки тогда не выводится */
    year: '',
    title: { az: 'Aforizmlər', ru: 'Афоризмы', en: 'Aphorisms' },
    meta: {
      az: 'Ziqmund Freyd · AZ',
      ru: 'Зигмунд Фрейд · AZ',
      en: 'Sigmund Freud · AZ',
    },
    price: null,                                  /* только чтение, без заказа */
    langs: ['az'],                                /* русской версии нет — есть только AZ */
    read: { az: '/books/freud-aforizmlar/', ru: null, en: null },
  },
  {
    /* «Недовольство культурой» (Das Unbehagen in der Kultur, 1930).
       Русский текст — зеркало freudproject.ru, пост 818 (пер. А.М. Руткевич);
       с 30.09.2026 к нему добавлен НАШ азербайджанский перевод (8 разделов,
       названия по содержанию — авторских у произведения нет). Книга двуязычная:
       «читать» ведёт в версию языка страницы (как у остальных парных книг). */
    id: 'freud-medeniyyetin-sancilari',
    authorKey: 'freud',
    cover: 'freud-medeniyyetin-sancilari.jpg',
    coverTitle: { az: 'Mədəniyyətin<br>sancıları', ru: 'Недовольство<br>культурой', en: 'Civilization and<br>Its Discontents' },
    coverAuthor: { az: 'ZIQMUND FREYD', ru: 'ЗИГМУНД ФРЕЙД', en: 'SIGMUND FREUD' },
    year: '1930',
    title: { az: 'Mədəniyyətin sancıları', ru: 'Недовольство культурой', en: 'Civilization and Its Discontents' },
    meta: {
      az: 'Ziqmund Freyd · 1930 · AZ',
      ru: 'Зигмунд Фрейд · 1930 · AZ',
      en: 'Sigmund Freud · 1930 · AZ',
    },
    price: null,                                  /* только чтение, без заказа */
    langs: ['az', 'ru'],                          /* AZ — наш перевод, RU — зеркало freudproject */
    read: {
      az: '/books/freud-medeniyyetin-sancilari/',
      ru: '/books/freud-medeniyyetin-sancilari/ru/',
      en: '/books/freud-medeniyyetin-sancilari/',
    },
  },
  {
    /* «Flissə məktublar» — НАШ перевод писем Фрейда Вильгельму Флиссу (1887–1904).
       Печатной азербайджанской книги нет, EPUB собран нами; русская версия — зеркало
       freudproject, отдельной страницей на сайт пока не выкладывалась. */
    id: 'freud-fliesse-mektublari',
    authorKey: 'freud',
    cover: 'freud-fliesse-mektublari.jpg',
    coverTitle: { az: 'Flissə<br>məktublar', ru: 'Письма<br>Флиссу', en: 'Letters to<br>Fliess' },
    coverAuthor: { az: 'ZIQMUND FREYD', ru: 'ЗИГМУНД ФРЕЙД', en: 'SIGMUND FREUD' },
    year: '1887–1904',
    title: { az: 'Flissə məktublar (1887–1904)', ru: 'Письма Вильгельму Флиссу (1887–1904)', en: 'Letters to Wilhelm Fliess (1887–1904)' },
    meta: {
      az: 'Ziqmund Freyd · 1887–1904 · AZ',
      ru: 'Зигмунд Фрейд · 1887–1904 · AZ',
      en: 'Sigmund Freud · 1887–1904 · AZ',
    },
    price: null,                                  /* только чтение, без заказа */
    langs: ['az'],
    read: { az: '/books/freud-fliesse-mektublari/', ru: null, en: null },
  },
  {
    id: 'freud-abriss',
    authorKey: 'freud',
    cover: 'freud-abriss.jpg',
    coverTitle: { az: 'Psixoanaliz<br>oçerki', ru: 'Очерк<br>психоанализа', en: 'An Outline of<br>Psycho-Analysis' },
    coverAuthor: { az: 'ZIQMUND FREYD', ru: 'ЗИГМУНД ФРЕЙД', en: 'SIGMUND FREUD' },
    year: '1938',
    title: { az: 'Psixoanaliz oçerki', ru: 'Очерк психоанализа', en: 'An Outline of Psycho-Analysis' },
    meta: {
      az: 'Ziqmund Freyd · 1938 · AZ',
      ru: 'Зигмунд Фрейд · 1938 · AZ',
      en: 'Sigmund Freud · 1938 · AZ',
    },
    price: null,
    langs: ['az', 'ru'],
    read: { az: '/books/freud-abriss/', ru: '/books/freud-abriss/ru/', en: null },
  },
  {
    id: 'freud-bir-illuziyanin-geleceyi',
    authorKey: 'freud',
    cover: 'freud-bir-illuziyanin-geleceyi.jpg',
    coverTitle: { az: 'Bir illüziyanın<br>gələcəyi', ru: 'Будущее<br>одной иллюзии', en: 'The Future<br>of an Illusion' },
    coverAuthor: { az: 'ZIQMUND FREYD', ru: 'ЗИГМУНД ФРЕЙД', en: 'SIGMUND FREUD' },
    year: '1927',
    title: { az: 'Bir illüziyanın gələcəyi', ru: 'Будущее одной иллюзии', en: 'The Future of an Illusion' },
    meta: {
      az: 'Ziqmund Freyd · 1927 · AZ',
      ru: 'Зигмунд Фрейд · 1927 · RU',
      en: 'Sigmund Freud · 1927 · EN',
    },
    price: null,
    langs: ['az', 'ru'],
    read: { az: '/books/freud-bir-illuziyanin-geleceyi/', ru: '/books/freud-bir-illuziyanin-geleceyi/ru/', en: null },
  },
  {
    id: 'freud-gundelik-heyat',
    authorKey: 'freud',
    cover: 'freud-gundelik-heyat.jpg',
    coverTitle: { az: 'Gündəlik həyatın<br>psixopatologiyası', ru: 'Психопатология<br>обыденной жизни', en: 'The Psychopathology<br>of Everyday Life' },
    coverAuthor: { az: 'ZIQMUND FREYD', ru: 'ЗИГМУНД ФРЕЙД', en: 'SIGMUND FREUD' },
    year: '1901',
    title: { az: 'Gündəlik həyatın psixopatologiyası', ru: 'Психопатология обыденной жизни', en: 'The Psychopathology of Everyday Life' },
    meta: {
      az: 'Ziqmund Freyd · 1901 · AZ',
      ru: 'Зигмунд Фрейд · 1901 · RU',
      en: 'Sigmund Freud · 1901 · EN',
    },
    price: null,
    langs: ['az', 'ru'],
    read: { az: '/books/freud-gundelik-heyat/', ru: '/books/freud-gundelik-heyat/ru/', en: null },
  },
  {
    id: 'freud-gwx',
    authorKey: 'freud',
    cover: 'freud-gwx.jpg',
    coverTitle: { az: 'Seçilmiş əsərlər', ru: 'Избранные<br>произведения', en: 'Selected<br>Works' },
    coverAuthor: { az: 'ZIQMUND FREYD', ru: 'ЗИГМУНД ФРЕЙД', en: 'SIGMUND FREUD' },
    year: '1913–1917',
    title: { az: 'Seçilmiş əsərlər 1913–1917', ru: 'Избранные произведения', en: 'Selected Works' },
    meta: {
      az: 'Ziqmund Freyd · 1913–1917 · AZ',
      ru: 'Зигмунд Фрейд · 1913–1917 · RU',
      en: 'Sigmund Freud · 1913–1917 · EN',
    },
    price: null,
    langs: ['az', 'ru'],
    read: { az: '/books/freud-gwx/', ru: '/books/freud-gwx/ru/', en: null },
  },
  {
    id: 'freud-histeriya',
    authorKey: 'freud',
    cover: 'freud-histeriya.jpg',
    coverTitle: { az: 'Histeriya üzrə<br>tədqiqatlar', ru: 'Исследования<br>истерии', en: 'Studies on<br>Hysteria' },
    coverAuthor: { az: 'ZIQMUND FREYD', ru: 'ЗИГМУНД ФРЕЙД', en: 'SIGMUND FREUD' },
    year: '1895',
    title: { az: 'Histeriya üzrə tədqiqatlar', ru: 'Исследования истерии', en: 'Studies on Hysteria' },
    meta: {
      az: 'Ziqmund Freyd · 1895 · AZ',
      ru: 'Зигмунд Фрейд · 1895 · AZ',
      en: 'Sigmund Freud · 1895 · AZ',
    },
    price: null,
    langs: ['az', 'ru'],
    read: { az: '/books/freud-histeriya/', ru: '/books/freud-histeriya/ru/', en: null },
  },
  {
    id: 'freud-jenseits',
    authorKey: 'freud',
    cover: 'freud-jenseits.jpg',
    coverTitle: { az: 'Həzz prinsipinin<br>o tayında', ru: 'По ту сторону<br>принципа удовольствия', en: 'Beyond the<br>Pleasure Principle' },
    coverAuthor: { az: 'ZIQMUND FREYD', ru: 'ЗИГМУНД ФРЕЙД', en: 'SIGMUND FREUD' },
    year: '1920',
    title: { az: 'Həzz prinsipinin o tayında', ru: 'По ту сторону принципа удовольствия', en: 'Beyond the Pleasure Principle' },
    meta: {
      az: 'Ziqmund Freyd · 1920 · AZ',
      ru: 'Зигмунд Фрейд · 1920 · RU',
      en: 'Sigmund Freud · 1920 · EN',
    },
    price: null,
    langs: ['az', 'ru'],
    read: { az: '/books/freud-jenseits/', ru: '/books/freud-jenseits/ru/', en: null },
  },
  {
    id: 'freud-manee-simptom-qorxu',
    authorKey: 'freud',
    cover: 'freud-manee-simptom-qorxu.jpg',
    coverTitle: { az: 'Maneə, simptom<br>və qorxu', ru: 'Торможение,<br>симптом и тревога', en: 'Inhibitions,<br>Symptoms and Anxiety' },
    coverAuthor: { az: 'ZIQMUND FREYD', ru: 'ЗИГМУНД ФРЕЙД', en: 'SIGMUND FREUD' },
    year: '1926',
    title: { az: 'Maneə, simptom və qorxu', ru: 'Торможение, симптом и тревога', en: 'Inhibitions, Symptoms and Anxiety' },
    meta: {
      az: 'Ziqmund Freyd · 1926 · AZ',
      ru: 'Зигмунд Фрейд · 1926 · RU',
      en: 'Sigmund Freud · 1926 · EN',
    },
    price: null,
    langs: ['az', 'ru'],
    read: { az: '/books/freud-manee-simptom-qorxu/', ru: '/books/freud-manee-simptom-qorxu/ru/', en: null },
  },
  {
    id: 'freud-massen',
    authorKey: 'freud',
    cover: 'freud-massen.jpg',
    coverTitle: { az: 'Kütlə psixologiyası<br>və Mən-analizi', ru: 'Психология масс<br>и анализ «Я»', en: 'Group Psychology and<br>the Analysis of the Ego' },
    coverAuthor: { az: 'ZIQMUND FREYD', ru: 'ЗИГМУНД ФРЕЙД', en: 'SIGMUND FREUD' },
    year: '1921',
    title: { az: 'Kütlə psixologiyası və Mən-analizi', ru: 'Психология масс и анализ «Я»', en: 'Group Psychology and the Analysis of the Ego' },
    meta: {
      az: 'Ziqmund Freyd · 1921 · AZ',
      ru: 'Зигмунд Фрейд · 1921 · RU',
      en: 'Sigmund Freud · 1921 · EN',
    },
    price: null,
    langs: ['az', 'ru'],
    read: { az: '/books/freud-massen/', ru: '/books/freud-massen/ru/', en: null },
  },
  {
    id: 'freud-men-ve-o',
    authorKey: 'freud',
    cover: 'freud-men-ve-o.jpg',
    coverTitle: { az: 'Mən<br>və O', ru: '«Я» и «Оно»', en: 'The Ego and the Id' },
    coverAuthor: { az: 'ZIQMUND FREYD', ru: 'ЗИГМУНД ФРЕЙД', en: 'SIGMUND FREUD' },
    year: '1923',
    title: { az: 'Mən və O', ru: '«Я» и «Оно»', en: 'The Ego and the Id' },
    meta: {
      az: 'Ziqmund Freyd · 1923 · AZ',
      ru: 'Зигмунд Фрейд · 1923 · RU',
      en: 'Sigmund Freud · 1923 · EN',
    },
    price: null,
    langs: ['az', 'ru'],
    read: { az: '/books/freud-men-ve-o/', ru: '/books/freud-men-ve-o/ru/', en: null },
  },
  {
    id: 'freud-metapsixologiya',
    authorKey: 'freud',
    cover: 'freud-metapsixologiya.jpg',
    coverTitle: { az: 'Metapsixologiya', ru: 'Метапсихология', en: 'Metapsychology' },
    coverAuthor: { az: 'ZIQMUND FREYD', ru: 'ЗИГМУНД ФРЕЙД', en: 'SIGMUND FREUD' },
    year: '1915',
    title: { az: 'Metapsixologiya', ru: 'Метапсихология', en: 'Metapsychology' },
    meta: {
      az: 'Ziqmund Freyd · 1915 · AZ',
      ru: 'Зигмунд Фрейд · 1915 · RU',
      en: 'Sigmund Freud · 1915 · EN',
    },
    price: null,
    langs: ['az', 'ru'],
    read: { az: '/books/freud-metapsixologiya/', ru: '/books/freud-metapsixologiya/ru/', en: null },
  },
  {
    id: 'freud-yeni-muhazireler',
    authorKey: 'freud',
    cover: 'freud-yeni-muhazireler.jpg',
    coverTitle: { az: 'Yeni<br>mühazirələr', ru: 'Новые лекции<br>по психоанализу', en: 'New Introductory<br>Lectures on Psycho-Analysis' },
    coverAuthor: { az: 'ZIQMUND FREYD', ru: 'ЗИГМУНД ФРЕЙД', en: 'SIGMUND FREUD' },
    year: '1933',
    title: { az: 'Yeni mühazirələr', ru: 'Новые лекции по психоанализу', en: 'New Introductory Lectures on Psycho-Analysis' },
    meta: {
      az: 'Ziqmund Freyd · 1933 · AZ',
      ru: 'Зигмунд Фрейд · 1933 · RU',
      en: 'Sigmund Freud · 1933 · EN',
    },
    price: null,
    langs: ['az', 'ru'],
    read: { az: '/books/freud-yeni-muhazireler/', ru: '/books/freud-yeni-muhazireler/ru/', en: null },
  },
  {
    id: 'freud-yumor',
    authorKey: 'freud',
    cover: 'freud-yumor.jpg',
    coverTitle: { az: 'Yumor və onun<br>qeyri-şüurla əlaqəsi', ru: 'Остроумие и его<br>отношение к бессознательному', en: 'Jokes and Their Relation<br>to the Unconscious' },
    coverAuthor: { az: 'ZIQMUND FREYD', ru: 'ЗИГМУНД ФРЕЙД', en: 'SIGMUND FREUD' },
    year: '1905',
    title: { az: 'Yumor və onun qeyri-şüurla əlaqəsi', ru: 'Остроумие и его отношение к бессознательному', en: 'Jokes and Their Relation to the Unconscious' },
    meta: {
      az: 'Ziqmund Freyd · 1905 · AZ',
      ru: 'Зигмунд Фрейд · 1905 · RU',
      en: 'Sigmund Freud · 1905 · EN',
    },
    price: null,
    langs: ['az', 'ru'],
    read: { az: '/books/freud-yumor/', ru: '/books/freud-yumor/ru/', en: null },
  },
];

function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

/* «читать» ведёт на версию того же языка; если её нет — на доступную (не битая ссылка) */
function readFor(book, code) {
  const r = book.read || {};
  if (r[code]) return r[code];
  const langs = book.langs && book.langs.length ? book.langs : ['az'];
  for (const c of langs) if (r[c]) return r[c];
  return null;
}

function card(book, code, ui) {
  const read = readFor(book, code);
  const cover = '<div class="cover" style="--tex:url(\'/books/covers/' + book.cover + '\')">' +
    '<span class="cover__frame" aria-hidden="true"></span>' +
    '<span class="cover__author">' + esc(book.coverAuthor[code]) + '</span>' +
    '<span class="cover__title">' + book.coverTitle[code] + '</span>' +
    (book.year ? '<span class="cover__year">' + book.year + '</span>' : '') +
    '</div>';
  const orderValue = book.title[code] + ' · ' + book.price;
  const canOrder = !!book.price;                 /* без цены — только чтение */
  return '        <article class="card" data-author="' + book.authorKey + '" data-title="' + esc(book.title[code]) + '">\n' +
    (read ? '          <a class="card__cover" href="' + read + '">\n' + cover + '\n          </a>\n'
          : '          <div class="card__cover">\n' + cover + '\n          </div>\n') +
    '          <div class="card__body">\n' +
    '            <h2 class="card__title">' + esc(book.title[code]) + '</h2>\n' +
    '            <p class="card__meta">' + esc(book.meta[code]) + '</p>\n' +
    '            <p class="card__price">' + esc(book.price || ui.free) + '</p>\n' +
    '            <div class="card__cta">\n' +
    (read ? '              <a class="btn" href="' + read + '">' + ui.read + ' <span aria-hidden="true">→</span></a>\n' : '') +
    (canOrder ? '              <button class="btn' + (read ? ' btn--ghost' : '') + '" data-order="' + esc(book.title[code]) + '" data-price="' + esc(book.price) + '">' + ui.order + '</button>\n' : '') +
    '            </div>\n' +
    '          </div>\n' +
    '        </article>';
}

function page(code) {
  const ui = UI[code];
  /* карточки — секциями по авторам */
  const AUTHOR_ORDER = ['kenan', 'samira', 'freud'];
  const cards = AUTHOR_ORDER.map((g) => {
    const list = BOOKS.filter((b) => b.authorKey === g);
    if (!list.length) return '';
    return '        <h2 class="author-sec" data-author="' + g + '">' + esc(ui.authors[g]) + '</h2>\n\n' +
      list.map((b) => card(b, code, ui)).join('\n\n');
  }).filter(Boolean).join('\n\n');
  /* в форме заказа — только книги с ценой: у бесплатных (price: null) печатного
     тиража нет, и раньше они выводились строкой «Название — null» */
  const options = BOOKS.filter((b) => b.price).map((b) => '            <option value="' + esc(b.title[code] + ' · ' + b.price) + '">' + esc(b.title[code]) + ' — ' + esc(b.price) + '</option>').join('\n');
  const alts = ['az', 'ru', 'en'].map((c) =>
    '  <link rel="alternate" hreflang="' + c + '" href="' + SITE + (c === 'az' ? '/books/' : '/books/' + c + '/') + '">').join('\n');
  return `<!doctype html>
<html lang="${code}" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="theme-color" content="#07090E">
  <title>${ui.title}</title>
  <meta name="description" content="${ui.desc}">
  <link rel="canonical" href="${SITE}${ui.href.books}">
${alts}
  <link rel="icon" href="/favicon.ico">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,400&family=IBM+Plex+Mono:wght@400;500&family=Montserrat:wght@300;400;500;600&display=swap" rel="stylesheet">
  <!-- books.css версионируем: иначе после правки у владельца остаётся старый CSS из кэша -->
  <link rel="stylesheet" href="/books/books.css?v=4">
  <!-- страховка на случай уже закэшированного старого books.css: в нём .card{display:flex}
       перебивал браузерное [hidden]{display:none}, и скрытые фильтром карточки оставались
       на странице. То же правило есть в books/books.css — здесь оно работает с первой загрузки. -->
  <style>[hidden] { display: none !important; }</style>
</head>
<body>

  <!-- ─────────────────────── ШАПКА ─────────────────────── -->
  <header class="hdr">
    <div class="wrap hdr__in">
      <a class="logo" href="${ui.href.home}">
        <span class="logo__t">RAGIMOFF<em>.</em></span>
        <span class="logo__s">${esc(ui.footer.tag)}</span>
      </a>
      <span data-lang-switch data-langs="az,ru,en"></span>
      <nav class="nav" aria-label="Naviqasiya">
        <a href="${ui.href.home}">${esc(ui.nav.home)}</a>
        <a href="${ui.href.edu}">${esc(ui.nav.edu)}</a>
        <a href="${ui.href.books}">${esc(ui.nav.books)}</a>
        <a href="${ui.href.blog}">${esc(ui.nav.blog)}</a>
      </nav>
    </div>
  </header>

  <main class="wrap">

    <!-- ─────────────────────── КНИГИ ─────────────────────── -->
    <section class="sec" id="kitablar">
      <h1 class="sr-only">${esc(ui.h1)}</h1>

      <div class="toolbar">
        <label class="search">
          <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.6-3.6"/></svg>
          <input type="search" id="q" placeholder="${esc(ui.searchPh)}" aria-label="${esc(ui.searchAria)}" autocomplete="off">
        </label>
        <span class="count" id="count">${ui.count(BOOKS.length)}</span>
      </div>

      <div class="afilter" id="afilter">
        <span class="afilter__label">${esc(ui.filterLabel)}</span>
        <button class="chip is-on" data-author="">${esc(ui.filterAll)}</button>
        <button class="chip" data-author="kenan">${esc(ui.authors.kenan)}</button>
        <button class="chip" data-author="samira">${esc(ui.authors.samira)}</button>
        <button class="chip" data-author="freud">${esc(ui.authors.freud)}</button>
      </div>

      <div class="grid">

${cards}

      </div>
    </section>

  </main>

  <!-- ─────────────────────── ФУТЕР ─────────────────────── -->
  <footer class="ft">
    <div class="wrap ft__grid">
      <a class="logo" href="${ui.href.home}">
        <span class="logo__t">RAGIMOFF<em>.</em></span>
        <span class="logo__s">${esc(ui.footer.tag)}</span>
      </a>
      <nav class="ft__nav" aria-label="Futermenü">
        <a href="${ui.href.home}">${esc(ui.nav.home)}</a>
        <a href="${ui.href.books}">${esc(ui.nav.books)}</a>
        <a href="${ui.href.blog}">${esc(ui.footer.blog)}</a>
        <a href="https://t.me/ragimoff">Telegram</a>
        <a href="mailto:info@ragimoff.org">info@ragimoff.org</a>
      </nav>
      <span class="mono">© 2026 RAGIMOFF</span>
    </div>
  </footer>

  <!-- ─────────── ФОРМА ЗАКАЗА (та же механика, что на сайте) ─────────── -->
  <div class="modal" data-modal aria-hidden="true">
    <div class="modal__scrim" data-close></div>
    <div class="modal__box" role="dialog" aria-modal="true" aria-labelledby="o-title">
      <button class="modal__x" data-close aria-label="${esc(ui.close)}">✕</button>
      <h2 class="h2" id="o-title">${esc(ui.modalTitle)}</h2>
      <p class="modal__sub" id="o-sub"></p>
      <form id="order-form" action="/api/book-order" method="POST" novalidate>
        <label class="field">
          <span>${esc(ui.bookLabel)}</span>
          <select id="o-book" name="book" required>
${options}
          </select>
        </label>
        <label class="field">
          <span>${esc(ui.nameLabel)}</span>
          <input id="o-name" type="text" name="name" placeholder="${esc(ui.namePh)}" autocomplete="name" required>
        </label>
        <label class="field">
          <span>${esc(ui.phoneLabel)}</span>
          <input id="o-phone" type="tel" name="phone" placeholder="+994 XX XXX XX XX" autocomplete="tel" required>
        </label>
        <button class="btn btn--main" type="submit">${esc(ui.submit)}</button>
      </form>
      <div class="modal__ok" id="o-ok" hidden>
        ${ui.ok}
      </div>
    </div>
  </div>

  <script>
    window.__booksUI = ${JSON.stringify({ sending: ui.sending, submit: ui.submit, fill: ui.fill, empty: ui.empty, count: code === 'ru' ? '%n книг' : (code === 'en' ? '%n books' : '%n kitab') })};
  </script>
  <script src="/books/books.js?v=9" defer></script>
  <script src="/_lang-switch.js?v=9" defer></script>
</body>
</html>
`;
}

['az', 'ru', 'en'].forEach((code) => {
  const dir = code === 'az' ? OUT : path.join(OUT, code);
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, 'index.html'), page(code), 'utf8');
  console.log('собрано:', path.relative(path.resolve(__dirname, '..'), path.join(dir, 'index.html')));
});
