/* ═══════════════════════════════════════════════════════════════════════
   xmotion.js — движок переходов между блоками
   ───────────────────────────────────────────────────────────────────────
   Общая библиотека примитивов для концептов v5 и v6. Обе страницы берут
   её как есть, а визуальный язык у каждой свой.

   Приёмы собраны по разбору verostudio.com:
     · маска, управляемая прокруткой (--mask-progress)
     · залипающий шаговый блок (pinned stepper)
     · две колонки: медиа держится, текст идёт (sticky diptych)
     · строка входит половинами с разных сторон
     · roll-up подписи на ссылках и кнопках (label + copy)
     · parallax через CSS-переменные
     · переход темы радиальной волной от кнопки

   Без JS страница полностью читаема: прячем состояния только под .js
   ═══════════════════════════════════════════════════════════════════════ */

(function () {
  'use strict';

  var doc = document;
  var root = doc.documentElement;
  var $  = function (s, c) { return (c || doc).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || doc).querySelectorAll(s)); };
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine   = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

  root.classList.add('js');

  function on(el, ev, fn, o) { el.addEventListener(ev, fn, o || { passive: true }); }
  function raf(fn) { return requestAnimationFrame(fn); }
  function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }

  /* ─────────────────────── 1. ТЕМА ─────────────────────── */

  function initTheme() {
    var KEY = 'ragimoff-theme';
    var toggles = $$('[data-theme-toggle]');
    if (!toggles.length) return;

    function current() { return root.getAttribute('data-theme') || 'light'; }

    function paint(next, originEl) {
      var apply = function () {
        root.setAttribute('data-theme', next);
        try { localStorage.setItem(KEY, next); } catch (e) {}
        $$('[data-theme-toggle]').forEach(function (b) {
          b.setAttribute('aria-pressed', next === 'dark' ? 'true' : 'false');
        });
      };

      if (!doc.startViewTransition || reduce || !originEl) { apply(); return; }

      var r = originEl.getBoundingClientRect();
      var x = r.left + r.width / 2;
      var y = r.top + r.height / 2;
      var R = Math.hypot(Math.max(x, window.innerWidth - x), Math.max(y, window.innerHeight - y));

      var vt = doc.startViewTransition(apply);
      vt.ready.then(function () {
        root.animate(
          { clipPath: ['circle(0px at ' + x + 'px ' + y + 'px)', 'circle(' + R + 'px at ' + x + 'px ' + y + 'px)'] },
          { duration: 640, easing: 'cubic-bezier(.16,1,.3,1)', pseudoElement: '::view-transition-new(root)' }
        );
      }).catch(function () {});
    }

    toggles.forEach(function (b) {
      b.addEventListener('click', function () {
        paint(current() === 'dark' ? 'light' : 'dark', b);
      });
    });

    // Ctrl/Cmd + J — быстрый перебор темы
    doc.addEventListener('keydown', function (e) {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'j') {
        e.preventDefault();
        paint(current() === 'dark' ? 'light' : 'dark', toggles[0]);
      }
    });

    // Тема по умолчанию у каждого концепта своя (её ставит inline-скрипт
    // страницы). Сохранённый выбор пользователя важнее.
    try {
      var saved = localStorage.getItem('ragimoff-theme');
      if (saved) root.setAttribute('data-theme', saved);
      else if (!root.getAttribute('data-theme')) {
        root.setAttribute('data-theme',
          window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
      }
    } catch (e) {
      if (!root.getAttribute('data-theme')) root.setAttribute('data-theme', 'light');
    }
  }

  /* ─────────────────────── 1b. АНИМАЦИИ ─────────────────────── */
  /* Системная настройка «уменьшить движение» гасит все переходы.
     Кнопка на сайте позволяет включить их принудительно, не заходя
     в параметры ОС. Флаг живёт в localStorage. */

  function initMotionToggle() {
    var KEY = 'ragimoff-motion';
    var btns = $$('[data-motion-toggle]');
    if (!btns.length) return;
    var sysReduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    function paint(on) {
      root.classList.toggle('force-motion', on);
      reduce = !on && sysReduce;
      btns.forEach(function (b) {
        b.setAttribute('aria-pressed', on ? 'true' : 'false');
        b.classList.toggle('is-on', on);
        b.setAttribute('title', on ? 'Animasiyalar: açıq' : 'Animasiyalar: bağlı');
      });
    }

    var saved = null;
    try { saved = localStorage.getItem(KEY); } catch (e) {}
    paint(saved === 'on');

    btns.forEach(function (b) {
      b.addEventListener('click', function () {
        var next = !root.classList.contains('force-motion');
        paint(next);
        try { localStorage.setItem(KEY, next ? 'on' : 'off'); } catch (e) {}
        // пересобираем зависящие от прокрутки блоки
        window.dispatchEvent(new Event('scroll'));
      });
    });
  }

  /* ─────────────────────── 2. ПОЯВЛЕНИЯ ─────────────────────── */

  function initReveal() {
    var els = $$('[data-reveal]');
    if (!els.length) return;

    if (!('IntersectionObserver' in window)) {
      els.forEach(function (e) { e.classList.add('is-in'); });
      return;
    }

    var io = new IntersectionObserver(function (list) {
      list.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add('is-in');
        io.unobserve(en.target);
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.01 });

    els.forEach(function (e) { io.observe(e); });

    // каскад внутри контейнера
    $$('[data-stagger]').forEach(function (box) {
      var step = parseInt(box.getAttribute('data-stagger'), 10) || 90;
      $$(':scope > *', box).forEach(function (c, i) {
        c.style.setProperty('--d', (i * step) + 'ms');
      });
    });
  }

  /* ─────────── 3. СТРОКА ВХОДИТ ПОЛОВИНАМИ ─────────── */
  /* Разметка:
     <span class="tl"><span class="tl__a">начало </span><span class="tl__b">конец</span></span>
     Первая половина едет слева, вторая — справа. Так же читается скринридером. */

  function initLines() {
    var groups = $$('[data-lines]');
    if (!groups.length) return;

    if (!('IntersectionObserver' in window)) {
      groups.forEach(function (g) { g.classList.add('is-in'); });
      return;
    }

    var io = new IntersectionObserver(function (list) {
      list.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add('is-in');
        io.unobserve(en.target);
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.02 });

    groups.forEach(function (g) { io.observe(g); });
  }

  /* ─────────── 4. МАСКА, УПРАВЛЯЕМАЯ ПРОКРУТКОЙ ─────────── */
  /* [data-mask] — элементу пишется --p от 0 до 1 по мере прохода через экран */

  function initMask() {
    var els = $$('[data-mask]');
    if (!els.length || reduce) return;

    var ticking = false;
    function paint() {
      var vh = window.innerHeight;
      els.forEach(function (el) {
        var r = el.getBoundingClientRect();
        if (r.bottom < -vh * 0.3 || r.top > vh * 1.3) return;
        var p = clamp((vh - r.top) / (vh + r.height), 0, 1);
        var mode = el.getAttribute('data-mask') || 'in';
        if (mode === 'in') {
          // раскрытие: 0.15 → 0.6 прохода
          p = clamp((p - 0.12) / 0.42, 0, 1);
        } else if (mode === 'through') {
          p = clamp((p - 0.1) / 0.8, 0, 1);
        }
        el.style.setProperty('--p', p.toFixed(4));
      });
      ticking = false;
    }
    function req() { if (!ticking) { ticking = true; raf(paint); } }
    on(window, 'scroll', req);
    window.addEventListener('resize', req);
    paint();
  }

  /* ─────────── 5. ЗАЛИПАЮЩИЙ ШАГОВЫЙ БЛОК ─────────── */
  /* [data-pin] — внутри N .pin__item. Прокрутка двигает --active и --p у каждого */

  function initPin() {
    var pins = $$('[data-pin]');
    if (!pins.length) return;

    var ticking = false;
    function paint() {
      var vh = window.innerHeight;
      pins.forEach(function (pin) {
        var r = pin.getBoundingClientRect();
        if (r.bottom < 0 || r.top > vh) return;
        var total = pin.offsetHeight - vh;
        if (total <= 0) return;
        var prog = clamp(-r.top / total, 0, 1);
        var items = $$('.pin__item', pin);
        var panels = $$('.pin__panel', pin);
        var dots = $$('.pin__dot', pin);
        var n = items.length;
        var centre = prog * n;               // 0 → n
        var active = Math.min(n - 1, Math.floor(centre));

        pin.style.setProperty('--progress', prog.toFixed(4));
        pin.style.setProperty('--active', String(active));

        // треугольное окно: элемент ярок в своём отрезке и гаснет на стыках
        items.forEach(function (it, i) {
          var v = clamp(1 - Math.abs(centre - (i + 0.5)) * 2, 0, 1);
          it.style.setProperty('--v', v.toFixed(4));
          it.style.setProperty('--s', (i - centre).toFixed(4));
        });
        panels.forEach(function (p, i) { p.style.setProperty('--v', (i === active ? 1 : 0)); });
        dots.forEach(function (d, i) {
          d.classList.toggle('is-on', i <= active);
          d.setAttribute('aria-current', i === active ? 'true' : 'false');
        });
      });
      ticking = false;
    }
    function req() { if (!ticking) { ticking = true; raf(paint); } }
    on(window, 'scroll', req);
    window.addEventListener('resize', req);
    paint();
  }

  /* ─────────── 5b. ГОРИЗОНТАЛЬНЫЙ ЗАЛИПАЮЩИЙ ТРЕК ─────────── */
  /* [data-pin-x] — секция высотой N экранов; внутри .xtrack едет вбок.
     При reduced-motion секция разворачивается в обычную горизонтальную
     ленту с прокруткой (см. CSS). */

  function initPinX() {
    var pins = $$('[data-pin-x]');
    if (!pins.length || reduce) return;

    var ticking = false;
    function paint() {
      var vh = window.innerHeight;
      pins.forEach(function (pin) {
        var r = pin.getBoundingClientRect();
        if (r.bottom < 0 || r.top > vh) return;
        var total = pin.offsetHeight - vh;
        if (total <= 0) return;
        var prog = clamp(-r.top / total, 0, 1);
        var track = $('.xtrack', pin);
        if (!track) return;
        var maxX = Math.max(0, track.scrollWidth - track.clientWidth);
        pin.style.setProperty('--progress', prog.toFixed(4));
        track.style.transform = 'translate3d(' + (-prog * maxX).toFixed(2) + 'px,0,0)';

        // подсветка текущей карточки
        var cards = $$('.xcard', pin);
        var n = cards.length;
        if (!n) return;
        var active = clamp(Math.round(prog * (n - 1)), 0, n - 1);
        cards.forEach(function (c, i) {
          c.classList.toggle('is-on', i === active);
          c.setAttribute('aria-current', i === active ? 'true' : 'false');
        });
        pin.style.setProperty('--active', String(active));
      });
      ticking = false;
    }
    function req() { if (!ticking) { ticking = true; raf(paint); } }
    on(window, 'scroll', req);
    window.addEventListener('resize', req);
    paint();
  }

  /* ─────────────────────── 6. PARALLAX ─────────────────────── */
  /* [data-parallax="40"] — глубина в процентах от высоты прохода.
     Пишутся --py (вертикаль) и --px (горизонталь от курсора в герое). */

  function initParallax() {
    if (reduce) return;
    var els = $$('[data-parallax]');
    var hero = $('[data-hero]');
    var mx = 0, cx = 0;

    if (hero && fine) {
      on(hero, 'mousemove', function (e) {
        mx = (e.clientX / window.innerWidth - 0.5) * 2;
      });
    }

    var ticking = false;
    function paint() {
      var vh = window.innerHeight;
      els.forEach(function (el) {
        var r = el.getBoundingClientRect();
        if (r.bottom < -200 || r.top > vh + 200) return;
        var range = parseFloat(el.getAttribute('data-parallax')) || 20;
        var mid = (r.top + r.height / 2) - vh / 2;
        var py = (-mid / vh) * range;
        el.style.setProperty('--py', py.toFixed(3) + '%');
      });

      if (hero && fine) {
        cx += (mx - cx) * 0.06;
        $$('[data-hero-shift]', hero).forEach(function (el) {
          var k = parseFloat(el.getAttribute('data-hero-shift')) || 1;
          el.style.setProperty('--px', (cx * k).toFixed(4));
        });
      }
      ticking = false;
    }
    function req() { if (!ticking) { ticking = true; raf(paint); } }
    on(window, 'scroll', req);
    window.addEventListener('resize', req);
    if (hero && fine) setInterval(req, 64);
    paint();
  }

  /* ─────────────────────── 7. СЧЁТЧИКИ ─────────────────────── */

  function initCounters() {
    var els = $$('[data-count]');
    if (!els.length) return;

    function run(el) {
      var to = parseFloat(el.getAttribute('data-count'));
      var sfx = el.getAttribute('data-suffix') || '';
      var dec = parseInt(el.getAttribute('data-decimals'), 10) || 0;
      if (reduce) { el.textContent = to.toFixed(dec) + sfx; return; }
      var t0 = null, dur = 1600;
      function step(t) {
        if (t0 === null) t0 = t;
        var p = clamp((t - t0) / dur, 0, 1);
        var e = 1 - Math.pow(1 - p, 4);
        el.textContent = (to * e).toFixed(dec) + (p === 1 ? sfx : '');
        if (p < 1) raf(step);
      }
      raf(step);
    }

    var io = new IntersectionObserver(function (list) {
      list.forEach(function (en) {
        if (!en.isIntersecting) return;
        run(en.target);
        io.unobserve(en.target);
      });
    }, { threshold: 0.35 });
    els.forEach(function (e) { io.observe(e); });
  }

  /* ─────────────────────── 8. ПЕРЕБОР БУКВ ─────────────────────── */

  function initScramble() {
    var els = $$('[data-scramble]');
    if (!els.length || reduce) return;
    var GLYPHS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ█▓▒░#@%/\\';

    function run(el) {
      var final = el.getAttribute('data-text') || el.textContent;
      var len = final.length, t0 = null, dur = 700;
      function step(t) {
        if (t0 === null) t0 = t;
        var p = clamp((t - t0) / dur, 0, 1);
        var solid = Math.floor(p * len * 1.25);
        var out = '';
        for (var i = 0; i < len; i++) {
          var ch = final[i];
          if (ch === ' ') { out += ' '; continue; }
          out += i < solid ? ch : GLYPHS[(Math.random() * GLYPHS.length) | 0];
        }
        el.textContent = out;
        if (p < 1) raf(step); else el.textContent = final;
      }
      raf(step);
    }

    var io = new IntersectionObserver(function (list) {
      list.forEach(function (en) {
        if (!en.isIntersecting) return;
        run(en.target);
        io.unobserve(en.target);
      });
    }, { threshold: 0.5 });
    els.forEach(function (e) { io.observe(e); });
  }

  /* ─────────────────────── 9. МЕНЮ ─────────────────────── */

  function initMenu() {
    var sheet = $('#sheet');
    var burger = $('#burger');
    var panel = $('#menuPanel');

    function setSheet(open) {
      if (!sheet) return;
      sheet.classList.toggle('is-open', open);
      doc.body.classList.toggle('is-locked', open);
      if (burger) {
        burger.classList.toggle('is-on', open);
        burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      }
      // каскад пунктов
      $$('li', sheet).forEach(function (li, i) {
        li.style.setProperty('--i', i);
      });
    }

    function setPanel(open) {
      if (!panel) return;
      panel.classList.toggle('is-open', open);
      doc.body.classList.toggle('is-locked', open);
      var t = $('[data-menu-toggle]');
      if (t) {
        t.setAttribute('aria-expanded', open ? 'true' : 'false');
        t.classList.toggle('is-on', open);
      }
    }

    if (burger) burger.addEventListener('click', function () {
      setSheet(!sheet.classList.contains('is-open'));
    });

    $$('[data-menu-toggle]').forEach(function (b) {
      b.addEventListener('click', function () {
        setPanel(!panel.classList.contains('is-open'));
      });
    });

    if (sheet) $$('a', sheet).forEach(function (a) {
      a.addEventListener('click', function () { setSheet(false); });
    });
    if (panel) $$('a', panel).forEach(function (a) {
      a.addEventListener('click', function () { setPanel(false); });
    });

    doc.addEventListener('keydown', function (e) {
      if (e.key !== 'Escape') return;
      setSheet(false); setPanel(false);
    });
  }

  /* ─────────────────────── 10. КУРСОР ─────────────────────── */

  function initCursor() {
    var cur = $('#cur');
    if (!cur || !fine || reduce) return;
    var ring = $('.cur__ring', cur), dot = $('.cur__dot', cur), txt = $('.cur__txt', cur);
    var tx = innerWidth / 2, ty = innerHeight / 2, cx = tx, cy = ty;
    root.classList.add('has-cur');

    on(doc, 'mousemove', function (e) { tx = e.clientX; ty = e.clientY; cur.style.opacity = '1'; });
    doc.addEventListener('mousedown', function () { cur.classList.add('is-down'); });
    doc.addEventListener('mouseup', function () { cur.classList.remove('is-down'); });
    doc.addEventListener('mouseleave', function () { cur.style.opacity = '0'; });

    (function loop() {
      cx += (tx - cx) * 0.18; cy += (ty - cy) * 0.18;
      ring.style.transform = 'translate3d(' + cx + 'px,' + cy + 'px,0)';
      dot.style.transform = 'translate3d(' + tx + 'px,' + ty + 'px,0)';
      raf(loop);
    })();

    var hit = 'a,button,[data-cur],.roll,.pin__dot';
    doc.addEventListener('mouseover', function (e) {
      var el = e.target.closest && e.target.closest(hit);
      if (!el) return;
      var label = el.getAttribute && el.getAttribute('data-cur');
      if (label) { txt.textContent = label; cur.classList.add('is-label'); cur.classList.remove('is-link'); }
      else if (el.tagName === 'A' || el.tagName === 'BUTTON') { cur.classList.add('is-link'); cur.classList.remove('is-label'); }
    });
    doc.addEventListener('mouseout', function (e) {
      var el = e.target.closest && e.target.closest(hit);
      if (el) cur.classList.remove('is-link', 'is-label');
    });
  }

  /* ─────────── 11. ПРОГРЕСС И РЕЛЬС РАЗДЕЛОВ ─────────── */

  function initProgress() {
    var bar = $('#progressBar');
    var dots = $$('[data-jump]');
    var sections = dots.map(function (d) { return doc.querySelector(d.getAttribute('data-jump')); });

    var ticking = false;
    function paint() {
      var y = window.scrollY || window.pageYOffset;
      var max = doc.documentElement.scrollHeight - window.innerHeight;
      var p = max > 0 ? y / max : 0;
      root.style.setProperty('--scroll', p.toFixed(4));
      if (bar) bar.style.transform = 'scaleX(' + p.toFixed(4) + ')';

      // активная точка рельса
      var idx = 0;
      sections.forEach(function (s, i) {
        if (s && s.getBoundingClientRect().top <= window.innerHeight * 0.42) idx = i;
      });
      dots.forEach(function (d, i) { d.classList.toggle('is-on', i === idx); });
      ticking = false;
    }
    function req() { if (!ticking) { ticking = true; raf(paint); } }
    on(window, 'scroll', req);
    window.addEventListener('resize', req);
    paint();

    dots.forEach(function (d) {
      d.addEventListener('click', function (e) {
        var t = doc.querySelector(d.getAttribute('data-jump'));
        if (!t) return;
        e.preventDefault();
        var yy = t.getBoundingClientRect().top + window.scrollY - 70;
        window.scrollTo({ top: yy, behavior: reduce ? 'auto' : 'smooth' });
      });
    });
  }

  /* ─────────── 12. ЛЕНТА: ПЕРЕТАСКИВАНИЕ МЫШЬЮ ─────────── */

  function initStrips() {
    $$('.film__strip, .vault__strip, [data-strip]').forEach(function (strip) {
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
        strip.addEventListener(ev, function () { down = false; strip.classList.remove('is-drag'); });
      });
      // не даём «клику» сработать после перетаскивания
      strip.addEventListener('click', function (e) {
        if (moved > 8) { e.preventDefault(); e.stopPropagation(); }
      }, true);

      // колесо мыши по горизонтали, только при зажатом Shift — иначе крадём прокрутку
      strip.addEventListener('wheel', function (e) {
        if (!e.shiftKey) return;
        strip.scrollLeft += e.deltaY;
        e.preventDefault();
      }, { passive: false });
    });
  }

  /* ─────────── 13. БЕГУЩАЯ СТРОКА ─────────── */

  function initMarquee() {
    $$('.mq').forEach(function (box) {
      var track = $('.mq__track', box);
      if (!track) return;
      // дублируем содержимое, чтобы шов не читался
      if (!track.dataset.duped) {
        track.innerHTML += track.innerHTML;
        track.dataset.duped = '1';
      }
      if (reduce) return;

      var last = window.scrollY, skew = 0, raf_ = false;
      function paint() {
        var y = window.scrollY;
        var v = y - last; last = y;
        skew += ((clamp(v * -0.25, -6, 6)) - skew) * 0.18;
        box.style.transform = 'skewX(' + skew.toFixed(2) + 'deg)';
        if (Math.abs(skew) > 0.02 || Math.abs(v) > 0) raf_ = raf(paint);
        else { raf_ = false; box.style.transform = 'skewX(0deg)'; }
      }
      on(window, 'scroll', function () { if (!raf_) raf_ = raf(paint); });
    });
  }

  /* ─────────── 13. ПОИСК (палитра) ─────────── */

  function initSearch() {
    var pal = $('#palette');
    var openers = $$('[data-search-open]');
    if (!pal || !openers.length) return;

    var input = $('#paletteInput'), res = $('#paletteRes');
    var index = null, sel = -1, loading = false;

    function load() {
      if (index || loading) return Promise.resolve();
      loading = true;
      var src = pal.getAttribute('data-index') || 'search-index.json';
      return fetch(src).then(function (r) { return r.ok ? r.json() : []; })
        .then(function (d) { index = Array.isArray(d) ? d : []; })
        .catch(function () { index = []; });
    }
    function open() {
      pal.classList.add('is-open'); doc.body.classList.add('is-locked');
      load().then(function () { render(input.value); });
      setTimeout(function () { input.focus(); input.select(); }, 60);
    }
    function close() { pal.classList.remove('is-open'); doc.body.classList.remove('is-locked'); }
    function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]; }); }

    function render(q) {
      q = (q || '').trim().toLowerCase();
      if (!index) { res.innerHTML = '<div class="pal__empty">Yüklənir…</div>'; return; }
      var hits = index.filter(function (it) {
        if (!q) return true;
        return (it.title + ' ' + (it.text || '') + ' ' + (it.sub || '')).toLowerCase().indexOf(q) > -1;
      }).slice(0, 40);
      if (!hits.length) { res.innerHTML = '<div class="pal__empty">Heç nə tapılmadı.</div>'; sel = -1; return; }
      res.innerHTML = hits.map(function (it) {
        var t = esc(it.title || it.page || '');
        if (q) { try { t = t.replace(new RegExp('(' + q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'ig'), '<mark>$1</mark>'); } catch (e) {} }
        return '<a href="' + esc(it.url || '#') + '"><div class="pal__t">' + t + '</div><div class="pal__s">' +
               esc(it.sub || '') + (it.text ? ' · ' + esc(it.text.slice(0, 92)) : '') + '</div></a>';
      }).join('');
      sel = -1;
    }

    openers.forEach(function (b) { b.addEventListener('click', function (e) { e.preventDefault(); open(); }); });
    pal.addEventListener('click', function (e) { if (e.target === pal) close(); });
    input.addEventListener('input', function () { render(input.value); });

    doc.addEventListener('keydown', function (e) {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); open(); return; }
      if (e.key === '/' && !pal.classList.contains('is-open') && !/^(INPUT|TEXTAREA)$/.test(doc.activeElement.tagName)) { e.preventDefault(); open(); return; }
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
      if (e.key === 'Enter' && sel > -1) location.href = links[sel].getAttribute('href');
    });
  }

  /* ─────────── 14. МЕЛОЧИ ─────────── */

  function initMisc() {
    // плавные якоря
    if (!reduce) {
      doc.addEventListener('click', function (e) {
        var a = e.target.closest && e.target.closest('a[href^="#"]');
        if (!a) return;
        var id = a.getAttribute('href');
        if (id === '#' || id.length < 2) return;
        var t = doc.querySelector(id);
        if (!t) return;
        e.preventDefault();
        window.scrollTo({ top: t.getBoundingClientRect().top + window.scrollY - 70, behavior: 'smooth' });
      });
    }

    // кнопка наверх
    var top = $('#toTop');
    if (top) {
      on(window, 'scroll', function () { top.classList.toggle('is-on', window.scrollY > 800); });
      top.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }); });
    }

    // залипающая шапка: прячем при прокрутке вниз
    var hdr = $('#hdr');
    if (hdr) {
      var last = 0, t = false;
      function paint() {
        var y = window.scrollY;
        hdr.classList.toggle('is-stuck', y > 30);
        if (y > 480 && y > last + 4) hdr.classList.add('is-hidden');
        else if (y < last - 4 || y < 480) hdr.classList.remove('is-hidden');
        last = y; t = false;
      }
      on(window, 'scroll', function () { if (!t) { t = true; raf(paint); } });
      paint();
    }
  }

  /* ─────────────────────── СТАРТ ─────────────────────── */

  function boot() {
    initTheme();
    initMotionToggle();
    initReveal();
    initLines();
    initMask();
    initPin();
    initPinX();
    initParallax();
    initCounters();
    initScramble();
    initMenu();
    initCursor();
    initProgress();
    initStrips();
    initMarquee();
    initSearch();
    initMisc();
    root.classList.add('is-ready');
  }

  if (doc.readyState === 'loading') doc.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
