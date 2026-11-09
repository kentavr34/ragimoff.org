/* RAGIMOFF · «Ноктюрн» — интерфейс: шапка, меню, язык, свет за курсором, появление блоков.
   Формы, оплата и галереи остаются за shared.js / training-pay.js (копии с боевого сайта). */
(function () {
  'use strict';
  /* Кенан 09.11: при выключенной в ОС анимации — мягкий режим, а не статичный сайт: проявления короче и тише,
     гаснут только бесконечные и параллакс-движения (см. .n-soft в nocturne.css) */
  var soft = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (soft) document.documentElement.classList.add('n-soft');
  var reduce = false;
  var head = document.getElementById('nHead');
  var burger = document.querySelector('.n-burger');
  var mob = document.getElementById('nMob');

  /* приложение RAGIMOFF (PWA, Кенан 09.11.2026): сохранение открытых страниц и книг на устройстве + предложение установить */
  if ('serviceWorker' in navigator && location.protocol === 'https:') {
    window.addEventListener('load', function () { navigator.serviceWorker.register('/sw.js', { scope: '/' }).catch(function () {}); });
  }
  (function () {
    var lang = document.documentElement.lang || 'az';
    var TX = {
      az: { t: 'RAGIMOFF tətbiqi', d: 'Saytı və kitabları telefonda açın — internetsiz də oxuyun.', go: 'Quraşdır', ios: 'Safari-də «Paylaş» → «Ana ekrana əlavə et» seçin.' },
      ru: { t: 'Приложение RAGIMOFF', d: 'Сайт и книги в телефоне — читайте даже без интернета.', go: 'Установить', ios: 'В Safari нажмите «Поделиться» → «На экран „Домой“».' },
      en: { t: 'RAGIMOFF app', d: 'The site and books on your phone — read even offline.', go: 'Install', ios: 'In Safari tap Share → “Add to Home Screen”.' }
    }[lang] || null;
    if (!TX) return;
    var standalone = window.matchMedia('(display-mode: standalone)').matches || navigator.standalone;
    if (standalone) return;
    var KEY = 'rgm_app_dismiss';
    try { if (Date.now() - (+localStorage.getItem(KEY) || 0) < 14 * 864e5) return; } catch (e) {}
    function bar(installFn) {
      if (document.querySelector('.n-app')) return;
      var b = document.createElement('div');
      b.className = 'n-app'; b.setAttribute('role', 'dialog'); b.setAttribute('aria-label', TX.t);
      b.innerHTML = '<span class="n-app-ico" aria-hidden="true">R<i></i></span><span class="n-app-txt"><b>' + TX.t + '</b><small>' +
        (installFn ? TX.d : TX.ios) + '</small></span>' + (installFn ? '<button type="button" class="n-app-go">' + TX.go + '</button>' : '') +
        '<button type="button" class="n-app-x" aria-label="×">×</button>';
      document.body.appendChild(b);
      requestAnimationFrame(function () { b.classList.add('is-in'); });
      function close() { b.classList.remove('is-in'); try { localStorage.setItem(KEY, Date.now()); } catch (e) {} setTimeout(function () { b.remove(); }, 500); }
      b.querySelector('.n-app-x').onclick = close;
      if (installFn) b.querySelector('.n-app-go').onclick = function () { installFn().then(close, close); };
    }
    window.addEventListener('beforeinstallprompt', function (e) {
      e.preventDefault();
      var ev = e;
      setTimeout(function () { bar(function () { ev.prompt(); return ev.userChoice; }); }, 2500);
    });
    var ios = /iphone|ipad|ipod/i.test(navigator.userAgent) && /safari/i.test(navigator.userAgent) && !/crios|fxios/i.test(navigator.userAgent);
    if (ios) setTimeout(function () { bar(null); }, 3500);
    /* Android без встроенной установки (Samsung Internet и др.) — кнопка скачивает APK приложения */
    var prompted = false;
    window.addEventListener('beforeinstallprompt', function () { prompted = true; });
    if (/android/i.test(navigator.userAgent)) setTimeout(function () {
      if (prompted) return;
      bar(function () { location.href = '/app/ragimoff.apk'; return Promise.resolve(); });
    }, 4500);
  })();

  /* header: solid after scroll, hides on scroll down, returns on scroll up */
  var lastY = 0;
  function onScroll() {
    var y = window.scrollY || 0;
    if (head) {
      head.classList.toggle('is-scrolled', y > 30);
      var menuOpen = mob && mob.classList.contains('is-open');
      head.classList.toggle('is-hidden', !menuOpen && y > 400 && y > lastY + 4);
      if (y < lastY - 4) head.classList.remove('is-hidden');
    }
    lastY = y;
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* mobile menu */
  function setMenu(open) {
    if (!mob || !burger) return;
    mob.classList.toggle('is-open', open);
    mob.setAttribute('aria-hidden', open ? 'false' : 'true');
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    document.documentElement.style.overflow = open ? 'hidden' : '';
  }
  if (burger) burger.addEventListener('click', function () { setMenu(!mob.classList.contains('is-open')); });
  if (mob) mob.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      setMenu(false);
      Array.prototype.forEach.call(document.querySelectorAll('.n-dd.is-open'), function (d) { d.classList.remove('is-open'); });
    }
  });

  /* dropdowns: touch / keyboard — first tap opens, second follows the link */
  Array.prototype.forEach.call(document.querySelectorAll('.n-dd > .n-link'), function (a) {
    a.addEventListener('click', function (e) {
      var dd = a.parentNode;
      if (window.matchMedia('(hover: none)').matches && !dd.classList.contains('is-open')) {
        e.preventDefault();
        Array.prototype.forEach.call(document.querySelectorAll('.n-dd.is-open'), function (d) { d.classList.remove('is-open'); });
        dd.classList.add('is-open');
      }
    });
  });
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.n-dd')) Array.prototype.forEach.call(document.querySelectorAll('.n-dd.is-open'), function (d) { d.classList.remove('is-open'); });
  });

  /* language choice is remembered (the router on /test/nocturne/ uses it) */
  document.addEventListener('click', function (e) {
    var l = e.target.closest && e.target.closest('.n-lang');
    if (l) { try { localStorage.setItem('ragimoff_lang', l.getAttribute('data-lang')); } catch (er) {} }
  });

  /* photo viewer: every gallery shot opens whole, with arrows and Esc */
  var shots = Array.prototype.slice.call(document.querySelectorAll('.n-shot'));
  if (shots.length) {
    var lb = document.createElement('div');
    lb.className = 'n-lb'; lb.setAttribute('role', 'dialog'); lb.setAttribute('aria-modal', 'true');
    lb.innerHTML = '<img alt=""><span class="n-lb-cap"></span><button class="n-lb-x" type="button" aria-label="Close">×</button><button class="n-lb-p" type="button" aria-label="Previous">‹</button><button class="n-lb-n" type="button" aria-label="Next">›</button>';
    document.body.appendChild(lb);
    var lbImg = lb.querySelector('img'), lbCap = lb.querySelector('.n-lb-cap'), cur = 0, group = [];
    function show(i) {
      cur = (i + group.length) % group.length;
      var b = group[cur]; lbImg.src = b.getAttribute('data-full'); lbImg.alt = b.getAttribute('aria-label') || '';
      lbCap.textContent = (b.querySelector('.n-shot-cap') || {}).textContent || '';
    }
    function close() { lb.classList.remove('is-open'); document.documentElement.style.overflow = ''; }
    shots.forEach(function (b) {
      b.addEventListener('click', function () {
        group = Array.prototype.slice.call(b.closest('.n-gallery').querySelectorAll('.n-shot'));
        show(group.indexOf(b)); lb.classList.add('is-open'); document.documentElement.style.overflow = 'hidden';
        lb.querySelector('.n-lb-x').focus();
      });
    });
    lb.querySelector('.n-lb-x').addEventListener('click', close);
    lb.querySelector('.n-lb-p').addEventListener('click', function () { show(cur - 1); });
    lb.querySelector('.n-lb-n').addEventListener('click', function () { show(cur + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
    document.addEventListener('keydown', function (e) {
      if (!lb.classList.contains('is-open')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowLeft') show(cur - 1);
      if (e.key === 'ArrowRight') show(cur + 1);
    });
  }

  /* law cards open / close */
  Array.prototype.forEach.call(document.querySelectorAll('.law-card-head'), function (h) {
    function t() { var c = h.closest('.law-card'); var o = c.classList.toggle('is-open'); h.setAttribute('aria-expanded', o ? 'true' : 'false'); }
    h.addEventListener('click', t);
    h.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); t(); } });
  });

  /* programme strip: drag with the mouse */
  Array.prototype.forEach.call(document.querySelectorAll('.n-strip'), function (st) {
    var down = false, sx = 0, sl = 0, moved = false;
    st.addEventListener('pointerdown', function (e) { if (e.pointerType !== 'mouse') return; down = true; moved = false; sx = e.clientX; sl = st.scrollLeft; });
    window.addEventListener('pointermove', function (e) { if (!down) return; var dx = e.clientX - sx; if (Math.abs(dx) > 4) { moved = true; st.classList.add('is-drag'); } st.scrollLeft = sl - dx; });
    window.addEventListener('pointerup', function () { if (!down) return; down = false; setTimeout(function () { st.classList.remove('is-drag'); }, 0); });
    st.addEventListener('click', function (e) { if (moved) { e.preventDefault(); e.stopPropagation(); moved = false; } }, true);
  });

  /* home first screen — frames of a video driven by the scroll wheel / swipe (forward and back).
     The shown position eases toward the scroll position and neighbouring frames are cross-faded, so it moves like video.
     At the tap a search line appears, the name is typed into it, then the title is written out. */
  var cine = document.querySelector('[data-cine]');
  if (cine) (function () {
    var frame = cine.querySelector('.n-cine-frame'), stick = cine.querySelector('.n-cine-stick'), cv = cine.querySelector('.n-cine-cv');
    var img = cine.querySelector('.n-cine-img'), sq = cine.querySelector('.n-cine-search'), q = cine.querySelector('.n-cine-q');
    if (!frame || !cv || !cv.getContext) return;
    var N = +frame.getAttribute('data-frames') || 0;
    if (!N) return;
    var mob = window.matchMedia('(max-width: 700px)');
    var ctx = cv.getContext('2d'), imgs = [], set = '', target = 0, shown = 0, raf = 0, title = false;
    var QTXT = q ? q.getAttribute('data-q') || '' : '';
    /* moments in frame numbers of the (trimmed) strip: tap → search line, typing, title; from data-marks set by the build */
    var M = (frame.getAttribute('data-marks') || '19,23,23,35,37').split(',').map(Number);
    var T = { video: .78, sqIn: [M[0], M[1]], type: [M[2], M[3]], title: M[4], out: [.9, 1] };
    function clamp(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }
    function seg(v, a, b) { return clamp((v - a) / (b - a)); }
    function load() {
      var want = mob.matches ? 'm' : 'd';
      if (want === set) return;
      set = want; imgs = [];
      var src = frame.getAttribute(want === 'm' ? 'data-msrc' : 'data-fsrc');
      /* the first frames and every 8th first, the rest after — scrubbing works at once and fills in */
      var order = [];
      for (var i = 0; i < N; i += 8) order.push(i);
      for (i = 0; i < N; i++) if (i % 8) order.push(i);
      order.forEach(function (i, n) {
        var im = new Image();
        im.decoding = 'async';
        im.onload = function () { if (Math.abs(i - shown) < 2) paint(true); };
        setTimeout(function () { im.src = src.replace('{i}', ('00' + i).slice(-3)); }, n < 24 ? 0 : 30 + n * 6);
        imgs[i] = im;
      });
      size();
    }
    function ok(im) { return im && im.complete && im.naturalWidth; }
    function near(i) { for (var d = 0; d < N; d++) { if (ok(imgs[i - d])) return imgs[i - d]; if (ok(imgs[i + d])) return imgs[i + d]; } return null; }
    function size() {
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      var w = frame.offsetWidth, h = frame.offsetHeight;
      cv.width = Math.round(w * dpr); cv.height = Math.round(h * dpr);
      paint(true);
    }
    var lastPainted = -1;
    function paint(force) {
      var i = Math.floor(shown), f = shown - i;
      var key = Math.round(shown * 20);
      if (!force && key === lastPainted) return;
      lastPainted = key;
      var a = ok(imgs[i]) ? imgs[i] : near(i), b = ok(imgs[i + 1]) ? imgs[i + 1] : null;
      if (!a) return;
      ctx.globalAlpha = 1; ctx.drawImage(a, 0, 0, cv.width, cv.height);
      if (b && f > .04) { ctx.globalAlpha = f; ctx.drawImage(b, 0, 0, cv.width, cv.height); ctx.globalAlpha = 1; }
      if (img && img.style.opacity !== '0') img.style.opacity = '0';
    }
    function scrollP() {
      var r = cine.getBoundingClientRect(), total = cine.offsetHeight - innerHeight;
      return clamp(-r.top / (total || 1));
    }
    function overlay(p) {
      var k = shown;
      if (sq) sq.style.setProperty('--sq', (seg(k, T.sqIn[0], T.sqIn[1]) * (title ? 0 : 1)).toFixed(3));
      if (q) { var n = Math.round(seg(k, T.type[0], T.type[1]) * QTXT.length); if (q.textContent.length !== n) q.textContent = QTXT.slice(0, n); }
      var on = k >= T.title;
      if (on !== title) { title = on; cine.classList.toggle('is-title', on); if (sq) sq.style.setProperty('--sq', on ? '0' : '1'); }
      stick.style.setProperty('--sh', (.15 + .7 * seg(k, T.sqIn[0], T.title + 4)).toFixed(3));
      stick.style.setProperty('--t2', seg(p, .02, .08).toFixed(3));
      stick.style.setProperty('--out', seg(p, T.out[0], T.out[1]).toFixed(3));
    }
    function loop() {
      raf = 0;
      var d = target - shown;
      shown = Math.abs(d) < .02 ? target : shown + d * (reduce ? 1 : .14);
      paint(false); overlay(scrollP());
      if (shown !== target) raf = requestAnimationFrame(loop);
    }
    function onScroll() {
      target = seg(scrollP(), 0, T.video) * (N - 1);
      if (!raf) raf = requestAnimationFrame(loop);
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', function () { load(); size(); onScroll(); });
    load(); onScroll();
  })();

  /* individual training calculator: specialist × format × hours → price at once (rates: Kenan 08.11.2026) */
  function calcInit(box) {
    var rates = JSON.parse(box.getAttribute('data-rates')), min = +box.getAttribute('data-min') || 20;
    var lang = document.documentElement.lang || 'az';
    var H = { az: 'saat', ru: 'ч', en: 'h' }[lang] || 'h';
    function pick(n) { var el = box.querySelector('input[name$="' + n + '"]:checked'); return el ? el.value : ''; }
    function upd() {
      var hrsEl = box.querySelector('input[type="number"]');
      var hrs = Math.max(min, Math.round(+hrsEl.value || min));
      var who = pick('mutexessis') === 'both' ? 'both' : 'one', fmt = pick('format') || 'online';
      var rate = rates[who][fmt], total = rate * hrs;
      box.querySelector('[data-rate]').textContent = rate + ' AZN × ' + hrs + ' ' + H;
      box.querySelector('[data-total]').textContent = total.toLocaleString('ru-RU').replace(/ /g, ' ') + ' AZN';
      box.setAttribute('data-sum', total); box.setAttribute('data-hours', hrs); box.setAttribute('data-rate-v', rate);
    }
    box.addEventListener('input', upd); box.addEventListener('change', function (e) {
      if (e.target.type === 'number' && (+e.target.value || 0) < min) e.target.value = min; upd(); });
    upd();
  }
  Array.prototype.forEach.call(document.querySelectorAll('[data-calc]'), calcInit);

  /* оплата ePoint: сумму считает сервер; браузер только ведёт. Язык — для страницы после оплаты. */
  var PAY_T = { az: { now: 'İndi ödə', inst: 'Hissə-hissə (bank)', one: 'Ödə' }, ru: { now: 'Оплатить сейчас', inst: 'В рассрочку (банк)', one: 'Оплатить' },
                en: { now: 'Pay now', inst: 'Instalments (bank)', one: 'Pay' } };
  function payGo(form, data, mode, btn) {
    try { localStorage.setItem('rgm_pay_lang', form.getAttribute('data-lang') || 'az'); } catch (e) {}
    if (btn) btn.disabled = true;
    data.mode = mode;
    return fetch('https://api.ragimoff.org/api/billing/epoint/training', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) })
      .then(function (r) { return r.json(); }).then(function (d) {
        if (d && d.ok && d.redirect_url) { location.href = d.redirect_url; return; }
        throw new Error('pay');
      }).catch(function () {
        if (btn) btn.disabled = false;
        var m = form.querySelector('.n-form-msg'); m.hidden = false; m.className = 'n-form-msg is-err';
        m.innerHTML = form.getAttribute('data-err') + ' <a href="https://wa.me/994702200376" target="_blank" rel="noopener">WhatsApp</a>';
      });
  }
  function payChoice(form, data, prices, single) {
    var L = PAY_T[form.getAttribute('data-lang')] || PAY_T.az, box = form.querySelector('.n-pay-choice');
    var sub = form.querySelector('button[type="submit"]');
    if (!box) { box = document.createElement('div'); box.className = 'n-pay-choice'; sub.insertAdjacentElement('afterend', box); }
    sub.hidden = true;
    box.innerHTML = single || prices.prepay === prices.full
      ? '<button type="button" class="n-btn" data-m="prepay">' + L.one + ' — ' + prices.prepay + ' AZN</button>'
      : '<button type="button" class="n-btn" data-m="prepay">' + L.now + ' — ' + prices.prepay + ' AZN</button>' +
        '<button type="button" class="n-btn n-btn-ghost" data-m="installment">' + L.inst + ' — ' + prices.full + ' AZN</button>';
    Array.prototype.forEach.call(box.querySelectorAll('button'), function (b) { b.onclick = function () { payGo(form, data, b.getAttribute('data-m'), b); }; });
  }

  /* запись на консультацию в одно касание (Кенан 09.11.2026) */
  var cf = document.getElementById('consultForm');
  if (cf) (function () {
    var show = JSON.parse(cf.getAttribute('data-show')), out = cf.querySelector('[data-cprice]'), other = cf.querySelector('[data-other]');
    function pick(n) { return (cf.querySelector('input[name="' + n + '"]:checked') || {}).value || ''; }
    function upd() {
      out.textContent = show[(pick('mutexessis') === 'both' ? 'both' : 'one') + '|' + (pick('format') || 'online')] || '';
      other.hidden = pick('movzu') !== 'other';
    }
    cf.addEventListener('change', upd); upd();
    cf.addEventListener('submit', async function (e) {
      e.preventDefault();
      var msg = cf.querySelector('.n-form-msg'), btn = cf.querySelector('button[type="submit"]'), ok = true;
      var need = ['ad', 'telefon']; if (pick('movzu') === 'other') need.push('simptom');
      need.forEach(function (n) { var el = cf.querySelector('[name="' + n + '"]'); var bad = !el.value.trim(); el.classList.toggle('is-bad', bad); if (bad) ok = false; });
      if (!ok) { msg.hidden = false; msg.className = 'n-form-msg is-err'; msg.textContent = cf.getAttribute('data-req'); return; }
      var lab = function (n) { var r = cf.querySelector('input[name="' + n + '"]:checked'); return r ? r.parentNode.textContent.trim() : ''; };
      var service = 'consult|' + pick('mutexessis') + '|' + pick('format');
      var note = lab('mutexessis') + ' · ' + lab('format') + ' · ' + lab('movzu') + (pick('movzu') === 'other' ? ': ' + cf.simptom.value.trim() : '');
      btn.disabled = true; var lbl = btn.textContent; btn.textContent = cf.getAttribute('data-sending');
      var payload = { type: 'registration', fname: cf.ad.value.trim(), lname: '', phone: cf.telefon.value.trim(), email: '', address: '',
                      service: service, lang: cf.getAttribute('data-lang'), note: note, source: location.pathname.replace(/^\//, ''), attachments: [] };
      var reg = await fetch('https://api.ragimoff.org/api/training-reg', { method: 'POST', headers: { 'Content-Type': 'text/plain;charset=utf-8' }, body: JSON.stringify(payload) })
        .then(function (r) { return r.ok ? r.json().catch(function () { return { ok: true }; }) : null; }, function () { return null; });
      if (reg && reg.prices) { btn.textContent = lbl; await payGo(cf, { name: payload.fname, phone: payload.phone, program: service, folder: reg.folder || '' }, 'prepay', btn); return; }
      btn.disabled = false; btn.textContent = lbl; msg.hidden = false;
      msg.className = 'n-form-msg' + (reg ? '' : ' is-err');
      msg.innerHTML = reg ? cf.getAttribute('data-ok') : cf.getAttribute('data-err') + ' <a href="https://wa.me/994702200376" target="_blank" rel="noopener">WhatsApp</a>';
    });
  })();

  /* short-term trainings form */
  var sf = document.getElementById('shortForm');
  if (sf) (function () {
    var groups = sf.querySelectorAll('[data-for]');
    function sync() {
      var v = (sf.querySelector('input[name="proqram"]:checked') || {}).value || '';
      Array.prototype.forEach.call(groups, function (g) { g.hidden = (g.getAttribute('data-for') === 'individual') !== (v === 'individual'); });
    }
    sf.addEventListener('change', sync); sync();
    Array.prototype.forEach.call(document.querySelectorAll('[data-pick]'), function (a) {
      a.addEventListener('click', function () {
        var r = sf.querySelector('input[name="proqram"][value="short-' + a.getAttribute('data-pick') + '"]');
        if (r) { r.checked = true; sync(); }
      });
    });
    function b64(f) { return new Promise(function (res) { var r = new FileReader(); r.onload = function () { res(String(r.result).split(',')[1] || ''); }; r.onerror = function () { res(''); }; r.readAsDataURL(f); }); }
    sf.addEventListener('submit', async function (e) {
      e.preventDefault();
      var msg = sf.querySelector('.n-form-msg'), btn = sf.querySelector('button[type="submit"]'), ok = true;
      ['ad', 'soyad', 'telefon', 'shexsiyyet'].forEach(function (n) {
        var el = sf.querySelector('[name="' + n + '"]');
        var bad = !el || (el.type === 'file' ? !el.files.length : !el.value.trim());
        if (el) el.classList.toggle('is-bad', bad);
        if (bad) ok = false;
      });
      if (!ok) { msg.hidden = false; msg.className = 'n-form-msg is-err'; msg.textContent = sf.getAttribute('data-req'); return; }
      var prog = sf.querySelector('input[name="proqram"]:checked'), progLbl = prog.parentNode.textContent.trim(), note, service = prog.value, mode = 'prepay';
      if (prog.value === 'individual') {
        var c = sf.querySelector('[data-calc]');
        var who = sf.querySelector('input[name="f_mutexessis"]:checked'), fmt = sf.querySelector('input[name="f_format"]:checked');
        note = progLbl + ' · ' + who.parentNode.textContent.trim() + ' · ' + fmt.parentNode.textContent.trim() + ' · ' +
               c.getAttribute('data-hours') + ' × ' + c.getAttribute('data-rate-v') + ' = ' + c.getAttribute('data-sum') + ' AZN';
        service = 'individual|' + who.value + '|' + fmt.value + '|' + c.getAttribute('data-hours');
      } else {
        note = progLbl;
      }
      btn.disabled = true; var lbl = btn.textContent; btn.textContent = sf.getAttribute('data-sending');
      var att = [], f = sf.querySelector('[name="shexsiyyet"]').files[0];
      if (f && f.size < 10 * 1024 * 1024) att.push({ field: 'shexsiyyet', filename: f.name, mime: f.type || 'application/octet-stream', data: await b64(f) });
      var payload = { type: 'registration', fname: sf.ad.value.trim(), lname: sf.soyad.value.trim(), phone: sf.telefon.value.trim(), email: '', address: '',
                      service: service, lang: sf.getAttribute('data-lang'), note: note, source: location.pathname.replace(/^\//, ''), attachments: att };
      var API = 'https://api.ragimoff.org';
      var reg = await fetch(API + '/api/training-reg', { method: 'POST', headers: { 'Content-Type': 'text/plain;charset=utf-8' }, body: JSON.stringify(payload) })
        .then(function (r) { return r.ok ? r.json().catch(function () { return { ok: true }; }) : null; }, function () { return null; });
      var res = !!reg;
      /* сумму считает сервер по коду программы (канон Кенана 08.11); браузер только ведёт на ePoint */
      if (reg && reg.prices) {
        btn.disabled = false; btn.textContent = lbl;
        payChoice(sf, { name: payload.fname + ' ' + payload.lname, phone: payload.phone, program: service, folder: reg.folder || '' }, reg.prices, service.indexOf('individual|') === 0);
        return;
      }
      btn.disabled = false; btn.textContent = lbl; msg.hidden = false;
      msg.className = 'n-form-msg' + (res ? '' : ' is-err');
      msg.innerHTML = res ? sf.getAttribute('data-ok') : sf.getAttribute('data-err') + ' <a href="https://wa.me/994702200376" target="_blank" rel="noopener">WhatsApp</a>';
      if (res) { sf.reset(); sync(); Array.prototype.forEach.call(sf.querySelectorAll('[data-calc]'), function (c) { c.dispatchEvent(new Event('input')); }); }
    });
  })();

  /* закреплённая горизонтальная лента (программы, статьи): вертикальная прокрутка двигает карточки влево по одной;
     карточка у центра выходит на передний план. После последней карточки страница идёт дальше. (Кенан 09.11) */
  Array.prototype.forEach.call(document.querySelectorAll('[data-hs]'), function (sec) {
    var stick = sec.querySelector('.n-hs-stick'), track = sec.querySelector('[data-hs-track]');
    if (!stick || !track) return;
    var cards = Array.prototype.slice.call(track.children), dist = 0, cur = 0, target = 0, raf = 0;
    function measure() {
      track.style.setProperty('--hx', '0px');
      dist = Math.max(0, track.scrollWidth - stick.clientWidth);
      sec.style.height = dist > 0 ? (innerHeight + dist * (innerWidth < 701 ? 1.1 : 0.9)) + 'px' : '';
      onScroll();
    }
    function apply(x) {
      track.style.setProperty('--hx', (-x).toFixed(1) + 'px');
      var mid = innerWidth / 2;
      cards.forEach(function (c) {
        var r = c.getBoundingClientRect(), d = Math.abs(r.left + r.width / 2 - mid) / innerWidth;
        c.style.setProperty('--cs', (1 - Math.min(.07, d * .12)).toFixed(3));
        c.style.setProperty('--co', (1 - Math.min(.5, d * .7)).toFixed(3));
      });
    }
    function loop() {
      raf = 0; cur += (target - cur) * .16;
      if (Math.abs(target - cur) < .3) cur = target;
      apply(cur);
      if (cur !== target) raf = requestAnimationFrame(loop);
    }
    function onScroll() {
      var r = sec.getBoundingClientRect(), total = sec.offsetHeight - innerHeight;
      var p = total > 0 ? Math.min(1, Math.max(0, -r.top / total)) : 0;
      target = p * dist;
      if (!raf) raf = requestAnimationFrame(loop);
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', measure);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(measure);
    measure();
  });

  /* выравнивание рядов карточек (Кенан 09.11): в каждом визуальном ряду соседние элементы карточек
     (метка, заголовок, текст, ссылка) получают общую высоту → стоят на одной линии; карточки одной высоты */
  var CARD = '.card, .svc-card, .feat-card, .xid-card, .info-card, .adv-card, .trust-card, .dir-card, .opp-card, .fmt-card, .step-card, .review-card, .def-card, .blog-card, .n-month';
  function alignRows() {
    var parents = [];
    Array.prototype.forEach.call(document.querySelectorAll(CARD), function (c) {
      if (c.closest('[data-hs]')) return;
      if (parents.indexOf(c.parentNode) < 0) parents.push(c.parentNode);
    });
    parents.forEach(function (par) {
      var cards = Array.prototype.filter.call(par.children, function (c) { return c.matches(CARD); });
      if (cards.length < 2) return;
      cards.forEach(function (c) { Array.prototype.forEach.call(c.children, function (k) { k.style.minHeight = ''; }); });
      var rows = { all: cards };   /* все карточки группы — одной высоты, даже в разных рядах */
      Object.keys(rows).forEach(function (t) {
        var row = rows[t];
        if (row.length < 2) return;
        var n = Math.max.apply(null, row.map(function (c) { return c.children.length; }));
        for (var i = 0; i < n - 1; i++) {      /* последний элемент (ссылка/кнопка) не тянем — его прижимает margin-top: auto */
          var els = row.map(function (c) { return c.children[i]; }).filter(Boolean);
          var h = Math.max.apply(null, els.map(function (e) { return e.getBoundingClientRect().height; }));
          els.forEach(function (e) { if (getComputedStyle(e).display !== 'none') e.style.minHeight = h + 'px'; });
        }
      });
    });
  }
  var alT = 0;
  function alignSoon() { clearTimeout(alT); alT = setTimeout(alignRows, 120); }
  window.addEventListener('resize', alignSoon);
  window.addEventListener('load', alignRows);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(alignRows);

  /* кнопки (Кенан 09.11): текст «перекатывается» при наведении, кнопка слегка тянется к курсору (только мышь) */
  if (window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
    Array.prototype.forEach.call(document.querySelectorAll('.n-btn, .n-body .btn, .n-cta'), function (b) {
      if (b.querySelector('.n-roll') || b.children.length > 1 || !b.textContent.trim()) return;
      var t = b.textContent.trim();
      b.innerHTML = '<span class="n-roll"><span>' + t.replace(/&/g, '&amp;').replace(/</g, '&lt;') + '</span><span aria-hidden="true">' +
        t.replace(/&/g, '&amp;').replace(/</g, '&lt;') + '</span></span>';
      b.addEventListener('mousemove', function (e) {
        var r = b.getBoundingClientRect();
        b.style.setProperty('--mxb', ((e.clientX - r.left - r.width / 2) * .18).toFixed(1) + 'px');
        b.style.setProperty('--myb', ((e.clientY - r.top - r.height / 2) * .28).toFixed(1) + 'px');
      });
      b.addEventListener('mouseleave', function () { b.style.setProperty('--mxb', '0px'); b.style.setProperty('--myb', '0px'); });
    });
  }

  if (reduce) return;

  /* spotlight in the first screen */
  Array.prototype.forEach.call(document.querySelectorAll('[data-spot]'), function (el) {
    el.addEventListener('mousemove', function (e) {
      var r = el.getBoundingClientRect();
      el.style.setProperty('--mx', (e.clientX - r.left) + 'px');
      el.style.setProperty('--my', (e.clientY - r.top) + 'px');
    });
  });

  /* painted first screen: the painting drifts slower than the page and slowly approaches (scroll-linked) */
  var paint = document.querySelector('[data-paint] img');
  if (paint) {
    var hero = paint.closest('.n-hero'), ticking = false;
    paint.addEventListener('animationend', function () { paint.style.animation = 'none'; upd(); });
    function upd() {
      ticking = false;
      var h = hero.offsetHeight || 1, y = Math.min(window.scrollY, h);
      var p = y / h;
      paint.style.setProperty('--py', (y * 0.35).toFixed(1) + 'px');
      paint.style.setProperty('--ps', (1.06 + p * 0.12).toFixed(4));
    }
    window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(upd); } }, { passive: true });
  }

  /* reveal content blocks as they enter the screen */
  if ('IntersectionObserver' in window) {
    var sel = '.n-body main > section:not(.n-hero) .sec-header, .xid-card, .feat-card, .price-card, .step-card, .opp-card, .adv-card, .review-card, .svc-card, .info-card, .trust-card, .fmt-card, .law-card, .dir-card, .def-card, .video-card, .blog-card, .bc, .process-step, .reg-path-step, .why-item, .stat-item, .n-person, .tl-row, .tl-item, .timeline-list li, .n-gallery .n-shot, .n-month, .price-card:not(.n-hs .price-card), .card, .n-who, .n-cta-box, .n-foot-mark, .book-card-row';
    var els = document.querySelectorAll(sel);
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.01 });
    Array.prototype.forEach.call(els, function (el, i) {
      var r = el.getBoundingClientRect();
      if (r.top < innerHeight || el.closest('[data-hs]')) return;   /* already on screen / inside a pinned ribbon — leave as is */
      el.classList.add('n-io');
      el.style.transitionDelay = (el.matches('.timeline-list li') ? (i % 2) * 0.12 : (i % 4) * 0.08) + 's';
      io.observe(el);
    });
  }
})();
