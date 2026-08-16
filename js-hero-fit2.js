/* Шапка страницы — перенос алгоритма главной страницы один в один.
   Черновик: подключён к samira.html и tehsil.html. После утверждения
   переносится в js-hero-fit.js и получает все страницы всех языков.

   ВСЕ ЧИСЛА СНЯТЫ С ГЛАВНОЙ ЗАМЕРОМ, не назначены. Паспорт шапки
   index.html на 375px (контейнер 335):

     объект 1 — бейдж
        14px/700, letter-spacing 1px, padding 10px 24px,
        рамка 1px solid rgba(230,180,74,.25), фон rgba(230,180,74,.1),
        line-height 14px, radius 0, uppercase, высота 36px
     объект 2 — заголовок
        строка 1: 50px, line-height 57.5px (1.15), margin-bottom 16px
        строка 2: 20px, line-height 23px (1.15)
        ширина текста обеих строк — 256px
     объект 3 — лид, три строки
        15 / 12 / 16px, line-height ровно 1.6 кегля
        ширина текста всех трёх — 242px
     объект 4 — поисковик 335×45

     зазоры по вертикали
        бейдж → заголовок      25px
        строка 1 → строка 2    16px
        заголовок → лид        20px
        между строками лида     0px (работает line-height)
        лид → поисковик        32px

   МЕРА одна на все объекты: натуральная ширина ВТОРОЙ строки заголовка
   при базовом кегле 20px. На главной это 256px. Строка 1 и каждая строка
   лида подгоняются под неё же — отсюда одинаковые края. Лид садится на
   242 вместо 256 потому, что кегль округляется вниз.

   Единственное отступление от главной — нижняя граница меры. На главной
   вторая строка «Psixologiya Məktəbi» (19 знаков) сама даёт 256px, а на
   внутренних страницах она бывает одним словом: «Terapiyası» даёт 128px,
   и тогда лид ужимается до 8px. Поэтому мера не опускается ниже 76%
   контейнера — на главной это 255px, то есть поведение главной не
   меняется ни на пиксель, а короткие заголовки перестают схлопываться. */
(function () {
  'use strict';

  var BASE_W2 = 20;      /* базовый кегль второй строки, как в CSS главной */
  var MIN_SHARE = 0.76;  /* нижняя граница меры: 0.76 × 335 = 255 ≈ 256 */
  var LH_H1 = 1.15;      /* line-height заголовка на главной */
  var LH_SUB = 1.6;      /* line-height лида на главной: 24/15, 19.2/12, 25.6/16 */
  var CAP_H1 = 64;       /* на главной строка 1 = 50px; выше уже давит страницу */

  /* Ритм РАЗДЕЛА. Снят с блока «Mütəxəssis Haqqında» на samira.html — он
     перенесён с главной страницы и, по словам владельца, единственный на
     странице выглядит аккуратно: 48px от верхней грани до бейджа и 26.6
     оптически от бейджа до заголовка. Остальные разделы имели 24 сверху,
     шапка 36, а разброс «бейдж → заголовок» доходил до 47.9 — отсюда
     ощущение, что блоки не в одной системе. Приводим ВСЕ разделы к этой
     паре, включая шапку. */
  var SEC_TOP = 48;
  var SEC_BADGE = 27;

  /* Ширина именно текста: у display:block элемента getBoundingClientRect
     возвращает ширину контейнера, мерить по нему нельзя. */
  function textWidth(el) {
    var r = document.createRange();
    r.selectNodeContents(el);
    return r.getBoundingClientRect().width;
  }

  /* Кегль ставится с приоритетом important: в gtc.css у .ph-h1 задано
     `font-size: 32px !important`, обычный inline-стиль его не перебивает.
     Из-за этого на десктопе заголовок оставался 32px, а лид растягивался
     свободно и выходил КРУПНЕЕ заголовка (замер: 481px против 886px). */
  function setSize(el, px) {
    el.style.setProperty('font-size', px + 'px', 'important');
  }

  /* Полулидинг: половина разницы интерлиньяжа и кегля. Визуально пустая
     часть строки сверху и снизу; по рамкам элемента её не видно. */
  function halfLeading(el) {
    var cs = getComputedStyle(el);
    var fs = parseFloat(cs.fontSize), lh = parseFloat(cs.lineHeight);
    if (!lh || isNaN(lh)) return 0;
    return (lh - fs) / 2;
  }

  /* Наибольший кегль, при котором текст ещё уже target. */
  function fitTo(el, target, lo, hi, cap) {
    if (!target) return 0;
    for (var i = 0; i < 28; i++) {
      var mid = (lo + hi) / 2;
      setSize(el, mid);
      if (textWidth(el) < target) lo = mid; else hi = mid;
    }
    var size = Math.floor(lo);
    if (cap && size > cap) size = cap;
    setSize(el, size);
    return size;
  }

  function fitHero(hero) {
    var h1 = hero.querySelector('.ph-h1');
    if (!h1) return;

    var badge = hero.querySelector('.ph-badge');
    var w1 = hero.querySelector('.ph-h1-w1');
    var w2 = hero.querySelector('.ph-h1-w2');
    var lead = hero.querySelector('.ph-sub');
    var sw = hero.querySelector('.ph-search-wrap');
    var inner = hero.querySelector('.page-hero-x-inner');
    var subDesk = hero.querySelectorAll('.ph-sub-desk');
    var subMob = hero.querySelectorAll('.ph-sub-mob');

    /* Сброс: без него прошлый прогон исказит измерение. */
    h1.style.cssText = '';
    if (w1) w1.style.cssText = '';
    if (w2) w2.style.cssText = '';
    if (lead) lead.style.cssText = '';
    [].forEach.call(subDesk, function (s) { s.style.cssText = ''; });
    [].forEach.call(subMob, function (s) { s.style.cssText = ''; });

    var box = inner ? inner.getBoundingClientRect().width : window.innerWidth;

    if (window.innerWidth > 768) {
      /* ── ДЕСКТОП ── строки заголовка идут в одну линию (display:inline),
         поэтому подгоняется весь <h1>. Мера — ширина поисковика: на главной
         заголовок, лид и поисковик стоят на одной вертикали. На страницах
         без поисковика держим ту же долю контейнера, что даёт поисковик
         на главной, — 53% (620 из 1164). */
      var dt = sw ? Math.round(sw.getBoundingClientRect().width)
                  : Math.round(Math.min(620, box * 0.53));
      if (!dt) dt = 620;

      h1.style.display = 'inline-block';
      h1.style.whiteSpace = 'nowrap';
      fitTo(h1, dt, 8, 120, 0);
      h1.style.display = '';
      h1.style.whiteSpace = '';

      if (lead) { lead.style.width = dt + 'px'; lead.style.maxWidth = 'none'; }
      [].forEach.call(subDesk, function (line) {
        line.style.display = 'inline';
        line.style.whiteSpace = 'nowrap';
        var s = fitTo(line, dt, 8, 48, 0);
        line.style.display = 'block';
        line.style.whiteSpace = '';
        line.style.lineHeight = (s * LH_SUB).toFixed(1) + 'px';
      });
      return;
    }

    /* ── МОБИЛЬНЫЙ ── одна мера на все объекты. */
    var target = box * MIN_SHARE;
    if (w2) {
      setSize(w2, BASE_W2);
      w2.style.display = 'inline';
      w2.style.whiteSpace = 'nowrap';
      var natural = textWidth(w2);
      if (natural > target) target = natural;
      w2.style.display = '';
      w2.style.whiteSpace = '';
    }
    if (!target) return;

    /* Строка 2 остаётся на базовом кегле, если сама задаёт меру,
       иначе растягивается до неё — как строка 1. */
    [w2, w1].forEach(function (line) {
      if (!line) return;
      line.style.display = 'inline';
      line.style.whiteSpace = 'nowrap';
      var s = fitTo(line, target, 10, 140, CAP_H1);
      line.style.display = 'block';
      line.style.textAlign = 'center';
      line.style.lineHeight = (s * LH_H1).toFixed(1) + 'px';
    });
    if (w1) w1.style.marginBottom = '16px';   /* зазор строка1→строка2 с главной */

    /* ── ОПТИЧЕСКИЕ ЗАЗОРЫ ──
       Половина разницы интерлиньяжа и кегля — пустое место внутри строки.
       Глаз видит его как отступ, getBoundingClientRect — нет. Кегль на
       каждой странице свой (подгоняется), поэтому фиксированный margin даёт
       РАЗНЫЙ видимый зазор. Считаем от цели и вычитаем полулидинг.

       Цели заданы Кенаном по месту: верхний зазор и зазор бейдж→заголовок
       должны быть равны и примерно в полтора раза больше прежних 24;
       перед панелью поиска — меньше, под ней — больше, чтобы панель
       поднялась внутри полосы. */
    var GAP_TOP = SEC_TOP;        /* верх шапки → бейдж, как в разделах */
    var GAP_BADGE = SEC_BADGE;    /* бейдж → заголовок, оптически */
    var GAP_LEAD_BAR = 30;        /* лид → панель, оптически */
    var GAP_BAR_BOTTOM = SEC_TOP; /* панель → низ шапки */

    /* important обязателен: в CSS страницы эти же свойства заданы с
       !important, обычный inline-стиль их не перебивает. */
    hero.style.setProperty('padding-bottom', GAP_BAR_BOTTOM + 'px', 'important');

    /* Как и в разделах — измеряем фактический зазор и правим на разницу:
       отступ складывается из padding шапки и внутреннего контейнера. */
    if (badge) {
      hero.style.removeProperty('padding-top');
      var gTop = badge.getBoundingClientRect().top - hero.getBoundingClientRect().top;
      var basePadTop = parseFloat(getComputedStyle(hero).paddingTop) || 0;
      hero.style.setProperty('padding-top',
        Math.max(0, basePadTop + (GAP_TOP - gTop)).toFixed(1) + 'px', 'important');
    }
    if (w1) {
      h1.style.removeProperty('margin-top');
      var gB = w1.getBoundingClientRect().top - badge.getBoundingClientRect().bottom + halfLeading(w1);
      var baseMT1 = parseFloat(getComputedStyle(h1).marginTop) || 0;
      h1.style.setProperty('margin-top',
        Math.max(-40, baseMT1 + (GAP_BADGE - gB)).toFixed(1) + 'px', 'important');
    }

    [].forEach.call(subMob, function (line) {
      line.style.display = 'inline';
      line.style.whiteSpace = 'nowrap';
      var s = fitTo(line, target, 8, 40, 0);
      line.style.display = 'block';
      line.style.whiteSpace = '';
      line.style.lineHeight = (s * LH_SUB).toFixed(1) + 'px';
    });

    if (lead && subMob.length) {
      var lastLine = subMob[subMob.length - 1];
      lead.style.setProperty('margin-bottom',
        Math.max(0, GAP_LEAD_BAR - halfLeading(lastLine)).toFixed(1) + 'px', 'important');
    }
  }

  /* Заголовок секции и его подпись — перенос блока fitAbout с главной.
     Без него «Samirə Rahimova/Rüstəmova» переносится как попало: одна
     строка короткая, вторая во всю ширину. */
  /* Ритм раздела: одинаковый для всех блоков страницы.

     Зазор НЕ задаётся напрямую: отступ до бейджа складывается из padding
     самой секции и padding внутреннего .sec-inner, а у заголовка сверху
     может стоять свой margin. Слепая установка padding-top: 48 дала 72 —
     проверено. Поэтому измеряем фактический зазор и правим на разницу. */
  function sectionRhythm(sec) {
    var badge = sec.querySelector('.badge');
    var h = sec.querySelector('h2');
    if (!badge || !h) return;

    sec.style.removeProperty('padding-top');
    h.style.removeProperty('margin-top');

    var gapTop = badge.getBoundingClientRect().top - sec.getBoundingClientRect().top;
    var basePad = parseFloat(getComputedStyle(sec).paddingTop) || 0;
    sec.style.setProperty('padding-top',
      Math.max(0, basePad + (SEC_TOP - gapTop)).toFixed(1) + 'px', 'important');

    /* Обрезка по нулю тут вредна: трём разделам зазор нужно УМЕНЬШИТЬ, а
       собственный margin у заголовка уже 0 — поправка обязана уходить в
       минус. Проверено: без этого 31.9 не опускалось до 27. */
    var gapB = h.getBoundingClientRect().top - badge.getBoundingClientRect().bottom + halfLeading(h);
    var baseMT = parseFloat(getComputedStyle(h).marginTop) || 0;
    h.style.setProperty('margin-top',
      Math.max(-40, baseMT + (SEC_BADGE - gapB)).toFixed(1) + 'px', 'important');
  }

  function fitSection(header) {
    if (window.innerWidth > 768) return;
    var h2 = header.querySelector('h2.sec-h2');
    if (!h2) return;
    var mob = header.querySelectorAll('.ab-lead-mob');
    var desk = header.querySelectorAll('.ab-lead-desk');
    [].forEach.call(desk, function (l) { l.style.cssText = 'display:none!important'; });

    var target = header.getBoundingClientRect().width - 32;  /* как на главной */
    if (!target) return;

    h2.style.cssText = '';
    h2.style.display = 'inline';
    h2.style.whiteSpace = 'nowrap';
    fitTo(h2, target, 10, 160, 0);
    h2.style.display = 'block';
    h2.style.whiteSpace = '';

    [].forEach.call(mob, function (line) {
      line.style.cssText = '';
      line.style.display = 'inline';
      line.style.whiteSpace = 'nowrap';
      var s = fitTo(line, target, 8, 60, 0);
      line.style.display = 'block';
      line.style.whiteSpace = '';
      line.style.lineHeight = (s * LH_SUB).toFixed(1) + 'px';
    });
  }

  /* Ритм и подгонка кегля зависят друг от друга: правка отступа меняет
     положение строк, а смена кегля меняет полулидинг, от которого считается
     отступ. Один проход недотягивает — замер показал 23.7 вместо 27 в шапке.
     Второй проход сходится, третий уже ничего не меняет. */
  function pass() {
    document.querySelectorAll('.page-hero-x').forEach(fitHero);
    document.querySelectorAll('.sec-header').forEach(fitSection);
    document.querySelectorAll('section').forEach(function (s) {
      if (s.classList.contains('page-hero-x')) return;
      sectionRhythm(s);
    });
  }

  function fitAll() {
    pass();
    pass();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', fitAll);
  } else {
    fitAll();
  }
  window.addEventListener('resize', fitAll, { passive: true });
  /* Шрифт грузится позже разметки — без пересчёта ширины будут от Arial. */
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(fitAll);
  }
})();
