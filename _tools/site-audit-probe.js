/* site-audit-probe.js — замерщик, который site-audit.js вставляет в копию
 * страницы перед </body>. Результат кладётся в <title> как AUDIT-JSON:{...},
 * драйвер вынимает его из `chrome --headless --dump-dom`.
 *
 * Мерит то, что статикой не видно: горизонтальную прокрутку, вылет за
 * вьюпорт, роль гарнитуры по факту отрисовки, контраст текста, наложения
 * текстовых блоков, битые картинки, светлые пятна, размеры кнопок.
 *
 * Ничего не меняет в DOM: только читает getBoundingClientRect/computedStyle.
 */
(function () {
  'use strict';
  if (window.__AUDIT_PROBE__) return;
  window.__AUDIT_PROBE__ = 1;
  /* __AUDIT_LIGHT__: дешёвый режим (мобильная ширина) — только прокрутка,
     вылет за вьюпорт, пустые блоки, битые картинки. Контраст, гарнитуры,
     наложения, светлые пятна, размеры кнопок там не считаем: это самые
     дорогие проходы, а на телефоне их дублировать незачем. */
  var LIGHT = !!window.__AUDIT_LIGHT__;

  function r1(v) { return Math.round(v * 10) / 10; }
  function clean(s) { return String(s == null ? '' : s).replace(/\s+/g, ' ').trim(); }
  function textOf(el, n) {
    var t = clean(el.textContent);
    n = n || 64;
    return t.length > n ? t.slice(0, n) + '…' : t;
  }
  function sel(el) {
    var parts = [], e = el, i = 0;
    while (e && e.nodeType === 1 && i < 4) {
      if (e.id) { parts.unshift('#' + e.id); break; }
      var s = e.tagName.toLowerCase();
      var cl = (typeof e.className === 'string' ? e.className : '').trim().split(/\s+/).filter(Boolean).slice(0, 2);
      if (cl.length) s += '.' + cl.join('.');
      parts.unshift(s);
      e = e.parentElement; i++;
    }
    return parts.join('>');
  }
  function hasText(el) { return clean(el.textContent).length > 0; }
  function ownText(el) {
    var t = '';
    for (var i = 0; i < el.childNodes.length; i++) {
      var n = el.childNodes[i];
      if (n.nodeType === 3) t += n.nodeValue;
    }
    return clean(t);
  }
  function box(el) {
    var r = el.getBoundingClientRect();
    return { t: r.top, b: r.bottom, l: r.left, rr: r.right, w: r.width, h: r.height };
  }
  function vis(el, cs) {
    if (cs.display === 'none' || cs.visibility === 'hidden') return false;
    if (parseFloat(cs.opacity) < 0.05) return false;
    var r = el.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) return false;
    return true;
  }
  /* внеэкранные по замыслу узлы: off-canvas меню, skip-link, «наверх» */
  var OFFCANVAS = /(mobile-?nav|mobilenav|drawer|off-?canvas|skip-link|skip-link2|menu-panel|side-menu|to-top|scroll-top|visually-hidden|sr-only)/i;
  function isOffCanvas(el) {
    var e = el, i = 0;
    while (e && e.nodeType === 1 && i < 8) {
      var cls = typeof e.className === 'string' ? e.className : '';
      if (OFFCANVAS.test(cls) || OFFCANVAS.test(e.id || '')) return true;
      e = e.parentElement; i++;
    }
    return false;
  }

  /* Обрезано ли содержимое родителем: свёрнутые аккордеоны (.law-body
     max-height:0; overflow:hidden), закрытые <details>, карусели. Без этой
     проверки невидимые строки давали «наложения текста» и «вылет за вьюпорт». */
  var RE_CLIP = /hidden|clip|auto|scroll/;
  function clipped(el, boxed) {
    /* boxed — результат box() с полями t/b/l/rr */
    var e = el.parentElement, n = 0;
    while (e && e.nodeType === 1 && n < 14) {
      var cs = getComputedStyle(e);
      if (cs.display === 'none') return true;
      /* закрытый <details>: Chrome держит боксовую геометрию содержимого,
         хотя оно не рисуется — из-за этого шли ложные «наложения» */
      if (e.tagName === 'DETAILS' && !e.open) return true;
      if (cs.contentVisibility === 'hidden') return true;
      if (RE_CLIP.test(cs.overflowX) || RE_CLIP.test(cs.overflowY)) {
        var r = e.getBoundingClientRect();
        if (Math.min(boxed.b, r.bottom) - Math.max(boxed.t, r.top) < 4) return true;
        if (Math.min(boxed.rr, r.right) - Math.max(boxed.l, r.left) < 4) return true;
      }
      e = e.parentElement; n++;
    }
    return false;
  }

  /* ── гарнитуры ─────────────────────────────────────────────── */
  function fam(cs) {
    var f = cs.fontFamily || '';
    if (/Cormorant/i.test(f)) return 'disp';
    if (/Literata/i.test(f)) return 'read';
    if (/Plex Mono/i.test(f)) return 'mono';
    if (/Montserrat/i.test(f)) return 'ui';
    if (/monospace|Consolas|Courier/i.test(f)) return 'mono-fallback';
    if (/Georgia|Times|serif/i.test(f)) return 'serif-fallback';
    if (/system-ui|-apple-system|sans-serif|Arial|Segoe/i.test(f)) return 'sans-fallback';
    return 'other:' + f.slice(0, 40);
  }
  var LEAD_CLASS = /(^|[-_])(hero-lead|ph-sub|ph-sub-mob|ph-sub-desk|sec-sub|sec-lead|eco-sub|eco-lead-line|section-sub|ab-lead-mob|ab-lead-desk|about-lead|svc-lead-desk|svc-lead-mob|pr-lead-desk|pr-lead-mob|blog-card-excerpt|price-card-desc|tl-desc|video-desc|age-desc|ssr-snip|form-success|article-body p|post-body p)([-_]|$)/;
  var ARTICLE = /(^|\s)(article-body|post-body|art-body)(\s|$)/;
  function expectedRole(el) {
    var tag = el.tagName.toLowerCase();
    var cls = typeof el.className === 'string' ? el.className : '';
    /* строка автора статьи — метаданные (site-concept.css §16), не лид */
    if (/(^|\s)post-byline(\s|$)/.test(cls)) return 'mono';
    /* заголовки внутри текста статьи набраны Literata — так решено в
       site-concept.css (.article-body h2/h3): это чтение, а не дисплей */
    if (/^h[1-4]$/.test(tag)) {
      var a = el.parentElement, n = 0;
      while (a && n < 4) {
        if (ARTICLE.test(typeof a.className === 'string' ? a.className : '')) return 'read';
        a = a.parentElement; n++;
      }
    }
    if (LEAD_CLASS.test(cls)) return 'read';
    if (/(^|\s)(badge|ph-badge)(\s|$)/.test(cls)) return 'mono';
    if (/(^|\s)(btn|btn-fill|btn-line|btn-dark)(\s|$)/.test(cls) || tag === 'button') return 'mono';
    if (/(^|\s)(card-link|blog-card-read|book-read-btn|date|post-date|fa-date|blog-card-date|badge|stat-label|sec-num)(\s|$)/.test(cls)) return 'mono';
    if (/(^|\s)(stat-num|stat-value)(\s|$)/.test(cls)) return 'disp';
    if (/(^|\s)(card-title|blog-card-title|bc-title|tl-title|step-title)(\s|$)/.test(cls)) return 'disp';
    if (tag === 'h1' || tag === 'h2') return 'disp';
    if (tag === 'h3' || tag === 'h4') {
      /* в карточках заголовок — дисплейный (§7 стандарта), вне — интерфейсный */
      var e = el;
      for (var n = 0; n < 4 && e; n++) {
        var ec = typeof e.className === 'string' ? e.className : '';
        if (/(^|\s)(card|svc-card|xid-card|feat-card|step-card|dir-card|blog-card|book-card|price-card)(\s|$)/.test(ec)) return 'disp';
        e = e.parentElement;
      }
      return 'ui';
    }
    if (tag === 'input' || tag === 'textarea' || tag === 'select') return 'ui';
    return null;
  }

  /* ── контраст ──────────────────────────────────────────────── */
  function parseColor(c) {
    var m = String(c).match(/rgba?\(([^)]+)\)/);
    if (!m) return null;
    var p = m[1].split(',').map(function (x) { return parseFloat(x); });
    return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 };
  }
  function over(fg, bg) { // fg поверх bg
    var a = fg.a;
    return { r: fg.r * a + bg.r * (1 - a), g: fg.g * a + bg.g * (1 - a), b: fg.b * a + bg.b * (1 - a), a: 1 };
  }
  function lum(c) {
    function ch(v) { v = v / 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }
    return 0.2126 * ch(c.r) + 0.7152 * ch(c.g) + 0.0722 * ch(c.b);
  }
  function baseBg(el) {
    /* композит цепочки фонов от <html> вниз; картинка-фон (герой) считается
       тёмной подложкой #07090E — так нормирует DESIGN-STANDARDS §4. */
    var chain = [], e = el;
    while (e && e.nodeType === 1) { chain.unshift(e); e = e.parentElement; }
    var acc = { r: 7, g: 9, b: 14, a: 1 };
    for (var i = 0; i < chain.length; i++) {
      var cs = getComputedStyle(chain[i]);
      /* фото-подложка (герой) считается тёмной: так нормирует §4 стандарта */
      if (cs.backgroundImage && cs.backgroundImage !== 'none') acc = { r: 7, g: 9, b: 14, a: 1 };
      var c = parseColor(cs.backgroundColor);
      if (c && c.a > 0.01) acc = over(c, acc);
    }
    return acc;
  }
  function contrastOf(el, cs) {
    var fg = parseColor(cs.color);
    if (!fg) return null;
    var bg = baseBg(el);
    var eff = fg.a < 1 ? over(fg, bg) : fg;
    var l1 = lum(eff), l2 = lum(bg);
    var hi = Math.max(l1, l2), lo = Math.min(l1, l2);
    return r1((hi + 0.05) / (lo + 0.05));
  }

  /* ── сбор ──────────────────────────────────────────────────── */
  function run() {
    var out = { url: location.pathname, w: window.innerWidth, cw: document.documentElement.clientWidth };
    try {
      var de = document.documentElement;
      out.scrollW = de.scrollWidth;
      out.hScroll = de.scrollWidth > de.clientWidth + 1;
      out.title = clean(document.title);
      if (document.body) {
        out.bodyScrollW = document.body.scrollWidth;
      }

      var all = document.querySelectorAll('body *');
      var i, el, cs, b, role, exp, f;
      var overflow = [], fonts = [], contrast = [], media = [], empty = [], light = [];
      var btns = {}, btnList = [], candidates = [], imgs = [];
      var maxRight = 0, maxRightEl = null;

      for (i = 0; i < all.length; i++) {
        el = all[i];
        cs = getComputedStyle(el);
        if (!vis(el, cs)) continue;
        b = box(el);
        if (b.rr > maxRight) { maxRight = b.rr; maxRightEl = el; }

        var tag = el.tagName.toLowerCase();
        var t = ownText(el);
        var isMedia = (tag === 'img' || tag === 'video' || tag === 'canvas' || (tag === 'svg' && b.w > 24));
        var isBox = /^(section|div|aside|header|footer)$/.test(tag) && b.w > 80 && b.h > 40;
        var hiddenByClip = clipped(el, b);

        /* 1. вылет за вьюпорт (внеэкранные меню и sr-only — не дефект) */
        if (hiddenByClip) continue;   /* обрезано родителем — невидимо, не считаем */
        if ((t.length > 0 || isMedia) && (b.rr > out.cw + 1.5 || b.l < -1.5) && !isOffCanvas(el)) {
          overflow.push({
            sel: sel(el), cls: (typeof el.className === 'string' ? el.className : '').slice(0, 60),
            tag: tag, right: r1(b.rr), left: r1(b.l), w: r1(b.w),
            text: textOf(el, 40), fixed: cs.position
          });
        }

        /* 2. роль гарнитуры */
        exp = LIGHT ? null : expectedRole(el);
        if (exp && t.length > 0) {
          f = fam(cs);
          if (f !== exp) {
            fonts.push({
              sel: sel(el), cls: (typeof el.className === 'string' ? el.className : '').slice(0, 50),
              tag: tag, exp: exp, got: f, fam: (cs.fontFamily || '').split(',')[0].replace(/["']/g, ''),
              size: r1(parseFloat(cs.fontSize)), weight: cs.fontWeight, transform: cs.textTransform,
              text: textOf(el, 48)
            });
          } else if (exp === 'read' && /uppercase/i.test(cs.textTransform)) {
            fonts.push({
              sel: sel(el), cls: (typeof el.className === 'string' ? el.className : '').slice(0, 50),
              tag: tag, exp: 'read(no-uppercase)', got: 'uppercase', fam: (cs.fontFamily || '').split(',')[0].replace(/["']/g, ''),
              size: r1(parseFloat(cs.fontSize)), weight: cs.fontWeight, transform: cs.textTransform,
              text: textOf(el, 48)
            });
          }
        }

        /* 3. контраст — только по листовому тексту */
        if (!LIGHT && t.length > 2 && !/^(script|style|noscript)$/.test(tag) && t.length > 0) {
          var base = contrastOf(el, cs);
          if (base != null) {
            var px = parseFloat(cs.fontSize);
            var bold = parseInt(cs.fontWeight, 10) >= 700;
            var need = (px >= 24 || (bold && px >= 18.66)) ? 3.0 : 4.5;
            if (base < need) {
              contrast.push({
                sel: sel(el), cls: (typeof el.className === 'string' ? el.className : '').slice(0, 50),
                ratio: base, need: need, color: cs.color, size: r1(px), weight: cs.fontWeight,
                text: textOf(el, 40)
              });
            }
          }
        }

        /* 4. светлые пятна: крупный светлый фон в тёмном шаблоне */
        if (!LIGHT && isBox) {
          var bgc = parseColor(cs.backgroundColor);
          if (bgc && bgc.a > 0.3 && lum(bgc) > 0.45 && b.w * b.h > 20000) {
            light.push({ sel: sel(el), bg: cs.backgroundColor, area: Math.round(b.w * b.h) });
          }
        }

        /* 5. пустые блоки */
        if (/^(section|article)$/.test(tag) || /(^|\s)(card|faq-item|svc-card|xid-card|feat-card|step-card|sec-inner)(\s|$)/.test(typeof el.className === 'string' ? el.className : '')) {
          if (!hasText(el) && !el.querySelector('img,video,canvas,svg,input,button,iframe')) {
            empty.push({ sel: sel(el), tag: tag, cls: (typeof el.className === 'string' ? el.className : '').slice(0, 50), h: r1(b.h) });
          }
        }

        /* 6. кнопки: единый размер */
        if (!isOffCanvas(el) && /(^|\s)(btn|btn-fill|btn-line|btn-dark|pdf-export-btn|social-btn)(\s|$)/.test(typeof el.className === 'string' ? el.className : '')) {
          var key = r1(b.h) + 'x' + r1(b.w);
          btns[key] = (btns[key] || 0) + 1;
          if (btnList.length < 24) {
            btnList.push({ cls: (typeof el.className === 'string' ? el.className : ''), h: r1(b.h), w: r1(b.w), text: textOf(el, 24), fam: fam(cs), radius: cs.borderRadius });
          }
        }

        /* 7. кандидаты в наложения: инлайн-элемент, разбитый на несколько
           строк, даёт объединяющий прямоугольник — это ложное наложение */
        if (LIGHT) continue;
        if (cs.display === 'inline' && el.getClientRects().length > 1) continue;
        if (t.length > 0 && /^(h1|h2|h3|h4|p|li|a|span|div|figcaption|blockquote|strong|em|td|th)$/.test(tag) && b.w * b.h > 300) {
          candidates.push({ el: el, sel: sel(el), b: b, text: textOf(el, 40), cls: (typeof el.className === 'string' ? el.className : '').slice(0, 40), tag: tag });
        }
      }

      /* картинки */
      imgs = document.querySelectorAll('img');
      for (i = 0; i < imgs.length; i++) {
        el = imgs[i];
        cs = getComputedStyle(el);
        var bb = box(el);
        var rec = {
          sel: sel(el), src: (el.getAttribute('src') || '').slice(0, 90),
          altAttr: el.hasAttribute('alt'), alt: (el.getAttribute('alt') || '').slice(0, 60),
          natural: [el.naturalWidth, el.naturalHeight], w: r1(bb.w), h: r1(bb.h),
          visible: vis(el, cs)
        };
        /* пустой alt законен, если картинка — обложка внутри ссылки, у которой
           есть свой текст (иначе скринридер прочитает название дважды) */
        var inLinkWithText = false;
        var p = el.parentElement, k = 0;
        while (p && k < 5) {
          if (p.tagName === 'A' && clean(p.textContent).length > 0) { inLinkWithText = true; break; }
          p = p.parentElement; k++;
        }
        if (!rec.altAttr) media.push({ kind: 'no-alt', sel: rec.sel, src: rec.src, w: rec.w, h: rec.h });
        else if (!LIGHT && !rec.alt && rec.visible && !inLinkWithText && bb.w > 150 && bb.h > 100) media.push({ kind: 'empty-alt', sel: rec.sel, src: rec.src, w: rec.w, h: rec.h });
        /* loading="lazy" ниже экрана браузер не грузит: это не «битая» картинка */
        var lazy = (el.getAttribute('loading') || '').toLowerCase() === 'lazy';
        if (!lazy && rec.visible && el.complete && el.naturalWidth === 0) media.push({ kind: 'broken', sel: rec.sel, src: rec.src, w: rec.w, h: rec.h });
      }

      overflow.sort(function (a, b) { return b.right - a.right; });
      out.overflow = overflow.slice(0, 12);
      out.overflowCount = overflow.length;
      out.maxRight = r1(maxRight);
      out.maxRightSel = maxRightEl ? sel(maxRightEl) : null;
      out.fonts = fonts.slice(0, 60);
      out.fontsCount = fonts.length;
      out.contrast = contrast.slice(0, 40);
      out.contrastCount = contrast.length;
      out.media = media.slice(0, 30);
      out.empty = empty.slice(0, 20);
      out.light = light.slice(0, 10);
      out.btnSizes = btns;
      out.btnList = btnList;
      out.lists = document.querySelectorAll('ul,ol').length;
      out.h1 = document.querySelectorAll('h1').length;
      out.imgs = imgs.length;

      /* наложения текста (пары без вложенности, пересечение > 30 % меньшего) */
      var overlaps = [];
      var C = candidates.slice(0, 320);
      for (i = 0; i < C.length; i++) {
        for (var j = i + 1; j < C.length; j++) {
          var A = C[i], B = C[j];
          if (A.el.contains(B.el) || B.el.contains(A.el)) continue;
          var x = Math.min(A.b.rr, B.b.rr) - Math.max(A.b.l, B.b.l);
          var y = Math.min(A.b.b, B.b.b) - Math.max(A.b.t, B.b.t);
          if (x <= 0 || y <= 0) continue;
          var inter = x * y;
          var amin = Math.min(A.b.w * A.b.h, B.b.w * B.b.h);
          if (amin <= 0) continue;
          if (inter / amin > 0.3) {
            overlaps.push({ a: A.sel, b: B.sel, at: A.text.slice(0, 30), bt: B.text.slice(0, 30), k: r1(inter / amin) });
          }
          if (overlaps.length > 25) break;
        }
        if (overlaps.length > 25) break;
      }
      out.overlaps = overlaps;

      /* герой: контроль стандарта (DESIGN-STANDARDS §4) */
      var hero = document.querySelector('.page-hero, .page-hero-x, .pg-hero');
      if (hero) {
        var hb = box(hero);
        var pimg = hero.querySelector('.photo-col img');
        var pb = pimg ? box(pimg) : null;
        var badge = hero.querySelector('.badge, .ph-badge');
        var fst = box(badge);
        var last = null;
        ['.badge', '.ph-badge', '.hero-h1', '.ph-h1', '.hero-lead', '.ph-sub', '.hero-search-wrap', '.ph-search-wrap'].forEach(function (s) {
          var e = hero.querySelector(s);
          if (e) { var b2 = box(e); if (!last || b2.b > last.b) last = b2; }
        });
        out.hero = {
          h: r1(hb.h), top: pb ? r1(pb.t - hb.t) : null, bottom: pb ? r1(hb.b - pb.b) : null,
          badgeTop: fst.t ? r1(fst.t - hb.t) : null, lastBottom: last ? r1(hb.b - last.b) : null,
          photoSrc: pimg ? (pimg.getAttribute('src') || '') : null,
          photoNat: pimg ? [pimg.naturalWidth, pimg.naturalHeight] : null
        };
      }
    } catch (err) {
      out.error = String(err && err.message || err);
    }
    document.title = 'AUDIT-JSON:' + JSON.stringify(out);
  }

  function go() {
    try { run(); } catch (e) { document.title = 'AUDIT-JSON:' + JSON.stringify({ error: String(e) }); }
  }
  if (document.readyState === 'complete') { go(); }
  window.addEventListener('load', function () { setTimeout(go, 300); });
  setTimeout(go, 3500);
  /* Последний замер — после того, как фиттер отработает по document.fonts:
     он правит паддинги героя, и на 3500 мс те ещё «до подгонки» (зазор
     блока героя читался как 40 вместо 32 случайным образом). */
  setTimeout(go, 6500);
})();
