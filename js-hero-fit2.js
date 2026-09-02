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

  /* Чернильная ширина заголовка = ширина его самой длинной ВИДИМОЙ строки.
     Раньше каждая `.sh-line` на время разворачивалась в inline+nowrap и мерилась
     целиком. Для строки, которая и так в одну физическую, это одно и то же, но
     когда авторская строка не влезает в контейнер и переносится, nowrap даёт её
     неразбитую ширину: на tehsil и valideyn-mektebi мера вышла 671 и 644 против
     видимых 590 и 587, и подзаголовок, «ровный» по этой мере, оказывался на 6—8 %
     ШИРЕ заголовка — то есть тем самым дефектом из §1. Мёрим фактические строки
     тем же widestLine(), что и подзаголовок: мера и проверяются одними чернилами. */
  function headingInk(h2) {
    /* Мера — самая широкая ВИДИМАЯ строка заголовка целиком, а не по каждой
       `.sh-line` в отдельности. Половинки автора — инлайновые: на десктопе
       «Diplomlar və» + «Sertifikatlar» стоят на одной строке 727 px, а по
       отдельности дают 437 и 291. Мерить по половинкам — значит занижать меру
       до 43 % и укладывать подзаголовок в 47—70 % вместо нормы §1. На мобильном
       те же половинки распадаются на строки, и `widestLine` снимает уже
       фактическую ширину — метод один для обоих случаев. */
    var w = widestLine(h2);
    /* Если чернил не снялось (скрытая разметка, нулевая высота), берём коробку:
       нулевая мера означала бы, что деко некуда укладывать и оно упадёт в MIN_SUB. */
    if (!w) w = h2.getBoundingClientRect().width;
    return w;
  }

  /* Сколько физических строк в элементе — по верхам прямоугольников Range.
     getClientRects() у блока таких строк не показывает. */
  function lineCount(el) {
    return lineRows(el).length;
  }

  /* Строки элемента как ряды чернил: rect'ы одной строки склеиваются по краям
     «влево-вправо», потому что внутренний span режет строку на фрагменты и по
     первому фрагменту мерится половина строки. Допуск по вертикали — половина
     высоты, а не фиксированные 3 px: половины заголовка разной высоты (курсив,
     `<sup>`) иначе разрываются на две «строки». */
  function lineRows(el) {
    var rr = document.createRange(), groups = [], i, rc, g, j;
    rr.selectNodeContents(el);
    var rs = rr.getClientRects();
    for (i = 0; i < rs.length; i++) {
      rc = rs[i];
      if (rc.height < 2 || rc.width < 1) continue;
      g = null;
      for (j = 0; j < groups.length; j++) {
        if (Math.abs(groups[j].top - rc.top) < Math.max(groups[j].height, rc.height) * 0.5) { g = groups[j]; break; }
      }
      if (!g) { g = { top: rc.top, l: rc.left, r: rc.right, height: rc.height }; groups.push(g); }
      g.height = Math.max(g.height, rc.height);
      g.l = Math.min(g.l, rc.left);
      g.r = Math.max(g.r, rc.right);
    }
    return groups;
  }

  /* Самая широкая ЧЕРНИЛЬНАЯ строка элемента. */
  function widestLine(el) {
    var rows = lineRows(el), i, w = 0;
    for (i = 0; i < rows.length; i++) w = Math.max(w, rows[i].r - rows[i].l);
    return w;
  }

  /* Подзаголовок раздела на десктопе (Кенан 03.09: «подзаголовок слишком мелкий,
     растянуть на 2 строки, разделить по словам приблизительно одинаково»).
     Строки автора — не приказ, а текст: весь подзаголовок собирается в один
     поток, переносится сам, а `text-wrap: balance` делит строки на части близкой
     длины — поэтому кегль у них общий и «ёлочки» нет. Кегль берётся наибольший
     из тех, при которых блок укладывается в MAX_SUB_LINES строк.
     Максимум строк (§1a): 3. Если и при нижнем кегле их больше — текст надо
     сокращать, а не мельчить: это сигнал на страницу, он пишется в отчёт.
     ПОТОЛОК. Ставить его нельзя в смысле §6a — там запрет на абсолютный потолок
     (20 px), который роняет ДОЛЮ: узкая строка при фиксированном кегле не
     дотягивает до заголовка. Относительный потолок долю не ломает, потому что
     доля здесь достигается числом строк, а не кеглем. Нужен он для другого:
     без потолка короткий подзаголовок раздувается до кегля заголовка — замер
     03.09 дал 30 и 37 px под заголовком 40, то есть два заголовка вместо пары.
     §1 прямо велит лечить это текстом, а не кеглем. Число 0.55 — верх наблюдаемой
     нормы сайта: 22 px подзаголовка при 40 px заголовка (§6a, «разброс 17/18/22 —
     приемлемая плата за равные ширины»). */
  var MAX_SUB_LINES = 3;
  var DESK_SHARE = 0.70;

  function fitDeskBlock(sub, h2, measure) {
    if (!sub || !measure) return;
    var headFS = parseFloat(getComputedStyle(h2).fontSize) || 40;
    var cap = Math.max(MIN_SUB, Math.round(headFS * DESK_SHARE));
    var desk = sub.querySelectorAll('[class$="-lead-desk"], [class*="-lead-desk "]');
    [].forEach.call(desk, function (l) {
      l.style.display = 'inline';
      l.style.whiteSpace = 'normal';
      l.style.setProperty('text-wrap', 'balance');
    });
    sub.style.whiteSpace = 'normal';
    sub.style.setProperty('text-wrap', 'balance');

    /* Критерий выбора кегля (Кенан 03.09: «подзаголовок слишком мелкий — если
       растянуть на 2 строчки и увеличить по размеру шрифт подзаголовка и
       разделить по словам приблизительно одинаково по длине, всё будет
       нормально»). Строки автора при этом не приказ: блок переносится сам, а
       `text-wrap: balance` делит чернила на близкие по длине части, поэтому
       «разделить приблизительно одинаково» выполняется само, без ручных переносов.

       Перебор кеглей ОТ ПОТОЛКА ВНИЗ, каждый проверяется на ФАКТИЧЕСКОЙ
       отрисовке — строки и чернильная ширина считаются после `setSize`, а не
       подсчётом «в одну строку»:

       1. первый (то есть наибольший) кегль, при котором блок укладывается в
          `MAX_SUB_LINES` строк и самая широкая строка заполняет меру на
          90—105 % (§1: ширина подзаголовка ≈ ширине заголовка);
       2. если такого нет — кегль с наибольшим заполнением из укладывающихся в
          `MAX_SUB_LINES` строк. Доля проседает потому, что текст короток
          относительно заголовка: это дефект текста (§1 «удлинять текст, а не
          раздувать кегль», §6b предел ~85 знаков), он уходит в отчёт;
       3. если ни один кегль не укладывается в `MAX_SUB_LINES` — `MIN_SUB` и
          признак `over`: текст длинен, лечить его копией, а не кеглем.

       Прежний перебор «наибольший кегль, не упёршийся в потолок» на коротком
       деке под узким заголовком давал 14 px в одну строку вместо 28 px в две
       на 94 % — то есть воспроизводил ровно ту претензию владельца, ради
       которой правка и началась. */
    var s = 0;
    /* Приоритет — кегль, а не попадание в полосу ширины. Замер прода (версия
       «до», 24 страницы) показал: у `3 Korporativ Proqram` подзаголовок стоял
       18 px в ОДНУ строку на 92 % меры — ширина была в порядке, а претензия
       владельца была именно про кегль (0,45 от заголовка). Подбор, который
       первым делом ищет 90—105 % ширины, на том же деке ушёл в 16 px, то есть
       сделал кегль ещё меньше. Поэтому: наибольший кегль не выше потолка, при
       котором блок укладывается в `MAX_SUB_LINES` строк; строки балансирует сам
       `text-wrap: balance`, а доля ширины измеряется и уходит в отчёт как
       дефект текста, если она недотянута (§1, §6b). */
    for (var t = cap; t >= MIN_SUB; t--) {
      setSize(sub, t);
      sub.style.lineHeight = (t * LH_SUB).toFixed(1) + 'px';
      if (lineCount(sub) <= MAX_SUB_LINES) { s = t; break; }
    }
    var over = !s;
    if (over) s = MIN_SUB;
    setSize(sub, s);
    sub.style.lineHeight = (s * LH_SUB).toFixed(1) + 'px';
    sub.style.lineHeight = (s * LH_SUB).toFixed(1) + 'px';

    /* Страховка от перелива. Подбор выше уже меряет фактическую отрисовку, а
       бокс дека ограничен мерой (`max-width` ставит `fitSection`), поэтому
       строка шире меры здесь быть не может. Цикл остаётся как сторож на случай,
       если порядок вызовов изменится: перелив за заголовок — тот дефект, ради
       которого всё переписывалось (§1: ширина подзаголовка ≈ ширине заголовка,
       ±10 %), и терять его молча нельзя. */
    for (var guard = 0; guard < 14 && s > MIN_SUB; guard++) {
      var wg = widestLine(sub);
      if (!wg || wg <= measure * 1.05) break;
      s -= 1;
      setSize(sub, s);
      sub.style.lineHeight = (s * LH_SUB).toFixed(1) + 'px';
    }

    /* Отчёт на страницу. Механизм честен только в том, что умеет: уложить в
       три строки и выровнять по мере. Если и при нижнем кегле строк больше,
       или верхняя строка не дотягивает до 90 % меры — это не дефект вёрстки,
       а текст не подходит к заголовку (§1: «слишком коротко — удлинять
       текст, а не раздувать кегль»; §6b: предел ~85 знаков). Упор кегля в
       потолок сам по себе дефектом не считается: замер 03.09 показал 15
       таких мест, и везде доля оставалась 89—99 %, то есть пара была
       ровной, просто текст не требовал крупнее. Признак висит на элементе,
       поэтому замерщик видит его без консоли; вывод в консоль включается
       флагом window.__ffDebug.
       Rect'ы одной строки суммируются по краям, а не берутся по первому:
       внутренний span режет строку на фрагменты, и «первый фрагмент» мерит
       половину строки — на этом спотыкался первый замер (ложные 29 %). */
    var widest = widestLine(sub);
    var h2el = sub.parentElement ? sub.parentElement.querySelector('h2.sec-h2') : null;
    sub.__ffM = Math.round(measure);
    sub.__ffW = widest ? Math.round(widest) : 0;
    sub.__ffN = lineCount(sub);
    sub.__ffS = s;
    sub.__ffH = h2el ? Math.round(parseFloat(getComputedStyle(h2el).fontSize)) : 0;
    sub.__ffIssue = over ? 'строк > ' + MAX_SUB_LINES + ' при ' + MIN_SUB + 'px'
      : (widest && widest < measure * 0.9 ? 'доля ' + Math.round(widest / measure * 100) + '%' : '');
    if (sub.__ffIssue && window.__ffDebug) {
      console.warn('[hero-fit] ' + sub.__ffIssue + ' — ' +
                   (sub.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 46) + '…');
    }
    return s;
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

    /* Заголовок подтягивается к ТОЙ ЖЕ мере, что и подзаголовок. Иначе
       выходило 250/245 у заголовка против 293/287/282 у подзаголовка:
       строки внутри каждого блока ровные, а блоки между собой нет, и
       правый край пары всё равно рваный. Меру задаёт самая длинная строка
       пары, и к ней тянутся оба. */
    if (natural > target + 1) {
      [w2, w1].forEach(function (line) {
        if (!line) return;
        line.style.display = 'inline';
        line.style.whiteSpace = 'nowrap';
        var sT = fitTo(line, natural, 10, 140, CAP_H1);
        line.style.display = 'block';
        line.style.textAlign = 'center';
        line.style.lineHeight = (sT * LH_H1).toFixed(1) + 'px';
      });
    }
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

    /* Сброс подзаголовка к авторскому состоянию. Простой cssText='' стёр бы
       инлайн-цвет тёмных секций (haqqimda: style="color:rgba(255,255,255,0.6)"),
       и текст провалился бы в тёмное поле — первый прогон запоминает оригинал. */
    var subEl = h2.parentElement ? h2.parentElement.querySelector('.sec-sub') : null;
    if (subEl) {
      if (subEl.__ffStyle === undefined) subEl.__ffStyle = subEl.getAttribute('style') || '';
      subEl.setAttribute('style', subEl.__ffStyle);
    }

    if (window.innerWidth > 768) {
      /* ДЕСКТОП. Мера пары — чернильная ширина строки заголовка, а не блок.
         `textWidth(h2)` у заголовка, разложенного на `.sh-line {display:block}`,
         возвращает ширину контейнера: Range по содержимому блока даёт прямоугольник
         блока (1250px), а не текста. Замер 03.09 на 1366: чернила заголовка
         «3 Korporativ / Proqram» — 423px, скрипт же мерил 1250px, поэтому
         подзаголовок растягивался в одну строку на всю колонку (114 знака при 22px).
         Доли «100 / 98 / 98 / 100» из DESIGN-STANDARD считались той же меркой —
         по блокам, а не по чернилам; настоящая доля на samira — 132 / 143 / 172 / 152 %,
         на шестнадцати страницах разброс 92—199 %. */
      var dTarget = headingInk(h2);
      if (dTarget) {
        var subP = h2.parentElement.querySelector('.sec-sub');
        if (subP) {
          subP.style.setProperty('max-width', Math.ceil(dTarget) + 'px', 'important');
          subP.style.setProperty('margin-left', 'auto');
          subP.style.setProperty('margin-right', 'auto');
        }
        fitDeskBlock(subP, h2, dTarget);
      }
      return;
    }

    [].forEach.call(desk, function (l) { l.style.cssText = 'display:none!important'; });

    var target = header.getBoundingClientRect().width - 32;  /* как на главной */
    if (!target) return;

    /* Заголовок раздела теперь разбит на строки-спаны (.sh-line), как в
       шапке. Если они есть — равняем КАЖДУЮ по общей мере: именно этого не
       хватало, чтобы пара сходилась. Ширина многострочного заголовка это
       длиннейшая строка, а не блок, и без разбивки подзаголовок всегда
       перетягивал. */
    var hLines = h2.querySelectorAll('.sh-line');
    h2.style.cssText = '';
    if (hLines.length > 1) {
      var hSizes = [];
      [].forEach.call(hLines, function (line) {
        line.style.cssText = '';
        line.style.display = 'inline';
        line.style.whiteSpace = 'nowrap';
        var sL = fitTo(line, target, MIN_H2 - 6, 160, 0);
        hSizes.push(sL);
        line.style.display = 'block';
        line.style.whiteSpace = '';
        line.style.lineHeight = (sL * LH_H1).toFixed(1) + 'px';
      });
      var sH = Math.max.apply(null, hSizes);
      var subPmL = h2.parentElement.querySelector('.sec-sub');
      if (subPmL) {
        subPmL.style.setProperty('max-width', Math.ceil(target) + 'px', 'important');
        subPmL.style.setProperty('margin-left', 'auto');
        subPmL.style.setProperty('margin-right', 'auto');
      }
      [].forEach.call(mob, function (line) {
        line.style.cssText = '';
        line.style.display = 'inline';
        line.style.whiteSpace = 'nowrap';
        var s2 = fitTo(line, target, MIN_SUB, Math.max(MIN_SUB + 1, sH - 2), 0);
        line.style.display = 'block';
        line.style.whiteSpace = 'normal';
        line.style.lineHeight = (s2 * LH_SUB).toFixed(1) + 'px';
      });
      return;
    }
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

  /* ── СТОРОЖ КОНТРАСТА ──────────────────────────────────────────────────
     Тёмная буква на тёмном фоне встречалась на сайте 64 раза, и правилами
     CSS её вывести не удалось: признак темы у секции говорит «светлая», а
     фон задан тёмным инлайн-стилем, поэтому привязка к атрибуту лишь
     переставляла дефект с места на место.

     Здесь дефект определяется по факту: считается настоящий контраст с
     учётом полупрозрачных слоёв, и если он ниже 3:1 — текст перекрашивается
     в читаемый. Светлый на тёмном, тёмный на светлом; ничего иного сторож
     не трогает, поэтому задуманная палитра остаётся на месте везде, где
     она читается. */
  function relLum(c) {
    var f = function (v) { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
    return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2]);
  }
  function parseColor(s) {
    var m = String(s).match(/[\d.]+/g);
    return m ? m.map(Number) : [0, 0, 0, 1];
  }
  /* Фон складывается по слоям: полупрозрачная подложка сама по себе цвет
     не задаёт, и без композитинга rgba читается как сплошная заливка. */
  function backdrop(el) {
    var layers = [], n = el;
    while (n && n.nodeType === 1) {
      var c = parseColor(getComputedStyle(n).backgroundColor);
      var a = c.length > 3 ? c[3] : 1;
      if (a > 0) { layers.push([c[0], c[1], c[2], a]); if (a >= 1) break; }
      n = n.parentElement;
    }
    if (!layers.length) return [11, 14, 17];
    var base = layers[layers.length - 1].slice(0, 3);
    for (var i = layers.length - 2; i >= 0; i--) {
      var l = layers[i];
      base = [l[0] * l[3] + base[0] * (1 - l[3]),
              l[1] * l[3] + base[1] * (1 - l[3]),
              l[2] * l[3] + base[2] * (1 - l[3])];
    }
    return base;
  }
  function ratio(a, b) {
    var l1 = relLum(a), l2 = relLum(b);
    return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
  }
  function guardContrast() {
    var nodes = document.querySelectorAll('body *');
    for (var i = 0; i < nodes.length; i++) {
      var el = nodes[i], own = false;
      for (var k = 0; k < el.childNodes.length; k++) {
        if (el.childNodes[k].nodeType === 3 && el.childNodes[k].textContent.trim()) { own = true; break; }
      }
      if (!own) continue;
      var cs = getComputedStyle(el);
      if (cs.display === 'none' || cs.visibility === 'hidden') continue;
      if (!el.getClientRects().length) continue;
      var f = parseColor(cs.color), fa = f.length > 3 ? f[3] : 1;
      var bg = backdrop(el);
      var fg = [f[0] * fa + bg[0] * (1 - fa), f[1] * fa + bg[1] * (1 - fa), f[2] * fa + bg[2] * (1 - fa)];
      if (ratio(fg, bg) >= 3) continue;
      /* тёмный фон — светлая буква, светлый фон — тёмная */
      el.style.setProperty('color', relLum(bg) < 0.25 ? '#EAECEF' : '#0B0E11', 'important');
    }
  }
  window.addEventListener('load', guardContrast);
  setTimeout(guardContrast, 1200);

})();
