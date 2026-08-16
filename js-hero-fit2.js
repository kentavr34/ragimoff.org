/* Шапка страницы — единая подгонка кегля («резиновый» заголовок).
   Черновик единого скрипта: пока подключён к samira.html и tehsil.html,
   после утверждения переносится в js-hero-fit.js и получает все страницы
   всех языков (az / ru / en / tr).

   ЗАДАЧА (Кенан 2026-08-16): «размер шрифта автоматически как резина
   подстраивается по размеру по горизонтали… если три строчки, то все три
   строчки должны быть одинаковой длины». И то же самое на десктопе.

   ПРОПОРЦИИ ВЗЯТЫ ЗАМЕРОМ С ГЛАВНОЙ, не назначены произвольно.
   На 375px: контейнер 335, ширина текста заголовка 257 (77%), ширина
   строк лида 242 (72%). Строки лида на главной имеют РАЗНЫЙ кегль
   (15/12/16), но ОДИНАКОВУЮ ширину — ровным блок выглядит именно от
   совпадения краёв. Предыдущая версия делала наоборот (один кегль,
   рваные края) — это было ошибкой.

   Потолок кегля нужен, потому что очень короткое слово («Ailə», 4 знака)
   при растягивании на всю меру уходит в 116px и давит страницу. */
(function () {
  'use strict';

  var SHARE_H1 = 0.77;   /* доля контейнера под заголовок — с главной */
  var SHARE_SUB = 0.72;  /* доля контейнера под лид — с главной */
  var MAX_H1_MOB = 56;   /* на главной строка 1 = 50px; чуть выше как запас */
  var MAX_SUB_MOB = 20;
  var LH_H1 = 1.15;      /* интерлиньяж заголовка на главной */

  /* Ширина именно текста, а не блока: у display:block элемента
     getBoundingClientRect даёт ширину контейнера и мерить по нему нельзя. */
  function textWidth(el) {
    var r = document.createRange();
    r.selectNodeContents(el);
    return r.getBoundingClientRect().width;
  }

  /* Кегль ставится с приоритетом important: в gtc.css у .ph-h1 задано
     `font-size: 32px !important`, и обычный inline-стиль его не перебивает.
     Из-за этого на десктопе заголовок оставался 32px, а подзаголовок,
     который никаким !important не защищён, растягивался до 40px — лид
     выходил КРУПНЕЕ заголовка. Замерено на samira.html: h1 481px против
     лида 886px. */
  function setSize(el, px) {
    el.style.setProperty('font-size', px + 'px', 'important');
  }

  /* Наибольший кегль, при котором текст ещё уже target. */
  function fitTo(el, target, lo, hi, cap) {
    if (!target) return 0;
    for (var i = 0; i < 26; i++) {
      var mid = (lo + hi) / 2;
      setSize(el, mid);
      if (textWidth(el) < target) lo = mid; else hi = mid;
    }
    var size = Math.floor(lo);
    if (cap && size > cap) size = cap;
    setSize(el, size);
    return size;
  }

  /* Лид: перебить текст на строки РАВНОЙ длины и дать им один кегль.

     Зачем не как на главной. Там строки лида зафиксированы в разметке
     вручную и имеют 34/41/32 знака — почти равные, поэтому подгонка
     каждой строки под общую ширину даёт близкие кегли (15/12/16) и
     ровный блок. На остальных страницах строки написаны как попало:
     на samira.html это 13/26/18 знаков, и та же подгонка разводит
     кегли вдвое либо оставляет рваные края. Ручная перебивка текста
     на 53 страницах × 4 языка не масштабируется, поэтому переносы
     считает скрипт: слова раскладываются так, чтобы самая широкая
     строка была минимальной, — тогда при ОДНОМ кегле края совпадают. */
  function balanceLead(lines, target) {
    if (!lines.length) return;

    var host = lines[0];

    /* Исходный текст запоминается один раз. Без этого повторный прогон
       (resize) собрал бы слова из уже перебитых строк вместе со спрятанными
       и задвоил бы текст. */
    if (!host.dataset.leadSrc) {
      var src = [];
      [].forEach.call(lines, function (l) {
        var t = (l.textContent || '').trim();
        if (t) src.push(t);
      });
      host.dataset.leadSrc = src.join(' ');
    }
    var words = host.dataset.leadSrc.split(/\s+/).filter(Boolean);
    if (!words.length) return;

    var nLines = lines.length;
    var REF = 20; /* опорный кегль для измерения; итоговый берётся пропорцией */

    /* Ширина слов и пробела при опорном кегле. */
    var probe = document.createElement('span');
    probe.style.cssText = 'position:absolute;visibility:hidden;white-space:pre;font-size:' + REF + 'px';
    probe.style.fontFamily = getComputedStyle(host).fontFamily;
    probe.style.fontWeight = getComputedStyle(host).fontWeight;
    probe.style.letterSpacing = getComputedStyle(host).letterSpacing;
    document.body.appendChild(probe);
    var wordW = words.map(function (w) { probe.textContent = w; return probe.getBoundingClientRect().width; });
    probe.textContent = ' ';
    var spaceW = probe.getBoundingClientRect().width;
    document.body.removeChild(probe);

    /* Строки хранятся как наборы ИНДЕКСОВ, а не слов: одно и то же слово
       может встретиться дважды, и поиск по значению дал бы чужую ширину. */
    function rowWidth(row) {
      var w = 0;
      for (var i = 0; i < row.length; i++) w += (i ? spaceW : 0) + wordW[row[i]];
      return w;
    }

    /* Жадная раскладка набивает первые строки под завязку и оставляет
       хвост: «Kişi-qadın və valideyn-uşaq / münasibətləri — terapiya /
       və təlim.» — последняя строка втрое короче. Поэтому раскладку
       ищем перебором с минимумом разброса: строки должны быть как можно
       ближе к средней длине. Слов в лиде десятки, строк три-четыре —
       динамика считается мгновенно. */
    var total = wordW.reduce(function (a, b) { return a + b; }, 0) + spaceW * (words.length - 1);
    var avg = total / nLines;

    var memo = {};
    function best(i, k) {
      if (k === 1) {
        var w = rowWidth(rangeIdx(i, words.length));
        return { cost: (w - avg) * (w - avg), cut: [words.length] };
      }
      var key = i + ':' + k;
      if (memo[key]) return memo[key];
      var bestRes = { cost: Infinity, cut: null };
      /* строке нужно хотя бы одно слово, и хвосту тоже */
      for (var j = i + 1; j <= words.length - (k - 1); j++) {
        var wr = rowWidth(rangeIdx(i, j));
        var sub = best(j, k - 1);
        var c = (wr - avg) * (wr - avg) + sub.cost;
        if (c < bestRes.cost) bestRes = { cost: c, cut: [j].concat(sub.cut) };
      }
      memo[key] = bestRes;
      return bestRes;
    }
    function rangeIdx(a, b) { var r = []; for (var t = a; t < b; t++) r.push(t); return r; }

    var rows;
    if (words.length < nLines) {
      rows = words.map(function (_, i) { return [i]; });
    } else {
      var cuts = best(0, nLines).cut;
      rows = [];
      var start = 0;
      cuts.forEach(function (c) { rows.push(rangeIdx(start, c)); start = c; });
    }

    /* Кегль: самая широкая строка должна дать ровно target. */
    var widest = 0;
    rows.forEach(function (r) { var w = rowWidth(r); if (w > widest) widest = w; });
    if (!widest) return;
    var size = Math.floor(REF * target / widest);
    if (size > MAX_SUB_MOB) size = MAX_SUB_MOB;
    if (size < 8) size = 8;

    /* Раскладываем обратно по существующим элементам: лишние прячем. */
    [].forEach.call(lines, function (l, i) {
      if (i < rows.length) {
        l.textContent = rows[i].map(function (idx) { return words[idx]; }).join(' ');
        l.style.display = 'block';
        l.style.whiteSpace = 'nowrap';
        setSize(l, size);
        l.style.lineHeight = Math.round(size * 1.5) + 'px';
      } else {
        l.style.display = 'none';
      }
    });
  }

  function fitOne() {
    document.querySelectorAll('.page-hero-x').forEach(function (hero) {
      var h1 = hero.querySelector('.ph-h1');
      if (!h1) return;

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
           поэтому подгоняется весь <h1>. Мера — ширина поисковика, чтобы
           заголовок, лид и поисковик стояли на одной вертикали. */
        /* Мера — ширина поисковика: на главной заголовок, лид и поисковик
           стоят на одной вертикали, 620px при контейнере 1164 (53%).
           На страницах без поисковика (samira.html) брать 77% контейнера
           нельзя — это 896px, заголовок раздувается. Держим ту же долю. */
        var dt = sw ? Math.round(sw.getBoundingClientRect().width) : Math.round(Math.min(620, box * 0.53));
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
          fitTo(line, dt, 8, 48, 0);
          line.style.display = 'block';
          line.style.whiteSpace = '';
        });
        return;
      }

      /* ── МОБИЛЬНЫЙ ── каждая строка тянется до общей меры отдельно. */
      var tH1 = box * SHARE_H1;
      var tSub = box * SHARE_SUB;

      [w1, w2].forEach(function (line) {
        if (!line) return;
        line.style.display = 'inline';
        line.style.whiteSpace = 'nowrap';
        var size = fitTo(line, tH1, 10, 140, MAX_H1_MOB);
        line.style.display = 'block';
        line.style.textAlign = 'center';
        /* Интерлиньяж считаем от кегля — иначе при крупной строке
           между строками открывается провал (было 133px при 116px). */
        line.style.lineHeight = Math.round(size * LH_H1) + 'px';
      });

      balanceLead(subMob, tSub);
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
