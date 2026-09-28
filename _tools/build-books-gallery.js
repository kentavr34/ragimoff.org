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
    cover: 'freud.jpg',
    coverTitle: { az: 'Yuxuların yozumu', ru: 'Yuxuların yozumu', en: 'Yuxuların yozumu' },
    coverAuthor: { az: 'ZIQMUND FREYD', ru: 'ЗИГМУНД ФРЕЙД', en: 'SIGMUND FREUD' },
    year: '2026',
    title: { az: 'Yuxuların yozumu', ru: 'Yuxuların yozumu', en: 'Yuxuların yozumu' },
    meta: { az: 'Ziqmund Freyd · 2026 · AZ', ru: 'Зигмунд Фрейд · 2026 · AZ', en: 'Sigmund Freud · 2026 · AZ' },
    price: null,                                  /* только чтение, без заказа */
    read: { az: '/books/freud-yuxularin-yozumu/', ru: '/books/freud-yuxularin-yozumu/', en: '/books/freud-yuxularin-yozumu/' },
  },
  {
    id: 'freud-musa',
    authorKey: 'freud',
    cover: 'freud.jpg',
    coverTitle: { az: 'Musa və təkallahlılıq', ru: 'Musa və təkallahlılıq', en: 'Musa və təkallahlılıq' },
    coverAuthor: { az: 'ZIQMUND FREYD', ru: 'ЗИГМУНД ФРЕЙД', en: 'SIGMUND FREUD' },
    year: '2026',
    title: { az: 'Musa və təkallahlılıq', ru: 'Musa və təkallahlılıq', en: 'Musa və təkallahlılıq' },
    meta: { az: 'Ziqmund Freyd · 2026 · AZ', ru: 'Зигмунд Фрейд · 2026 · AZ', en: 'Sigmund Freud · 2026 · AZ' },
    price: null,                                  /* только чтение, без заказа */
    read: { az: '/books/freud-musa/', ru: '/books/freud-musa/', en: '/books/freud-musa/' },
  },
  {
    id: 'freud-psixoanalizle-tanishliq',
    authorKey: 'freud',
    cover: 'freud.jpg',
    coverTitle: { az: 'Psixoanalizlə ilkin tanışlıq', ru: 'Psixoanalizlə ilkin tanışlıq', en: 'Psixoanalizlə ilkin tanışlıq' },
    coverAuthor: { az: 'ZIQMUND FREYD', ru: 'ЗИГМУНД ФРЕЙД', en: 'SIGMUND FREUD' },
    year: '2026',
    title: { az: 'Psixoanalizlə ilkin tanışlıq', ru: 'Psixoanalizlə ilkin tanışlıq', en: 'Psixoanalizlə ilkin tanışlıq' },
    meta: { az: 'Ziqmund Freyd · 2026 · AZ', ru: 'Зигмунд Фрейд · 2026 · AZ', en: 'Sigmund Freud · 2026 · AZ' },
    price: null,                                  /* только чтение, без заказа */
    read: { az: '/books/freud-psixoanalizle-tanishliq/', ru: '/books/freud-psixoanalizle-tanishliq/', en: '/books/freud-psixoanalizle-tanishliq/' },
  },
  {
    id: 'freud-seksualligin-psixologiyasi',
    authorKey: 'freud',
    cover: 'freud.jpg',
    coverTitle: { az: 'Seksuallığın psixologiyası', ru: 'Seksuallığın psixologiyası', en: 'Seksuallığın psixologiyası' },
    coverAuthor: { az: 'ZIQMUND FREYD', ru: 'ЗИГМУНД ФРЕЙД', en: 'SIGMUND FREUD' },
    year: '2026',
    title: { az: 'Seksuallığın psixologiyası', ru: 'Seksuallığın psixologiyası', en: 'Seksuallığın psixologiyası' },
    meta: { az: 'Ziqmund Freyd · 2026 · AZ', ru: 'Зигмунд Фрейд · 2026 · AZ', en: 'Sigmund Freud · 2026 · AZ' },
    price: null,                                  /* только чтение, без заказа */
    read: { az: '/books/freud-seksualligin-psixologiyasi/', ru: '/books/freud-seksualligin-psixologiyasi/', en: '/books/freud-seksualligin-psixologiyasi/' },
  },
  {
    id: 'freud-sevgi-mektublari',
    authorKey: 'freud',
    cover: 'freud.jpg',
    coverTitle: { az: 'Sevgi məktubları', ru: 'Sevgi məktubları', en: 'Sevgi məktubları' },
    coverAuthor: { az: 'ZIQMUND FREYD', ru: 'ЗИГМУНД ФРЕЙД', en: 'SIGMUND FREUD' },
    year: '2026',
    title: { az: 'Sevgi məktubları', ru: 'Sevgi məktubları', en: 'Sevgi məktubları' },
    meta: { az: 'Ziqmund Freyd · 2026 · AZ', ru: 'Зигмунд Фрейд · 2026 · AZ', en: 'Sigmund Freud · 2026 · AZ' },
    price: null,                                  /* только чтение, без заказа */
    read: { az: '/books/freud-sevgi-mektublari/', ru: '/books/freud-sevgi-mektublari/', en: '/books/freud-sevgi-mektublari/' },
  },
];

function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

function card(book, code, ui) {
  const read = book.read && book.read[code];
  const cover = '<div class="cover" style="--tex:url(\'/books/covers/' + book.cover + '\')">' +
    '<span class="cover__frame" aria-hidden="true"></span>' +
    '<span class="cover__author">' + esc(book.coverAuthor[code]) + '</span>' +
    '<span class="cover__title">' + book.coverTitle[code] + '</span>' +
    '<span class="cover__year">' + book.year + '</span>' +
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
  const options = BOOKS.map((b) => '            <option value="' + esc(b.title[code] + ' · ' + b.price) + '">' + esc(b.title[code]) + ' — ' + esc(b.price) + '</option>').join('\n');
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
  <link rel="stylesheet" href="/books/books.css">
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
  <script src="/books/books.js?v=4" defer></script>
  <script src="/_lang-switch.js?v=4" defer></script>
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
