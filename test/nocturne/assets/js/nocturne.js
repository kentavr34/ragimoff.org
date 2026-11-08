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

  /* home first screen — a pinned scene driven by scroll (user-controlled, so it works with reduced motion too):
     frames of the video on <canvas> if data-frames is set, otherwise a camera move over the painting */
  var cine = document.querySelector('[data-cine]');
  if (cine) (function () {
    var frame = cine.querySelector('.n-cine-frame'), b1 = cine.querySelector('.n-cine-b1'), b2 = cine.querySelector('.n-cine-b2');
    var stick = cine.querySelector('.n-cine-stick'), cv = cine.querySelector('.n-cine-cv'), dust = cine.querySelector('.n-cine-dust');
    if (!frame) return;
    var N = +frame.getAttribute('data-frames') || 0, fsrc = frame.getAttribute('data-fsrc') || '', imgs = [], cur = -1, ctx = null;
    function clamp(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }
    function ease(t) { return t < .5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2; }
    function seg(p, a, b) { return clamp((p - a) / (b - a)); }
    function sizeCv() {
      if (!ctx) return;
      var dpr = Math.min(window.devicePixelRatio || 1, 1.5);
      cv.width = Math.min(1920, Math.round(frame.offsetWidth * dpr)); cv.height = Math.round(cv.width * 928 / 1664);
      draw(cur < 0 ? 0 : cur, true);
    }
    function draw(i, force) {
      i = Math.max(0, Math.min(N - 1, i));
      if (i === cur && !force) return;
      var j = i;
      while (j >= 0 && !(imgs[j] && imgs[j].complete && imgs[j].naturalWidth)) j--;
      if (j < 0) return;
      cur = i; ctx.drawImage(imgs[j], 0, 0, cv.width, cv.height);
    }
    if (N && cv && cv.getContext) {
      ctx = cv.getContext('2d');
      for (var i = 0; i < N; i++) {
        (function (i) {
          var im = new Image();
          im.decoding = 'async';
          im.onload = function () { if (i === 0) { frame.classList.add('has-frames'); sizeCv(); } else if (i === cur) draw(cur, true); };
          im.src = fsrc.replace('{i}', ('00' + i).slice(-3));
          imgs[i] = im;
        })(i);
      }
    }
    var mob = window.matchMedia('(max-width: 700px)'), ticking = false;
    function upd() {
      ticking = false;
      var r = cine.getBoundingClientRect(), total = cine.offsetHeight - innerHeight;
      var p = clamp(-r.top / (total || 1));
      if (N) draw(Math.round(p * (N - 1)));
      var z = ease(seg(p, 0, .92));
      if (mob.matches) {   /* phone: the camera first walks sideways from the book to the lamp, then moves in */
        frame.style.setProperty('--cx', (-ease(seg(p, 0, .55)) * Math.min(frame.offsetWidth * .18, 300)).toFixed(1) + 'px');
        frame.style.setProperty('--cz', (1 + (N ? .12 : .38) * ease(seg(p, .35, 1))).toFixed(4));
      } else {
        frame.style.setProperty('--cx', '0px');
        frame.style.setProperty('--cz', (1 + (N ? .14 : .62) * z).toFixed(4));
      }
      var t1 = 1 - seg(p, .06, .3);
      b1.style.setProperty('--t1', t1.toFixed(3));
      b1.style.setProperty('--y1', (-90 * seg(p, .06, .3)).toFixed(1) + 'px');
      b1.style.visibility = t1 < .02 ? 'hidden' : '';
      var t2 = seg(p, .36, .5) * (1 - seg(p, .74, .86));
      if (b2) { b2.style.setProperty('--t2', t2.toFixed(3)); stick.style.setProperty('--t2', Math.max(t2, 1 - t1).toFixed(3)); }
      stick.style.setProperty('--out', seg(p, .8, 1).toFixed(3));
    }
    function req() { if (!ticking) { ticking = true; requestAnimationFrame(upd); } }
    window.addEventListener('scroll', req, { passive: true });
    window.addEventListener('resize', function () { sizeCv(); req(); });
    upd();

    /* dust in the lamp light */
    if (reduce || !dust || !dust.getContext) return;
    var dc = dust.getContext('2d'), parts = [], run = false, W = 0, Hh = 0;
    function dsize() { var dpr = Math.min(window.devicePixelRatio || 1, 1.5); W = dust.width = Math.round(frame.offsetWidth * dpr / 2); Hh = dust.height = Math.round(W * 928 / 1664); }
    function spawn(p) {
      p.x = .52 + Math.random() * .4; p.y = .3 + Math.random() * .55;
      p.r = .6 + Math.random() * 1.8; p.vx = (Math.random() - .5) * .00018; p.vy = -.00008 - Math.random() * .00022;
      p.a = 0; p.life = 0; p.max = 500 + Math.random() * 700; p.ph = Math.random() * 6.28;
      return p;
    }
    for (var k = 0; k < 70; k++) { var q = spawn({}); q.life = Math.random() * q.max; parts.push(q); }
    function tick() {
      if (!run) return;
      dc.clearRect(0, 0, W, Hh);
      for (var k = 0; k < parts.length; k++) {
        var p = parts[k];
        p.life++; p.x += p.vx + Math.sin((p.life + p.ph * 90) / 140) * .00012; p.y += p.vy;
        var f = p.life / p.max, al = Math.sin(Math.PI * f) * (.35 + .25 * Math.sin(p.life / 20 + p.ph));
        var lit = Math.max(0, 1 - Math.hypot((p.x - .7) / .32, (p.y - .55) / .42));   /* brighter inside the cone of light */
        dc.globalAlpha = Math.max(0, al * (.25 + lit));
        dc.fillStyle = '#FFE2A8';
        dc.beginPath(); dc.arc(p.x * W, p.y * Hh, p.r * (W / 1200), 0, 6.283); dc.fill();
        if (p.life >= p.max || p.y < .2) spawn(p);
      }
      requestAnimationFrame(tick);
    }
    dsize(); window.addEventListener('resize', dsize);
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (en) { var v = en[0].isIntersecting; if (v && !run) { run = true; requestAnimationFrame(tick); } else if (!v) run = false; }).observe(stick);
    } else { run = true; requestAnimationFrame(tick); }
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
