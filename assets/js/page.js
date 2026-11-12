/* test/11 — внутренняя страница из блоков: один сценарий на специалистов, консультации, контакты, тренинги, право, блог и статью.
   Вид страницы — <body data-kind="spec|cons|page|blog|post" data-slug="…">; данные — data/<папка>/<slug>.<lang>.json; рама — chrome.js; форма — reg.js. */
import { initChrome, esc } from './chrome.js?v=11122110';
import { renderBlocks, fixImg, fixUrl, rich } from './blocks.js?v=11122110';
import { regRender, regOpen } from './reg.js?v=11122110';
import { CONS, CONS_TOPIC } from './content.js?v=11122110';

const V = '11122110';
const $ = s => document.querySelector(s), $$ = s => [...document.querySelectorAll(s)];
const kind = document.body.dataset.kind || 'page';
const q = new URLSearchParams(location.search);
const DIR = { spec: 'spec', cons: 'cons', page: 'page', blog: 'blog', post: 'blog' };
const DEF = { spec: 'kenan', cons: CONS[0], page: 'contact', blog: 'index', post: 'depressiya' };
const slug = kind === 'blog' ? 'index' : ((document.body.dataset.slug || q.get('s') || q.get('c') || q.get('a') || DEF[kind]).replace(/[^\w-]/g, '') || DEF[kind]);
const cache = {};
async function load(dir, name, lang) {                       /* нет страницы на этом языке — берём азербайджанскую, затем русскую */
  for (const l of [lang, 'az', 'ru']) {
    const k = dir + '/' + name + '.' + l; if (cache[k] !== undefined) { if (cache[k]) return cache[k]; continue; }
    try { const r = await fetch('data/' + k + '.json?v=' + V); cache[k] = r.ok ? await r.json() : null; } catch (e) { cache[k] = null; }
    if (cache[k]) return cache[k];
  }
  return null;
}
let cat = 'all', turn = 0;

function hero(d, u, back, backHref, cta) {
  const im = d.img ? fixImg(d.img) : '';
  $('#pgHero').className = 'wrap pg__hero' + (im ? ' pg__hero--art' : '') + (kind === 'spec' ? ' pg__hero--face' : '');
  $('#pgHero').innerHTML = `<div class="pg__ht"><a class="pp__back" href="${backHref}">← ${esc(back)}</a>${d.eye ? `<p class="pp__kind">${esc(d.eye)}</p>` : ''}<h1 class="pp__t${String(d.title || '').length > 64 ? ' pp__t--long' : ''}">${rich(d.title)}</h1>${d.lead ? `<p class="pp__lead">${rich(d.lead)}</p>` : ''}${cta ? `<p class="pp__cta"><a class="btn" href="#reg">${esc(cta)}</a></p>` : ''}</div>${im ? `<figure class="pg__art"><img src="${esc(im)}" alt="${esc(d.title)}" width="1200" height="900"${d.imgPos ? ` style="object-position:${esc(d.imgPos)}"` : ''}></figure>` : ''}`;
}

function blogPage(d, u) {
  const f = d.featured, its = d.items.filter(x => (cat === 'all' ? !(f && x.slug === f.slug) : x.cat === cat)), fi = f && d.items.find(x => x.slug === f.slug);
  const chips = `<div class="chips pg__cats" role="group">${d.cats.filter(c => c[0] === 'all' || d.items.some(x => x.cat === c[0])).map(c => `<button type="button" class="chip${c[0] === cat ? ' is-on' : ''}" data-cat="${esc(c[0])}" aria-pressed="${c[0] === cat}">${esc(c[1])}</button>`).join('')}</div>`;
  const feat = f && cat === 'all' ? `<a class="feat rv" href="article.html?a=${esc(f.slug)}">${fi && fi.cover ? `<span class="feat__ph"><img src="${esc(fixImg(fi.cover))}" alt="" width="1600" height="900"></span>` : ''}<span class="feat__b"><span class="pst__m">${esc(f.badge)}</span><b class="feat__t">${esc(f.title)}</b><span class="pst__m">${esc(f.meta)}</span><span class="feat__d">${esc(f.excerpt)}</span><span class="btn">${esc(f.cta)}</span></span></a>` : '';
  const grid = `<div class="psts psts--grid">${its.map(a => `<a class="pst rv" href="article.html?a=${esc(a.slug)}">${a.cover ? `<span class="pst__ph"><img src="${esc(fixImg(a.cover))}" alt="" loading="lazy" width="1600" height="900"></span>` : ''}<span class="pst__b"><span class="pst__m">${esc(a.meta || a.catLabel)}</span><b class="pst__t">${esc(a.title)}</b><span class="pst__d">${esc(a.excerpt)}</span></span></a>`).join('')}</div>`;
  return `<section class="sec sec--blog"><div class="wrap">${chips}${feat}${grid}</div></section>`;
}

const page = initChrome({
  async onRender(t, L, lang) {
    const my = ++turn, u = t.pg;
    const h = t.reg; $('#regH').textContent = h.h; $('#regS').textContent = h.sub; regRender(t, lang);
    let d = await load(DIR[kind], slug, lang); if (my !== turn) return;
    /* общая страница раздела «Консультации» (consult.html?c=index): список всех консультаций из data/cons/index.<язык>.json */
    if (d && !d.title && Array.isArray(d.items)) d = { title: t.nav.cons, blocks: [{ type: 'links', items: d.items.map(x => [x.title, 'consult.html?c=' + x.slug]) }] };
    if (!d) { document.title = u.none + ' — Doctor Ragimoff'; $('#pgHero').innerHTML = `<div class="pg__ht"><h1 class="pp__t">${esc(u.none)}</h1><p class="pp__cta"><a class="btn" href="index.html">${esc(u.home)}</a></p></div>`; $('#pgBlocks').innerHTML = ''; return; }
    document.title = d.title.replace(/<[^>]+>/g, '') + ' — Doctor Ragimoff';
    const needBlog = kind === 'post' || (d.blocks || []).some(b => b.type === 'articles');
    const ix = needBlog ? await load('blog', 'index', lang) : null; if (my !== turn) return;
    const blog = {}; if (ix) ix.items.forEach(a => { blog[a.slug] = a; });
    const backHref = { spec: 'index.html#spec', cons: 'index.html#cons', page: 'index.html', blog: 'index.html#blog', post: 'blog.html' }[kind];
    const cta = kind === 'spec' || kind === 'cons' || slug === 'corporate' ? t.nav.cta : '';
    hero(d, u, u.back[kind], backHref, cta);
    let blocks = (d.blocks || []).slice();
    while (blocks.length && blocks[blocks.length - 1].type === 'cta') blocks.pop();                    /* призыв прямо перед формой записи лишний: форма ниже */
    let seenArt = false; blocks = blocks.filter(b => { if (b.type !== 'articles') return true; if (seenArt) return false; seenArt = true; return true; });   /* второй список статей подряд не нужен */
    if (kind === 'post') { blocks = blocks.map(b => (b.type === 'sources' ? Object.assign({}, b, { h: u.sources, sub: b.t }) : b)); if (d.author) { const i = blocks.findIndex(b => b.type === 'articles'); blocks.splice(i < 0 ? blocks.length : i, 0, { type: 'note', h: u.author, t: d.author[0], d: d.author[1] }); } }
    $('#pgBlocks').innerHTML = kind === 'blog' ? blogPage(d, u) : renderBlocks(blocks, u, { t, blog });
    /* нижняя навигация: соседние страницы раздела */
    let other = '';
    if (kind === 'spec') other = `<span>${esc(u.other.spec)}</span>` + t.spec.p.map((p, i) => [i ? 'samira' : 'kenan', p.n]).filter(x => x[0] !== slug).map(x => `<a href="specialist.html?s=${x[0]}">${esc(x[1])}</a>`).join('');
    if (kind === 'cons') { const ci = await load('cons', 'index', lang); if (my !== turn) return; other = `<span>${esc(u.other.cons)}</span>` + (ci ? ci.items : []).filter(x => x.slug !== slug).map(x => `<a href="consult.html?c=${esc(x.slug)}">${esc(x.title)}</a>`).join(''); }
    if (kind === 'page' || kind === 'blog' || kind === 'post') other = `<span>${esc(u.other.page)}</span>` + [['contact.html', u.pages.contact, 'contact'], ['corporate.html', u.pages.corporate, 'corporate'], [L.law, u.pages.law, 'law'], ['blog.html', t.nav.blog, 'index'], [L.tests, u.pages.tests, '']].filter(x => !(x[2] === slug && kind !== 'post')).map(x => `<a href="${x[0]}">${esc(x[1])}</a>`).join('');
    $('#ppOther').innerHTML = other;
    /* форма уже настроена на эту страницу */
    const TOPIC = [['panik', 0], ['depressiya', 1], ['sosial-fobiya', 2], ['enurez', 3], ['aile', 4], ['yeniyetme', 4]];
    if (kind === 'spec') regOpen('consult', slug === 'samira' ? 4 : null, null, slug);
    else if (kind === 'post') { const m = TOPIC.find(x => slug.indexOf(x[0]) === 0); if (m) regOpen('consult', m[1], null, m[1] === 4 ? 'samira' : 'kenan'); }
    else if (kind === 'cons') { const i = CONS_TOPIC[slug]; regOpen('consult', i != null ? i : t.cons.t.length, null, /^(aile|valideyn)/.test(slug) ? 'samira' : null); }
    else if (slug === 'corporate') regOpen('b2b');
    $$('#pgBlocks table').forEach(tb => { const hd = [...tb.querySelectorAll('thead th')].map(x => x.textContent.trim()); tb.classList.toggle('tbl--nohead', !hd.length); tb.querySelectorAll('tbody tr').forEach(tr => [...tr.children].forEach((td, i) => { if (hd[i]) td.dataset.l = hd[i]; })); });
    setTimeout(() => page && page.watch(), 0);
  },
});

/* просмотр снимков: дипломы, сертификаты, снимки экрана */
let gal = [], gi = 0;
function show(i) { if (!gal.length) return; gi = (i + gal.length) % gal.length; $('#lbImg').src = gal[gi].src; $('#lbCap').textContent = gal[gi].cap; $('#lb').classList.add('is-open'); $('#lb').setAttribute('aria-hidden', 'false'); }
function hide() { $('#lb').classList.remove('is-open'); $('#lb').setAttribute('aria-hidden', 'true'); }
document.addEventListener('click', e => {
  const c = e.target.closest('[data-cat]'); if (c) { cat = c.dataset.cat; page.render(); return; }
  const z = e.target.closest('[data-zoom]'); if (z) { const all = $$('[data-zoom]'); gal = all.map(x => ({ src: x.dataset.zoom, cap: x.dataset.cap })); show(all.indexOf(z)); return; }
  if (e.target.closest('#lbNext')) { show(gi + 1); return; } if (e.target.closest('#lbPrev')) { show(gi - 1); return; }
  if (e.target.closest('#lb') && (!e.target.closest('figure') || e.target.closest('.lb__x'))) hide();
});
addEventListener('keydown', e => { if (!$('#lb').classList.contains('is-open')) return; if (e.key === 'Escape') hide(); if (e.key === 'ArrowRight') show(gi + 1); if (e.key === 'ArrowLeft') show(gi - 1); });
let x0 = null; $('#lb').addEventListener('touchstart', e => { x0 = e.touches[0].clientX; }, { passive: true });
$('#lb').addEventListener('touchend', e => { if (x0 == null) return; const dx = e.changedTouches[0].clientX - x0; x0 = null; if (Math.abs(dx) > 40) show(gi + (dx < 0 ? 1 : -1)); });
