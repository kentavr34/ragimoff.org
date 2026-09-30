#!/usr/bin/env node
/* Замер блока героя headless-Chrome'ом (CLI, без DevTools-протокола).
 *
 * Зачем: у блока героя три числа, которые владелец проверяет линейкой —
 *   gapTop    «верх блока → верх фото»        (стандарт 50 px)
 *   gapBottom «низ фото → низ блока»          (стандарт 50 px)
 *   padBottom «низ последнего элемента → низ блока»
 * Плюс контрольные: высота блока, наложение на мобильном, гориз. прокрутка.
 *
 * Как: страница копируется во временный файл РЯДОМ С СОБОЙ (иначе
 * относительные пути images/ и css/ не найдут файлов), в копию
 * подставляется замеряющий скрипт, результат кладётся в <title>,
 * chrome --headless --dump-dom печатает DOM, из него вынимается JSON.
 *
 * Запуск:
 *   node _tools/hero-measure.js index.html 1440 [--json]
 *   node _tools/hero-measure.js --batch 1440 index.html tehsil.html ...
 * Сервер: python -m http.server 8765 --bind 127.0.0.1 (корень репозитория).
 */
'use strict';
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const PORT = process.env.HERO_PORT || '8765';
/* Профиль — СВЕЖИЙ на каждый замер: shared.js держит выбор языка в
   localStorage, и унаследованный профиль уводит страницу на /ru/ (замер
   мерил бы не ту страницу). Язык браузера тоже задаём: --lang=az
   выключает авто-редирект shared.js. */
const USER_DIR = (process.env.HERO_PROFILE || 'D:/ragimoff-tmp/chrome') + '-' + process.pid;

const PROBE = `
(function () {
  function r1(v) { return Math.round(v * 10) / 10; }
  function box(el) {
    if (!el) return null;
    var r = el.getBoundingClientRect();
    return { t: r1(r.top), b: r1(r.bottom), l: r1(r.left), rr: r1(r.right), w: r1(r.width), h: r1(r.height) };
  }
  function q(s) { return document.querySelector(s); }
  function run() {
    var hero = q('.page-hero, .page-hero-x, .pg-hero');
    if (!hero) { document.title = 'HERO-JSON:' + JSON.stringify({ hero: null }); return; }
    var cs = getComputedStyle(hero);
    var img = q('.page-hero .photo-col img, .page-hero-x .photo-col img, .pg-hero .photo-col img');
    var col = q('.page-hero .photo-col, .page-hero-x .photo-col, .pg-hero .photo-col');
    var inner = q('.hero-inner, .page-hero-x-inner, .pg-hero-inner');
    var texts = ['.badge', '.ph-badge', '.hero-h1', '.ph-h1', '.hero-lead', '.ph-sub', '.hero-search-wrap', '.ph-search-wrap'];
    var last = null, lastSel = null;
    for (var i = 0; i < texts.length; i++) {
      var e = hero.querySelector(texts[i]);
      if (e) { var b = box(e); if (!last || b.b > last.b) { last = b; lastSel = texts[i]; } }
    }
    var hb = box(hero), ib = box(inner), pb = box(img), cb = box(col);
    var first = box(hero.querySelector('.badge, .ph-badge'));
    var strip = box(document.querySelector('.stats-strip, .en-stats'));
    var bs = getComputedStyle(hero);
    var lastEl = null;
    for (var j = 0; j < texts.length; j++) {
      var e2 = hero.querySelector(texts[j]);
      if (e2) { var b2 = box(e2); if (!lastEl || b2.b > lastEl.b) lastEl = b2; }
    }
    var lastM = null, lastMB = null;
    for (var k = 0; k < texts.length; k++) {
      var e3 = hero.querySelector(texts[k]);
      if (e3) { var b3 = box(e3); if (b3 && lastEl && b3.b === lastEl.b) { lastM = getComputedStyle(e3).marginBottom; lastMB = e3.className; } }
    }
    var out = {
      w: window.innerWidth, cw: document.documentElement.clientWidth,
      scrollW: document.documentElement.scrollWidth,
      hScroll: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
      heroClass: hero.className.split(' ')[0],
      hero: hb, inner: ib, photo: pb, col: cb,
      natural: img ? [img.naturalWidth, img.naturalHeight] : null,
      photoSrc: img ? img.getAttribute('src') : null,
      lastSel: lastSel, last: last,
      padTop: cs.paddingTop, padBottom: cs.paddingBottom, minH: cs.minHeight,
      gapTopPhoto: pb && hb ? r1(pb.t - hb.t) : null,
      gapBottomPhoto: pb && hb ? r1(hb.b - pb.b) : null,
      padBottomLast: last && hb ? r1(hb.b - last.b) : null,
      innerH: ib ? ib.h : null,
      first: first, strip: strip,
      firstTop: first && hb ? r1(first.t - hb.t) : null,
      stripTop: strip && hb ? r1(strip.t - hb.t) : null,
      stripOverlap: strip && pb ? r1(pb.b - strip.t) : null,
      borderBottom: bs.borderBottomWidth, borderTop: bs.borderTopWidth,
      lastMarginBottom: lastM, lastClass: lastMB,
      varGapBottom: getComputedStyle(document.documentElement).getPropertyValue('--hero-gap-bottom').trim(),
      varSBlock: getComputedStyle(document.documentElement).getPropertyValue('--s-block').trim(),
      colPos: cb ? getComputedStyle(col).position : null
    };
    document.title = 'HERO-JSON:' + JSON.stringify(out);
  }
  if (document.readyState === 'complete') { run(); } else { window.addEventListener('load', run); }
  setTimeout(run, 1200);
  setTimeout(run, 2600);
})();
`;

function withProbe(rel) {
  const src = path.join(ROOT, rel);
  const dir = path.dirname(src);
  const tmp = path.join(dir, '_m.' + path.basename(src));
  let html = fs.readFileSync(src, 'utf8');
  html = html.replace(/<\/body>/i, '<script>' + PROBE + '</script></body>');
  if (html.indexOf('HERO-JSON') === -1) html += '<script>' + PROBE + '</script>';
  fs.writeFileSync(tmp, html, 'utf8');
  return tmp;
}

function measure(rel, width, height) {
  const tmp = withProbe(rel);
  const relTmp = path.relative(ROOT, tmp).replace(/\\/g, '/');
  const url = 'http://127.0.0.1:' + PORT + '/' + encodeURI(relTmp);
  let dom = '';
  try {
    dom = execFileSync(CHROME, [
      '--headless=new', '--disable-gpu', '--no-sandbox', '--disable-extensions',
      '--lang=az', '--accept-lang=az',
      '--user-data-dir=' + USER_DIR,
      '--virtual-time-budget=9000',
      '--window-size=' + width + ',' + (height || 1600),
      '--dump-dom', url
    ], { encoding: 'utf8', maxBuffer: 1 << 28, stdio: ['ignore', 'pipe', 'ignore'] });
  } finally {
    try { fs.unlinkSync(tmp); } catch (e) {}
    try { fs.rmSync(USER_DIR, { recursive: true, force: true }); } catch (e) {}
  }
  const m = dom.match(/HERO-JSON:(\{[\s\S]*?\})<\/title>/);
  if (!m) return { file: rel, width: width, error: 'no HERO-JSON in dump' };
  let data;
  try { data = JSON.parse(m[1]); } catch (e) { return { file: rel, width: width, error: 'bad json: ' + m[1].slice(0, 120) }; }
  data.file = rel; data.width = width;
  return data;
}

const argv = process.argv.slice(2);
const json = argv.includes('--json');
const args = argv.filter(function (a) { return a !== '--json'; });
const width = parseInt(args[0], 10);
const pages = args.slice(1);
const out = pages.map(function (p) { return measure(p, width); });

if (json) { console.log(JSON.stringify(out, null, 1)); }
else {
  out.forEach(function (d) {
    if (d.error) { console.log('  ' + d.file + ' @' + d.width + '  ERROR ' + d.error); return; }
    console.log('  ' + (d.file + ' @' + d.width).padEnd(34) +
      ' hero=' + (d.hero ? d.hero.h : '-').toString().padStart(6) +
      '  top(hero→photo)=' + String(d.gapTopPhoto).padStart(6) +
      '  bottom(photo→hero)=' + String(d.gapBottomPhoto).padStart(6) +
      '  bottom(last→hero)=' + String(d.padBottomLast).padStart(6) +
      '  top(badge)=' + String(d.firstTop).padStart(5) +
      '  stripOverlap=' + String(d.stripOverlap).padStart(5) +
      '  col=' + String(d.colPos).padEnd(8) +
      (d.hScroll ? ' HSCROLL!' : '') +
      '  inner=' + d.w + '/' + d.cw);
  });
}
