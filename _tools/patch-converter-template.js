/* Патч конвертера: генерация страниц из каркаса эталонной книги
   (_tools/book-template.json) — тот же head/шапка/сайдбар/скрипты,
   меняются только метаданные, оглавление и контент. */
'use strict';
const fs = require('fs');
const path = require('path');

const f = '_tools/docx-to-book.js';
let s = fs.readFileSync(f, 'utf8');

/* ── 1. Загрузка шаблона ── */
s = s.replace(
  "const UI = {",
  `const TPL = JSON.parse(fs.readFileSync(path.join(__dirname, 'book-template.json'), 'utf8'));

const UI = {`
);

/* ── 2. Новый генератор страницы главы ── */
const start = s.indexOf('function chapterPage(');
const end = s.indexOf('/* ─────────── main ─────────── */');
if (start < 0 || end < 0) throw new Error('не найдены функции генерации');

const newFns = `function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

/* шапка: подмена бренда книги */
function bodyTop(cfg, lang) {
  return TPL.bodyTop
    .replace(/<div class="hdr-logo">[^<]*<\\/div>/, '<div class="hdr-logo">' + cfg.logo + '</div>')
    .replace(/<strong>[^<]*<\\/strong>/, '<strong>' + esc(lang.title.toUpperCase()) + '</strong>')
    .replace(/<small>[^<]*<\\/small>/, '<small>' + esc(cfg.author) + ' · ' + cfg.year + '</small>');
}

/* сайдбар: оглавление книги в классовой структуре эталона */
function sidebarHtml(cfg, all, idx, rel) {
  const items = all.map((c, i) =>
    '<div class="nav-item"><a href="' + c.file + '" class="nav-link' + (i === idx ? ' is-active' : '') + '">' +
    '<span class="nav-code">' + c.num + '</span><span>' + esc(c.short) + '</span></a></div>'
  ).join('\\n      ');
  return '<aside class="sidebar" id="sb">\\n' +
    '    <div class="sb-hdr"><a class="sb-site" href="https://ragimoff.org/books/" title="Kitablar">← ' + (UI[lang.ui] || UI.az).back + '</a>' +
    '<button class="sb-close" onclick="toggleSb()" aria-label="Bağla">✕</button></div>\\n' +
    '    <nav>\\n      <div class="nav-item"><a href="' + rel + 'index.html" class="nav-link nav-front">' + (UI[lang.ui] || UI.az).home + '</a></div>\\n      ' +
    items + '\\n    </nav>\\n  </aside>';
}

/* хвост: поисковый индекс книги (ALL_PAGES) + текущая страница */
function tailHtml(all, idx) {
  const pages = JSON.stringify(all.map((c) => ({ slug: c.file.replace(/\\.html$/, ''), title: c.short, code: c.num })));
  return TPL.tail
    .replace(/const CURRENT = "[^"]*";/, 'const CURRENT = "' + all[idx].file.replace(/\\.html$/, '') + '";')
    .replace(/const ALL_PAGES = \\[[\\s\\S]*?\\];/, 'const ALL_PAGES = ' + pages + ';');
}

/* метаданные страницы */
function headHtml(cfg, lang, title, desc) {
  return TPL.head
    .replace(/<title>[\\s\\S]*?<\\/title>/, '<title>' + esc(title) + ' | ' + esc(lang.title.toUpperCase()) + '</title>')
    .replace(/<meta name="description" content="[^"]*"/, '<meta name="description" content="' + esc(desc) + '"')
    .replace(/<meta property="og:title" content="[^"]*"/, '<meta property="og:title" content="' + esc(title) + '"')
    .replace(/<meta property="og:description" content="[^"]*"/, '<meta property="og:description" content="' + esc(desc) + '"')
    .replace(/<meta property="og:url" content="[^"]*"/, '<meta property="og:url" content="https://ragimoff.org/' + cfg.slug + '/"')
    .replace(/"name":"[^"]*","inLanguage":"[^"]*"/, '"name":"' + esc(cfg.title) + '","inLanguage":"' + lang.code + '"')
    .replace(/"about":"[^"]*"/, '"about":"' + esc(cfg.subtitle || cfg.title) + '"');
}

function chapterPage(cfg, lang, ch, idx, all, rel) {
  const ui = UI[lang.ui] || UI.az;
  const prev = idx > 0 ? all[idx - 1] : null;
  const next = idx < all.length - 1 ? all[idx + 1] : null;
  const body = ch.paras.map((p) => {
    const t = esc(p.text);
    if (p.text.length < 95 && /^\\d+(\\.\\d+)*[.)]?\\s/.test(p.text)) return '<h2>' + t + '</h2>';
    if (p.bold && p.sz >= 26 && p.text.length < 95) return '<h2>' + t + '</h2>';
    if (p.bold && p.text.length < 90 && /[:.]$/.test(p.text)) return '<h3>' + t + '</h3>';
    return '<p>' + t + '</p>';
  }).join('\\n');

  return headHtml(cfg, lang, ch.short, lang.title + ' — ' + ch.short) +
    '\\n</head>\\n' + bodyTop(cfg, lang) + sidebarHtml(cfg, all, idx, rel) + TPL.mid + TPL.contentOpen +
    '\\n<nav class="crumb"><a href="' + rel + 'index.html">‹ ' + esc(lang.title) + '</a></nav>' +
    '<header class="chap-head"><h1 class="chap-h1"><span class="chap-range">' + ch.num + '</span>' +
    '<span class="chap-title">' + esc(ch.short) + '</span></h1></header>\\n' +
    body +
    '\\n<nav class="chapter-nav">' +
    (prev ? '<a href="' + prev.file + '">← ' + ui.prev + '</a>' : '<span></span>') +
    (next ? '<a href="' + next.file + '">' + ui.next + ' →</a>' : '<span></span>') +
    '</nav>\\n' + tailHtml(all, idx);
}

function indexPage(cfg, lang, all, rel) {
  const ui = UI[lang.ui] || UI.az;
  const items = all.map((c, i) =>
    '<div class="nav-item"><a href="' + c.file + '" class="nav-link"><span class="nav-code">' + c.num + '</span><span>' + esc(c.short) + '</span></a></div>'
  ).join('\\n      ');
  const langs = cfg.langs.map((l) =>
    '<a href="' + (l.dir ? '../' + l.dir + '/' : '../') + '"' + (l.code === lang.code ? ' class="is-active"' : '') + '>' + l.code.toUpperCase() + '</a>'
  ).join(' · ');
  const list = all.map((c) =>
    '<li><a href="' + c.file + '"><span class="n">' + c.num + '</span> <span>' + esc(c.short) + '</span></a></li>'
  ).join('\\n      ');
  const content =
    '\\n<nav class="crumb">' + ui.home + ' · ' + esc(cfg.title) + '</nav>' +
    '<header class="chap-head"><h1 class="chap-h1"><span class="chap-title">' + esc(lang.title) + '</span></h1>' +
    '<div class="chap-en">' + esc(cfg.subtitle || '') + '</div></header>' +
    '<p>' + langs + '</p>' +
    '<p><a class="read-btn" href="' + (all.length ? all[0].file : '#') + '">' + ui.read + ' →</a></p>' +
    '<h2>' + ui.toc + '</h2><ol class="toc-list">\\n      ' + list + '\\n    </ol>\\n';
  return headHtml(cfg, lang, lang.title, lang.title + ' — ' + (cfg.subtitle || '')) +
    '\\n</head>\\n' + bodyTop(cfg, lang) + sidebarHtml(cfg, all, -1, rel) + TPL.mid + TPL.contentOpen +
    content + '\\n' + tailHtml(all, 0);
}

`;
s = s.slice(0, start) + newFns + s.slice(end);
fs.writeFileSync(f, s);
console.log('генератор переписан под шаблон эталона');
