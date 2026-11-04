/* RAGIMOFF · Элементы читалки для многостраничных книг (Klinik Psixiatriya: глава = страница, около 150 страниц на язык).
   Те же управления, что в читалке серии Фрейда: A−/A+, день/ночь, листание ←/→ и свайпом. Настройки общие с
   читалкой (localStorage rd-fs, rd-theme), поэтому выбранный размер и тема переходят между книгами. Кенан 31.10.2026. 04.11.2026: свайп и кнопка «наверх» — общий rd-nav.js, A−/A+ растит и меню с титулом. */
(function () {
  var root = document.documentElement, body = document.body;
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };
  var L = { az: ['Şrifti kiçilt', 'Şrifti böyüt', 'Gecə / gündüz'], ru: ['Уменьшить шрифт', 'Увеличить шрифт', 'Ночь / день'],
            en: ['Smaller text', 'Larger text', 'Night / day'], tr: ['Yazıyı küçült', 'Yazıyı büyüt', 'Gece / gündüz'] }[(root.lang || 'az').slice(0, 2)] ||
          ['Şrifti kiçilt', 'Şrifti böyüt', 'Gecə / gündüz'];

  // размер шрифта: та же шкала, что в читалке (0.9–1.5, по умолчанию 1.1) → множитель к утверждённому кеглю
  var fs = parseFloat(store.get('rd-fs') || '1.1');
  function applyFs() { root.style.setProperty('--rd-k', (fs / 1.1).toFixed(3)); }
  // тема: paper / night (по умолчанию — как у сайта, ночь)
  var theme = store.get('rd-theme') || 'night';
  function applyTheme() { root.setAttribute('data-rd', theme); }
  applyFs(); applyTheme();

  var css = '' +
    'body.bk .bk-read{--read-size:calc(18px * var(--rd-k,1))}' +
    '@media(max-width:720px){body.bk .bk-read{--read-size:calc(17.5px * var(--rd-k,1))}}' +
    /* 04.11.2026 (Кенан): A−/A+ растит и заголовки текста, боковое оглавление, титульную страницу и «Mündəricat»;
       при множителе 1 (по умолчанию) все кегли равны утверждённым в book.css */
    'body.bk .bk-read h2{font-size:calc(30px * var(--rd-k,1))}body.bk .bk-read h3{font-size:calc(22px * var(--rd-k,1))}' +
    'body.bk .bk-read h4{font-size:calc(19px * var(--rd-k,1))}body.bk .bk-note__t{font-size:calc(15px * var(--rd-k,1))}' +
    'body.bk .bk-chead__h1{font-size:calc(34px * var(--rd-k,1))}@media(max-width:720px){body.bk .bk-chead__h1{font-size:calc(30px * var(--rd-k,1))}}' +
    'body.bk .bk-sb{--sb-fs:calc(11px * var(--rd-k,1));--sb-num-fs:calc(10px * var(--rd-k,1))}' +
    'body.bk .bk-toc__t{font-size:calc(clamp(1.15rem,1.5vw,1.4rem) * var(--rd-k,1))}@media(max-width:620px){body.bk .bk-toc__t{font-size:calc(1.1rem * var(--rd-k,1))}}' +
    'body.bk .bk-toc__n{font-size:calc(.78rem * var(--rd-k,1))}body.bk .bk-toc__row--group .bk-toc__g{font-size:calc(.72rem * var(--rd-k,1))}' +
    '.rdp{display:inline-flex;gap:4px;align-items:center;margin-right:8px}' +
    '.rdp button{min-width:36px;height:36px;padding:0 8px;border:1px solid var(--line-2);border-radius:8px;background:transparent;' +
    'color:var(--fg);font:600 13px/1 var(--f-ui);cursor:pointer;display:inline-flex;align-items:center;justify-content:center}' +
    '.rdp button:hover{border-color:var(--acc);color:var(--acc-2)}.rdp svg{width:16px;height:16px}' +
    '@media(max-width:720px){.rdp{margin-right:4px;gap:2px}.rdp button{min-width:32px;height:32px;padding:0 6px;font-size:12px}}' +
    'html[data-rd="paper"] .bk,html[data-rd="paper"]{--bg:#F4EFE6;--bg-2:#ECE5D8;--bg-3:#E2D9C8;--fg:#1E1B16;' +
    '--mid:rgba(30,27,22,.80);--mute:rgba(30,27,22,.68);--acc:#8A6A22;--acc-2:#6E5418;--acc-bg:rgba(138,106,34,.08);--on-acc:#fff;' +
    '--line:rgba(30,27,22,.14);--line-2:rgba(30,27,22,.32)}' +
    'html[data-rd="paper"] body.bk{background:var(--bg);color:var(--fg)}' +
    'html[data-rd="paper"] .bk-hdr{background:rgba(244,239,230,.92)}' +
    'html[data-rd="paper"] body.bk::before,html[data-rd="paper"] body.bk::after{opacity:.25}';
  var st = document.createElement('style'); st.id = 'rd-pages-css'; st.textContent = css; document.head.appendChild(st);

  // кнопки — в шапку книги, перед «Sifariş et»
  var host = document.querySelector('.bk-hdr__in');
  if (host) {
    var box = document.createElement('div'); box.className = 'rdp';
    box.innerHTML = '<button type="button" id="rdp-minus" aria-label="' + L[0] + '" title="' + L[0] + '">A−</button>' +
      '<button type="button" id="rdp-plus" aria-label="' + L[1] + '" title="' + L[1] + '">A+</button>' +
      '<button type="button" id="rdp-theme" aria-label="' + L[2] + '" title="' + L[2] + '"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="12" cy="12" r="8"/><path d="M12 4a8 8 0 0 0 0 16z" fill="currentColor"/></svg></button>';
    var before = host.querySelector('.bk-btn');
    host.insertBefore(box, before || null);
    box.querySelector('#rdp-minus').onclick = function () { fs = Math.max(.9, +(fs - .06).toFixed(2)); applyFs(); store.set('rd-fs', fs); };
    box.querySelector('#rdp-plus').onclick = function () { fs = Math.min(1.5, +(fs + .06).toFixed(2)); applyFs(); store.set('rd-fs', fs); };
    box.querySelector('#rdp-theme').onclick = function () { theme = theme === 'paper' ? 'night' : 'paper'; applyTheme(); store.set('rd-theme', theme); };
  }

  // листание: ←/→ и свайп. Соседние страницы — ссылки «предыдущая / следующая» внизу главы, а где их нет
  // (титул, «Mündəricat», обзоры глав — 56 страниц на язык) — по порядку бокового меню (rd-nav.js, 04.11.2026).
  var prev = null, next = null;
  [].forEach.call(document.querySelectorAll('.bk-pn__a'), function (a) {
    var d = (a.querySelector('.bk-pn__dir') || a).textContent;
    if (/Əvvəl|Пред|Назад|Prev|Önceki/i.test(d)) prev = a.href; else next = a.href;
  });
  document.addEventListener('keydown', function (e) {
    if (e.altKey || e.ctrlKey || e.metaKey || (e.target.closest && e.target.closest('input,textarea,select'))) return;
    if (e.key === 'ArrowLeft' && prev) location.href = prev;
    if (e.key === 'ArrowRight' && next) location.href = next;
  });
  function withNav(cb) {
    if (window.rdNav && window.rdNav.swipe) return cb(window.rdNav);
    var s = document.createElement('script'); s.src = '/books/reader/rd-nav.js?v=20261104';
    s.onload = function () { if (window.rdNav) cb(window.rdNav); };
    document.head.appendChild(s);
  }
  withNav(function (RD) {
    var nb = RD.neighbours('.bk-sb__nav a[href]');
    if (!prev) prev = nb.prev;
    if (!next) next = nb.next;
    RD.swipe({
      left: function () { if (next) location.href = next; },
      right: function () { if (prev) location.href = prev; },
      blocked: function () {
        var sb = document.getElementById('bk-sb'), m = document.getElementById('kitab-modal');
        return !!((sb && sb.classList.contains('is-open')) || root.classList.contains('bk-lock') || (m && getComputedStyle(m).display !== 'none'));
      }
    });
    RD.toTop();
  });
})();
