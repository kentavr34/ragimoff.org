/* test/11 — единая читалка библиотеки: read.html?b=<книга>&c=<глава>.
   Текст хранится отдельно: books/<книга>/book.json (паспорт и оглавление) и books/<книга>/<язык>/NN.html (главы) —
   собирает _tools/build_library.py. Новая книга или язык не требуют новых страниц.
   Как в прежней читалке: одна глава на экране, листание кнопками, клавишами ←/→ и свайпом, оглавление, размер шрифта,
   сноски во всплывающем окне, место чтения запоминается. Рама (шапка, темы, язык) — chrome.js, стили — site.css (раздел RDR). */
import { initChrome, esc } from './chrome.js?v=11121250';

const $ = s => document.querySelector(s), $$ = s => [...document.querySelectorAll(s)];
const V = '11121146', q = new URLSearchParams(location.search), bid = (q.get('b') || '').replace(/[^\w-]/g, '');
const U = {
  ru: { toc: 'Содержание', start: 'Начать чтение', cont: 'Продолжить чтение', prev: 'Назад', next: 'Дальше', title: 'Титульная страница', lib: 'Все книги', notes: 'Примечания', fs: 'Размер шрифта',
        only: 'Эта книга издана на языке:', other: 'Читать на другом языке:', none: 'Книга не найдена', ch: 'Глава', of: 'из', close: 'Закрыть', search: 'Поиск по книге', searchPh: 'Название или код, например 6B00', nores: 'Ничего не найдено', toggle: 'Открыть или закрыть группу', names: { az: 'азербайджанском', ru: 'русском', en: 'английском', tr: 'турецком' }, short: { az: 'Azərbaycanca', ru: 'По-русски', en: 'English', tr: 'Türkçe' } },
  az: { toc: 'Mündəricat', start: 'Oxumağa başlayın', cont: 'Oxumağa davam edin', prev: 'Geri', next: 'İrəli', title: 'Titul səhifəsi', lib: 'Bütün kitablar', notes: 'Qeydlər', fs: 'Şriftin ölçüsü',
        only: 'Bu kitab bu dildə nəşr olunub:', other: 'Başqa dildə oxuyun:', none: 'Kitab tapılmadı', ch: 'Fəsil', of: '/', close: 'Bağlayın', search: 'Kitabda axtarış', searchPh: 'Ad və ya kod, məsələn 6B00', nores: 'Heç nə tapılmadı', toggle: 'Qrupu açın və ya bağlayın', names: { az: 'Azərbaycan dili', ru: 'rus dili', en: 'ingilis dili', tr: 'türk dili' }, short: { az: 'Azərbaycanca', ru: 'По-русски', en: 'English', tr: 'Türkçe' } },
  en: { toc: 'Contents', start: 'Start reading', cont: 'Continue reading', prev: 'Back', next: 'Next', title: 'Title page', lib: 'All books', notes: 'Notes', fs: 'Font size',
        only: 'This book is published in:', other: 'Read in another language:', none: 'Book not found', ch: 'Chapter', of: 'of', close: 'Close', search: 'Search the book', searchPh: 'Title or code, e.g. 6B00', nores: 'Nothing found', toggle: 'Open or close the group', names: { az: 'Azerbaijani', ru: 'Russian', en: 'English', tr: 'Turkish' }, short: { az: 'Azərbaycanca', ru: 'По-русски', en: 'English', tr: 'Türkçe' } },
};
const store = { get: k => { try { return localStorage.getItem(k); } catch (e) { return null; } }, set: (k, v) => { try { localStorage.setItem(k, v); } catch (e) {} } };
let B = null, site = 'ru', lang = 'az', cur = 0, curId = '', turn = 0, clsSel = store.get('r11_rd_cls_' + bid) || 'icd', forced = store.get('r11_rd_lang_' + bid) || '';
let fs = Math.min(1.5, Math.max(.9, parseFloat(store.get('r11_rd_fs') || '1.1')));
const u = () => U[site] || U.ru, toc = () => (B && B.toc[lang]) || [], N = () => toc().length;
const idxById = id => { const k = toc().findIndex(x => x.id === id); return k < 0 ? 0 : k + 1; };
const cd = c => esc(c).replace(/–/g, '⁠–⁠');
const pad = n => String(n).padStart(2, '0');
const hrefOf = i => 'read.html?b=' + bid + (toc()[i - 1] && toc()[i - 1].id ? '&p=' + encodeURIComponent(toc()[i - 1].id) : '&c=' + i);
const trees = () => (B && B.trees && B.trees[lang]) || null;
const startIdx = () => { const p = q.get('p'); return p ? idxById(p) : (+(q.get('c') || 0) || 0); };
const posKey = () => 'r11_rd_pos_' + bid + '_' + lang;

async function passport() {
  if (B !== null) return B;
  try { const r = await fetch('books/' + bid + '/book.json?v=' + V); B = r.ok ? await r.json() : false; } catch (e) { B = false; }
  return B;
}
const cover = () => `<div class="rdr__cover" style="background-image:url('${esc(B.cover)}')"><span class="rdr__ca">${esc(B.kicker[lang] || '')}</span><span class="rdr__ct">${esc(B.t[lang])}</span></div>`;

const li = (x, i) => `${x.part ? `<li class="rdr__part">${esc(x.part)}</li>` : ''}<li><a href="${hrefOf(i + 1)}" data-go="${i + 1}"><span>${pad(i + 1)}</span><b>${esc(x.t)}</b></a></li>`;
function tocMarkup(search) {
  const T = trees(), t = u();
  if (!T) return null;
  if (!T[clsSel]) clsSel = T.order[0];
  const ids = {}; toc().forEach((x, i) => { if (x.id) ids[x.id] = i + 1; });
  const inTree = {}; (T.icd || T[T.order[0]]).forEach(g => { if (g.id) inTree[g.id] = 1; g.items.forEach(it => { inTree[it.id] = 1; }); });
  let a = -1, z = -1; toc().forEach((x, i) => { if (inTree[x.id]) { if (a < 0) a = i; z = i; } });
  const row = (x, i) => `<li><a href="${hrefOf(i + 1)}" data-go="${i + 1}"><span>—</span><b>${esc(x.t)}</b></a></li>`;
  const front = toc().map((x, i) => i < a ? row(x, i) : '').join(''), back = toc().map((x, i) => i > z ? row(x, i) : '').join('');
  const tabs = T.order.map(k => `<button type="button" class="rdr__ct" data-cls="${k}" aria-pressed="${k === clsSel}">${esc(T.names[k] || k)}</button>`).join('');
  const groups = T[clsSel].map(g => {
    const head = g.id && ids[g.id] ? `<a class="rdr__ga" href="${hrefOf(ids[g.id])}" data-go="${ids[g.id]}"><span>${cd(g.code)}</span><b>${esc(g.t)}</b></a>` : `<button type="button" class="rdr__ga" data-tg><span>${cd(g.code)}</span><b>${esc(g.t)}</b></button>`;
    return `<div class="rdr__g">${head}<button type="button" class="rdr__gt" data-tg aria-expanded="false" aria-label="${esc(t.toggle)}"></button><div class="rdr__gi" hidden>${g.items.filter(it => ids[it.id]).map(it => `<a href="${hrefOf(ids[it.id])}" data-go="${ids[it.id]}"><span>${cd(it.code)}</span><b>${esc(it.t)}</b></a>`).join('')}</div></div>`;
  }).join('');
  return `${search ? `<div class="rdr__q"><input type="search" id="rdQ" placeholder="${esc(t.searchPh)}" aria-label="${esc(t.search)}" autocomplete="off"><ol class="rdr__sr" id="rdSr"></ol></div>` : ''}<div class="rdr__fb"><ol>${front}</ol></div><div class="rdr__cts" role="group">${tabs}</div><div class="rdr__tree">${groups}</div><div class="rdr__fb"><ol>${back}</ol></div>`;
}
function markTree() {
  $$('#rdTocL a, .rdr__contents a').forEach(a => a.setAttribute('aria-current', String(+a.dataset.go === cur)));
  $$('.rdr__g').forEach(g => { if (g.querySelector('a[aria-current="true"]')) { g.classList.add('is-open'); g.querySelector('.rdr__gi').hidden = false; g.querySelector('.rdr__gt').setAttribute('aria-expanded', 'true'); } });
}
function renderTocs() {
  const pm = tocMarkup(true), tm = tocMarkup(false);
  if (pm) { $('#rdTocL').innerHTML = `<li class="rdr__tl">${pm}</li>`; $('.rdr__contents').lastElementChild.outerHTML = `<div class="rdr__tl">${tm}</div>`; markTree(); }
}
function bodyCls() {
  if (!$('#rdChap .rdr__body') || !trees()) return;
  $$('#rdChap .cls-tab').forEach(x => x.classList.toggle('is-active', x.dataset.cls === clsSel));
  $$('#rdChap .cls-panel').forEach(x => { x.hidden = x.dataset.cls !== clsSel; });
}
function setCls(k) { clsSel = k; store.set('r11_rd_cls_' + bid, k); renderTocs(); bodyCls(); }
function search(v) {
  const box = $('#rdSr'); if (!box) return;
  const w = v.toLowerCase().split(/\s+/).filter(Boolean);
  if (!w.length) { box.innerHTML = ''; return; }
  const hit = []; toc().forEach((x, i) => { const h = (x.t + ' ' + (x.code || '') + ' ' + (x.en || '')).toLowerCase(); if (w.every(k => h.indexOf(k) >= 0)) hit.push(i); });
  box.innerHTML = hit.length ? hit.slice(0, 20).map(i => `<li><a href="${hrefOf(i + 1)}" data-go="${i + 1}"><span>${toc()[i].code ? cd(toc()[i].code) : '—'}</span><b>${esc(toc()[i].t)}</b></a></li>`).join('') : `<li class="rdr__no">${esc(u().nores)}</li>`;
}
function frame() {
  const t = u(), saved = +(store.get(posKey()) || 0);
  document.documentElement.style.setProperty('--rd-fs', fs + 'rem');
  $('#rdTocT').textContent = t.toc; $('#rdTocX').setAttribute('aria-label', t.close);
  $('#rdTocL').innerHTML = `<li><a href="#" data-go="0"><span>—</span><b>${esc(t.title)}</b></a></li>` + toc().map(li).join('');
  $('#rdBar').innerHTML = `<a class="rdr__lib" href="shop.html">← ${esc(t.lib)}</a><b class="rdr__bt">${esc(B.t[lang])}</b><span class="rdr__tools"><button type="button" id="rdFsM" aria-label="${esc(t.fs)} −">A−</button><button type="button" id="rdFsP" aria-label="${esc(t.fs)} +">A+</button><button type="button" id="rdTocB">${esc(t.toc)}</button></span>`;
  const others = B.langs.filter(l => l !== lang);
  const note = (B.langs.indexOf(site) < 0 ? `<p class="rdr__note">${esc(t.only)} ${B.langs.map(l => esc(t.names[l] || l)).join(', ')}.</p>` : '') + (others.length ? `<p class="rdr__langs"><span>${esc(t.other)}</span>${others.map(l => `<button type="button" class="chip" data-rl="${l}">${esc(t.short[l] || l)}</button>`).join('')}</p>` : '');
  $('#rdTitle').innerHTML = `<div class="rdr__tp">${cover()}<div class="rdr__ti">${B.kicker[lang] ? `<p class="pp__kind">${esc(B.kicker[lang])}</p>` : ''}<h1 class="pp__t${B.t[lang].length > 40 ? ' pp__t--long' : ''}">${esc(B.t[lang])}</h1>${B.sub[lang] ? `<p class="pp__lead">${esc(B.sub[lang])}</p>` : ''}
    <dl class="rdr__meta">${(B.meta[lang] || []).map(m => `<div><dt>${esc(m[0])}</dt><dd>${esc(m[1])}</dd></div>`).join('')}</dl>${note}
    <p class="pp__cta"><button type="button" class="btn" data-go="${saved > 0 && saved <= N() ? saved : 1}">${esc(saved > 0 && saved <= N() ? t.cont : t.start)}</button></p></div></div>
    <nav class="rdr__contents" aria-label="${esc(t.toc)}"><h2 class="pp__h">${esc(t.toc)}</h2><ol>${toc().map(li).join('')}</ol></nav>`;
  renderTocs();
  document.title = B.t[lang] + ' — Doctor Ragimoff';
}

async function show(i, push, hash) {
  const my = ++turn, t = u();
  cur = Math.max(0, Math.min(N(), i | 0));
  document.body.classList.toggle('is-reading', cur > 0); document.body.classList.remove('rd-toc-open');
  $('#rdTitle').hidden = cur !== 0; $('#rdChap').hidden = cur === 0; $('#rdPager').hidden = cur === 0;
  curId = cur ? (toc()[cur - 1].id || '') : '';
  markTree();
  const url = (cur ? hrefOf(cur) : 'read.html?b=' + bid) + (hash || '');
  if (push) history.pushState({ c: cur }, '', url); else history.replaceState({ c: cur }, '', url);
  if (cur > 0) {
    store.set(posKey(), cur);
    const x = toc()[cur - 1];
    $('#rdChap').innerHTML = `<header class="rdr__ch"><p class="rdr__n">${x.code ? esc(x.code) : `${cur} ${esc(t.of)} ${N()}`}</p>${x.part ? `<p class="rdr__pt">${esc(x.part)}</p>` : ''}<h1 class="rdr__h">${esc(x.t)}</h1>${x.en ? `<p class="rdr__en" lang="en">${esc(x.en)}</p>` : ''}<span class="rdr__orn" aria-hidden="true"></span></header><div class="rdr__body" lang="${lang}"><p class="rdr__load">…</p></div>`;
    let html = '';
    try { const r = await fetch('books/' + bid + '/' + lang + '/' + String(cur).padStart(3, '0') + '.html?v=' + V); html = r.ok ? await r.text() : ''; } catch (e) { html = ''; }
    if (my !== turn) return;
    $('#rdChap .rdr__body').innerHTML = html || `<p class="rdr__note">${esc(t.none)}</p>`;
    $$('#rdChap .rdr__body table').forEach(tb => { if (!tb.parentElement.classList.contains('rdr__tw') && !(trees() && (tb.parentElement.classList.contains('tbl-wrap') || tb.classList.contains('bk-codes')))) { const w = document.createElement('div'); w.className = 'rdr__tw'; tb.replaceWith(w); w.appendChild(tb); } });
    const pv = $('#rdPrev'), nx = $('#rdNext');
    pv.querySelector('span').textContent = cur > 1 ? toc()[cur - 2].t : t.title; pv.querySelector('i').textContent = '← ' + t.prev;
    nx.hidden = cur >= N(); if (cur < N()) { nx.querySelector('span').textContent = toc()[cur].t; nx.querySelector('i').textContent = t.next + ' →'; }
  }
  bodyCls();
  scrollTo(0, 0); if (hash && cur) anchor(hash); progress();
}
function anchor(h) { let el = null; try { el = document.getElementById(decodeURIComponent(String(h).replace(/^#/, ''))); } catch (e) {} if (el) el.scrollIntoView(); return !!el; }
function progress() { const d = document.documentElement, h = d.scrollHeight - innerHeight, p = cur > 0 && h > 0 ? scrollY / h : 0; $('#rdProg').style.transform = 'scaleX(' + ((Math.max(0, cur - 1) + p) / Math.max(1, N())).toFixed(4) + ')'; }

const page = initChrome({
  async onRender(t, L, l) {
    site = l;
    const hc = $('#headCta'); if (hc) hc.href = L.form || 'index.html#reg';
    if (!bid || !(await passport())) { $('#rdTitle').innerHTML = `<div class="rdr__ti"><h1 class="pp__t">${esc(u().none)}</h1><p class="pp__cta"><a class="btn" href="shop.html">${esc(u().lib)}</a></p></div>`; $('#rdTitle').hidden = false; return; }
    document.querySelector('.rdr').dataset.book = bid;
    const want = forced && B.langs.indexOf(forced) >= 0 ? forced : (B.langs.indexOf(site) >= 0 ? site : B.langs[0]);
    const init = !$('#rdTocL').children.length, keep = curId; lang = want;
    frame();
    if (init) show(Math.min(startIdx(), N()), false, location.hash); else show(keep ? (idxById(keep) || cur) : cur, false);
  },
});
page.watch();

document.addEventListener('click', e => {
  const go = e.target.closest('[data-go]'); if (go) { e.preventDefault(); show(+go.dataset.go, true); return; }
  const rl = e.target.closest('[data-rl]'); if (rl) { const keep = curId; forced = rl.dataset.rl; store.set('r11_rd_lang_' + bid, forced); lang = forced; frame(); show(keep ? idxById(keep) : 0, false); return; }
  const tg = e.target.closest('[data-tg]'); if (tg) { const g = tg.closest('.rdr__g'), op = g.classList.toggle('is-open'); g.querySelector('.rdr__gi').hidden = !op; g.querySelector('.rdr__gt').setAttribute('aria-expanded', String(op)); return; }
  const ct = e.target.closest('.rdr__ct, #rdChap .cls-tab'); if (ct) { setCls(ct.dataset.cls); return; }
  const ia = e.target.closest('.rdr__body a[href]');
  if (ia && !ia.closest('.fn-ref')) {
    const h = ia.getAttribute('href');
    if (h.charAt(0) === '#') { e.preventDefault(); if (anchor(h)) history.replaceState(history.state, '', location.pathname + location.search + h); return; }
    try { const uu = new URL(h, location.href), p = uu.searchParams.get('p');
      if (/read\.html$/.test(uu.pathname) && uu.searchParams.get('b') === bid) { e.preventDefault(); const k = p ? idxById(p) : (+uu.searchParams.get('c') || 0); if (k === cur) { if (uu.hash) { anchor(uu.hash); history.replaceState(history.state, '', hrefOf(cur) + uu.hash); } else scrollTo(0, 0); } else if (k) show(k, true, uu.hash); return; } } catch (er) {}
  }
  if (e.target.closest('#rdTocB')) { document.body.classList.add('rd-toc-open'); const ac = $('#rdTocL a[aria-current="true"]'); if (ac && trees()) setTimeout(() => ac.scrollIntoView({ block: 'center' }), 60); return; }
  if (e.target.closest('#rdTocX') || e.target.closest('#rdScrim')) { document.body.classList.remove('rd-toc-open'); return; }
  if (e.target.closest('#rdPrev')) { show(cur - 1, true); return; }
  if (e.target.closest('#rdNext')) { show(cur + 1, true); return; }
  const fm = e.target.closest('#rdFsM'), fp = e.target.closest('#rdFsP');
  if (fm || fp) { fs = Math.min(1.5, Math.max(.9, +(fs + (fp ? .06 : -.06)).toFixed(2))); document.documentElement.style.setProperty('--rd-fs', fs + 'rem'); store.set('r11_rd_fs', fs); return; }
  /* сноска: текст примечания показывается во всплывающем окне, а не прыжком в конец главы */
  const ref = e.target.closest('.fn-ref a'); const pop = $('#rdPop');
  if (ref) { e.preventDefault(); const n = document.getElementById((ref.getAttribute('href') || '').slice(1)); if (n) { const c = n.cloneNode(true); c.querySelectorAll('.fn-back').forEach(x => x.remove()); pop.innerHTML = `<b>${esc(u().notes)} · ${esc(ref.textContent)}</b><p>${c.innerHTML}</p>`; pop.hidden = false; } return; }
  if (e.target.closest('.fn-back')) { e.preventDefault(); return; }
  if (!e.target.closest('#rdPop')) pop.hidden = true;
});
addEventListener('popstate', () => { const sp = new URLSearchParams(location.search), p = sp.get('p'); show(p ? idxById(p) : (+(sp.get('c') || 0) || 0), false, location.hash); });
document.addEventListener('input', e => { if (e.target.id === 'rdQ') search(e.target.value); });
addEventListener('scroll', progress, { passive: true });
document.addEventListener('keydown', e => {
  if (e.target.closest && e.target.closest('input,textarea,select')) return;
  if (e.key === 'Escape') { document.body.classList.remove('rd-toc-open'); $('#rdPop').hidden = true; }
  if (!B || e.altKey || e.ctrlKey || e.metaKey) return;
  if (e.key === 'ArrowRight' && cur < N()) show(cur + 1, true);
  if (e.key === 'ArrowLeft' && cur > 0) show(cur - 1, true);
});
/* свайп по тексту: влево — следующая глава, вправо — предыдущая */
let sx = 0, sy = 0, st = 0;
document.addEventListener('touchstart', e => { const p = e.changedTouches[0]; sx = p.clientX; sy = p.clientY; st = Date.now(); }, { passive: true });
document.addEventListener('touchend', e => { if (!B || cur === 0 || e.target.closest('.rdr__tw, #rdToc')) return; const p = e.changedTouches[0], dx = p.clientX - sx, dy = p.clientY - sy;
  if (Date.now() - st < 600 && Math.abs(dx) > 90 && Math.abs(dy) < 50) { if (dx < 0 && cur < N()) show(cur + 1, true); if (dx > 0) show(cur - 1, true); } }, { passive: true });
