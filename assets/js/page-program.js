/* test/11 — страница программы обучения: один шаблон на все программы. Данные — programs.js, подписи — content.js (T[l].pp), форма — reg.js. */
import { PROGRAMS } from './programs.js?v=11140607';
import { initChrome, esc, ARR, progUrl } from './chrome.js?v=11140607';
import { rich, fixImg } from './blocks.js?v=11140607';
import { regRender, regOpen } from './reg.js?v=11140607';

const $ = s => document.querySelector(s);
const slug = (() => { const p = new URLSearchParams((location.search || window.__Q || '')).get('p'); return PROGRAMS.items[p] ? p : PROGRAMS.order[0]; })();
const P = PROGRAMS.items[slug];
const LAW_ON = slug === 'general' || slug === 'clinical';          /* блок «Юридические основы деятельности» — только у программ с дипломом института */
const V = '11120255', lawCache = {};
const ext = u => (/^https?:/.test(u) ? ' target="_blank" rel="noopener"' : '');
async function lawRender(lang) {
  if (!(lang in lawCache)) { try { const r = await fetch('data/law/law.' + lang + '.json?v=' + V); lawCache[lang] = r.ok ? await r.json() : null; } catch (e) { lawCache[lang] = null; } }
  const d = lawCache[lang]; if (!d || document.documentElement.lang !== lang) return;
  $('#hLaw').textContent = d.h; $('#sLaw').textContent = d.sub; $('#hLawDocs').textContent = d.docs;
  $('#ppLawDocs').innerHTML = d.gallery.filter(x => !x.only || x.only.indexOf(slug) >= 0).map(x => `<button type="button" class="gal__i rv" data-zoom="${esc(fixImg(x.src))}" data-cap="${esc(x.cap || '')}"><img src="${esc(fixImg(x.thumb || x.src))}" alt="${esc(x.cap || '')}" loading="lazy" width="400" height="300"><span>${esc(x.cap || '')}</span></button>`).join('');
  $('#ppLaw').innerHTML = d.items.map((x, i) => `<details class="acc acc--law rv"${i === 0 ? ' open' : ''}><summary><span>${esc(x.q)}</span><i aria-hidden="true"></i></summary><div class="law__a"><p>${esc(x.a)}</p>${x.law ? `<p class="law__n">${esc(x.law)}</p>` : ''}${(x.quotes || []).map(q => `${q[0] ? `<p class="law__c">${esc(q[0])}</p>` : ''}${q[2] ? `<blockquote class="law__q">${rich(q[1])}</blockquote>` : `<p>${rich(q[1])}</p>`}`).join('')}${[].concat(x.link ? [x.link] : [], x.links || []).map(a => `<a class="law__l" href="${esc(a[1])}"${ext(a[1])}>${esc(a[0])} ↗</a>`).join('')}</div></details>`).join('');
  sec('law', true); setTimeout(() => page && page.watch(), 0);
  if (location.hash === '#law' && !lawRender.done) { lawRender.done = true; setTimeout(() => $('#law').scrollIntoView(), 60); }   /* переход по ссылке «Юридические основы» */
}
const sec = (id, on) => { const el = $('#' + id); if (el) el.hidden = !on; };

const page = initChrome({
  onRender(t, L, lang) {
    const d = P[lang], u = t.pp;
    document.title = d.title + ' — Doctor Ragimoff';
    $('#ppBack').innerHTML = '← ' + esc(u.back); $('#ppBack').href = 'index.html#edu';
    $('#ppKind').textContent = P.kind === 'long' ? u.long : u.short;
    $('#ppT').textContent = d.title; $('#ppLead').textContent = d.lead;
    $('#ppFacts').innerHTML = d.facts.filter(f => f[1]).map(f => `<div class="fact"><dt>${esc(f[0])}</dt><dd>${esc(f[1])}</dd></div>`).join('');
    $('#ppGo').textContent = u.reg; $('#ppGo2').textContent = u.reg;
    [['hFor', u.forWhom], ['hTeach', u.teachers], ['hInc', u.includes], ['hProg', u.program], ['hDoc', u.doc], ['hFaq', u.faq], ['hPrice', u.price]].forEach(([id, v]) => { $('#' + id).textContent = v; });
    $('#ppFor').innerHTML = d.forWhom.map(x => `<li>${esc(x)}</li>`).join(''); sec('for', d.forWhom.length);
    $('#ppTeach').innerHTML = d.teachers.map(x => { const sam = /Самир|Samir/.test(x[0]); return `<a class="tch rv" href="${L.spec[sam ? 1 : 0]}"><span class="tch__ph"><img src="assets/img/specialists/${sam ? 'samira' : 'kenan'}.jpg" alt="${esc(x[0])}" loading="lazy" width="96" height="96"></span><span class="tch__b"><b>${esc(x[0])}</b><span>${esc(x[1])}</span></span></a>`; }).join(''); sec('teach', d.teachers.length);
    $('#ppInc').innerHTML = d.includes.map(x => `<li>${esc(x)}</li>`).join(''); sec('inc', d.includes.length);
    $('#ppProg').innerHTML = d.program.map((m, i) => `<details class="acc rv"${i === 0 ? ' open' : ''}><summary><span>${esc(m.t)}</span><i aria-hidden="true"></i></summary><ul>${m.items.map(x => `<li>${esc(x)}</li>`).join('')}</ul></details>`).join(''); sec('prog', d.program.length);
    $('#ppDoc').innerHTML = `<div class="doc__b"><h3 class="doc__t">${esc(d.doc.t)}</h3><p class="doc__d">${esc(d.doc.d)}</p></div><button type="button" class="doc__i" id="docBtn" aria-label="${esc(u.sample)}"><img src="assets/img/programs/proof/${P.sample}.jpg" alt="${esc(d.doc.t)}" loading="lazy" width="1500" height="1070"><span>${esc(u.sample)}</span></button>`; sec('doc', !!d.doc.t);
    $('#ppFaq').innerHTML = d.faq.map(q => `<details class="acc rv"><summary><span>${esc(q[0])}</span><i aria-hidden="true"></i></summary><p>${esc(q[1])}</p></details>`).join(''); sec('faq', d.faq.length);
    $('#ppPrice').innerHTML = d.price.rows.map(r => `<div class="prow"><span>${esc(r[0])}</span><b>${esc(r[1])}</b></div>`).join('') + (d.price.note ? `<p class="pnote">${esc(d.price.note)}</p>` : ''); sec('price', d.price.rows.length);
    const h = t.reg; $('#regH').textContent = h.h; $('#regS').textContent = h.sub;
    $('#ppOther').innerHTML = `<span>${esc(u.other)}</span>` + PROGRAMS.order.filter(s => s !== slug).map(s => `<a href="${progUrl(s)}">${esc(PROGRAMS.items[s][lang].title)}</a>`).join('');
    sec('law', false); if (LAW_ON) lawRender(lang);
    regRender(t, lang); regOpen('edu', null, P.reg);
    setTimeout(() => page && page.watch(), 0);
  },
});
page.watch();
document.addEventListener('click', e => {
  if (e.target.closest('#docBtn')) { const lb = $('#lb'); $('#lbImg').src = $('#docBtn img').src; $('#lbCap').textContent = $('#docBtn img').alt; lb.classList.add('is-open'); lb.setAttribute('aria-hidden', 'false'); return; }
  const z = e.target.closest('.gal__i'); if (z) { const lb = $('#lb'); lb.classList.add('lb--doc');     /* документ открывается во всю ширину и листается */ $('#lbImg').src = z.dataset.zoom; $('#lbCap').textContent = z.dataset.cap; lb.classList.add('is-open'); lb.setAttribute('aria-hidden', 'false'); return; }
  if (e.target.closest('#lb')) { $('#lb').classList.remove('is-open'); $('#lb').setAttribute('aria-hidden', 'true'); }
});

addEventListener('keydown', e => { if (e.key === 'Escape' && $('#lb').classList.contains('is-open')) { $('#lb').classList.remove('is-open'); $('#lb').setAttribute('aria-hidden', 'true'); } });
