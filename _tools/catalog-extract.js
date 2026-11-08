/* =====================================================================
   RAGIMOFF · _tools/catalog-extract.js — снять каталог книг с ЖИВЫХ страниц
   (08.11.2026). Читает books/index.html, books/ru/index.html, books/en/index.html и пишет:
     _tools/catalog.json                 — данные карточек и баннера коллекции (один источник);
     _tools/catalog-shell/books.<яз>.html — «оболочка» страницы (шапка, стили, футер, скрипты)
                                          с метками <!--@@BANNER@@-->, <!--@@CARDS@@-->, <!--@@OPTIONS@@-->.
   Генератор build-books-gallery.js собирает страницы обратно из этих файлов.
   Нужен, если живую страницу правили руками: снять заново и сверить (dry-run).
   Запуск: node _tools/catalog-extract.js [--force]  (без --force не перезаписывает готовый catalog.json)
   ===================================================================== */
const fs = require('fs');
const path = require('path');

const SITE = path.resolve(__dirname, '..');
const LANGS = ['az', 'ru', 'en'];
const PAGE = (c) => path.join(SITE, 'books', c === 'az' ? '' : c, 'index.html');
const OUT_JSON = path.join(__dirname, 'catalog.json');
const SHELL_DIR = path.join(__dirname, 'catalog-shell');

if (fs.existsSync(OUT_JSON) && !process.argv.includes('--force')) {
  console.error('catalog.json уже есть — перезапись только с --force (правки в нём будут потеряны).');
  process.exit(1);
}

const unq = (s) => s.replace(/&quot;/g, '"');
function must(re, s, what) {
  const m = s.match(re);
  if (!m) throw new Error('не найдено: ' + what);
  return m;
}

/* ── карточка ── */
const ART_RE = /<article class="card( card--soon)?" data-author="(\w+)" data-title="([^"]*)">\n([\s\S]*?)\n {8}<\/article>/g;
function parseCard(m) {
  const [, soon, author, dataTitle, body] = m;
  const c = { soon: !!soon, author, dataTitle };
  const cov = must(/^ {10}(?:<a class="card__cover" href="([^"]*)">|<div class="card__cover">)\n(<div class="cover[^"]*"[^>]*>[\s\S]*?<\/div>)\n {10}<\/(?:a|div)>\n/, body, 'обложка');
  c.coverHref = cov[1] || null;
  const cv = cov[2];
  let mm;
  if ((mm = cv.match(/^<div class="cover" style="--tex:url\('\/books\/covers\/([^']*)'\)"><span class="cover__frame" aria-hidden="true"><\/span><span class="cover__author">([^<]*)<\/span><span class="cover__title">(.*?)<\/span><span class="cover__year">([^<]*)<\/span><\/div>$/))) {
    c.style = 'classic'; [, c.cover, c.coverAuthor, c.coverTitle, c.coverYear] = mm;
  } else if ((mm = cv.match(/^<div class="cover cover--art" style="--tex:url\(&quot;\/books\/covers\/([^&]*)&quot;\)"><span class="cover__author">([^<]*)<\/span><span class="cover__rule" aria-hidden="true"><\/span><span class="cover__title">(.*?)<\/span><span class="cover__year">([^<]*)<\/span><\/div>$/))) {
    c.style = 'art'; [, c.cover, c.coverAuthor, c.coverTitle, c.coverYear] = mm;
  } else throw new Error('неизвестная обложка: ' + cv);
  const rest = body.slice(cov[0].length);
  mm = must(/^ {10}<div class="card__body">\n {12}<h2 class="card__title">(.*?)<\/h2>\n {12}<p class="card__meta">(.*?)<\/p>\n {12}<p class="card__price">(.*?)<\/p>\n([\s\S]*?) {10}<\/div>$/, rest, 'тело карточки ' + dataTitle);
  [, c.title, c.meta, c.priceText] = mm;
  const cta = mm[4];
  c.read = null; c.readClass = null; c.readLabel = null; c.cart = null;
  if (cta) {
    const r = cta.match(/<a class="(btn(?: btn--read)?)" href="([^"]*)">([^<]*) <span aria-hidden="true">→<\/span><\/a>/);
    if (r) { c.readClass = r[1]; c.read = r[2]; c.readLabel = r[3]; }
    const b = cta.match(/<button class="btn btn--cart" type="button" data-cart-btn="1" data-order="([^"]*)" data-price="([^"]*)">([^<]*)<\/button>/);
    if (b) c.cart = { order: b[1], price: b[2], label: b[3] };
    const rebuilt = ' '.repeat(12) + '<div class="card__cta">\n' +
      (r ? ' '.repeat(14) + r[0] + '\n' : '') + (b ? ' '.repeat(14) + b[0] + '\n' : '') + ' '.repeat(12) + '</div>\n';
    if (rebuilt !== cta) throw new Error('непонятный блок кнопок: ' + dataTitle + '\n' + cta);
  }
  return c;
}

/* ── баннер коллекции ── */
const BANNER_RE = /    <section class="coll-banner">\n[\s\S]*?\n    <\/section>\n/;
function parseBanner(s) {
  const g = (re, what) => must(re, s, 'баннер: ' + what)[1];
  return {
    author: g(/<span class="coll-banner__author">([^<]*)<\/span>/, 'author'),
    coverTitle: g(/<span class="coll-banner__title">(.*?)<\/span>/, 'title'),
    countText: g(/<span class="coll-banner__count">([^<]*)<\/span>/, 'count'),
    tag: g(/<span class="coll-banner__tag">([^<]*)<\/span>/, 'tag'),
    heading: g(/<h2 class="coll-banner__h">([^<]*)<\/h2>/, 'h'),
    text: g(/<p class="coll-banner__p">\n([\s\S]*?)\n {10}<\/p>/, 'p'),
    oldText: g(/<span class="coll-banner__old">([^<]*)<\/span>/, 'old'),
    newText: g(/<span class="coll-banner__new">([^<]*)<\/span>/, 'new'),
    saveText: g(/<span class="coll-banner__save">([^<]*)<\/span>/, 'save'),
    note: g(/<p class="coll-banner__note">\n([\s\S]*?)\n {10}<\/p>/, 'note'),
    order: g(/data-order="([^"]*)" data-price/, 'order'),
    priceAttr: g(/data-order="[^"]*" data-price="([^"]*)"/, 'price'),
    collection: g(/data-collection="([^"]*)"/, 'collection'),
    discount: g(/data-discount="([^"]*)"/, 'discount'),
    btnFull: g(/<span class="cb-full">([^<]*)<\/span>/, 'full'),
    btnShort: g(/<span class="cb-short">([^<]*)<\/span>/, 'short'),
    hint: g(/<p class="coll-banner__hint">\n([\s\S]*?)\n {10}<\/p>/, 'hint'),
  };
}

const pages = {};
for (const c of LANGS) {
  const html = fs.readFileSync(PAGE(c), 'utf8');
  const bm = html.match(BANNER_RE);
  const cards = [...html.matchAll(ART_RE)].map(parseCard);
  /* заголовки разделов по авторам */
  const secs = [...html.matchAll(/<h2 class="author-sec" data-author="(\w+)"( id="([^"]*)")?>([^<]*)<\/h2>/g)]
    .map((m) => ({ author: m[1], id: m[3] || null, heading: m[4] }));
  /* блок карточек: от первого заголовка раздела до конца последней карточки */
  const first = html.indexOf('        <h2 class="author-sec"');
  const lastArt = html.lastIndexOf('</article>') + '</article>'.length;
  /* варианты формы заказа */
  const opts = [...html.matchAll(/ {12}<option value="([^"]*)">([^<]*)<\/option>\n/g)];
  let shell = html.slice(0, first) + '<!--@@CARDS@@-->' + html.slice(lastArt);
  if (bm) shell = shell.replace(bm[0], '<!--@@BANNER@@-->');
  if (opts.length) {
    const a = shell.indexOf(opts[0][0]);
    const last = opts[opts.length - 1];
    const z = shell.indexOf(last[0]) + last[0].length;
    shell = shell.slice(0, a) + '<!--@@OPTIONS@@-->' + shell.slice(z);
  }
  pages[c] = { html, shell, banner: bm ? parseBanner(bm[0]) : null, cards, secs, options: opts.map((o) => o[1]) };
}

/* ── слияние по языкам: книга = одна запись, тексты — {az, ru, en} ── */
const n = pages.az.cards.length;
for (const c of LANGS) if (pages[c].cards.length !== n) throw new Error('разное число карточек: ' + c);
const per = (f) => { const o = {}; LANGS.forEach((c, i) => { o[c] = f(c, i); }); return o; };
const collapse = (o) => (LANGS.every((c) => o[c] === o.az) ? o.az : o);

const ui = per((c) => {
  const any = pages[c].cards.find((k) => k.cart);
  const rd = pages[c].cards.find((k) => k.readLabel);
  const sn = pages[c].cards.find((k) => k.soon);
  return { read: rd.readLabel, cart: any.cart.label, soon: sn ? sn.priceText : null };
});

const sections = pages.az.secs.map((s, i) => ({
  author: s.author,
  id: s.id,
  style: pages.az.cards.find((k) => k.author === s.author).style,
  heading: collapse(per((c) => pages[c].secs[i].heading)),
}));

const books = [];
for (let i = 0; i < n; i++) {
  const k = per((c) => pages[c].cards[i]);
  const a = k.az;
  for (const c of LANGS) {
    const x = k[c];
    if (x.cover !== a.cover || x.author !== a.author || x.style !== a.style || x.soon !== a.soon) throw new Error('карточки не совпадают по порядку: #' + i + ' ' + c);
    if (x.dataTitle !== x.title) throw new Error('data-title ≠ заголовок: ' + x.title);
    if (x.cart && x.cart.order !== x.title) throw new Error('data-order ≠ заголовок: ' + x.title);
    if (x.cart && x.cart.price !== x.priceText) throw new Error('data-price ≠ цена: ' + x.title);
    if (x.read && x.coverHref !== x.read) throw new Error('ссылки обложки и «Oxu» разные: ' + x.title);
    if (!x.read && x.coverHref) throw new Error('обложка-ссылка без «Oxu»: ' + x.title);
    if (x.soon && x.priceText !== ui[c].soon) throw new Error('soon-карточка с ценой: ' + x.title);
  }
  const id = a.cover.replace(/\?.*$/, '').replace(/\.jpg$/, '').replace(/^art-/, '');
  const b = { id, author: a.author, style: a.style, cover: a.cover };
  if (a.soon) b.status = 'soon';
  b.title = collapse(per((c) => k[c].title));
  b.coverTitle = collapse(per((c) => k[c].coverTitle));
  b.coverAuthor = collapse(per((c) => k[c].coverAuthor));
  b.coverYear = collapse(per((c) => k[c].coverYear));
  b.meta = collapse(per((c) => k[c].meta));
  if (!a.soon) {
    b.price = collapse(per((c) => k[c].priceText));
    b.read = collapse(per((c) => k[c].read));
    /* корзина есть у каждой продаваемой карточки — отдельным полем не храним */
    if (!LANGS.every((c) => k[c].cart)) throw new Error('карточка с ценой без корзины: ' + id);
    const rc = collapse(per((c) => k[c].readClass));
    if (typeof rc !== 'string') throw new Error('класс кнопки «Oxu» разный по языкам: ' + id);
    if (rc !== (a.style === 'art' ? 'btn btn--read' : 'btn')) throw new Error('нестандартный класс «Oxu»: ' + id);
  }
  books.push(b);
}

/* ── баннер коллекции: числа — из книг коллекции, тексты — шаблоны {n} {old} {new} {save} {unit} {per} {disc} ── */
const memberRe = /^freud-(gw\d+|fliesse-mektublari)$/; /* как в живом скрипте страницы: тома GW + Флисс */
books.forEach((b) => { if (memberRe.test(b.id) && b.status !== 'soon') b.collection = 'freud'; });
const members = books.filter((b) => b.collection === 'freud');
const unit = parseInt(members[0].price, 10);
const disc = parseInt(pages.az.banner.discount, 10);
const nm = members.length, old = nm * unit, now = Math.round(old * (1 - disc / 100));
const vals = { n: nm, old, new: now, save: old - now, unit, per: (now / nm).toFixed(2), disc };
const tpl = (s) => {
  let t = s;
  /* заменяем только числа, совпадающие с вычисленными; порядок — от длинных к коротким */
  for (const [k, v] of Object.entries(vals).sort((x, y) => String(y[1]).length - String(x[1]).length)) {
    t = t.split(String(v)).join('{' + k + '}');
  }
  return t;
};
const collection = per((c) => {
  const bn = pages[c].banner;
  if (!bn) return null;
  const o = {};
  /* многострочные тексты (p, note, hint) хранятся без отступа 12 пробелов — генератор вернёт его */
  const dedent = (v) => v.split('\n').map((l) => l.replace(/^ {12}/, '')).join('\n');
  for (const [k, v] of Object.entries(bn)) o[k] = (k === 'collection' || k === 'discount') ? v : tpl(dedent(v));
  delete o.collection; delete o.discount;
  return o;
});

const out = {
  _note: 'Каталог книг ragimoff.org/books/ (AZ/RU/EN) — единственный источник для _tools/build-books-gallery.js. ' +
    'Снят с живых страниц 08.11.2026 (_tools/catalog-extract.js). Поля-тексты: строка (одинаково во всех языках) или {az,ru,en}. ' +
    'status:"soon" или id в closed-books.json → карточка «Hazırlanır» без Oxu и корзины. ' +
    'collection.freud: книги с collection:"freud"; цена набора = Σ цен × (1 − discount/100); в текстах баннера {n} {old} {new} {save} {unit} {per} {disc} подставляются генератором. ' +
    'Форма заказа (RU/EN): книги не из серии Фрейда с ценой.',
  langs: LANGS,
  ui,
  sections,
  collections: { freud: { discount: disc, text: collection } },
  books,
};
fs.writeFileSync(OUT_JSON, JSON.stringify(out, null, 2) + '\n', 'utf8');
fs.mkdirSync(SHELL_DIR, { recursive: true });
for (const c of LANGS) fs.writeFileSync(path.join(SHELL_DIR, 'books.' + c + '.html'), pages[c].shell, 'utf8');
console.log('catalog.json:', books.length, 'книг;', 'в коллекции', nm, '→', old, '/', now, '₼; оболочки:', LANGS.join(', '));
