/* =====================================================================
   RAGIMOFF · test/nur/nur.js — движок концепта «NÜR»
   Прелоадер-счётчик · плавный скролл · магнитный курсор · золотые частицы ·
   видео-герой с параллаксом · пословный выезд заголовков · блок специалиста
   в одном экране · хроника по кадру · превью услуг · тилт книги · маркиза ·
   живое меню · тема с круговой волной · режим движения.
   Принцип: обработчики навешиваются ВСЕГДА; видимость решает html.mo/no-mo.
   ===================================================================== */
(function () {
  'use strict';

  var root = document.documentElement;
  var reduceQ = window.matchMedia('(prefers-reduced-motion: reduce)');
  var fineQ = window.matchMedia('(hover: hover) and (pointer: fine)');
  var THEME_KEY = root.getAttribute('data-theme-key') || 'ragimoff-theme';
  var MOTION_KEY = root.getAttribute('data-motion-key') || 'ragimoff-motion';
  var SCR = 'ABCDEFGHIJKLMNOPQRSTUVXYZ0123456789';
  var reduce = false, fine = false;

  function lsGet(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function lsSet(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  function $(s, c) { return (c || document).querySelector(s); }
  function $$(s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); }
  function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }

  /* ─────────────────────────── ТЕМА ─────────────────────────── */
  var theme = lsGet(THEME_KEY) || root.getAttribute('data-theme-default') || 'dark';
  function paintTheme(t) {
    root.setAttribute('data-theme', t);
    var meta = $('meta[name="theme-color"]');
    if (meta) meta.setAttribute('content', t === 'dark' ? (root.getAttribute('data-tc-dark') || '#06080D') : (root.getAttribute('data-tc-light') || '#F5F1E8'));
    $$('[data-theme-toggle]').forEach(function (b) {
      b.setAttribute('aria-pressed', t === 'dark' ? 'false' : 'true');
      var l = $('[data-theme-label]', b);
      if (l) l.textContent = t === 'dark' ? (b.getAttribute('data-label-to-light') || 'İşıq rejimi') : (b.getAttribute('data-label-to-dark') || 'Qaranlıq rejim');
    });
  }
  function setTheme(t, ev) {
    if (t === root.getAttribute('data-theme')) return;
    lsSet(THEME_KEY, t);
    var x = innerWidth - 48, y = 40, r = Math.hypot(innerWidth, innerHeight);
    if (ev && ev.currentTarget && ev.currentTarget.getBoundingClientRect) {
      var b = ev.currentTarget.getBoundingClientRect();
      x = b.left + b.width / 2; y = b.top + b.height / 2;
      r = Math.hypot(Math.max(x, innerWidth - x), Math.max(y, innerHeight - y));
    }
    var ok = !reduce && document.startViewTransition && window.CSS && CSS.supports && CSS.supports('view-transition-name', 'root');
    if (!ok) { paintTheme(t); return; }
    var vt = document.startViewTransition(function () { paintTheme(t); });
    vt.ready.then(function () {
      root.animate(
        { clipPath: ['circle(0px at ' + x + 'px ' + y + 'px)', 'circle(' + r + 'px at ' + x + 'px ' + y + 'px)'] },
        { duration: 700, easing: 'cubic-bezier(.625,.05,0,1)', pseudoElement: '::view-transition-new(root)' }
      );
    }).catch(function () {});
  }

  /* ─────────────────────── РЕЖИМ ДВИЖЕНИЯ ─────────────────────── */
  function computeReduce() {
    var p = lsGet(MOTION_KEY);
    if (p === 'on') return false;
    if (p === 'off') return true;
    return reduceQ.matches;
  }
  function paintMotion() {
    root.classList.toggle('mo', !reduce);
    root.classList.toggle('no-mo', reduce);
    root.setAttribute('data-motion', reduce ? 'off' : 'on');
    $$('[data-motion-toggle]').forEach(function (b) {
      b.setAttribute('aria-pressed', reduce ? 'false' : 'true');
      var l = $('[data-motion-label]', b);
      if (l) l.textContent = reduce ? (b.getAttribute('data-label-on') || 'Hərəkəti yandır') : (b.getAttribute('data-label-off') || 'Hərəkəti söndür');
    });
  }

  /* ───────────────────────── МЕНЮ ───────────────────────── */
  var menuOpen = false;
  function setMenu(open) {
    var m = $('[data-menu]');
    if (!m) return;
    menuOpen = open;
    m.classList.toggle('is-open', open);
    m.setAttribute('aria-hidden', open ? 'false' : 'true');
    root.classList.toggle('lock', open);
    $$('[data-menu-toggle]').forEach(function (b) { b.setAttribute('aria-expanded', open ? 'true' : 'false'); });
    if (open) { var f = m.querySelector('a, button'); if (f) setTimeout(function () { f.focus(); }, 80); }
  }
  function initMenuStage() {
    var m = $('[data-menu]'); if (!m) return;
    var stage = $('[data-menu-stage]', m); if (!stage) return;
    $$('[data-menu-img]', m).forEach(function (a) {
      a.addEventListener('mouseenter', function () {
        var src = a.getAttribute('data-menu-img');
        if (!src || stage.getAttribute('data-src') === src) return;
        stage.setAttribute('data-src', src);
        stage.style.backgroundImage = 'url("' + src + '")';
        stage.classList.remove('is-pop'); void stage.offsetWidth; stage.classList.add('is-pop');
      });
    });
    var first = $('[data-menu-img]', m);
    if (first && first.getAttribute('data-menu-img')) stage.style.backgroundImage = 'url("' + first.getAttribute('data-menu-img') + '")';
  }

  /* ──────────────────── ПЛАВНЫЙ СКРОЛЛ (lerp) ──────────────────── */
  function initSmooth() {
    if (!fine || reduce) return;
    var target = window.pageYOffset, current = target, raf = 0;
    root.classList.add('smooth');
    function loop() {
      current += (target - current) * 0.115;
      if (Math.abs(target - current) < 0.5) { current = target; window.scrollTo(0, Math.round(current)); raf = 0; return; }
      window.scrollTo(0, current);
      raf = requestAnimationFrame(loop);
    }
    window.addEventListener('wheel', function (e) {
      if (e.ctrlKey || root.classList.contains('lock')) return;
      e.preventDefault();
      var max = root.scrollHeight - innerHeight;
      target = clamp(target + e.deltaY, 0, max);
      if (!raf) raf = requestAnimationFrame(loop);
    }, { passive: false });
    window.addEventListener('scroll', function () {
      if (!raf) { target = current = window.pageYOffset; }
    }, { passive: true });
  }

  /* ──────────────────────── КУРСОР ──────────────────────── */
  var cur = null, cx = 0, cy = 0, tx = 0, ty = 0, curRaf = 0;
  function initCursor() {
    if (!fine) return;
    cur = document.createElement('div');
    cur.className = 'cur';
    cur.setAttribute('aria-hidden', 'true');
    cur.innerHTML = '<span class="cur__dot"></span><span class="cur__ring"></span><span class="cur__lbl"></span>';
    document.body.appendChild(cur);
    var lbl = $('.cur__lbl', cur);
    root.classList.add('cur-on');
    document.addEventListener('mousemove', function (e) {
      tx = e.clientX; ty = e.clientY;
      if (!curRaf) curRaf = requestAnimationFrame(tick);
    });
    function tick() {
      var k = reduce ? 1 : 0.2;
      cx += (tx - cx) * k; cy += (ty - cy) * k;
      cur.style.transform = 'translate3d(' + cx.toFixed(1) + 'px,' + cy.toFixed(1) + 'px,0)';
      if (Math.abs(tx - cx) > 0.4 || Math.abs(ty - cy) > 0.4) curRaf = requestAnimationFrame(tick); else curRaf = 0;
    }
    $$('a, button, [data-cursor-label]').forEach(function (el) {
      el.addEventListener('mouseenter', function () {
        cur.classList.add('is-hot');
        lbl.textContent = el.getAttribute('data-cursor-label') || '';
      });
      el.addEventListener('mouseleave', function () { cur.classList.remove('is-hot'); });
    });
  }

  /* ─────────────────────── МАГНИТНЫЕ КНОПКИ ─────────────────────── */
  function initMagnets() {
    if (!fine) return;
    $$('[data-magnet]').forEach(function (el) {
      var raf = 0, tX = 0, tY = 0, cX = 0, cY = 0;
      function tick() {
        cX += (tX - cX) * 0.2; cY += (tY - cY) * 0.2;
        el.style.transform = 'translate3d(' + cX.toFixed(1) + 'px,' + cY.toFixed(1) + 'px,0)';
        if (Math.abs(tX - cX) > 0.2 || Math.abs(tY - cY) > 0.2) raf = requestAnimationFrame(tick); else raf = 0;
      }
      el.addEventListener('mousemove', function (e) {
        if (reduce) return;
        var b = el.getBoundingClientRect();
        tX = (e.clientX - (b.left + b.width / 2)) * 0.24;
        tY = (e.clientY - (b.top + b.height / 2)) * 0.3;
        if (!raf) raf = requestAnimationFrame(tick);
      });
      el.addEventListener('mouseleave', function () { tX = 0; tY = 0; if (!raf) raf = requestAnimationFrame(tick); });
    });
  }

  /* ──────────────── ПОСЛОВНЫЙ ВЫЕЗД ЗАГОЛОВКОВ ──────────────── */
  function wordSpan(word, i) {
    var w = document.createElement('span'); w.className = 'w';
    var inner = document.createElement('i'); inner.textContent = word;
    inner.style.setProperty('--wd', i);
    w.appendChild(inner); return w;
  }
  function splitHeadings() {
    $$('[data-split]').forEach(function (h) {
      if (h.getAttribute('data-split-done')) return;
      var idx = 0, frag = document.createDocumentFragment();
      Array.prototype.slice.call(h.childNodes).forEach(function (node) {
        if (node.nodeType === 3) {
          node.textContent.split(/(\s+)/).forEach(function (part) {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(part)); return; }
            frag.appendChild(wordSpan(part, idx++));
          });
        } else if (node.nodeType === 1) {
          var el = node.cloneNode(false);
          var words = node.textContent.split(/\s+/).filter(Boolean);
          words.forEach(function (w, k) {
            el.appendChild(wordSpan(w, idx++));
            if (k < words.length - 1) el.appendChild(document.createTextNode(' '));
          });
          frag.appendChild(el);
        }
      });
      h.innerHTML = ''; h.appendChild(frag); h.setAttribute('data-split-done', '1');
    });
  }

  /* ─────────────────────── REVEAL ─────────────────────── */
  var rvIO = null;
  function initReveal() {
    var nodes = $$('[data-rv], [data-split]');
    if (!nodes.length) return;
    if (!('IntersectionObserver' in window)) { nodes.forEach(function (n) { n.classList.add('in'); }); return; }
    rvIO = new IntersectionObserver(function (ents) {
      ents.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); rvIO.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.08 });
    nodes.forEach(function (n) {
      var d = n.getAttribute('data-stagger'); if (d) n.style.setProperty('--delay', d + 'ms');
      rvIO.observe(n);
    });
  }

  /* ─────────── СПЕЦИАЛИСТ: появление в одном экране ─────────── */
  function initSpec() {
    var el = $('.spec'); if (!el) return;
    if (!('IntersectionObserver' in window)) { el.classList.add('in'); return; }
    var io = new IntersectionObserver(function (ents) {
      ents.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: 0.45 });
    io.observe(el);
    $$('.spec__dots li', el).forEach(function (li, i) { li.style.setProperty('--d', 350 + i * 120); });
  }

  /* ─────────────────────── СЧЁТЧИКИ ─────────────────────── */
  function initCounts() {
    var nodes = $$('[data-count]');
    if (!nodes.length || !('IntersectionObserver' in window)) return;
    var io = new IntersectionObserver(function (ents) {
      ents.forEach(function (e) {
        if (!e.isIntersecting) return;
        var el = e.target; io.unobserve(el);
        var to = parseFloat(el.getAttribute('data-count')) || 0;
        if (reduce) { el.textContent = el.getAttribute('data-count-final') || to; return; }
        var t0 = 0, dur = 1500;
        function step(ts) {
          if (!t0) t0 = ts;
          var k = clamp((ts - t0) / dur, 0, 1), e2 = 1 - Math.pow(1 - k, 3);
          var val = Math.round(to * e2);
          el.textContent = val >= 1000 ? val.toLocaleString('az') : String(val);
          if (k < 1) requestAnimationFrame(step); else el.textContent = el.getAttribute('data-count-final') || String(to);
        }
        requestAnimationFrame(step);
      });
    }, { threshold: 0.4 });
    nodes.forEach(function (n) { io.observe(n); });
  }

  /* ─────────────────────── ПАРАЛЛАКС ─────────────────────── */
  var plx = [];
  function collectPlx() {
    plx = $$('[data-plx]').map(function (el) { return { el: el, k: parseFloat(el.getAttribute('data-plx')) || 0.05 }; });
  }
  function runPlx() {
    if (reduce) return;
    var h = innerHeight;
    for (var i = 0; i < plx.length; i++) {
      var r = plx[i].el.getBoundingClientRect();
      if (r.bottom < -120 || r.top > h + 120) continue;
      var mid = r.top + r.height / 2 - h / 2;
      plx[i].el.style.setProperty('--plx', (-mid * plx[i].k).toFixed(1) + 'px');
    }
  }

  /* ──────────── ГЕРОЙ: видео, мышь-параллакс, скролл-аут ──────────── */
  var hero = null, heroVid = null, heroLayers = [];
  function initHero() {
    hero = $('.hero'); if (!hero) return;
    heroVid = $('.hero__media video', hero);
    if (heroVid) { var p = heroVid.play(); if (p && p.catch) p.catch(function () {}); }
    heroLayers = $$('[data-hx]', hero).map(function (el) {
      return { el: el, k: parseFloat(el.getAttribute('data-hx')) || 0.01 };
    });
    if (fine) {
      hero.addEventListener('mousemove', function (e) {
        if (reduce) return;
        var b = hero.getBoundingClientRect();
        var dx = (e.clientX - b.left) / b.width - 0.5;
        var dy = (e.clientY - b.top) / b.height - 0.5;
        heroLayers.forEach(function (L) {
          L.el.style.setProperty('--mx', (dx * L.k * 100).toFixed(2) + 'px');
          L.el.style.setProperty('--my', (dy * L.k * 100).toFixed(2) + 'px');
        });
      });
    }
  }

  /* ──────────────── ЗОЛОТЫЕ ЧАСТИЦЫ (canvas) ──────────────── */
  function initDust() {
    var cv = $('.hero__canvas');
    if (!cv || reduce || !fine) { if (cv) cv.style.display = 'none'; return; }
    var ctx = cv.getContext('2d');
    var dpr = Math.min(2, window.devicePixelRatio || 1);
    var W = 0, H = 0, parts = [];
    function size() {
      W = cv.clientWidth; H = cv.clientHeight;
      cv.width = W * dpr; cv.height = H * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var n = innerWidth < 900 ? 34 : 70;
      parts = [];
      for (var i = 0; i < n; i++) {
        parts.push({
          x: Math.random() * W, y: Math.random() * H,
          r: 0.5 + Math.random() * 1.5,
          v: 0.12 + Math.random() * 0.35,
          a: 0.12 + Math.random() * 0.5,
          ph: Math.random() * Math.PI * 2
        });
      }
    }
    size();
    window.addEventListener('resize', size);
    (function loop(t) {
      if (!reduce) {
        ctx.clearRect(0, 0, W, H);
        for (var i = 0; i < parts.length; i++) {
          var p = parts[i];
          p.y -= p.v;
          p.x += Math.sin((t || 0) / 2600 + p.ph) * 0.22;
          if (p.y < -6) { p.y = H + 6; p.x = Math.random() * W; }
          ctx.beginPath();
          ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
          ctx.fillStyle = 'rgba(201,169,97,' + p.a.toFixed(2) + ')';
          ctx.fill();
        }
      }
      requestAnimationFrame(loop);
    })(0);
  }

  /* ──────────────── ХРОНИКА: кадр на шаг скролла ──────────────── */
  var seqs = [];
  function collectSeqs() {
    var narrow = innerWidth <= 720;
    seqs = $$('[data-seq]').map(function (el) {
      var items = $$('[data-seq-item]', el);
      var idxRoot = el.closest('[data-seq-root]') || el;
      el.style.setProperty('--seq-n', items.length);
      var stepAttr = el.getAttribute('data-seq-step');
      if (stepAttr) el.style.setProperty('--seq-step', stepAttr);
      el.classList.toggle('is-static', narrow);
      return {
        el: el, items: items, n: items.length || 1, static: narrow,
        num: $('[data-seq-num]', el),
        bar: (function () { var w = $('[data-seq-bar]', el); return w ? ($('i', w) || w) : null; })(),
        idx: $$('[data-seq-idx]', idxRoot)
      };
    });
  }
  function runSeq() {
    for (var s = 0; s < seqs.length; s++) {
      var q = seqs[s], r = q.el.getBoundingClientRect();
      if (r.bottom < -200 || r.top > innerHeight + 200) {
        q.items.forEach(function (it) { it.classList.remove('is-live'); });
        if (q.idx) q.idx.forEach(function (it) { it.classList.remove('is-live'); });
        continue;
      }
      if (reduce || q.static) {
        for (var j = 0; j < q.n; j++) q.items[j].style.removeProperty('--o');
        if (q.bar) q.bar.style.transform = '';
        continue;
      }
      var span = q.el.offsetHeight - innerHeight; if (span <= 1) span = 1;
      var p = clamp(-r.top / span, 0, 1);
      var head = p * q.n;
      var live = Math.min(q.n - 1, Math.floor(head));
      if (q.bar) q.bar.style.transform = 'scaleX(' + p.toFixed(4) + ')';
      for (var i = 0; i < q.n; i++) {
        var o = clamp((head - i) / 0.62, 0, 1);
        q.items[i].style.setProperty('--o', o.toFixed(3));
      }
      if (q.num) {
        var t = String(live + 1); if (t.length < 2) t = '0' + t;
        t = t + '/' + (q.n < 10 ? '0' + q.n : q.n);
        if (q.num.textContent !== t) q.num.textContent = t;
      }
      if (q.idx && q.idx.length) {
        for (var k2 = 0; k2 < q.idx.length; k2++) q.idx[k2].classList.toggle('is-live', k2 === live);
      }
    }
  }

  /* ──────────────── КУРСОР-ПРЕВЬЮ УСЛУГ ──────────────── */
  var peek = null, pX = 0, pY = 0, pTX = 0, pTY = 0, pRaf = 0;
  function initPeek() {
    var host = $('[data-peek-host]'); if (!host) return;
    peek = document.createElement('div');
    peek.className = 'peek'; peek.setAttribute('aria-hidden', 'true');
    peek.innerHTML = '<span class="peek__img"></span>';
    host.appendChild(peek);
    var img = $('.peek__img', peek);
    $$('[data-img]', host).forEach(function (row) {
      function show() { var s = row.getAttribute('data-img'); if (s) img.style.backgroundImage = 'url("' + s + '")'; peek.classList.add('is-on'); }
      function hide() { peek.classList.remove('is-on'); }
      row.addEventListener('mouseenter', show);
      row.addEventListener('mouseleave', hide);
      row.addEventListener('focus', show); row.addEventListener('blur', hide);
    });
    host.addEventListener('mousemove', function (e) {
      var b = host.getBoundingClientRect();
      pTX = e.clientX - b.left; pTY = e.clientY - b.top;
      if (!pRaf) pRaf = requestAnimationFrame(tick);
    });
    host.addEventListener('mouseleave', function () { if (peek) peek.classList.remove('is-on'); });
    function tick() {
      var k = reduce ? 1 : 0.16;
      pX += (pTX - pX) * k; pY += (pTY - pY) * k;
      peek.style.transform = 'translate3d(' + pX.toFixed(1) + 'px,' + pY.toFixed(1) + 'px,0)';
      if (Math.abs(pTX - pX) > 0.4 || Math.abs(pTY - pY) > 0.4) pRaf = requestAnimationFrame(tick); else pRaf = 0;
    }
  }

  /* ──────────────── ТИЛТ КНИГИ ──────────────── */
  function initTilt() {
    if (!fine) return;
    $$('[data-tilt]').forEach(function (el) {
      el.addEventListener('mousemove', function (e) {
        if (reduce) return;
        var b = el.getBoundingClientRect();
        var dx = (e.clientX - b.left) / b.width - 0.5;
        var dy = (e.clientY - b.top) / b.height - 0.5;
        el.style.transform = 'perspective(900px) rotateY(' + (dx * 8).toFixed(2) + 'deg) rotateX(' + (-dy * 8).toFixed(2) + 'deg)';
      });
      el.addEventListener('mouseleave', function () { el.style.transform = ''; });
    });
  }

  /* ──────────────── МАРКИЗА + ФУТЕР-ВОРДМАРК ──────────────── */
  var mq = null, ftWord = null;
  function prepMarquee() {
    mq = $('.mq__track');
    if (mq) mq.innerHTML += mq.innerHTML;
    ftWord = $('.ft__word');
  }

  /* ──────────────── ПРЕЛОАДЕР ──────────────── */
  function initPre() {
    var n = $('[data-pre-num]'), bar = $('[data-pre-bar]');
    if (!n) return;
    if (reduce) { n.textContent = '100'; if (bar) bar.style.transform = 'scaleX(1)'; return; }
    var t0 = 0, dur = 1250;
    function step(ts) {
      if (!t0) t0 = ts;
      var k = clamp((ts - t0) / dur, 0, 1);
      var e = 1 - Math.pow(1 - k, 2.2);
      n.textContent = String(Math.round(e * 100)).padStart(3, '0');
      if (bar) bar.style.transform = 'scaleX(' + e.toFixed(3) + ')';
      if (k < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  /* ──────────────── ПРОКРУТКА ──────────────── */
  var prog = null, hdr = null, railFill = null, railDot = null, railPct = null, railLbl = null, railSecs = [], lastY = 0;
  function runScroll() {
    var y = window.pageYOffset || root.scrollTop;
    if (prog) {
      var max = root.scrollHeight - innerHeight;
      prog.style.transform = 'scaleX(' + (max > 0 ? clamp(y / max, 0, 1).toFixed(4) : 0) + ')';
    }
    if (hdr) {
      hdr.classList.toggle('is-stuck', y > 40);
      var dy = y - lastY;
      if (y > 200 && dy > 6) hdr.classList.add('is-hidden');
      else if (dy < -6 || y <= 200) hdr.classList.remove('is-hidden');
    }
    if (mq) mq.style.setProperty('--mq-skew', (clamp((y - lastY) / 26, -3, 3) * 0.22).toFixed(2) + 'deg');
    if (hero) hero.style.setProperty('--hero-y', y.toFixed(0) + 'px');
    if (ftWord) {
      var fr = ftWord.getBoundingClientRect();
      var p = clamp((innerHeight - fr.top) / (innerHeight + fr.height), 0, 1);
      ftWord.style.setProperty('--ft-x', ((p - 0.5) * -12).toFixed(2) + '%');
    }
    if (railFill) {
      var mx = root.scrollHeight - innerHeight;
      var t = mx > 0 ? clamp(y / mx, 0, 1) : 0;
      railFill.style.transform = 'scaleY(' + t.toFixed(4) + ')';
      if (railDot) railDot.style.top = (t * 100).toFixed(2) + '%';
      if (railPct) { var s = Math.round(t * 100) + '%'; if (railPct.textContent !== s) railPct.textContent = s; }
      if (railLbl && railSecs.length) {
        var mid = innerHeight * 0.45, name = railSecs[0].getAttribute('data-rail');
        for (var i = 0; i < railSecs.length; i++) { if (railSecs[i].getBoundingClientRect().top <= mid) name = railSecs[i].getAttribute('data-rail'); }
        if (railLbl.textContent !== name) railLbl.textContent = name;
      }
    }
    lastY = y;
    runSeq(); runPlx();
  }
  function onScroll() {
    if (onScroll.q) return;
    onScroll.q = true;
    requestAnimationFrame(function () { onScroll.q = false; runScroll(); });
  }

  /* ──────────────── SCRAMBLE ──────────────── */
  function initScramble() {
    $$('[data-scramble]').forEach(function (el) {
      var orig = el.textContent, busy = false;
      el.addEventListener('mouseenter', function () {
        if (reduce || busy) return;
        busy = true;
        var t0 = 0, dur = 420;
        function step(ts) {
          if (!t0) t0 = ts;
          var k = clamp((ts - t0) / dur, 0, 1), out = '';
          for (var i = 0; i < orig.length; i++) {
            var ch = orig.charAt(i);
            if (ch === ' ') { out += ch; continue; }
            out += (k >= i / orig.length) ? ch : SCR.charAt((Math.random() * SCR.length) | 0);
          }
          el.textContent = out;
          if (k < 1) requestAnimationFrame(step); else { el.textContent = orig; busy = false; }
        }
        requestAnimationFrame(step);
      });
    });
  }

  /* ──────────────── СТАРТ ──────────────── */
  function bind() {
    $$('[data-theme-toggle]').forEach(function (b) {
      b.addEventListener('click', function (e) { setTheme(root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark', e); });
    });
    $$('[data-motion-toggle]').forEach(function (b) {
      b.addEventListener('click', function () {
        reduce = !reduce;
        lsSet(MOTION_KEY, reduce ? 'off' : 'on');
        paintMotion();
        if (!reduce) requestAnimationFrame(runScroll);
        b.blur();
      });
    });
    $$('[data-menu-toggle]').forEach(function (b) { b.addEventListener('click', function () { setMenu(!menuOpen); }); });
    var x = $('[data-menu-close]'); if (x) x.addEventListener('click', function () { setMenu(false); });
    $$('[data-menu] a').forEach(function (a) { a.addEventListener('click', function () { setMenu(false); }); });
    document.addEventListener('keydown', function (e) {
      var tag = (e.target.tagName || '').toLowerCase();
      var typing = tag === 'input' || tag === 'textarea' || e.target.isContentEditable;
      if (e.key === 'Escape' && menuOpen) { setMenu(false); return; }
      if (typing) return;
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'j') { e.preventDefault(); setTheme(root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark'); }
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); setMenu(!menuOpen); }
    });
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', function () { fine = fineQ.matches; collectSeqs(); collectPlx(); onScroll(); });
    reduceQ.addEventListener && reduceQ.addEventListener('change', function () {
      if (!lsGet(MOTION_KEY)) { reduce = computeReduce(); paintMotion(); onScroll(); }
    });
  }

  function boot() {
    reduce = computeReduce();
    fine = fineQ.matches;
    paintTheme(theme);
    paintMotion();
    if (root.getAttribute('data-theme-default') !== theme) lsSet(THEME_KEY, theme);

    prog = $('[data-progress]');
    hdr = $('[data-header]');
    railFill = $('[data-rail-fill]'); railDot = $('[data-rail-dot]');
    railPct = $('[data-pct]'); railLbl = $('[data-rail-lbl]');
    railSecs = $$('[data-rail]');

    bind();
    initPre();
    initSmooth();
    prepMarquee();
    splitHeadings();
    initMenuStage();
    initHero();
    initDust();
    initSpec();
    collectSeqs();
    collectPlx();
    initReveal();
    initCounts();
    initPeek();
    initTilt();
    initScramble();
    initMagnets();
    initCursor();

    root.classList.add('js-ready');
    if (hero) {
      var delay = reduce ? 0 : 1650;
      if (reduce) hero.classList.add('is-in');
      else requestAnimationFrame(function () { setTimeout(function () { hero.classList.add('is-in'); }, delay); });
    }
    requestAnimationFrame(function () { onScroll(); });
    setTimeout(onScroll, 300);
    setTimeout(onScroll, 1200);
    window.addEventListener('load', onScroll);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();