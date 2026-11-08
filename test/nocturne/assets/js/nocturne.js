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

  if (reduce) return;

  /* spotlight in the first screen */
  Array.prototype.forEach.call(document.querySelectorAll('[data-spot]'), function (el) {
    el.addEventListener('mousemove', function (e) {
      var r = el.getBoundingClientRect();
      el.style.setProperty('--mx', (e.clientX - r.left) + 'px');
      el.style.setProperty('--my', (e.clientY - r.top) + 'px');
    });
  });

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
