/* =====================================================================
   _tools/check-freud-book.js — проверка AZ-книг Фрейда после сборки.
   • издательский/переводческий мусор: 0 абзацев на всех страницах;
   • пустых глав нет (в каждой главе ≥ 2 абзаца);
   • ссылки оглавления, сайдбара, нижней навигации и хлебной крошки ведут
     на существующие файлы (0 битых);
   • число пунктов TOC = число файлов глав;
   • языковые атрибуты (data-lang-url-*, data-lang-avail) и версии ?v=.
   Плюс RU_ONLY — книги, у которых есть только русская версия (AZ-издания нет):
   у них нет data-lang-url-az и переключателя языков (data-lang-avail="ru").
   Запуск: node _tools/check-freud-book.js
   ===================================================================== */
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const ALL = ['freud-musa', 'freud-yuxularin-yozumu', 'freud-seksualligin-psixologiyasi',
  'freud-psixoanalizle-tanishliq', 'freud-sevgi-mektublari', 'freud-aforizmlar',
  'freud-totem-ve-tabu'];
const RU_ONLY = ['freud-medeniyyetin-sancilari'];

/* тот же список мусора, что в _tools/freud-az-book.js */
const JUNK = [
  /^Converted Ebook$/i, /^Telegram\b/i, /kitabbul/i, /^Cover$/i,
  /^ISBN\b/i, /^İSBN\b/i, /^©/, /^\(c\)/i, /^Qanun Nəşriyyatı\b/i, /Nəşriyyatı[, ]/i,
  /^Bakı\b/i, /^Tel(efon)?[:.]/i, /^Mobil[:.]/i, /^e-?mail\b/i, /^www\./i, /^https?:\/\//i,
  /^info@|@qanun|@kitabbul|@\w+\.(az|com|ru)$/i,
  /facebook\.com|instagram\.com|fb\.com|t\.me\//i,
  /^Çapa imzalanmışdır/i, /^Çapa\b/i, /^Sifariş/i, /^Tiraj/i, /^Kağız/i,
  /müəlliflik hüququ/i, /hüquqları .*məxsusdur/i, /hissə-hissə nəşri/i, /ziddir\.?$/i,
  /^Redaktor/i, /^Korrektor/i, /^Tərcümə\b/i, /^Tercümə\b/i, /^Rus dilindən tərcümə/i,
  /^Tərtib(çi)?\b/i, /^Ön sözü yazan/i, /^Buraxılışa/i, /^Nəşrə hazırlayan/i,
  /^MÜNDƏRİCAT$/i, /^Mündəricat$/i, /^İçindəkilər$/i,
  /^Sigmund Freud\b/i, /^Ziqmund Freyd$/i, /^Moses and Monotheism$/i, /^Die Brautbriefe/i,
  /^Introduction to Psychoanalysis$/i, /^SIgmund Freud DIe Traumdeutung$/i,
  /^Annotasiya$/i, /^Annotation$/i,
];

/* Сокращённое имя автора — запрещено (владелец, 29.09.2026): писать полностью
   «Ziqmund Freyd» / «Зигмунд Фрейд». Ловим в текстах страниц отдельным правилом. */
const SF_ABBR = /[ЗZ]\.\s?[ФF](рейд|reyd)/i;

let junkTotal = 0, broken = 0, pages = 0;
const fail = (m) => { console.log('  БИТО: ' + m); broken++; };

ALL.forEach((slug) => {
  const dir = path.join(ROOT, 'books', slug);
  const files = fs.readdirSync(dir).filter((f) => f.endsWith('.html')).sort();
  const index = fs.readFileSync(path.join(dir, 'index.html'), 'utf8');
  const chapters = files.filter((f) => /^\d{2}-/.test(f));
  const toc = [...index.matchAll(/<a href="([^"]+)" class="toc-chapter-title">/g)].map((m) => m[1]);
  const sb = [...index.matchAll(/<a href="([^"]+)" class="nav-sub-link/g)].map((m) => m[1]);
  console.log('# ' + slug + ': файлов глав ' + chapters.length + ', пунктов TOC ' + toc.length);
  if (chapters.length !== toc.length) fail(slug + ': число глав ≠ числу пунктов TOC');
  toc.forEach((h) => { if (!fs.existsSync(path.join(dir, h))) fail(slug + ' TOC → ' + h); });
  sb.forEach((h) => { if (!fs.existsSync(path.join(dir, h))) fail(slug + ' сайдбар → ' + h); });

  files.forEach((f) => {
    const html = fs.readFileSync(path.join(dir, f), 'utf8');
    pages++;
    /* мусор в абзацах */
    const paras = [...html.matchAll(/<p(?:\s[^>]*)?>([\s\S]*?)<\/p>/g)].map((m) => m[1].replace(/<[^>]+>/g, '').trim());
    const abbr = paras.filter((p) => SF_ABBR.test(p));
    if (abbr.length) fail(slug + '/' + f + ': сокращённое имя автора, напр. «' + abbr[0].slice(0, 60) + '»');
    const junk = paras.filter((p) => JUNK.some((re) => re.test(p)))
      /* на ТИТУЛЬНОЙ странице книги имя автора — законный элемент, а не колонтитул */
      .filter((p) => !(f === 'index.html' && /^Ziqmund Freyd$/i.test(p.trim())));
    if (junk.length) {
      junkTotal += junk.length;
      fail(slug + '/' + f + ': мусор ' + junk.length + ' абз., напр. «' + junk[0].slice(0, 70) + '»');
    }
    /* пустая глава */
    if (/^\d{2}-/.test(f) && paras.length < 2) fail(slug + '/' + f + ': пустая глава (' + paras.length + ' абз.)');
    /* внутренние ссылки страницы */
    [...html.matchAll(/href="([^"]+)"/g)].map((m) => m[1])
      .filter((h) => !/^(https?:|mailto:|#|javascript:|\/)/.test(h))
      .forEach((h) => {
        const p = path.resolve(dir, h);
        if (!fs.existsSync(p) && !fs.existsSync(path.join(p, 'index.html'))) fail(slug + '/' + f + ' → ' + h);
      });
    /* языковые атрибуты и версии скриптов */
    const htmlTag = (html.match(/<html[^>]*>/) || [''])[0];
    if (!/data-lang-url-az="\/books\//.test(htmlTag)) fail(slug + '/' + f + ': нет data-lang-url-az');
    if (!/data-lang-avail="/.test(htmlTag)) fail(slug + '/' + f + ': нет data-lang-avail');
    if (!/\/_lang-switch\.js\?v=\d+/.test(html)) fail(slug + '/' + f + ': _lang-switch.js без ?v=');
  });
});

/* книги только на русском: AZ-издания нет → data-lang-url-az быть не должно,
   доступный язык один (data-lang-avail="ru") — переключатель скрывается сам */
RU_ONLY.forEach((slug) => {
  const dir = path.join(ROOT, 'books', slug, 'ru');
  const index = fs.readFileSync(path.join(dir, 'index.html'), 'utf8');
  const toc = [...index.matchAll(/<a href="([^"]+)\/index\.html" class="toc-chapter-title"/g)].map((m) => m[1]);
  const dirs = fs.readdirSync(dir).filter((f) => fs.statSync(path.join(dir, f)).isDirectory());
  const files = fs.readdirSync(dir).filter((f) => f.endsWith('.html')).sort();
  console.log('# ' + slug + ' (только ru): файлов ' + files.length + ', пунктов TOC ' + toc.length + ', папок глав ' + dirs.length);
  if (toc.length !== dirs.length) fail(slug + ': число глав ' + toc.length + ' ≠ папок ' + dirs.length);
  toc.forEach((t) => {
    const p = path.join(dir, t, 'index.html');
    if (!fs.existsSync(p)) { fail(slug + ': нет главы ' + t + '/index.html'); return; }
    const html = fs.readFileSync(p, 'utf8');
    const sb = (html.match(/<aside class="sidebar"[\s\S]*?<\/aside>/) || [''])[0];
    if ((sb.match(/nav-sub-link/g) || []).length !== toc.length)
      fail(t + ': в сайдбаре ' + (sb.match(/nav-sub-link/g) || []).length + ' глав, в оглавлении ' + toc.length);
    if (!/class="d-nav"/.test(html)) fail(t + ': нет нижней навигации');
    if (/data-lang-url-az/.test(html)) fail(t + ': лишний data-lang-url-az (AZ-версии нет)');
    if (!/data-lang-avail="ru"/.test(html)) fail(t + ': нет data-lang-avail="ru"');
    if (!/hreflang="ru"/.test(html)) fail(t + ': нет hreflang ru');
  });
  files.forEach((f) => {
    const html = fs.readFileSync(path.join(dir, f), 'utf8');
    pages++;
    const paras = [...html.matchAll(/<p(?:\s[^>]*)?>([\s\S]*?)<\/p>/g)].map((m) => m[1].replace(/<[^>]+>/g, '').trim());
    const abbr = paras.filter((p) => SF_ABBR.test(p));
    if (abbr.length) fail(slug + '/' + f + ': сокращённое имя автора, напр. «' + abbr[0].slice(0, 60) + '»');
    const junk = paras.filter((p) => JUNK.some((re) => re.test(p)))
      /* на ТИТУЛЬНОЙ странице книги имя автора — законный элемент, а не колонтитул */
      .filter((p) => !(f === 'index.html' && /^Ziqmund Freyd$/i.test(p.trim())));
    if (junk.length) {
      junkTotal += junk.length;
      fail(slug + '/ru/' + f + ': мусор ' + junk.length + ' абз., напр. «' + junk[0].slice(0, 70) + '»');
    }
    [...html.matchAll(/href="([^"]+)"/g)].map((m) => m[1])
      .filter((h) => !/^(https?:|mailto:|#|javascript:|\/)/.test(h))
      .forEach((h) => {
        const p = path.resolve(path.join(dir, f === 'index.html' ? '' : f), h);
        if (!fs.existsSync(p) && !fs.existsSync(path.join(p, 'index.html'))) fail(slug + '/ru/' + f + ' → ' + h);
      });
  });
  if (!/data-lang-avail="ru"/.test(index)) fail('index.html: нет data-lang-avail="ru"');
  if (/data-lang-url-az/.test(index)) fail('index.html: лишний data-lang-url-az');
});

console.log('\nИтого страниц проверено: ' + pages);
console.log('Абзацев издательского мусора: ' + junkTotal + (junkTotal === 0 ? '  ✔' : '  ✘'));
console.log('Битых ссылок/ошибок: ' + broken + (broken === 0 ? '  ✔' : '  ✘'));
process.exit(junkTotal + broken === 0 ? 0 : 1);
