/* test/11 — главная: отрисовка из content.js, герой на кадрах, лента программ, книги в объёме, мифы, меню. */
import { T, LINKS } from './content.js?v=11112004';
import { regRender, regOpen } from './reg.js?v=11112004';
import { initLight } from './light.js?v=11112004';

const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const store = { get: k => { try { return localStorage.getItem(k); } catch (e) { return null; } }, set: (k, v) => { try { localStorage.setItem(k, v); } catch (e) {} } };
const pick = (o, path) => path.split('.').reduce((a, k) => (a == null ? a : a[k]), o);
const clamp = v => (v < 0 ? 0 : v > 1 ? 1 : v), seg = (v, a, b) => clamp((v - a) / (b - a));
const CHEV = '<svg viewBox="0 0 10 10" aria-hidden="true"><path d="M2 3.5l3 3 3-3" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>';
const ARR = '<span class="arrow">→</span>';

let GAL = [], galI = 0;
let lang = T[document.documentElement.lang] ? document.documentElement.lang : 'ru';
const light = initLight($('#light'));

/* ───────── отрисовка ───────── */
function render() {
  const t = T[lang], L = LINKS(lang);
  document.documentElement.lang = lang;
  $$('[data-i]').forEach(e => { const v = pick(t, e.dataset.i); if (v != null) e.textContent = v; });
  $$('[data-h]').forEach(h => { const s = t[h.dataset.h]; const row = h.dataset.h === 'blog'; h.innerHTML = `${row ? '<div class="sh__g">' : ''}<h2 class="sh__h rv" style="--d:.08s">${esc(s.h)}</h2>${s.sub ? `<p class="sh__s rv" style="--d:.16s">${esc(s.sub)}</p>` : ''}${row ? `</div><a class="sh__link rv" href="${L.blogAll}">${esc(s.all)} ${ARR}</a>` : ''}`; });

  /* меню: заголовки, под ними — подзаголовки (на телефоне по стрелке) */
  const groups = [
    { k: 'spec', href: '#spec', sub: t.spec.p.map((p, i) => [L.spec[i], p.n]) },
    { k: 'books', href: '#books', sub: t.books.b.map((b, i) => [L.books[i], b.t]) },
    { k: 'edu', href: '#edu', sub: t.edu.p.map((p, i) => [L.prog[i], p.t]).concat([[L.law, t.nav.law]]) },
    { k: 'cons', href: '#cons', sub: t.cons.t.map((x, i) => [L.cons[i], x[0]]) },
    { k: 'corp', href: '#corp', sub: t.corp.t.map(x => [L.corp, x]) }, { k: 'blog', href: '#blog', sub: [] }, { k: 'contact', href: L.contact, sub: [] },
  ];
  $('#nav').innerHTML = groups.map(g => `<div class="nav__i"><a class="nav__l" href="${g.href}">${esc(t.nav[g.k])}${g.sub.length ? CHEV : ''}</a>${g.sub.length ? `<div class="nav__dd">${g.sub.map(s => `<a href="${s[0]}">${esc(s[1])}</a>`).join('')}</div>` : ''}</div>`).join('');
  $('#mobIn').innerHTML = groups.map(g => `<div class="mob__g"><div class="mob__row"><a class="mob__big" href="${g.href}">${esc(t.nav[g.k])}</a>${g.sub.length ? `<button class="mob__tog" type="button" aria-label="+">${CHEV.replace('<svg', '<svg width="14" height="14"')}</button>` : ''}</div>${g.sub.length ? `<div class="mob__sub">${g.sub.map(s => `<a href="${s[0]}">${esc(s[1])}</a>`).join('')}</div>` : ''}</div>`).join('');
  $('#headCta').textContent = t.nav.cta;
  $('#mobIn').insertAdjacentHTML('afterbegin', `<a class="btn mob__cta" href="#reg" data-reg="consult">${esc(t.nav.cta)}</a>`);   /* на телефоне «Записаться» — в меню */

  $('#school').innerHTML = [...t.hero.school].map((ch, i) => ch === ' ' ? ' ' : `<span style="--i:${i}">${esc(ch)}</span>`).join('');   /* строгая строка встаёт по буквам */
  $('#heroBtns').innerHTML = ['#cons', '#edu', '#books', '#corp'].map((h, i) => `<a href="${h}" style="--i:${i}">${esc(t.hero.b[i])}</a>`).join('');
  const beltHtml = t.belt.map(x => `<span>${esc(x)}</span>`).join(''); $('#belt').innerHTML = beltHtml + beltHtml;

  $('#people').innerHTML = t.spec.p.map((p, i) => `<a class="person rv" href="${L.spec[i]}" style="--d:${i * .12}s"><div class="person__ph"><img src="assets/img/${i ? 'samira' : 'kenan'}.jpg" alt="${esc(p.n)}" loading="lazy"></div>
    <div class="person__b"><span class="person__r">${esc(p.r)}</span><h3 class="person__n">${esc(p.n)}</h3><ul class="facts">${p.f.map(f => `<li>${esc(f)}</li>`).join('')}</ul><span class="person__more">${esc(t.spec.more)} ${ARR}</span></div></a>`).join('');

  const cov = ['klinik', 'freud', 'phoenix', 'guilt', 'pandemic'];
  const bkAll = t.books.b.map((b, i) => ({ b, href: L.books[i], img: `assets/img/book-${cov[i]}-${lang}.jpg` })).concat(t.books.soon ? [{ b: t.books.soon, href: L.shop, img: '' }] : []);
  $('#shelf').innerHTML = bkAll.map(({ b, href, img }) => `<article class="bk"><div class="bk__scene"><a class="bk__obj${img ? '' : ' bk__obj--txt'}" href="${href}" aria-label="${esc(b.t)}">${img ? `<img src="${img}" alt="${esc(b.t)}" loading="lazy">` : `<span class="bk__ct"><i>${esc(b.a)}</i><b>${esc(b.t)}</b><u>Doctor Ragimoff</u></span>`}</a></div>
    <div class="bk__txt">${b.k ? `<p class="bk__k">${esc(b.k)}</p>` : ''}<h3 class="bk__t">${esc(b.t)}</h3><p class="bk__a">${esc(b.a)}</p>
    <ul class="bk__f">${b.f.map((f, j) => `<li><b>0${j + 1}</b><span>${esc(f)}</span></li>`).join('')}</ul>
    <div class="bk__btns"><a class="btn" href="${href}">${esc(t.books.read)}</a></div></div></article>`).join('');
  bkMeasure(); bkScroll();

  $('#progs').innerHTML = t.edu.p.map((p, i) => `<article class="pc"><span class="pc__n">0${i + 1} / 07</span><h3 class="pc__t">${esc(p.t)}</h3><p class="pc__d">${esc(p.d)}</p><div class="pc__m">${p.m.map(m => `<span>${esc(m)}</span>`).join('')}</div><p class="pc__p">${esc(p.price)}</p><a class="btn btn--line btn--sm" href="${L.prog[i]}">${esc(t.edu.more)} ${ARR}</a></article>`).join('');

  $('#topics').innerHTML = t.cons.t.map((x, i) => `<li class="topic rv" style="--d:${i * .05}s"><a href="${L.cons[i]}"><span class="topic__n">0${i + 1}</span><span class="topic__t">${esc(x[0])}</span><span class="topic__s">${esc(x[1])}</span><span class="topic__a arrow">→</span></a></li>`).join('')
    + `<li class="topic topic--other rv"><a href="${L.wa}" target="_blank" rel="noopener"><span class="topic__n">+</span><span class="topic__t">${esc(t.cons.other[0])}</span><span class="topic__s">${esc(t.cons.other[1])}</span><span class="topic__a arrow">→</span></a></li>`;   /* клиент может обратиться с любой темой */
  const cb = $('#consBtn'); cb.textContent = t.cons.cta; cb.href = '#reg'; cb.dataset.reg = 'consult'; cb.removeAttribute('target'); $('#fab').href = L.wa;
  const wb = $('#consWa'); wb.textContent = t.cons.wa; wb.href = L.wa;

  $('#corpTags').innerHTML = t.corp.t.map(x => `<li>${esc(x)}</li>`).join('');
  $('#corpClients').innerHTML = (t.corp.clients || []).map(x => `<li>${esc(x)}</li>`).join('');
  const fc = t.foot.cols || [], fl = L.foot || [];
  $('#footCols').innerHTML = fc.map((c, i) => `<div class="foot__col"><h3>${esc(c.h)}</h3><ul>${c.l.map((x, j) => { const u = (fl[i] || [])[j]; return `<li>${u ? `<a href="${u}"${/^https?:/.test(u) ? ' target="_blank" rel="noopener"' : ''}>${esc(x)}</a>` : esc(x)}</li>`; }).join('')}</ul></div>`).join('');
  $('#footCopy').innerHTML = (t.foot.copy || []).map(x => `<span>${esc(x)}</span>`).join('');
  const kb = $('#corpBtn'); kb.innerHTML = esc(t.corp.cta) + ' ' + ARR; kb.href = '#reg'; kb.dataset.reg = 'b2b';

  $('#myths').innerHTML = t.enl.m.map((m, i) => `<a class="mth rv" href="${L.myths[i] || L.books[0]}" style="--d:${i * .06}s"><span class="mth__k">${esc(t.enl.myth)} · ${esc(m[0])}</span><span class="mth__q">${esc(m[1])}</span><span class="mth__go">${esc(t.enl.go)} ${ARR}</span></a>`).join('');

  $('#posts').innerHTML = t.blog.p.map((p, i) => `<a class="post rv" href="${L.blog[i]}" style="--d:${i * .1}s"><div class="post__i"><img src="assets/img/blog-${i + 1}.jpg" alt="" loading="lazy"></div><div class="post__b"><span class="post__k">${esc(p[0])}</span><h3 class="post__t">${esc(p[1])}</h3></div></a>`).join('');
  $('#tgBtn').href = L.tg;
  const vid = (id, title) => `<button type="button" class="vid" data-yt="${id}" aria-label="${esc(title)}"><img src="https://i.ytimg.com/vi/${id}/hqdefault.jpg" alt="" loading="lazy" width="480" height="360"><span class="vid__play" aria-hidden="true"></span></button>`;
  GAL = (t.edu.gal || []).map(g => ({ src: 'assets/img/proof/' + g[0] + '.jpg', cap: g[1] }));
  $('#proofs').innerHTML = GAL.slice(0, 3).map((g, i) => `<button type="button" class="proof rv" data-gal="${i}" style="--d:${i * .08}s"><span class="proof__i"><img src="${g.src}" alt="${esc(g.cap)}" loading="lazy" width="1500" height="1070"></span><span class="proof__c">${esc(g.cap)}</span></button>`).join('');
  $('#galBtn').textContent = t.edu.galBtn + ' · ' + GAL.length;
  const ld = t.spec.lead; $('#lead').innerHTML = ld ? `<h3 class="lead__h">${esc(ld.h)}</h3><div class="lead__g">${ld.items.map(x => `<div class="qual"><b>${esc(x[0])}</b><span>${esc(x[1])}</span></div>`).join('')}</div>` : '';
  if (t.a11y && t.a11y.prev) { $('#bkPrev').setAttribute('aria-label', t.a11y.prev); $('#bkNext').setAttribute('aria-label', t.a11y.next); $('#lbPrev').setAttribute('aria-label', t.a11y.prev); $('#lbNext').setAttribute('aria-label', t.a11y.next); $('#lbX').setAttribute('aria-label', t.a11y.close); }
  const fm = t.cons.film; $('#film').innerHTML = fm ? `${vid(fm.id, fm.t)}<div class="film__b"><h3 class="film__t">${esc(fm.t)}</h3><p class="film__d">${esc(fm.d)}</p>${fm.cta ? `<button type="button" class="btn btn--line film__go">${esc(fm.cta)}</button>` : ''}</div>` : '';
  const ax = t.a11y; if (ax) { document.title = ax.title; $('#nav').setAttribute('aria-label', ax.menu); $('#burger').setAttribute('aria-label', ax.menu); $('#themes').setAttribute('aria-label', ax.theme); $('#langs').setAttribute('aria-label', ax.lang); $$('[data-theme-btn]').forEach(b => b.setAttribute('aria-label', ax[b.dataset.themeBtn])); }
  $('#corpVids').innerHTML = (t.corp.vids || []).map(v => `<figure class="vids__i rv">${vid(v[1], v[0])}<figcaption>${esc(v[0])}</figcaption></figure>`).join('');
  regRender(t, lang);
  const ea = $('#enlAll'); ea.innerHTML = esc(t.enl.more) + ' ' + ARR; ea.href = L.books[0];

  $$('[data-lang-btn]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.langBtn === lang)));
  $$('[data-theme-btn]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.themeBtn === document.documentElement.dataset.theme)));
  cineQ = t.hero.q; observe(); ribMeasure(); onScroll();
}

/* ───────── появление блоков ───────── */
let io = null;
function observe() {
  if (!io) io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('is-in'); if (e.target.querySelector && e.target.matches('.num')) count(e.target.querySelector('b')); io.unobserve(e.target); } }), { rootMargin: '0px 0px -8% 0px', threshold: .06 });
  $$('.rv:not(.is-in)').forEach(e => io.observe(e));
}
function count(b) {                       /* цифры набегают */
  const raw = b.dataset.count, m = raw.match(/^(\d+)(\D*)$/); if (!m) return;
  const end = +m[1], suf = m[2], t0 = performance.now(), dur = 1500;
  (function tick(now) { const k = clamp((now - t0) / dur), v = Math.round(end * (1 - Math.pow(1 - k, 3))); b.textContent = v + suf; if (k < 1) requestAnimationFrame(tick); })(t0);
}

/* ───────── 1. герой: кадры видео по прокрутке ───────── */
const cine = $('#hero'), frame = $('#cineFrame'), cv = $('#cineCv'), ctx = cv.getContext('2d');
const N = +cine.dataset.frames, M = cine.dataset.marks.split(',').map(Number);
let cineQ = '', imgs = [], set = '', shownF = 0, targetF = 0, cineRaf = 0;
const mqM = matchMedia('(max-width: 760px)');
function cineLoad() {
  const want = mqM.matches ? 'm' : 'd'; if (want === set) return; set = want; imgs = [];
  $('#cineImg').src = `assets/hero/${want}/f000.webp`;
  const order = []; for (let i = 0; i < N; i += 6) order.push(i); for (let i = 0; i < N; i++) if (i % 6) order.push(i);
  order.forEach((i, n) => { const im = new Image(); im.decoding = 'async'; im.onload = () => { if (Math.abs(i - shownF) < 2) cinePaint(); };
    setTimeout(() => { im.src = `assets/hero/${want}/f${String(i).padStart(3, '0')}.webp`; }, n < 20 ? 0 : 40 + n * 8); imgs[i] = im; });
  cineSize();
}
function cineSize() { const d = Math.min(devicePixelRatio || 1, 1.5); cv.width = Math.round(frame.offsetWidth * d); cv.height = Math.round(frame.offsetHeight * d); cinePaint(); }
const ok = im => im && im.complete && im.naturalWidth;
function near(i) { for (let d = 0; d < N; d++) { if (ok(imgs[i - d])) return imgs[i - d]; if (ok(imgs[i + d])) return imgs[i + d]; } return null; }
function cinePaint() {
  const f = Math.max(0, Math.min(N - 1, shownF)), a = Math.floor(f), b = Math.min(N - 1, a + 1), k = f - a, A = near(a); if (!A) return;
  ctx.globalAlpha = 1; ctx.drawImage(A, 0, 0, cv.width, cv.height);
  if (k > .02 && ok(imgs[b])) { ctx.globalAlpha = k; ctx.drawImage(imgs[b], 0, 0, cv.width, cv.height); ctx.globalAlpha = 1; }   /* соседние кадры смешиваются — движение как у видео */
}
function cineLoop() {
  cineRaf = 0; shownF += (targetF - shownF) * .16; if (Math.abs(targetF - shownF) < .02) shownF = targetF;
  cinePaint();
  const sq = seg(shownF, M[0], M[1]) * (1 - seg(shownF, M[4] - 1, M[4] + 1.5));
  cine.style.setProperty('--sq', sq.toFixed(3));
  $('#cineQ').textContent = cineQ.slice(0, Math.round(seg(shownF, M[2], M[3]) * cineQ.length));
  const title = shownF >= M[4]; cine.classList.toggle('is-title', title);
  const sh = +cine.style.getPropertyValue('--sh') || 0, shT = title ? 1 : 0; cine.style.setProperty('--sh', (sh + (shT - sh) * .08).toFixed(3));
  if (shownF !== targetF || Math.abs(shT - sh) > .01) cineRaf = requestAnimationFrame(cineLoop);
}
function cineScroll() {
  const r = cine.getBoundingClientRect(), total = cine.offsetHeight - innerHeight, p = total > 0 ? clamp(-r.top / total) : 0;
  targetF = clamp(p / .74) * (N - 1);
  cine.style.setProperty('--p', p.toFixed(3)); cine.style.setProperty('--out', seg(p, .9, 1).toFixed(3));   /* затемнение — только в самом конце и плавно */
  if (!cineRaf) cineRaf = requestAnimationFrame(cineLoop);
}

/* ───────── 4. закреплённая лента программ ───────── */
const rib = $('[data-rib]'), ribStick = $('.rib__stick', rib), track = $('[data-rib-track]', rib);
let ribDist = 0, ribCur = 0, ribTarget = 0, ribRaf = 0;
function stickTop(el) { el.style.top = Math.max(innerWidth < 761 ? 60 : 0, Math.round((innerHeight - el.offsetHeight) / 2)) + 'px'; }
function ribMeasure() {
  track.style.setProperty('--x', '0px'); stickTop(ribStick);
  ribDist = Math.max(0, track.scrollWidth - ribStick.clientWidth);
  rib.style.height = (ribStick.offsetHeight + ribDist * (innerWidth < 761 ? 1.05 : .9)) + 'px';   /* высота = панель + путь ленты: после неё нет пустого экрана */
}
function ribLoop() {
  ribRaf = 0; ribCur += (ribTarget - ribCur) * .15; if (Math.abs(ribTarget - ribCur) < .3) ribCur = ribTarget;
  track.style.setProperty('--x', (-ribCur).toFixed(1) + 'px');
  const mid = innerWidth / 2;
  $$('.pc', track).forEach(c => { const b = c.getBoundingClientRect(), d = Math.abs(b.left + b.width / 2 - mid) / innerWidth; c.style.setProperty('--s', (1 - Math.min(.06, d * .1)).toFixed(3)); c.style.setProperty('--o', (1 - Math.min(.45, d * .6)).toFixed(3)); });
  $('#ribBar').style.setProperty('--pr', ribDist ? (ribCur / ribDist).toFixed(3) : 0);
  if (ribCur !== ribTarget) ribRaf = requestAnimationFrame(ribLoop);
}
function ribScroll() {
  const r = rib.getBoundingClientRect(), total = rib.offsetHeight - ribStick.offsetHeight, p = total > 0 ? clamp((parseFloat(ribStick.style.top) - r.top) / total) : 0;
  ribTarget = p * ribDist; if (!ribRaf) ribRaf = requestAnimationFrame(ribLoop);
}

/* ───────── прокрутка: шапка, книги, портреты ───────── */
const head = $('#head'), fab = $('#fab'); let lastY = 0, travel = 0;
function onScroll() {
  const y = scrollY, vh = innerHeight, dy = y - lastY; if ((dy > 0) !== (travel > 0)) travel = 0; travel += dy; lastY = y;
  const overHero = cine.getBoundingClientRect().bottom > 70;
  head.classList.toggle('on-dark', overHero); head.classList.toggle('is-solid', !overHero);
  const menuOpen = $('#mob').classList.contains('is-open'); head.classList.toggle('is-menu', menuOpen);
  if (y < 120 || menuOpen) head.classList.remove('is-hidden'); else if (travel > 48) head.classList.add('is-hidden'); else if (travel < -32) head.classList.remove('is-hidden');
  fab.classList.toggle('is-on', !overHero);
  const rr = rib.getBoundingClientRect(); fab.classList.toggle('is-off', (rr.top <= 1 && rr.bottom >= vh - 1) || (innerWidth < 761 && head.classList.contains('is-hidden')));   /* на телефоне при чтении вниз кнопка уходит вместе с шапкой и не закрывает текст */   /* в закреплённой ленте кнопка не закрывает карточки */
  cineScroll(); ribScroll();
  $$('.bk__obj').forEach(o => { const r = o.getBoundingClientRect(); if (r.bottom < -100 || r.top > vh + 100) return; const k = clamp(1 - (r.top + r.height / 2) / vh); o.style.setProperty('--ry', (-38 + seg(k, .1, .6) * 22).toFixed(1) + 'deg'); });   /* книга поворачивается к читателю */
  $$('.person__ph img').forEach(im => { const r = im.parentNode.getBoundingClientRect(); if (r.bottom < 0 || r.top > vh) return; im.style.setProperty('--py', (-(r.top + r.height / 2 - vh / 2) / vh * 7).toFixed(2) + '%'); });
}
addEventListener('scroll', onScroll, { passive: true }); addEventListener('scroll', bkScroll, { passive: true });
let rt = 0; addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(() => { cineLoad(); cineSize(); ribMeasure(); bkMeasure(); bkScroll(); onScroll(); }, 120); });

/* ───────── нажатия ───────── */
function setMenu(open) { $('#mob').classList.toggle('is-open', open); $('#mob').setAttribute('aria-hidden', String(!open)); $('#burger').setAttribute('aria-expanded', String(open)); document.documentElement.style.overflow = open ? 'hidden' : ''; if (open) head.classList.remove('is-hidden'); head.classList.toggle('is-menu', open); }
/* книги: лента по одной, стрелки и свайп */
function galShow(i) { if (!GAL.length) return; galI = (i + GAL.length) % GAL.length; $('#lbImg').src = GAL[galI].src; $('#lbCap').textContent = GAL[galI].cap; $('#lbN').textContent = (galI + 1) + ' / ' + GAL.length; $('#lb').classList.add('is-open'); $('#lb').setAttribute('aria-hidden', 'false'); }
function galClose() { $('#lb').classList.remove('is-open'); $('#lb').setAttribute('aria-hidden', 'true'); }
addEventListener('keydown', e => { if (!$('#lb').classList.contains('is-open')) return; if (e.key === 'Escape') galClose(); if (e.key === 'ArrowRight') galShow(galI + 1); if (e.key === 'ArrowLeft') galShow(galI - 1); });
let lbX0 = null; $('#lb').addEventListener('touchstart', e => { lbX0 = e.touches[0].clientX; }, { passive: true }); $('#lb').addEventListener('touchend', e => { if (lbX0 == null) return; const d = e.changedTouches[0].clientX - lbX0; lbX0 = null; if (Math.abs(d) > 40) galShow(galI + (d < 0 ? 1 : -1)); }, { passive: true });
const shelf = $('#shelf'), bkSec = $('[data-bk]'), bkStick = $('.bk__stick');
let bkI = 0, bkStep = 1;
function bkMeasure() { const n = shelf.children.length; stickTop(bkStick); bkStep = Math.round(innerHeight * (innerWidth < 761 ? .75 : .6)); bkSec.style.height = (bkStick.offsetHeight + Math.max(0, n - 1) * bkStep) + 'px'; }
function bkScroll() {                                   /* прокрутка листает книги по одной: большую часть шага книга стоит, переход — в середине */
  const n = shelf.children.length; if (!n) return;
  const r = bkSec.getBoundingClientRect(), total = bkSec.offsetHeight - bkStick.offsetHeight, p = total > 0 ? clamp((parseFloat(bkStick.style.top) - r.top) / total) : 0;
  const x = p * (n - 1), k = Math.floor(x), f = x - k, e = f < .3 ? 0 : f > .7 ? 1 : (f - .3) / .4, pos = Math.min(n - 1, k + e * e * (3 - 2 * e));
  shelf.style.setProperty('--bx', (-pos * 100).toFixed(2) + '%');
  const i = Math.round(pos); if (i !== bkI || !$('#bkPos').textContent) { bkI = i; $('#bkPos').textContent = String(i + 1).padStart(2, '0') + ' / ' + String(n).padStart(2, '0'); $('#bkPrev').disabled = i <= 0; $('#bkNext').disabled = i >= n - 1; }
}
function bkGo(d) { const n = shelf.children.length, i = Math.max(0, Math.min(n - 1, bkI + d)); scrollTo({ top: bkSec.getBoundingClientRect().top + scrollY - parseFloat(bkStick.style.top) + i * bkStep + 2, behavior: 'smooth' }); }
let bkX0 = null; shelf.addEventListener('touchstart', e => { bkX0 = [e.touches[0].clientX, e.touches[0].clientY]; }, { passive: true });
shelf.addEventListener('touchend', e => { if (!bkX0) return; const dx = e.changedTouches[0].clientX - bkX0[0], dy = e.changedTouches[0].clientY - bkX0[1]; bkX0 = null; if (Math.abs(dx) > 44 && Math.abs(dx) > Math.abs(dy) * 1.4) bkGo(dx < 0 ? 1 : -1); }, { passive: true });
document.addEventListener('click', e => {
  const tog = e.target.closest('.mob__tog'); if (tog) { tog.closest('.mob__g').classList.toggle('is-open'); return; }
  if (e.target.closest('#burger')) { setMenu(!$('#mob').classList.contains('is-open')); return; }
  if (e.target.closest('#mob a')) setMenu(false);
  const mf = e.target.closest('.myth__f'); if (mf) { mf.closest('.myth').classList.add('is-flip'); return; }
  const mb = e.target.closest('.myth__b'); if (mb && !e.target.closest('a')) { mb.closest('.myth').classList.remove('is-flip'); return; }
  const go = e.target.closest('.film__go'); const yt = go ? $('#film .vid[data-yt]') : e.target.closest('.vid[data-yt]'); if (go && !yt) return; if (yt) { yt.outerHTML = `<div class="vid vid--on"><iframe src="https://www.youtube-nocookie.com/embed/${yt.dataset.yt}?autoplay=1&rel=0" title="${yt.getAttribute('aria-label')}" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen></iframe></div>`; return; }
  const pf = e.target.closest('[data-gal]'); if (pf) { galShow(+pf.dataset.gal); return; }
  if (e.target.closest('#galBtn')) { galShow(0); return; }
  if (e.target.closest('#lbNext')) { galShow(galI + 1); return; } if (e.target.closest('#lbPrev')) { galShow(galI - 1); return; }
  if (e.target.closest('#lb')) { if (!e.target.closest('figure') || e.target.closest('#lbX')) galClose(); return; }
  if (e.target.closest('#bkPrev')) { bkGo(-1); return; } if (e.target.closest('#bkNext')) { bkGo(1); return; }
  let th = e.target.closest('[data-theme-btn]');
  if (th && innerWidth < 761 && th.getAttribute('aria-pressed') === 'true') { const all = $$('[data-theme-btn]'); th = all[(all.indexOf(th) + 1) % all.length]; }   /* на телефоне одна кнопка: нажатие — следующая тема */
  if (th) { document.documentElement.dataset.theme = th.dataset.themeBtn; store.set('r11_theme', th.dataset.themeBtn); if (light) light.setTheme(); render(); return; }
  const lg = e.target.closest('[data-lang-btn]'); if (lg) { lang = lg.dataset.langBtn; store.set('r11_lang', lang); render(); return; }
  const rg = e.target.closest('[data-reg]'); if (rg) regOpen(rg.dataset.reg);
  const a = e.target.closest('a[href^="#"]'); if (a && a.getAttribute('href').length > 1) { const el = $(a.getAttribute('href')); if (el) { e.preventDefault(); scrollTo({ top: el.getBoundingClientRect().top + scrollY - (el.matches('.sec--rib') ? 0 : 10), behavior: 'smooth' }); } }
});
document.addEventListener('keydown', e => { if (e.key === 'Escape') setMenu(false); });

/* ───────── запуск ───────── */
render(); cineLoad();
(document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve()).then(() => { ribMeasure(); onScroll(); });
addEventListener('load', () => { cineSize(); ribMeasure(); onScroll(); });
