/* Книга «Klinik Psixiatriya»: ссылка в сайдбаре «← ragimoff.org» → «← Kitablar» (на /books/),
   как в книге «Feniks Erası». Языки: AZ/TR → Kitablar, RU → Книги, EN → Books. */
'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = 'klinik-psixiatriya';
const pairs = [
  ['<a class="sb-site" href="https://ragimoff.org/" title="Əsas sayta qayıt">← ragimoff.org</a>',
   '<a class="sb-site" href="/books/" title="Kitablar">← Kitablar</a>'],
  ['<a class="sb-site" href="https://ragimoff.org/" title="Ana siteye dön">← ragimoff.org</a>',
   '<a class="sb-site" href="/books/" title="Kitaplar">← Kitaplar</a>'],
  ['<a class="sb-site" href="https://ragimoff.org/ru/" title="Вернуться на основной сайт">← ragimoff.org</a>',
   '<a class="sb-site" href="/books/" title="Книги">← Книги</a>'],
  ['<a class="sb-site" href="https://ragimoff.org/en/" title="Back to the main site">← ragimoff.org</a>',
   '<a class="sb-site" href="/books/" title="Books">← Books</a>']
];

let files = 0, hits = 0;
function walk(dir) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p);
    else if (e.name.endsWith('.html')) {
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
walk(path.resolve(ROOT));
console.log('файлов обновлено:', files, '| ссылок:', hits);
