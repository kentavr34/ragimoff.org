/* Извлекает каркас эталонной страницы книги («Klinik Psixiatriya») в шаблон:
   head (стили/мета), тело до <main>, сайдбар-пример, хвост (скрипты поиска/меню).
   Запуск: node _tools/make-book-template.js  → _tools/book-template.json */
'use strict';
const fs = require('fs');

const REF = 'klinik-psixiatriya/01-6A0-neyroinkisaf.html';
const src = fs.readFileSync(REF, 'utf8');

const iHead = src.indexOf('</head>') + '</head>'.length;
const iBody = src.indexOf('<body>');
const iMain = src.indexOf('<main class="site-main">');
const iAside = src.indexOf('<aside class="sidebar"');
const iAsideEnd = src.indexOf('</aside>') + '</aside>'.length;
const iContentOpen = src.indexOf('<div class="content-wrap">', iMain) + '<div class="content-wrap">'.length;
const iMainEnd = src.indexOf('</main>', iContentOpen);

const tpl = {
  head: src.slice(0, iHead),
  bodyTop: src.slice(iBody, iAside),          // <body> … шапка, прогресс, оверлей, открытие layout
  sidebar: src.slice(iAside, iAsideEnd),      // пример сайдбара (структура классов)
  mid: src.slice(iAsideEnd, iMain),           // от </aside> до <main>
  contentOpen: src.slice(iMain, iContentOpen),
  tail: src.slice(iMainEnd)
};

fs.writeFileSync('_tools/book-template.json', JSON.stringify(tpl, null, 1), 'utf8');
console.log('шаблон собран из', REF);
console.log('head:', tpl.head.length, '| bodyPre:', tpl.bodyPre.length, '| sidebar:', tpl.sidebar.length, '| tail:', tpl.tail.length);
console.log('\n— фрагмент шапки (hdr) —');
const h = tpl.bodyPre.match(/<header[\s\S]{0,700}/);
console.log(h ? h[0].slice(0, 700) : 'нет');
