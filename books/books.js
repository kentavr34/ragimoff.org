/* =====================================================================
   RAGIMOFF · books/books.js — «Kitablar»
   Заказ — та же механика, что на основном сайте: POST в Apps Script
   (сервер + Google-таблица + Telegram). Плюс: модал заказа, появление
   карточек, лёгкий тилт обложек.
   ===================================================================== */
(function () {
  'use strict';

  var root = document.documentElement;
  var reduceQ = window.matchMedia('(prefers-reduced-motion: reduce)');
  var fineQ = window.matchMedia('(hover: hover) and (pointer: fine)');
  var reduce = reduceQ.matches, fine = fineQ.matches;

  /* тот же эндпоинт, что на главной (форма «Kitabın sifarişi») */
  var ORDER_API = 'https://script.google.com/macros/s/AKfycbw-ejwk4wslNpEhMB11Yknj5cjPBZJkoc4nf8BTMP8lxROc8ZxtAWkkXtgv5E8GLzxyfw/exec';

  function $(s, c) { return (c || document).querySelector(s); }
  function $$(s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); }

  /* ── появление карточек ── */
  function initReveal() {
    var nodes = $$('.card, .h1');
    if (!nodes.length) return;
    nodes.forEach(function (n, i) { n.style.setProperty('--d', (i * 70) + 'ms'); });
    if (!('IntersectionObserver' in window) || reduce) return;
    root.classList.add('anim');
    var io = new IntersectionObserver(function (ents) {
      ents.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: 0.08, rootMargin: '0px 0px -8% 0px' });
    nodes.forEach(function (n) { io.observe(n); });
  }

  /* ── модал заказа ── */
  function initOrder() {
    var modal = $('[data-modal]');
    if (!modal) return;
    var form = $('#order-form');
    var ok = $('#o-ok');
    var sub = $('#o-book');
    var nameI = $('#o-name');
    var phoneI = $('#o-phone');
    var current = '';
    var lastFocus = null;

    function open(book) {
      current = book || '';
      lastFocus = document.activeElement;
      sub.textContent = current;
      ok.hidden = true;
      form.hidden = false;
      form.reset();
      modal.classList.add('is-open');
      modal.setAttribute('aria-hidden', 'false');
      root.classList.add('lock');
      setTimeout(function () { if (nameI) nameI.focus(); }, 80);
    }
    function close() {
      modal.classList.remove('is-open');
      modal.setAttribute('aria-hidden', 'true');
      root.classList.remove('lock');
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    }

    $$('[data-order]').forEach(function (b) {
      b.addEventListener('click', function () {
        var book = b.getAttribute('data-order') || '';
        var price = b.getAttribute('data-price') || '';
        open(price ? book + ' · ' + price : book);
      });
    });
    $$('[data-close]', modal).forEach(function (b) { b.addEventListener('click', close); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });

    form.addEventListener('submit', async function (e) {
      e.preventDefault();
      var name = (nameI.value || '').trim();
      var phone = (phoneI.value || '').trim();
      if (!name || !phone) { alert('Zəhmət olmasa Ad Soyad və Telefon daxil edin.'); return; }
      var parts = name.split(/\s+/);
      var payload = {
        type: 'registration',
        fname: parts[0] || '',
        lname: parts.slice(1).join(' ') || '',
        phone: phone,
        service: 'Kitab sifarişi — ' + current,
        source: 'ragimoff.org/books'
      };
      var btn = $('button[type="submit"]', form);
      if (btn) { btn.textContent = 'Göndərilir...'; btn.disabled = true; }
      try {
        await fetch(ORDER_API, {
          method: 'POST', mode: 'no-cors',
          headers: { 'Content-Type': 'text/plain;charset=utf-8' },
          body: JSON.stringify(payload)
        });
      } catch (err) { /* no-cors: ответ не читаем, ошибка сети не блокирует UX */ }
      if (btn) { btn.textContent = 'Sifariş et'; btn.disabled = false; }
      form.hidden = true;
      ok.hidden = false;
    });
  }

  /* ── тилт обложек ── */
  function initTilt() {
    if (!fine) return;
    $$('.card__cover').forEach(function (el) {
      var cover = $('.cover', el);
      if (!cover) return;
      el.addEventListener('mousemove', function (e) {
        if (reduce) return;
        var b = el.getBoundingClientRect();
        var dx = (e.clientX - b.left) / b.width - 0.5;
        var dy = (e.clientY - b.top) / b.height - 0.5;
        cover.style.transform = 'perspective(1000px) rotateY(' + (dx * 6).toFixed(2) + 'deg) rotateX(' + (-dy * 6).toFixed(2) + 'deg) translateY(-8px)';
      });
      el.addEventListener('mouseleave', function () { cover.style.transform = ''; });
    });
  }

  function boot() {
    initReveal();
    initOrder();
    initTilt();
    reduceQ.addEventListener && reduceQ.addEventListener('change', function () { reduce = reduceQ.matches; });
    fineQ.addEventListener && fineQ.addEventListener('change', function () { fine = fineQ.matches; });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
