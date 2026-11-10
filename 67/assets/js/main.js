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

  /* reveal */
  var items = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('is-in'); });
  }

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
})();
