/* =====================================================================
   _tools/freud-ru-royallib.js — русские версии двух книг Фрейда,
   которых нет на русском зеркале freudproject.ru: «Толкование сновидений»
   и «Введение в психоанализ (лекции)».
   Источник: EPUB с royallib.com, скачаны в D:/Документы/ZFreud/royallib/
   (вне репозитория). Главы берутся из toc.ncx источника — не эвристикой.
   Каркас страниц — как у остальных книг (book-template.json, TOC_STYLE,
   сайдбар, d-nav, data-lang-url-*).

   Запуск: node _tools/freud-ru-royallib.js
   ===================================================================== */
const fs = require('fs');
const path = require('path');
const os = require('os');
const { execFileSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const SRC = 'D:/Документы/ZFreud/royallib';
const TPL = JSON.parse(fs.readFileSync(path.join(__dirname, 'book-template.json'), 'utf8'));
const LSV = 6;
const UI = { toc: 'СОДЕРЖАНИЕ', back: 'Книги', home: 'Главная', up: 'Книга', note: 'Примечания', notes: 'Примечания' };

function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
function up(s) { return String(s).toUpperCase(); }
function key(s) {
  return String(s).toLowerCase().replace(/ё/g, 'е')
    .replace(/[’'«»"'`.,:;!?()\[\]{}—–\-]/g, ' ').replace(/\s+/g, ' ').trim();
}
/* кириллица → латиница: адреса глав как у остальных русских книг сайта */
const TRANSLIT = { 'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e', 'ж': 'zh',
  'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p',
  'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh',
  'щ': 'shch', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya' };
function slugify(s) {
  const lat = String(s).toLowerCase().replace(/ё/g, 'е')
    .replace(/[а-я]/g, (c) => (TRANSLIT[c] === undefined ? c : TRANSLIT[c]));
  return lat.replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 44);
}

/* ── источник: EPUB с royallib ── */
function epubParas(file) {
  const tmp = path.join(os.tmpdir(), 'roy-' + Date.now() + '.epub');
  fs.copyFileSync(file, tmp);
  const list = execFileSync('unzip', ['-Z1', tmp], { maxBuffer: 64 * 1024 * 1024 }).toString('utf8')
    .split('\n').map((x) => x.trim()).filter((x) => /\.x?html?$/i.test(x));
  /* порядок файлов — числовой: ch1-2, ch1-10 … */
  const num = (f) => (f.match(/(\d+)-(\d+)\.x?html?$/i) || [0, 0, 0]).slice(1).map(Number);
  list.sort((a, b) => { const x = num(a), y = num(b); return (x[0] - y[0]) || (x[1] - y[1]); });
  const out = [];
  list.forEach((f) => {
    const raw = execFileSync('unzip', ['-p', tmp, f], { maxBuffer: 256 * 1024 * 1024 }).toString('utf8');
    const clean = raw.replace(/<(script|style)[\s\S]*?<\/\1>/gi, ' ')
      .replace(/<\/(p|div|h[1-6]|li|tr)>/gi, '\n').replace(/<br\s*\/?>/gi, '\n')
      .replace(/<[^>]+>/g, ' ');
    clean.split('\n').forEach((x) => {
      const t = x.replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&lt;/g, '<')
        .replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#(\d+);/g, (m, d) => String.fromCharCode(+d))
        .replace(/\s+/g, ' ').trim();
      if (t) out.push(t);
    });
  });
  return out;
}

/* мусор royallib/издательский — в книгу не идёт */
const JUNK = [
  /^royallib/i, /^Скачать/i, /^Читать/i, /^ЛитРес/i, /^litres/i, /^ISBN\b/i, /^©/, /^\(c\)/i,
  /^УДК\b/i, /^ББК\b/i, /^Фрейд З\./i, /^\d+\s*[–-]\s*\d+\s*$/,
  /^Перевод( с немецкого)?:/i, /^Пер\. /i, /^Издательство/i, /^М\.:/i, /^СПб/i, /^Москва/i,
  /^Редактор/i, /^Корректор/i, /^Художник/i, /^Компьютерная верстка/i, /^Подписано/i,
  /^www\./i, /^https?:\/\//i, /^e-?mail/i, /^Тел\./i, /^Электронная версия/i,
  /* подвал/водяные знаки royallib */
  /^Спасибо, что скачали/i, /электронной библиотек/i, /^Приятного чтения/i,
  /^Оставить отзыв о книге/i, /^Все книги автора/i, /^Читайте также/i, /^Наш сайт/i,
  /^Вы можете разместить/i, /^Библиотека Royallib/i,
];
const runHead = (t) => /^(Зигмунд Фрейд|Фрейд З\.|З\. Фрейд)$/i.test(t);
/* примечания: концевой блок «N Текст…» */
const NOTE_TAIL = /^\d{1,3}\s+\S/;

const BOOKS = [
  {
    slug: 'freud-yuxularin-yozumu',
    file: SRC + '/tolkovanie.epub',
    title: 'Толкование сновидений',
    author: 'Зигмунд Фрейд', year: '1900', yearSub: 'Первое издание — 1900', logo: 'ZY',
    chapters: ['Предисловие', 'Введение', 'I. Научная литература по вопросу о сновидениях (до 1900 г.)',
      'II. Метод толкования сновидений', 'III. Сновидение – осуществление желания',
      'IV. Искажающая деятельность сновидения', 'V. Материал и источники сновидений',
      'VI. Работа сновидения', 'VII. Психология процессов сновидения', 'Указатель литературы'],
  },
  {
    slug: 'freud-psixoanalizle-tanishliq',
    file: SRC + '/vvedenie.epub',
    title: 'Введение в психоанализ. Лекции',
    author: 'Зигмунд Фрейд', year: '1917', yearSub: 'Первое издание — 1917', logo: 'PT',
    chapters: ['Предисловие',
      'ПЕРВАЯ ЛЕКЦИЯ. ВВЕДЕНИЕ', 'ВТОРАЯ ЛЕКЦИЯ. ОШИБОЧНЫЕ ДЕЙСТВИЯ',
      'ТРЕТЬЯ ЛЕКЦИЯ. ОШИБОЧНЫЕ ДЕЙСТВИЯ (ПРОДОЛЖЕНИЕ)', 'ЧЕТВЕРТАЯ ЛЕКЦИЯ. ОШИБОЧНЫЕ ДЕЙСТВИЯ (ОКОНЧАНИЕ)',
      'ПЯТАЯ ЛЕКЦИЯ. ТРУДНОСТИ И ПЕРВЫЕ ПОПЫТКИ ПОНИМАНИЯ', 'ШЕСТАЯ ЛЕКЦИЯ ПРЕДПОЛОЖЕНИЯ И ТЕХНИКА ТОЛКОВАНИЯ',
      'СЕДЬМАЯ ЛЕКЦИЯ. ЯВНОЕ СОДЕРЖАНИЕ СНОВИДЕНИЯ И СКРЫТЫЕ ЕГО МЫСЛИ', 'ВОСЬМАЯ ЛЕКЦИЯ. ДЕТСКИЕ СНОВИДЕНИЯ',
      'ДЕВЯТАЯ ЛЕКЦИЯ. ЦЕНЗУРА СНОВИДЕНИЯ', 'ДЕСЯТАЯ ЛЕКЦИЯ. СИМВОЛИКА СНОВИДЕНИЯ',
      'ОДИННАДЦАТАЯ ЛЕКЦИЯ. РАБОТА СНОВИДЕНИЯ', 'ДВЕНАДЦАТАЯ ЛЕКЦИЯ. АНАЛИЗ ОТДЕЛЬНЫХ СНОВИДЕНИЙ',
      'ТРИНАДЦАТАЯ ЛЕКЦИЯ. АРХАИЧЕСКИЕ ЧЕРТЫ И ИНФАНТИЛИЗМ СНОВИДЕНИЯ', 'ЧЕТЫРНАДЦАТАЯ ЛЕКЦИЯ. ИСПОЛНЕНИЕ ЖЕЛАНИЯ',
      'ПЯТНАДЦАТАЯ ЛЕКЦИЯ. СОМНЕНИЯ И КРИТИКА', 'ШЕСТНАДЦАТАЯ ЛЕКЦИЯ. ПСИХОАНАЛИЗ И ПСИХИАТРИЯ',
      'СЕМНАДЦАТАЯ ЛЕКЦИЯ. СМЫСЛ СИМПТОМОВ', 'ВОСЕМНАДЦАТАЯ ЛЕКЦИЯ. ФИКСАЦИЯ НА ТРАВМЕ, БЕССОЗНАТЕЛЬНОЕ',
      'ДЕВЯТНАДЦАТАЯ ЛЕКЦИЯ. СОПРОТИВЛЕНИЕ И ВЫТЕСНЕНИЕ', 'ДВАДЦАТАЯ ЛЕКЦИЯ. СЕКСУАЛЬНАЯ ЖИЗНЬ ЧЕЛОВЕКА',
      'ДВАДЦАТЬ ПЕРВАЯ ЛЕКЦИЯ. РАЗВИТИЕ ЛИБИДО И СЕКСУАЛЬНАЯ ОРГАНИЗАЦИЯ',
      'ДВАДЦАТЬ ВТОРАЯ ЛЕКЦИЯ. ПРЕДСТАВЛЕНИЕ О РАЗВИТИИ И РЕГРЕССИИ. ЭТИОЛОГИЯ',
      'ДВАДЦАТЬ ТРЕТЬЯ ЛЕКЦИЯ. ПУТИ ОБРАЗОВАНИЯ СИМПТОМОВ', 'ДВАДЦАТЬ ЧЕТВЕРТАЯ ЛЕКЦИЯ. ОБЫЧНАЯ НЕРВОЗНОСТЬ',
      'ДВАДЦАТЬ ПЯТАЯ ЛЕКЦИЯ. СТРАХ', 'ДВАДЦАТЬ ШЕСТАЯ ЛЕКЦИЯ. ТЕОРИЯ ЛИБИДО И НАРЦИССИЗМ',
      'ДВАДЦАТЬ СЕДЬМАЯ ЛЕКЦИЯ. ПЕРЕНЕСЕНИЕ', 'ДВАДЦАТЬ ВОСЬМАЯ ЛЕКЦИЯ. АНАЛИТИЧЕСКАЯ ТЕРАПИЯ'],
  },
];

/* ── каркас страниц ── */
const TOC_STYLE = '<style>' +
  '.home-hero{padding:4px 0 2px}' +
  '.home-hero h1.home-title{font-size:clamp(22px,4.4vw,32px);line-height:1.18;letter-spacing:.01em;margin:0}' +
  '.home-hero .sub{font-size:15px;line-height:1.5;margin:10px 0 0;color:var(--text2);letter-spacing:.02em}' +
  '.home-hero .sub:first-of-type{color:var(--text)}' +
  '.book-toc{margin:16px auto 6px}' +
  '.book-toc .toc-chapter{margin:0}' +
  '.content-wrap{padding-top:.6rem;padding-bottom:2rem}' +
  '.content-wrap p{font-size:clamp(16.5px,1.05rem,19px);line-height:1.78;margin:0 0 1.05em;color:var(--text)}' +
  '@media(max-width:600px){.content-wrap{padding-left:18px;padding-right:18px}.content-wrap p{font-size:17.5px;line-height:1.8}}' +
  '.d-nav{display:flex;align-items:center;justify-content:space-between;gap:.5rem;margin:2.2rem 0 .5rem;padding:.7rem 0 0;border-top:1px solid var(--border)}' +
  '.d-nav a{color:var(--text);text-decoration:none;padding:.35rem .7rem;border-radius:6px;font-family:var(--mono,monospace);font-weight:700;font-size:.95rem;white-space:nowrap;max-width:42%;overflow:hidden;text-overflow:ellipsis}' +
  '.d-nav .up{color:var(--gold);font-family:var(--font);font-weight:600}' +
  '.d-nav .dn-name{color:var(--text2);font-weight:400;font-family:var(--font);font-size:.85rem}' +
  '.sidebar .nav-sub-link{padding:7px 14px 7px 18px;font-size:11px;gap:.5rem;line-height:1.4}' +
  '.sidebar .sub-code{flex:0 0 auto;width:auto;white-space:nowrap;margin-right:0;font-size:10px}' +
  '.sidebar .nav-sub-link.is-active{color:var(--gold);border-left-color:var(--gold);background:var(--gold-bg)}' +
  '.content-wrap h3.sub{font-size:1rem;font-weight:700;line-height:1.35;margin:1.5rem 0 .5rem;padding:0;border:0;color:var(--text)}' +
  '.content-wrap .notes{margin:2.4rem 0 0;padding-top:1.1rem;border-top:1px solid var(--border)}' +
  '.content-wrap .notes-title{font-size:.8rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);margin:0 0 .7rem}' +
  '.content-wrap .note{font-size:.92rem;line-height:1.6;margin:0 0 .5em;color:var(--text2)}' +
  '</style>';

function headHtml(b, href, title, desc, depth) {
  const azUrl = 'https://ragimoff.org/books/' + b.slug + '/' + (href || '');
  const ruUrl = 'https://ragimoff.org/books/' + b.slug + '/ru/' + (href || '');
  const alt = '  <link rel="canonical" href="' + ruUrl + '" />\n\n' +
    '  <link rel="alternate" hreflang="az" href="' + azUrl + '" />\n\n' +
    '  <link rel="alternate" hreflang="ru" href="' + ruUrl + '" />\n\n' +
    '  <link rel="alternate" hreflang="x-default" href="' + azUrl + '" />';
  return TPL.head
    .replace('<html lang="az">', '<html data-langs="az,ru" data-lang-url-az="/books/' + b.slug + '/" ' +
      'data-lang-url-ru="/books/' + b.slug + '/ru/" data-lang-avail="az ru" lang="ru">')
    .replace('<link rel="stylesheet" href="style.css">', '<link rel="stylesheet" href="' + (depth ? '../style.css' : 'style.css') + '">')
    .replace(/<title>[\s\S]*?<\/title>/, '<title>' + esc(title) + ' | ' + esc(up(b.title)) + '</title>')
    .replace(/<meta name="description" content="[^"]*"/, '<meta name="description" content="' + esc(desc) + '"')
    .replace(/<meta property="og:title" content="[^"]*"/, '<meta property="og:title" content="' + esc(title) + '"')
    .replace(/<meta property="og:description" content="[^"]*"/, '<meta property="og:description" content="' + esc(desc) + '"')
    .replace(/<meta property="og:url" content="[^"]*"/, '<meta property="og:url" content="' + ruUrl + '"')
    .replace(/"name":"[^"]*","inLanguage":"[^"]*"/, '"name":"' + esc(b.title) + '","inLanguage":"ru"')
    .replace(/"author":\{"@type":"Person","name":"[^"]*"\}/, '"author":{"@type":"Person","name":"' + esc(b.author) + '"}')
    .replace(/\n[ \t]*<link rel="canonical"[\s\S]*?x-default[^>]*>/, '\n' + alt)
    .replace('</head>', TOC_STYLE + '</head>');
}

function bodyTop(b) {
  return TPL.bodyTop
    .replace(/<div class="hdr-logo">[^<]*<\/div>/, '<div class="hdr-logo">' + b.logo + '</div>')
    .replace(/<a href="https:\/\/ragimoff\.org" class="hdr-back"[^>]*>/, '<a href="https://ragimoff.org/ru/" class="hdr-back" title="Вернуться на главную сайта">')
    .replace(/<strong>[^<]*<\/strong>/, '<strong>' + esc(up(b.title)) + '</strong>')
    .replace(/<small>[^<]*<\/small>/, '<small>' + esc(b.author) + ' · ' + esc(b.year) + '</small>')
    .replace('data-lang-switch', 'data-lang-switch data-langs="az,ru" data-lang-avail="az ru"')
    .replace('src="/_lang-switch.js"', 'src="/_lang-switch.js?v=' + LSV + '"');
}

function sidebarHtml(list, idx, pre) {
  const items = list.map((c, i) =>
    '<div class="nav-item"><a href="' + pre + c.slug + '/index.html" class="nav-sub-link' + (i === idx ? ' is-active' : '') + '">' +
    '<span class="sub-code">' + c.num + '</span><span class="sub-name">' + esc(c.short || c.title) + '</span></a></div>').join('\n      ');
  return '<aside class="sidebar" id="sb">\n    <div class="sb-hdr"><a class="sb-site" href="https://ragimoff.org/books/" title="' + UI.back + '">← ' + UI.back + '</a>' +
    '<button class="sb-close" onclick="toggleSb()" aria-label="Закрыть">✕</button></div>\n    <nav>\n      ' +
    '<div class="nav-item"><a href="' + pre + 'index.html" class="nav-link nav-front">' + UI.home + '</a></div>\n      ' +
    items + '\n    </nav>\n  </aside>';
}

function chapterPage(b, list, idx) {
  const ch = list[idx];
  const prev = idx > 0 ? list[idx - 1] : null, next = idx < list.length - 1 ? list[idx + 1] : null;
  const content = '\n<nav class="crumb"><a href="../index.html">‹ ' + esc(b.title) + '</a></nav>\n' +
    '<h1 class="chap-title-wrap"><span class="chap-title">' + esc(ch.title) + '</span></h1>\n' +
    ch.body.map((p) => '<p>' + esc(p) + '</p>').join('\n') + '\n' +
    '<nav class="d-nav">' +
    (prev ? '<a href="../' + prev.slug + '/index.html">← ' + prev.num + ' <span class="dn-name">' + esc(prev.short || prev.title) + '</span></a>' : '<span></span>') +
    '<a class="up" href="../index.html">↑ ' + UI.up + '</a>' +
    (next ? '<a href="../' + next.slug + '/index.html"><span class="dn-name">' + esc(next.short || next.title) + '</span> ' + next.num + ' →</a>' : '<span></span>') +
    '</nav>\n' + TPL.tail;
  return headHtml(b, ch.slug + '/index.html', ch.title, b.title + ' — ' + ch.title, true) + '\n</head>\n' +
    bodyTop(b) + sidebarHtml(list, idx, '../') + TPL.mid + TPL.contentOpen + content;
}

function indexPage(b, list) {
  const cards = list.map((c) =>
    '<div class="toc-chapter"><a href="' + c.slug + '/index.html" class="toc-chapter-title"><span class="toc-name">' + esc(c.title) + '</span></a></div>').join('\n      ');
  const content = '\n<div class="home-hero"><h1 class="home-title">' + esc(up(b.title)) + '</h1>' +
    '<p class="sub">' + esc(b.author) + '</p>' +
    '<p class="sub">' + esc(b.yearSub) + '</p></div>\n' +
    '<section class="book-toc"><h2 class="toc-title">' + esc(UI.toc) + '</h2>\n      ' + cards + '\n    </section>\n';
  return headHtml(b, '', b.title, b.title + ' — ' + b.author, false) + '\n</head>\n' +
    bodyTop(b) + sidebarHtml(list, -1, '') + TPL.mid + TPL.contentOpen + content;
}

/* ── сборка книги ── */
function buildBook(b) {
  const raw = epubParas(b.file);
  const keyed = raw.map(key);
  let cursor = 0;
  const marks = [];
  b.chapters.forEach((title, ci) => {
    const k = key(title);
    let found = -1;
    for (let i = cursor; i < raw.length; i++) {
      if (keyed[i] === k || (k.length >= 18 && keyed[i].startsWith(k))) { found = i; break; }
    }
    if (found < 0) throw new Error(b.slug + ': не найден заголовок главы ' + (ci + 1) + ': ' + title);
    marks.push(found);
    cursor = found + 1;
  });
  const list = [];
  b.chapters.forEach((title, ci) => {
    const from = marks[ci] + 1;
    const to = ci + 1 < marks.length ? marks[ci + 1] : raw.length;
    let paras = raw.slice(from, to).filter((t) =>
      !JUNK.some((re) => re.test(t)) && !runHead(t) && t.replace(/\s+/g, '').length > 1);
    let tail = paras.length;
    while (tail > 0 && NOTE_TAIL.test(paras[tail - 1])) tail--;
    if (paras.length - tail >= 3) paras = paras.slice(0, tail);
    /* примечания вида «133» + текст: склеиваем в один абзац «133. текст» */
    const merged = [];
    for (let i = 0; i < paras.length; i++) {
      if (/^\d{1,3}$/.test(paras[i]) && i + 1 < paras.length) { merged.push(paras[i] + '. ' + paras[i + 1]); i++; }
      else merged.push(paras[i]);
    }
    paras = merged;
    if (paras.length < 2) throw new Error(b.slug + ': пустая глава «' + title + '»');
    list.push({ title, slug: slugify(title) || ('glava-' + (ci + 1)), body: paras, num: String(ci + 1).padStart(2, '0') });
  });
  const dir = path.join(ROOT, 'books', b.slug, 'ru');
  fs.mkdirSync(dir, { recursive: true });
  const style = path.join(ROOT, 'klinik-psixiatriya', 'style.css');
  if (fs.existsSync(style)) fs.copyFileSync(style, path.join(dir, 'style.css'));
  /* старые главы, которых нет в новом списке — убрать */
  const keep = new Set(list.map((c) => c.slug).concat('index.html', 'style.css'));
  fs.readdirSync(dir).filter((f) => !keep.has(f) && fs.statSync(path.join(dir, f)).isDirectory()).forEach((f) =>
    fs.rmSync(path.join(dir, f), { recursive: true, force: true }));
  list.forEach((ch, i) => {
    const d = path.join(dir, ch.slug);
    fs.mkdirSync(d, { recursive: true });
    fs.writeFileSync(path.join(d, 'index.html'), chapterPage(b, list, i), 'utf8');
  });
  fs.writeFileSync(path.join(dir, 'index.html'), indexPage(b, list), 'utf8');
  console.log(b.slug + ' (ru): глав ' + list.length + ' → books/' + b.slug + '/ru/');
  list.forEach((c) => console.log('    ' + c.num + '  ' + c.slug + '   ' + c.title));
  return list;
}

/* AZ-страницы этих книг: у них теперь есть русская версия */
function patchAz(slug) {
  const dir = path.join(ROOT, 'books', slug);
  let n = 0;
  fs.readdirSync(dir).filter((f) => f.endsWith('.html')).forEach((f) => {
    const file = path.join(dir, f);
    let h = fs.readFileSync(file, 'utf8');
    const before = h;
    h = h.replace(/<html[^>]*>/, '<html data-langs="az,ru" data-lang-url-az="/books/' + slug + '/" ' +
      'data-lang-url-ru="/books/' + slug + '/ru/" data-lang-avail="az ru" lang="az">');
    h = h.replace(/src="\/_lang-switch\.js(?:\?v=\d+)?"/, 'src="/_lang-switch.js?v=' + LSV + '"');
    if (h !== before) { fs.writeFileSync(file, h, 'utf8'); n++; }
  });
  return n;
}

let pages = 0;
BOOKS.forEach((b) => { pages += buildBook(b).length + 1; });
BOOKS.forEach((b) => console.log('AZ ' + b.slug + ': страниц с русской парой — ' + patchAz(b.slug)));
console.log('всего страниц:', pages);
