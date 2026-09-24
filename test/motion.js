/* =====================================================================
   RAGIMOFF · test/motion.js
   Ядро: тема, режим движения, меню, покадровые галереи (data-seq),
   reveal, счётчики, параллакс, курсор-превью, прогресс, маркиза.
   Базис: x2motion.js (v7–v9) + починки:
     ① читается data-seq-step (раньше всегда был фолбэк),
     ② прогресс умеет и scaleX, и scaleY (v8 горизонтальный),
     ③ на мобильной хроника становится статичным списком кадров,
     ④ маркиза клонится вручную (без CSS-дубля).
   Принцип x2-движка: обработчики навешиваются ВСЕГДА, а видимость
   эффектов решают классы html.mo / html.no-mo.
   ===================================================================== */
(function () {
  'use strict';

  var root = document.documentElement;
  var reduceQ = window.matchMedia('(prefers-reduced-motion: reduce)');
  var THEME_KEY = root.getAttribute('data-theme-key') || 'ragimoff-theme';
  var MOTION_KEY = root.getAttribute('data-motion-key') || 'ragimoff-motion';
  var reduce = false;

  function lsGet(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function lsSet(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  function $(s, c) { return (c || document).querySelector(s); }
  function $$(s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); }
  function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }

  /* ─────────────────────────────── ТЕМА ─────────────────────────────── */
  var theme = lsGet(THEME_KEY) || root.getAttribute('data-theme-default') || 'dark';

  function paintTheme(t) {
    root.setAttribute('data-theme', t);
    var meta = $('meta[name="theme-color"]');
    if (meta) {
      meta.setAttribute('content',
        t === 'dark'
          ? (root.getAttribute('data-tc-dark') || '#0A0F18')
          : (root.getAttribute('data-tc-light') || '#F4F0E8'));
    }
    $$('[data-theme-toggle]').forEach(function (b) {
      b.setAttribute('aria-pressed', t === 'dark' ? 'false' : 'true');
      var l = $('[data-theme-label]', b);
      if (l) l.textContent = t === 'dark'
        ? (b.getAttribute('data-label-to-light') || 'İşıq rejimi')
        : (b.getAttribute('data-label-to-dark') || 'Qaranlıq rejim');
    });
  }

  function setTheme(t, ev) {
    if (t === root.getAttribute('data-theme')) return;
    lsSet(THEME_KEY, t);
    var x = innerWidth - 48, y = 40, r = Math.hypot(innerWidth, innerHeight);
    if (ev && ev.currentTarget && ev.currentTarget.getBoundingClientRect) {
      var b = ev.currentTarget.getBoundingClientRect();
      x = b.left + b.width / 2;
      y = b.top + b.height / 2;
      r = Math.hypot(Math.max(x, innerWidth - x), Math.max(y, innerHeight - y));
    }
    var ok = !reduce && document.startViewTransition &&
      window.CSS && CSS.supports && CSS.supports('view-transition-name', 'root');
    if (!ok) { paintTheme(t); return; }
    var vt = document.startViewTransition(function () { paintTheme(t); });
    vt.ready.then(function () {
      root.animate(
        { clipPath: ['circle(0px at ' + x + 'px ' + y + 'px)',
                     'circle(' + r + 'px at ' + x + 'px ' + y + 'px)'] },
        { duration: 640, easing: 'cubic-bezier(.625,.05,0,1)',
          pseudoElement: '::view-transition-new(root)' }
      );
    }).catch(function () {});
  }

  /* ────────────────────────── РЕЖИМ ДВИЖЕНИЯ ───────────────────────── */
  function computeReduce() {
    var p = lsGet(MOTION_KEY);
    if (p === 'on') return false;
    if (p === 'off') return true;
    return reduceQ.matches;
  }
  function paintMotion() {
    root.classList.toggle('mo', !reduce);
    root.classList.toggle('no-mo', reduce);
    root.setAttribute('data-motion', reduce ? 'off' : 'on');
    $$('[data-motion-toggle]').forEach(function (b) {
      b.setAttribute('aria-pressed', reduce ? 'false' : 'true');
      var l = $('[data-motion-label]', b);
      if (l) l.textContent = reduce
        ? (b.getAttribute('data-label-on') || 'Hərəkəti yandır')
        : (b.getAttribute('data-label-off') || 'Hərəkəti söndür');
    });
  }

  /* ───────────────────────── МЕНЮ ───────────────────────── */
  var menuOpen = false;
  function setMenu(open) {
    var m = $('[data-menu]');
    if (!m) return;
    menuOpen = open;
    m.classList.toggle('is-open', open);
    m.setAttribute('aria-hidden', open ? 'false' : 'true');
    root.classList.toggle('menu-lock', open);
    $$('[data-menu-toggle]').forEach(function (b) { b.setAttribute('aria-expanded', open ? 'true' : 'false'); });
    if (open) {
      var f = m.querySelector('a, button');
      if (f) setTimeout(function () { f.focus(); }, 60);
    }
  }

  /* ───────────────────── ПОСЛЕДОВАТЕЛЬНАЯ ГАЛЕРЕЯ ───────────────────── */
  var seqs = [];
  function collectSeqs() {
    var narrow = innerWidth <= 720;
    seqs = $$('[data-seq]').map(function (el) {
      var items = $$('[data-seq-item]', el);
      var idxRoot = el.closest('[data-seq-root]') || el;
      el.style.setProperty('--seq-n', items.length);
      /* ① шаг сцены читается из разметки */
      var stepAttr = el.getAttribute('data-seq-step');
      if (stepAttr) el.style.setProperty('--seq-step', stepAttr);
      /* ③ на телефоне хроника — обычный стоп-список кадров */
      el.classList.toggle('is-static', narrow);
      return {
        el: el, items: items, n: items.length || 1, static: narrow,
        num: $('[data-seq-num]', el),
        cap: $('[data-seq-cap]', el),
        bar: $('[data-seq-bar] i, [data-seq-bar]', el),
        idx: $$('[data-seq-idx]', idxRoot)
      };
    });
  }
  function runSeq() {
    for (var s = 0; s < seqs.length; s++) {
      var q = seqs[s], r = q.el.getBoundingClientRect();
      if (r.bottom < -200 || r.top > innerHeight + 200) continue;

      if (reduce || q.static) {
        for (var j = 0; j < q.n; j++) q.items[j].style.removeProperty('--o');
        q.items.forEach(function (it) { it.classList.remove('is-live'); });
        if (q.idx) q.idx.forEach(function (it) { it.classList.remove('is-live'); });
        if (q.bar) q.bar.style.transform = '';
        if (q.num && q.num.textContent !== '01/' + (q.n < 10 ? '0' + q.n : q.n)) {
          q.num.textContent = '01/' + (q.n < 10 ? '0' + q.n : q.n);
        }
        continue;
      }

      var span = q.el.offsetHeight - innerHeight;
      if (span <= 1) span = 1;
      var p = clamp(-r.top / span, 0, 1);
      var head = p * q.n;
      var live = Math.min(q.n - 1, Math.floor(head));
      q.el.style.setProperty('--seq-p', p.toFixed(4));
      if (q.bar) q.bar.style.transform = 'scaleX(' + p.toFixed(4) + ')';

      for (var i = 0; i < q.n; i++) {
        var o = clamp((head - i) / 0.62, 0, 1);
        var on = r.top < innerHeight * 0.62 && r.bottom > innerHeight * 0.25;
        q.items[i].style.setProperty('--o', o.toFixed(3));
        q.items[i].classList.toggle('is-live', on && i === live);
      }
      if (q.num) {
        var t = String(live + 1);
        if (t.length < 2) t = '0' + t;
        t = t + '/' + (q.n < 10 ? '0' + q.n : q.n);
        if (q.num.textContent !== t) q.num.textContent = t;
      }
      if (q.idx && q.idx.length) {
        for (var k2 = 0; k2 < q.idx.length; k2++) {
          q.idx[k2].classList.toggle('is-live', k2 === live);
        }
      }
      if (q.cap) {
        var c = q.items[live] && q.items[live].getAttribute('data-cap');
        if (c && q.cap.textContent !== c) {
          q.cap.classList.add('is-out');
          (function (node, txt) {
            setTimeout(function () { node.textContent = txt; node.classList.remove('is-out'); }, reduce ? 0 : 180);
          })(q.cap, c);
        }
      }
    }
  }

  /* ───────────────────────── REVEAL ───────────────────────── */
  var rvIO = null;
  function initReveal() {
    var nodes = $$('[data-rv]');
    if (!nodes.length) return;
    if (!('IntersectionObserver' in window)) {
      nodes.forEach(function (n) { n.classList.add('in'); });
      return;
    }
    rvIO = new IntersectionObserver(function (ents) {
      ents.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add('in');
          rvIO.unobserve(e.target);
        }
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.08 });
    nodes.forEach(function (n) {
      var d = n.getAttribute('data-stagger');
      if (d) n.style.setProperty('--delay', d + 'ms');
      rvIO.observe(n);
    });
  }

  /* ──────────────────────── СЧЁТЧИКИ ──────────────────────── */
  var cntIO = null;
  function initCounts() {
    var nodes = $$('[data-count]');
    if (!nodes.length || !('IntersectionObserver' in window)) return;
    cntIO = new IntersectionObserver(function (ents) {
      ents.forEach(function (e) {
        if (!e.isIntersecting) return;
        var el = e.target;
        cntIO.unobserve(el);
        var to = parseFloat(el.getAttribute('data-count')) || 0;
        if (reduce) { el.textContent = el.getAttribute('data-count-final') || to; return; }
        var t0 = 0, dur = 1400;
        function step(ts) {
          if (!t0) t0 = ts;
          var k = clamp((ts - t0) / dur, 0, 1);
          var e2 = 1 - Math.pow(1 - k, 3);
          var val = Math.round(to * e2);
          el.textContent = val >= 1000 ? val.toLocaleString('az') : String(val);
          if (k < 1) requestAnimationFrame(step);
          else el.textContent = el.getAttribute('data-count-final') || String(to);
        }
        requestAnimationFrame(step);
      });
    }, { threshold: 0.4 });
    nodes.forEach(function (n) { cntIO.observe(n); });
  }

  /* ───────────────────────── ПАРАЛЛАКС ───────────────────────── */
  var plx = [];
  function collectPlx() {
    plx = $$('[data-plx]').map(function (el) {
      return { el: el, k: parseFloat(el.getAttribute('data-plx')) || 0.05 };
    });
  }
  function runPlx() {
    if (reduce) return;
    var h = innerHeight;
    for (var i = 0; i < plx.length; i++) {
      var r = plx[i].el.getBoundingClientRect();
      if (r.bottom < -100 || r.top > h + 100) continue;
      var mid = r.top + r.height / 2 - h / 2;
      plx[i].el.style.setProperty('--plx', (-mid * plx[i].k).toFixed(1) + 'px');
    }
  }

  /* ──────────────────────── КУРСОР-ПРЕВЬЮ ───────────────────────── */
  var peek = null, peekX = 0, peekY = 0, peekTX = 0, peekTY = 0, peekRaf = 0;
  function initPeek() {
    var host = $('[data-peek-host]');
    if (!host) return;
    peek = document.createElement('div');
    peek.className = 'peek';
    peek.setAttribute('aria-hidden', 'true');
    peek.innerHTML = '<span class="peek__img"></span>';
    host.appendChild(peek);
    var imgNode = $('.peek__img', peek);

    $$('[data-img]', host).forEach(function (row) {
      function show() {
        var src = row.getAttribute('data-img');
        if (src) imgNode.style.backgroundImage = 'url("' + src + '")';
        peek.classList.add('is-on');
        row.classList.add('is-hot');
      }
      function hide() {
        peek.classList.remove('is-on');
        row.classList.remove('is-hot');
      }
      row.addEventListener('mouseenter', show);
      row.addEventListener('mouseleave', hide);
      row.addEventListener('focus', show);
      row.addEventListener('blur', hide);
    });

    host.addEventListener('mousemove', function (e) {
      var b = host.getBoundingClientRect();
      peekTX = e.clientX - b.left;
      peekTY = e.clientY - b.top;
      if (!peekRaf) peekRaf = requestAnimationFrame(peekTick);
    });
    host.addEventListener('mouseleave', function () { if (peek) peek.classList.remove('is-on'); });

    function peekTick() {
      var k = reduce ? 1 : 0.16;
      peekX += (peekTX - peekX) * k;
      peekY += (peekTY - peekY) * k;
      peek.style.transform = 'translate3d(' + peekX.toFixed(1) + 'px,' + peekY.toFixed(1) + 'px,0)';
      if (Math.abs(peekTX - peekX) > 0.4 || Math.abs(peekTY - peekY) > 0.4) {
        peekRaf = requestAnimationFrame(peekTick);
      } else { peekRaf = 0; }
    }
  }

  /* ──────────────────────── МАРКИЗА (наклон от скорости) ───────────── */
  var mqTrack = null;
  function prepMarquee() {
    mqTrack = $('.mq__track');
    if (!mqTrack) return;
    /* ④ клон содержимого для бесшовного цикла */
    mqTrack.innerHTML += mqTrack.innerHTML;
  }

  /* ───────────────────────── ПРОКРУТКА ───────────────────────── */
  var bar = null, header = null, lastY = 0;
  function runScroll() {
    var y = window.pageYOffset || root.scrollTop;
    if (bar) {
      var max = root.scrollHeight - innerHeight;
      /* ② orient=h → scaleX, иначе scaleY (вертикальная полоса справа) */
      var horiz = bar.getAttribute('data-progress') === 'h';
      var t = max > 0 ? clamp(y / max, 0, 1) : 0;
      var target = bar.matches('i') ? bar : (bar.querySelector('i') || bar);
      target.style.transform = horiz ? 'scaleX(' + t.toFixed(4) + ')' : 'scaleY(' + t.toFixed(4) + ')';
    }
    if (header) header.classList.toggle('is-stuck', y > 40);

    /* маркиза-склон: ~±0.6deg пропорционально скорости (+ едва заметный стоп) */
    if (mqTrack) {
      var v = clamp((y - lastY) / 24, -3, 3);
      mqTrack.style.setProperty('--mq-skew', (v * 0.2).toFixed(2) + 'deg');
    }
    lastY = y;

    runSeq();
    runPlx();
  }
  function onScroll() {
    if (onScroll.q) return;
    onScroll.q = true;
    requestAnimationFrame(function () {
      onScroll.q = false;
      runScroll();
    });
  }

  /* ───────────────────────── СТАРТ ───────────────────────── */
  function bind() {
    $$('[data-theme-toggle]').forEach(function (b) {
      b.addEventListener('click', function (e) {
        setTheme(root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark', e);
      });
    });
    $$('[data-motion-toggle]').forEach(function (b) {
      b.addEventListener('click', function () {
        reduce = !reduce;
        lsSet(MOTION_KEY, reduce ? 'off' : 'on');
        paintMotion();
        if (!reduce) requestAnimationFrame(runScroll);
        b.blur();
      });
    });
    $$('[data-menu-toggle]').forEach(function (b) {
      b.addEventListener('click', function () { setMenu(!menuOpen); });
    });
    var close = $('[data-menu-close]');
    if (close) close.addEventListener('click', function () { setMenu(false); });
    $$('[data-menu] a').forEach(function (a) {
      a.addEventListener('click', function () { setMenu(false); });
    });
    document.addEventListener('keydown', function (e) {
      var tag = (e.target.tagName || '').toLowerCase();
      var typing = tag === 'input' || tag === 'textarea' || e.target.isContentEditable;
      if (e.key === 'Escape' && menuOpen) { setMenu(false); return; }
      if (typing) return;
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'j') {
        e.preventDefault();
        setTheme(root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
      }
    });
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', function () {
      collectSeqs(); collectPlx();
      onScroll();
    });
    reduceQ.addEventListener && reduceQ.addEventListener('change', function () {
      if (!lsGet(MOTION_KEY)) { reduce = computeReduce(); paintMotion(); onScroll(); }
    });
  }

  function boot() {
    reduce = computeReduce();
    paintTheme(theme);
    paintMotion();
    if (root.getAttribute('data-theme-default') !== theme) lsSet(THEME_KEY, theme);

    /* Прогресс-полосы: [data-progress="h"] — верх, .prog--v i — правая вертикаль */
    bar = $('[data-progress]') || $('.prog--v i');

    header = $('[data-header]');

    bind();
    prepMarquee();
    collectSeqs();
    collectPlx();
    initReveal();
    initCounts();
    initPeek();

    root.classList.add('js-ready');
    var heroEl = document.querySelector('.hero');
    if (heroEl) {
      if (reduce) { heroEl.classList.add('is-in'); }
      else {
        requestAnimationFrame(function () {
          setTimeout(function () { heroEl.classList.add('is-in'); }, 60);
        });
      }
    }
    requestAnimationFrame(function () { onScroll(); });
    setTimeout(onScroll, 240);
    window.addEventListener('load', onScroll);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else { boot(); }
})();