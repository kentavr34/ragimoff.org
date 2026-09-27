/* Патч: подзаголовок по языку (lang.subtitle) + сжатые отступы вокруг «СОДЕРЖАНИЕ». */
'use strict';
const fs = require('fs');
const f = '_tools/docx-to-book.js';
let s = fs.readFileSync(f, 'utf8');
const log = [];

/* 1) подзаголовок по языку на главной книги */
const a1 = "'<p class=\"sub\">' + esc(cfg.subtitle || '') + '</p></div>\\n' +";
const b1 = "'<p class=\"sub\">' + esc(lang.subtitle || cfg.subtitle || '') + '</p></div>\\n' +";
if (s.includes(a1)) { s = s.replace(a1, b1); log.push('hero: подзаголовок по языку'); }
else log.push('⚠ hero-подзаголовок: анкер не найден');

/* 2) JSON-LD «about» — тоже по языку */
const a2 = `'"about":"' + esc(cfg.subtitle || cfg.title) + '"'`;
const b2 = `'"about":"' + esc(lang.subtitle || cfg.subtitle || cfg.title) + '"'`;
if (s.includes(a2)) { s = s.replace(a2, b2); log.push('JSON-LD about: по языку'); }
else log.push('⚠ about: анкер не найден');

/* 3) отступы вокруг «СОДЕРЖАНИЕ» — сжать */
const a3 = "  '.home-hero{padding:16px 0 22px}' +";
const b3 = "  '.home-hero{padding:16px 0 22px}' +\n  '.book-toc{margin:16px auto 36px}' +\n  '.book-toc .toc-title{margin:0 0 16px 0;padding-bottom:8px}' +";
if (s.includes(a3) && !s.includes('.book-toc{margin:16px')) { s = s.replace(a3, b3); log.push('book-toc: отступы сжаты'); }
else log.push(s.includes('.book-toc{margin:16px') ? 'book-toc: уже сжато' : '⚠ book-toc: анкер не найден');

fs.writeFileSync(f, s);
console.log(log.join('\n'));

/* 4) конфиг: подзаголовок для каждого языка */
const cfgPath = '_tools/configs/phoenix-era.json';
const cfg = JSON.parse(fs.readFileSync(cfgPath, 'utf8'));
cfg.langs = cfg.langs.map((l) => Object.assign({}, l, {
  subtitle: l.code === 'ru'
    ? 'Путь к осознанным взаимоотношениям · Методология психотерапии'
    : 'Şüurlu münasibətlərə aparan yol · Psixoterapiya metodologiyası'
}));
fs.writeFileSync(cfgPath, JSON.stringify(cfg, null, 2) + '\n');
console.log('конфиг: подзаголовки по языкам —', cfg.langs.map((l) => l.code + ': ' + l.subtitle.slice(0, 30)).join(' | '));
