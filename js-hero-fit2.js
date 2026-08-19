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
  /* Ниже 13px подзаголовок на телефоне не читается. Замер на 375 без
     порога давал 9px. */
  var MIN_SUB = 13;
  /* Нижняя граница кегля заголовка раздела на мобильном. Без неё заголовок
     сжимается, лишь бы влезть в одну строку, а levelH2 потом раздаёт этот
     кегль всем заголовкам страницы. На aile-terapiyasi самый длинный —
     «Ailə Terapiyası Haqqında Məqalələr», 34 знака: замер дал 18px ВСЕМ семи
     заголовкам при подзаголовке 16px. Иерархия пропадала — заголовок и
     подзаголовок читались одним уровнем. Заголовку лучше перенестись на две
     строки, чем сравняться с подзаголовком. */
  var MIN_H2 = 24;
  var SEC_TOP = 48;
  var SEC_BADGE = 27;

  /* Ширина именно текста: у display:block элемента getBoundingClientRect
     возвращает ширину контейнера, мерить по нему нельзя. */
  /* Ширина ТЕКСТА, а не блока. Для одной строки достаточно объединяющего
     прямоугольника. Для текста, разложенного на несколько строк, этот
     прямоугольник равен ширине контейнера и врёт: заголовок «Samirə
     Rəhimova/Rüstəmova» на 375px мерился как 343px, хотя длиннейшая его
     строка занимает заметно меньше. В таком случае берём максимум по
     строкам — но только тогда, иначе на однострочном элементе с вложенными
     span максимум вернёт ширину одного span (проверено: 263% против
     реальных 99%). */
  function textWidth(el) {
    var r = document.createRange();
    r.selectNodeContents(el);
    var box = r.getBoundingClientRect();
    var rects = r.getClientRects();
    if (rects.length < 2) return box.width;
    var tops = [], i;
    for (i = 0; i < rects.length; i++) {
      var top = Math.round(rects[i].top);
      if (tops.indexOf(top) < 0) tops.push(top);
    }
    if (tops.length < 2) return box.width;      /* один ряд — блок и есть текст */
    var widest = 0;
    for (i = 0; i < tops.length; i++) {
      var lineW = 0, j;
      for (j = 0; j < rects.length; j++) {
        if (Math.round(rects[j].top) === tops[i]) lineW += rects[j].width;
      }
      if (lineW > widest) widest = lineW;
    }
    return widest || box.width;
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
      var deskSizes = [];
      [].forEach.call(subDesk, function (line) {
        line.style.display = 'inline';
        line.style.whiteSpace = 'nowrap';
        deskSizes.push(fitTo(line, dt, 8, 48, 0));
        line.style.display = 'block';
        line.style.whiteSpace = '';
      });
      /* Интерлиньяж ОДИН на все строки подзаголовка. Считать его от кегля
         каждой строки нельзя: строки разного кегля (25 и 29) дают 40 и 46.4,
         и промежутки внутри одного абзаца выходят разными — это видно глазом.
         Берём по самой крупной строке. */
      /* Как и на мобильном: ширины равны, интерлиньяж — от кегля своей
         строки. */
      [].forEach.call(subDesk, function (line) {
        var szD = parseFloat(getComputedStyle(line).fontSize) || 8;
        line.style.lineHeight = (szD * LH_SUB).toFixed(1) + 'px';
      });

      /* Зазор бейдж → заголовок нужен и на десктопе: раньше ветка выходила
         до блока отступов, и в шапке оставалось 26 вместо 40. */
      if (badge && w1) {
        h1.style.removeProperty('margin-top');
        var gD = w1.getBoundingClientRect().top - badge.getBoundingClientRect().bottom + halfLeading(w1);
        var baseD = parseFloat(getComputedStyle(h1).marginTop) || 0;
        h1.style.setProperty('margin-top',
          Math.max(-40, baseD + (40 - gD)).toFixed(1) + 'px', 'important');
      }
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
    /* В шапке зазор после бейджа БОЛЬШЕ, чем в разделах: заголовок здесь
       крупный (43px против 40px в разделах и куда крупнее на мобильном),
       и та же цифра 27 читается как теснота. Кенан 2026-08-17. */
    var GAP_BADGE = 40;           /* бейдж → заголовок в шапке, оптически */
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

    /* Мера блока берётся в два прохода. Сначала каждая строка подгоняется
       под расчётную ширину; если самая длинная не влезает даже на нижнем
       кегле, она сама и задаёт меру — иначе она осталась бы шире прочих и
       правый край всё равно был бы рваным. Вторым проходом остальные
       строки подтягиваются к этой мере. */
    var mobSizes = [];
    var natural = target;
    [].forEach.call(subMob, function (line) {
      line.style.display = 'inline';
      line.style.whiteSpace = 'nowrap';
      setSize(line, MIN_SUB);
      var atMin = textWidth(line);
      if (atMin > natural) natural = atMin;
      line.style.display = 'block';
      line.style.whiteSpace = '';
    });
    [].forEach.call(subMob, function (line) {
      line.style.display = 'inline';
      line.style.whiteSpace = 'nowrap';
      var sM = fitTo(line, natural, MIN_SUB, 40, 0);
      if (sM < MIN_SUB) { sM = MIN_SUB; setSize(line, sM); }
      mobSizes.push(sM);
      line.style.display = 'block';
      line.style.whiteSpace = '';
    });
    /* Абзац прозы набирается ОДНИМ кеглем. Подгонять каждую строку под
       общую ширину — приём для заголовка, где слова стоят столбиком; в
       подзаголовке он давал «Qəfil narahatlıq,» 32px и «panik
       bozğunluğunun müalicəsi.» 15px в одном предложении, а интерлиньяж
       считался по самой крупной строке и на мелкой выглядел провалом
       (51px при кегле 15). Берём наименьший из подогнанных: он
       гарантирует, что самая длинная строка помещается по ширине. */
    /* Строки подзаголовка выравниваются ПО ШИРИНЕ, а не по кеглю: короткая
       строка набирается крупнее, длинная мельче, и правый край блока
       становится ровным — тот же приём, что уже работает у заголовка
       (28 и 21px дают 250 и 245px). Это канон владельца.

       Интерлиньяж при этом считается от кегля СВОЕЙ строки. Раньше он
       брался по самой крупной, и на мелкой строке выходило 51px при кегле
       15 — множитель 3.4 вместо 1.6, что и читалось как «слишком большой
       интервал». Разброс кеглей сам по себе не порок; порок — интервал,
       посчитанный не от той строки. */
    [].forEach.call(subMob, function (line) {
      var sz = parseFloat(getComputedStyle(line).fontSize) || MIN_SUB;
      line.style.lineHeight = (sz * LH_SUB).toFixed(1) + 'px';
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
    /* Скрытые секции пропускаем. У display:none все размеры нулевые, и замер
       выдаёт мусор: на tehsil форма отзыва (#reviewFormSection) показала
       зазор 0 вместо 48, и скрипт записывал ей случайную поправку, которая
       вылезла бы в момент открытия формы. */
    if (!sec.getClientRects().length) return;

    sec.style.removeProperty('padding-top');
    h.style.removeProperty('margin-top');

    /* Отступ сверху создаёт не только сама секция, но и внутренний
       .sec-inner со своим padding. Когда правка уходит в минус, а padding
       секции уже 0, Math.max(0,…) её съедает и зазор застревает: три
       раздела держали 55 вместо 48. Остаток переносим на .sec-inner. */
    var inner = sec.querySelector('.sec-inner');
    if (inner) inner.style.removeProperty('padding-top');
    var gapTop = badge.getBoundingClientRect().top - sec.getBoundingClientRect().top;
    var basePad = parseFloat(getComputedStyle(sec).paddingTop) || 0;
    var wantPad = basePad + (SEC_TOP - gapTop);
    sec.style.setProperty('padding-top', Math.max(0, wantPad).toFixed(1) + 'px', 'important');
    if (wantPad < 0 && inner) {
      var baseIn = parseFloat(getComputedStyle(inner).paddingTop) || 0;
      inner.style.setProperty('padding-top',
        Math.max(0, baseIn + wantPad).toFixed(1) + 'px', 'important');
    }

    /* Обрезка по нулю тут вредна: трём разделам зазор нужно УМЕНЬШИТЬ, а
       собственный margin у заголовка уже 0 — поправка обязана уходить в
       минус. Проверено: без этого 31.9 не опускалось до 27. */
    /* Нижний зазор. Кенан: «текст не должен быть прижат к стенке, зазор
       должен быть пропорционален тому, что выше». Последняя строка текста
       упиралась прямо в серую полосу следующего блока. Делаем снизу
       столько же, сколько сверху. Ищем нижнюю границу самого нижнего
       содержимого, а не последнего ребёнка: он может быть пустым. */
    sec.style.removeProperty('padding-bottom');
    /* Только ПРЯМЫЕ дети: их рамка уже включает всё содержимое. Обход всех
       потомков затягивал в расчёт скрытый <ol> внутри закрытого <details> —
       у раздела программ padding-bottom вырастал до 534px и на странице
       зияла дыра. */
    /* Нижняя граница содержимого — по последнему СОДЕРЖАТЕЛЬНОМУ элементу.
       Считать по .sec-inner нельзя: его собственный padding добавлялся к
       зазору, и от кнопки до края раздела выходило 103 вместо 48. Обход
       всех потомков тоже не годится — затягивает скрытый <ol> внутри
       закрытого <details>. */
    var deepest = 0;
    [].forEach.call(sec.querySelectorAll('p, h1, h2, h3, a, ul, ol, img, .btn, .stat-item, .mod-panel'),
      function (el) {
        if (el.closest('details') && !el.closest('details').open) return;
        var r = el.getBoundingClientRect();
        if (r.height > 0 && r.bottom > deepest) deepest = r.bottom;
      });
    if (!deepest) {
      [].forEach.call(sec.children, function (el) {
        var r = el.getBoundingClientRect();
        if (r.height > 0 && r.bottom > deepest) deepest = r.bottom;
      });
    }
    if (deepest) {
      var innerB = sec.querySelector('.sec-inner');
      if (innerB) innerB.style.removeProperty('padding-bottom');
      var gapBot = sec.getBoundingClientRect().bottom - deepest;
      var basePadB = parseFloat(getComputedStyle(sec).paddingBottom) || 0;
      var wantB = basePadB + (SEC_TOP - gapBot);
      sec.style.setProperty('padding-bottom', Math.max(0, wantB).toFixed(1) + 'px', 'important');
      if (wantB < 0 && innerB) {
        var baseInB = parseFloat(getComputedStyle(innerB).paddingBottom) || 0;
        innerB.style.setProperty('padding-bottom',
          Math.max(0, baseInB + wantB).toFixed(1) + 'px', 'important');
      }
    }

    var gapB = h.getBoundingClientRect().top - badge.getBoundingClientRect().bottom + halfLeading(h);
    var baseMT = parseFloat(getComputedStyle(h).marginTop) || 0;
    h.style.setProperty('margin-top',
      Math.max(-40, baseMT + (SEC_BADGE - gapB)).toFixed(1) + 'px', 'important');
  }

  function fitSection(header) {
    var h2 = header.querySelector('h2.sec-h2');
    if (!h2) return;
    /* Классы строк подзаголовка исторически именуются по разделу: ab-lead-*
       на samira, pr-lead-* на tehsil. Скрипт знал только ab-, и на tehsil
       подгонка молча не срабатывала: замер дал 263 % в разделе программ —
       подзаголовок втрое шире своего заголовка. Ищем по суффиксу. */
    var mob = header.querySelectorAll('[class$="-lead-mob"], [class*="-lead-mob "]');
    var desk = header.querySelectorAll('[class$="-lead-desk"], [class*="-lead-desk "]');

    /* Сброс ДО проверки ширины. Раньше выход стоял первой строкой, и при
       переходе с узкого экрана на широкий инлайн-кегли, выставленные для
       мобильного, оставались: заголовки разделов застревали на 10px —
       нижней границе бинарного поиска. Замер на 1366 показал h2 = 10px
       во всех пяти разделах. */
    h2.style.removeProperty('font-size');
    [].forEach.call(mob, function (l) { l.style.cssText = ''; });
    [].forEach.call(desk, function (l) { l.style.cssText = ''; });

    if (window.innerWidth > 768) {
      /* ДЕСКТОП. Раньше здесь стоял просто return, и подзаголовки разделов
         не подгонялись вовсе: кегль оставался 18px из CSS, а ширина
         получалась случайной — замер дал 52 / 63 / 78 / 121% от ширины
         заголовка вместо нормы ±10%. Заголовок на десктопе не трогаем
         (40px по CSS, как на главной), а строки подзаголовка сводим к его
         ширине. */
      var dTarget = textWidth(h2);
      if (dTarget) {
        /* В gtc.css у `.sec-sub` стоит max-width: 650px, а заголовок бывает
           шире — «Ailə Münasibətləri Haqqında» это 786px. Подогнанная строка
           в 650 не влезала и переносилась, ширина падала с 786 до 548 и
           баланс пары рушился. Даём подзаголовку ровно ширину заголовка. */
        var subP = h2.parentElement.querySelector('.sec-sub');
        if (subP) {
          subP.style.setProperty('max-width', Math.ceil(dTarget) + 'px', 'important');
          subP.style.setProperty('margin-left', 'auto');
          subP.style.setProperty('margin-right', 'auto');
        }
        [].forEach.call(desk, function (line) {
          line.style.display = 'inline';
          line.style.whiteSpace = 'nowrap';
          /* Потолок кегля здесь ставить нельзя. Пробовал 20px, чтобы убрать
             разброс подзаголовков (17 / 18 / 22 в соседних разделах
             aile-terapiyasi) — на samira это уронило доли со 100 / 98 / 98 / 100
             до 66 / 98 / 82 / 82, то есть сломало ГЛАВНОЕ правило владельца
             ради косметики. Ширина пары важнее одинакового кегля. */
          var s = fitTo(line, dTarget, 8, 48, 0);
          line.style.display = 'block';
          line.style.whiteSpace = '';
          line.style.lineHeight = (s * LH_SUB).toFixed(1) + 'px';
        });
      }
      return;
    }

    [].forEach.call(desk, function (l) { l.style.cssText = 'display:none!important'; });

    var target = header.getBoundingClientRect().width - 32;  /* как на главной */
    if (!target) return;

    h2.style.cssText = '';
    h2.style.display = 'inline';
    h2.style.whiteSpace = 'nowrap';
    var sH = fitTo(h2, target, MIN_H2, 160, 0);
    /* Упёрлись в пол — значит в одну строку текст не входит. Снимаем nowrap
       и отдаём заголовок на перенос: две строки крупным кеглем читаются, одна
       строка кеглем подзаголовка — нет. */
    if (sH <= MIN_H2) setSize(h2, MIN_H2);
    h2.style.display = 'block';
    h2.style.whiteSpace = '';

    /* ГЛАВНОЕ ПРАВИЛО ПАРЫ «заголовок ↔ подзаголовок» (скилл kenan-design-rules):
       подзаголовок по ширине ≈ заголовку, ±10%. Не по ширине контейнера!
       Замер до правки: 52 / 63 / 78 / 121% — ни один раздел в норму не попадал.
       Мера для строк подзаголовка — ширина ТЕКСТА заголовка после его подгонки. */
    /* На МОБИЛЬНОМ мера подзаголовка — контейнер, а не ширина заголовка.
       Правило «равная ширина» — типографика широкого блока; на 375px
       заголовок сам сжат, и привязка к нему давала кегль 9–15px, то есть
       нечитаемо, а в двух разделах подзаголовок всё равно выходил вдвое
       шире заголовка, упёршись в нижнюю границу поиска. Скилл
       kenan-design-rules это допускает: на мобайле сохраняется ПОРЯДОК,
       размеры адаптируются. */
    /* Пара выравнивается и на мобильном — по требованию владельца. Но
       мерой служит НЕ кегль, а ширина блока: подзаголовок секции обычно не
       разбит на строки вручную и переносится сам, поэтому достаточно
       ограничить его max-width шириной заголовка. Кегль остаётся читаемым,
       а правый край блока совпадает с заголовком.

       Нижняя граница 78% контейнера: у короткого заголовка («Kənan
       Rəhimov») привязка один в один сжала бы текст в узкую колонку из
       обрывков. Ширина заголовка при этом остаётся потолком. */
    var subPm = h2.parentElement.querySelector('.sec-sub');
    var h2w = textWidth(h2);
    var subTarget = Math.min(target, Math.max(h2w, target * 0.78));
    if (subPm) {
      subPm.style.setProperty('max-width', Math.ceil(subTarget) + 'px', 'important');
      subPm.style.setProperty('margin-left', 'auto');
      subPm.style.setProperty('margin-right', 'auto');
    }

    /* max-width только ограничивает — короткий подзаголовок так и остаётся
       уже заголовка. Если текст помещается в одну строку, подтягиваем его
       кеглем до той же меры: пара выравнивается с обеих сторон, а не
       только сверху. Потолок MIN_H2 - 4 держит подзаголовок мельче
       заголовка, как и требует правило. */
    if (subPm && !mob.length) {
      var probe = subPm.cloneNode(true);
      probe.style.cssText = 'position:absolute;visibility:hidden;white-space:nowrap;' +
                            'max-width:none;display:inline-block;left:-9999px';
      subPm.parentNode.appendChild(probe);
      var oneLine = probe.getBoundingClientRect().width;
      probe.parentNode.removeChild(probe);
      if (oneLine && oneLine <= subTarget * 1.05) {
        subPm.style.setProperty('white-space', 'nowrap');
        fitTo(subPm, subTarget, MIN_SUB, MIN_H2 - 4, 0);
        subPm.style.removeProperty('white-space');
      }
    }
    var mobSubSizes = [];
    [].forEach.call(mob, function (line) {
      line.style.cssText = '';
      line.style.display = 'inline';
      line.style.whiteSpace = 'nowrap';
      /* Потолок MIN_H2 - 6. На мобильном мера — контейнер, и короткая строка
         («İki modul, hər biri 16 dərs.») растягивалась до 27px при заголовке
         24px: подзаголовок выходил КРУПНЕЕ заголовка, а потом ещё и не влезал
         и ломался на 4 строки. Здесь потолок безопасен — в отличие от
         десктопа, где мера это ширина заголовка и потолок ломает правило пары. */
      var s = fitTo(line, subTarget, MIN_SUB, MIN_H2 - 6, 0);
      if (s < MIN_SUB) { s = MIN_SUB; setSize(line, s); }
      mobSubSizes.push(s);
      line.style.display = 'block';
      line.style.whiteSpace = 'normal';
    });
    if (mobSubSizes.length) {
      var lhS = (Math.max.apply(null, mobSubSizes) * LH_SUB).toFixed(1) + 'px';
      [].forEach.call(mob, function (line) { line.style.lineHeight = lhS; });
    }
  }

  /* Ритм и подгонка кегля зависят друг от друга: правка отступа меняет
     положение строк, а смена кегля меняет полулидинг, от которого считается
     отступ. Один проход недотягивает — замер показал 23.7 вместо 27 в шапке.
     Второй проход сходится, третий уже ничего не меняет. */
  /* Заголовки разделов — ОДИН кегль на всю страницу.
     Подгонка каждого под общую ширину даёт разный кегль: «Ailə Terapiyası»
     (15 знаков) выходил 41px, «Ailə Münasibətləri Haqqında» (27) — 21px.
     Заголовки одного уровня обязаны быть одного размера, иначе иерархия
     рассыпается. Берём наименьший из подогнанных и ставим всем: тогда ни
     один не вылезет за меру. */
  function levelH2() {
    if (window.innerWidth > 768) return;
    var hs = [];
    document.querySelectorAll('h2.sec-h2').forEach(function (h) {
      var v = parseFloat(h.style.fontSize);
      if (v) hs.push({ el: h, size: v });
    });
    if (hs.length < 2) return;
    var min = hs.reduce(function (a, b) { return a.size < b.size ? a : b; }).size;
    hs.forEach(function (x) { setSize(x.el, min); });
  }

  function pass() {
    document.querySelectorAll('.page-hero-x').forEach(fitHero);
    /* Заголовочным блоком считается РОДИТЕЛЬ h2.sec-h2, а не только
       обёртка .sec-header. На samira и tehsil это тот же самый узел —
       h2 лежит внутри .sec-header. Но на большинстве страниц сайта
       (aile-terapiyasi и её родня) бейдж, заголовок и подзаголовок лежат
       прямо в .sec-inner, без обёртки, и подгонка их просто не находила:
       замер дал 70 / 82 / 61 / 41% вместо нормы ±10%. */
    var headers = [];
    document.querySelectorAll('h2.sec-h2').forEach(function (h) {
      var box = h.closest('.sec-header') || h.parentElement;
      if (box && headers.indexOf(box) < 0) headers.push(box);
    });
    headers.forEach(fitSection);
    levelH2();
    document.querySelectorAll('section').forEach(function (s) {
      if (s.classList.contains('page-hero-x')) return;
      sectionRhythm(s);
    });
  }

  /* ВНУТРЕННИЙ РИТМ РАЗДЕЛА.
     Замер раздела «Konsultasiya» до правки: подзаголовок → текст 71,
     текст → кнопка 33, кнопка → низ 103. Большой, маленький, снова
     большой — блоки не читаются как одна система. Ставим одну единицу
     между разнородными блоками: 40. Считается оптически, с вычетом
     полулидинга: у абзаца 14px с интерлиньяжем 24.5 сверху и снизу по
     5px пустоты, которой не видно в рамках. */
  var SEC_INNER = 40;

  function innerRhythm(sec) {
    var sub = sec.querySelector('.sec-sub');
    var body = sec.querySelector('.sec-body, .mod-foot');
    var btn = sec.querySelector('.btn');
    var btnRow = btn ? btn.parentElement : null;

    /* Правило действует, только если текст идёт СРАЗУ за подзаголовком.
       В разделе программ между ними стоят две панели модулей, и замер
       давал 743px — попытка «сжать» этот зазор до 40 схлопнула бы панели. */
    if (sub && body) {
      body.style.removeProperty('margin-top');
      var g1 = body.getBoundingClientRect().top - sub.getBoundingClientRect().bottom
               + halfLeading(sub) + halfLeading(body);
      if (g1 < 200) {
        var b1 = parseFloat(getComputedStyle(body).marginTop) || 0;
        body.style.setProperty('margin-top',
          Math.max(0, b1 + (SEC_INNER - g1)).toFixed(1) + 'px', 'important');
      }
    }
    if (btnRow && body && btnRow !== body) {
      btnRow.style.removeProperty('margin-top');
      var g2 = btn.getBoundingClientRect().top - body.getBoundingClientRect().bottom
               + halfLeading(body);
      var b2 = parseFloat(getComputedStyle(btnRow).marginTop) || 0;
      btnRow.style.setProperty('margin-top',
        Math.max(0, b2 + (SEC_INNER - g2)).toFixed(1) + 'px', 'important');
    }
  }

  function inner() {
    document.querySelectorAll('section').forEach(function (s) {
      if (!s.classList.contains('page-hero-x')) innerRhythm(s);
    });
  }

  /* Порядок важен: внутренний ритм сдвигает содержимое, значит нижний
     зазор надо пересчитать ПОСЛЕ него. Раньше цикл кончался на inner(),
     и от кнопки до края раздела оставалось 55 вместо 48. */
  function fitAll() {
    pass();
    inner();
    pass();
    inner();
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
