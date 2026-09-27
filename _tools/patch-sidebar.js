/* Патч: сайдбар книги — компактные пункты как у эталона (.nav-sub-link),
   узкая колонка номера главы (чтобы название начиналось сразу за цифрой). */
'use strict';
const fs = require('fs');

const f = '_tools/docx-to-book.js';
let s = fs.readFileSync(f, 'utf8');
let changed = 0;

/* 1. Пункты глав в сайдбаре: nav-link → nav-sub-link (+ sub-code/sub-name) */
const before1 = `'<div class="nav-item"><a href="' + c.file + '" class="nav-link' + (i === idx ? ' is-active' : '') + '">' +
    '<span class="nav-code">' + c.num + '</span><span>' + esc(shortLabel(c.short)) + '</span></a></div>'`;
const after1 = `'<div class="nav-item"><a href="' + c.file + '" class="nav-sub-link' + (i === idx ? ' is-active' : '') + '">' +
    '<span class="sub-code">' + c.num + '</span><span class="sub-name">' + esc(shortLabel(c.short)) + '</span></a></div>'`;
if (s.includes(before1)) { s = s.replace(before1, after1); changed++; }

/* второй вариант (страница-индекс) — та же замена по классам */
const before2 = `'<div class="nav-item"><a href="' + c.file + '" class="nav-link">' +
    '<span class="nav-code">' + c.num + '</span><span>' + esc(shortLabel(c.short)) + '</span></a></div>'`;
if (s.includes(before2)) { s = s.replace(before2, after1.replace('(i === idx ? ', '(')); changed++; }

/* 2. Узкая колонка номера + компактные отступы: добавляем в head книг */
s = s.replace(
  "function headHtml(cfg, lang, title, desc) {",
  `/* стиль оглавления книги (запомнен как канон): компактные пункты, узкая колонка номера */
const TOC_STYLE = '<style>' +
  '.sidebar .nav-sub-link{padding:7px 14px 7px 18px;font-size:12.5px;gap:8px}' +
  '.sidebar .sub-code{flex:0 0 30px;width:30px;font-size:10.5px}' +
  '.sidebar .nav-sub-link.is-active{color:var(--gold);border-left-color:var(--gold);background:var(--gold-bg)}' +
  '</style>';

function headHtml(cfg, lang, title, desc) {`
);
s = s.replace(
  "    .replace(/<\\/head>/, '</head>');",
  "    .replace(/<\\/head>/, TOC_STYLE + '</head>');"
);
/* если замены </head> нет — добавим стиль иначе */
if (!s.includes("TOC_STYLE + '</head>'")) {
  s = s.replace(
    "    .replace(/\"about\":\"[^\"]*\"/, '\"about\":\"' + esc(cfg.subtitle || cfg.title) + '\"');",
    "    .replace(/\"about\":\"[^\"]*\"/, '\"about\":\"' + esc(cfg.subtitle || cfg.title) + '\"')\n    .replace('</head>', TOC_STYLE + '</head>');"
  );
}

fs.writeFileSync(f, s);
console.log('замен в сайдбаре:', changed, '| TOC_STYLE:', s.includes('TOC_STYLE'), '| в head:', s.includes("TOC_STYLE + '</head>'"));
