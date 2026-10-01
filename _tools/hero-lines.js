#!/usr/bin/env node
/* hero-lines.js — построчный обмер заголовка и лида героя (headless Chrome CLI).
 *
 * Зачем: правило владельца «делить на строки по словам, строки равной длины».
 * Существующие инструменты считают ЧИСЛО строк, но не их длину и не то,
 * какие спаны реально видны. Этот зонд печатает по каждому текстовому узлу:
 *   - display и видимость (mob/desk-спаны),
 *   - прямоугольники строк (Range.getClientRects) — сколько строк и какая
 *     у каждой ширина и «перекос» (max/min).
 *
 * Запуск (сервер: python -m http.server 8765 --bind 127.0.0.1 -d .):
 *   node _tools/hero-lines.js 390 index.html ru/index.html en/index.html
 *   node _tools/hero-lines.js 390 --json index.html
 * Узкая ширина (<500) меряется в iframe: окно Chrome на Windows не бывает
 * уже 500 px, --window-size=390 даёт innerWidth 500.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const CHROME = process.env.HERO_CHROME || 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const PORT = process.env.HERO_PORT || '8765';
const TMPBASE = process.env.HERO_TMP || 'D:/ragimoff-tmp';

const PROBE = `
(function () {
  function r1(v) { return Math.round(v * 10) / 10; }
  function rectOf(node) {
    var r = document.createRange();
    r.selectNodeContents(node);
    var rects = r.getClientRects(), out = [];
    for (var i = 0; i < rects.length; i++) {
      var b = rects[i];
      if (b.width < 1 || b.height < 1) continue;
      var top = Math.round(b.top);
      var found = null;
      for (var j = 0; j < out.length; j++) if (out[j].top === top) { found = out[j]; break; }
      if (found) { found.l = Math.min(found.l, r1(b.left)); found.r = Math.max(found.r, r1(b.right)); }
      else out.push({ top: top, l: r1(b.left), r: r1(b.right) });
    }
    out.sort(function (a, b) { return a.top - b.top; });
    out.forEach(function (o) { o.w = r1(o.r - o.l); });
    return out;
  }
  function linesOf(el) {
    if (!el) return null;
    var cs = getComputedStyle(el);
    var b = el.getBoundingClientRect();
    var rects = rectOf(el);
    var ws = rects.map(function (o) { return o.w; });
    var mx = ws.length ? Math.max.apply(null, ws) : 0;
    var mn = ws.length ? Math.min.apply(null, ws) : 0;
    var spans = [];
    var kids = el.querySelectorAll('span');
    for (var i = 0; i < kids.length; i++) {
      var k = kids[i], kcs = getComputedStyle(k), kb = k.getBoundingClientRect();
      var klines = kcs.display === 'none' ? [] : rectOf(k);
      if (!/lead|sub|h1/.test(k.className)) continue;
      spans.push({
        cls: k.className, display: kcs.display, visible: kb.width > 0 && kb.height > 0,
        n: klines.length, ws: klines.map(function (o) { return o.w; }),
        text: (k.textContent || '').replace(/\\s+/g, ' ').trim().slice(0, 70)
      });
    }
    return {
      sel: el.className || el.tagName, x: r1(b.left), w: r1(b.width), h: r1(b.height),
      fs: cs.fontSize, lh: cs.lineHeight, wrap: cs.textWrap || cs.textWrapStyle || '-',
      align: cs.textAlign, textAlign: cs.textAlign,
      n: rects.length, ws: ws, skew: mn ? r1(mx / mn) : null,
      maxw: mx, spans: spans,
      text: (el.textContent || '').replace(/\\s+/g, ' ').trim().slice(0, 130)
    };
  }
  function run() {
    var out = {
      url: location.pathname, w: window.innerWidth, cw: document.documentElement.clientWidth,
      docW: document.documentElement.scrollWidth,
      hScroll: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1
    };
    var hero = document.querySelector('.page-hero, .page-hero-x, .pg-hero');
    out.heroFound = !!hero;
    if (hero) {
      out.h1 = linesOf(hero.querySelector('.hero-h1, .ph-h1, h1'));
      out.lead = linesOf(hero.querySelector('.hero-lead, .ph-sub'));
      var badge = hero.querySelector('.badge, .ph-badge');
      if (badge) { var bb = badge.getBoundingClientRect(); out.badgeTop = r1(bb.top - hero.getBoundingClientRect().top); }
      var col = hero.querySelector('.photo-col'), img = hero.querySelector('.photo-col img');
      if (img) {
        var ib = img.getBoundingClientRect(), cb = col.getBoundingClientRect();
        out.photo = { w: r1(ib.width), h: r1(ib.height), colW: r1(cb.width), ratio: r1(ib.width / cb.width), src: img.getAttribute('src') };
      }
      var hb = hero.getBoundingClientRect();
      out.hero = { h: r1(hb.height), top: r1(hb.top) };
    }
    document.title = 'HL-JSON:' + JSON.stringify(out);
  }
  function go() { setTimeout(run, 400); }
  if (document.readyState === 'complete') go(); else window.addEventListener('load', go);
})();
`;

function withProbe(rel) {
  const src = path.join(ROOT, rel);
  const tmp = path.join(path.dirname(src), '_hl.' + process.pid + '.' + path.basename(src));
  let html = fs.readFileSync(src, 'utf8');
  const lang = /(^|[\/])ru[\/]/.test(rel) ? 'ru' : (/(^|[\/])en[\/]/.test(rel) ? 'en' : 'az');
  html = html.replace(/<head([^>]*)>/i, '<head$1><script>try{localStorage.setItem("ragimoff_lang","' + lang + '");}catch(e){}</script>');
  html = html.replace(/<\/body>/i, '<script>' + PROBE + '</script></body>');
  fs.writeFileSync(tmp, html, 'utf8');
  return tmp;
}

function measure(rel, width) {
  const tmp = withProbe(rel);
  const relTmp = path.relative(ROOT, tmp).replace(/\\/g, '/');
  let target = 'http://127.0.0.1:' + PORT + '/' + encodeURI(relTmp);
  let wrapper = null;
  if (width < 500) {
    wrapper = path.join(ROOT, '_hl.w.' + process.pid + '.html');
    fs.writeFileSync(wrapper,
      '<!DOCTYPE html><html><head><meta charset="utf-8"></head><body style="margin:0">' +
      '<iframe id="f" src="' + encodeURI(relTmp) + '" style="width:' + width + 'px;height:1200px;border:0"></iframe>' +
      '<script>(function(){var t0=Date.now();var iv=setInterval(function(){try{var d=document.getElementById("f").contentDocument;var ti=d.title||"";if(ti.indexOf("HL-JSON:")===0){clearInterval(iv);var j=ti.slice(8);document.title="HL-JSON:"+j;}}catch(e){}if(Date.now()-t0>20000)clearInterval(iv);},200);})();</script>' +
      '</body></html>', 'utf8');
    target = 'http://127.0.0.1:' + PORT + '/' + path.relative(ROOT, wrapper).replace(/\\/g, '/');
  }
  const userDir = TMPBASE + '/hl-prof-' + PORT + '-' + process.pid + '-' + Math.floor(Math.random() * 1e6);
  let dom = '';
  try {
    dom = execFileSync(CHROME, [
      '--headless=new', '--disable-gpu', '--no-sandbox', '--disable-extensions',
      '--lang=az', '--accept-lang=az',
      '--host-resolver-rules=MAP ipapi.co 127.0.0.1:9',
      '--user-data-dir=' + userDir,
      '--virtual-time-budget=11000',
      '--window-size=' + Math.max(520, width) + ',1400',
      '--dump-dom', target
    ], { encoding: 'utf8', maxBuffer: 1 << 28, stdio: ['ignore', 'pipe', 'ignore'] });
  } finally {
    try { fs.unlinkSync(tmp); } catch (e) {}
    if (wrapper) { try { fs.unlinkSync(wrapper); } catch (e) {} }
    try { fs.rmSync(userDir, { recursive: true, force: true }); } catch (e) {}
  }
  const m = dom.match(/HL-JSON:(\{[\s\S]*?\})<\/title>/);
  if (!m) return { file: rel, width: width, error: 'no HL-JSON' };
  try { const d = JSON.parse(m[1]); d.file = rel; d.width = width; return d; }
  catch (e) { return { file: rel, width: width, error: 'bad json' }; }
}

const argv = process.argv.slice(2);
const json = argv.includes('--json');
const args = argv.filter(function (a) { return a !== '--json'; });
const width = parseInt(args[0], 10);
const pages = args.slice(1);
const res = pages.map(function (p) { return measure(p, width); });
if (json) { console.log(JSON.stringify(res, null, 1)); process.exit(0); }

const fs2 = fs;
pages.forEach(function (p) {
  const d = res[pages.indexOf(p)];
  if (d.error) { console.log(p + '  ERROR ' + d.error); return; }
  console.log('── ' + p + ' @' + width + '  hero=' + (d.hero ? d.hero.h : '-') + '  hScroll=' + d.hScroll + (d.photo ? ('  photo=' + d.photo.w + 'x' + d.photo.h + ' ratio=' + d.photo.ratio) : '  photo=-'));
  ['h1', 'lead'].forEach(function (k) {
    const L = d[k];
    if (!L) { console.log('   ' + k + ': —'); return; }
    console.log('   ' + k + ': lines=' + L.n + ' widths=[' + L.ws.join(', ') + '] skew=' + L.skew + ' fs=' + L.fs + ' wrap=' + L.wrap);
    (L.spans || []).forEach(function (s) {
      console.log('      span .' + s.cls + ' display=' + s.display + ' n=' + s.n + ' ws=[' + s.ws.join(', ') + '] «' + s.text + '»');
    });
  });
});
