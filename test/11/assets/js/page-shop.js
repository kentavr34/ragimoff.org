/* test/11 — прототип книжного магазина (shop.html) и страницы книги (book.html?b=<id>).
   Каталог — data/shop/index.<lang>.json (собирает _tools/build_shop.py из действующего магазина /books/, который не меняется).
   Чтение и заказ ведут в действующий магазин: корзина и оплата остаются там. Рама — chrome.js, стили — site.css (раздел SHP). */
import { initChrome, esc, ARR } from './chrome.js?v=11121036';

const $ = s => document.querySelector(s), $$ = s => [...document.querySelectorAll(s)];
const V = '11120953', kind = document.body.dataset.kind, cache = {};
const bid = new URLSearchParams(location.search).get('b') || '';
const OWN = ['klinik', 'guilt', 'pandemic', 'phoenix'];                 /* у этих книг готовая обложка с названием на трёх языках */
let turn = 0, filter = 'all';

async function load(lang) {
  if (!(lang in cache)) { try { const r = await fetch('data/shop/index.' + lang + '.json?v=' + V); cache[lang] = r.ok ? await r.json() : null; } catch (e) { cache[lang] = null; } }
  return cache[lang];
}
/* обложка: готовая картинка или фактура с набранными автором и названием (буква Ə не превращается в квадрат) */
const cover = (it, lang, big) => OWN.includes(it.id)
  ? `<img src="assets/img/book-${it.id}-${lang}.jpg" alt="${esc(it.t)}" loading="lazy" width="600" height="900">`
  : `<span class="shp__tex" style="background-image:url('${esc(it.img)}')"></span><span class="shp__ct"><i>${esc(it.a)}</i><b${it.t.length > 34 ? ' class="is-long"' : ''}>${esc(it.t)}</b><u>${esc(it.y)}</u></span>`;
const book3d = (it, lang, href) => `<a class="shp__obj${OWN.includes(it.id) ? '' : ' shp__obj--tex'}" href="${href}" aria-label="${esc(it.t)}">${cover(it, lang)}</a>`;
const url = it => 'book.html?b=' + encodeURIComponent(it.id);
const price = (it, u) => it.price ? `<p class="shp__price"><span>${esc(u.price)}</span><b>${esc(it.price)}</b></p>` : '';
const btns = (it, d) => `<div class="shp__btns">${it.read ? `<a class="btn" href="${esc(it.href)}">${esc(d.u.read)}</a>` : `<span class="shp__soon">${esc(d.u.soon)}</span>`}${it.price ? `<a class="btn btn--line" href="${esc(d.orderUrl)}">${esc(d.u.order)}</a>` : ''}</div>`;

function shop(d, lang) {
  const all = d.groups.flatMap(g => g.items);
  $('#shpHero').innerHTML = `<p class="pp__kind">Doctor Ragimoff</p><h1 class="pp__t">${esc(d.title)}</h1><p class="pp__lead">${esc(d.lead)}</p>
    <div class="shp__chips" role="group">${[['all', d.u.all, all.length]].concat(d.groups.map(g => [g.id, g.name, g.items.length])).map(c => `<button type="button" class="chip" data-f="${c[0]}" aria-pressed="${String(filter === c[0])}">${esc(c[1])} <i>${c[2]}</i></button>`).join('')}</div>`;
  $('#shpBody').innerHTML = d.groups.filter(g => filter === 'all' || filter === g.id).map(g => {
    const lead = g.items.filter(it => it.f), rest = g.items.filter(it => !it.f);
    return `<section class="sec shp__grp" data-g="${g.id}"><div class="wrap"><header class="shp__gh rv"><h2 class="shp__gt">${esc(g.name)}</h2><span class="shp__gn">${g.items.length}</span></header>
      ${lead.map((it, i) => `<article class="shp__row rv${i % 2 ? ' shp__row--rev' : ''}"><div class="shp__scene">${book3d(it, lang, url(it))}</div><div class="shp__txt">${it.k ? `<p class="shp__k">${esc(it.k)}</p>` : ''}<h3 class="shp__t"><a href="${url(it)}">${esc(it.t)}</a></h3><p class="shp__m">${esc(it.meta)}</p>
        <ul class="shp__f">${it.f.map((f, j) => `<li><b>0${j + 1}</b><span>${esc(f)}</span></li>`).join('')}</ul>${price(it, d.u)}${btns(it, d)}</div></article>`).join('')}
      ${rest.length ? `<div class="shp__grid">${rest.map(it => `<a class="shp__card rv" href="${url(it)}"><span class="shp__cv">${cover(it, lang)}</span><span class="shp__cb"><b>${esc(it.t)}</b><span>${esc(it.meta)}</span>${it.price ? `<em>${esc(it.price)}</em>` : ''}</span></a>`).join('')}</div>` : ''}
    </div></section>`;
  }).join('');
  document.title = d.title + ' — Doctor Ragimoff';
}

function book(d, lang) {
  const all = d.groups.flatMap(g => g.items.map(it => Object.assign({ g }, it)));
  const it = all.find(x => x.id === bid) || all[0];
  const sib = all.filter(x => x.g.id === it.g.id && x.id !== it.id).slice(0, 8), other = sib.length >= 3 ? sib : all.filter(x => x.id !== it.id && x.f).concat(sib).slice(0, 8);
  $('#shpHero').innerHTML = `<div class="shp__bk"><div class="shp__scene shp__scene--big">${book3d(it, lang, it.read ? esc(it.href) : '#')}</div>
    <div class="shp__txt"><a class="pp__back" href="shop.html">← ${esc(d.title)}</a>${it.k ? `<p class="pp__kind">${esc(it.k)}</p>` : `<p class="pp__kind">${esc(it.y)}</p>`}<h1 class="pp__t${it.t.length > 40 ? ' pp__t--long' : ''}">${esc(it.t)}</h1>
      <p class="shp__au">${esc(it.g.name)}</p><p class="shp__m">${esc(it.meta)}</p>${it.f ? `<ul class="shp__f">${it.f.map((f, j) => `<li><b>0${j + 1}</b><span>${esc(f)}</span></li>`).join('')}</ul>` : ''}${price(it, d.u)}${btns(it, d)}</div></div>`;
  $('#shpBody').innerHTML = `<section class="sec"><div class="wrap"><header class="shp__gh rv"><h2 class="shp__gt">${esc(d.u.other)}</h2><a class="sh__link" href="shop.html">${esc(d.title)} ${ARR}</a></header>
    <div class="shp__grid">${other.map(x => `<a class="shp__card rv" href="${url(x)}"><span class="shp__cv">${cover(x, lang)}</span><span class="shp__cb"><b>${esc(x.t)}</b><span>${esc(x.meta)}</span>${x.price ? `<em>${esc(x.price)}</em>` : ''}</span></a>`).join('')}</div></div></section>`;
  document.title = it.t + ' — Doctor Ragimoff';
}

const page = initChrome({
  async onRender(t, L, lang) {
    const my = ++turn, d = await load(lang) || await load('az');
    if (my !== turn || !d) return;
    (kind === 'book' ? book : shop)(d, lang);
    const hc = $('#headCta'); if (hc) { hc.href = L.form || 'index.html#reg'; }
    setTimeout(() => page && page.watch(), 0);
  },
});
page.watch();
document.addEventListener('click', e => {
  const c = e.target.closest('.shp__chips .chip'); if (!c) return;
  filter = c.dataset.f; const lang = document.documentElement.lang; if (cache[lang]) { shop(cache[lang], lang); setTimeout(() => page.watch(), 0); }
});
/* книга слегка поворачивается за указателем (только там, где есть мышь) */
if (matchMedia('(hover: hover) and (pointer: fine)').matches && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
  document.addEventListener('pointermove', e => { const s = e.target.closest && e.target.closest('.shp__scene'); if (!s) return; const r = s.getBoundingClientRect(), o = s.querySelector('.shp__obj'); if (o) o.style.setProperty('--ry', (-26 + ((e.clientX - r.left) / r.width - .5) * 30).toFixed(1) + 'deg'); });
  document.addEventListener('pointerout', e => { const s = e.target.closest && e.target.closest('.shp__scene'); if (s && !s.contains(e.relatedTarget)) { const o = s.querySelector('.shp__obj'); if (o) o.style.removeProperty('--ry'); } });
}
