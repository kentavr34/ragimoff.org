/* =====================================================================
   RAGIMOFF · _tools/build-books-gallery.js — каталог книг на трёх языках
   Собирает books/index.html (AZ), books/ru/index.html (RU), books/en/index.html (EN).

   Переписан 08.11.2026: прежний генератор держал свой список из 43 старых карточек
   (без томов серии по GW, корзин и баннера коллекции) и отстал от живого каталога.
   Старая версия — build-books-gallery.js.bak_20261108.

   Источники:
     _tools/catalog.json                  — данные карточек и баннера коллекции (ОДИН источник);
     _tools/catalog-shell/books.<яз>.html — оболочка страницы (стили, шапка, футер, скрипты)
                                           с метками <!--@@BANNER@@-->, <!--@@CARDS@@-->, <!--@@OPTIONS@@-->;
     _tools/closed-books.json             — закрытые книги: только карточка «Hazırlanır», без Oxu и корзины.
   Снять всё это заново с живых страниц (если их правили руками): node _tools/catalog-extract.js --force

   Запуск:
     node _tools/build-books-gallery.js              — dry-run: пишет в _tools/_gallery_dryrun/ и сверяет с books/
     node _tools/build-books-gallery.js --out <папка> — dry-run в другую папку
     node _tools/build-books-gallery.js --write-live — ЕДИНСТВЕННЫЙ способ записи в books/
                                                       (отказ, если карточек меньше, чем на живой странице; обход — --force)
   ===================================================================== */
const fs = require('fs');
const path = require('path');

const SITE = path.resolve(__dirname, '..');
const OUT = path.join(SITE, 'books');
const CATALOG = JSON.parse(fs.readFileSync(path.join(__dirname, 'catalog.json'), 'utf8'));
const CLOSED = new Set(JSON.parse(fs.readFileSync(path.join(__dirname, 'closed-books.json'), 'utf8')).closed);
/* оболочка — всегда с LF, как живые страницы (git с autocrlf может выдать её с CRLF) */
const SHELL = (code) => fs.readFileSync(path.join(__dirname, 'catalog-shell', 'books.' + code + '.html'), 'utf8').replace(/\r\n/g, '\n');
const LANGS = CATALOG.langs;

/* поле-текст: строка (одна на все языки) или {az, ru, en}. Тексты в catalog.json — уже HTML. */
const L = (v, code) => (v !== null && typeof v === 'object' ? v[code] : v);
const isSoon = (b) => b.status === 'soon' || CLOSED.has(b.id);
/* 08.11.2026, решение Кенана: продаётся ли книга на этом языке каталога.
   saleLangs.<автор> — языки продажи; автора там нет → продаётся на всех языках.
   Фрейд — только az: на RU/EN карточке нет цены и корзины, только «Читать». */
const SALE = CATALOG.saleLangs || {};
const onSale = (b, code) => !isSoon(b) && (!SALE[b.author] || SALE[b.author].includes(code));
const pad = (n) => ' '.repeat(n);

/* ── проверка данных: закрытые книги не продаются и не читаются ── */
function validate() {
  const ids = new Set();
  for (const b of CATALOG.books) {
    if (ids.has(b.id)) throw new Error('повтор id в catalog.json: ' + b.id);
    ids.add(b.id);
    if (!CATALOG.sections.some((s) => s.author === b.author)) throw new Error('нет раздела для автора ' + b.author + ' (' + b.id + ')');
    if (!isSoon(b) && (!b.price || !b.read)) throw new Error('у открытой книги нет цены или ссылки: ' + b.id);
    if (CLOSED.has(b.id) && b.status !== 'soon') {
      console.warn('ВНИМАНИЕ: ' + b.id + ' в closed-books.json — собираю как «Hazırlanır» (без Oxu и корзины).');
    }
    if (CLOSED.has(b.id) && b.collection) throw new Error('закрытая книга в коллекции: ' + b.id);
    for (const code of LANGS) {
      const r = L(b.read, code);
      /* 09.11.2026: ссылка может вести прямо на страницу .html (работы вне серии внутри прежних сборников) */
      const file = r && /\.html$/.test(r) ? path.join(SITE, r) : path.join(SITE, r || '', 'index.html');
      if (!isSoon(b) && r && /^\/books\//.test(r) && !fs.existsSync(file)) {
        console.warn('ВНИМАНИЕ: ссылка «' + r + '» (' + b.id + ', ' + code + ') — нет файла ' + path.relative(SITE, file));
      }
    }
  }
}

/* ── обложки ── */
function cover(b, code) {
  const author = L(b.coverAuthor, code), title = L(b.coverTitle, code), year = L(b.coverYear, code);
  if (b.style === 'classic') {
    return '<div class="cover" style="--tex:url(\'/books/covers/' + b.cover + '\')"><span class="cover__frame" aria-hidden="true"></span>' +
      '<span class="cover__author">' + author + '</span><span class="cover__title">' + title + '</span>' +
      '<span class="cover__year">' + year + '</span></div>';
  }
  return '<div class="cover cover--art" style="--tex:url(&quot;/books/covers/' + b.cover + '&quot;)"><span class="cover__author">' + author + '</span>' +
    '<span class="cover__rule" aria-hidden="true"></span><span class="cover__title">' + title + '</span>' +
    '<span class="cover__year">' + year + '</span></div>';
}

/* ── карточка (без отступа перед <article>; его ставит раздел) ── */
function card(b, code) {
  const ui = CATALOG.ui[code];
  const title = L(b.title, code), meta = L(b.meta, code);
  if (isSoon(b)) {
    /* 08.11.2026, решение Кенана: книги с чужим переводом закрыты — «Hazırlanır», без Oxu и корзины */
    return '<article class="card card--soon" data-author="' + b.author + '" data-title="' + title + '">\n' +
      pad(10) + '<div class="card__cover">\n' + cover(b, code) + '\n' + pad(10) + '</div>\n' +
      pad(10) + '<div class="card__body">\n' +
      pad(12) + '<h2 class="card__title">' + title + '</h2>\n' +
      pad(12) + '<p class="card__meta">' + meta + '</p>\n' +
      pad(12) + '<p class="card__price">' + ui.soon + '</p>\n' +
      pad(10) + '</div>\n' +
      pad(8) + '</article>';
  }
  const read = L(b.read, code), price = L(b.price, code);
  const readClass = b.style === 'art' ? 'btn btn--read' : 'btn';
  const sale = onSale(b, code);
  return '<article class="card" data-author="' + b.author + '" data-title="' + title + '">\n' +
    pad(10) + '<a class="card__cover" href="' + read + '">\n' + cover(b, code) + '\n' + pad(10) + '</a>\n' +
    pad(10) + '<div class="card__body">\n' +
    pad(12) + '<h2 class="card__title">' + title + '</h2>\n' +
    pad(12) + '<p class="card__meta">' + meta + '</p>\n' +
    (sale ? pad(12) + '<p class="card__price">' + price + '</p>\n' : '') +
    pad(12) + '<div class="card__cta">\n' +
    pad(14) + '<a class="' + readClass + '" href="' + read + '">' + ui.read + ' <span aria-hidden="true">→</span></a>\n' +
    (sale ? pad(14) + '<button class="btn btn--cart" type="button" data-cart-btn="1" data-order="' + title + '" data-price="' + price + '">' + ui.cart + '</button>\n' : '') +
    pad(12) + '</div>\n' +
    pad(10) + '</div>\n' +
    pad(8) + '</article>';
}

/* ── разделы по авторам: «classic» — карточки с отступом через пустую строку, «art» (серия Фрейда) — подряд ── */
function cards(code) {
  return CATALOG.sections.map((s) => {
    const list = CATALOG.books.filter((b) => b.author === s.author);
    const h = pad(8) + '<h2 class="author-sec" data-author="' + s.author + '"' + (s.id ? ' id="' + s.id + '"' : '') + '>' + L(s.heading, code) + '</h2>';
    if (s.style === 'art') return h + '\n' + list.map((b) => card(b, code)).join('\n');
    return h + '\n\n' + list.map((b) => pad(8) + card(b, code)).join('\n\n');
  }).join('\n\n');
}

/* ── баннер коллекции: числа считаются из книг коллекции ── */
function collectionValues(key) {
  const coll = CATALOG.collections[key];
  const members = CATALOG.books.filter((b) => b.collection === key && !isSoon(b));
  const prices = members.map((b) => parseInt(L(b.price, 'az'), 10));
  if (!members.length || prices.some((p) => p !== prices[0])) throw new Error('коллекция ' + key + ': нет книг или цены разные — текст «hər kitab N ₼» не годится');
  const n = members.length, unit = prices[0], old = n * unit, now = Math.round(old * (1 - coll.discount / 100));
  return { n, unit, old, new: now, save: old - now, per: (now / n).toFixed(2), disc: coll.discount };
}
function banner(code) {
  const key = 'freud';
  const coll = CATALOG.collections[key];
  const t = coll && coll.text[code];
  if (!t) return '';
  if (SALE.freud && !SALE.freud.includes(code)) throw new Error('баннер коллекции Фрейда на языке ' + code + ', где Фрейд не продаётся');
  const v = collectionValues(key);
  const f = (s) => s.replace(/\{(\w+)\}/g, (m, k) => (k in v ? String(v[k]) : m));
  const para = (s) => f(s).split('\n').map((l) => pad(12) + l).join('\n');
  return `    <section class="coll-banner">
      <div class="coll-banner__inner">
        <div class="coll-banner__cover">
          <div class="coll-banner__stack">
            <span class="coll-banner__b coll-banner__b--1"></span>
            <span class="coll-banner__b coll-banner__b--2"></span>
            <span class="coll-banner__b coll-banner__b--3"></span>
            <div class="coll-banner__front">
              <span class="coll-banner__author">${f(t.author)}</span>
              <span class="coll-banner__title">${f(t.coverTitle)}</span>
              <span class="coll-banner__count">${f(t.countText)}</span>
            </div>
          </div>
        </div>
        <div class="coll-banner__body">
          <span class="coll-banner__tag">${f(t.tag)}</span>
          <h2 class="coll-banner__h">${f(t.heading)}</h2>
          <p class="coll-banner__p">
${para(t.text)}
          </p>
          <div class="coll-banner__price">
            <span class="coll-banner__old">${f(t.oldText)}</span>
            <span class="coll-banner__new">${f(t.newText)}</span>
            <span class="coll-banner__save">${f(t.saveText)}</span>
          </div>
          <p class="coll-banner__note">
${para(t.note)}
          </p>
          <button class="btn coll-banner__btn" type="button" data-cart-btn="1"
                  data-order="${f(t.order)}" data-price="${f(t.priceAttr)}"
                  data-collection="${key}" data-discount="${coll.discount}">
            <span class="cb-full">${f(t.btnFull)}</span><span class="cb-short">${f(t.btnShort)}</span>
          </button>
          <p class="coll-banner__hint">
${para(t.hint)}
          </p>
        </div>

</div>
    </section>
`;
}

/* ── форма заказа (RU/EN): книги вне серии Фрейда с ценой ── */
function options(code) {
  return CATALOG.books.filter((b) => b.author !== 'freud' && onSale(b, code) && b.price)
    .map((b) => pad(12) + '<option value="' + L(b.title, code) + ' · ' + L(b.price, code) + '">' + L(b.title, code) + ' — ' + L(b.price, code) + '</option>\n')
    .join('');
}

function page(code) {
  const shell = SHELL(code);
  const once = (s, mark, val) => {
    const parts = s.split(mark);
    if (parts.length > 2) throw new Error('метка ' + mark + ' встречается в оболочке ' + code + ' больше одного раза');
    return parts.join(val);
  };
  if (!shell.includes('<!--@@CARDS@@-->')) throw new Error('в оболочке ' + code + ' нет метки <!--@@CARDS@@-->');
  let html = once(shell, '<!--@@CARDS@@-->', cards(code));
  html = once(html, '<!--@@BANNER@@-->', banner(code));
  html = once(html, '<!--@@OPTIONS@@-->', options(code));
  return html;
}

/* ── запись ── */
validate();
const OUT_ARG = process.argv.indexOf('--out');
const LIVE = process.argv.includes('--write-live');
const DEST = LIVE ? OUT : path.resolve(OUT_ARG > 0 ? process.argv[OUT_ARG + 1] : path.join(__dirname, '_gallery_dryrun'));
const countCards = (s) => (s.match(/<article class="card[ "]/g) || []).length;
let same = 0;
LANGS.forEach((code) => {
  const dir = code === 'az' ? DEST : path.join(DEST, code);
  fs.mkdirSync(dir, { recursive: true });
  const target = path.join(dir, 'index.html');
  const live = path.join(OUT, code === 'az' ? '' : code, 'index.html');
  const next = page(code);

  /* ЗАЩИТА ОТ ПОТЕРИ КНИГ (13.10.2026): не пишем в books/ версию беднее живой. Обход — --force. */
  if (LIVE && fs.existsSync(target) && !process.argv.includes('--force')) {
    const prev = countCards(fs.readFileSync(target, 'utf8'));
    const now = countCards(next);
    if (now < prev) {
      console.error('ОТКАЗ: в ' + path.relative(SITE, target) + ' было ' + prev + ' карточек, сборка даёт ' + now +
        '. Дополните _tools/catalog.json или запустите с --force, если потеря книг намеренная.');
      process.exitCode = 1;
      return;
    }
  }

  fs.writeFileSync(target, next, 'utf8');
  let note = '';
  if (!LIVE && fs.existsSync(live)) {
    const cur = fs.readFileSync(live, 'utf8');
    if (cur === next) { same++; note = ' — совпадает с ' + path.relative(SITE, live) + ' байт в байт'; }
    else note = ' — ОТЛИЧАЕТСЯ от ' + path.relative(SITE, live) + ' (diff -u ' + path.relative(SITE, live) + ' ' + path.relative(SITE, target) + ')';
  }
  console.log((LIVE ? 'записано: ' : 'dry-run: ') + path.relative(SITE, target) + ' · ' + countCards(next) + ' карточек' + note);
});
if (!LIVE && same !== LANGS.length) process.exitCode = process.exitCode || 2;
