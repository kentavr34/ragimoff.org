/* RAGIMOFF · books/reader/rd-nav.js — общие жесты читалок всех книг сайта (04.11.2026, задача Кенана).
   · Свайп влево/вправо = следующая/предыдущая глава (страница). Не срабатывает при вертикальной прокрутке,
     в таблицах с горизонтальной прокруткой, при выделении текста, при открытом меню/модалке и от самого края
     экрана (там жест браузера «назад/вперёд»).
   · Кнопка «наверх»: скрыта; появляется при прокрутке вверх (не у самого верха страницы), висит ~5 с и
     исчезает; при прокрутке вниз исчезает сразу; нажатие — плавно к началу (без анимации при
     prefers-reduced-motion). Подпись — на языке страницы (<html lang>).
   Подключается из reader.js (серия Фрейда, книги Кенана) и reader-pages.js («Клиническая психиатрия»);
   на страницах старого шаблона (без читалки) — тегом <script src=".../rd-nav.js" data-rd-auto defer>. */
(function () {
  var W = window, D = document, root = D.documentElement;
  var lang = (root.lang || 'az').slice(0, 2).toLowerCase();
  var RD = W.rdNav = W.rdNav || {};
  RD.v = '20261104';
  function reduced() { try { return W.matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) { return false; } }
  function norm(p) { return p.replace(/\/index\.html$/, '/'); }

  /* Свайп. o.left() — следующая, o.right() — предыдущая, o.blocked() — true, когда листать нельзя (открыто меню). */
  RD.swipe = function (o) {
    o = o || {};
    if (RD._swipe) return;
    RD._swipe = true;
    var IGN = o.ignore || 'table,.tbl-wrap,pre,input,textarea,select,[contenteditable],.rd-toc,.bk-sb,.sidebar,.fn-pop,.kitab-overlay,.rd-top';
    var x0 = 0, y0 = 0, t0 = 0, live = false;
    D.addEventListener('touchstart', function (e) {
      live = false;
      if (e.touches.length !== 1) return;
      var t = e.touches[0];
      if (t.clientX < 28 || t.clientX > W.innerWidth - 28) return;          // край экрана — жест браузера
      if (e.target && e.target.closest && e.target.closest(IGN)) return;
      x0 = t.clientX; y0 = t.clientY; t0 = Date.now(); live = true;
    }, { passive: true });
    D.addEventListener('touchmove', function (e) {
      if (!live) return;
      if (e.touches.length !== 1) { live = false; return; }
      var t = e.touches[0], dx = Math.abs(t.clientX - x0), dy = Math.abs(t.clientY - y0);
      if (dy > 14 && dy > dx) live = false;                                 // пошла вертикальная прокрутка — не листаем
    }, { passive: true });
    D.addEventListener('touchend', function (e) {
      if (!live) return;
      live = false;
      if (o.blocked && o.blocked()) return;
      try { var s = W.getSelection(); if (s && String(s).length) return; } catch (err) {}
      var t = e.changedTouches[0], dx = t.clientX - x0, dy = t.clientY - y0, dt = Date.now() - t0;
      if (dt > 900 || Math.abs(dx) < 56 || Math.abs(dx) < Math.abs(dy) * 1.5) return;
      if (dx < 0) { if (o.left) o.left(); } else if (o.right) o.right();
    }, { passive: true });
    D.addEventListener('touchcancel', function () { live = false; }, { passive: true });
  };

  /* Соседние страницы книги по порядку ссылок меню (одна папка = одна книга-язык): {prev, next, list}. */
  RD.neighbours = function (sel) {
    var here = norm(location.pathname), dir = here.slice(0, here.lastIndexOf('/') + 1);
    var seen = {}, list = [];
    [].forEach.call(D.querySelectorAll(sel), function (a) {
      var p;
      try { p = norm(new URL(a.getAttribute('href'), location.href).pathname); } catch (e) { return; }
      if (p.slice(0, dir.length) !== dir || p.slice(dir.length).indexOf('/') >= 0) return;
      if (a.closest && a.closest('[hidden]')) return;
      if (seen[p]) return;
      seen[p] = 1; list.push(p);
    });
    var i = list.indexOf(here);
    return { prev: i > 0 ? list[i - 1] : null, next: i >= 0 && i < list.length - 1 ? list[i + 1] : null, list: list };
  };

  /* Кнопка «наверх». */
  RD.toTop = function (o) {
    o = o || {};
    if (D.querySelector('.rd-top')) return;
    var L = { az: 'Yuxarı', ru: 'Наверх', en: 'Back to top', tr: 'Yukarı' };
    var label = o.label || L[lang] || L.az;
    var css = '.rd-top{position:fixed;right:max(16px,env(safe-area-inset-right));bottom:max(20px,env(safe-area-inset-bottom));z-index:60;' +
      'width:46px;height:46px;margin:0;padding:0;border-radius:50%;display:grid;place-items:center;' +
      'background:var(--bg-2,#121722);color:var(--ink,var(--fg,#E9E3D6));border:1px solid var(--acc,#C9A961);' +
      'box-shadow:0 8px 24px rgba(0,0,0,.35);cursor:pointer;font:inherit;opacity:0;visibility:hidden;transform:translateY(10px);' +
      'transition:opacity .22s,transform .22s,visibility 0s linear .22s;-webkit-tap-highlight-color:transparent}' +
      '.rd-top.is-on{opacity:1;visibility:visible;transform:none;transition-delay:0s}' +
      '.rd-top:hover,.rd-top:focus-visible{background:var(--acc,#C9A961);color:#0B0E14}' +
      '.rd-top svg{width:20px;height:20px;display:block}' +
      '@media(prefers-reduced-motion:reduce){.rd-top{transition:none}}' +
      '@media print{.rd-top{display:none!important}}';
    var st = D.createElement('style'); st.id = 'rd-top-css'; st.textContent = css; D.head.appendChild(st);
    var b = D.createElement('button');
    b.type = 'button'; b.className = 'rd-top'; b.setAttribute('aria-label', label); b.title = label;
    b.setAttribute('aria-hidden', 'true'); b.tabIndex = -1;
    b.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 19V5"/><path d="M5 12l7-7 7 7"/></svg>';
    D.body.appendChild(b);
    var MIN = o.min || 240, DELAY = o.delay || 5000, STEP = o.step || 20;
    var last = W.scrollY, up = 0, down = 0, timer = 0, on = false, going = 0;
    function set(v) {
      if (on === v) return;
      on = v;
      b.classList.toggle('is-on', v);
      b.setAttribute('aria-hidden', v ? 'false' : 'true');
      b.tabIndex = v ? 0 : -1;
      if (!v && D.activeElement === b) b.blur();
      if (!v) clearTimeout(timer);
    }
    function arm() { clearTimeout(timer); timer = setTimeout(function () { set(false); }, DELAY); }
    W.addEventListener('scroll', function () {
      var y = W.scrollY, d = y - last; last = y;
      if (going) { if (y <= 0 || Date.now() > going) going = 0; return; }   // едем наверх по нажатию
      if (y < MIN) { set(false); up = down = 0; return; }
      if (d < 0) { up -= d; down = 0; if (up >= STEP) { set(true); arm(); } }
      else if (d > 0) { down += d; up = 0; if (down > 6) set(false); }
    }, { passive: true });
    b.addEventListener('click', function () {
      set(false); going = Date.now() + 1500;
      try { W.scrollTo({ top: 0, behavior: reduced() ? 'instant' : 'smooth' }); } catch (e) { W.scrollTo(0, 0); }
    });
    RD.top = { hide: function () { set(false); }, el: b };
  };

  /* Автономный режим — страницы старого шаблона без читалки: <script src="…/rd-nav.js" data-rd-auto defer>. */
  var me = D.currentScript;
  if (me && me.hasAttribute('data-rd-auto')) {
    var init = function () {
      var old = D.getElementById('btt'); if (old) old.style.display = 'none';  // прежняя статичная кнопка «↑»
      var nb = RD.neighbours('#sb a[href], .sidebar a[href]');
      RD.swipe({
        left: function () { if (nb.next) location.href = nb.next; },
        right: function () { if (nb.prev) location.href = nb.prev; },
        blocked: function () {
          var sb = D.getElementById('sb'), m = D.getElementById('kitab-modal');
          return !!((sb && sb.classList.contains('on')) || (m && getComputedStyle(m).display !== 'none'));
        }
      });
      RD.toTop();
    };
    if (D.readyState === 'loading') D.addEventListener('DOMContentLoaded', init); else init();
  }
})();
