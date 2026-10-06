/* ═══ Титул книги: строка «Автор, İlk nəşr — YYYY» по ширине названия ═══
   Владелец (06.10.2026): строка стоит под названием, по центру названия и
   растянута до его краёв — «растянуть, увеличивая размер шрифта».
   Скрипт меряет видимую ширину названия (текст — по краске строк, картинка-
   lockup — по краске PNG без прозрачных полей) и подбирает кегль мета-строки
   так, чтобы её ширина совпала с шириной названия (±5%). Кегль держим в
   границах MIN..MAX; если упёрлись в предел — остаток добираем межбуквенным
   (не больше LS_MAX, иначе строка «разваливается»). Строка ставится так, чтобы
   её середина совпала с серединой названия, и не выходила за вьюпорт.
   Страницы: .bk-tp__title/.bk-tp__meta и .home-title/.book-meta. */
(function () {
  'use strict';
  var MIN = 12;        /* px — ниже не опускаем: микроскопический текст */
  var MAX = 38;        /* px — выше не поднимаем: строка не должна равняться названию */
  var LS_MAX = 0.06;   /* em — предел добавки межбуквенного */
  var TOL = 0.05;      /* допуск совпадения ширин — 5% */
  var GUTTER = 8;      /* px — зазор до края экрана */

  /* прямоугольник краски названия: left/right/width/center */
  function inkRect(t) {
    var box = t.getBoundingClientRect();
    if (t.tagName === 'IMG') return imgInkRect(t);
    var img = t.querySelector && t.querySelector('img');
    if (img) return imgInkRect(img);
    var l = Infinity, r = -Infinity;
    try {
      var range = document.createRange();
      range.selectNodeContents(t);
      var rects = range.getClientRects();
      for (var i = 0; i < rects.length; i++) {
        if (rects[i].width < 0.5) continue;
        if (rects[i].left < l) l = rects[i].left;
        if (rects[i].right > r) r = rects[i].right;
      }
    } catch (e) {}
    if (r <= l) { l = box.left; r = box.right; }
    return { left: l, right: r, width: r - l, center: (l + r) / 2 };
  }

  /* краска PNG-lockup: прозрачные поля краями названия не считаем */
  function imgInkRect(img) {
    var b = img.getBoundingClientRect();
    var out = { left: b.left, right: b.right, width: b.width, center: b.left + b.width / 2 };
    try {
      if (!img.naturalWidth || !img.complete) return out;
      var c = document.createElement('canvas');
      c.width = img.naturalWidth; c.height = img.naturalHeight;
      var g = c.getContext('2d');
      g.drawImage(img, 0, 0);
      var d = g.getImageData(0, 0, c.width, c.height).data;
      var x0 = c.width, x1 = -1;
      for (var y = 0; y < c.height; y++) {
        for (var x = 0; x < c.width; x++) {
          if (d[(y * c.width + x) * 4 + 3] > 8) { if (x < x0) x0 = x; if (x > x1) x1 = x; }
        }
      }
      if (x1 < x0) return out;
      var k = b.width / c.width;
      out.left = b.left + x0 * k;
      out.right = b.left + (x1 + 1) * k;
      out.width = out.right - out.left;
      out.center = (out.left + out.right) / 2;
    } catch (e) {}
    return out;
  }

  /* доступная ширина: первый предок, влезающий во вьюпорт, минус его поля */
  function availWidth(t) {
    var vw = document.documentElement.clientWidth;
    var el = t.parentElement, w = 0;
    while (el && el !== document.documentElement) {
      var cs = getComputedStyle(el);
      var inner = el.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
      if (inner > 40 && el.clientWidth <= vw + 1) { w = inner; break; }
      el = el.parentElement;
    }
    if (!w) w = vw;
    return Math.min(w, vw - 2 * GUTTER);
  }

  function fit() {
    var m = document.querySelector('.bk-tp__meta') || document.querySelector('.book-meta');
    var t = document.querySelector('.bk-tp__title') || document.querySelector('.home-title');
    if (!m || !t) return;
    var ink = inkRect(t);
    if (!ink.width) return;
    var target = Math.min(ink.width, availWidth(t));

    /* замер строки «как есть» — без влияния раскладки и контейнера */
    var prevW = m.style.width, prevMax = m.style.maxWidth;
    m.style.width = 'max-content';
    m.style.maxWidth = 'none';
    m.style.setProperty('--bk-meta-ls', '0px');
    m.style.setProperty('--bk-meta-fs', MAX + 'px');
    var wMax = m.getBoundingClientRect().width;
    m.style.width = prevW;
    m.style.maxWidth = prevMax;
    if (!wMax) return;

    var fs = MAX * target / wMax;
    if (fs > MAX) fs = MAX;
    if (fs < MIN) fs = MIN;
    m.style.setProperty('--bk-meta-fs', fs.toFixed(2) + 'px');

    /* кегль упёрся в предел и строка короче названия — добираем межбуквенным */
    var ls = 0;
    if (fs >= MAX) {
      var wNow = m.getBoundingClientRect().width;
      var chars = (m.textContent || '').replace(/\s+/g, ' ').trim().length;
      if (chars > 2 && wNow > 0 && wNow < target * (1 - TOL)) {
        ls = Math.min((target - wNow) / (chars - 1), LS_MAX * fs);
      }
    }
    m.style.setProperty('--bk-meta-ls', ls > 0.05 ? ls.toFixed(2) + 'px' : '0px');

    /* середина строки — на середине названия, но не за краем колонки и экрана */
    var mb = m.getBoundingClientRect();
    var host = m.parentElement || m.offsetParent || document.body;
    var hb = host.getBoundingClientRect();
    var left = ink.center - mb.width / 2;
    var lo = hb.left, hi = hb.right - mb.width;
    var vlo = window.scrollX + GUTTER, vhi = window.scrollX + document.documentElement.clientWidth - mb.width - GUTTER;
    if (hi < lo) hi = lo;
    left = Math.max(lo, Math.min(left, hi));
    if (left < vlo) left = vlo;
    if (left > vhi && vhi > vlo) left = vhi;
    m.style.marginLeft = (left - hb.left).toFixed(2) + 'px';
    m.style.marginRight = 'auto';
  }

  var raf = 0;
  function schedule() {
    if (raf) return;
    raf = requestAnimationFrame(function () { raf = 0; fit(); });
  }

  function boot() {
    fit();
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(schedule);
    window.addEventListener('resize', schedule, { passive: true });
    window.addEventListener('orientationchange', schedule, { passive: true });
    window.addEventListener('load', schedule);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
  window.__bkMetaFit = fit;   /* ручной пересчёт (после смены шрифта/размера) */
})();
