/* Page Hero — подгонка кегля под общую ширину.
   Подключается всеми страницами с .page-hero-x.

   ЗАЧЕМ ПЕРЕПИСАНО (Кенан 2026-08-16: «на всех других страницах этот
   шаблон не держится на мобильной версии, поэтому коряво выглядит»).

   Эталон — шапка главной страницы; её алгоритм живёт внутри index.html
   и работает так:

     target = натуральная ширина ВТОРОЙ строки заголовка при её CSS-кегле
     первая строка  → бинарным поиском подгоняется под target
     строки лида    → каждая подгоняется под тот же target

   Из-за этого «PEŞƏKAR» выходит крупным, «PSİXOLOGİYA MƏKTƏBİ» остаётся
   мелким, и обе строки заканчиваются на одной вертикали. Контраст кеглей
   получается сам собой: короткой строке, чтобы добрать до той же ширины,
   нужен больший кегль.

   Прежняя версия этого файла делала два других действия:
     1. брала target = ширина контейнера − 40, а не ширину второй строки;
     2. подгоняла ВЕСЬ <h1> целиком, а не строки по отдельности.
   Поскольку .ph-h1-w1/.ph-h1-w2 на мобильном display:block, измерение
   всего <h1> в nowrap возвращало ширину самой длинной строки — обе строки
   получали ОДИН кегль, контраст пропадал, а короткая строка не добирала
   до края. Лид при этом равнялся на контейнер, а не на заголовок, и
   строки разъезжались сильнее, чем на главной.

   Десктопная ветка не менялась: там строки идут в одну линию (display:inline),
   и подгонка всего <h1> под ширину поисковика — верное поведение. */
(function () {
  'use strict';

  /* Бинарный поиск максимального кегля, при котором элемент уже target. */
  function fitTo(el, target, lo, hi) {
    if (!target) return;
    for (var i = 0; i < 30; i++) {
      var mid = (lo + hi) / 2;
      el.style.fontSize = mid + 'px';
      if (el.getBoundingClientRect().width < target) lo = mid;
      else hi = mid;
    }
    el.style.fontSize = Math.floor(lo) + 'px';
  }

  function fitOne() {
    document.querySelectorAll('.page-hero-x').forEach(function (hero) {
      var h1 = hero.querySelector('.ph-h1');
      if (!h1) return;

      var w1 = hero.querySelector('.ph-h1-w1');
      var w2 = hero.querySelector('.ph-h1-w2');
      var lead = hero.querySelector('.ph-sub');
      var sw = hero.querySelector('.ph-search-wrap');
      var subDesk = hero.querySelectorAll('.ph-sub-desk');
      var subMob = hero.querySelectorAll('.ph-sub-mob');

      /* Сброс: иначе прошлый прогон исказит измерение. */
      h1.style.cssText = '';
      if (w1) w1.style.cssText = '';
      if (w2) w2.style.cssText = '';
      if (lead) lead.style.cssText = '';
      [].forEach.call(subDesk, function (s) { s.style.cssText = ''; });
      [].forEach.call(subMob, function (s) { s.style.cssText = ''; });

      if (window.innerWidth > 768) {
        /* ── ДЕСКТОП: строки в одну линию, равняемся на поисковик ── */
        var dt = sw ? Math.round(sw.getBoundingClientRect().width) : 620;
        if (!dt) dt = 620;

        h1.style.display = 'inline-block';
        h1.style.whiteSpace = 'nowrap';
        fitTo(h1, dt, 8, 80);
        h1.style.display = '';
        h1.style.whiteSpace = '';

        if (lead) { lead.style.width = dt + 'px'; lead.style.maxWidth = 'none'; }
        [].forEach.call(subDesk, function (line) {
          line.style.display = 'inline';
          line.style.whiteSpace = 'nowrap';
          fitTo(line, dt, 8, 40);
          line.style.display = 'block';
          line.style.whiteSpace = '';
        });
        return;
      }

      /* ── МОБИЛЬНЫЙ ──
         Общая мера — ширина контейнера. Обе строки заголовка подгоняются
         под неё ПО ОТДЕЛЬНОСТИ: короткой строке, чтобы добрать до той же
         ширины, нужен больший кегль — контраст возникает сам, а строки
         заканчиваются на одной вертикали.

         Меру НЕЛЬЗЯ брать от второй строки, как это сделано в index.html:
         там «PSİXOLOGİYA MƏKTƏBİ» при 20px само по себе почти во всю
         ширину, а здесь вторая строка бывает одним коротким словом
         («Terapiyası» → 128px). Мера схлопывалась, и подзаголовок ужимался
         до 8px. Проверено на samira.html. */
      var inner = hero.querySelector('.page-hero-x-inner');
      var target = inner
        ? inner.getBoundingClientRect().width - 40
        : window.innerWidth - 60;
      if (!target) return;

      [w1, w2].forEach(function (line) {
        if (!line) return;
        line.style.display = 'inline';
        line.style.whiteSpace = 'nowrap';
        fitTo(line, target, 10, 160);
        line.style.display = 'block';
        line.style.textAlign = 'center';
      });

      /* Подзаголовок — ОДИН кегль на все строки, а не по строке на каждую.
         Подгонка каждой строки по отдельности (прежнее поведение) давала
         «Fərdi, ailə və» огромным, а следующую строку вдвое мельче: именно
         на это Кенан и указал — «пробелы между строками не одинаковые,
         выглядит некорректно». Берём самую длинную строку, подгоняем её,
         полученный кегль ставим всем — тогда межстрочные интервалы ровные. */
      if (subMob.length) {
        var smallest = 99;
        [].forEach.call(subMob, function (line) {
          line.style.display = 'inline';
          line.style.whiteSpace = 'nowrap';
          fitTo(line, target, 8, 30);
          var got = parseFloat(line.style.fontSize);
          if (got < smallest) smallest = got;
        });
        [].forEach.call(subMob, function (line) {
          line.style.fontSize = smallest + 'px';
          line.style.display = 'block';
          line.style.whiteSpace = '';
        });
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', fitOne);
  } else {
    fitOne();
  }
  window.addEventListener('resize', fitOne, { passive: true });
  /* Шрифт грузится позже разметки — без пересчёта ширины будут от Arial. */
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(fitOne);
  }
})();
