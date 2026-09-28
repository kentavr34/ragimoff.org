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

  /* эндпоинты заказа — те же, что у формы «Kitabın sifarişi» на сайте:
     сервер сайта (api.ragimoff.org) + Apps Script (Google-таблица + Telegram) */
  var BOOK_API = 'https://api.ragimoff.org/api/book-order';
  var ORDER_API = 'https://script.google.com/macros/s/AKfycbw-ejwk4wslNpEhMB11Yknj5cjPBZJkoc4nf8BTMP8lxROc8ZxtAWkkXtgv5E8GLzxyfw/exec';

  /* строки интерфейса — из страницы (window.__booksUI), запас — азербайджанский */
  var T = window.__booksUI || {};
  function t(key, fallback) { return T[key] || fallback; }

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

  /* ── поиск по книгам (название, автор, год) ── */
  function initSearch() {
    var q = $('#q'); if (!q) return;
    var cards = $('.card');
    var count = $('#count');
    var chips = $('.chip');
    var activeAuthor = '';
    var empty = null;
    function run() {
      var v = (q.value || '').trim().toLowerCase();
      var shown = 0;
      cards.forEach(function (c) {
        var okAuthor = !activeAuthor || c.getAttribute('data-author') === activeAuthor;
        var hay = (c.textContent || '').toLowerCase().replace(/\s+/g, ' ');
        var ok = (!v || hay.indexOf(v) !== -1) && okAuthor;
        c.hidden = !ok;
        if (ok) shown++;
      });
      /* секция автора видна, только если в ней остались карточки */
      $('.author-sec').forEach(function (h) {
        var g = h.getAttribute('data-author');
        h.hidden = !$('.card[data-author="' + g + '"]').some(function (c) { return !c.hidden; });
      });
      if (count) count.textContent = t('count', '%n kitab').replace('%n', shown);
      var grid = $('.grid');
      if (grid) {
        if (!empty) { empty = document.createElement('p'); empty.className = 'no-results'; empty.textContent = t('empty', 'Heç nə tapılmadı'); grid.parentNode.appendChild(empty); }
        empty.hidden = shown !== 0;
      }
    }
    chips.forEach(function (b) {
      b.addEventListener('click', function () {
        activeAuthor = b.getAttribute('data-author') || '';
        chips.forEach(function (x) { x.classList.toggle('is-on', x === b); });
        run();
      });
    });
    q.addEventListener('input', run);
    run();
  }

  /* ── модал заказа ── */
  function initOrder() {
    var modal = $('[data-modal]');
    if (!modal) return;
    var form = $('#order-form');
    var ok = $('#o-ok');
    var sub = $('#o-sub');
    var select = $('#o-book');
    var nameI = $('#o-name');
    var phoneI = $('#o-phone');
    var current = '';
    var lastFocus = null;

    function open(book) {
      current = book || '';
      lastFocus = document.activeElement;
      ok.hidden = true;
      form.hidden = false;
      form.reset();
      if (select) { for (var i = 0; i < select.options.length; i++) { if (select.options[i].value === current) { select.selectedIndex = i; break; } } }
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
      if (!name || !phone) { alert(t('fill', 'Zəhmət olmasa Ad Soyad və Telefon daxil edin.')); return; }
      var parts = name.split(/\s+/);
      var book = (select && select.value) || current;   /* «Название · цена» */
      var payload = {
        type: 'registration',
        fname: parts[0] || '',
        lname: parts.slice(1).join(' ') || '',
        phone: phone,
        service: 'Kitab sifarişi — ' + book,
        note: book,
        source: 'ragimoff.org' + location.pathname
      };
      var btn = $('button[type="submit"]', form);
      if (btn) { btn.textContent = t('sending', 'Göndərilir…'); btn.disabled = true; }
      var body = JSON.stringify(payload);
      /* оба канала, как в форме «Kitabın sifarişi» на сайте:
         сервер сайта (регистрация заказа) + Apps Script (Google-таблица + Telegram) */
      try { fetch(BOOK_API, { method: 'POST', headers: { 'Content-Type': 'text/plain;charset=utf-8' }, body: body }).catch(function () {}); } catch (err) {}
      try {
        await fetch(ORDER_API, {
          method: 'POST', mode: 'no-cors',
          headers: { 'Content-Type': 'text/plain;charset=utf-8' },
          body: body
        });
      } catch (err) { /* no-cors: ответ не читаем, ошибка сети не блокирует UX */ }
      if (btn) { btn.textContent = t('submit', 'Sifariş et'); btn.disabled = false; }
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
    initSearch();
    initOrder();
    initTilt();
    reduceQ.addEventListener && reduceQ.addEventListener('change', function () { reduce = reduceQ.matches; });
    fineQ.addEventListener && fineQ.addEventListener('change', function () { fine = fineQ.matches; });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
