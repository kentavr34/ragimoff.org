/* RAGIMOFF · «Ноктюрн» — интерфейс: шапка, меню, язык, свет за курсором, появление блоков.
   Формы, оплата и галереи остаются за shared.js / training-pay.js (копии с боевого сайта). */
(function () {
  'use strict';
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches && !window.RGM_FORCE_MOTION;
  var head = document.getElementById('nHead');
  var burger = document.querySelector('.n-burger');
  var mob = document.getElementById('nMob');

  /* header: solid after scroll, hides on scroll down, returns on scroll up */
  var lastY = 0;
  function onScroll() {
    var y = window.scrollY || 0;
    if (head) {
      head.classList.toggle('is-scrolled', y > 30);
      var menuOpen = mob && mob.classList.contains('is-open');
      head.classList.toggle('is-hidden', !menuOpen && y > 400 && y > lastY + 4);
      if (y < lastY - 4) head.classList.remove('is-hidden');
    }
    lastY = y;
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* mobile menu */
  function setMenu(open) {
    if (!mob || !burger) return;
    mob.classList.toggle('is-open', open);
    mob.setAttribute('aria-hidden', open ? 'false' : 'true');
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    document.documentElement.style.overflow = open ? 'hidden' : '';
  }
  if (burger) burger.addEventListener('click', function () { setMenu(!mob.classList.contains('is-open')); });
  if (mob) mob.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      setMenu(false);
      Array.prototype.forEach.call(document.querySelectorAll('.n-dd.is-open'), function (d) { d.classList.remove('is-open'); });
    }
  });

  /* dropdowns: touch / keyboard — first tap opens, second follows the link */
  Array.prototype.forEach.call(document.querySelectorAll('.n-dd > .n-link'), function (a) {
    a.addEventListener('click', function (e) {
      var dd = a.parentNode;
      if (window.matchMedia('(hover: none)').matches && !dd.classList.contains('is-open')) {
        e.preventDefault();
        Array.prototype.forEach.call(document.querySelectorAll('.n-dd.is-open'), function (d) { d.classList.remove('is-open'); });
        dd.classList.add('is-open');
      }
    });
  });
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.n-dd')) Array.prototype.forEach.call(document.querySelectorAll('.n-dd.is-open'), function (d) { d.classList.remove('is-open'); });
  });

  /* language choice is remembered (the router on /test/nocturne/ uses it) */
  document.addEventListener('click', function (e) {
    var l = e.target.closest && e.target.closest('.n-lang');
    if (l) { try { localStorage.setItem('ragimoff_lang', l.getAttribute('data-lang')); } catch (er) {} }
  });

  /* photo viewer: every gallery shot opens whole, with arrows and Esc */
  var shots = Array.prototype.slice.call(document.querySelectorAll('.n-shot'));
  if (shots.length) {
    var lb = document.createElement('div');
    lb.className = 'n-lb'; lb.setAttribute('role', 'dialog'); lb.setAttribute('aria-modal', 'true');
    lb.innerHTML = '<img alt=""><span class="n-lb-cap"></span><button class="n-lb-x" type="button" aria-label="Close">×</button><button class="n-lb-p" type="button" aria-label="Previous">‹</button><button class="n-lb-n" type="button" aria-label="Next">›</button>';
    document.body.appendChild(lb);
    var lbImg = lb.querySelector('img'), lbCap = lb.querySelector('.n-lb-cap'), cur = 0, group = [];
    function show(i) {
      cur = (i + group.length) % group.length;
      var b = group[cur]; lbImg.src = b.getAttribute('data-full'); lbImg.alt = b.getAttribute('aria-label') || '';
      lbCap.textContent = (b.querySelector('.n-shot-cap') || {}).textContent || '';
    }
    function close() { lb.classList.remove('is-open'); document.documentElement.style.overflow = ''; }
    shots.forEach(function (b) {
      b.addEventListener('click', function () {
        group = Array.prototype.slice.call(b.closest('.n-gallery').querySelectorAll('.n-shot'));
        show(group.indexOf(b)); lb.classList.add('is-open'); document.documentElement.style.overflow = 'hidden';
        lb.querySelector('.n-lb-x').focus();
      });
    });
    lb.querySelector('.n-lb-x').addEventListener('click', close);
    lb.querySelector('.n-lb-p').addEventListener('click', function () { show(cur - 1); });
    lb.querySelector('.n-lb-n').addEventListener('click', function () { show(cur + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
    document.addEventListener('keydown', function (e) {
      if (!lb.classList.contains('is-open')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowLeft') show(cur - 1);
      if (e.key === 'ArrowRight') show(cur + 1);
    });
  }

  /* law cards open / close */
  Array.prototype.forEach.call(document.querySelectorAll('.law-card-head'), function (h) {
    function t() { var c = h.closest('.law-card'); var o = c.classList.toggle('is-open'); h.setAttribute('aria-expanded', o ? 'true' : 'false'); }
    h.addEventListener('click', t);
    h.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); t(); } });
  });

  /* programme strip: drag with the mouse */
  Array.prototype.forEach.call(document.querySelectorAll('.n-strip'), function (st) {
    var down = false, sx = 0, sl = 0, moved = false;
    st.addEventListener('pointerdown', function (e) { if (e.pointerType !== 'mouse') return; down = true; moved = false; sx = e.clientX; sl = st.scrollLeft; });
    window.addEventListener('pointermove', function (e) { if (!down) return; var dx = e.clientX - sx; if (Math.abs(dx) > 4) { moved = true; st.classList.add('is-drag'); } st.scrollLeft = sl - dx; });
    window.addEventListener('pointerup', function () { if (!down) return; down = false; setTimeout(function () { st.classList.remove('is-drag'); }, 0); });
    st.addEventListener('click', function (e) { if (moved) { e.preventDefault(); e.stopPropagation(); moved = false; } }, true);
  });

  /* home first screen — frames of a video driven by the scroll wheel / swipe (forward and back).
     The shown position eases toward the scroll position and neighbouring frames are cross-faded, so it moves like video.
     At the tap a search line appears, the name is typed into it, then the title is written out. */
  var cine = document.querySelector('[data-cine]');
  if (cine) (function () {
    var frame = cine.querySelector('.n-cine-frame'), stick = cine.querySelector('.n-cine-stick'), cv = cine.querySelector('.n-cine-cv');
    var img = cine.querySelector('.n-cine-img'), sq = cine.querySelector('.n-cine-search'), q = cine.querySelector('.n-cine-q');
    if (!frame || !cv || !cv.getContext) return;
    var N = +frame.getAttribute('data-frames') || 0;
    if (!N) return;
    var mob = window.matchMedia('(max-width: 700px)');
    var ctx = cv.getContext('2d'), imgs = [], set = '', target = 0, shown = 0, raf = 0, title = false;
    var QTXT = q ? q.getAttribute('data-q') || '' : '';
    var T = { video: .8, sqIn: [86, 90], type: [90, 102], title: 106, out: [.9, 1] };   /* frame indices of the tap / typing, scroll fractions */
    function clamp(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }
    function seg(v, a, b) { return clamp((v - a) / (b - a)); }
    function load() {
      var want = mob.matches ? 'm' : 'd';
      if (want === set) return;
      set = want; imgs = [];
      var src = frame.getAttribute(want === 'm' ? 'data-msrc' : 'data-fsrc');
      /* the first frames and every 8th first, the rest after — scrubbing works at once and fills in */
      var order = [];
      for (var i = 0; i < N; i += 8) order.push(i);
      for (i = 0; i < N; i++) if (i % 8) order.push(i);
      order.forEach(function (i, n) {
        var im = new Image();
        im.decoding = 'async';
        im.onload = function () { if (Math.abs(i - shown) < 2) paint(true); };
        setTimeout(function () { im.src = src.replace('{i}', ('00' + i).slice(-3)); }, n < 24 ? 0 : 30 + n * 6);
        imgs[i] = im;
      });
      size();
    }
    function ok(im) { return im && im.complete && im.naturalWidth; }
    function near(i) { for (var d = 0; d < N; d++) { if (ok(imgs[i - d])) return imgs[i - d]; if (ok(imgs[i + d])) return imgs[i + d]; } return null; }
    function size() {
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      var w = frame.offsetWidth, h = frame.offsetHeight;
      cv.width = Math.round(w * dpr); cv.height = Math.round(h * dpr);
      paint(true);
    }
    var lastPainted = -1;
    function paint(force) {
      var i = Math.floor(shown), f = shown - i;
      var key = Math.round(shown * 20);
      if (!force && key === lastPainted) return;
      lastPainted = key;
      var a = ok(imgs[i]) ? imgs[i] : near(i), b = ok(imgs[i + 1]) ? imgs[i + 1] : null;
      if (!a) return;
      ctx.globalAlpha = 1; ctx.drawImage(a, 0, 0, cv.width, cv.height);
      if (b && f > .04) { ctx.globalAlpha = f; ctx.drawImage(b, 0, 0, cv.width, cv.height); ctx.globalAlpha = 1; }
      if (img && img.style.opacity !== '0') img.style.opacity = '0';
    }
    function scrollP() {
      var r = cine.getBoundingClientRect(), total = cine.offsetHeight - innerHeight;
      return clamp(-r.top / (total || 1));
    }
    function overlay(p) {
      var k = shown;
      if (sq) sq.style.setProperty('--sq', (seg(k, T.sqIn[0], T.sqIn[1]) * (title ? 0 : 1)).toFixed(3));
      if (q) { var n = Math.round(seg(k, T.type[0], T.type[1]) * QTXT.length); if (q.textContent.length !== n) q.textContent = QTXT.slice(0, n); }
      var on = k >= T.title;
      if (on !== title) { title = on; cine.classList.toggle('is-title', on); if (sq) sq.style.setProperty('--sq', on ? '0' : '1'); }
      stick.style.setProperty('--sh', (.15 + .7 * seg(k, T.sqIn[0], T.title + 4)).toFixed(3));
      stick.style.setProperty('--t2', seg(p, .02, .08).toFixed(3));
      stick.style.setProperty('--out', seg(p, T.out[0], T.out[1]).toFixed(3));
    }
    function loop() {
      raf = 0;
      var d = target - shown;
      shown = Math.abs(d) < .02 ? target : shown + d * (reduce ? 1 : .14);
      paint(false); overlay(scrollP());
      if (shown !== target) raf = requestAnimationFrame(loop);
    }
    function onScroll() {
      target = seg(scrollP(), 0, T.video) * (N - 1);
      if (!raf) raf = requestAnimationFrame(loop);
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', function () { load(); size(); onScroll(); });
    load(); onScroll();
  })();

  if (reduce) return;

  /* spotlight in the first screen */
  Array.prototype.forEach.call(document.querySelectorAll('[data-spot]'), function (el) {
    el.addEventListener('mousemove', function (e) {
      var r = el.getBoundingClientRect();
      el.style.setProperty('--mx', (e.clientX - r.left) + 'px');
      el.style.setProperty('--my', (e.clientY - r.top) + 'px');
    });
  });

  /* painted first screen: the painting drifts slower than the page and slowly approaches (scroll-linked) */
  var paint = document.querySelector('[data-paint] img');
  if (paint) {
    var hero = paint.closest('.n-hero'), ticking = false;
    paint.addEventListener('animationend', function () { paint.style.animation = 'none'; upd(); });
    function upd() {
      ticking = false;
      var h = hero.offsetHeight || 1, y = Math.min(window.scrollY, h);
      var p = y / h;
      paint.style.setProperty('--py', (y * 0.35).toFixed(1) + 'px');
      paint.style.setProperty('--ps', (1.06 + p * 0.12).toFixed(4));
    }
    window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(upd); } }, { passive: true });
  }

  /* reveal content blocks as they enter the screen */
  if ('IntersectionObserver' in window) {
    var sel = '.n-body main > section:not(.n-hero) .sec-header, .xid-card, .feat-card, .price-card, .step-card, .opp-card, .adv-card, .review-card, .svc-card, .info-card, .trust-card, .fmt-card, .law-card, .dir-card, .def-card, .video-card, .blog-card, .bc, .process-step, .reg-path-step, .why-item, .stat-item, .n-person, .tl-row, .tl-item';
    var els = document.querySelectorAll(sel);
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.01 });
    Array.prototype.forEach.call(els, function (el, i) {
      var r = el.getBoundingClientRect();
      if (r.top < innerHeight) return;           /* already on screen — leave as is */
      el.classList.add('n-io');
      el.style.transitionDelay = ((i % 4) * 0.08) + 's';
      io.observe(el);
    });
  }
})();
