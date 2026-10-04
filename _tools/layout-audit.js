#!/usr/bin/env node
/* layout-audit.js — обмер двух вещей headless-Chrome'ом (CLI, без DevTools):
 *
 *   ЧАСТЬ 1. Полоса цифр относительно героя:
 *     heroBottom / statsTop / overlap (пересечение, px) / gap (зазор, px)
 *     overlap > 0 — полоса НАЛОЖЕНА на герой (баг владельца).
 *
 *   ЧАСТЬ 2. Отступы ярлыков (.badge и родня) от граней своего блока:
 *     insetL  = left ярлыка  − left блока  (ожидаемый стандарт)
 *     insetT  = top  ярлыка  − top  блока
 *     + высота и кегль ярлыка.
 *
 * Как: копия страницы РЯДОМ С СОБОЙ (иначе относительные images/ и css/ не
 * найдутся), в копию вставляется пробник, результат кладётся в <title>,
 * chrome --headless --dump-dom печатает DOM, из него вынимается JSON.
 *
 * Запуск (сервер: python -m http.server 8765 --bind 127.0.0.1 -d .):
 *   node _tools/layout-audit.js 1440 index.html enurez.html
 *   node _tools/layout-audit.js 1440 --json index.html > audit.json
 *   node _tools/layout-audit.js 1440 --badges index.html tehsil.html
 */
'use strict';
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const CHROME = process.env.AUDIT_CHROME || 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const PORT = process.env.AUDIT_PORT || '8765';
/* Свежий профиль на каждый замер: shared.js держит язык в localStorage и
   унаследованный профиль увёл бы замер на /ru/. */
const USER_DIR = (process.env.AUDIT_PROFILE || 'D:/ragimoff-tmp/la-profile') + '-' + process.pid;

const BADGE_SEL = '.badge, .ph-badge, .hero__badge, .ab__badge, .blog-featured-badge, .def-code, .card-label, .book-card-tag, .klinik-tag, .tag-pill';

const PROBE = `
(function () {
  function r1(v) { return Math.round(v * 10) / 10; }
  function box(el) {
    if (!el) return null;
    var r = el.getBoundingClientRect();
    return { t: r1(r.top + window.scrollY), b: r1(r.bottom + window.scrollY),
             l: r1(r.left), rr: r1(r.right), w: r1(r.width), h: r1(r.height) };
  }
  function q(s) { return document.querySelector(s); }
  /* «Блок» ярлыка — ближайший предок с видимым оформлением:
     непрозрачный фон, рамка, либо section/article. */
  function blockOf(el) {
    var p = el.parentElement;
    while (p && p !== document.body) {
      var cs = getComputedStyle(p);
      if (/^(SECTION|ARTICLE|MAIN|ASIDE|LI|TD|FIGURE)$/.test(p.tagName)) return p;
      var bg = cs.backgroundColor || '';
      var opaque = bg && bg !== 'transparent' && !/rgba\\(0, 0, 0, 0\\)/.test(bg);
      var bordered = parseFloat(cs.borderTopWidth) > 0 || parseFloat(cs.borderLeftWidth) > 0;
      if (opaque || bordered) return p;
      p = p.parentElement;
    }
    return null;
  }
  function tag(el) {
    var s = el.tagName.toLowerCase();
    if (el.id) s += '#' + el.id;
    if (el.className && typeof el.className === 'string') {
      s += '.' + el.className.trim().split(/\\s+/).slice(0, 2).join('.');
    }
    return s;
  }
  function path(el) {
    var out = [], n = el, i = 0;
    while (n && n !== document.body && i < 4) { out.unshift(tag(n)); n = n.parentElement; i++; }
    return out.join('>');
  }
  function run() {
    var hero = q('.page-hero, .page-hero-x, .pg-hero');
    var strip = q('.stats-strip, .en-stats');
    var hb = box(hero), sb = box(strip);
    /* Первый блок ПОСЛЕ героя (если полосы нет) — чтобы видеть зазор. */
    var next = null, nextTag = null;
    if (hero && !strip) {
      var sib = hero.nextElementSibling;
      while (sib && !box(sib)) sib = sib.nextElementSibling;
      if (sib) { next = box(sib); nextTag = tag(sib); }
    }
    var badges = [];
    var all = document.querySelectorAll('${BADGE_SEL}');
    for (var i = 0; i < all.length; i++) {
      var el = all[i];
      var cs = getComputedStyle(el);
      if (cs.display === 'none' || cs.visibility === 'hidden') continue;
      var bb = box(el);
      if (!bb || bb.w === 0 || bb.h === 0) continue;
      var blk = blockOf(el);
      var kb = box(blk);
      var inStrip = false, n = el;
      while (n) { if (n === strip) { inStrip = true; break; } n = n.parentElement; }
      var bs = blk ? getComputedStyle(blk) : null;
      badges.push({
        text: (el.textContent || '').trim().slice(0, 40),
        cls: typeof el.className === 'string' ? el.className.trim() : '',
        where: path(el),
        block: blk ? tag(blk) : null,
        blockH: kb ? kb.h : null,
        insetL: blk ? r1(bb.l - kb.l) : null,
        insetT: blk ? r1(bb.t - kb.t) : null,
        padL: bs ? bs.paddingLeft : null,
        padT: bs ? bs.paddingTop : null,
        h: bb.h, fs: cs.fontSize,
        inStrip: inStrip
      });
    }
    var out = {
      w: window.innerWidth,
      hero: hero ? tag(hero) : null,
      strip: strip ? tag(strip) : null,
      heroB: hb ? hb.b : null,
      stripT: sb ? sb.t : null,
      stripB: sb ? sb.b : null,
      /* overlap>0 — полоса НАЛОЖЕНА на герой */
      overlap: (hb && sb) ? r1(hb.b - sb.t) : null,
      /* gap — чистый зазор между низом героя и верхом полосы */
      gap: (hb && sb) ? r1(sb.t - hb.b) : null,
      nextTop: next ? next.t : null,
      nextTag: nextTag,
      nextGap: (hb && next) ? r1(next.t - hb.b) : null,
      stripH: sb ? sb.h : null,
      badges: badges
    };
    document.title = 'LA-JSON:' + JSON.stringify(out);
  }
  if (document.readyState === 'complete') { run(); } else { window.addEventListener('load', run); }
  setTimeout(run, 1200);
  setTimeout(run, 2600);
})();
`;

function withProbe(rel) {
  const src = path.join(ROOT, rel);
  const dir = path.dirname(src);
  const tmp = path.join(dir, '_la.' + path.basename(src));
  let html = fs.readFileSync(src, 'utf8');
  html = html.replace(/<\/body>/i, '<script>' + PROBE + '</script></body>');
  if (html.indexOf('LA-JSON') === -1) html += '<script>' + PROBE + '</script>';
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
      '--window-size=' + width + ',' + (height || 2000),
      '--dump-dom', url
    ], { encoding: 'utf8', maxBuffer: 1 << 28, stdio: ['ignore', 'pipe', 'ignore'] });
  } finally {
    try { fs.unlinkSync(tmp); } catch (e) {}
    try { fs.rmSync(USER_DIR, { recursive: true, force: true }); } catch (e) {}
  }
  const m = dom.match(/LA-JSON:(\{[\s\S]*?\})<\/title>/);
  if (!m) return { file: rel, width, error: 'no LA-JSON in dump' };
  let data;
  try { data = JSON.parse(m[1]); } catch (e) { return { file: rel, width, error: 'bad json' }; }
  data.file = rel; data.width = width;
  return data;
}

const argv = process.argv.slice(2);
const flags = { json: false, badges: false, tsv: false };
const args = [];
for (const a of argv) {
  if (a === '--json') flags.json = true;
  else if (a === '--badges') flags.badges = true;
  else if (a === '--tsv') flags.tsv = true;
  else args.push(a);
}
const width = parseInt(args[0], 10);
const pages = args.slice(1);
const out = pages.map(function (p) { return measure(p, width); });

if (flags.json) {
  console.log(JSON.stringify(out, null, 1));
} else if (flags.tsv) {
  console.log(['page', 'width', 'block', 'label', 'insetL', 'insetT', 'padL', 'padT', 'h', 'fs'].join('\t'));
  for (const d of out) {
    if (d.error) { console.log(d.file + '\t' + d.width + '\tERROR\t' + d.error); continue; }
    for (const b of d.badges) {
      console.log([d.file, d.width, b.block || '-', b.text, b.insetL, b.insetT, b.padL, b.padT, b.h, b.fs].join('\t'));
    }
  }
} else {
  for (const d of out) {
    if (d.error) { console.log('  ' + d.file + ' @' + d.width + '  ERROR ' + d.error); continue; }
    console.log('  ' + (d.file + ' @' + d.width).padEnd(32) +
      ' hero=' + String(d.heroB).padStart(8) +
      ' stripT=' + String(d.stripT).padStart(8) +
      ' OVERLAP=' + String(d.overlap).padStart(6) +
      ' gap=' + String(d.gap).padStart(6) +
      ' stripH=' + String(d.stripH).padStart(6) +
      ' next=' + String(d.nextTop).padStart(8) + '/' + String(d.nextGap).padStart(6) +
      ' badges=' + d.badges.length);
    if (flags.badges) {
      for (const b of d.badges) {
        console.log('      insetL=' + String(b.insetL).padStart(6) + ' insetT=' + String(b.insetT).padStart(6) +
          ' padL=' + String(b.padL).padStart(7) + ' padT=' + String(b.padT).padStart(7) +
          ' h=' + String(b.h).padStart(5) + ' fs=' + String(b.fs).padStart(6) +
          '  ' + JSON.stringify(b.text.slice(0, 26)) + '  in=' + b.block + '  ' + b.where);
      }
    }
  }
}
