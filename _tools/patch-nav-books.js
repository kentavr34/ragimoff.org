/* Замена пункта меню «XBT-11 / МКБ-11 / ICD-11» на «Kitablar / Книги / Books»
   с переходом на /books/ — в словаре, партиалах и во всех готовых страницах. */
'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = process.cwd();
const log = [];

/* ── 1. Словарь ── */
const i18nPath = path.join(ROOT, '_i18n.json');
const i18n = JSON.parse(fs.readFileSync(i18nPath, 'utf8'));
const labels = { az: 'Kitablar', ru: 'Книги', en: 'Books' };
Object.keys(labels).forEach((lang) => {
  if (i18n[lang]) { i18n[lang].clinical_psychiatry = labels[lang]; }
});
fs.writeFileSync(i18nPath, JSON.stringify(i18n, null, 2) + '\n', 'utf8');
log.push('_i18n.json: clinical_psychiatry → ' + JSON.stringify(labels));

/* ── 2. Партиалы (источник сборки) ── */
['_partials/header.html', '_partials/mobile-nav.html'].forEach((p) => {
  const fp = path.join(ROOT, p);
  if (!fs.existsSync(fp)) return;
  let s = fs.readFileSync(fp, 'utf8');
  s = s.split('href="/klinik-psixiatriya/"').join('href="/books/"');
  fs.writeFileSync(fp, s, 'utf8');
  log.push(p + ': ссылка → /books/');
});

/* ── 3. Готовые страницы ── */
const pairs = [
  ['<a href="/klinik-psixiatriya/">XBT-11</a>', '<a href="/books/">Kitablar</a>'],
  ['<a href="/klinik-psixiatriya/" onclick="toggleMenu()">XBT-11</a>', '<a href="/books/" onclick="toggleMenu()">Kitablar</a>'],
  ['<a href="/klinik-psixiatriya/">МКБ-11</a>', '<a href="/books/">Книги</a>'],
  ['<a href="/klinik-psixiatriya/" onclick="toggleMenu()">МКБ-11</a>', '<a href="/books/" onclick="toggleMenu()">Книги</a>'],
  ['<a href="/klinik-psixiatriya/">ICD-11</a>', '<a href="/books/">Books</a>'],
  ['<a href="/klinik-psixiatriya/" onclick="toggleMenu()">ICD-11</a>', '<a href="/books/" onclick="toggleMenu()">Books</a>'],
  ['<a href="https://ragimoff.org/klinik-psixiatriya/">XBT-11</a>', '<a href="https://ragimoff.org/books/">Kitablar</a>']
];

let files = 0, hits = 0;
function walk(dir) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) {
      if (/^(_old_web|\.git|node_modules|_deploy|_tools|_history|graphify-out)$/.test(e.name)) continue;
      walk(p);
    } else if (e.name.endsWith('.html')) {
      let s = fs.readFileSync(p, 'utf8');
      let n = 0;
      pairs.forEach(([a, b]) => {
        const parts = s.split(a);
        if (parts.length > 1) { n += parts.length - 1; s = parts.join(b); }
      });
      if (n) { fs.writeFileSync(p, s, 'utf8'); files++; hits += n; }
    }
  }
}
walk(ROOT);
log.push('страниц обновлено: ' + files + ', замен: ' + hits);

console.log(log.join('\n'));
