/* RAGIMOFF · Читалка серии «Ziqmund Freyd · Toplu əsərlər»: одна глава на экране, листание кнопками,
   клавишами ←/→ и свайпом, оглавление, размер шрифта, тема «бумага/ночь», сноски во всплывающем окне,
   место чтения запоминается. Работает без внешних библиотек. */
(function () {
  var root = document.documentElement, body = document.body;
  var book = body.getAttribute('data-book') || 'book';
  var chaps = [].slice.call(document.querySelectorAll('.rd-chap'));
  var titlePage = document.getElementById('rd-title');
  var bar = document.querySelector('.rd-progress');
  var N = chaps.length, cur = 0;
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };

  // тема и размер шрифта
  var theme = store.get('rd-theme') || (matchMedia('(prefers-color-scheme: dark)').matches ? 'night' : 'paper');
  root.setAttribute('data-theme', theme);
  var fs = parseFloat(store.get('rd-fs') || '1.1');
  root.style.setProperty('--fs', fs + 'rem');
  function btn(id, fn) { var b = document.getElementById(id); if (b) b.addEventListener('click', fn); }
  btn('rd-theme', function () { theme = theme === 'paper' ? 'night' : 'paper'; root.setAttribute('data-theme', theme); store.set('rd-theme', theme); });
  btn('rd-fs-minus', function () { fs = Math.max(.9, +(fs - .06).toFixed(2)); root.style.setProperty('--fs', fs + 'rem'); store.set('rd-fs', fs); });
  btn('rd-fs-plus', function () { fs = Math.min(1.5, +(fs + .06).toFixed(2)); root.style.setProperty('--fs', fs + 'rem'); store.set('rd-fs', fs); });

  // оглавление
  function tocOpen(v) { body.classList.toggle('toc-open', v); }
  btn('rd-toc-btn', function () { tocOpen(true); });
  btn('rd-toc-close', function () { tocOpen(false); });
  var scrim = document.querySelector('.rd-scrim'); if (scrim) scrim.addEventListener('click', function () { tocOpen(false); });

  // показ главы (0 — титульная страница)
  var pv = document.getElementById('rd-prev'), nx = document.getElementById('rd-next'), pos = document.getElementById('rd-pos');
  var pager = document.querySelector('.rd-pager'), hint = document.querySelector('.rd-hint');
  function label(i) { return i === 0 ? (body.getAttribute('data-title-label') || '') : (chaps[i - 1].getAttribute('data-title') || ''); }
  function show(i, scroll) {
    cur = Math.max(0, Math.min(N, i));
    titlePage.hidden = cur !== 0;
    chaps.forEach(function (c, k) { c.classList.toggle('is-on', k === cur - 1); });
    body.classList.toggle('is-reading', cur > 0);
    pager.hidden = hint.hidden = cur === 0;
    pv.disabled = cur === 0;
    nx.disabled = cur === N;
    pv.querySelector('span').textContent = label(cur - 1 < 0 ? 0 : cur - 1);
    nx.querySelector('span').textContent = cur < N ? label(cur + 1) : '';
    pos.textContent = cur > 0 ? cur + ' / ' + N : '';
    [].forEach.call(document.querySelectorAll('.toc-row[data-i]'), function (a) { a.setAttribute('aria-current', String(+a.getAttribute('data-i') === cur)); });
    var h = cur > 0 ? '#ch' + cur : '#';
    if (location.hash !== h && (cur > 0 || location.hash)) history.replaceState(null, '', cur > 0 ? h : location.pathname);
    store.set('rd-pos-' + book, cur);
    if (scroll !== false) window.scrollTo({ top: 0, behavior: 'instant' in window ? 'instant' : 'auto' });
    progress();
  }
  pv.addEventListener('click', function () { show(cur - 1); });
  nx.addEventListener('click', function () { show(cur + 1); });
  [].forEach.call(document.querySelectorAll('[data-go]'), function (a) {
    a.addEventListener('click', function (e) { e.preventDefault(); tocOpen(false); show(+a.getAttribute('data-go')); });
  });
  document.addEventListener('keydown', function (e) {
    if (e.target.closest && e.target.closest('input,textarea')) return;
    if (e.key === 'ArrowRight' && cur < N) show(cur + 1);
    else if (e.key === 'ArrowLeft' && cur > 0) show(cur - 1);
    else if (e.key === 'Escape') { tocOpen(false); closePop(); }
  });

  // свайп влево/вправо — следующая/предыдущая глава
  var sx = 0, sy = 0, st = 0;
  document.addEventListener('touchstart', function (e) { if (e.touches.length !== 1) return; sx = e.touches[0].clientX; sy = e.touches[0].clientY; st = Date.now(); }, { passive: true });
  document.addEventListener('touchend', function (e) {
    if (!st || body.classList.contains('toc-open')) return;
    var t = e.changedTouches[0], dx = t.clientX - sx, dy = t.clientY - sy, dt = Date.now() - st; st = 0;
    if (Math.abs(dx) > 70 && Math.abs(dx) > Math.abs(dy) * 1.8 && dt < 700) {
      if (dx < 0 && cur < N) show(cur + 1); else if (dx > 0 && cur > 0) show(cur - 1);
    }
  }, { passive: true });

  // прогресс чтения главы
  function progress() {
    if (!bar) return;
    if (cur === 0) { bar.style.width = '0'; return; }
    var el = chaps[cur - 1], r = el.getBoundingClientRect(), h = el.offsetHeight - innerHeight + 120;
    var p = h > 0 ? Math.min(1, Math.max(0, -r.top / h)) : 1;
    bar.style.width = (((cur - 1) + p) / N * 100).toFixed(2) + '%';
  }
  addEventListener('scroll', progress, { passive: true });

  // сноски: всплывающее окно у ссылки
  var pop = null;
  function closePop() { if (pop) { pop.remove(); pop = null; } }
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('.fn-ref a');
    if (!a) { if (pop && !e.target.closest('.fn-pop')) closePop(); return; }
    e.preventDefault(); closePop();
    var n = document.getElementById(a.getAttribute('href').slice(1)); if (!n) return;
    pop = document.createElement('div'); pop.className = 'fn-pop'; pop.setAttribute('role', 'note');
    pop.innerHTML = n.innerHTML.replace(/<a[^>]*class="fn-back"[^>]*>(.*?)<\/a>/, '<b>$1.</b>');
    document.body.appendChild(pop);
    var r = a.getBoundingClientRect(), w = pop.offsetWidth;
    pop.style.left = Math.max(10, Math.min(scrollX + r.left - w / 2, scrollX + innerWidth - w - 10)) + 'px';
    pop.style.top = (scrollY + r.bottom + 10) + 'px';
  });

  // «Kitabı al»: кладём печатный экземпляр в ту же корзину, что у каталога (ragimoff_cart_v1), и открываем её там
  btn('rd-buy', function () {
    var b = document.getElementById('rd-buy'), title = b.getAttribute('data-order'), price = b.getAttribute('data-price');
    try {
      var items = JSON.parse(localStorage.getItem('ragimoff_cart_v1') || '[]');
      if (!items.some(function (x) { return x.title === title; })) items.push({ title: title, qty: 1, price: price });
      localStorage.setItem('ragimoff_cart_v1', JSON.stringify(items));
    } catch (e) {}
    b.classList.add('is-added');
    setTimeout(function () { location.href = '/books/#sebet'; }, 350);
  });

  // старт: из адреса (#chN) или с последнего места чтения
  var m = /^#ch(\d+)$/.exec(location.hash);
  var start = m ? +m[1] : +(store.get('rd-pos-' + book) || 0);
  if (!(start >= 0 && start <= N)) start = 0;
  show(start, !!m);
  addEventListener('hashchange', function () { var mm = /^#ch(\d+)$/.exec(location.hash); if (mm) show(+mm[1]); });
})();
