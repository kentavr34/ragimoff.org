/* Патч: оглавление книги — как в «Klinik Psixiatriya»:
   section.book-toc > h2.toc-title + div.toc-chapter > a.toc-chapter-title > (span.toc-name + span.toc-range)
   Имена глав: капс, из «…» заголовка или первых абзацев, без дублей; опечатка «bÖLÜM» чинится. */
'use strict';
const fs = require('fs');

const f = '_tools/docx-to-book.js';
let s = fs.readFileSync(f, 'utf8');
const log = [];

/* 1) нормализация опечаток в префиксе (bÖLÜM → BÖLÜM) в shortLabel */
s = s.replace(
  'function shortLabel(title) {\n  const t = String(title).trim();',
  "function shortLabel(title) {\n  const t = String(title).trim().replace(/^bÖLÜM/i, 'BÖLÜM');"
);
log.push('shortLabel: нормализация bÖLÜM');

/* 2) имя главы для оглавления: «…» из заголовка или первых абзацев, иначе — заголовок без номера */
s = s.replace(
  'function dnName(title) {',
  `function chapterName(ch) {
  const t = String(ch.title || '').trim();
  let m = t.match(/«([^»]+)»/);
  if (!m) {
    for (let i = 0; i < Math.min(3, (ch.paras || []).length); i++) {
      const p = String((ch.paras[i] || {}).text || '').trim();
      const mm = p.match(/^«([^»]+)»$/);
      if (mm) { m = mm; break; }
    }
  }
  let name = m ? m[1] : t.replace(/^[^.]*\\.\\s*/, '');
  name = name.replace(/«[^»]*»\\s*/g, ' ').replace(/\\s+/g, ' ').trim();
  return name.toUpperCase();
}

/* имена без дублей: повтор → берём полный заголовок без номера */
function uniqueNames(all) {
  const seen = {};
  return all.map((c) => {
    let n = chapterName(c);
    if (!n) n = 'BÖLMƏ';
    if (seen[n]) {
      const full = String(c.short).replace(/^[^.]*\\.\\s*/, '').toUpperCase().trim();
      n = full && full !== n ? full : n + ' (' + c.num + ')';
    }
    seen[n] = 1;
    return n;
  });
}

function dnName(title) {`
);
log.push('chapterName + uniqueNames');

/* 3) оглавление на странице книги — разметка эталона */
const oldCards = `  const cards = all.map((c) =>
    '<a class="ch-disorder" href="' + c.file + '"><span class="ch-code">' + c.num + '</span><span class="ch-name">' + esc(shortLabel(c.short)) + '</span></a>'
  ).join('\\n      ');`;
const newCards = `  const names = uniqueNames(all);
  const cards = all.map((c, i) =>
    '<div class="toc-chapter"><a href="' + c.file + '" class="toc-chapter-title">' +
    '<span class="toc-name">' + esc(names[i]) + '</span>' +
    '<span class="toc-range">' + c.num + '</span></a></div>'
  ).join('\\n      ');`;
if (s.includes(oldCards)) { s = s.replace(oldCards, newCards); log.push('карточки оглавления → toc-chapter'); }
else log.push('⚠ карточки оглавления: анкер не найден');

/* 4) обёртка section.book-toc + h2.toc-title */
s = s.replace(
  "'<div class=\"chapter-menu\">\\n      ' + cards + '\\n    </div>\\n';",
  "'<section class=\"book-toc\"><h2 class=\"toc-title\">' + (UI[lang.ui] || UI.az).toc.toUpperCase() + '</h2>\\n      ' + cards + '\\n    </section>\\n';"
);
log.push('обёртка book-toc + toc-title');

fs.writeFileSync(f, s);
console.log(log.join('\n'));
console.log('проверки:', s.includes('chapterName'), s.includes('toc-chapter-title'), s.includes('book-toc'));
