/* ═══════════════════════════════════════════════════════════════════════
   RAGIMOFF · ATLAS — поведение
   ───────────────────────────────────────────────────────────────────────
   Без внешних библиотек. Всё на IntersectionObserver + rAF.
   Если этот файл не загрузился, страница остаётся полностью читаемой:
   «спрятанные» состояния включаются только классом html.js (см. <head>).
   ═══════════════════════════════════════════════════════════════════════ */

(function () {
  'use strict';

  var doc = document;
  var root = doc.documentElement;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var $  = function (s, c) { return (c || doc).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || doc).querySelectorAll(s)); };

  /* ───────────────────────── 1. КУРСОР ───────────────────────── */

  function initCursor() {
    var cur = $('#cur');
    if (!cur || !fine || reduce) return;

    var ring = $('.cur__ring', cur);
    var dot  = $('.cur__dot', cur);
    var txt  = $('.cur__txt', cur);
    var tx = window.innerWidth / 2, ty = window.innerHeight / 2;
    var cx = tx, cy = ty;

    root.classList.add('has-cur');

    doc.addEventListener('mousemove', function (e) {
      tx = e.clientX; ty = e.clientY;
      cur.style.opacity = '1';
    }, { passive: true });

    doc.addEventListener('mousedown', function () { cur.classList.add('is-down'); });
    doc.addEventListener('mouseup',   function () { cur.classList.remove('is-down'); });
    doc.addEventListener('mouseleave', function () { cur.style.opacity = '0'; });
    doc.addEventListener('mouseenter', function () { cur.style.opacity = '1'; });

    function loop() {
      cx += (tx - cx) * 0.17;
      cy += (ty - cy) * 0.17;
      ring.style.transform = 'translate3d(' + cx + 'px,' + cy + 'px,0)';
      dot.style.transform  = 'translate3d(' + tx + 'px,' + ty + 'px,0)';
      requestAnimationFrame(loop);
    }
    requestAnimationFrame(loop);

    // состояния
    var hit = 'a, button, [data-cur], input, .svc__row, .vault__strip';
    doc.addEventListener('mouseover', function (e) {
      var el = e.target.closest && e.target.closest(hit);
      if (!el) return;
      var label = el.getAttribute && el.getAttribute('data-cur');
      if (label) {
        txt.textContent = label;
        cur.classList.add('is-label');
        cur.classList.remove('is-link');
      } else if (el.tagName === 'A' || el.tagName === 'BUTTON') {
        cur.classList.add('is-link');
        cur.classList.remove('is-label');
      }
    });
    doc.addEventListener('mouseout', function (e) {
      var el = e.target.closest && e.target.closest(hit);
      if (!el) return;
      cur.classList.remove('is-link', 'is-label');
    });
  }

  /* ───────────────────────── 2. ШАПКА ───────────────────────── */

  function initHeader() {
    var hdr = $('#hdr');
    if (!hdr) return;
    var last = 0, ticking = false;

    function paint() {
      var y = window.scrollY || window.pageYOffset;
      hdr.classList.toggle('is-stuck', y > 40);

      if (y > 520 && y > last + 4) hdr.classList.add('is-hidden');
      else if (y < last - 4 || y < 520) hdr.classList.remove('is-hidden');
      last = y;

      // тема шапки — по разделу, который сейчас под ней
      var probe = doc.elementsFromPoint
        ? doc.elementsFromPoint(window.innerWidth / 2, 40)
        : [];
      var theme = 'ink';
      for (var i = 0; i < probe.length; i++) {
        var t = probe[i].getAttribute && probe[i].getAttribute('data-theme');
        if (t) { theme = t; break; }
      }
      hdr.classList.toggle('is-onlight', theme !== 'ink');

      var fill = $('#railFill');
      if (fill) {
        var max = doc.documentElement.scrollHeight - window.innerHeight;
        fill.style.transform = 'scaleX(' + (max > 0 ? Math.min(1, y / max) : 0) + ')';
      }
      ticking = false;
    }

    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(paint); }
    }, { passive: true });
    paint();
  }

  /* ───────────────────────── 3. ПОЯВЛЕНИЯ ───────────────────────── */

  function initReveals() {
    var targets = $$('.rv, .rv-l, .rv-s, .rv-rule, .mask, [data-split]');
    if (!targets.length) return;

    if (!('IntersectionObserver' in window)) {
      targets.forEach(function (el) { el.classList.add('is-in'); });
      $$('[data-split]').forEach(function (el) { splitWords(el); el.classList.add('is-in'); });
      return;
    }

    // разбивка по словам до наблюдения
    $$('[data-split]').forEach(function (el) {
      var step = parseInt(el.getAttribute('data-split'), 10) || 55;
      splitWords(el, step);
    });

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add('is-in');
        io.unobserve(en.target);
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.01 });

    targets.forEach(function (el) { io.observe(el); });

    // каскад внутри контейнера
    $$('[data-stagger]').forEach(function (box) {
      var step = parseInt(box.getAttribute('data-stagger'), 10) || 90;
      $$(':scope > *', box).forEach(function (c, i) {
        c.style.setProperty('--d', (i * step) + 'ms');
      });
    });
  }

  /* разбивает текст на слова, каждое — в маске; <em> и прочее сохраняются */
  function splitWords(el, step) {
    var i = 0;
    (function walk(node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (n) {
        if (n.nodeType === 3) {
          var parts = n.textContent.split(/(\s+)/);
          if (!parts.length) return;
          var frag = doc.createDocumentFragment();
          parts.forEach(function (p) {
            if (!p) return;
            if (!p.trim()) { frag.appendChild(doc.createTextNode(p)); return; }
            var mask = doc.createElement('span');
            mask.className = 'w';
            var inner = doc.createElement('span');
            inner.className = 'w-i';
            inner.textContent = p;
            mask.appendChild(inner);
            frag.appendChild(mask);
            i++;
          });
          n.parentNode.replaceChild(frag, n);
        } else if (n.nodeType === 1 && !n.classList.contains('w')) {
          walk(n);
        }
      });
    })(el);

    $$('.w-i', el).forEach(function (w, k) {
      w.style.transitionDelay = (k * step) + 'ms';
    });
  }

  /* ───────────────────────── 4. ПАРАЛЛАКС ───────────────────────── */

  function initParallax() {
    if (reduce) return;
    var items = $$('[data-plx]');
    var hero = $('.hero');
    var mouseX = 0, mouseY = 0, lx = 0, ly = 0;

    if (hero && fine) {
      hero.addEventListener('mousemove', function (e) {
        mouseX = (e.clientX / window.innerWidth  - 0.5) * 2;
        mouseY = (e.clientY / window.innerHeight - 0.5) * 2;
      }, { passive: true });
    }

    var ticking = false;
    function paint() {
      var y = window.scrollY || window.pageYOffset;
      var vh = window.innerHeight;

      items.forEach(function (el) {
        var r = el.getBoundingClientRect();
        if (r.bottom < -200 || r.top > vh + 200) return;
        var depth = parseFloat(el.getAttribute('data-plx')) || 0.1;
        var mid = r.top + r.height / 2 - vh / 2;
        el.style.transform = 'translate3d(0,' + (-mid * depth).toFixed(2) + 'px,0)';
      });

      if (hero) {
        var fig = $('.hero__fig', hero);
        var head = $('.hero__plate', hero);
        var cue = $('.hero__cue', hero);
        lx += (mouseX - lx) * 0.06;
        ly += (mouseY - ly) * 0.06;
        if (fig)  fig.style.transform  = 'translate3d(' + (lx * 14).toFixed(2) + 'px,' + (-y * 0.06 + ly * 10).toFixed(2) + 'px,0)';
        if (head && y < vh) head.style.transform = 'translate3d(' + (-lx * 5).toFixed(2) + 'px,' + (-y * 0.13).toFixed(2) + 'px,0)';
        if (cue) cue.style.opacity = String(Math.max(0, 1 - y / 260));
      }

      ticking = false;
    }

    function request() {
      if (!ticking) { ticking = true; requestAnimationFrame(paint); }
    }
    window.addEventListener('scroll', request, { passive: true });
    window.addEventListener('resize', request);
    if (hero && fine) setInterval(request, 60);   // догоняем инерцию курсора
    paint();
  }

  /* ───────────────────────── 5. СЧЁТЧИКИ ───────────────────────── */

  function initCounters() {
    var nums = $$('[data-to]');
    if (!nums.length) return;

    function run(el) {
      var to = parseFloat(el.getAttribute('data-to'));
      var sfx = el.getAttribute('data-suffix') || '';
      if (reduce) { el.textContent = to + sfx; return; }
      var dur = 1500, t0 = null;
      function step(t) {
        if (t0 === null) t0 = t;
        var p = Math.min(1, (t - t0) / dur);
        var e = 1 - Math.pow(1 - p, 4);
        el.textContent = Math.round(to * e) + (p === 1 ? sfx : '');
        if (p < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    }

    var io = new IntersectionObserver(function (en) {
      en.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.closest('.stat') && e.target.closest('.stat').classList.add('is-in');
        run(e.target);
        io.unobserve(e.target);
      });
    }, { threshold: 0.4 });

    nums.forEach(function (n) { io.observe(n); });
  }

  /* ───────────────────────── 6. DRAG-ГАЛЕРЕЯ ───────────────────────── */

  function initDragStrip() {
    $$('.vault__strip').forEach(function (strip) {
      var down = false, startX = 0, startLeft = 0, moved = 0;

      strip.addEventListener('pointerdown', function (e) {
        if (e.pointerType === 'touch') return;
        down = true; moved = 0;
        startX = e.clientX; startLeft = strip.scrollLeft;
        strip.classList.add('is-drag');
      });
      strip.addEventListener('pointermove', function (e) {
        if (!down) return;
        var dx = e.clientX - startX;
        moved = Math.max(moved, Math.abs(dx));
        strip.scrollLeft = startLeft - dx;
      });
      ['pointerup', 'pointerleave', 'pointercancel'].forEach(function (ev) {
        strip.addEventListener(ev, function () {
          down = false; strip.classList.remove('is-drag');
        });
      });
      strip.addEventListener('click', function (e) {
        if (moved > 8) { e.preventDefault(); e.stopPropagation(); }
      }, true);
    });

    $$('[data-vault-nav]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var strip = $(btn.getAttribute('data-vault-nav'));
        if (!strip) return;
        var item = $('.vault__item', strip);
        var w = item ? item.getBoundingClientRect().width + 16 : 280;
        strip.scrollBy({ left: w * (btn.getAttribute('data-dir') === 'prev' ? -1 : 1),
                         behavior: reduce ? 'auto' : 'smooth' });
      });
    });
  }

  /* ───────────────────────── 7. ПРЕВЬЮ УСЛУГ ───────────────────────── */

  function initPeek() {
    var rows = $$('.svc__row[data-img]');
    if (!rows.length || !fine) return;

    var box = doc.createElement('div');
    box.className = 'svc__peek';
    box.innerHTML = '<img alt="" />';
    doc.body.appendChild(box);
    var img = $('img', box);

    var visible = false, tx = 0, ty = 0, x = 0, y = 0, raf = null;

    function loop() {
      x += (tx - x) * 0.14;
      y += (ty - y) * 0.14;
      box.style.left = x + 'px';
      box.style.top  = y + 'px';
      raf = requestAnimationFrame(loop);
    }

    rows.forEach(function (row) {
      row.addEventListener('mouseenter', function () {
        var src = row.getAttribute('data-img');
        if (img.getAttribute('src') !== src) img.setAttribute('src', src);
        box.classList.add('is-on');
        visible = true;
        if (!raf) raf = requestAnimationFrame(loop);
      });
      row.addEventListener('mouseleave', function () {
        box.classList.remove('is-on');
        visible = false;
        if (raf) { cancelAnimationFrame(raf); raf = null; }
      });
      row.addEventListener('mousemove', function (e) {
        var off = window.innerWidth > 1280 ? 190 : 130;
        tx = Math.min(e.clientX + off, window.innerWidth - 170);
        ty = e.clientY;
      }, { passive: true });
    });
  }

  /* ───────────────────────── 8. МОБИЛЬНОЕ МЕНЮ ───────────────────────── */

  function initSheet() {
    var sheet  = $('#sheet');
    var burger = $('#burger');
    if (!sheet || !burger) return;

    function set(open) {
      sheet.classList.toggle('is-open', open);
      burger.classList.toggle('is-on', open);
      doc.body.classList.toggle('is-locked', open);
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    }

    burger.addEventListener('click', function () {
      set(!sheet.classList.contains('is-open'));
    });
    $$('a', sheet).forEach(function (a) {
      a.addEventListener('click', function () { set(false); });
    });
    doc.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') set(false);
    });
  }

  /* ───────────────────────── 9. ПАЛИТРА ПОИСКА ───────────────────────── */

  function initSearch() {
    var pal = $('#palette');
    var openers = $$('[data-search-open]');
    if (!pal || !openers.length) return;

    var input = $('#paletteInput');
    var res   = $('#paletteRes');
    var index = null, sel = -1, loading = false;

    function load() {
      if (index || loading) return Promise.resolve();
      loading = true;
      return fetch('search-index.json')
        .then(function (r) { return r.ok ? r.json() : []; })
        .then(function (d) { index = Array.isArray(d) ? d : []; })
        .catch(function () { index = []; });
    }

    function open() {
      pal.classList.add('is-open');
      doc.body.classList.add('is-locked');
      load().then(function () { render(input.value); });
      setTimeout(function () { input.focus(); input.select(); }, 60);
    }
    function close() {
      pal.classList.remove('is-open');
      doc.body.classList.remove('is-locked');
    }

    function esc(s) {
      return String(s).replace(/[&<>"]/g, function (c) {
        return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
      });
    }

    function render(q) {
      q = (q || '').trim().toLowerCase();
      if (!index) { res.innerHTML = '<div class="palette__empty">Yüklənir…</div>'; return; }

      var hits = index.filter(function (it) {
        if (!q) return true;
        return (it.title + ' ' + (it.text || '') + ' ' + (it.sub || '')).toLowerCase().indexOf(q) > -1;
      }).slice(0, 40);

      if (!hits.length) {
        res.innerHTML = '<div class="palette__empty">Heç nə tapılmadı. Başqa sözlə yoxlayın.</div>';
        sel = -1; return;
      }

      res.innerHTML = hits.map(function (it, i) {
        var t = esc(it.title || it.page || '');
        if (q) {
          try {
            t = t.replace(new RegExp('(' + q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'ig'), '<mark>$1</mark>');
          } catch (err) { /* оставляем как есть */ }
        }
        return '<a href="' + esc(it.url || '#') + '" data-i="' + i + '">' +
                 '<div class="palette__t">' + t + '</div>' +
                 '<div class="palette__s">' + esc(it.sub || '') + (it.text ? ' · ' + esc(it.text.slice(0, 96)) : '') + '</div>' +
               '</a>';
      }).join('');
      sel = -1;
    }

    openers.forEach(function (b) {
      b.addEventListener('click', function (e) { e.preventDefault(); open(); });
    });
    pal.addEventListener('click', function (e) { if (e.target === pal) close(); });

    input.addEventListener('input', function () { render(input.value); });

    doc.addEventListener('keydown', function (e) {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); open(); return; }
      if (e.key === '/' && !pal.classList.contains('is-open') &&
          !/^(INPUT|TEXTAREA)$/.test(doc.activeElement.tagName)) { e.preventDefault(); open(); return; }
      if (!pal.classList.contains('is-open')) return;

      if (e.key === 'Escape') { close(); return; }
      var links = $$('a', res);
      if (!links.length) return;
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
        e.preventDefault();
        sel += (e.key === 'ArrowDown' ? 1 : -1);
        if (sel < 0) sel = links.length - 1;
        if (sel >= links.length) sel = 0;
        links.forEach(function (a, i) { a.classList.toggle('is-sel', i === sel); });
        links[sel].scrollIntoView({ block: 'nearest' });
      }
      if (e.key === 'Enter' && sel > -1) { window.location.href = links[sel].getAttribute('href'); }
    });
  }

  /* ───────────────────────── 10. МЕЛОЧИ ───────────────────────── */

  function initExtras() {
    var top = $('#toTop');
    if (top) {
      window.addEventListener('scroll', function () {
        top.classList.toggle('is-on', (window.scrollY || 0) > 900);
      }, { passive: true });
      top.addEventListener('click', function () {
        window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' });
      });
    }

    // мягкий наклон бегущей строки по скорости прокрутки
    var mq = $('.mq');
    if (mq && !reduce) {
      var lastY = window.scrollY, v = 0;
      window.addEventListener('scroll', function () {
        var y = window.scrollY;
        v = y - lastY; lastY = y;
        var skew = Math.max(-5, Math.min(5, v * -0.25));
        mq.style.transform = 'skewX(' + skew.toFixed(2) + 'deg)';
        clearTimeout(mq._t);
        mq._t = setTimeout(function () { mq.style.transform = 'skewX(0deg)'; }, 140);
      }, { passive: true });
    }

    // зерно дышит от прокрутки
    var grain = $('.grain');
    if (grain && !reduce) {
      window.addEventListener('scroll', function () {
        grain.style.transform = 'translate3d(0,' + (-(window.scrollY % 200) * 0.4).toFixed(1) + 'px,0)';
      }, { passive: true });
    }

    // плавные внутренние переходы
    if (!reduce) {
      doc.addEventListener('click', function (e) {
        var a = e.target.closest && e.target.closest('a[href^="#"]');
        if (!a) return;
        var id = a.getAttribute('href');
        if (id === '#' || id.length < 2) return;
        var t = doc.querySelector(id);
        if (!t) return;
        e.preventDefault();
        var y = t.getBoundingClientRect().top + window.scrollY - 90;
        window.scrollTo({ top: y, behavior: 'smooth' });
      });
    }
  }

  /* ───────────────────────── СТАРТ ───────────────────────── */

  function boot() {
    initCursor();
    initHeader();
    initReveals();
    initParallax();
    initCounters();
    initDragStrip();
    initPeek();
    initSheet();
    initSearch();
    initExtras();
  }

  if (doc.readyState === 'loading') doc.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
