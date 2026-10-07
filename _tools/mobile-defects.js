#!/usr/bin/env node
/* mobile-defects.js — сплошной обмер мобильной вёрстки на 7 классов дефектов.
 *
 * Задание владельца 05.10.2026: «Проверь все страницы сайта в мобильной версии
 * на наличие таких дизайнерских уродств… составь список причин… измени и добавь
 * как правило в файл стиля дизайна; примени ко всем страницам».
 *
 * Классы (пороговые значения — DESIGN-STANDARDS §30 «Мобильная сетка и запреты»):
 *   GAP   пустая полоса по вертикали (нет ни текста, ни изображения, ни границы,
 *         ни контрастной заливки) больше 100 px;
 *   INSET элемент прижат к грани блока: панель без паддинга и её первый
 *         ярлык/заголовок/кнопка ближе 20 px по горизонтали, 12 px по вертикали;
 *   OVERF переполнение: вылет за вьюпорт, обрезанный текст (scrollWidth >
 *         clientWidth при overflow hidden/clip), текст шире своего контейнера;
 *   PHOTO фотография лежит прямоугольником на тёмной подложке (по пикселям:
 *         непрозрачная рамка, близкая к фону страницы, при контрастной середине)
 *         — вместо вырезки или маски-градиента;
 *   ALIGN разъезд выравнивания: у центрированного заголовка блока лид/подзаголовок
 *         того же стека идёт по левому краю; наезд подписи на ярлык/кнопку;
 *   SIZE  непропорциональные размеры: кнопка ниже 44 px, заголовок выше нормы,
 *         межстрочный интервал больше 1.78, фото уже 45 % колонки;
 *   STICK липкое/наезжающее: полоса цифр накрывает герой; fixed/sticky панель
 *         перекрывает чужой текст.
 *
 * Запуск (из корня репозитория, сервер на HERO_PORT и font-cache на 8776):
 *   python -m http.server 8765 --bind 127.0.0.1 -d .
 *   FONTCACHE_PORT=8776 node _tools/font-cache-server.js &
 *   node _tools/mobile-defects.js --width 390 --jobs 4 --out before_390.json --list pages.txt
 */
'use strict';
const fs = require('fs');
const path = require('path');
const { execFile } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const CHROME = process.env.HERO_CHROME || 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const PORT = process.env.HERO_PORT || '8765';
const TMPBASE = process.env.HERO_TMP || 'D:/ragimoff-tmp';

/* ────────────────────────── пробник (исполняется в странице) ────────────── */
function probeFn() {
  var CW = document.documentElement.clientWidth;
  var r1 = function (v) { return Math.round(v * 10) / 10; };
  function boxOf(el) {
    var r = el.getBoundingClientRect();
    return { l: r1(r.left), t: r1(r.top), r: r1(r.right), b: r1(r.bottom), w: r1(r.width), h: r1(r.height) };
  }
  function csOf(el) { return getComputedStyle(el); }
  function selOf(el) {
    var s = el.tagName.toLowerCase();
    var cn = (typeof el.className === 'string') ? el.className.trim() : '';
    if (cn) s += '.' + cn.split(/\s+/).slice(0, 2).join('.');
    else if (el.id) s += '#' + el.id;
    return s;
  }
  function visCache() {
    var m = new Map();
    return function (el) {
      if (m.has(el)) return m.get(el);
      var v = true, p = el;
      for (var i = 0; p && p !== document.documentElement && i < 60; p = p.parentElement, i++) {
        var s = csOf(p);
        if (s.display === 'none' || s.visibility === 'hidden') { v = false; break; }
        if (parseFloat(s.opacity) < 0.05) { v = false; break; }
      }
      if (v) { var r = el.getBoundingClientRect(); v = r.width > 0.5 && r.height > 0.5; }
      m.set(el, v);
      return v;
    };
  }
  var visible = visCache();

  function parseColor(c) {
    var m = /rgba?\(([^)]+)\)/.exec(c || '');
    if (!m) return null;
    var p = m[1].split(',').map(function (s) { return parseFloat(s); });
    return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 };
  }
  function dist(a, b) {
    return Math.sqrt(Math.pow(a.r - b.r, 2) + Math.pow(a.g - b.g, 2) + Math.pow(a.b - b.b, 2));
  }
  var bodyS = csOf(document.body), htmlS = csOf(document.documentElement);
  var pageBg = parseColor(bodyS.backgroundColor);
  if (!pageBg || pageBg.a < 0.5) pageBg = parseColor(htmlS.backgroundColor) || { r: 7, g: 9, b: 14, a: 1 };

  /* ── 1. ИНК: текст + медиа + границы + контрастные заливки ───────────── */
  var ink = [];
  function addInk(t, b, src) {
    if (b < t) { var x = t; t = b; b = x; }
    if (b - t < 0.5) return;
    ink.push({ t: t, b: b, src: src });
  }
  var textRects = [];
  var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null);
  var n, guard = 0;
  while ((n = walker.nextNode()) && guard < 6000) {
    guard++;
    if (!n.nodeValue || !/\S/.test(n.nodeValue)) continue;
    var pe = n.parentElement;
    if (!pe || !visible(pe)) continue;
    var rg = document.createRange();
    rg.selectNodeContents(n);
    var rc = rg.getClientRects();
    for (var i = 0; i < rc.length; i++) {
      var q = rc[i];
      if (q.width > 1 && q.height > 1) {
        textRects.push({ l: r1(q.left), t: r1(q.top), r: r1(q.right), b: r1(q.bottom), el: pe });
        addInk(q.top, q.bottom, 'text:' + selOf(pe));
      }
    }
    if (textRects.length > 6000) break;
  }
  var media = document.querySelectorAll('img,svg,video,canvas,iframe,input,textarea,select,button,[contenteditable]');
  for (var mi = 0; mi < media.length && mi < 700; mi++) {
    var me = media[mi];
    if (!visible(me)) continue;
    var mb = boxOf(me);
    addInk(mb.t, mb.b, 'media:' + selOf(me));
  }
  var allEls = document.querySelectorAll('body *');
  for (var ei = 0; ei < allEls.length && ei < 6000; ei++) {
    var ee = allEls[ei];
    var es = csOf(ee);
    if (es.display === 'none') continue;
    var eb = ee.getBoundingClientRect();
    if (eb.width < 1 || eb.height < 1) continue;
    var bt = parseFloat(es.borderTopWidth) || 0, bb = parseFloat(es.borderBottomWidth) || 0;
    if (bt > 0) addInk(eb.top, eb.top + bt, 'border:' + selOf(ee));
    if (bb > 0) addInk(eb.bottom - bb, eb.bottom, 'border:' + selOf(ee));
    var bg = parseColor(es.backgroundColor);
    if (bg && bg.a > 0.02) {
      var eff = { r: bg.r * bg.a + pageBg.r * (1 - bg.a), g: bg.g * bg.a + pageBg.g * (1 - bg.a), b: bg.b * bg.a + pageBg.b * (1 - bg.a) };
      if (dist(eff, pageBg) > 24) addInk(eb.top, eb.bottom, 'fill:' + selOf(ee));
    }
  }

  /* ── GAP: незакрытые полосы по вертикали ─────────────────────────────── */
  var docH = Math.max(document.documentElement.scrollHeight, document.body ? document.body.scrollHeight : 0);
  ink.sort(function (a, b) { return a.t - b.t; });
  var gaps = [], cur = 0, prevSrc = 'top', srcIdx = 0;
  for (var k = 0; k < ink.length; k++) {
    if (ink[k].t > cur + 0.5) {
      var nx = ink[k];
      gaps.push({ t: r1(cur), b: r1(nx.t), h: r1(nx.t - cur), above: prevSrc, below: nx.src });
    }
    if (ink[k].b > cur) { cur = ink[k].b; prevSrc = ink[k].src; }
  }
  if (docH > cur + 0.5) gaps.push({ t: r1(cur), b: r1(docH), h: r1(docH - cur), above: prevSrc, below: 'end' });
  var containers = document.querySelectorAll('section[class],section[id],div.sec-pad,div.sec-3cards,div.sec-2col,div.sec-services,div.sec-blog,.stats-strip,.en-stats,.cta-band,.gallery-band,.books-band,.sec-inner,.ps-inner,.card,.blog-card');
  var containerBoxes = [];
  for (var ci = 0; ci < containers.length && ci < 900; ci++) {
    var ce = containers[ci];
    if (!visible(ce)) continue;
    var cb = boxOf(ce);
    containerBoxes.push({ el: ce, b: cb, s: selOf(ce) });
  }
  var bigGaps = [];
  for (var gi = 0; gi < gaps.length; gi++) {
    if (gaps[gi].h <= 100) continue;
    var g = gaps[gi];
    var holder = null;
    for (var hi = 0; hi < containerBoxes.length; hi++) {
      var hb = containerBoxes[hi].b;
      if (hb.t <= g.t + 1.5 && hb.b >= g.b - 1.5) { if (!holder || (hb.w * hb.h) < holder.w * holder.h) holder = { s: containerBoxes[hi].s, w: hb.w, h: hb.h }; }
    }
    g.where = holder ? holder.s : 'page';
    /* КТО ВИНОВАТ: границы и паддинги, попавшие ВНУТРЬ полосы */
    var crosses = [];
    for (var xi = 0; xi < containerBoxes.length && crosses.length < 5; xi++) {
      var xb = containerBoxes[xi].b, xel = containerBoxes[xi].el;
      var inTop = xb.t > g.t + 1 && xb.t < g.b - 1;
      var inBot = xb.b > g.t + 1 && xb.b < g.b - 1;
      if (!inTop && !inBot) continue;
      var xs = csOf(xel);
      crosses.push({
        s: containerBoxes[xi].s, t: xb.t, b: xb.b,
        pt: parseFloat(xs.paddingTop) || 0, pb: parseFloat(xs.paddingBottom) || 0,
        mt: parseFloat(xs.marginTop) || 0, mb: parseFloat(xs.marginBottom) || 0,
        gapIn: inTop ? r1(xb.t - g.t) : null, gapOut: inBot ? r1(g.b - xb.b) : null
      });
    }
    g.crosses = crosses;
    /* ГРАНИЦЫ ВНУТРИ ПОЛОСЫ: любой элемент, чей верх или низ попал в пустую
       полосу. Это и есть «кто оставил пустоту» — его класс, высота, отступы. */
    var edges = [];
    for (var yi = 0; yi < allEls.length && edges.length < 5; yi++) {
      var ye = allEls[yi];
      if (ye === document.body || ye === document.documentElement) continue;
      var yb = ye.getBoundingClientRect();
      if (yb.width < 1 || yb.height < 0.5) continue;
      var edgeIn = (yb.top > g.t + 1 && yb.top < g.b - 1) || (yb.bottom > g.t + 1 && yb.bottom < g.b - 1);
      if (!edgeIn) continue;
      var ycs = csOf(ye);
      if (ycs.display === 'none' || ycs.visibility === 'hidden') continue;
      edges.push({
        s: selOf(ye), t: r1(yb.top), b: r1(yb.bottom), h: r1(yb.height),
        mt: ycs.marginTop, mb: ycs.marginBottom, pt: ycs.paddingTop, pb: ycs.paddingBottom,
        bg: ycs.backgroundColor, txt: (ye.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 30)
      });
    }
    g.edges = edges;
    bigGaps.push(g);
  }

  /* ── INSET: ярлыки/кнопки/заголовки у грани панели без паддинга ──────── */
  /* Кнопки-пилюли внутри контролов (.hero-search-btn в .hero-search-bar) не
     считаем: у поисковой строки своя геометрия (кнопка 44 внутри 52), и её
     паддинг 4 px — не «прижатый к грани» элемент. Проверяем ярлыки, метки,
     заголовки, лиды и ссылки-действия. */
  var LABEL = '.badge,.card-label,.ph-badge,.stat-label,.mn-label,.lbl,.tag,.chip,.kicker,.eyebrow,.mark,.dir-link,.card-link,.blog-card-read,h1,h2,h3,h4,.sec-sub,.sec-lead';
  var inset = [];
  var labelEls = document.querySelectorAll(LABEL);
  for (var li = 0; li < labelEls.length && li < 2500; li++) {
    var le = labelEls[li];
    if (!visible(le)) continue;
    var par = le.parentElement;
    if (!par || par === document.body) continue;
    var ps = csOf(par);
    var pb = boxOf(par), lb = boxOf(le);
    var pl = parseFloat(ps.paddingLeft) || 0, pt = parseFloat(ps.paddingTop) || 0;
    var pr = parseFloat(ps.paddingRight) || 0, pbot = parseFloat(ps.paddingBottom) || 0;
    var pbw = parseFloat(ps.borderLeftWidth) || 0, ptw = parseFloat(ps.borderTopWidth) || 0;
    var pbg = parseColor(ps.backgroundColor);
    var panel = pbw > 0 || ptw > 0 || (pbg && pbg.a > 0.02 && dist({ r: pbg.r * pbg.a + pageBg.r * (1 - pbg.a), g: pbg.g * pbg.a + pageBg.g * (1 - pbg.a), b: pbg.b * pbg.a + pageBg.b * (1 - pbg.a) }, pageBg) > 24);
    if (!panel) continue;
    /* «грань блока» — только у внешней панели: внутренние колонки
       (.stat-item шириной в половину ряда) гранью не считаются */
    if (pb.w < 0.6 * CW) continue;
    /* Меру снимаем по ЧЕРНИЛАМ текста, а не по боксу: у центрированного
       заголовка бокс начинается от грани, а строка стоит по центру. */
    var inkBox = null;
    var iw = document.createTreeWalker(le, NodeFilter.SHOW_TEXT, null), itn;
    while ((itn = iw.nextNode())) {
      if (!itn.nodeValue || !/\S/.test(itn.nodeValue)) continue;
      var irg = document.createRange();
      irg.selectNodeContents(itn);
      var irc = irg.getClientRects();
      for (var ii = 0; ii < irc.length; ii++) {
        var rr = irc[ii];
        if (rr.width < 1 || rr.height < 1) continue;
        if (!inkBox) inkBox = { l: rr.left, t: rr.top };
        else { inkBox.l = Math.min(inkBox.l, rr.left); inkBox.t = Math.min(inkBox.t, rr.top); }
      }
    }
    var il = inkBox ? inkBox.l : lb.l, it = inkBox ? inkBox.t : lb.t;
    var insetL = r1(il - (pb.l + pbw)), insetT = r1(it - (pb.t + ptw));
    /* дефект только на той оси, где панель сама не держит инсет (паддинг < 12) */
    var badL = insetL < 20 && pl < 12;
    var badT = insetT < 12 && pt < 12;
    if (badL || badT) {
      inset.push({ el: selOf(le), panel: selOf(par), insetL: insetL, insetT: insetT, pad: ps.padding });
    }
  }

  /* ── OVERF: вылет за вьюпорт и обрезанный/переполненный текст ─────────── */
  var overf = [];
  for (var oi = 0; oi < allEls.length && oi < 6000; oi++) {
    var oe = allEls[oi], ost = csOf(oe);
    if (ost.display === 'none' || ost.visibility === 'hidden') continue;
    var fixedLike = false;
    for (var p2 = oe; p2 && p2 !== document.body; p2 = p2.parentElement) {
      var s2 = csOf(p2);
      if (s2.position === 'fixed') { fixedLike = true; break; }
      if (s2.display === 'none' || s2.visibility === 'hidden') { fixedLike = true; break; }
    }
    if (fixedLike) continue;
    if (oe.classList.contains('skip-link')) continue;
    var ob = oe.getBoundingClientRect();
    if (ob.width < 1 || ob.height < 1) continue;
    if (ob.right > CW + 1.5 || ob.left < -1.5) {
      overf.push({
        cls: 'viewport', el: selOf(oe), par: oe.parentElement ? selOf(oe.parentElement) : '', l: r1(ob.left), r: r1(ob.right), w: r1(ob.width), cw: CW,
        txt: (oe.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 34), src: oe.getAttribute ? String(oe.getAttribute('src') || '') : ''
      });
      continue;
    }
    /* Замещённые элементы (img и пр.) с overflow hidden обрезает сам
       object-fit: cover — это замысел, а не обрезка текста. */
    var replaced = /^(IMG|SVG|VIDEO|CANVAS|IFRAME|INPUT|TEXTAREA|SELECT)$/.test(oe.tagName);
    if (replaced) continue;
    var ox = ost.overflowX;
    if ((ox === 'hidden' || ox === 'clip') && oe.clientWidth > 8 && oe.scrollWidth > oe.clientWidth + 1) {
      var direct = '';
      for (var cn2 = 0; cn2 < oe.childNodes.length; cn2++) if (oe.childNodes[cn2].nodeType === 3) direct += oe.childNodes[cn2].nodeValue;
      overf.push({
        cls: 'clipped', el: selOf(oe), par: oe.parentElement ? selOf(oe.parentElement) : '',
        txt: direct.replace(/\s+/g, ' ').trim().slice(0, 40) || (oe.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 40),
        cw: oe.clientWidth, sw: oe.scrollWidth
      });
      continue;
    }
    /* текст шире своего родителя-контейнера (не обрезан, а выпирает) */
    if (oe.scrollWidth > oe.clientWidth + 2 && oe.clientWidth > 40 && ost.overflowX === 'visible') {
      var hasDirect = false;
      for (var cn3 = 0; cn3 < oe.childNodes.length; cn3++) if (oe.childNodes[cn3].nodeType === 3 && /\S/.test(oe.childNodes[cn3].nodeValue || '')) hasDirect = true;
      if (hasDirect) overf.push({
        cls: 'wider', el: selOf(oe), par: oe.parentElement ? selOf(oe.parentElement) : '',
        txt: (oe.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 40), cw: oe.clientWidth, sw: oe.scrollWidth
      });
    }
  }

  /* ── ТЕКСТ ЗА ВЬЮПОРТОМ / ЗА КОНТЕЙНЕРОМ (по чернилам строки) ──────────
     Бокс элемента может быть в норме, а строка внутри — вылезать: так в
     полосе цифр enurez подпись «AZTƏMİNATLI …» обрезалась правой гранью
     экрана (бокс колонки 160 px, строка шире). */
  for (var toi = 0; toi < textRects.length && overf.length < 20; toi++) {
    var tro = textRects[toi];
    if (tro.r - tro.l < 6 || tro.b - tro.t < 3) continue;
    var ttxt = (tro.el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 34);
    if (tro.r > CW + 1.5 || tro.l < -1.5) {
      overf.push({ cls: 'text-viewport', el: selOf(tro.el), l: tro.l, r: tro.r, cw: CW, txt: ttxt });
      continue;
    }
    var cont = null;
    for (var cp = tro.el.parentElement; cp && cp !== document.body; cp = cp.parentElement) {
      var cps2 = csOf(cp);
      var cbg2 = parseColor(cps2.backgroundColor);
      var bounded = (parseFloat(cps2.borderLeftWidth) > 0 || parseFloat(cps2.borderRightWidth) > 0) ||
        (cbg2 && cbg2.a > 0.02 && dist({ r: cbg2.r * cbg2.a + pageBg.r * (1 - cbg2.a), g: cbg2.g * cbg2.a + pageBg.g * (1 - cbg2.a), b: cbg2.b * cbg2.a + pageBg.b * (1 - cbg2.a) }, pageBg) > 24);
      if (bounded) { cont = cp; break; }
    }
    if (!cont) continue;
    var ccs2 = csOf(cont), cr2 = cont.getBoundingClientRect();
    if (cr2.width < 40) continue;
    var cpl = parseFloat(ccs2.paddingLeft) || 0, cpr = parseFloat(ccs2.paddingRight) || 0;
    if (tro.r > cr2.right - cpr + 8 || tro.l < cr2.left + cpl - 8) {
      overf.push({
        cls: 'text-out', el: selOf(tro.el), cont: selOf(cont), txt: ttxt,
        l: tro.l, r: tro.r, boxL: r1(cr2.left), boxR: r1(cr2.right),
        over: r1(Math.max(0, tro.r - (cr2.right - cpr)))
      });
    }
  }

  /* ── PHOTO: кромка предметного фото не погашена — снимок лежит
     прямоугольником на подложке. Мерим альфу кромки (внешние 2 px) и глубину
     гашения (альфа на 6–10 % внутрь кадра). Эталон «гашеных» кадров сайта
     (images/hero/haqqimda-az.png, aile-terapiyasi-az.png, xidmetler-az.png):
     кромка 0.23, гашение до 0.93 за 4 % кадра. Кадры с кромкой 0.73 —
     прямоугольник с видимой гранью.
     Проверяем только предметные слоты: фото героя (.photo-col) и портреты
     (team/bio). Обложки статей и карточек — прямоугольники по замыслу. ───── */
  var photo = [];
  var imgs = document.querySelectorAll('img');
  for (var pi = 0; pi < imgs.length && pi < 200; pi++) {
    var im = imgs[pi];
    if (!visible(im)) continue;
    var ib = boxOf(im);
    if (ib.w < 80 || ib.h < 80) continue;
    if (!im.naturalWidth || !im.naturalHeight) continue;
    var slot = im.closest('.photo-col,.ph-photo,.hero-photo,.en-hero-photo,.pg-photo,.team-photo,.bio-photo');
    if (!slot) continue;
    var is = csOf(im);
    var mask = is.maskImage || is.webkitMaskImage;
    if (mask && mask !== 'none') { photo.push({ el: selOf(im), src: String(im.currentSrc || im.src).split('/').pop(), masked: true }); continue; }
    var S = 64;
    var cnv = document.createElement('canvas');
    cnv.width = S; cnv.height = S;
    var cx = cnv.getContext('2d');
    var res = null;
    try {
      cx.drawImage(im, 0, 0, S, S);
      var dd = cx.getImageData(0, 0, S, S).data;
      function alphaAt(x, y) { return dd[(y * S + x) * 4 + 3] / 255; }
      var ringA = [], deepA = [], edgeRoom = Math.round(S * 0.02), deepRoom = Math.round(S * 0.06);
      for (var y = 0; y < S; y++) for (var x = 0; x < S; x++) {
        var onEdge = (x < edgeRoom + 1 || x >= S - edgeRoom - 1 || y < edgeRoom + 1 || y >= S - edgeRoom - 1);
        if (onEdge) ringA.push(alphaAt(x, y));
        else {
          var inner = (x < deepRoom + 1 || x >= S - deepRoom - 1 || y < deepRoom + 1 || y >= S - deepRoom - 1);
          if (inner) deepA.push(alphaAt(x, y));
        }
      }
      function mean(a) { var s = 0; for (var k2 = 0; k2 < a.length; k2++) s += a[k2]; return s / a.length; }
      var mRing = mean(ringA), mDeep = mean(deepA);
      res = {
        el: selOf(im), slot: selOf(slot), src: String(im.currentSrc || im.src).split('/').pop().slice(0, 48),
        ringA: r1(mRing * 1000) / 1000, deepA: r1(mDeep * 1000) / 1000
      };
    } catch (e) { res = { el: selOf(im), src: '', err: String(e).slice(0, 60) }; }
    if (res && !res.err) {
      res.defect = res.ringA > 0.45 && res.deepA > 0.8;
      photo.push(res);
    }
  }

  /* ── ALIGN: разъезд выравнивания заголовочного стека; наезд на ярлык ───── */
  var align = [];
  /* (1) РАЗЪЕЗД ЗАГОЛОВОЧНОГО СТЕКА: у блока с центрированным .sec-h2 лид или
     подзаголовок того же стека идёт по левому краю (§29 стандарта). Тело
     блока (обычные абзацы, таблицы) в проверку не входит — оно левое
     по замыслу. */
  /* ВАЖНО: `:scope >` надо навесить на КАЖДЫЙ селектор списка — иначе
     `:scope > .a, .b, .c` разбирается как «прямый ребёнок .a» ИЛИ «.b где
     угодно» и в проверку попадают чужие элементы (так в первый прогон
     «прижатыми» оказались все .pt-sub таблицы цен, лежащие в .pt-row). */
  var LEADS = ['.sec-sub', '.sec-lead', '.pt-sub', '.bc-lead', '.ssr-sub', '.mod-lead', '.prog-lead', '.z-lead',
    '[class$="-lead"]', '[class*="-lead "]', '[class$="-sub"]', '[class*="-sub "]'];
  var scope1 = LEADS.map(function (s) { return ':scope > ' + s; }).join(',');
  var scope2 = LEADS.map(function (s) { return ':scope > .sec-header > ' + s; }).join(',');
  var stacks = document.querySelectorAll('.sec-inner:has(.sec-h2),.ps-inner:has(.sec-h2),.sec-header:has(.sec-h2)');
  for (var si = 0; si < stacks.length && si < 300; si++) {
    var ske = stacks[si];
    var kids = ske.querySelectorAll(scope1 + ',' + scope2);
    for (var kj = 0; kj < kids.length && kj < 40; kj++) {
      var kk = kids[kj];
      if (!visible(kk)) continue;
      var ks = csOf(kk);
      if (ks.textAlign === 'center') continue;
      if (kk.querySelector('.sec-h2,h2,.sec-sub,.sec-lead')) continue;
      if (!/\S/.test(kk.textContent || '')) continue;
      align.push({ cls: 'mix', el: selOf(kk), where: selOf(ske), ta: ks.textAlign, txt: (kk.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 40) });
    }
  }
  /* (2) НАЕЗД: строка текста пересекает другую строку текста (настоящая
     коллизия вёрстки, а не бокс ссылки-обёртки). Сравниваем ректы соседей
     по вертикали. */
  var byTop = textRects.slice(0).sort(function (a, b) { return a.t - b.t; });
  var hits = [];
  for (var a1 = 0; a1 < byTop.length && hits.length < 20; a1++) {
    var ra = byTop[a1];
    if (ra.r - ra.l < 6 || ra.b - ra.t < 3) continue;
    /* пропускаем текст, который сам лежит в фиксированной/абсолютной
       панели — его наложения разбирает проверка STICK */
    var pa = csOf(ra.el);
    if (pa.position === 'absolute' || pa.position === 'fixed') continue;
    for (var b1 = a1 + 1; b1 < byTop.length && b1 < a1 + 60; b1++) {
      var rb = byTop[b1];
      if (rb.t >= ra.b) break;
      if (rb.r - rb.l < 6 || rb.b - rb.t < 3) continue;
      if (ra.el === rb.el) continue;
      if (ra.el.contains(rb.el) || rb.el.contains(ra.el)) continue;
      var ox4 = Math.min(ra.r, rb.r) - Math.max(ra.l, rb.l);
      var oy4 = Math.min(ra.b, rb.b) - Math.max(ra.t, rb.t);
      if (ox4 > 8 && oy4 > 5 && ox4 * oy4 > 60) {
        var ce = ra.el, cbx = csOf(ce);
        var posA = cbx.position, trA = cbx.transform;
        hits.push({
          cls: 'overlap', a: selOf(ra.el), b: selOf(rb.el),
          txtA: (ra.el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 26),
          txtB: (rb.el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 26),
          ox: r1(ox4), oy: r1(oy4), pos: posA, tf: trA === 'none' ? '' : trA
        });
        break;
      }
    }
  }
  align = align.concat(hits);

  /* ── SIZE: кнопки, заголовки, интерлиньяж, доля фото ─────────────────── */
  var size = [];
  var bsel = '.btn,.btn-fill,.btn-line,.btn-dark,.filter-btn,.card-link,.blog-card-read,.dir-link,.mn-toggle,button[type=submit],.hero-search-btn,.ph-search-btn,.social-btn,.book-read-btn';
  var bels = document.querySelectorAll(bsel);
  for (var bi = 0; bi < bels.length && bi < 400; bi++) {
    var be2 = bels[bi];
    if (!visible(be2)) continue;
    var bb2 = boxOf(be2);
    if (bb2.w < 1) continue;
    if (bb2.h < 43.5) size.push({ cls: 'lowbtn', el: selOf(be2), w: bb2.w, h: bb2.h, txt: (be2.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 26) });
  }
  var hs = document.querySelectorAll('h1,h2,h3');
  for (var hi2 = 0; hi2 < hs.length && hi2 < 300; hi2++) {
    var he = hs[hi2];
    if (!visible(he)) continue;
    var hfs = parseFloat(csOf(he).fontSize);
    var lvl = he.tagName;
    var lim = lvl === 'H1' ? 35 : (lvl === 'H2' ? 31 : 27);
    if (hfs > lim) size.push({ cls: 'bigh', el: selOf(he), fs: hfs, lim: lim, txt: (he.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 34) });
  }
  /* интерлиньяж: порог зависит от роли. Лиды/подзаголовки — 1.75 (§6a),
     тело статьи — 1.85 (DESIGN-STANDARDS §2 «18 px / 1.85»). Дефект — когда
     роль перебрала свой порог. */
  var lhEls = document.querySelectorAll('p,li,.sec-sub,.sec-lead,blockquote,.lead,.post-byline');
  for (var lhi = 0; lhi < lhEls.length && lhi < 900; lhi++) {
    var lhe = lhEls[lhi];
    if (!visible(lhe)) continue;
    var lcs = csOf(lhe);
    var lfs = parseFloat(lcs.fontSize), llh = parseFloat(lcs.lineHeight);
    if (!(lfs >= 12) || !(llh > 0)) continue;
    var lrole = lhe.matches('.sec-sub,.sec-lead,.hero-lead,.ph-sub,.pt-sub,.bc-lead,.lead,[class*="-lead"],[class*="lead-"],[class*="-sub"],[class*="sub-"]') ? 'lead' : 'body';
    var llim = lrole === 'lead' ? 1.78 : 1.92;
    var ratio = llh / lfs;
    if (ratio <= llim) continue;
    /* число строк: считаем ректы текстовых узлов этого элемента */
    var lines = 0, tw = document.createTreeWalker(lhe, NodeFilter.SHOW_TEXT, null), tn2;
    var tops = [];
    while ((tn2 = tw.nextNode())) {
      if (!tn2.nodeValue || !/\S/.test(tn2.nodeValue)) continue;
      var rge = document.createRange(); rge.selectNodeContents(tn2);
      var rcs = rge.getClientRects();
      for (var ri2 = 0; ri2 < rcs.length; ri2++) { if (rcs[ri2].height > 2) tops.push(Math.round(rcs[ri2].top)); }
    }
    tops = tops.filter(function (v, i2, a2) { return a2.indexOf(v) === i2; });
    lines = tops.length;
    if (lines >= 2) size.push({ cls: 'lineh', role: lrole, lim: llim, el: selOf(lhe), fs: r1(lfs), lh: r1(llh), ratio: r1(ratio * 100) / 100, lines: lines, txt: (lhe.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 34) });
  }
  /* фото уже 45 % колонки — только «стоячие» кадры (слот фото героя или
     блок, где картинка — сам сюжет). Миниатюры в карточках списка
     маленькие по замыслу и в проверку не входят. */
  for (var ii2 = 0; ii2 < imgs.length && ii2 < 200; ii2++) {
    var im2 = imgs[ii2];
    if (!visible(im2)) continue;
    var ib2 = boxOf(im2);
    if (ib2.w < 80 || ib2.h < 60) continue;
    if (!im2.naturalWidth || im2.naturalWidth < 400) continue;
    var par2 = im2.parentElement;
    var pw2 = par2 ? par2.getBoundingClientRect().width : CW;
    var inSlot = !!im2.closest('.photo-col,.ph-photo,.hero-photo,.en-hero-photo,.pg-photo,.team-photo,.bio-photo');
    if (!inSlot && pw2 < 0.8 * CW) continue;
    var share = ib2.w / Math.max(Math.min(pw2, CW), 1);
    if (share < 0.45) size.push({ cls: 'smallimg', el: selOf(im2), w: ib2.w, parW: r1(pw2), share: r1(share * 100) / 100, src: String(im2.currentSrc || im2.src).split('/').pop().slice(0, 40) });
  }

  /* ── STICK: полоса цифр на герое; fixed/sticky поверх чужого текста ───── */
  var stick = [];
  var hero = document.querySelector('.page-hero,.page-hero-x,.pg-hero,.en-hero');
  var strips = document.querySelectorAll('.stats-strip,.en-stats,.stats-row,.en-stats-row,section.stats-strip');
  if (hero) {
    var hb2 = boxOf(hero);
    for (var sti = 0; sti < strips.length; sti++) {
      var se2 = strips[sti];
      if (!visible(se2)) continue;
      var sb2 = boxOf(se2);
      if (sb2.t < hb2.b - 1) stick.push({ cls: 'strip-over-hero', el: selOf(se2), stripTop: sb2.t, heroBottom: hb2.b, overlap: r1(hb2.b - sb2.t) });
    }
  }
  var fixedEls = document.querySelectorAll('body *');
  var seenFixed = 0;
  for (var fi = 0; fi < fixedEls.length && fi < 6000; fi++) {
    var fe2 = fixedEls[fi], fs2 = csOf(fe2);
    if (fs2.position !== 'fixed' && fs2.position !== 'sticky') continue;
    if (!visible(fe2)) continue;
    if (fe2.closest('.wa-float') || fe2.classList.contains('wa-float') || fe2.classList.contains('skip-link')) continue;
    if (fe2.closest('.mobile-nav,.mn-panel,.mn-drawer')) continue;
    var fb2 = boxOf(fe2);
    if (fb2.w < 40 || fb2.h < 20) continue;
    seenFixed++;
    if (seenFixed > 6) break;
    var hits = 0, sample = '';
    for (var ti2 = 0; ti2 < textRects.length; ti2++) {
      var tx = textRects[ti2];
      if (fe2.contains(tx.el)) continue;
      if (fe2.tagName === 'HEADER' && tx.t < fb2.b) { /* шапка: перекрытие с контентом героя проверяем отдельно */ }
      var ox3 = Math.min(tx.r, fb2.r) - Math.max(tx.l, fb2.l);
      var oy3 = Math.min(tx.b, fb2.b) - Math.max(tx.t, fb2.t);
      if (ox3 > 8 && oy3 > 6 && ox3 * oy3 > 120) { hits++; if (!sample) sample = selOf(tx.el) + ':' + (tx.el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 24); }
    }
    if (hits > 0) stick.push({ cls: fe2.tagName === 'HEADER' ? 'header-over-text' : 'fixed-over-text', el: selOf(fe2), pos: fs2.position, top: fb2.t, bottom: fb2.b, hits: hits, sample: sample });
  }

  /* КАРТА БЛОКОВ: секция → её прямые дети (для разбора причин в отчёте) */
  var map = [];
  var mapSecs = document.querySelectorAll('section, footer, header, main > div, .stats-strip, .cta-band, .gallery-band, .books-band');
  for (var msi = 0; msi < mapSecs.length && map.length < 40; msi++) {
    var mse = mapSecs[msi];
    if (!visible(mse)) continue;
    var msb = boxOf(mse), mss = csOf(mse);
    var mrow = { s: selOf(mse), t: msb.t, b: msb.b, h: msb.h, pt: mss.paddingTop, pb: mss.paddingBottom, mt: mss.marginTop, mb: mss.marginBottom, kids: [] };
    for (var mki = 0; mki < mse.children.length && mki < 10; mki++) {
      var mke = mse.children[mki];
      if (!visible(mke)) continue;
      var mkb = boxOf(mke), mks = csOf(mke);
      mrow.kids.push({ s: selOf(mke), t: mkb.t, b: mkb.b, h: mkb.h, mt: mks.marginTop, mb: mks.marginBottom, pt: mks.paddingTop, pb: mks.paddingBottom });
    }
    map.push(mrow);
  }

  var out = {
    url: location.pathname, w: window.innerWidth, cw: CW,
    docW: document.documentElement.scrollWidth,
    hScroll: document.documentElement.scrollWidth > CW + 1,
    docH: docH,
    counts: { textRects: textRects.length, gaps: bigGaps.length, inset: inset.length, overf: overf.length, photo: photo.length, align: align.length, size: size.length, stick: stick.length },
    gap: bigGaps.slice(0, 12),
    inset: inset.slice(0, 12),
    overf: overf.slice(0, 12),
    photo: photo.filter(function (p) { return p.defect || p.masked; }).slice(0, 10),
    photosAll: photo.slice(0, 12),
    align: align.slice(0, 14),
    size: size.slice(0, 20),
    stick: stick.slice(0, 10),
    map: map,
    st: document.readyState,
    fonts: (document.fonts && document.fonts.status) || 'n/a'
  };
  return out;
}

/* Драйвер: ждёт загрузки страницы, шрифтов и картинок, гоняет пробник до
   стабилизации высоты документа и только потом отдаёт результат в <pre>. */
const DRIVER = '(function(){' +
  'var fn=' + probeFn.toString() + ';' +
  'function emit(o){var doc=document;try{if(window.top&&window.top!==window.self)doc=window.top.document;}catch(e){}' +
  'var pre=doc.getElementById("__mdef_out");if(!pre){pre=doc.createElement("pre");pre.id="__mdef_out";' +
  'pre.style.display="none";(doc.body||doc.documentElement).appendChild(pre);}' +
  'try{pre.textContent+=btoa(unescape(encodeURIComponent(JSON.stringify(o))))+"\\n";}catch(e){}}' +
  'function imgsReady(){var im=document.images;for(var i=0;i<im.length;i++){if(!im[i].complete)return false;}' +
  'var hp=document.querySelector(".photo-col img,.en-hero-photo img,.ph-photo img");if(hp&&!hp.naturalWidth)return false;return true;}' +
  'try{var li=document.querySelectorAll("img[loading=lazy]");for(var lk=0;lk<li.length;lk++)li[lk].loading="eager";}catch(e){}' +
  'var last=null,tries=0,done=false;' +
  'function tick(){if(done)return;tries++;var o;try{o=fn();}catch(e){emit({err:String(e).slice(0,140)});return;}' +
  'var stable=last&&Math.abs((last.docH||0)-(o.docH||0))<0.6&&last.cw===o.cw;' +
  'if((o.st==="complete"&&imgsReady()&&stable&&o.fonts!=="loading")||tries>40){done=true;emit(o);return;}' +
  'last=o;setTimeout(tick,300);}' +
  'if(document.readyState==="complete")tick();else window.addEventListener("load",tick);' +
  'setTimeout(function(){if(!done)tick();},1600);' +
  'window.addEventListener("load",function(){if(document.fonts&&document.fonts.ready)document.fonts.ready.then(function(){setTimeout(function(){if(!done)tick();},600);});});' +
  '})();';
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
  const tmp = path.join(path.dirname(src), '_mdef.' + process.pid + '.' + (++dirSeq) + '.' + path.basename(src));
  let html = fs.readFileSync(src, 'utf8');
  const lang = /(^|[\/])ru[\/]/.test(rel) ? 'ru' : (/(^|[\/])en[\/]/.test(rel) ? 'en' : 'az');
  html = html.replace(/<head([^>]*)>/i, '<head$1><script>' + PRESCRIPT.replace('___LANG___', '"' + lang + '"') + '</script>');
  html = rewriteFonts(html, !process.env.HERO_NO_FONTCACHE);
  html = html.replace(/<\/body>/i, '<script>' + DRIVER + '</script></body>');
  if (html.indexOf('__mdef_out') === -1) html += '<script>' + DRIVER + '</script>';
  fs.writeFileSync(tmp, html, 'utf8');
  return tmp;
}

function measureOnce(rel, width, profileDir) {
  return new Promise((resolve) => {
    const tmp = withProbe(rel);
    const relTmp = path.relative(ROOT, tmp).replace(/\\/g, '/');
    let url, wrapper = null, winW = width;
    if (width < 500) {
      const wtmp = path.join(ROOT, '_mdef.w.' + process.pid + '.' + (++dirSeq) + '.html');
      fs.writeFileSync(wtmp, '<!DOCTYPE html><html><head><meta charset="utf-8"><title>narrow</title>' +
        '<style>html,body{margin:0;padding:0;background:#07090E}#f{width:' + width + 'px;height:1000px;border:0;display:block}</style>' +
        '</head><body><iframe id="f" src="' + encodeURI(relTmp) + '"></iframe></body></html>', 'utf8');
      wrapper = wtmp;
      url = 'http://127.0.0.1:' + PORT + '/' + encodeURI(path.relative(ROOT, wtmp).replace(/\\/g, '/'));
      winW = 520;
    } else {
      url = 'http://127.0.0.1:' + PORT + '/' + encodeURI(relTmp);
    }
    const userDir = profileDir || (TMPBASE + '/mdef-prof-' + process.pid + '-' + dirSeq);
    execFile(CHROME, [
      '--headless=new', '--disable-gpu', '--no-sandbox', '--disable-extensions',
      '--lang=az', '--accept-lang=az',
      '--user-data-dir=' + userDir,
      '--host-resolver-rules=MAP ipapi.co 127.0.0.1:9',
      '--virtual-time-budget=15000',
      '--window-size=' + winW + ',1600',
      '--dump-dom', url
    ], { encoding: 'utf8', maxBuffer: 1 << 28, timeout: 240000, killSignal: 'SIGKILL' }, (err, stdout) => {
      if (!process.env.MDEF_KEEP) { try { fs.unlinkSync(tmp); } catch (e) {} }
      if (wrapper) { try { fs.unlinkSync(wrapper); } catch (e) {} }
      if (err) { resolve({ error: String(err.message || err).slice(0, 160) }); return; }
      const block = stdout.match(/<pre id="__mdef_out"[^>]*>([\s\S]*?)<\/pre>/);
      if (!block) { resolve({ error: 'no __mdef_out in dump' }); return; }
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
      const profile = TMPBASE + '/mdef-prof-' + PORT + '-' + size + '-' + slot;
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
    const ok = r.snaps.filter(d => d.st === 'complete' && (d.fonts === 'loaded' || d.fonts === 'n/a') && !d.err);
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
