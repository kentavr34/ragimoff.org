/* =====================================================================
   _tools/check-freud-ru.js — проверка собранных русских книг Фрейда.
   Проверяет: все ссылки оглавления/сайдбара/нижней навигации ведут на
   существующие файлы; число глав = числу страниц глав; языковые адреса
   (data-lang-url-*) и список доступных языков (data-lang-avail) на RU- и
   AZ-страницах; canonical/hreflang. Запуск: node _tools/check-freud-ru.js
   ===================================================================== */
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const RU_BOOKS = ['freud-musa', 'freud-seksualligin-psixologiyasi', 'freud-sevgi-mektublari',
  'freud-yuxularin-yozumu', 'freud-psixoanalizle-tanishliq'];   /* у всех пяти есть русская версия */
const AZ_ONLY = [];
/* русская версия есть, азербайджанского издания нет: языковая пара не объявляется —
   ни data-lang-url-az, ни hreflang az, ни AZ-страниц у книги быть не должно,
   доступный язык один (data-lang-avail="ru" — переключатель скрывает сам скрипт) */
const RU_ONLY = ['freud-medeniyyetin-sancilari'];
let bad = 0, links = 0;
const fail = (m) => { console.log('  БИТО: ' + m); bad++; };

function hrefs(html) {
  return [...html.matchAll(/href="([^"]+)"/g)].map((m) => m[1])
    .filter((h) => !/^(https?:|mailto:|#|javascript:|\/$|\/books\/)/.test(h));
}
const RU_JUNK = [
  /^ISBN/i, /^©/, /royallib/i, /^Скачать/i, /^Читать$/i, /^ЛитРес/i, /^УДК/i, /^ББК/i,
  /^www\./i, /^https?:\/\//i, /^e-?mail/i, /^Перевод .{0,60}дополнен редакторскими/i,
  /^Вводное примечание издателей/i, /^От редакции/i, /^Издательство/i, /^Подписано/i,
  /^Редактор/i, /^Корректор/i, /^Зигмунд Фрейд$/
];
let junk = 0;
function checkFile(file, dir) {
  const html = fs.readFileSync(file, 'utf8');
  [...html.matchAll(/<p>([\s\S]*?)<\/p>/g)].forEach((m) => {
    const t = m[1].replace(/<[^>]+>/g, '').trim();
    if (RU_JUNK.some((re) => re.test(t))) {
      junk++;
      fail(path.relative(ROOT, file) + ': мусор «' + t.slice(0, 60) + '»');
    }
  });
  hrefs(html).forEach((h) => {
    const clean = h.split('#')[0];
    if (!clean) return;
    if (clean.startsWith('/')) return;                       /* адреса сайта */
    links++;
    const p = path.resolve(path.dirname(file), clean);
    const ok = fs.existsSync(p) || fs.existsSync(path.join(p, 'index.html'));
    if (!ok) fail(path.relative(ROOT, file) + ' → ' + h);
  });
  return html;
}

RU_BOOKS.forEach((slug) => {
  const dir = path.join(ROOT, 'books', slug, 'ru');
  console.log('# ' + slug + ' (ru)');
  if (!fs.existsSync(dir)) { fail('нет папки ' + path.relative(ROOT, dir)); return; }
  const index = checkFile(path.join(dir, 'index.html'), dir);
  const toc = [...index.matchAll(/<a href="([^"]+)\/index\.html" class="toc-chapter-title"/g)].map((m) => m[1]);
  const dirs = fs.readdirSync(dir).filter((f) => fs.statSync(path.join(dir, f)).isDirectory());
  console.log('  глав в оглавлении: ' + toc.length + ' | папок глав: ' + dirs.length);
  if (toc.length !== dirs.length) fail('число глав ' + toc.length + ' ≠ папок ' + dirs.length);
  toc.forEach((t, i) => {
    const f = path.join(dir, t, 'index.html');
    if (!fs.existsSync(f)) { fail('нет главы ' + t + '/index.html'); return; }
    const html = checkFile(f, dir);
    /* сайдбар главы = все главы + «Главная»; d-nav — соседи */
    const sb = (html.match(/<aside class="sidebar"[\s\S]*?<\/aside>/) || [''])[0];
    const sbN = (sb.match(/nav-sub-link/g) || []).length;
    if (sbN !== toc.length) fail(t + ': в сайдбаре ' + sbN + ' глав, в оглавлении ' + toc.length);
    if (!/class="d-nav"/.test(html)) fail(t + ': нет нижней навигации');
    if (!/data-lang-url-az="\/books\//.test(html) || !/data-lang-url-ru="\/books\//.test(html))
      fail(t + ': нет data-lang-url-az/ru');
    if (!/data-lang-avail="az ru"/.test(html)) fail(t + ': нет data-lang-avail="az ru"');
    if (!/hreflang="ru"/.test(html)) fail(t + ': нет hreflang ru');
  });
  if (!/data-lang-avail="az ru"/.test(index)) fail('index.html: нет data-lang-avail');
  /* AZ-версия этой же книги должна вести в /ru/ */
  const azDir = path.join(ROOT, 'books', slug);
  const azIndex = fs.readFileSync(path.join(azDir, 'index.html'), 'utf8');
  if (!azIndex.includes('data-lang-url-ru="/books/' + slug + '/ru/"'))
    fail('AZ index.html: неверный data-lang-url-ru');
  if (!/data-lang-avail="az ru"/.test(azIndex)) fail('AZ index.html: нет data-lang-avail="az ru"');
});

AZ_ONLY.forEach((slug) => {
  console.log('# ' + slug + ' (только az)');
  const f = path.join(ROOT, 'books', slug, 'index.html');
  const h = fs.readFileSync(f, 'utf8');
  if (!/data-lang-avail="az"/.test(h)) fail(slug + ': нет data-lang-avail="az"');
  if (/data-lang-url-ru/.test(h)) fail(slug + ': лишний data-lang-url-ru');
  if (fs.existsSync(path.join(ROOT, 'books', slug, 'ru'))) fail(slug + ': неожиданная папка ru');
});

RU_ONLY.forEach((slug) => {
  const dir = path.join(ROOT, 'books', slug, 'ru');
  const index = checkFile(path.join(dir, 'index.html'), dir);
  const toc = [...index.matchAll(/<a href="([^"]+)\/index\.html" class="toc-chapter-title"/g)].map((m) => m[1]);
  const dirs = fs.readdirSync(dir).filter((f) => fs.statSync(path.join(dir, f)).isDirectory());
  console.log('# ' + slug + ' (только ru): глав в оглавлении ' + toc.length + ' | папок глав ' + dirs.length);
  if (toc.length !== dirs.length) fail('число глав ' + toc.length + ' ≠ папок ' + dirs.length);
  toc.forEach((t) => {
    const f = path.join(dir, t, 'index.html');
    if (!fs.existsSync(f)) { fail('нет главы ' + t + '/index.html'); return; }
    const html = checkFile(f, dir);
    const sb = (html.match(/<aside class="sidebar"[\s\S]*?<\/aside>/) || [''])[0];
    const sbN = (sb.match(/nav-sub-link/g) || []).length;
    if (sbN !== toc.length) fail(t + ': в сайдбаре ' + sbN + ' глав, в оглавлении ' + toc.length);
    if (!/class="d-nav"/.test(html)) fail(t + ': нет нижней навигации');
    if (/data-lang-url-az/.test(html)) fail(t + ': лишний data-lang-url-az (AZ-версии нет)');
    if (!/data-lang-avail="ru"/.test(html)) fail(t + ': нет data-lang-avail="ru"');
    if (!/hreflang="ru"/.test(html)) fail(t + ': нет hreflang ru');
    if (/hreflang="az"/.test(html)) fail(t + ': лишний hreflang az (AZ-версии нет)');
  });
  if (!/data-lang-avail="ru"/.test(index)) fail('index.html: нет data-lang-avail="ru"');
  if (/data-lang-url-az/.test(index)) fail('index.html: лишний data-lang-url-az');
  /* AZ-страницы у книги быть не должно: адрес /books/<slug>/ не существует */
  if (fs.existsSync(path.join(ROOT, 'books', slug, 'index.html')))
    fail(slug + ': есть корневой index.html, хотя AZ-версии нет');
});

/* галерея: ссылки «читать» ведут на существующие версии */
['index.html', 'ru/index.html', 'en/index.html'].forEach((rel) => {
  const f = path.join(ROOT, 'books', rel);
  const h = fs.readFileSync(f, 'utf8');
  [...h.matchAll(/class="btn" href="([^"]+)"/g)].map((m) => m[1]).forEach((u) => {
    const p = path.join(ROOT, u.replace(/^\//, ''), 'index.html');
    if (!fs.existsSync(p)) fail('галерея books/' + rel + ' → ' + u);
  });
  /* карточки новых книг: data-author="freud" у каждой карточки Фрейда */
  const cred = [...h.matchAll(/<article class="card" data-author="([^"]+)"[^>]*data-title="([^"]*)"/g)];
  if (!cred.some((m) => m[1] === 'freud')) fail('галерея books/' + rel + ': нет карточек Фрейда');
});

console.log('\nпроверено ссылок: ' + links + ' | проблем: ' + bad);
if (bad) process.exitCode = 1;
