/* book-audit-probe.js — замерщик страниц КНИГ (books/** и klinik-psixiatriya/**).
 *
 * Драйвер: _tools/book-audit.js (headless Chrome, --dump-dom, результат в <title>
 * как BOOK-AUDIT-JSON:{...}). Ничего не меняет в DOM — только читает.
 *
 * Что мерит (классы нарушений из задания владельца):
 *   (а) структура меню — группы/подменю, ссылка или подпись заголовок группы,
 *       «выпавшие» пункты (подпункт вне группы), раскрытые группы, активная группа;
 *   (б) типографика — кегли ролей (h1/h2/h3/h4/текст), отношение заголовка
 *       раздела к тексту, серые заголовки;
 *   (в) контраст — цвет текста против фактического фона (норма 4.5:1, 3:1 для
 *       крупного ≥24 px или жирного ≥18.66 px);
 *   (г) отступы и «пустые полосы» — зазор «название → первый блок» и пустые
 *       блоки высотой ≥ 24 px без текста;
 *   (д) ссылки — пустой href, '#', javascript:, href на несуществующий файл
 *       (по статике), дубли aria/id;
 *   (е) пустые страницы — объём текста в теле главы.
 */
(function () {
  'use strict';
  if (window.__BOOK_AUDIT__) return;
  window.__BOOK_AUDIT__ = 1;

  function cs(el) { return el ? getComputedStyle(el) : null; }
  function clean(s) { return String(s == null ? '' : s).replace(/\s+/g, ' ').trim(); }
  function txt(el, n) { var t = clean(el.textContent); n = n || 48; return t.length > n ? t.slice(0, n) + '…' : t; }
  function sel(el) {
    var parts = [], e = el, i = 0;
    while (e && e.nodeType === 1 && i < 4) {
      if (e.id) { parts.unshift('#' + e.id); break; }
      var s = e.tagName.toLowerCase();
      var cl = (typeof e.className === 'string' ? e.className : '').trim().split(/\s+/).filter(Boolean).slice(0, 2);
      if (cl.length) s += '.' + cl.join('.');
      parts.unshift(s);
      e = e.parentElement; i++;
    }
    return parts.join('>');
  }
  function ownText(el) {
    var t = '';
    for (var i = 0; i < el.childNodes.length; i++) {
      var n = el.childNodes[i];
      if (n.nodeType === 3) t += n.nodeValue;
    }
    return clean(t);
  }
  function vis(el, style) {
    var c = style || cs(el);
    if (!c || c.display === 'none' || c.visibility === 'hidden') return false;
    if (parseFloat(c.opacity) < 0.05) return false;
    var r = el.getBoundingClientRect();
    return r.width > 1 && r.height > 1;
  }
  function parseColor(v) {
    var m = /^rgba?\(([^)]+)\)$/.exec(String(v || ''));
    if (!m) return null;
    var p = m[1].split(',').map(function (x) { return parseFloat(x); });
    return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 };
  }
  function over(fg, bg) {   // alpha-композит fg поверх bg
    var a = fg.a;
    return { r: fg.r * a + bg.r * (1 - a), g: fg.g * a + bg.g * (1 - a), b: fg.b * a + bg.b * (1 - a), a: 1 };
  }
  function lum(c) {
    function f(v) { v = v / 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }
    return 0.2126 * f(c.r) + 0.7152 * f(c.g) + 0.0722 * f(c.b);
  }
  function ratio(a, b) {
    var la = lum(a), lb = lum(b), hi = Math.max(la, lb), lo = Math.min(la, lb);
    return Math.round(((hi + 0.05) / (lo + 0.05)) * 100) / 100;
  }
  function hex(c) { function h(v) { var s = Math.round(v).toString(16); return s.length < 2 ? '0' + s : s; } return '#' + h(c.r) + h(c.g) + h(c.b); }
  /* фактический фон: идём вверх и композитим слои; градиент/картинка — стоп
     (фон считаем неизвестным и берём базовый цвет страницы) */
  function bgOf(el) {
    var layers = [], e = el;
    while (e && e.nodeType === 1) {
      var c = cs(e);
      if (!c) break;
      if (c.backgroundImage && c.backgroundImage !== 'none' && /gradient|url/.test(c.backgroundImage)) break;
      var col = parseColor(c.backgroundColor);
      if (col && col.a > 0) {
        layers.push(col);
        if (col.a >= 0.999) break;
      }
      e = e.parentElement;
    }
    var base = parseColor(cs(document.body) ? cs(document.body).backgroundColor : null) || { r: 7, g: 9, b: 14, a: 1 };
    if (base.a < 1) base = { r: 7, g: 9, b: 14, a: 1 };
    for (var i = layers.length - 1; i >= 0; i--) base = over(layers[i], base);
    return base;
  }

  var R = { url: location.pathname, title: document.title, findings: [] };
  function add(cls, page, reason, was, became, extra) {
    R.findings.push({ cls: cls, page: page, reason: reason, was: was, became: became, extra: extra || null });
  }

  /* ── (а) структура меню ─────────────────────────────────────────────── */
  var nav = document.querySelector('.bk-sb__nav') || document.querySelector('nav[aria-label]') || document.querySelector('.bk-sb');
  R.menu = { trees: [], rows: 0, deadRows: 0 };
  if (nav) {
    var rows = nav.querySelectorAll('.bk-row');
    R.menu.rows = rows.length;
    for (var i = 0; i < rows.length; i++) {
      var r = rows[i];
      if (!r.getAttribute('href') && !r.closest('.bk-grp__sub') && !r.closest('.bk-grp')
          && r.className.indexOf('bk-row--sec') >= 0) {
        R.menu.deadRows++;
      }
    }
    var trees = nav.querySelectorAll('.cls-tree');
    for (var t = 0; t < trees.length; t++) {
      var tr = trees[t], key = tr.getAttribute('data-cls');
      var grps = tr.querySelectorAll('.bk-grp');
      var links = 0, spans = 0, cur = 0, open = 0, flat = 0, nosub = 0;
      for (var g = 0; g < grps.length; g++) {
        var head = grps[g].querySelector('.bk-row--sec');
        var hasSubs = grps[g].querySelectorAll('.bk-row--sub').length > 0;
        if (!head) { nosub++; continue; }
        if (head.tagName === 'A' && head.getAttribute('href')) links++;
        else if (hasSubs) spans++;          /* подпись вместо ссылки — только у группы с подпунктами */
        if (grps[g].classList.contains('is-open')) open++;
        if (grps[g].getAttribute('data-here') === '1') cur++;
        if (!grps[g].querySelector('.bk-grp__sub')) nosub++;
      }
      /* пункты, выпавшие из групп: .bk-row--sub прямо в дереве */
      for (var k = 0; k < tr.children.length; k++) {
        var ch = tr.children[k];
        if (ch.className.indexOf('bk-row--sub') >= 0) flat++;
      }
      var tab = document.querySelector('.cls-tab[data-cls="' + key + '"]');
      R.menu.trees.push({ tree: key, groups: grps.length, headers_link: links, headers_span: spans,
        current: cur, open: open, flat_rows: flat, broken_groups: nosub, active_tab: !!(tab && tab.classList.contains('is-active')) });
      if (spans) add('структура меню', '.bk-sb', 'заголовок группы — подпись, не ссылка', spans + ' группы(без href)', 'ссылка на страницу главы', { tree: key });
      if (cur > 1) add('структура меню', '.bk-sb', 'в дереве больше одной «текущей» группы', cur + ' группы с is-on', 'одна', { tree: key });
      if (flat) add('структура меню', '.bk-sb', 'подпункты выпали из групп (плоский список)', flat + ' шт. верхнего уровня', 'внутри .bk-grp__sub', { tree: key });
      if (nosub) add('структура меню', '.bk-sb', 'группа без подменю/заголовка', nosub + ' шт.', 'группа с .bk-grp__sub', { tree: key });
    }
    if (R.menu.deadRows) add('структура меню', '.bk-sb', 'заголовок раздела не кликабелен', R.menu.deadRows + ' строк без href', 'ссылка на страницу раздела', null);
  }

  /* ── (б) типографика ────────────────────────────────────────────────── */
  var read = document.querySelector('.bk-read') || document.querySelector('.bk-main');
  R.typo = [];
  if (read) {
    var base = parseFloat(cs(read).fontSize) || 18;
    var roles = [['body', 'p', read], ['h1', 'h1', document], ['h2', 'h2', read], ['h3', 'h3', read], ['h4', 'h4', read]];
    for (var ri = 0; ri < roles.length; ri++) {
      var nm = roles[ri][0], q = roles[ri][1], scope = roles[ri][2];
      var el2 = scope.querySelector(q);
      if (!el2) continue;
      var c2 = cs(el2), fsz = parseFloat(c2.fontSize);
      R.typo.push({ role: nm, size: Math.round(fsz * 10) / 10, color: hex(parseColor(c2.color) || { r: 0, g: 0, b: 0 }),
        ratio_body: Math.round((fsz / base) * 100) / 100, sample: txt(el2, 40), sel: sel(el2) });
    }
    var h2 = null, h3 = null;
    for (var q2 = 0; q2 < R.typo.length; q2++) { if (R.typo[q2].role === 'h2') h2 = R.typo[q2]; if (R.typo[q2].role === 'h3') h3 = R.typo[q2]; }
    if (h2 && h2.ratio_body < 1.6) {
      add('типографика', sel(read) + ' h2', 'заголовок раздела меньше 1.6 кегля текста', h2.size + ' px (' + h2.ratio_body + '×)', '≥ ' + Math.round(base * 1.6) + ' px');
    }
    if (h2 && h3 && h3.size > h2.size) {
      add('типографика', sel(read) + ' h3', 'подраздел крупнее раздела (лестница сломана)', h3.size + ' > ' + h2.size, 'h3 ≤ h2');
    }
    if (h3 && h3.ratio_body < 1.05) {
      add('типографика', sel(read) + ' h3', 'подраздел не крупнее текста', h3.size + ' px (' + h3.ratio_body + '×)', '> ' + base + ' px');
    }
    /* серые заголовки */
    var fg = parseColor(cs(document.body).color) || { r: 242, g: 237, b: 227 };
    var heads = read.querySelectorAll('h1,h2,h3,h4');
    var grey = 0, greySample = '';
    for (var hi = 0; hi < heads.length; hi++) {
      var hc = parseColor(cs(heads[hi]).color);
      if (!hc) continue;
      var rr = ratio(hc.a < 1 ? over(hc, bgOf(heads[hi])) : hc, bgOf(heads[hi]));
      var sameAsFg = Math.abs(hc.r - fg.r) < 6 && Math.abs(hc.g - fg.g) < 6 && Math.abs(hc.b - fg.b) < 6;
      if (!sameAsFg && rr < 9) { grey++; if (!greySample) greySample = txt(heads[hi], 28) + ' [' + hex(hc) + ' ' + rr + ':1]'; }
    }
    if (grey) add('типографика', sel(read), 'заголовок не цветом основного текста', grey + ' заголовков тише нормы', 'цвет --fg', greySample);
  }

  /* ── (в) контраст ───────────────────────────────────────────────────── */
  R.contrast = [];
  var all = document.querySelectorAll('body *');
  var seen = 0;
  for (var ai = 0; ai < all.length; ai++) {
    var el3 = all[ai];
    if (el3.closest('.kitab-overlay')) continue;              /* модал скрыт, свой оверлей */
    var own = ownText(el3);
    if (!own || own.length < 2) continue;
    var c3 = cs(el3);
    if (!vis(el3, c3)) continue;
    var fgc = parseColor(c3.color);
    if (!fgc) continue;
    var bgc = bgOf(el3);
    var eff = fgc.a < 1 ? over(fgc, bgc) : fgc;
    var r3 = ratio(eff, bgc);
    var fsz3 = parseFloat(c3.fontSize);
    var isLarge = fsz3 >= 24 || (fsz3 >= 18.66 && parseInt(c3.fontWeight, 10) >= 600);
    var norm = isLarge ? 3.0 : 4.5;
    seen++;
    if (r3 < norm) {
      R.contrast.push({ sel: sel(el3), text: txt(el3, 40), color: hex(fgc), bg: hex(bgc), size: Math.round(fsz3 * 10) / 10, ratio: r3, norm: norm });
      if (R.contrast.length > 40) break;
    }
  }
  if (R.contrast.length) {
    add('контраст', '(разные)', 'контраст текста ниже нормы', R.contrast.length + ' узлов (первый: ' + R.contrast[0].sel + ' ' + R.contrast[0].ratio + ':1)', '≥ ' + R.contrast[0].norm + ':1', R.contrast.slice(0, 12));
  }

  /* ── (г) отступы и пустые полосы ────────────────────────────────────── */
  var head2 = document.querySelector('.bk-chead');
  var tp = document.querySelector('.bk-tp');
  var first = null;
  var rest = document.querySelector('.bk-read--rest') || read;
  if (rest) {
    var kids = rest.children;
    for (var ki = 0; ki < kids.length; ki++) { if (vis(kids[ki])) { first = kids[ki]; break; } }
  }
  var anchor = head2 || tp;
  if (anchor && first) {
    var gap = Math.round(first.getBoundingClientRect().top - anchor.getBoundingClientRect().bottom);
    R.gap_title_to_content = gap;
    var restMT = rest ? parseFloat(cs(rest).marginTop) : 0;
    if (gap > 64 || restMT > 48) {
      add('отступы', sel(first), '«пустая полоса» после названия', 'зазор ' + gap + ' px (margin-top ' + restMT + ' px)', 'шаг шкалы ≤ 32 px');
    }
  }
  /* пустые блоки внутри чтения */
  var blanks = [];
  if (read) {
    var cand = read.querySelectorAll('div,section,article,p,span');
    for (var bi = 0; bi < cand.length; bi++) {
      var el4 = cand[bi], c4 = cs(el4);
      if (c4.display === 'none' || c4.visibility === 'hidden') continue;
      if (clean(el4.textContent).length || el4.querySelector('img,svg,canvas,iframe,table')) continue;
      var r4 = el4.getBoundingClientRect();
      if (r4.height >= 24 && r4.width > 40) blanks.push({ sel: sel(el4), h: Math.round(r4.height) });
    }
  }
  R.blank_blocks = blanks.slice(0, 10);
  if (blanks.length) add('отступы', sel(read), 'пустые блоки в тексте', blanks.length + ' шт. (высший ' + Math.max.apply(null, blanks.map(function (b) { return b.h; })) + ' px)', '0', blanks.slice(0, 5));

  /* ── (д)/(е) страница целиком ───────────────────────────────────────── */
  var whole = document.querySelector('.bk-read') || document.querySelector('.bk-tp') || document.querySelector('.bk-toc');
  if (whole) {
    var body_text = '';
    var zones = document.querySelectorAll('.bk-read, .bk-tp, .bk-toc');
    for (var zi = 0; zi < zones.length; zi++) body_text += ' ' + clean(zones[zi].textContent);
    body_text = clean(body_text);
    R.text_len = body_text.length;
    if (body_text.length < 400) add('пустые страницы', sel(whole), 'текста меньше 400 знаков', body_text.length + ' знаков', 'страница с содержимым');
  }
  R.h1 = document.querySelectorAll('.bk-read h1, .bk-chead__h1, h1').length;
  R.title = document.title;

  /* страница помечена как «книга», но это заглушка-редирект */
  if (document.querySelector('meta[http-equiv="refresh"]')) add('пустые страницы', '(редирект)', 'страница-заглушка вместо содержимого', 'meta refresh', 'контент или удаление');

  document.title = 'BOOK-AUDIT-JSON:' + JSON.stringify(R);
})();
