#!/usr/bin/env node
/* standard-audit.js — сплошной обмер страниц сайта на соответствие
 * DESIGN-STANDARDS.md (шкала 88/48/32, лиды 1.75, ярлыки 32/24, таблицы,
 * центрированный стек, герой V=48/36, H2 на 390).
 *
 * Запуск (сервер: python -m http.server 8765 --bind 127.0.0.1 -d .):
 *   node _tools/standard-audit.js --width 1440,390 --jobs 4 --out D:/ragimoff-tmp/sa aile-terapiyasi.html samira.html
 *   node _tools/standard-audit.js --width 1440,390 --jobs 4 --out DIR --all
 *
 * Пишет в --out (каталог только латиницей):
 *   standard_<w>.tsv   — отклонения: page width class item before target note
 *   standard_<w>.json  — сырые замеры по странице
 */
'use strict';
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { execFile } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const CHROME = process.env.AUDIT_CHROME || 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const PORT = process.env.AUDIT_PORT || '8765';

const argv = process.argv.slice(2);
function arg(name, def) {
  const i = argv.indexOf('--' + name);
  return i === -1 ? def : argv[i + 1];
}
const WIDTHS = String(arg('width', '1440')).split(',').map(Number);
const JOBS = parseInt(arg('jobs', '3'), 10);
const OUT = arg('out', 'D:/ragimoff-tmp/sa');
const ALL = argv.includes('--all');
const PAGES = [];
const WITHARG = ['width', 'jobs', 'out', 'pages'];
for (let i = 0; i < argv.length; i++) {
  if (argv[i] === '--pages') { for (let j = i + 1; j < argv.length && argv[j][0] !== '-'; j++) { PAGES.push(argv[j]); i = j; } }
  else if (argv[i][0] === '-' && WITHARG.indexOf(argv[i].slice(2)) >= 0) { i++; }
  else if (argv[i][0] !== '-') PAGES.push(argv[i]);
}
if (ALL) {
  const skip = /^(temp_index|test-wave-elements|template)\.html$/;
  for (const d of ['', 'ru/', 'en/']) {
    const dir = path.join(ROOT, d);
    for (const f of fs.readdirSync(dir)) {
      if (!f.endsWith('.html') || skip.test(f)) continue;
      PAGES.push(d + f);
    }
  }
}
if (!PAGES.length) { console.error('no pages'); process.exit(1); }
fs.mkdirSync(OUT, { recursive: true });

/* ── ПРОБНИК ─────────────────────────────────────────────────────────── */
const PROBE = `(function () {
  'use strict';
  function r1(v) { return Math.round(v * 10) / 10; }
  function bx(el) { var r = el.getBoundingClientRect();
    return { t: r1(r.top + window.scrollY), b: r1(r.bottom + window.scrollY), l: r1(r.left), r: r1(r.right), w: r1(r.width), h: r1(r.height) }; }
  function vis(e) {
    if (!e || e.nodeType !== 1) return false;
    var c = getComputedStyle(e);
    if (c.display === 'none' || c.visibility === 'hidden' || c.display === 'contents') return false;
    if (c.position === 'absolute' || c.position === 'fixed') return false;
    var r = e.getBoundingClientRect();
    return r.height > 0.5 && r.width > 0.5;
  }
  function tag(el) {
    var s = el.tagName.toLowerCase();
    if (el.id) s += '#' + el.id;
    if (el.className && typeof el.className === 'string') s += '.' + el.className.trim().split(/\\s+/).slice(0, 2).join('.');
    return s;
  }
  /* строки элемента по Range-ректам (та же методика, что в фиттере) */
  function lineRows(el) {
    var rr = document.createRange(), groups = [], i, rc, g, j;
    rr.selectNodeContents(el);
    var rs = rr.getClientRects();
    for (i = 0; i < rs.length; i++) {
      rc = rs[i];
      if (rc.height < 2 || rc.width < 1) continue;
      g = null;
      for (j = 0; j < groups.length; j++) {
        if (Math.abs(groups[j].top - rc.top) < Math.max(groups[j].height, rc.height) * 0.5) { g = groups[j]; break; }
      }
      if (!g) { g = { top: rc.top, l: rc.left, r: rc.right, height: rc.height }; groups.push(g); }
      g.height = Math.max(g.height, rc.height);
      g.l = Math.min(g.l, rc.left);
      g.r = Math.max(g.r, rc.right);
    }
    return groups;
  }
  function stepOf(el) {
    /* Строку ведёт сам лид: если у подзаголовка есть видимые спаны-строки
       (*-lead-mob/-desk), мерим их; иначе — сам элемент. Иначе в замер
       попадает высокая рамка блока (Range отдаёт её отдельным ректом) и
       шаг считается по её верху: было 32.6 вместо 30.6. */
    var owners = [];
    [].forEach.call(el.children, function (k) {
      var c = getComputedStyle(k);
      if (c.display !== 'none' && c.visibility !== 'hidden') owners.push(k);
    });
    var rows = [];
    if (owners.length) {
      owners.forEach(function (k) { rows = rows.concat(lineRows(k)); });
    } else rows = lineRows(el);
    rows.sort(function (a, b) { return a.top - b.top; });
    var steps = [];
    for (var i = 1; i < rows.length; i++) if (rows[i].top > rows[i - 1].top + 1) steps.push(rows[i].top - rows[i - 1].top);
    var fs = owners.length ? parseFloat(getComputedStyle(owners[0]).fontSize) : parseFloat(getComputedStyle(el).fontSize);
    return { n: rows.length, step: steps.length ? r1(Math.max.apply(null, steps)) : null, fs: r1(fs),
             ink: rows.length ? r1(Math.max.apply(null, rows.map(function (x) { return x.r - x.l; }))) : 0 };
  }
  var SUB_SEL = '.sec-sub, .sec-lead, .eco-sub, .section-sub, .hero-lead, .ph-sub, .bc-lead, .pt-sub,' +
    '[class$="-lead-mob"], [class*="-lead-mob "], [class$="-lead-desk"], [class*="-lead-desk "]';
  var SUB_CARD = '.card, .svc-card, .blog-card, .book-card, .mod-panel, .kitab-box, .price-card, .pricing-card, .team-card, .prog-card, .feat-card, .xid-card, .step-card';
  var DEAD = '.site-header, .mobile-nav, footer, .wa-float, .kitab-modal, #kitab-modal';
  var INLINE = /^(SPAN|A|EM|STRONG|B|I|SMALL|SUP|SUB|BR|LABEL|MARK|TIME|SVG|PATH|CODE|WBR)$/;
  var CONTENT = 'p, h1, h2, h3, h4, h5, h6, ul, ol, table, form, details, img, input:not([type=hidden]), select, textarea, button, .btn, .badge, .ph-badge, .stat-item, .mod-panel, .faq-item';
  var BADGE = '.badge, .ph-badge';

  function subNextFlow(el) {
    var bot = el.getBoundingClientRect().bottom, n = el;
    while (n && n !== document.body && n.parentElement) {
      var s = n.nextElementSibling;
      while (s && (!vis(s) || INLINE.test(s.tagName) || s.getBoundingClientRect().top < bot - 1)) s = s.nextElementSibling;
      if (s) return s;
      n = n.parentElement;
    }
    return null;
  }
  /* блок ярлыка: ближайший предок с видимым оформлением */
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

  function run() {
    var out = { w: window.innerWidth, cw: document.documentElement.clientWidth };
    out.scrollW = document.documentElement.scrollWidth;
    out.hScroll = out.scrollW > out.cw + 1;
    out.offenders = [];
    [].forEach.call(document.querySelectorAll('body *'), function (el) {
      if (out.offenders.length > 14) return;
      if (el.closest('.site-header, .mobile-nav, #kitab-modal, .wa-float, .hero-sd, .search-drop, .skip-link')) return;
      var c = getComputedStyle(el);
      if (c.position === 'fixed' || c.display === 'none' || c.visibility === 'hidden') return;
      var r = el.getBoundingClientRect();
      if (r.width > 0.5 && (r.right > out.cw + 1.5 || r.left < -1.5)) {
        out.offenders.push({ el: tag(el), l: r1(r.left), r: r1(r.right), w: r1(r.width) });
      }
    });

    /* ── ГЕРОЙ ── */
    var hero = document.querySelector('.page-hero-x, .page-hero, .pg-hero');
    if (hero) {
      var hb = bx(hero);
      function hq(s) { return hero.querySelector(s); }
      var badge = hq('.ph-badge, .badge'), h1 = hq('.ph-h1, .hero-h1, h1'), sub = hq('.ph-sub, .hero-lead'),
          srch = hq('.hero-search-bar, .ph-search-bar'), photo = hq('.photo-col img');
      /* фото героя спозиционировано абсолютно — меряем его независимо от vis() */
      out.hero = {
        h: hb.h, top: hb.t, bot: hb.b,
        gapBadgeTop: badge ? r1(bx(badge).t - hb.t) : null,
        gapBadgeH1: badge && h1 ? r1(bx(h1).t - bx(badge).b) : null,
        gapH1Sub: h1 && sub ? r1(bx(sub).t - bx(h1).b) : null,
        gapH1Photo: h1 && photo ? r1(bx(photo).t - bx(h1).b) : null,
        gapPhotoSub: photo && sub ? r1(bx(sub).t - bx(photo).b) : null,
        gapSubSearch: sub && srch ? r1(bx(srch).t - bx(sub).b) : null,
        gapSearchBot: srch ? r1(hb.b - bx(srch).b) : null,
        photoTop: photo ? r1(bx(photo).t - hb.t) : null,
        photoBot: photo ? r1(hb.b - bx(photo).b) : null,
        subStep: sub ? (function () { var st = stepOf(sub); return { n: st.n, step: st.step }; })() : null,
        h1FS: h1 ? getComputedStyle(h1).fontSize : null
      };
    }
    /* полоса цифр: без наложения */
    var strip = document.querySelector('.stats-strip, .en-stats');
    if (hero && strip) out.stripOverlap = r1(bx(hero).b - bx(strip).t);
    else out.stripOverlap = strip && !hero ? 0 : null;

    /* ── БЛОКИ ── */
    out.blocks = [];
    out.subs = [];
    out.h2s = [];
    out.cards = [];
    out.tables = [];
    out.badges = [];
    var secs = [];
    function pushSec(s) {
      if (!s || s.nodeType !== 1) return;
      if (s.closest(DEAD) || s.closest('.mobile-nav')) return;
      if (s.classList.contains('page-hero-x') || s.classList.contains('page-hero') || s.classList.contains('pg-hero')) return;
      if (!vis(s)) return;
      if (secs.indexOf(s) >= 0) return;
      secs.push(s);
    }
    /* Блок — ЛЮБОЙ верхнеуровневый бокс основного потока, а не только
       <section>: у tehsil между двумя секциями стоит <div class="legal-banner">
       (218 px), и зазор «блок → блок» считался через него как 306 px пустоты. */
    [].forEach.call(document.querySelectorAll('main > *, .page-main > *, body > section'), pushSec);
    [].forEach.call(document.querySelectorAll('section'), function (s) {
      if (s.parentElement && s.parentElement.tagName === 'BODY') pushSec(s);
      if (s.parentElement && (s.parentElement.tagName === 'MAIN' || s.parentElement.classList.contains('page-main'))) pushSec(s);
    });
    secs.forEach(function (sec) {
      var sb = bx(sec);
      var badge = sec.querySelector(BADGE);
      var isBand = sec.classList.contains('cta-band');
      /* Границы содержимого — по ВСЕМ видимым боксам: закрытый <details> сам
         имеет рект (его содержимое скрыто, но FAQ-строка на экране видна), и
         без него низ блока считался бы по подзаголовку (замер: 958 вместо 88). */
      var ctop = null, cbot = null, ctopEl = null, cbotEl = null;
      [].forEach.call(sec.querySelectorAll('*'), function (el) {
        var dd = el.closest('details');
        if (dd && !dd.open && el !== dd && !el.closest('summary')) return;
        if (el.closest(DEAD)) return;
        if (!vis(el)) return;
        var b = bx(el);
        if (ctop === null || b.t < ctop) { ctop = b.t; ctopEl = el; }
        if (cbot === null || b.b > cbot) { cbot = b.b; cbotEl = el; }
      });
      /* Если первый элемент блока лежит в вертикально центрированной обёртке
         (flex/grid align-items: center), зазор «верх блока → метка» зависит от
         высоты соседней колонки, а не от шкалы: у div.tg-band на program-*
         замер @1440 дал 114,4 при паддинге блока 85,44 — метку опустила
         центровка. Такие блоки в проверке SEC-TOP пропускаем. */
      var centered = false;
      (function () {
        var n = badge;
        while (n && n !== sec) {
          var pc = n.parentElement;
          if (!pc) break;
          var pcs = getComputedStyle(pc);
          if ((pcs.display.indexOf('flex') >= 0 || pcs.display.indexOf('grid') >= 0) && pcs.alignItems === 'center') { centered = true; break; }
          n = pc;
        }
      })();
      var bcb = badge && vis(badge) ? bx(badge) : null;
      out.blocks.push({
        sel: tag(sec),
        h: sb.h, top: sb.t, bot: sb.b,
        band: isBand,
        centered: centered,
        gapTop: bcb ? r1(bcb.t - sb.t) : (ctop !== null ? r1(ctop - sb.t) : null),
        badgeText: badge ? (badge.textContent || '').trim().slice(0, 30) : null,
        gapBot: cbot !== null ? r1(sb.b - cbot) : null,
        botEl: cbotEl ? tag(cbotEl) : null,
        padTop: getComputedStyle(sec).paddingTop,
        padBot: getComputedStyle(sec).paddingBottom
      });
      /* пустоты: полосы текста (текстовые узлы) + атомарные боксы; максимальный
         разрыв между соседними полосами. Раньше брали «листья-элементы» —
         абзац с инлайновой ссылкой считался листом, и хвост его текста после
         ссылки давал ложную пустоту 160 px. */
      var bands = [];
      /* Верхнеуровневый блок полосы: пустоту считаем ТОЛЬКО внутри одного
         такого блока. Между колонками грида (текст кончился раньше портрета
         соседней колонки) разрыв — не дефект интервалов, а следствие сетки:
         без этого правила index.sec-2col давал ложные 131 px между списком
         дипломов и полосой галереи. */
      function centeredRow(el) {
        var n = el, i = 0;
        while (n && n.nodeType === 1 && i++ < 12) {
          var pc = n.parentElement;
          if (!pc) break;
          var c2 = getComputedStyle(pc);
          if ((c2.display.indexOf('flex') >= 0 || c2.display.indexOf('grid') >= 0) && c2.alignItems === 'center') return true;
          n = pc;
        }
        return false;
      }
      function topBlockOf(el) {
        var cur = el, i = 0;
        while (cur && cur.parentElement && cur.parentElement !== sec && i++ < 30) {
          if (cur.parentElement.matches('.sec-inner, .ps-inner')) break;
          cur = cur.parentElement;
        }
        return cur || el;
      }
      (function walk(n) {
        for (var i = 0; i < n.childNodes.length; i++) {
          var ch = n.childNodes[i];
          if (ch.nodeType === 3) {
            if (!ch.nodeValue || !ch.nodeValue.trim()) continue;
            var pr = ch.parentElement;
            if (pr.closest(DEAD)) continue;
            var ddp = pr.closest('details');
            if (ddp && !ddp.open && !pr.closest('summary')) continue;
            var rr2 = document.createRange();
            rr2.selectNodeContents(ch);
            var rcs = rr2.getClientRects();
            for (var j = 0; j < rcs.length; j++) {
              if (rcs[j].height > 1 && rcs[j].width > 1) bands.push({ t: rcs[j].top + window.scrollY, b: rcs[j].bottom + window.scrollY, tb: topBlockOf(pr), l: rcs[j].left, r: rcs[j].right, cRow: centeredRow(pr) });
            }
            continue;
          }
          if (ch.nodeType !== 1) continue;
          var dc = getComputedStyle(ch);
          if (dc.display === 'none' || dc.visibility === 'hidden' || dc.position === 'absolute' || dc.position === 'fixed') continue;
          var hasBgImg = dc.backgroundImage && dc.backgroundImage !== 'none';
          if (/^(IMG|SVG|INPUT|SELECT|TEXTAREA|BUTTON|IFRAME|VIDEO|CANVAS|TABLE|HR)$/.test(ch.tagName) ||
              (dc.display.indexOf('inline') < 0 && !ch.children.length) ||
              hasBgImg) {
            var rb = ch.getBoundingClientRect();
            if (rb.height > 1 && rb.width > 1) bands.push({ t: rb.top + window.scrollY, b: rb.bottom + window.scrollY, tb: topBlockOf(ch), el: ch, l: rb.left, r: rb.right, cRow: centeredRow(ch) });
          }
          walk(ch);
        }
      })(sec);
      bands.sort(function (a, b) { return a.t - b.t; });
      /* Меряем разрыв между соседними полосами ОДНОГО верхнеуровневого блока */
      var groups = [];
      bands.forEach(function (b) {
        var g = null;
        for (var i = 0; i < groups.length; i++) { if (groups[i].key === b.tb) { g = groups[i]; break; } }
        if (!g) { g = { key: b.tb, bands: [] }; groups.push(g); }
        g.bands.push(b);
      });
      /* Разрыв НЕ считаем, если полосы лежат в одной grid/flex-сетке: пустота
         между строкой карточек и следующей строкой — свойство сетки (высоту
         держит самая высокая карточка), а не интервал между блоками. Замер
         blog-klinik-psixiatriya: 208 px между заголовком карточки и кодом
         следующей строки при сетке .bolme-card. */
      function sameGrid(a, b) {
        if (!a.el || !b.el) return false;
        var lca = null, n = a.el;
        while (n && n.nodeType === 1) {
          if (n.contains(b.el)) { lca = n; break; }
          n = n.parentElement;
        }
        if (!lca) return false;
        var d = getComputedStyle(lca).display;
        return d.indexOf('grid') >= 0 || d.indexOf('flex') >= 0;
      }
      var maxGap = 0;
      groups.forEach(function (g) {
        var curBot = null, curOwner = null;
        g.bands.forEach(function (b) {
          if (curBot === null) { curBot = b.b; curOwner = b; return; }
          var xOverlap = curOwner && b && (curOwner.r > b.l + 0.5) && (b.r > curOwner.l + 0.5);
          var centeredPair = (curOwner && curOwner.cRow) || b.cRow;
          if (b.t > curBot + 0.5 && !sameGrid(curOwner, b) && xOverlap && !centeredPair) {
            var gg = b.t - curBot;
            if (gg > maxGap) maxGap = gg;
          }
          if (b.b > curBot) { curBot = b.b; curOwner = b; }
        });
      });
      if (maxGap > 0.5) out.blocks[out.blocks.length - 1].voidMax = r1(maxGap);

      /* подзаголовки/лиды блока */
      var seen = [];
      [].forEach.call(sec.querySelectorAll(SUB_SEL), function (el) {
        if (el.closest(DEAD)) return;
        if (el.closest('details') && !el.closest('details').open) return;
        if (!vis(el)) return;
        var p = el.parentElement;
        if (p) { try { if (p.matches(SUB_SEL)) return; } catch (e) { /* */ } }
        if (seen.indexOf(el) >= 0) return; seen.push(el);
        var st = stepOf(el);
        var cs = getComputedStyle(el);
        var fs = st.fs || parseFloat(cs.fontSize);
        var nxt = subNextFlow(el);
        var inCard = el.closest(SUB_CARD);
        /* .pt-sub и родня — ПОДПИСЬ внутри строки таблицы цен, а не лид блока:
           следующий «элемент в потоке» у неё — соседняя строка в 15 px, и
           правило «после подзаголовка 48» к ней не относится (enurez ×3). */
        var inRow = !!el.closest('.pt-row, .price-row, .pricing-tbl-row, .info-row, .cur-row, .tl-item, tr, td');
        var gap = nxt ? r1(bx(nxt).t - bx(el).b) : null;
        var outsideMain = !!(nxt && nxt.closest('footer, .site-footer'));
        out.subs.push({
          block: tag(sec), cls: (typeof el.className === 'string' ? el.className.trim() : '').slice(0, 40),
          text: (el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 46),
          fs: r1(fs), lh: cs.lineHeight, lines: st.n, step: st.step, ink: st.ink,
          align: cs.textAlign, card: !!inCard, inRow: inRow, next: nxt ? tag(nxt) : null, gap: gap, outsideMain: outsideMain
        });
      });
      /* заголовки H2 */
      [].forEach.call(sec.querySelectorAll('h2.sec-h2, h2.section-title'), function (h) {
        if (!vis(h)) return;
        var st = stepOf(h);
        var cs = getComputedStyle(h);
        var inner = h.closest('.sec-inner, .ps-inner') || sec;
        var inn = getComputedStyle(inner);
        var availW = bx(inner).w - parseFloat(inn.paddingLeft) - parseFloat(inn.paddingRight);
        out.h2s.push({
          block: tag(sec), text: (h.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 40),
          fs: r1(parseFloat(cs.fontSize)), lines: st.n, ink: st.ink, boxW: bx(h).w,
          align: cs.textAlign, avail: r1(availW), overflow: st.ink > availW + 1
        });
      });
      /* таблицы */
      [].forEach.call(sec.querySelectorAll('.price-table, .pricing-tbl, .art-table, .diff-table, .price-grid-3'), function (t) {
        if (!vis(t)) return;
        var tb = bx(t);
        /* Мера — КОНТЕНТНАЯ ЧАСТЬ НЕПОСРЕДСТВЕННОГО РОДИТЕЛЯ таблицы: у статей
           .art-table живёт в колонке 720 px внутри .sec-inner 1209, и мера по
           .sec-inner давала ложные 59,5 % на blog-*-protokol (правило §3c и
           образец из DESIGN-STANDARDS считают от контейнера таблицы). */
        var cont = t.parentElement || t.closest('.sec-inner, .ps-inner');
        var cs2 = getComputedStyle(cont);
        var avail = bx(cont).w - parseFloat(cs2.paddingLeft) - parseFloat(cs2.paddingRight);
        var subEl = sec.querySelector('.sec-sub, .sec-lead');
        out.tables.push({
          block: tag(sec), cls: tag(t), w: tb.w, avail: r1(avail),
          ratio: avail ? r1(tb.w / avail * 100) : null,
          subAlign: subEl ? getComputedStyle(subEl).textAlign : null,
          h2Align: (function () { var h = sec.querySelector('.sec-h2'); return h ? getComputedStyle(h).textAlign : null; })()
        });
      });
    });

    /* ── КАРТОЧКИ: заголовок → текст ── */
    [].forEach.call(document.querySelectorAll('.card, .svc-card, .xid-card, .feat-card, .step-card, .faq-item, .process-step, .price-card, .blog-card, .book-card, .team-card, .prog-card'), function (c) {
      if (!vis(c) || c.closest(DEAD)) return;
      var head = c.querySelector('h3, h4');
      if (!head || !vis(head)) return;
      /* Головной группой считаем заголовок и его некрупные соседи внутри
         общей обёртки (.price-card-head: h4 + span-подпись) — иначе подпись
         попадала в зазор и он выходил 76 px на ровном месте. */
      var headEnd = head;
      while (headEnd.nextElementSibling &&
             !/^(P|LI|UL|OL|TABLE|DIV)$/.test(headEnd.nextElementSibling.tagName) &&
             headEnd.parentElement === head.parentElement) {
        headEnd = headEnd.nextElementSibling;
      }
      var hb2 = bx(headEnd);
      var next = null, best = null;
      [].forEach.call(c.querySelectorAll('p, li'), function (el) {
        if (el === head || head.contains(el) || el.contains(head) || headEnd.contains(el)) return;
        if (el.closest('details') && !el.closest('details').open && !el.closest('summary')) return;
        if (!vis(el)) return;
        var b = bx(el);
        if (b.t >= hb2.b - 1 && (best === null || b.t < best)) { best = b.t; next = el; }
      });
      if (next) out.cards.push({ cls: tag(c), head: tag(head), next: tag(next), gap: r1(best - hb2.b) });
    });

    /* ── СЕТКИ КАРТОЧЕК: карточка → карточка (внутри сетки) = 24/16 ──
       Стандарт DESIGN-STANDARDS §3d. Замер: разброс по сайту 16/20/24/32;
       отклонением считаем < 12 (слиплись) и > 32 (разъехались). */
    out.grids = [];
    [].forEach.call(document.querySelectorAll("[class*=grid], .process-grid, .team-grid, .prog-grid, .yt-grid, .yt-grid-3"), function (g) {
      if (g.closest(DEAD) || !vis(g)) return;
      var gc = getComputedStyle(g);
      if (!/grid|flex/.test(gc.display)) return;
      /* Считаем только СЕТКИ КАРТОЧЕК: у раскладочных сеток (.about-grid
         «текст | портрет», gap 64) свой замысел, к шкале карточек он не
         относится. */
      var CARDK = /(^|s)(card|svc-card|xid-card|feat-card|step-card|price-card|blog-card|book-card|team-card|prog-card|process-step|price-card-head|dir-card)(s|$)/;
      var kids = 0;
      for (var i = 0; i < g.children.length; i++) {
        if (vis(g.children[i]) && CARDK.test(g.children[i].className || "")) kids++;
      }
      if (kids < 2) return;
      out.grids.push({
        cls: tag(g), kids: kids,
        rowGap: parseFloat(gc.rowGap) || 0, colGap: parseFloat(gc.columnGap) || 0
      });
    });
    /* ── КНОПКИ: зазор от предыдущего видимого элемента (текст → кнопка) ──
       Стандарт: 24–32 px на десктопе, 16–24 на телефоне (DESIGN-STANDARDS,
       «абзац → кнопка»). Владелец 05.10.2026: «где-то пропуски между текстом
       и кнопкой отсутствуют, а где-то они очень большие». */
    out.btns = [];
    [].forEach.call(document.querySelectorAll("a.btn, button.btn, .btn-fill, .btn-line, .btn-dark, input[type=submit], button[type=submit]"), function (b) {
      if (b.closest(DEAD) || b.closest(".pricing-tbl, .hero-search-bar, .ph-search-wrap")) return;
      if (!vis(b)) return;
      var prev = null, n = b;
      while (n && n !== document.body && n.parentElement) {
        var p2 = n.previousElementSibling;
        while (p2 && !vis(p2)) p2 = p2.previousElementSibling;
        if (p2) { prev = p2; break; }
        n = n.parentElement;
      }
      if (!prev) return;
      /* Пара считается только «стопкой»: заголовок кнопке не текст-абзац,
         а кнопка сбоку (cta-band, .cta-pair) — не пропуск по вертикали. */
      if (/^(H1|H2|H3|H4|H5|H6)$/.test(prev.tagName)) return;
      /* Пара стандарта — АБЗАЦ → КНОПКА; кнопка→кнопка (столбик действий) идёт по своей сетке. */
      if (prev.tagName === 'BUTTON' || prev.tagName === 'A' || /(^|s)btn(-|s|$)/.test(prev.className || '')) return;
      var pb = bx(prev), bb = bx(b);
      if (bb.t < pb.b - 0.5) return;
      out.btns.push({
        block: (function () { var s2 = b.closest("section, .cta-band"); return s2 ? tag(s2) : "-"; })(),
        prev: tag(prev), btn: tag(b),
        text: (b.textContent || "").replace(/s+/g, " ").trim().slice(0, 30),
        gap: r1(bb.t - pb.b)
      });
    });
    /* ── ЯРЛЫКИ: инсеты от граней блока ── */
    [].forEach.call(document.querySelectorAll(BADGE), function (el) {
      if (el.closest('.mobile-nav') || !vis(el)) return;
      var blk = blockOf(el);
      if (!blk) return;
      var bb = bx(el), kb = bx(blk);
      var bs = getComputedStyle(blk);
      out.badges.push({
        text: (el.textContent || '').trim().slice(0, 30), block: tag(blk),
        insetL: r1(bb.l - kb.l), insetT: r1(bb.t - kb.t),
        padL: bs.paddingLeft, padT: bs.paddingTop,
        textAlign: getComputedStyle(el.parentElement).textAlign
      });
    });

    out.st = document.readyState;
    /* Признак, что site-concept.css ПРИМЕНИЛСЯ (а не только числится в списке): без него страница снималась «полугрузом» и section-ритм мерился по gtc.css (55 вместо 88). */
    out.okCss = getComputedStyle(document.documentElement).getPropertyValue("--s-block").trim() === "88px"; out.sheets = (function(){var a=[];for(var i=0;i<document.styleSheets.length;i++){try{a.push(String(document.styleSheets[i].href||'').split('/').pop());}catch(e){a.push('X');}}return a;})();
    out.fonts = (document.fonts && document.fonts.status) || 'n/a';
    emit(out);
  }
  function emit(o) {
    var doc = document;
    try { if (window.top && window.top !== window.self) doc = window.top.document; } catch (e) { /* cross-origin */ }
    var pre = doc.getElementById('__sa_out');
    if (!pre) { pre = doc.createElement('pre'); pre.id = '__sa_out'; (doc.body || doc.documentElement).appendChild(pre); }
    pre.textContent += btoa(unescape(encodeURIComponent(JSON.stringify(o)))) + '\\n';
  }
  if (document.readyState === 'complete') { run(); } else { window.addEventListener('load', run); }
  setTimeout(run, 1400);
  setTimeout(run, 3200);
  setTimeout(run, 6000);
})();
`;

/* ── запуск ─────────────────────────────────────────────────────────── */
const FC_PORT = process.env.FONTCACHE_PORT || '8766';
/* Уникальный токен прогона: постоянный ?sa=1 кэшировался между прогонами, и «после» мерилось по копии CSS из профиля. */
const BUST = 'sa=' + Date.now();
let seq = 0;
function rewriteFonts(html) {
  if (process.env.SA_NO_FONTCACHE) return html;
  const h = (u) => crypto.createHash('md5').update(u).digest('hex');
  html = html.replace(/https:\/\/fonts\.googleapis\.com\/css2\?[^"'`)\s<>]+/g,
    (u) => 'http://127.0.0.1:' + FC_PORT + '/fc/' + h(u.replace(/&amp;/g, '&')) + '.css');
  html = html.replace(/https:\/\/fonts\.gstatic\.com\/[^"'`)\s<>)]+/g,
    (u) => 'http://127.0.0.1:' + FC_PORT + '/fc/' + h(u) + '.woff2');
  return html;
}
function withProbe(rel) {
  const src = path.join(ROOT, rel);
  const dir = path.dirname(src);
  const tmp = path.join(dir, '_sa.' + process.pid + '.' + (++seq) + '.' + path.basename(src));
  let html = fs.readFileSync(src, 'utf8');
  /* Язык в localStorage ДО shared.js: иначе авто-редирект уводит на /ru/ */
  const lang = /(^|[\/\\])ru[\/\\]/.test(rel) ? 'ru' : (/(^|[\/\\])en[\/\\]/.test(rel) ? 'en' : 'az');
  html = html.replace(/<head([^>]*)>/i, '<head$1><script>try{localStorage.setItem("ragimoff_lang","' + lang + '");}catch(e){}</script>');
  html = rewriteFonts(html);
  /* Сброс кэша локальных css/js: профиль Chrome тёплый (иначе обход длится
     часы), и без этого «после» мерилось бы по старым копиям из кэша. К URL
     добавляется ?sa=1 (или &sa=1) — сервер отдаёт файл с диска как есть. */
  html = html.replace(/(href|src)="([^"]*\.(?:css|js))(\?[^"]*)?"/g,
    function (m, a, u, q) {
      if (/^(https?:)?\/\//.test(u)) return m;
      return a + '="' + u + (q ? q + '&' : '?') + BUST + '"';
    });
  html = html.replace(/<\/body>/i, '<script>' + PROBE + '</script></body>');
  if (html.indexOf('__sa_out') === -1) html += '<script>' + PROBE + '</script>';
  fs.writeFileSync(tmp, html, 'utf8');
  return tmp;
}

function measureOnce(rel, width, profileDir, attempt) {
  return new Promise(function (resolve) {
    let tmp, wrapper = null, winW = width;
    try { tmp = withProbe(rel); } catch (e) { resolve({ file: rel, width, error: 'inject: ' + e.message }); return; }
    const relTmp = path.relative(ROOT, tmp).replace(/\\/g, '/');
    let url = 'http://127.0.0.1:' + PORT + '/' + encodeURI(relTmp);
    /* Chrome на Windows не даёт окно уже 500 px: 390 меряем через обёртку с
       iframe ровно 390 (как site-shot.js/mobile-audit.js). Результат пробник
       кладёт в <pre id="__sa_out"> документа-обёртки. */
    if (width < 500) {
      wrapper = path.join(ROOT, '_sa.w.' + process.pid + '.' + (++seq) + '.html');
      fs.writeFileSync(wrapper, '<!DOCTYPE html><html><head><meta charset="utf-8"><title>narrow</title>' +
        '<style>html,body{margin:0;padding:0;background:#07090E}#f{width:' + width + 'px;height:1200px;border:0;display:block}</style>' +
        '</head><body><iframe id="f" src="' + encodeURI(relTmp) + '"></iframe></body></html>', 'utf8');
      url = 'http://127.0.0.1:' + PORT + '/' + encodeURI(path.relative(ROOT, wrapper).replace(/\\/g, '/'));
      winW = 520;
    }
    /* Профиль — СВОЙ на воркер и ОДИН на всю его очередь: свежий профиль на
       каждую страницу стоил минуты (first-run + шрифты), тёплый — секунды.
       Шрифты переписаны на локальный кэш (fonts.googleapis.com с этой машины
       отвечает ~8 с — замер одного обхода растягивался на часы). */
    execFile(CHROME, [
      '--headless=new', '--disable-gpu', '--no-sandbox', '--disable-extensions',
      '--lang=az', '--accept-lang=az',
      '--no-first-run', '--no-default-browser-check',
      '--host-resolver-rules=MAP ipapi.co 127.0.0.1:9',
      '--user-data-dir=' + profileDir,
      '--virtual-time-budget=14000',
      '--window-size=' + winW + ',2400',
      '--dump-dom', url
    ], { encoding: 'utf8', maxBuffer: 1 << 28, timeout: 90000, killSignal: 'SIGKILL' }, function (err, dom) {
      try { fs.unlinkSync(tmp); } catch (e) { /* */ }
      if (wrapper) { try { fs.unlinkSync(wrapper); } catch (e) { /* */ } }
      if (!dom) { resolve({ file: rel, width, error: 'no dump ' + (err && err.message) }); return; }
      const block = dom.match(/<pre id="__sa_out">([\s\S]*?)<\/pre>/);
      if (!block) { resolve({ file: rel, width, error: 'no __sa_out' }); return; }
      const lines = block[1].split('\n').map(s => s.trim()).filter(Boolean);
      let data = null;
      for (const ln of lines) { try { data = JSON.parse(Buffer.from(ln, 'base64').toString('utf8')); } catch (e) { /* */ } }
      if (!data) { resolve({ file: rel, width, error: 'bad json' }); return; }
      data.file = rel; data.width = width;
      resolve(data);
    });
  });
}

/* Страница может быть снята «на полпути»: с обнулёнными ?sa=1 URL Chrome
   иногда отдаёт DOM до применения site-concept.css (замер: секции с padTop 0,
   герой по gtc.css). Признак — число загруженных таблиц стилей; при нём же
   повторяем замер (до 3 попыток) — данные такой страницы иначе врут. */
function loadedSheets(data) {
  if (!data) return 0;
  if (data.okCss) return 4;
  return 0;
}
async function measure(rel, width, profileDir) {
  let d = await measureOnce(rel, width, profileDir, 0);
  for (let i = 0; i < 2 && loadedSheets(d) < 4; i++) {
    if (process.env.SA_VERBOSE) process.stderr.write("    retry " + rel + " (sheets=" + loadedSheets(d) + String.fromCharCode(10));
    d = await measureOnce(rel, width, profileDir, i + 1);
  }
  return d;
}
async function run() {
  const tasks = [];
  for (const w of WIDTHS) for (const p of PAGES) tasks.push({ w, p });
  const results = [];
  let idx = 0, done = 0;
  const profiles = [];
  async function worker(wi) {
    /* Каталоги профилей — ПОСТОЯННЫЕ (не по pid): кэш шрифтов переживает
       прогон, и повторный обмер идёт по 3-4 с на страницу вместо минут. */
    const profileDir = (process.env.SA_PROFILE_DIR || 'D:/ragimoff-tmp/saprof') + '-' + wi;
    profiles.push(profileDir);
    while (idx < tasks.length) {
      const t = tasks[idx++];
      const t0 = Date.now();
      const r = await measure(t.p, t.w, profileDir);
      results.push(r);
      done++;
      if (process.env.SA_VERBOSE) process.stderr.write('  [' + wi + '] ' + t.p + ' @' + t.w + ' ' + ((Date.now() - t0) / 1000).toFixed(1) + 's' + (r.error ? ' ERR ' + r.error : '') + '\n');
      else if (done % 20 === 0) process.stderr.write('  ...' + done + '/' + tasks.length + '\n');
    }
  }
  await Promise.all(Array.from({ length: JOBS }, (_, wi) => worker(wi)));
  /* Профили не удаляем (кэш): чистка — вручную или --clean-profiles */
  if (process.env.SA_CLEAN_PROFILES) profiles.forEach(p => { try { fs.rmSync(p, { recursive: true, force: true }); } catch (e) { /* */ } });

  for (const w of WIDTHS) {
    const rows = [];
    const raw = results.filter(r => r.width === w);
    for (const d of raw) {
      if (d.error) { rows.push([d.file, w, 'ERROR', '-', d.error, '-', '']); continue; }
      const P = d.file;
      const T_top = w > 768 ? 88 : (w > 560 ? 48 : 32);
      const T_card = w > 560 ? 16 : 12;
      const T_sub = w > 768 ? 48 : 32;
      const T_ins = w > 860 ? 32 : 24;
      if (d.hScroll) rows.push([P, w, 'HSCROLL', 'doc', d.scrollW + '>' + d.cw, d.cw, (d.offenders[0] ? d.offenders[0].el + ' r=' + d.offenders[0].r : '')]);
      for (const b of (d.blocks || [])) {
        if (b.band) continue;
        if (b.badgeText && b.gapTop !== null && Math.abs(b.gapTop - T_top) > 2 && !b.centered) {
          rows.push([P, w, 'SEC-TOP', b.sel + ' [' + b.badgeText + ']', b.gapTop, T_top, 'padTop=' + b.padTop]);
        }
        if (!b.badgeText && b.gapTop !== null && b.gapTop > 112) {
          rows.push([P, w, 'SEC-TOP-', b.sel, b.gapTop, T_top, 'no badge, padTop=' + b.padTop]);
        }
        if (b.gapBot !== null && b.gapBot > 112) rows.push([P, w, 'SEC-BOT', b.sel + ' after ' + b.botEl, b.gapBot, '<=96', 'padBot=' + b.padBot]);
        if (b.voidMax && b.voidMax > 120) rows.push([P, w, 'VOID', b.sel, b.voidMax, '<=96', '']);
      }
      for (const s of (d.subs || [])) {
        const exp = 1.75 * s.fs;
        if (s.step !== null && Math.abs(s.step - exp) > 0.9 && s.lines > 1) {
          rows.push([P, w, 'LEAD-LH', s.block + ' ' + s.cls, s.step + ' (' + s.fs + 'px, ' + s.lines + ' lines)', r1x(exp), s.text]);
        }
        const tg = s.card ? T_card : T_sub;
        if (s.gap !== null && s.gap < tg - 1 && !s.inRow) rows.push([P, w, 'SUB-GAP', s.block + ' -> ' + s.next, s.gap, tg, s.cls + ' ' + s.text]);
        if (s.gap !== null && s.gap > 140 && !s.outsideMain && !s.inRow) rows.push([P, w, 'SUB-VOID', s.block + ' -> ' + s.next, s.gap, '<=120', s.cls + ' ' + s.text]);
      }
      for (const h of (d.h2s || [])) {
        if (h.overflow && w <= 560) rows.push([P, w, 'H2-WIDE', h.block, h.ink + ' > ' + h.avail, '<=avail', h.text + ' fs=' + h.fs + ' lines=' + h.lines]);
        else if (h.overflow && w > 560) rows.push([P, w, 'H2-WIDE', h.block, h.ink + ' > ' + h.avail, '<=avail', h.text + ' fs=' + h.fs]);
        if (h.align === 'center' && h.lines > 3) rows.push([P, w, 'H2-LINES', h.block, h.lines, '<=3', h.text]);
      }
      for (const t of (d.tables || [])) {
        if (t.ratio !== null && t.ratio < 99) rows.push([P, w, 'TABLE-W', t.block + ' ' + t.cls, t.ratio + '%', '100%', 'w=' + t.w + ' avail=' + t.avail]);
        if (t.h2Align === 'center' && t.subAlign && t.subAlign !== 'center') rows.push([P, w, 'TBL-ALIGN', t.block, t.subAlign, 'center', '']);
      }
      for (const c of (d.cards || [])) {
        if (c.gap < 6 || c.gap > 48) rows.push([P, w, 'CARD-GAP', c.cls + ' ' + c.head + '->' + c.next, c.gap, '16/12', '']);
      }
      for (const bg of (d.badges || [])) {
        if (bg.insetL !== null && bg.insetL < T_ins - 1 && !/^(SECTION|ARTICLE|MAIN|ASIDE)$/.test(bg.block)) {
          rows.push([P, w, 'BADGE-IN', bg.block + ' [' + bg.text + ']', 'L=' + bg.insetL + ' T=' + bg.insetT, T_ins, 'pad=' + bg.padL + '/' + bg.padT]);
        }
        if (bg.insetT !== null && bg.insetT < T_ins - 1 && !/^(SECTION|ARTICLE|MAIN|ASIDE)$/.test(bg.block)) {
          rows.push([P, w, 'BADGE-IN', bg.block + ' [' + bg.text + ']', 'L=' + bg.insetL + ' T=' + bg.insetT, T_ins, 'pad=' + bg.padL + '/' + bg.padT]);
        }
      }
      if (d.hero) {
        const V = w > 860 ? 48 : 36;
        const h = d.hero;
        if (h.gapBadgeTop !== null && Math.abs(h.gapBadgeTop - V) > 2) rows.push([P, w, 'HERO-TOP', 'badge', h.gapBadgeTop, V, '']);
        if (h.gapBadgeH1 !== null && Math.abs(h.gapBadgeH1 - V) > 2) rows.push([P, w, 'HERO-B-H1', 'badge->h1', h.gapBadgeH1, V, '']);
        if (w > 860) {
          /* десктоп: фото спозиционировано абсолютно, H1 → лид напрямую */
          if (h.gapH1Sub !== null && Math.abs(h.gapH1Sub - V) > 2) rows.push([P, w, 'HERO-H1-SUB', 'h1->lead', h.gapH1Sub, V, '']);
          if (h.photoTop !== null && Math.abs(h.photoTop) > 2) rows.push([P, w, 'HERO-PH-T', 'photoTop', h.photoTop, 0, '']);
          if (h.photoBot !== null && Math.abs(h.photoBot) > 2) rows.push([P, w, 'HERO-PH-B', 'photoBot', h.photoBot, 0, '']);
        } else {
          /* телефон/планшет: фото в потоке между H1 и лидом, тот же V */
          if (h.gapH1Photo !== null) {
            if (Math.abs(h.gapH1Photo - V) > 2) rows.push([P, w, 'HERO-H1-PH', 'h1->photo', h.gapH1Photo, V, '']);
            if (h.gapPhotoSub !== null && Math.abs(h.gapPhotoSub - V) > 2) rows.push([P, w, 'HERO-PH-SUB', 'photo->lead', h.gapPhotoSub, V, '']);
          } else if (h.gapH1Sub !== null && Math.abs(h.gapH1Sub - V) > 2) {
            rows.push([P, w, 'HERO-H1-SUB', 'h1->lead', h.gapH1Sub, V, '']);
          }
        }
        if (h.gapSubSearch !== null && h.gapSubSearch < V - 2) rows.push([P, w, 'HERO-LEAD-S', 'lead->search', h.gapSubSearch, '>=' + V, '']);
        if (h.gapSearchBot !== null && Math.abs(h.gapSearchBot - (V + 1)) > 2.5) rows.push([P, w, 'HERO-BOT', 'search->bottom', h.gapSearchBot, V + 1, '']);
      }
      /* БЛОК → БЛОК: низ содержимого блока N до верха содержимого блока N+1.
         Стандарт — ОДИН шаг (88/48/32): нижний паддинг блока снимается у того,
         за кем идёт ещё блок (site-concept.css, «ОДИН зазор между блоками»),
         иначе 88+88=176. Владелец 05.10.2026: «150 px вместо стандартных 88». */
      const bl = (d.blocks || []).filter(b => b.top !== undefined);
      for (let i = 0; i + 1 < bl.length; i++) {
        /* У вертикально центрированного блока первый элемент опущен
           внутренней центровкой (tg-band: метка на 114 при паддинге 85,44) —
           для него берём ГРАНЬ блока, а не позицию метки: иначе внутренняя
           центровка читалась бы как разрыв между блоками. */
        const cBot = bl[i].centered ? bl[i].bot : bl[i].bot - (bl[i].gapBot || 0);
        const cTop = bl[i + 1].centered ? bl[i + 1].top : bl[i + 1].top + (bl[i + 1].gapTop || 0);
        const g = Math.round((cTop - cBot) * 10) / 10;
        if (g > 100) rows.push([P, w, 'BLOCK-GAP', bl[i].sel + ' -> ' + bl[i + 1].sel, g, T_top, bl[i].botEl + ' / ' + (bl[i + 1].badgeText || '-')]);
      }
      for (const g of (d.grids || [])) {
        const gl = Math.min(g.rowGap || 999, g.colGap || 999);
        if (g.colGap >= 3 && (g.colGap < 12 || g.colGap > 32)) rows.push([P, w, 'GRID-GAP', g.cls + ' (' + g.kids + ')', g.colGap, '24/16', 'rowGap=' + g.rowGap]);
      }
      for (const b of (d.btns || [])) {
        const lo = w > 768 ? 24 : 16, hi = w > 768 ? 32 : 24;
        if (b.gap < 12 || b.gap > 48) rows.push([P, w, 'BTN-GAP', b.block + ' ' + b.prev + ' -> btn[' + b.text + ']', b.gap, lo + '-' + hi, b.btn]);
      }
      if (d.stripOverlap !== null && d.stripOverlap > 1) rows.push([P, w, 'STRIP-OVL', 'stats-strip', d.stripOverlap, 0, '']);
      /* примечание: HSCROLL-оффендеры */
      const note = (d.offenders && d.offenders.length && !d.hScroll)
        ? 'clipped=' + d.offenders.slice(0, 3).map(o => o.el + '@' + o.r).join(' | ') : '';
      if (note) rows.push([P, w, 'CLIPPED', 'doc', d.offenders.length, 0, note]);
    }
    const tsv = ['page\twidth\tclass\titem\tbefore\ttarget\tnote']
      .concat(rows.map(r => r.join('\t'))).join('\n') + '\n';
    fs.writeFileSync(path.join(OUT, 'standard_' + w + '.tsv'), tsv, 'utf8');
    fs.writeFileSync(path.join(OUT, 'standard_' + w + '.json'), JSON.stringify(raw, null, 1), 'utf8');
    const byClass = {};
    rows.forEach(r => { byClass[r[2]] = (byClass[r[2]] || 0) + 1; });
    console.log('width=' + w + '  rows=' + rows.length + '  ' + JSON.stringify(byClass));
  }
}
function r1x(v) { return Math.round(v * 100) / 100; }

run().catch(e => { console.error(e); process.exit(1); });
