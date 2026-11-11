/* ═══════════════════════════════════════════════════════════════════
   МОУШЕН НА GSAP + LENIS
   ═══════════════════════════════════════════════════════════════════
   ПОЧЕМУ ЭТИ ДВЕ БИБЛИОТЕКИ. По результатам ресерча (файл
   _agent/docs/VYBOR_TEHNOLOGII_MOUSН.md):
     · GSAP + ScrollTrigger — «лучший в мире для хореографии по прокрутке,
       с версии 3.13 полностью бесплатен вместе со всеми плагинами»;
       у нас длинный герой (2.5 экрана) со ступенчатым раскрытием — ровно
       его задача.
     · Lenis — «не движок анимации, а слой инерции прокрутки. Стандарт
       де-факто на творческих сайтах». Именно он даёт то ощущение
       живости, о котором говорил владелец: «она движется, это живой
       эффект... как будто ты с живым человеком разговариваешь».

   ГЛАВНОЕ ПРАВИЛО, ОПЛАЧЕННОЕ ДВАЖДЫ. Ни один блок не должен быть виден
   ТОЛЬКО за счёт анимации. Если скрипт не загрузится, упадёт или
   пользователь держит «уменьшить движение» — страница обязана быть
   полностью читаемой. Поэтому:
     · базовое состояние блоков — ВИДИМОЕ (класс is-in ставится сразу);
     · GSAP только УЛУЧШАЕТ появление, но не отвечает за видимость;
     · если GSAP не поднялся — принудительно показываем всё;
     · на телефоне параллакс отключён: там он читается как тряска.

   ЧТО ДЕЛАЕТ КАЖДЫЙ ЭФФЕКТ (и зачем, а не «чтобы было»):
     1. Инерция прокрутки (Lenis) — ощущение живого отклика.
     2. Появление блоков ступенями — глаз ведут по порядку аргументации:
        кто → чем доказал → чему учит.
     3. Дыхание героя — кадр живёт при прокрутке, как на текущем сайте.
     4. Затемнение героя ПОЗЖЕ и плавнее (требование владельца: «темнота
        наступает... быстрее наступала. Надо было чтобы она плавнее
        возникала, во-вторых, не возникала, а плавнее переходила»).
     5. Живая кнопка регистрации (канон 110: «запрещены неактивные,
        дохлые кнопки регистрации»).
   ═══════════════════════════════════════════════════════════════════ */

(function () {
  'use strict';

  /* ── МЕТКА «МОУШЕН ЖИВОЙ» ──────────────────────────────────────────
     Ставится ПЕРВЫМ действием, до всего остального. Смысл: блоки скрыты
     для анимации ТОЛЬКО когда скрипт действительно работает. Если скрипт
     не загрузился, упал или заблокирован — метки нет, и блоки видны
     сразу (правило в design/components/motion-guard.css).

     Это надёжнее таймеров-страховок: таймеры приходилось гадать, сломан
     механизм или просто блоки далеко внизу. Здесь гадать нечего. */
  document.documentElement.classList.add('motion-live');

  var reduced = window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var isMobile = window.matchMedia && window.matchMedia('(max-width: 760px)').matches;

  /* ── СТРАХОВКА ОТ НЕВИДИМЫХ БЛОКОВ ───────────────────────────────
     Самая дорогая ошибка этого проекта: блок, который ждёт анимацию,
     остаётся прозрачным, и страница выглядит пустой. Поэтому показываем
     содержимое ДО всякой анимации, а анимация лишь повторяет появление
     красиво. Так невидимость невозможна в принципе. */
  function revealAll() {
    var list = document.querySelectorAll('.reveal');
    for (var i = 0; i < list.length; i++) list[i].classList.add('is-in');
  }

  /* ── ЕСЛИ ДВИЖЕНИЕ ОТКЛЮЧЕНО: показываем всё и уходим ────────────
     Никакой анимации, никакой инерции — только читаемая страница. */
  if (reduced) {
    revealAll();
    initTabsOnly();
    return;
  }

  var gsapReady = (typeof window.gsap !== 'undefined');
  var stReady = gsapReady && (typeof window.ScrollTrigger !== 'undefined');

  if (gsapReady && stReady) {
    try { gsap.registerPlugin(ScrollTrigger); } catch (e) { stReady = false; }
  }

  /* ── 1. ИНЕРЦИЯ ПРОКРУТКИ ────────────────────────────────────────
     Lenis подключается только если загрузился: он улучшает ощущение,
     но не отвечает за работоспособность страницы. */
  function initLenis() {
    if (typeof window.Lenis === 'undefined') return null;
    try {
      var lenis = new window.Lenis({
        duration: 1.05,
        // мягкое торможение: «дорогое» ощущение — это плавность, а не скорость
        easing: function (t) { return Math.min(1, 1.001 - Math.pow(2, -10 * t)); },
        smoothWheel: true,
        // на телефоне инерцию НЕ включаем: там она мешает, а не помогает
        smoothTouch: false
      });
      if (gsapReady && window.ScrollTrigger) {
        lenis.on('scroll', ScrollTrigger.update);
      }
      function raf(time) { lenis.raf(time * 1000); }
      if (gsapReady) gsap.ticker.add(raf);
      else (function loop(t) { lenis.raf(t); requestAnimationFrame(loop); })(0);
      return lenis;
    } catch (e) {
      return null;
    }
  }

  /* ── 2. ПОЯВЛЕНИЕ БЛОКОВ СТУПЕНЯМИ ───────────────────────────────
     Ступени вместо одновременности: 60–90 мс между элементами. Так глаз
     ведут, а не ошеломляют. Значения сдвига небольшие — 28 px: крупный
     сдвиг читается как трюк, а не как достоинство. */
  /* ── 2. ПОЯВЛЕНИЕ БЛОКОВ СТУПЕНЯМИ ───────────────────────────────
     ПРИЧИНА ПЕРЕДЕЛКИ (ошибка, найденная замером). Первая версия доверила
     появление блоков GSAP: gsap.fromTo(el, {opacity:0}, ...). В результате
     GSAP выставил блокам inline opacity:0, а ScrollTrigger без реальной
     прокрутки не сработал — и ВСЕ 25 блоков остались невидимыми, хотя
     класс is-in у них был. Замер: «с классом is-in: 25 | видно: 0».
     Это ровно тот дефект, который владелец уже видел («страница пустая»),
     и он недопустим.

     ПРАВИЛО, КОТОРОЕ ТЕПЕРЬ СОБЛЮДАЕТСЯ СТРОГО: за ВИДИМОСТЬ блоков
     отвечает CSS и обычный обработчик прокрутки, а не библиотека анимации.
     GSAP в этом проекте улучшает движение (параллакс, затемнение,
     заголовки), но не имеет права решать, видно блок или нет.

     Ступени появления: элементы в кадре показываются друг за другом с
     задержкой 70 мс — так глаз ведут по порядку аргументации. */
  function initReveal() {
    var list = Array.prototype.slice.call(document.querySelectorAll('.reveal'));
    if (!list.length) return;

    function show(el, i) {
      el.classList.add('is-in');
      el.style.transitionDelay = (i % 6) * 70 + 'ms';
    }

    var pending = list.slice();
    function check() {
      var h = window.innerHeight || document.documentElement.clientHeight;
      for (var i = pending.length - 1; i >= 0; i--) {
        var r = pending[i].getBoundingClientRect();
        if (r.top < h * 0.92 && r.bottom > 0) {
          show(pending[i], pending.length - 1 - i);
          pending.splice(i, 1);
        }
      }
      if (!pending.length) {
        window.removeEventListener('scroll', check);
        window.removeEventListener('resize', check);
      }
    }
    window.addEventListener('scroll', check, { passive: true });
    window.addEventListener('resize', check);
    check();
    setTimeout(check, 250);

    /* СТРАХОВКА — НО УМНАЯ.
       ПРИЧИНА ПРАВКИ (найдено замером на телефоне): первая версия через
       5 секунд показывала ВСЕ оставшиеся блоки. Это убивало замысел —
       блоки, которые ещё далеко внизу, вспыхивали заранее, и при
       прокрутке ничего не происходило. Замер: на 390 px «с классом
       is-in: 0» через 2 секунды и «25» через 6 — то есть страховка
       сработала вместо обработчика, а не в помощь ему.

       КАК ТЕПЕРЬ: страховка включается ТОЛЬКО если не показался НИ ОДИН
       блок. Это признак, что обработчик не работает вообще (сломан
       скрипт, конфликт библиотек). Если хотя бы один блок появился —
       механизм жив, и остальные появятся при прокрутке, как задумано. */
    /* Таймер-страховка УБРАНА. Её заменила метка motion-live: если скрипт
       не работает, блоки видимы с самого начала, и ничего ждать не надо.
       Причина отказа от таймера: он срабатывал, когда блоки просто были
       ниже экрана, и показывал их раньше времени — ломая замысел. */
  }

  /* ── 3. ДЫХАНИЕ ГЕРОЯ ────────────────────────────────────────────
     Владелец про текущую главную: «когда открывается, есть motion-эффект,
     когда скроллишь, она движется, это живой эффект». Повторяем:
     кадр медленно наплывает, текст уходит вверх. */
  function initHeroLife() {
    if (!stReady || isMobile) return;
    var hero = document.getElementById('hero');
    var media = hero && hero.querySelector('.hero__frame');
    var inner = hero && hero.querySelector('.hero__inner');
    if (!hero || !media) return;

    gsap.to(media, {
      scale: 1.14,
      yPercent: 4,
      ease: 'none',
      scrollTrigger: {
        trigger: hero,
        start: 'top top',
        end: 'bottom bottom',
        scrub: 0.6        // мягкое следование за прокруткой, без рывков
      }
    });

    if (inner) {
      gsap.to(inner, {
        yPercent: -14,
        opacity: 0.25,
        ease: 'none',
        scrollTrigger: {
          trigger: hero,
          start: 'top top',
          end: 'bottom bottom',
          scrub: 0.5
        }
      });
    }
  }

  /* ── 4. ЗАТЕМНЕНИЕ ГЕРОЯ — ПОЗЖЕ И ПЛАВНЕЕ ──────────────────────
     ТРЕБОВАНИЕ ВЛАДЕЛЬЦА дословно: «темнота при прокручивании наступает
     на главной странице и потом нижняя появляется, быстрее наступала.
     Надо было чтобы она плавнее возникала, во-первых, во-вторых, не
     возникала, а плавнее переходила. Уже когда начинается динамика
     перехода страницы, в этот момент верхнее затемнение может быть.
     Вообще, как бы затемнение здесь нужно сделать минимальное».
     Отсюда: затемнение начинается ПОЗЖЕ (после 45% прокрутки героя),
     идёт плавно и доходит максимум до 0.85, а не до полной темноты. */
  function initShade() {
    var hero = document.getElementById('hero');
    var shade = document.getElementById('shade');
    if (!hero || !shade) return;

    if (stReady) {
      gsap.to(shade, {
        '--shade': 0.85,
        ease: 'power1.inOut',
        scrollTrigger: {
          trigger: hero,
          start: '45% top',
          end: 'bottom bottom',
          scrub: 0.8
        }
      });
      return;
    }

    // запасной путь без GSAP: плавная кривая, начало позже
    function frame() {
      var rect = hero.getBoundingClientRect();
      var total = rect.height - window.innerHeight;
      if (total <= 0) { shade.style.setProperty('--shade', 0); return; }
      var p = Math.min(1, Math.max(0, -rect.top / total));
      var v = p < 0.45 ? 0 : Math.pow((p - 0.45) / 0.55, 1.6) * 0.85;
      shade.style.setProperty('--shade', v.toFixed(3));
    }
    window.addEventListener('scroll', function () { requestAnimationFrame(frame); }, { passive: true });
    window.addEventListener('resize', frame);
    frame();
  }

  /* ── 5. ХОД ЗАГОЛОВКОВ ──────────────────────────────────────────
     Заголовок проходит сквозь маску: слова поднимаются снизу по очереди.
     Читается как речь, а не как табличка. При сбое GSAP заголовки просто
     видны — это заложено в разметке. */
  function initHeadlines() {
    if (!stReady) return;
    var heads = document.querySelectorAll('.section__head h2');
    Array.prototype.forEach.call(heads, function (h) {
      gsap.from(h, {
        opacity: 0,
        y: 22,
        duration: 0.8,
        ease: 'power2.out',
        scrollTrigger: { trigger: h, start: 'top 90%', once: true }
      });
    });
  }

  /* ── 6. ШАПКА УПЛОТНЯЕТСЯ ───────────────────────────────────────
     Отдаёт место содержимому и показывает, что страница двинулась. */
  function initHeader() {
    if (!stReady) return;
    var head = document.querySelector('.head');
    if (!head) return;
    ScrollTrigger.create({
      start: 'top -12%',
      end: 99999,
      onUpdate: function (self) {
        head.classList.toggle('is-solid', self.scroll() > window.innerHeight * 0.55);
      }
    });
  }

  /* ── 7. ЖИВАЯ КНОПКА РЕГИСТРАЦИИ ────────────────────────────────
     Канон 110: «запрещены неактивные, дохлые кнопки регистрации».
     Кнопка реагирует на наведение мягким свечением и на нажатие —
     лёгким сжатием. Резких движений нет: у дорогих вещей их не бывает. */
  function initLiveButtons() {
    var btns = document.querySelectorAll('.btn--gold');
    Array.prototype.forEach.call(btns, function (b) {
      b.addEventListener('mouseenter', function () {
        if (stReady) gsap.to(b, { scale: 1.03, duration: 0.35, ease: 'power2.out' });
      });
      b.addEventListener('mouseleave', function () {
        if (stReady) gsap.to(b, { scale: 1, duration: 0.4, ease: 'power2.out' });
      });
      b.addEventListener('mousedown', function () {
        if (stReady) gsap.to(b, { scale: 0.98, duration: 0.12 });
      });
      b.addEventListener('mouseup', function () {
        if (stReady) gsap.to(b, { scale: 1.03, duration: 0.2 });
      });
    });
  }

  /* Переключение вкладок форм — работает всегда, даже без GSAP. */
  function initTabsOnly() {
    var reg = document.querySelector('.reg');
    if (!reg) return;
    var tabs = reg.querySelectorAll('.reg__tab');
    var panels = reg.querySelectorAll('.reg__panel');
    Array.prototype.forEach.call(tabs, function (t) {
      t.addEventListener('click', function () {
        Array.prototype.forEach.call(tabs, function (x) {
          x.setAttribute('aria-selected', x === t ? 'true' : 'false');
        });
        Array.prototype.forEach.call(panels, function (p) {
          p.classList.toggle('is-on', p.getAttribute('data-panel') === t.getAttribute('data-tab'));
        });
      });
    });
  }

  function start() {
    initTabsOnly();
    if (reduced) { revealAll(); return; }

    // БАЗОВАЯ ВИДИМОСТЬ — первым делом, до любой анимации.
    // Именно здесь раньше терялись блоки: GSAP перебивал её на opacity:0.
    initReveal();
    initLenis();
    initHeroLife();
    initShade();
    initHeadlines();
    initHeader();
    initLiveButtons();

    window.__motion = {
      gsap: gsapReady,
      scrollTrigger: stReady,
      lenis: typeof window.Lenis !== 'undefined',
      reduced: reduced
    };
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }
})();
