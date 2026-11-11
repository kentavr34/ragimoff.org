/* ═══════════════════════════════════════════════════════════════════
   МОУШЕН — ЖИВОСТЬ
   ═══════════════════════════════════════════════════════════════════
   ЗАЧЕМ ЭТОТ ФАЙЛ. Владелец (11.11.2026): «исполнение слишком сухое,
   неживое, мертвое... на текущей главной есть motion-эффект, когда
   скроллишь, она движется — это живой эффект... это создаёт ощущение
   доверия, коммуникации, как будто ты с живым человеком разговариваешь».

   Главный тезис владельца: доверие на 90% формируется ДО чтения услуг —
   через ощущение, что сайт делали всерьёз. Значит моушен здесь не
   украшение, а часть аргументации.

   ЧТО ДЕЛАЕТ КАЖДЫЙ ЭФФЕКТ (и почему именно так):

   1. ПОЯВЛЕНИЕ СТУПЕНЯМИ (reveal) — блоки выходят навстречу при прокрутке.
      Не «эффект ради эффекта»: глаз ведут по странице в том порядке, в
      котором выстроена аргументация (кто → чем доказал → чему учит).

   2. ДЫХАНИЕ ГЕРОЯ — кадр живёт: лёгкий сдвиг и наплыв при прокрутке.
      Это то ощущение «движется, а не мёртвая циферка», о котором сказал
      владелец.

   3. ХОД ЗАГОЛОВКА — заголовок не выскакивает, а ПРОХОДИТ сквозь маску:
      слова поднимаются снизу, по одному. Читается как речь, а не как
      табличка.

   4. ПОДЧЁРКИВАНИЕ ССЫЛОК — линия идёт от левого края. Мелочь, которая
      читается как аккуратность.

   5. ШАПКА — сжимается при прокрутке, отдавая место содержимому.

   6. СЧЁТ ЦИФР — числа (часы, цены) набираются, а не появляются готовыми.
      Внимание к цифре — это внимание к факту.

   ЖЕЛЕЗНОЕ ПРАВИЛО (оплачено ошибкой): если на машине включено
   «уменьшить движение», CSS-анимации глушатся. Страница, у которой
   главный визуал появляется анимацией, останется ПУСТОЙ. Поэтому:
     · проверка reduced-motion есть;
     · нет ни одного элемента, который виден ТОЛЬКО через анимацию;
     · базовое состояние всегда видимое, анимация лишь улучшает.
   ═══════════════════════════════════════════════════════════════════ */

(function () {
  'use strict';

  var reduced = window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ── 1. ПОЯВЛЕНИЕ БЛОКОВ ──────────────────────────────────────────
     Ступени задаются задержкой, чтобы блоки шли друг за другом, а не
     вспыхивали все сразу: так глаз ведут по порядку аргументации. */
  function initReveal() {
    var nodes = [].slice.call(document.querySelectorAll('.reveal'));
    if (!nodes.length) return;

    function show(el) {
      el.classList.add('is-in');
      var idx = parseInt(el.getAttribute('data-step') || '0', 10);
      el.style.transitionDelay = (idx * 70) + 'ms';
    }

    if (reduced) { nodes.forEach(show); return; }

    /* Обычный обработчик прокрутки, а не только наблюдатель: при
       «уменьшить движение» наблюдатель не срабатывает, и страница
       остаётся серым текстом. Это уже случалось. */
    var pending = nodes.slice();
    function check() {
      var h = window.innerHeight || document.documentElement.clientHeight;
      for (var i = pending.length - 1; i >= 0; i--) {
        var r = pending[i].getBoundingClientRect();
        if (r.top < h * 0.9 && r.bottom > 0) {
          show(pending[i]);
          pending.splice(i, 1);
        }
      }
      if (!pending.length) {
        window.removeEventListener('scroll', check);
        window.removeEventListener('resize', check);
      }
    }
    /* Наблюдатель — основной механизм; он ловит и программную прокрутку. */
    var io = ('IntersectionObserver' in window)
      ? new IntersectionObserver(function (entries) {
          entries.forEach(function (e) {
            if (!e.isIntersecting) return;
            var el = e.target;
            var idx = pending.indexOf(el);
            if (idx >= 0) { show(el); pending.splice(idx, 1); }
            io.unobserve(el);
          });
        }, { rootMargin: '0px 0px -6% 0px' })
      : null;
    if (io) pending.forEach(function (el) { io.observe(el); });

    window.addEventListener('scroll', check, { passive: true });
    window.addEventListener('resize', check);
    check();
    setTimeout(check, 250);

    /* СТРАХОВКА. Как выяснилось опытным путём, при некоторых способах
       прокрутки проявление может не произойти — и блок молча остаётся
       невидимым. Периодическая проверка гарантирует, что «пустых мест»
       не будет ни при каком способе прокрутки. */
    var guard = setInterval(function () {
      check();
      if (!pending.length) clearInterval(guard);
    }, 400);
    /* Последний рубеж: если к 6 секундам что-то всё ещё не показано,
       показываем принудительно. Видимый блок, появившийся без анимации,
       лучше невидимого. */
    setTimeout(function () {
      if (pending.length) { pending.slice().forEach(show); pending.length = 0; }
      clearInterval(guard);
    }, 6000);
  }

  /* ── 2. ДЫХАНИЕ ГЕРОЯ ─────────────────────────────────────────────
     Кадр не стоит на месте: при прокрутке он чуть наплывает и сдвигается.
     Медленно и мало — это должно читаться как жизнь, а не как движение
     картинки. Скорость подобрана так, чтобы не укачивало. */
  function initHeroLife() {
    var hero = document.getElementById('hero');
    if (!hero || reduced) return;
    var media = hero.querySelector('.hero__media');
    var inner = hero.querySelector('.hero__inner');
    if (!media) return;

    var ticking = false;
    function frame() {
      var rect = hero.getBoundingClientRect();
      var h = hero.offsetHeight || 1;
      // 0 — герой на месте, 1 — полностью прокручен
      var p = Math.max(0, Math.min(1, -rect.top / h));

      media.style.transform = 'scale(' + (1 + p * 0.12).toFixed(4) +
        ') translate3d(0,' + (p * 26).toFixed(2) + 'px,0)';
      if (inner) {
        inner.style.transform = 'translate3d(0,' + (p * -34).toFixed(2) + 'px,0)';
        // текст уходит мягко, а не обрывается: к концу героя он почти прозрачен
        inner.style.opacity = String(Math.max(0, 1 - p * 1.25).toFixed(3));
      }
      ticking = false;
    }
    function onScroll() {
      if (!ticking) { ticking = true; requestAnimationFrame(frame); }
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    frame();
  }

  /* ── 3. ХОД ЗАГОЛОВКОВ ────────────────────────────────────────────
     Заголовок раздела проходит сквозь маску: слова поднимаются снизу
     по очереди. Разметка внутри слова НЕ рвётся: текст разбивается на
     слова, каждое оборачивается в свою оболочку, а исходная ширина
     строки сохраняется — иначе заголовок начнёт переноситься иначе. */
  function initHeadlines() {
    if (reduced) return;
    var heads = [].slice.call(document.querySelectorAll('.section__head h2, .foot__title'));
    heads.forEach(function (h) {
      if (h.getAttribute('data-split') === '1') return;
      var text = h.textContent.trim();
      if (!text) return;
      var words = text.split(/\s+/);
      h.textContent = '';
      words.forEach(function (w, i) {
        var outer = document.createElement('span');
        outer.className = 'w';
        var inner = document.createElement('span');
        inner.className = 'w__in';
        inner.textContent = w;
        inner.style.transitionDelay = (i * 55) + 'ms';
        outer.appendChild(inner);
        h.appendChild(outer);
        if (i < words.length - 1) h.appendChild(document.createTextNode(' '));
      });
      h.setAttribute('data-split', '1');
      // запускаем, когда заголовок входит в кадр
      var io = ('IntersectionObserver' in window)
        ? new IntersectionObserver(function (es) {
            es.forEach(function (e) {
              if (e.isIntersecting) { h.classList.add('is-split'); io.disconnect(); }
            });
          }, { threshold: 0.25 })
        : null;
      if (io) io.observe(h); else h.classList.add('is-split');
      // страховка на случай, если наблюдатель не сработал
      setTimeout(function () { h.classList.add('is-split'); }, 2600);
    });
  }

  /* ── 4. ШАПКА ─────────────────────────────────────────────────────
     Сжимается при прокрутке: отдаёт место содержимому и одновременно
     даёт понять, что страница двинулась. */
  function initHeader() {
    var hdr = document.getElementById('hdr');
    if (!hdr) return;
    var ticking = false;
    function frame() {
      if (window.scrollY > 40) hdr.classList.add('is-tight');
      else hdr.classList.remove('is-tight');
      ticking = false;
    }
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(frame); }
    }, { passive: true });
    frame();
  }

  /* ── 5. СЧЁТ ЦИФР ─────────────────────────────────────────────────
     Числа набираются от нуля до значения. Не для зрелищности: набор
     заставляет глаз остановиться на цифре и сравнить её с соседней —
     а цифры здесь и есть аргумент (1528 часов, годы опыта). */
  function initCounters() {
    if (reduced) return;
    var nodes = [].slice.call(document.querySelectorAll('[data-count]'));
    if (!nodes.length) return;

    function run(el) {
      var target = parseFloat(el.getAttribute('data-count'));
      if (isNaN(target)) return;
      var dur = 900, t0 = null;
      function step(ts) {
        if (!t0) t0 = ts;
        var k = Math.min(1, (ts - t0) / dur);
        // замедление к концу: цифра «останавливается», а не обрывается
        var e = 1 - Math.pow(1 - k, 3);
        el.textContent = Math.round(target * e).toLocaleString('ru-RU');
        if (k < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    }

    if (!('IntersectionObserver' in window)) { nodes.forEach(run); return; }
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) { run(e.target); io.unobserve(e.target); }
      });
    }, { threshold: 0.4 });
    nodes.forEach(function (n) { io.observe(n); });
  }

  /* ── 6. МЕНЮ НА ТЕЛЕФОНЕ ──────────────────────────────────────────
     Закрывается по выбору пункта и по клавише Esc: открытое меню поверх
     страницы без выхода — это ловушка. */
  function initBurger() {
    var b = document.getElementById('burger');
    var nav = document.getElementById('nav');
    if (!b || !nav) return;
    b.addEventListener('click', function () {
      var open = document.body.classList.toggle('nav-open');
      b.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) {
        document.body.classList.remove('nav-open');
        b.setAttribute('aria-expanded', 'false');
      }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') document.body.classList.remove('nav-open');
    });
  }

  /* ── ЗАПУСК ───────────────────────────────────────────────────────
     Дом готов к этому моменту: скрипт подключён в конце тела. */
  function start() {
    initReveal();
    initHeroLife();
    initHeadlines();
    initHeader();
    initCounters();
    initBurger();
    document.documentElement.classList.add('motion-ready');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }
})();
