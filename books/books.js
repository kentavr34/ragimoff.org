/* =====================================================================
   RAGIMOFF · books/books.js — «Kitabxana»: фильтры, модал деталей,
   появление при скролле, тилт обложек, бегущая полоса миниатюр.
   ===================================================================== */
(function () {
  'use strict';

  var root = document.documentElement;
  var reduceQ = window.matchMedia('(prefers-reduced-motion: reduce)');
  var fineQ = window.matchMedia('(hover: hover) and (pointer: fine)');
  var reduce = reduceQ.matches, fine = fineQ.matches;

  function $(s, c) { return (c || document).querySelector(s); }
  function $$(s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); }

  /* ── режим движения ── */
  function paintMotion() {
    root.classList.toggle('no-mo', reduce);
    root.classList.toggle('mo', !reduce);
  }

  /* ── данные книг для модала ── */
  var BOOKS = {
    klinik: {
      tex: "covers/klinik.jpg",
      eyebrow: 'Elektron · Ödənişsiz · 4 dil',
      title: 'Klinik Psixiatriya',
      desc: 'Psixoloji pozğunluqların diaqnostikası və müalicəsi üzrə hərtərəfli sorğu vəsaiti: 2026-cı ilə aktual klinik protokollar, XBT-11 üzrə şərhlər və daxili axtarış sistemi ilə.',
      specs: [['Müəllif', 'Kənan Rəhimov'], ['İl', '2026'], ['Dillər', 'AZ · RU · EN · TR'], ['Standart', 'XBT-11 · DSM-5'], ['Format', 'Elektron (veb)'], ['Bölmələr', '15 + alt bölmələr']],
      cta: [['btn', 'Elektron versiyanı oxu', '../klinik-psixiatriya/'], ['ghost', 'Çap versiyasını sifariş et', 'https://wa.me/994702200376?text=Salam%2C%20%22Klinik%20Psixiatriya%22%20kitab%C4%B1n%C4%B1%20sifari%C5%9F%20etm%C9%99k%20ist%C9%99yir%C9%99m']]
    },
    guilt: {
      tex: "covers/guilt.jpg",
      eyebrow: 'Çap nəşri · 2024',
      title: 'Guilt Virus',
      desc: 'Şəxsiyyət və emosional «viruslar» haqqında: günah, utanc, daxili ssenarilər və onların davranışda təzahürü. Klinik praktika və müəllifin 23 illik təcrübəsi əsasında.',
      specs: [['Müəllif', 'Kənan Rəhimov'], ['İl', '2024'], ['Səhifə', '280'], ['Dil', 'AZ'], ['Format', 'Çap'], ['Mövzu', 'Şəxsiyyət · emosiyalar']],
      cta: [['btn', 'Sifariş et', 'https://wa.me/994702200376?text=Salam%2C%20%22Guilt%20Virus%22%20kitab%C4%B1n%C4%B1%20sifari%C5%9F%20etm%C9%99k%20ist%C9%99yir%C9%99m']]
    },
    pandemic: {
      tex: "covers/pandemic.jpg",
      eyebrow: 'Çap nəşri · 2025',
      title: 'Pandemic of Madness',
      desc: 'Elm və səs əsasında: kollektiv təşviş, qorxu dalğaları, informasiya təzyiqi və cəmiyyətin psixikası. Psixiatriya ilə sosiologiyanın kəsişməsində.',
      specs: [['Müəllif', 'Kənan Rəhimov'], ['İl', '2025'], ['Səhifə', '320'], ['Dil', 'AZ'], ['Format', 'Çap'], ['Mövzu', 'Kollektiv psixika']],
      cta: [['btn', 'Sifariş et', 'https://wa.me/994702200376?text=Salam%2C%20%22Pandemic%20of%20Madness%22%20kitab%C4%B1n%C4%B1%20sifari%C5%9F%20etm%C9%99k%20ist%C9%99yir%C9%99m']]
    },
    phoenix: {
      tex: "covers/phoenix.jpg",
      eyebrow: 'Çap nəşri · 2025',
      title: 'Phoenix Era',
      desc: 'Fəlsəfə və mədəniyyət üzərində qurulmuş əsər: yenidən doğulma, məna axtarışı və insanın öz hekayəsini yenidən yazması.',
      specs: [['Müəllif', 'Kənan Rəhimov'], ['İl', '2025'], ['Səhifə', '340'], ['Dil', 'AZ'], ['Format', 'Çap'], ['Mövzu', 'Fəlsəfə · mədəniyyət']],
      cta: [['btn', 'Sifariş et', 'https://wa.me/994702200376?text=Salam%2C%20%22Phoenix%20Era%22%20kitab%C4%B1n%C4%B1%20sifari%C5%9F%20etm%C9%99k%20ist%C9%99yir%C9%99m']]
    }
  };

  /* ── появление при скролле ── */
  function initReveal() {
    var nodes = $$('[data-rv]');
    if (!nodes.length) return;
    if (!('IntersectionObserver' in window)) { nodes.forEach(function (n) { n.classList.add('in'); }); return; }
    var io = new IntersectionObserver(function (ents) {
      ents.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.08 });
    nodes.forEach(function (n) { io.observe(n); });
  }

  /* ── фильтры ── */
  function initFilters() {
    var state = { type: 'all', lang: 'all' };
    var cards = $$('.card');
    var label = $('[data-count-label]');
    var empty = $('.empty');

    function apply() {
      var shown = 0;
      cards.forEach(function (c) {
        var typeOk = state.type === 'all' || c.getAttribute('data-type') === state.type;
        var langs = (c.getAttribute('data-langs') || '').split(/\s+/);
        var langOk = state.lang === 'all' || langs.indexOf(state.lang) !== -1;
        var ok = typeOk && langOk;
        c.hidden = !ok;
        if (ok) shown++;
      });
      if (label) label.textContent = shown + ' kitab';
      if (empty) empty.hidden = shown !== 0;
    }

    $$('.chip[data-filter]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var f = btn.getAttribute('data-filter');
        state[f] = btn.getAttribute('data-value');
        $$('.chip[data-filter="' + f + '"]').forEach(function (b) { b.classList.toggle('is-on', b === btn); });
        apply();
      });
    });
    apply();
  }

  /* ── модал деталей ── */
  function initModal() {
    var modal = $('[data-modal]');
    if (!modal) return;
    var cover = $('#m-cover'), eyebrow = $('#m-eyebrow'), title = $('#m-title'),
        desc = $('#m-desc'), specs = $('#m-specs'), cta = $('#m-cta');
    var lastFocus = null;

    function open(id) {
      var b = BOOKS[id];
      if (!b) return;
      lastFocus = document.activeElement;
      cover.setAttribute('style', "--tex:url('" + b.tex + "')");
      cover.innerHTML = '<span class="cover__frame" aria-hidden="true"></span>' +
        '<span class="cover__author">KƏNAN RƏHİMOV</span>' +
        '<span class="cover__title">' + b.title.replace(/ /g, '<br>') + '</span>';
      eyebrow.textContent = b.eyebrow;
      title.textContent = b.title;
      desc.textContent = b.desc;
      specs.innerHTML = b.specs.map(function (s) {
        return '<div><dt>' + s[0] + '</dt><dd>' + s[1] + '</dd></div>';
      }).join('');
      cta.innerHTML = b.cta.map(function (c) {
        var cls = c[0] === 'btn' ? 'btn btn--main' : 'btn btn--ghost';
        var ext = /^https?:/.test(c[2]) ? ' target="_blank" rel="noopener"' : '';
        return '<a class="' + cls + '" href="' + c[2] + '"' + ext + '>' + c[1] + '</a>';
      }).join('');
      modal.classList.add('is-open');
      modal.setAttribute('aria-hidden', 'false');
      root.classList.add('lock');
      var f = $('.modal__x', modal); if (f) setTimeout(function () { f.focus(); }, 60);
    }
    function close() {
      modal.classList.remove('is-open');
      modal.setAttribute('aria-hidden', 'true');
      root.classList.remove('lock');
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    }

    $$('[data-open]').forEach(function (b) {
      b.addEventListener('click', function () { open(b.getAttribute('data-open')); });
    });
    $$('[data-close]', modal).forEach(function (b) { b.addEventListener('click', close); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
  }

  /* ── тилт обложек ── */
  function initTilt() {
    if (!fine) return;
    $$('[data-tilt], .card__cover').forEach(function (el) {
      var target = el.classList.contains('card__cover') ? $('.cover', el) : el;
      if (!target) return;
      el.addEventListener('mousemove', function (e) {
        if (reduce) return;
        var b = el.getBoundingClientRect();
        var dx = (e.clientX - b.left) / b.width - 0.5;
        var dy = (e.clientY - b.top) / b.height - 0.5;
        target.style.transform = 'perspective(1000px) rotateY(' + (dx * 7).toFixed(2) + 'deg) rotateX(' + (-dy * 7).toFixed(2) + 'deg) translateY(-8px)';
      });
      el.addEventListener('mouseleave', function () { target.style.transform = ''; });
    });
  }

  /* ── бегущая полоса миниатюр: дублируем для бесшовности ── */
  function initStrip() {
    var strip = $('.hero__strip');
    if (!strip) return;
    if (reduce) { strip.style.animation = 'none'; return; }
    strip.innerHTML += strip.innerHTML;
  }

  /* ── старт ── */
  function boot() {
    paintMotion();
    initStrip();
    initReveal();
    initFilters();
    initModal();
    initTilt();
    root.classList.add('js-ready');
    reduceQ.addEventListener && reduceQ.addEventListener('change', function () {
      reduce = reduceQ.matches; paintMotion();
    });
    fineQ.addEventListener && fineQ.addEventListener('change', function () { fine = fineQ.matches; });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
