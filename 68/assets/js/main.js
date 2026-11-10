/* RAGIMOFF · 67 — interactions (no dependencies) */
(function () {
  'use strict';
  var root = document.documentElement;

  /* theme */
  var saved = null;
  try { saved = localStorage.getItem('rgm67-theme'); } catch (e) {}
  if (saved) root.setAttribute('data-theme', saved);
  document.querySelectorAll('[data-theme-toggle]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('rgm67-theme', next); } catch (e) {}
    });
  });

  /* mobile menu */
  var burger = document.querySelector('[data-burger]');
  var mob = document.querySelector('[data-mob]');
  if (burger && mob) {
    burger.addEventListener('click', function () {
      var open = mob.classList.toggle('is-open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      document.body.classList.toggle('is-locked', open);
    });
    mob.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        mob.classList.remove('is-open');
        burger.setAttribute('aria-expanded', 'false');
        document.body.classList.remove('is-locked');
      });
    });
  }

  /* header hide on scroll down */
  var head = document.querySelector('[data-head]');
  var lastY = 0;
  window.addEventListener('scroll', function () {
    var y = window.scrollY;
    if (head) {
      head.classList.toggle('is-scrolled', y > 24);
      if (y > 160 && y > lastY + 6) head.classList.add('is-hidden');
      else if (y < lastY - 6) head.classList.remove('is-hidden');
    }
    lastY = y;
  }, { passive: true });

  /* reveal — отметка ниже: надёжный движок на scroll+rAF (IO в некоторых
     движках/встройках не срабатывает при программной прокрутке) */

  /* counters */
  document.querySelectorAll('[data-count]').forEach(function (el) {
    var target = parseFloat(el.getAttribute('data-count'));
    var suffix = el.getAttribute('data-suffix') || '';
    var done = false;
    function run() {
      if (done) return; done = true;
      var start = performance.now(), dur = 1200;
      function tick(now) {
        var p = Math.min(1, (now - start) / dur);
        var v = Math.round(target * (1 - Math.pow(1 - p, 3)));
        el.textContent = v + suffix;
        if (p < 1) requestAnimationFrame(tick);
      }
      requestAnimationFrame(tick);
    }
    if ('IntersectionObserver' in window) {
      var o = new IntersectionObserver(function (e) {
        if (e[0].isIntersecting) { run(); o.disconnect(); }
      }, { threshold: 0.4 });
      o.observe(el);
    } else { run(); }
  });

  /* lazy video: poster -> iframe on click */
  document.querySelectorAll('[data-video]').forEach(function (box) {
    box.addEventListener('click', function () {
      var id = box.getAttribute('data-video');
      var iframe = document.createElement('iframe');
      iframe.src = 'https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0';
      iframe.title = box.getAttribute('data-title') || 'Video';
      iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
      iframe.allowFullscreen = true;
      box.innerHTML = '';
      box.appendChild(iframe);
    });
  });

  /* year */
  document.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  /* ────────────────────────────────────────────────────────────
     ПЕРВЫЙ ЭКРАН — СКРАБ КАДРОВ ВИДЕО ПО СКРОЛЛУ
     Взято из Ноктюрна (_tools/nocturne, nocturne.js 172–256).
     Позиция кадров тянется к позиции скролла с затуханием,
     соседние кадры кросс-фейдятся — движение как у видео.
     На «касании» появляется поисковая строка, в неё печатается
     имя, затем посимвольно выдаётся заголовок.
     ──────────────────────────────────────────────────────────── */
  const cine = document.querySelector('[data-cine]');
  if (cine) (function () {
    const frame = cine.querySelector('.cine__frame');
    const stick = cine.querySelector('.cine__stick');
    const cv = cine.querySelector('.cine__cv');
    const img = cine.querySelector('.cine__img');
    const sq = cine.querySelector('.cine__search');
    const q = cine.querySelector('.cine__q');
    const mob = window.matchMedia('(max-width: 700px)');
    if (!frame || !cv || !cv.getContext) return;
    const N = +frame.getAttribute('data-frames') || 0;
    if (!N) return;

    const ctx = cv.getContext('2d');
    let imgs = [], set = '', target = 0, shown = 0, raf = 0, title = false;
    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const QTXT = q ? (q.getAttribute('data-q') || '') : '';
    const M = (frame.getAttribute('data-marks') || '19,23,23,35,37').split(',').map(Number);
    const T = { video: .78, sqIn: [M[0], M[1]], type: [M[2], M[3]], title: M[4], out: [.9, 1] };

    const clamp = v => v < 0 ? 0 : v > 1 ? 1 : v;
    const seg = (v, a, b) => clamp((v - a) / (b - a));
    const ok = im => im && im.complete && im.naturalWidth;

    function near(i) {
      for (let d = 0; d < N; d++) {
        if (ok(imgs[i - d])) return imgs[i - d];
        if (ok(imgs[i + d])) return imgs[i + d];
      }
      return null;
    }

    let lastPainted = -1;
    function paint(force) {
      const i = Math.floor(shown), f = shown - i;
      const key = Math.round(shown * 20);
      if (!force && key === lastPainted) return;
      lastPainted = key;
      const a = ok(imgs[i]) ? imgs[i] : near(i);
      const b = ok(imgs[i + 1]) ? imgs[i + 1] : null;
      if (!a) return;
      ctx.globalAlpha = 1;
      ctx.drawImage(a, 0, 0, cv.width, cv.height);
      if (b && f > .04) {
        ctx.globalAlpha = f;
        ctx.drawImage(b, 0, 0, cv.width, cv.height);
        ctx.globalAlpha = 1;
      }
      if (img && img.style.opacity !== '0') img.style.opacity = '0';
    }

    function size() {
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      const w = frame.offsetWidth, h = frame.offsetHeight;
      cv.width = Math.round(w * dpr);
      cv.height = Math.round(h * dpr);
      paint(true);
    }

    function load() {
      const want = mob.matches ? 'm' : 'd';
      if (want === set) return;
      set = want;
      imgs = [];
      const src = frame.getAttribute(want === 'm' ? 'data-msrc' : 'data-fsrc');
      /* первые кадры и каждый 8-й — сразу, остальные после: скраб работает мгновенно и дозаполняется */
      const order = [];
      for (let i = 0; i < N; i += 8) order.push(i);
      for (let i = 0; i < N; i++) if (i % 8) order.push(i);
      order.forEach(function (i, n) {
        const im = new Image();
        im.decoding = 'async';
        im.onload = function () { if (Math.abs(i - shown) < 2) paint(true); };
        setTimeout(function () {
          im.src = src.replace('{i}', ('00' + i).slice(-3));
        }, n < 24 ? 0 : 30 + n * 6);
        imgs[i] = im;
      });
      frame.classList.add('has-frames');
      size();
    }

    /* Прод: cine — сам скролл-контейнер (position: sticky внутри него).
       scrollP() идёт от верха секции, без вычитания высоты панели. */
    function scrollP() {
      const r = cine.getBoundingClientRect();
      const total = cine.offsetHeight - window.innerHeight;
      return clamp(-r.top / (total || 1));
    }

    function overlay(p) {
      const k = shown;
      if (sq) sq.style.setProperty('--sq', (seg(k, T.sqIn[0], T.sqIn[1]) * (title ? 0 : 1)).toFixed(3));
      if (q) {
        const n = Math.round(seg(k, T.type[0], T.type[1]) * QTXT.length);
        if (q.textContent.length !== n) q.textContent = QTXT.slice(0, n);
      }
      const on = k >= T.title;
      if (on !== title) {
        title = on;
        cine.classList.toggle('is-title', on);
        if (sq) sq.style.setProperty('--sq', on ? '0' : '1');
      }
      if (stick) {
        stick.style.setProperty('--sh', (.15 + .7 * seg(k, T.sqIn[0], T.title + 4)).toFixed(3));
        stick.style.setProperty('--t2', seg(p, .02, .08).toFixed(3));
        stick.style.setProperty('--out', seg(p, T.out[0], T.out[1]).toFixed(3));
      }
    }

    function loop() {
      raf = 0;
      const d = target - shown;
      shown = Math.abs(d) < .02 ? target : shown + d * (reduce ? 1 : .14);
      paint(false);
      overlay(scrollP());
      if (shown !== target) raf = requestAnimationFrame(loop);
    }

    function onScroll() {
      target = seg(scrollP(), 0, T.video) * (N - 1);
      if (!raf) raf = requestAnimationFrame(loop);
    }

    /* Страховка от «голого» скролла: если rAF не тикает (часть встроенных браузеров),
       догоняем позицию прямым вызовом. В нормальном браузере ветка не срабатывает. */
    let lastLoopAt = 0;
    function watchdog() {
      if (shown !== target && Date.now() - lastLoopAt > 400) {
        shown = Math.abs(target - shown) < .02 ? target : shown + (target - shown) * .5;
        paint(true);
        overlay(scrollP());
      }
      lastLoopAt = Date.now();
    }
    setInterval(watchdog, 500);

    mob.addEventListener('change', function () { load(); size(); onScroll(); });
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', function () { load(); size(); onScroll(); });
    load();
    onScroll();
  })();

  /* ────────────────────────────────────────────────────────────
     SPLIT-TEXT: заголовки секций раскрываются по скроллу.
     Каждое слово — в маске, выезжает снизу с задержкой по порядку.
     Замысел: сайт «раскрывается» и рассказывает, а не выдаёт
     сухую стену текста.
     ──────────────────────────────────────────────────────────── */
  const stHeads = document.querySelectorAll('.sec-head h2, h2.st');
  stHeads.forEach(function (h) {
    if (h.dataset.st) return;
    h.dataset.st = '1';
    const words = h.textContent.trim().split(/\s+/).filter(Boolean);
    if (words.length < 2) return;
    h.textContent = '';
    words.forEach(function (w, i) {
      const outer = document.createElement('span');
      outer.className = 'st-w';
      const inner = document.createElement('i');
      inner.textContent = w;
      inner.style.transitionDelay = (i * 0.055).toFixed(3) + 's';
      outer.appendChild(inner);
      h.appendChild(outer);
      if (i < words.length - 1) h.appendChild(document.createTextNode(' '));
    });
    h.classList.add('st');
  });
  /* ЗАПУСК ПОЯВЛЕНИЙ: без rAF и без IntersectionObserver.
     Оба механизма отказывают в части движков (IO не ловит программную прокрутку,
     rAF не тикает в некоторых встроенных браузерах). Поэтому: прямой вызов по
     scroll с частотным ограничением + страховочный интервал, который останавливается,
     как только очередь опустела. Прошедшие элементы из списка убираются, поэтому
     каждый проход стоит почти ничего. */
  const pending = Array.prototype.slice.call(document.querySelectorAll('.reveal, h2.st'));
  let lastCheck = 0;
  function checkReveal() {
    const vh = window.innerHeight || document.documentElement.clientHeight;
    for (let i = pending.length - 1; i >= 0; i--) {
      const el = pending[i];
      const r = el.getBoundingClientRect();
      if (r.top < vh * 0.88 && r.bottom > 0) {
        el.classList.add('is-in');
        pending.splice(i, 1);
      }
    }
    return pending.length;
  }
  function queueReveal() {
    const now = Date.now();
    if (now - lastCheck < 60) return;
    lastCheck = now;
    checkReveal();
  }
  window.addEventListener('scroll', queueReveal, { passive: true });
  window.addEventListener('resize', queueReveal);
  window.addEventListener('load', checkReveal);
  checkReveal();
  const _revealTick = setInterval(function () {
    if (checkReveal() === 0) clearInterval(_revealTick);
  }, 350);
})();
