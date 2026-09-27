/* Патч: имена глав для оглавления — чище и короче; пустая первая глава убирается. */
'use strict';
const fs = require('fs');
const f = '_tools/docx-to-book.js';
let s = fs.readFileSync(f, 'utf8');
const log = [];

/* 1) chapterName: «…» из заголовка → из первых абзацев (до 6) → короткий заголовок без служебного */
const oldFn = s.match(/function chapterName\(ch\) \{[\s\S]*?\n\}/);
if (oldFn) {
  const newFn = `function chapterName(ch) {
  const t = String(ch.title || '').trim();
  let m = t.match(/«([^»]+)»/);
  if (!m) {
    for (let i = 0; i < Math.min(6, (ch.paras || []).length); i++) {
      const p = String((ch.paras[i] || {}).text || '').trim();
      const mm = p.match(/^«([^»]+)»/) || p.match(/^\\u00ab([^\\u00bb]+)\\u00bb/);
      if (mm && p.length < 60) { m = mm; break; }
    }
  }
  if (m) return m[1].toUpperCase().trim();
  let name = t
    .replace(/^\\s*(BÖLÜM|Bölüm|bÖLÜM|ГЛАВА|Глава|CHAPTER|Chapter|FƏSİL|Fəsil|ÇAP)\\s*[IVXLC\\d]*[.)]?\\s*/i, '')
    .replace(/MÜNASİBƏT MODELİ|МОДЕЛЬ ВЗАИМООТНОШЕНИЙ|MODEL OF RELATIONSHIPS/gi, '')
    .replace(/^[·.\\s—–-]+/, '')
    .split(/[·]/)[0]
    .trim();
  return (name || t).toUpperCase().slice(0, 60);
}`;
  s = s.replace(oldFn[0], newFn);
  log.push('chapterName обновлён');
}

/* 2) пустая первая глава (без заголовка) — убрать, если следующая есть */
s = s.replace(
  '  return flat;\n}',
  `  /* первая глава без названия — служебная шапка файла: если у неё мало текста, убрать */
  if (flat.length > 1 && !String(flat[0].title || '').trim()) {
    const len0 = flat[0].paras.reduce((n, p) => n + p.text.length, 0);
    if (len0 < 1200) flat.shift();
  }
  return flat;
}`
);
log.push('пустая первая глава убирается');

fs.writeFileSync(f, s);
console.log(log.join('\n'));
console.log('проверки:', s.includes('MODEL OF RELATIONSHIPS'), s.includes('flat.shift()'));
