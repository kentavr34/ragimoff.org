#!/usr/bin/env node
/* mobile-audit.js — обмер мобильных пропорций страницы (headless Chrome CLI).
 *
 * Отвечает на запрос владельца 03.10.2026: «в мобильной версии пропорции
 * неверны у многих объектов — стилизовать, стандартизировать».
 * Снимает по каждому объекту: ширину/высоту, долю от колонки, кегль,
 * отступы секций; отмечает больные места:
 *   smallimg — изображение уже 60 % колонки там, где несёт смысл;
 *   lowbtn   — кнопка ниже 44 px по высоте;
 *   overflow — элемент вылезает за правое поле (гориз. прокрутка).
 *
 * Запуск (из корня репозитория, сервер на HERO_PORT):
 *   node _tools/mobile-audit.js --out out.json --width 390 --jobs 4 index.html tehsil.html
 */
'use strict';
const fs = require('fs');
const path = require('path');
const { execFile } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const CHROME = process.env.HERO_CHROME || 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const PORT = process.env.HERO_PORT || '8765';
const TMPBASE = process.env.HERO_TMP || 'D:/ragimoff-tmp';

const PROBE = `
(function () {
  function r1(v) { return Math.round(v * 10) / 10; }
  function box(el) { if (!el) return null; var r = el.getBoundingClientRect();
    return { x: r1(r.left), y: r1(r.top), w: r1(r.width), h: r1(r.height), b: r1(r.bottom), r: r1(r.right) }; }
  function cs(el) { return getComputedStyle(el); }
  var out = {};
  function measure() {
    var doc = document;
    out.w = window.innerWidth; out.cw = document.documentElement.clientWidth;
    out.docW = document.documentElement.scrollWidth;
    out.hScroll = out.docW > out.cw + 1;
    out.href = location.pathname;
    /* виновники горизонтальной прокрутки. Считаем ВСЕГДА, а не только при
       hScroll: html/body несут overflow-x: clip, и вылет за вьюпорт не даёт
       полосы прокрутки — содержимое просто срезается, а замер молчит
       (так выглядела подпись «BEYNƏLXALQ METODİKA…» в полосе цифр). */
    out.overflow = [];
    function inFixed(el) {
      for (var p = el; p && p !== document.body; p = p.parentElement) {
        var ps2 = cs(p);
        if (ps2.position === 'fixed') return true;
        if (ps2.visibility === 'hidden' || ps2.display === 'none') return true;
      }
      return false;
    }
    {
      var all = document.querySelectorAll('body *');
      for (var i = 0; i < all.length; i++) {
        var el = all[i], st = cs(el);
        if (st.position === 'fixed' || inFixed(el)) continue;
        var b = el.getBoundingClientRect();
        if (b.width < 1) continue;
        if (b.right > out.cw + 1.5 || b.left < -1.5) {
          out.overflow.push({ sel: el.tagName.toLowerCase() + (el.className && typeof el.className === 'string' ? '.' + el.className.split(/\\s+/).slice(0, 2).join('.') : ''), l: r1(b.left), r: r1(b.right), w: r1(b.width) });
          if (out.overflow.length > 12) break;
        }
      }
    }
    /* Полоса цифр: подписи в две колонки — проверяем, что текст не срезан */
    out.stats = [];
    var stats = document.querySelectorAll('.stat-item, .en-stat, .ind-stat');
    for (var si = 0; si < stats.length && si < 8; si++) {
      var se = stats[si], sn = se.querySelector('.stat-num, .num, .l'), sl = se.querySelector('.stat-label, .lbl, .t'), sb = box(se);
      out.stats.push({
        x: sb.x, y: sb.y, w: sb.w,
        num: sn ? { t: (sn.textContent || '').trim().slice(0, 14), fs: cs(sn).fontSize, sw: sn.scrollWidth, cw: sn.clientWidth } : null,
        label: sl ? { t: (sl.textContent || '').trim().slice(0, 26), fs: cs(sl).fontSize, sw: sl.scrollWidth, cw: sl.clientWidth, ws: cs(sl).whiteSpace, cut: sl.scrollWidth > sl.clientWidth + 1 } : null
      });
    }
    /* полотно страницы: контейнер, от которого считаем долю */
    var container = document.querySelector('.hero-inner, .page-hero-x-inner, .pg-hero-inner, .sec-inner, .container, main') || document.body;
    var cwb = box(container);
    out.colW = cwb ? cwb.w : out.cw;
    /* Клипованнный текст: коробка режет содержимое по горизонтали
       (ovh/overflow-x: hidden или clip). Именно так выглядит «обкусанная»
       подпись в полосе цифр на телефоне. */
    out.clipped = [];
    var walk = document.querySelectorAll('body *');
    for (var ci = 0; ci < walk.length; ci++) {
      var cel = walk[ci], cst2 = cs(cel);
      if (cst2.display === 'none' || cst2.visibility === 'hidden') continue;
      if (cel.clientWidth < 8) continue;
      var ox = cst2.overflowX;
      if (ox !== 'hidden' && ox !== 'clip') continue;
      var direct = '';
      for (var n2 = 0; n2 < cel.childNodes.length; n2++) if (cel.childNodes[n2].nodeType === 3) direct += cel.childNodes[n2].nodeValue;
      if (!/\\S/.test(direct)) continue;
      if (cel.scrollWidth > cel.clientWidth + 1) {
        out.clipped.push({ cls: cel.tagName.toLowerCase() + (typeof cel.className === 'string' && cel.className ? '.' + cel.className.split(/\\s+/).slice(0, 2).join('.') : ''), txt: direct.replace(/\\s+/g, ' ').trim().slice(0, 40), cw: cel.clientWidth, sw: cel.scrollWidth, ws: cst2.whiteSpace });
      }
      if (out.clipped.length > 10) break;
    }
    /* ── ГЕРОЙ ── */
    var hero = document.querySelector('.page-hero, .page-hero-x, .pg-hero');
    if (hero) {
      var hb = box(hero), hs = cs(hero);
      var badge = hero.querySelector('.badge, .ph-badge');
      var h1 = hero.querySelector('.hero-h1, .ph-h1');
      var lead = hero.querySelector('.hero-lead, .ph-sub');
      var search = hero.querySelector('.hero-search-wrap, .ph-search-wrap');
      var img = hero.querySelector('.photo-col img');
      var col = hero.querySelector('.photo-col');
      function ink(el) {
        if (!el) return 0;
        var walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, null), rows = [], n;
        while ((n = walker.nextNode())) {
          if (!n.nodeValue || !/\\S/.test(n.nodeValue)) continue;
          var pe = n.parentElement; if (!pe) continue;
          var ps = cs(pe); if (ps.display === 'none' || ps.visibility === 'hidden') continue;
          var rg = document.createRange(); rg.selectNodeContents(n);
          var rc = rg.getClientRects();
          for (var k = 0; k < rc.length; k++) if (rc[k].width > 1 && rc[k].height > 1) {
            var t = Math.round(rc[k].top), f = 0;
            for (var q = 0; q < rows.length; q++) if (rows[q] === t) { f = 1; break; }
            if (!f) rows.push(t);
          }
        }
        return rows.length;
      }
      function rel(el) { if (!el) return null; var b = box(el); return { y: r1(b.y - hb.y), h: b.h, w: b.w, b: r1(b.b - hb.y), fs: cs(el).fontSize }; }
      out.hero = {
        h: hb.h, w: hb.w,
        badge: rel(badge), h1: rel(h1), lead: rel(lead), search: rel(search),
        photo: img ? (function () { var b = box(img); return { y: r1(b.y - hb.y), w: b.w, h: b.h, b: r1(b.b - hb.y), share: r1(b.w / (col ? box(col).w : out.colW) * 100) / 100, shareCol: r1(b.w / out.colW * 100) / 100, natural: [img.naturalWidth, img.naturalHeight] }; })() : null,
        photoBand: col ? box(col).h : null,
        gaps: {
          badgeToH1: (badge && h1) ? r1(h1.getBoundingClientRect().top - badge.getBoundingClientRect().bottom) : null,
          h1ToLead: (h1 && lead) ? r1(lead.getBoundingClientRect().top - (h1.getBoundingClientRect().top + (ink(h1) || 1) * parseFloat(cs(h1).fontSize) * 1.15)) : null,
          leadToSearch: (lead && search) ? r1(search.getBoundingClientRect().top - lead.getBoundingClientRect().bottom) : null,
          searchToBottom: search ? r1(hb.b - search.getBoundingClientRect().bottom) : null
        },
        h1Lines: ink(h1), leadLines: ink(lead)
      };
    } else { out.hero = null; }
    /* ── СЕКЦИИ: паддинги и кегли ── */
    out.sections = [];
    var secs = document.querySelectorAll('section[class], .stats-strip, .cta-band, .gallery-band, .books-band, div.sec-pad');
    for (var s = 0; s < secs.length && s < 14; s++) {
      var el2 = secs[s], st2 = cs(el2), b2 = box(el2);
      var h2 = el2.querySelector('.sec-h2, h2'), sub = el2.querySelector('.sec-sub, .sec-lead, p');
      out.sections.push({
        cls: String(el2.className).split(/\\s+/).slice(0, 3).join('.'), h: r1(b2.h),
        padTop: parseFloat(st2.paddingTop), padBottom: parseFloat(st2.paddingBottom),
        h2fs: h2 ? cs(h2).fontSize : null, h2w: h2 ? box(h2).w : null,
        subfs: sub ? cs(sub).fontSize : null,
        subw: sub ? r1(box(sub).w) : null
      });
    }
    /* ── КАРТОЧКИ ── */
    out.cards = [];
    var cardSel = '.card, .blog-card, .svc-card, .xid-card, .feat-card, .step-card, .price-card, .book-card, .review-card, .article-card, .post-card, .news-card';
    var cards = document.querySelectorAll(cardSel);
    var seen = {};
    for (var c = 0; c < cards.length && out.cards.length < 10; c++) {
      var ce = cards[c], key = String(ce.className).split(/\\s+/)[0];
      var cb = box(ce), cst = cs(ce);
      var cimg = ce.querySelector('img'), ch3 = ce.querySelector('h3, h4'), cp = ce.querySelector('p');
      out.cards.push({ cls: String(ce.className).split(/\\s+/).slice(0, 2).join('.'), w: cb.w, h: r1(cb.h), pad: cst.padding,
        imgW: cimg ? box(cimg).w : null, imgH: cimg ? box(cimg).h : null,
        h3fs: ch3 ? cs(ch3).fontSize : null, pfs: cp ? cs(cp).fontSize : null });
    }
    /* ── КНОПКИ ── */
    out.buttons = [];
    var btns = document.querySelectorAll('.btn, .btn-fill, .btn-line, .btn-dark, .hero-search-btn, .ph-search-btn, .filter-btn, .c-link, .card-link, button[type=submit], .dir-link');
    for (var b3 = 0; b3 < btns.length && out.buttons.length < 14; b3++) {
      var be = btns[b3], bb2 = box(be), bcs = cs(be);
      if (bb2.w < 1) continue;
      out.buttons.push({ cls: String(be.className).split(/\\s+/).slice(0, 2).join('.'), w: r1(bb2.w), h: r1(bb2.h), fs: bcs.fontSize, low: bb2.h < 44 });
    }
    /* ── ИЗОБРАЖЕНИЯ В СЕКЦИЯХ ── */
    out.imgs = [];
    var imgs = document.querySelectorAll('img');
    for (var im = 0; im < imgs.length && out.imgs.length < 16; im++) {
      var ie = imgs[im], ib = box(ie);
      if (ib.w < 4 || ib.h < 4) continue;
      var par = ie.closest('.sec-inner, section, .card, .grid-3, .grid-2, div') || document.body;
      var pw = box(par) ? box(par).w : out.colW;
      out.imgs.push({ cls: String(ie.className || '').split(/\\s+/)[0], src: (ie.getAttribute('src') || '').split('/').pop().slice(0, 40),
        w: ib.w, h: ib.h, parW: r1(pw), share: r1(ib.w / Math.max(pw, 1) * 100) / 100 });
    }
    /* ── ПОЛЯ/ФОРМЫ ── */
    out.fields = [];
    var flds = document.querySelectorAll('input[type=text], input[type=email], input[type=tel], textarea, select');
    for (var f = 0; f < flds.length && out.fields.length < 8; f++) {
      var fe = flds[f], fb = box(fe);
      if (fb.w < 1) continue;
      out.fields.push({ id: fe.id || String(fe.className).split(/\\s+/)[0] || fe.tagName.toLowerCase(), w: r1(fb.w), h: r1(fb.h), fs: cs(fe).fontSize });
    }
    out.st = document.readyState;
    out.fonts = (document.fonts && document.fonts.status) || 'n/a';
    out.panW = document.documentElement.clientWidth;
    return out;
  }
  function emit(o) {
    var doc = document;
    try { if (window.top && window.top !== window.self) doc = window.top.document; } catch (e) {}
    var pre = doc.getElementById('__mob_out');
    if (!pre) { pre = doc.createElement('pre'); pre.id = '__mob_out'; (doc.body || doc.documentElement).appendChild(pre); }
    pre.textContent += btoa(unescape(encodeURIComponent(JSON.stringify(o)))) + '\\n';
  }
  var last = null;
  function imgsReady() {
    /* пока фото не доехало, naturalWidth = 0 и пропорция кадра неизвестна:
       замер ловил фото 147,9×284,7 (0,42 колонки) вместо 271×285 (0,77) —
       width:auto без собственной ширины отдаёт браузеру «заглушку» 300×150 */
    var im = document.images;
    for (var i = 0; i < im.length; i++) { if (!im[i].complete) return false; }
    var hp = document.querySelector('.photo-col img');
    if (hp && !hp.naturalWidth) return false;
    return true;
  }
  /* ленивую загрузку снимаем сразу: при 320 фото героя уезжало за кадр
     обёртки и не грузилось вовсе (замер: naturalWidth 0) */
  try {
    var li = document.querySelectorAll('img[loading="lazy"]');
    for (var lk = 0; lk < li.length; lk++) li[lk].loading = 'eager';
  } catch (e) {}
  function settled(tries) {
    tries = tries || 0;
    var a = last, b = measure();
    if (a && imgsReady() && Math.abs((a.hero ? a.hero.h : 0) - (b.hero ? b.hero.h : 0)) < 0.6 && a.cw === b.cw) { emit(b); return; }
    if (tries > 40) { emit(b); return; }
    last = b;
    setTimeout(function () { settled(tries + 1); }, 300);
  }
  if (document.readyState === 'complete') settled(); else window.addEventListener('load', function () { settled(); });
  setTimeout(settled, 1500);
  window.addEventListener('load', function () {
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { setTimeout(function () { settled(); }, 600); });
  });
})();
`;

const PRESCRIPT = 'try{localStorage.setItem("ragimoff_lang",___LANG___);}catch(e){}';

function rewriteFonts(html, on) {
  if (!on) return html;
  const P = process.env.AUDIT_FONTCACHE_PORT || '8776';
  const crypto = require('crypto');
  const h = (u) => crypto.createHash('md5').update(u).digest('hex');
  html = html.replace(/https:\/\/fonts\.googleapis\.com\/css2\?[^"'`)\s<>]+/g, (u) => 'http://127.0.0.1:' + P + '/fc/' + h(u.replace(/&amp;/g, '&')) + '.css');
  html = html.replace(/https:\/\/fonts\.gstatic\.com\/[^"'`)\s<>)]+/g, (u) => 'http://127.0.0.1:' + P + '/fc/' + h(u) + '.woff2');
  return html;
}

let dirSeq = 0;
function withProbe(rel) {
  const src = path.join(ROOT, rel);
  const tmp = path.join(path.dirname(src), '_mob.' + process.pid + '.' + (++dirSeq) + '.' + path.basename(src));
  let html = fs.readFileSync(src, 'utf8');
  const lang = /(^|[\/])ru[\/]/.test(rel) ? 'ru' : (/(^|[\/])en[\/]/.test(rel) ? 'en' : 'az');
  html = html.replace(/<head([^>]*)>/i, '<head$1><script>' + PRESCRIPT.replace('___LANG___', '"' + lang + '"') + '</script>');
  html = rewriteFonts(html, !process.env.HERO_NO_FONTCACHE);
  html = html.replace(/<\/body>/i, '<script>' + PROBE + '</script></body>');
  if (html.indexOf('__mob_out') === -1) html += '<script>' + PROBE + '</script>';
  fs.writeFileSync(tmp, html, 'utf8');
  return tmp;
}

function measureOnce(rel, width, profileDir) {
  return new Promise((resolve) => {
    const tmp = withProbe(rel);
    const relTmp = path.relative(ROOT, tmp).replace(/\\/g, '/');
    let url, wrapper = null, winW = width;
    if (width < 500) {
      const wtmp = path.join(ROOT, '_mob.w.' + process.pid + '.' + (++dirSeq) + '.html');
      fs.writeFileSync(wtmp, '<!DOCTYPE html><html><head><meta charset="utf-8"><title>narrow</title>' +
        '<style>html,body{margin:0;padding:0;background:#07090E}#f{width:' + width + 'px;height:1000px;border:0;display:block}</style>' +
        '</head><body><iframe id="f" src="' + encodeURI(relTmp) + '"></iframe></body></html>', 'utf8');
      wrapper = wtmp;
      url = 'http://127.0.0.1:' + PORT + '/' + encodeURI(path.relative(ROOT, wtmp).replace(/\\/g, '/'));
      winW = 520;
    } else {
      url = 'http://127.0.0.1:' + PORT + '/' + encodeURI(relTmp);
    }
    const userDir = profileDir || (TMPBASE + '/mob-prof-' + process.pid + '-' + dirSeq);
    execFile(CHROME, [
      '--headless=new', '--disable-gpu', '--no-sandbox', '--disable-extensions',
      '--lang=az', '--accept-lang=az',
      '--user-data-dir=' + userDir,
      '--host-resolver-rules=MAP ipapi.co 127.0.0.1:9',
      '--virtual-time-budget=12000',
      '--window-size=' + winW + ',1600',
      '--dump-dom', url
    ], { encoding: 'utf8', maxBuffer: 1 << 28, timeout: 240000, killSignal: 'SIGKILL' }, (err, stdout) => {
      try { fs.unlinkSync(tmp); } catch (e) {}
      if (wrapper) { try { fs.unlinkSync(wrapper); } catch (e) {} }
      if (err) { resolve({ error: String(err.message || err).slice(0, 160) }); return; }
      const block = stdout.match(/<pre id="__mob_out">([\s\S]*?)<\/pre>/);
      if (!block) { resolve({ error: 'no __mob_out in dump' }); return; }
      const lines = block[1].split('\n').map(s => s.trim()).filter(Boolean);
      const snaps = [];
      for (const ln of lines) { try { snaps.push(JSON.parse(Buffer.from(ln, 'base64').toString('utf8'))); } catch (e) {} }
      if (!snaps.length) { resolve({ error: 'bad json' }); return; }
      resolve({ snaps });
    });
  });
}

async function pool(items, size, fn) {
  const out = new Array(items.length);
  let idx = 0;
  async function worker(slot) {
    while (idx < items.length) {
      const i = idx++;
      const profile = TMPBASE + '/mob-prof-' + PORT + '-' + size + '-' + slot;
      out[i] = await fn(items[i], profile);
      process.stderr.write('.');
    }
  }
  await Promise.all(Array.from({ length: Math.min(size, items.length) }, (_, k) => worker(k)));
  process.stderr.write('\n');
  return out;
}

async function measure(rel, width, profile, attempts) {
  attempts = attempts || 3;
  let lastErr = null;
  for (let a = 0; a < attempts; a++) {
    const r = await measureOnce(rel, width, profile);
    if (r.error) { lastErr = r.error; continue; }
    const ok = r.snaps.filter(d => d.st === 'complete' && (d.fonts === 'loaded' || d.fonts === 'n/a'));
    if (!ok.length) { lastErr = 'no settled snapshot'; continue; }
    const good = ok[ok.length - 1];
    good.file = rel; good.width = width;
    return good;
  }
  return { file: rel, width, error: lastErr || 'failed' };
}

(async () => {
  const argv = process.argv.slice(2);
  let width = 390, jobs = 4, outFile = null, listFile = null;
  const pages = [];
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--width') width = parseInt(argv[++i], 10);
    else if (a === '--jobs') jobs = parseInt(argv[++i], 10);
    else if (a === '--out') outFile = argv[++i];
    else if (a === '--list') listFile = argv[++i];
    else pages.push(a);
  }
  const list = listFile ? fs.readFileSync(listFile, 'utf8').split(/\r?\n/).map(s => s.trim()).filter(Boolean) : pages;
  const res = await pool(list, jobs, (p, profile) => measure(p, width, profile, 3));
  if (outFile) fs.writeFileSync(outFile, JSON.stringify(res, null, 1), 'utf8');
  else console.log(JSON.stringify(res, null, 1));
})();
