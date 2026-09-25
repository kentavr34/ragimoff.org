/* =====================================================================
   RAGIMOFF · test/motion.js — движок концепта «NƏBZ»
   Модули: тема · режим движения · полноэкранное меню с фото-сценой ·
   пульс-рельс с названием раздела · ЭКГ-линия по скроллу · пословный
   выезд заголовков · scramble-текст · магнитные кнопки · курсор-кольцо ·
   покадровая галерея (data-seq) · reveal · счётчики · параллакс ·
   курсор-превью · маркиза со склоном · прогресс.
   Принцип: обработчики навешиваются ВСЕГДА; видимость эффектов решают
   классы html.mo / html.no-mo (уважение prefers-reduced-motion, §0.18).
   ===================================================================== */
(function () {
  'use strict';

  var root = document.documentElement;
  var reduceQ = window.matchMedia('(prefers-reduced-motion: reduce)');
  var fineQ = window.matchMedia('(hover: hover) and (pointer: fine)');
  var THEME_KEY = root.getAttribute('data-theme-key') || 'ragimoff-theme';
  var MOTION_KEY = root.getAttribute('data-motion-key') || 'ragimoff-motion';
  var SCR = 'ABCDEFGHIJKLMNOPQRSTUVXYZ0123456789';
  var reduce = false;
  var fine = false;

  function lsGet(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function lsSet(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  function $(s, c) { return (c || document).querySelector(s); }
  function $$(s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); }
  function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }

  /* ─────────────────────────────── ТЕМА ─────────────────────────────── */
  var theme = lsGet(THEME_KEY) || root.getAttribute('data-theme-default') || 'dark';

  function paintTheme(t) {
    root.setAttribute('data-theme', t);
    var meta = $('meta[name="theme-color"]');
    if (meta) {
      meta.setAttribute('content',
        t === 'dark'
          ? (root.getAttribute('data-tc-dark') || '#0A0F18')
          : (root.getAttribute('data-tc-light') || '#F4F0E8'));
    }
    $$('[data-theme-toggle]').forEach(function (b) {
      b.setAttribute('aria-pressed', t === 'dark' ? 'false' : 'true');
      var l = $('[data-theme-label]', b);
      if (l) l.textContent = t === 'dark'
        ? (b.getAttribute('data-label-to-light') || 'İşıq rejimi')
        : (b.getAttribute('data-label-to-dark') || 'Qaranlıq rejim');
    });
  }

  function setTheme(t, ev) {
    if (t === root.getAttribute('data-theme')) return;
    lsSet(THEME_KEY, t);
    var x = innerWidth - 48, y = 40, r = Math.hypot(innerWidth, innerHeight);
    if (ev && ev.currentTarget && ev.currentTarget.getBoundingClientRect) {
      var b = ev.currentTarget.getBoundingClientRect();
      x = b.left + b.width / 2;
      y = b.top + b.height / 2;
      r = Math.hypot(Math.max(x, innerWidth - x), Math.max(y, innerHeight - y));
    }
    var ok = !reduce && document.startViewTransition &&
      window.CSS && CSS.supports && CSS.supports('view-transition-name', 'root');
    if (!ok) { paintTheme(t); return; }
    var vt = document.startViewTransition(function () { paintTheme(t); });
    vt.ready.then(function () {
      root.animate(
        { clipPath: ['circle(0px at ' + x + 'px ' + y + 'px)',
                     'circle(' + r + 'px at ' + x + 'px ' + y + 'px)'] },
        { duration: 640, easing: 'cubic-bezier(.625,.05,0,1)',
          pseudoElement: '::view-transition-new(root)' }
      );
    }).catch(function () {});
  }

  /* ────────────────────────── РЕЖИМ ДВИЖЕНИЯ ───────────────────────── */
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
      if (l) l.textContent = reduce
        ? (b.getAttribute('data-label-on') || 'Hərəkəti yandır')
        : (b.getAttribute('data-label-off') || 'Hərəkəti söndür');
    });
  }

  /* ───────────────────────── МЕНЮ + ФОТО-СЦЕНА ───────────────────────── */
  var menuOpen = false;
  function setMenu(open) {
    var m = $('[data-menu]');
    if (!m) return;
    menuOpen = open;
    m.classList.toggle('is-open', open);
    m.setAttribute('aria-hidden', open ? 'false' : 'true');
    root.classList.toggle('menu-lock', open);
    $$('[data-menu-toggle]').forEach(function (b) { b.setAttribute('aria-expanded', open ? 'true' : 'false'); });
    if (open) {
      var f = m.querySelector('a, button');
      if (f) setTimeout(function () { f.focus(); }, 60);
    }
  }
  function initMenuStage() {
    var m = $('[data-menu]');
    if (!m) return;
    var stage = $('[data-menu-stage]', m);
    if (!stage) return;
    $$('[data-menu-img]', m).forEach(function (a) {
      a.addEventListener('mouseenter', function () {
        var src = a.getAttribute('data-menu-img');
        if (!src || stage.getAttribute('data-src') === src) return;
        stage.setAttribute('data-src', src);
        stage.style.backgroundImage = 'url("' + src + '")';
        stage.classList.remove('is-pop');
        void stage.offsetWidth;
        stage.classList.add('is-pop');
      });
    });
    var first = $('[data-menu-img]', m);
    if (first && first.getAttribute('data-menu-img')) {
      stage.style.backgroundImage = 'url("' + first.getAttribute('data-menu-img') + '")';
    }
  }

  /* ───────────────────── ПОСЛЕДОВАТЕЛЬНАЯ ГАЛЕРЕЯ ───────────────────── */
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
        cap: $('[data-seq-cap]', el),
        bar: $('[data-seq-bar] i, [data-seq-bar]', el),
        idx: $$('[data-seq-idx]', idxRoot)
      };
    });
  }
  function runSeq() {
    for (var s = 0; s < seqs.length; s++) {
      var q = seqs[s], r = q.el.getBoundingClientRect();
      if (r.bottom < -200 || r.top > innerHeight + 200) continue;

      if (reduce || q.static) {
        for (var j = 0; j < q.n; j++) q.items[j].style.removeProperty('--o');
        q.items.forEach(function (it) { it.classList.remove('is-live'); });
        if (q.idx) q.idx.forEach(function (it) { it.classList.remove('is-live'); });
        if (q.bar) q.bar.style.transform = '';
        continue;
      }

      var span = q.el.offsetHeight - innerHeight;
      if (span <= 1) span = 1;
      var p = clamp(-r.top / span, 0, 1);
      var head = p * q.n;
      var live = Math.min(q.n - 1, Math.floor(head));
      q.el.style.setProperty('--seq-p', p.toFixed(4));
      if (q.bar) q.bar.style.transform = 'scaleX(' + p.toFixed(4) + ')';

      for (var i = 0; i < q.n; i++) {
        var o = clamp((head - i) / 0.62, 0, 1);
        var on = r.top < innerHeight * 0.62 && r.bottom > innerHeight * 0.25;
        q.items[i].style.setProperty('--o', o.toFixed(3));
        q.items[i].classList.toggle('is-live', on && i === live);
      }
      if (q.num) {
        var t = String(live + 1);
        if (t.length < 2) t = '0' + t;
        t = t + '/' + (q.n < 10 ? '0' + q.n : q.n);
        if (q.num.textContent !== t) q.num.textContent = t;
      }
      if (q.idx && q.idx.length) {
        for (var k2 = 0; k2 < q.idx.length; k2++) {
          q.idx[k2].classList.toggle('is-live', k2 === live);
        }
      }
      if (q.cap) {
        var c = q.items[live] && q.items[live].getAttribute('data-cap');
        if (c && q.cap.textContent !== c) {
          q.cap.classList.add('is-out');
          (function (node, txt) {
            setTimeout(function () { node.textContent = txt; node.classList.remove('is-out'); }, reduce ? 0 : 180);
          })(q.cap, c);
        }
      }
    }
  }

  /* ──────────────────────── ЭКГ-ЛИНИЯ ПО СКРОЛЛУ ──────────────────── */
  var ecgPath = null, ecgStage = null, ecgDot = null, ecgLen = 0, ecgVB = [0, 0, 1200, 160];
  function initEcg() {
    ecgPath = $('[data-ecg]');
    if (!ecgPath) return;
    ecgStage = ecgPath.closest('.nbz__stage') || ecgPath.parentElement;
    ecgDot = $('[data-ecg-dot]');
    try { ecgLen = ecgPath.getTotalLength(); } catch (e) { ecgLen = 0; }
    if (ecgLen) ecgPath.style.setProperty('--ecg-len', ecgLen.toFixed(1));
    var vb = (ecgPath.getAttribute('viewBox') || '0 0 1200 160').split(/[\s,]+/).map(parseFloat);
    if (vb.length === 4) ecgVB = vb;
  }
  function runEcg() {
    if (!ecgPath || !ecgLen || reduce || !ecgStage) return;
    var r = ecgStage.getBoundingClientRect();
    if (r.bottom < 0 || r.top > innerHeight) return;
    var span = r.height + innerHeight * 0.55;
    var p = clamp((innerHeight - r.top) / span, 0, 1);
    ecgPath.style.setProperty('--ecg-off', (ecgLen * (1 - p)).toFixed(1));
    if (ecgDot) {
      var pt = ecgPath.getPointAtLength(ecgLen * p);
      var sr = ecgPath.getBoundingClientRect();
      var sx = sr.width / (ecgVB[2] || 1200), sy = sr.height / (ecgVB[3] || 160);
      ecgDot.style.left = ((sr.left - r.left) + pt.x * sx).toFixed(1) + 'px';
      ecgDot.style.top = ((sr.top - r.top) + pt.y * sy).toFixed(1) + 'px';
    }
  }

  /* ───────────────────────── ПУЛЬС-РЕЛЬС ───────────────────────── */
  var railFill = null, railDot = null, railPct = null, railLbl = null, railSecs = [];
  function initRail() {
    railFill = $('[data-rail-fill]');
    railDot = $('[data-rail-dot]');
    railPct = $('[data-pct]');
    railLbl = $('[data-rail-lbl]');
    railSecs = $$('[data-rail]');
  }
  function runRail() {
    if (!railFill) return;
    var y = window.pageYOffset || root.scrollTop;
    var max = root.scrollHeight - innerHeight;
    var t = max > 0 ? clamp(y / max, 0, 1) : 0;
    railFill.style.transform = 'scaleY(' + t.toFixed(4) + ')';
    if (railDot) railDot.style.top = (t * 100).toFixed(2) + '%';
    if (railPct) {
      var s = Math.round(t * 100) + '%';
      if (railPct.textContent !== s) railPct.textContent = s;
    }
    if (railLbl && railSecs.length) {
      var mid = innerHeight * 0.45, name = railSecs[0].getAttribute('data-rail');
      for (var i = 0; i < railSecs.length; i++) {
        var r = railSecs[i].getBoundingClientRect();
        if (r.top <= mid) name = railSecs[i].getAttribute('data-rail');
      }
      if (railLbl.textContent !== name) railLbl.textContent = name;
    }
  }

  /* ─────────────── ПОСЛОВНЫЙ ВЫЕЗД ЗАГОЛОВКОВ (data-split) ─────────── */
  function wordSpan(word, i) {
    var w = document.createElement('span');
    w.className = 'w';
    var inner = document.createElement('i');
    inner.textContent = word;
    inner.style.setProperty('--wd', i);
    w.appendChild(inner);
    return w;
  }
  function splitHeadings() {
    $$('[data-split]').forEach(function (h) {
      if (h.getAttribute('data-split-done')) return;
      var idx = 0;
      var frag = document.createDocumentFragment();
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
      h.innerHTML = '';
      h.appendChild(frag);
      h.setAttribute('data-split-done', '1');
    });
  }

  /* ───────────────────────── REVEAL ───────────────────────── */
  var rvIO = null;
  function initReveal() {
    var nodes = $$('[data-rv], [data-split]');
    if (!nodes.length) return;
    if (!('IntersectionObserver' in window)) {
      nodes.forEach(function (n) { n.classList.add('in'); });
      return;
    }
    rvIO = new IntersectionObserver(function (ents) {
      ents.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add('in');
          rvIO.unobserve(e.target);
        }
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.08 });
    nodes.forEach(function (n) {
      var d = n.getAttribute('data-stagger');
      if (d) n.style.setProperty('--delay', d + 'ms');
      rvIO.observe(n);
    });
  }

  /* ──────────────────────── SCRAMBLE-ТЕКСТ ──────────────────────── */
  function initScramble() {
    $$('[data-scramble]').forEach(function (el) {
      var orig = el.textContent;
      var busy = false;
      el.addEventListener('mouseenter', function () {
        if (reduce || busy) return;
        busy = true;
        var t0 = 0, dur = 420;
        function step(ts) {
          if (!t0) t0 = ts;
          var k = clamp((ts - t0) / dur, 0, 1);
          var out = '';
          for (var i = 0; i < orig.length; i++) {
            var ch = orig.charAt(i);
            if (ch === ' ' || ch === '·') { out += ch; continue; }
            out += (k >= i / orig.length) ? ch : SCR.charAt((Math.random() * SCR.length) | 0);
          }
          el.textContent = out;
          if (k < 1) requestAnimationFrame(step);
          else { el.textContent = orig; busy = false; }
        }
        requestAnimationFrame(step);
      });
    });
  }

  /* ─────────────────────── МАГНИТНЫЕ КНОПКИ ─────────────────────── */
  function initMagnets() {
    if (!fine) return;
    $$('[data-magnet]').forEach(function (el) {
      var raf = 0, tx = 0, ty = 0, cx = 0, cy = 0;
      function tick() {
        cx += (tx - cx) * 0.18;
        cy += (ty - cy) * 0.18;
        el.style.transform = 'translate3d(' + cx.toFixed(1) + 'px,' + cy.toFixed(1) + 'px,0)';
        if (Math.abs(tx - cx) > 0.2 || Math.abs(ty - cy) > 0.2) raf = requestAnimationFrame(tick);
        else raf = 0;
      }
      el.addEventListener('mousemove', function (e) {
        if (reduce) return;
        var b = el.getBoundingClientRect();
        tx = (e.clientX - (b.left + b.width / 2)) * 0.26;
        ty = (e.clientY - (b.top + b.height / 2)) * 0.32;
        if (!raf) raf = requestAnimationFrame(tick);
      });
      el.addEventListener('mouseleave', function () {
        tx = 0; ty = 0;
        if (!raf) raf = requestAnimationFrame(tick);
      });
    });
  }

  /* ──────────────────────── КУРСОР-КОЛЬЦО ──────────────────────── */
  var cur = null, curX = 0, curY = 0, curTX = 0, curTY = 0, curRaf = 0;
  function initCursor() {
    if (!fine) return;
    cur = document.createElement('div');
    cur.className = 'cur';
    cur.setAttribute('aria-hidden', 'true');
    cur.innerHTML = '<span class="cur__ring"></span><span class="cur__lbl"></span>';
    document.body.appendChild(cur);
    var lbl = $('.cur__lbl', cur);

    document.addEventListener('mousemove', function (e) {
      curTX = e.clientX; curTY = e.clientY;
      if (!curRaf) curRaf = requestAnimationFrame(curTick);
    });
    function curTick() {
      var k = reduce ? 1 : 0.18;
      curX += (curTX - curX) * k;
      curY += (curTY - curY) * k;
      cur.style.transform = 'translate3d(' + curX.toFixed(1) + 'px,' + curY.toFixed(1) + 'px,0)';
      if (Math.abs(curTX - curX) > 0.4 || Math.abs(curTY - curY) > 0.4) curRaf = requestAnimationFrame(curTick);
      else curRaf = 0;
    }
    $$('a, button, [data-cursor-label]').forEach(function (el) {
      el.addEventListener('mouseenter', function () {
        cur.classList.add('is-hot');
        lbl.textContent = el.getAttribute('data-cursor-label') || '';
      });
      el.addEventListener('mouseleave', function () { cur.classList.remove('is-hot'); });
    });
  }

  /* ──────────────────────── СЧЁТЧИКИ ──────────────────────── */
  var cntIO = null;
  function initCounts() {
    var nodes = $$('[data-count]');
    if (!nodes.length || !('IntersectionObserver' in window)) return;
    cntIO = new IntersectionObserver(function (ents) {
      ents.forEach(function (e) {
        if (!e.isIntersecting) return;
        var el = e.target;
        cntIO.unobserve(el);
        var to = parseFloat(el.getAttribute('data-count')) || 0;
        if (reduce) { el.textContent = el.getAttribute('data-count-final') || to; return; }
        var t0 = 0, dur = 1400;
        function step(ts) {
          if (!t0) t0 = ts;
          var k = clamp((ts - t0) / dur, 0, 1);
          var e2 = 1 - Math.pow(1 - k, 3);
          var val = Math.round(to * e2);
          el.textContent = val >= 1000 ? val.toLocaleString('az') : String(val);
          if (k < 1) requestAnimationFrame(step);
          else el.textContent = el.getAttribute('data-count-final') || String(to);
        }
        requestAnimationFrame(step);
      });
    }, { threshold: 0.4 });
    nodes.forEach(function (n) { cntIO.observe(n); });
  }

  /* ───────────────────────── ПАРАЛЛАКС ───────────────────────── */
  var plx = [];
  function collectPlx() {
    plx = $$('[data-plx]').map(function (el) {
      return { el: el, k: parseFloat(el.getAttribute('data-plx')) || 0.05 };
    });
  }
  function runPlx() {
    if (reduce) return;
    var h = innerHeight;
    for (var i = 0; i < plx.length; i++) {
      var r = plx[i].el.getBoundingClientRect();
      if (r.bottom < -100 || r.top > h + 100) continue;
      var mid = r.top + r.height / 2 - h / 2;
      plx[i].el.style.setProperty('--plx', (-mid * plx[i].k).toFixed(1) + 'px');
    }
  }

  /* ──────────────────────── КУРСОР-ПРЕВЬЮ (§0.17) ───────────────── */
  var peek = null, peekX = 0, peekY = 0, peekTX = 0, peekTY = 0, peekRaf = 0;
  function initPeek() {
    var host = $('[data-peek-host]');
    if (!host) return;
    peek = document.createElement('div');
    peek.className = 'peek';
    peek.setAttribute('aria-hidden', 'true');
    peek.innerHTML = '<span class="peek__img"></span>';
    host.appendChild(peek);
    var imgNode = $('.peek__img', peek);

    $$('[data-img]', host).forEach(function (row) {
      function show() {
        var src = row.getAttribute('data-img');
        if (src) imgNode.style.backgroundImage = 'url("' + src + '")';
        peek.classList.add('is-on');
        row.classList.add('is-hot');
      }
      function hide() {
        peek.classList.remove('is-on');
        row.classList.remove('is-hot');
      }
      row.addEventListener('mouseenter', show);
      row.addEventListener('mouseleave', hide);
      row.addEventListener('focus', show);
      row.addEventListener('blur', hide);
    });

    host.addEventListener('mousemove', function (e) {
      var b = host.getBoundingClientRect();
      peekTX = e.clientX - b.left;
      peekTY = e.clientY - b.top;
      if (!peekRaf) peekRaf = requestAnimationFrame(peekTick);
    });
    host.addEventListener('mouseleave', function () { if (peek) peek.classList.remove('is-on'); });

    function peekTick() {
      var k = reduce ? 1 : 0.16;
      peekX += (peekTX - peekX) * k;
      peekY += (peekTY - peekY) * k;
      peek.style.transform = 'translate3d(' + peekX.toFixed(1) + 'px,' + peekY.toFixed(1) + 'px,0)';
      if (Math.abs(peekTX - peekX) > 0.4 || Math.abs(peekTY - peekY) > 0.4) {
        peekRaf = requestAnimationFrame(peekTick);
      } else { peekRaf = 0; }
    }
  }

  /* ──────────────────────── МАРКИЗА ──────────────────────── */
  var mqTrack = null;
  function prepMarquee() {
    mqTrack = $('.mq__track');
    if (!mqTrack) return;
    mqTrack.innerHTML += mqTrack.innerHTML;
  }

  /* ───────────────────────── ПРОКРУТКА ───────────────────────── */
  var bar = null, header = null, lastY = 0;
  function runScroll() {
    var y = window.pageYOffset || root.scrollTop;
    if (bar) {
      var max = root.scrollHeight - innerHeight;
      var horiz = bar.getAttribute('data-progress') === 'h';
      var t = max > 0 ? clamp(y / max, 0, 1) : 0;
      var target = bar.matches('i') ? bar : (bar.querySelector('i') || bar);
      target.style.transform = horiz ? 'scaleX(' + t.toFixed(4) + ')' : 'scaleY(' + t.toFixed(4) + ')';
    }
    if (header) header.classList.toggle('is-stuck', y > 40);

    if (mqTrack) {
      var v = clamp((y - lastY) / 24, -3, 3);
      mqTrack.style.setProperty('--mq-skew', (v * 0.2).toFixed(2) + 'deg');
    }
    lastY = y;

    runSeq();
    runPlx();
    runRail();
    runEcg();
  }
  function onScroll() {
    if (onScroll.q) return;
    onScroll.q = true;
    requestAnimationFrame(function () {
      onScroll.q = false;
      runScroll();
    });
  }

  /* ───────────────────────── СТАРТ ───────────────────────── */
  function bind() {
    $$('[data-theme-toggle]').forEach(function (b) {
      b.addEventListener('click', function (e) {
        setTheme(root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark', e);
      });
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
    $$('[data-menu-toggle]').forEach(function (b) {
      b.addEventListener('click', function () { setMenu(!menuOpen); });
    });
    var close = $('[data-menu-close]');
    if (close) close.addEventListener('click', function () { setMenu(false); });
    $$('[data-menu] a').forEach(function (a) {
      a.addEventListener('click', function () { setMenu(false); });
    });
    document.addEventListener('keydown', function (e) {
      var tag = (e.target.tagName || '').toLowerCase();
      var typing = tag === 'input' || tag === 'textarea' || e.target.isContentEditable;
      if (e.key === 'Escape' && menuOpen) { setMenu(false); return; }
      if (typing) return;
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'j') {
        e.preventDefault();
        setTheme(root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
      }
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        setMenu(!menuOpen);
      }
    });
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', function () {
      fine = fineQ.matches;
      collectSeqs(); collectPlx();
      onScroll();
    });
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

    bar = $('[data-progress]');
    header = $('[data-header]');

    bind();
    prepMarquee();
    splitHeadings();
    initMenuStage();
    initEcg();
    initRail();
    collectSeqs();
    collectPlx();
    initReveal();
    initCounts();
    initPeek();
    initScramble();
    initMagnets();
    initCursor();

    root.classList.add('js-ready');
    var heroEl = document.querySelector('.hero');
    if (heroEl) {
      var hasIntro = $('[data-intro]');
      var delay = (reduce || !hasIntro) ? 60 : 1700;
      if (reduce) { heroEl.classList.add('is-in'); }
      else {
        requestAnimationFrame(function () {
          setTimeout(function () { heroEl.classList.add('is-in'); }, delay);
        });
      }
    }
    requestAnimationFrame(function () { onScroll(); });
    setTimeout(onScroll, 240);
    setTimeout(onScroll, 900);
    window.addEventListener('load', onScroll);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else { boot(); }
})();