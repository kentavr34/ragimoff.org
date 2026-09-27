/* Патч конвертера: контент на классах эталона (home-hero, chapter-menu, ch-disorder),
   короткие подписи в сайдбаре, переключатель на 2 языка. */
'use strict';
const fs = require('fs');

const f = '_tools/docx-to-book.js';
let s = fs.readFileSync(f, 'utf8');

/* ── 1. Короткая подпись для сайдбара: «BÖLÜM 1. MÜNASİBƏT MODELİ · «LİLİT»» → «Bölüm 1 · «Lilit»» ── */
s = s.replace(
  "function esc(s) {",
  `function shortLabel(title) {
  const t = String(title).trim();
  const num = (t.match(/^(?:BÖLÜM|Bölüm|ГЛАВА|Глава|CHAPTER|Chapter)\\s*([IVXLC]+|\\d+)/) || [])[1];
  const name = (t.match(/«([^»]+)»/) || [])[1];
  if (num && name) return (t.slice(0, 2) === 'ГЛ' || t.slice(0, 2) === 'Гл' ? 'Глава ' : 'Bölüm ') + num + ' · «' + name + '»';
  if (num) return (t.slice(0, 2) === 'ГЛ' || t.slice(0, 2) === 'Гл' ? 'Глава ' : 'Bölüm ') + num + ' · ' + t.replace(/^[^.]*\\.\\s*/, '').slice(0, 34);
  return t.length > 46 ? t.slice(0, 44) + '…' : t;
}

function esc(s) {`
);

/* ── 2. Сайдбар: короткие подписи ── */
s = s.replace(
  "'<span class=\"nav-code\">' + c.num + '</span><span>' + esc(c.short) + '</span></a></div>'",
  "'<span class=\"nav-code\">' + c.num + '</span><span>' + esc(shortLabel(c.short)) + '</span></a></div>'"
);
s = s.replace(
  "'<span class=\"nav-code\">' + c.num + '</span><span>' + esc(c.short) + '</span></a></div>'\n  ).join('\\n      ');\n  const langs",
  "'<span class=\"nav-code\">' + c.num + '</span><span>' + esc(shortLabel(c.short)) + '</span></a></div>'\n  ).join('\\n      ');\n  const langs"
);

/* ── 3. Страница главы: навигация классами эталона ── */
s = s.replace(
  `    '\\n<nav class="chapter-nav">' +
    (prev ? '<a href="' + prev.file + '">← ' + ui.prev + '</a>' : '<span></span>') +
    (next ? '<a href="' + next.file + '">' + ui.next + ' →</a>' : '<span></span>') +
    '</nav>\\n' + tailHtml(all, idx);`,
  `    '\\n<div class="chapter-menu">' +
    (prev ? '<a class="ch-disorder" href="' + prev.file + '"><span class="ch-code">← ' + ui.prev + '</span><span class="ch-name">' + esc(shortLabel(prev.short)) + '</span></a>' : '') +
    (next ? '<a class="ch-disorder" href="' + next.file + '"><span class="ch-code">' + ui.next + ' →</span><span class="ch-name">' + esc(shortLabel(next.short)) + '</span></a>' : '') +
    '</div>\\n' + tailHtml(all, idx);`
);

/* ── 4. Индекс книги: классы эталона (home-hero, chapter-menu) ── */
const iIdx = s.indexOf('function indexPage(');
const iEnd = s.indexOf('/* ─────────── main ─────────── */');
const newIndex = `function indexPage(cfg, lang, all, rel) {
  const ui = UI[lang.ui] || UI.az;
  const cards = all.map((c) =>
    '<a class="ch-disorder" href="' + c.file + '"><span class="ch-code">' + c.num + '</span><span class="ch-name">' + esc(c.short) + '</span></a>'
  ).join('\\n      ');
  const content =
    '\\n<div class="home-hero"><h1 class="home-title">' + esc(lang.title.toUpperCase()) + '</h1>' +
    '<p class="sub">' + esc(cfg.subtitle || '') + '</p></div>\\n' +
    '<section class="author-note">' +
    '<p><a class="read-link" href="' + (all.length ? all[0].file : '#') + '">' + ui.read + ' →</a></p>' +
    '<button type="button" class="btn-order" onclick="openKitabModal()">' + ui.order + '</button>' +
    '</section>\\n' +
    '<div class="chapter-menu">\\n      ' + cards + '\\n    </div>\\n';
  return headHtml(cfg, lang, lang.title, lang.title + ' — ' + (cfg.subtitle || '')) +
    '\\n</head>\\n' + bodyTop(cfg, lang) + sidebarHtml(cfg, lang, all, -1, rel) + TPL.mid + TPL.contentOpen +
    content + '\\n' + tailHtml(all, 0);
}

`;
s = s.slice(0, iIdx) + newIndex + s.slice(iEnd);
fs.writeFileSync(f, s);
console.log('конвертер обновлён: классы эталона + короткие подписи + навигация');
