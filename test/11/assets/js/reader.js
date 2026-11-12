/* test/11 — единая читалка библиотеки: read.html?b=<книга>&c=<глава>.
   Текст хранится отдельно: books/<книга>/book.json (паспорт и оглавление) и books/<книга>/<язык>/NN.html (главы) —
   собирает _tools/build_library.py. Новая книга или язык не требуют новых страниц.
   Как в прежней читалке: одна глава на экране, листание кнопками, клавишами ←/→ и свайпом, оглавление, размер шрифта,
   сноски во всплывающем окне, место чтения запоминается. Рама (шапка, темы, язык) — chrome.js, стили — site.css (раздел RDR). */
import { initChrome, esc } from './chrome.js?v=11121155';

const $ = s => document.querySelector(s), $$ = s => [...document.querySelectorAll(s)];
const V = '11121146', q = new URLSearchParams(location.search), bid = (q.get('b') || '').replace(/[^\w-]/g, '');
const U = {
  ru: { toc: 'Содержание', start: 'Начать чтение', cont: 'Продолжить чтение', prev: 'Назад', next: 'Дальше', title: 'Титульная страница', lib: 'Все книги', notes: 'Примечания', fs: 'Размер шрифта',
        only: 'Эта книга издана на языке:', other: 'Читать на другом языке:', none: 'Книга не найдена', ch: 'Глава', of: 'из', close: 'Закрыть', names: { az: 'азербайджанском', ru: 'русском', en: 'английском', tr: 'турецком' }, short: { az: 'Azərbaycanca', ru: 'По-русски', en: 'English', tr: 'Türkçe' } },
  az: { toc: 'Mündəricat', start: 'Oxumağa başlayın', cont: 'Oxumağa davam edin', prev: 'Geri', next: 'İrəli', title: 'Titul səhifəsi', lib: 'Bütün kitablar', notes: 'Qeydlər', fs: 'Şriftin ölçüsü',
        only: 'Bu kitab bu dildə nəşr olunub:', other: 'Başqa dildə oxuyun:', none: 'Kitab tapılmadı', ch: 'Fəsil', of: '/', close: 'Bağlayın', names: { az: 'Azərbaycan dili', ru: 'rus dili', en: 'ingilis dili', tr: 'türk dili' }, short: { az: 'Azərbaycanca', ru: 'По-русски', en: 'English', tr: 'Türkçe' } },
  en: { toc: 'Contents', start: 'Start reading', cont: 'Continue reading', prev: 'Back', next: 'Next', title: 'Title page', lib: 'All books', notes: 'Notes', fs: 'Font size',
        only: 'This book is published in:', other: 'Read in another language:', none: 'Book not found', ch: 'Chapter', of: 'of', close: 'Close', names: { az: 'Azerbaijani', ru: 'Russian', en: 'English', tr: 'Turkish' }, short: { az: 'Azərbaycanca', ru: 'По-русски', en: 'English', tr: 'Türkçe' } },
};
const store = { get: k => { try { return localStorage.getItem(k); } catch (e) { return null; } }, set: (k, v) => { try { localStorage.setItem(k, v); } catch (e) {} } };
let B = null, site = 'ru', lang = 'az', cur = 0, turn = 0, forced = store.get('r11_rd_lang_' + bid) || '';
let fs = Math.min(1.5, Math.max(.9, parseFloat(store.get('r11_rd_fs') || '1.1')));
const u = () => U[site] || U.ru, toc = () => (B && B.toc[lang]) || [], N = () => toc().length;
const posKey = () => 'r11_rd_pos_' + bid + '_' + lang;

async function passport() {
  if (B !== null) return B;
  try { const r = await fetch('books/' + bid + '/book.json?v=' + V); B = r.ok ? await r.json() : false; } catch (e) { B = false; }
  return B;
}
const cover = () => `<div class="rdr__cover" style="background-image:url('${esc(B.cover)}')"><span class="rdr__ca">${esc(B.kicker[lang] || '')}</span><span class="rdr__ct">${esc(B.t[lang])}</span></div>`;

function frame() {
  const t = u(), saved = +(store.get(posKey()) || 0);
  document.documentElement.style.setProperty('--rd-fs', fs + 'rem');
  $('#rdTocT').textContent = t.toc; $('#rdTocX').setAttribute('aria-label', t.close);
  $('#rdTocL').innerHTML = `<li><a href="#" data-go="0"><span>—</span><b>${esc(t.title)}</b></a></li>` + toc().map((x, i) => `${x.part ? `<li class="rdr__part">${esc(x.part)}</li>` : ''}<li><a href="#" data-go="${i + 1}"><span>${String(i + 1).padStart(2, '0')}</span><b>${esc(x.t)}</b></a></li>`).join('');
  $('#rdBar').innerHTML = `<a class="rdr__lib" href="shop.html">← ${esc(t.lib)}</a><b class="rdr__bt">${esc(B.t[lang])}</b><span class="rdr__tools"><button type="button" id="rdFsM" aria-label="${esc(t.fs)} −">A−</button><button type="button" id="rdFsP" aria-label="${esc(t.fs)} +">A+</button><button type="button" id="rdTocB">${esc(t.toc)}</button></span>`;
  const others = B.langs.filter(l => l !== lang);
  const note = (B.langs.indexOf(site) < 0 ? `<p class="rdr__note">${esc(t.only)} ${B.langs.map(l => esc(t.names[l] || l)).join(', ')}.</p>` : '') + (others.length ? `<p class="rdr__langs"><span>${esc(t.other)}</span>${others.map(l => `<button type="button" class="chip" data-rl="${l}">${esc(t.short[l] || l)}</button>`).join('')}</p>` : '');
  $('#rdTitle').innerHTML = `<div class="rdr__tp">${cover()}<div class="rdr__ti">${B.kicker[lang] ? `<p class="pp__kind">${esc(B.kicker[lang])}</p>` : ''}<h1 class="pp__t${B.t[lang].length > 40 ? ' pp__t--long' : ''}">${esc(B.t[lang])}</h1>${B.sub[lang] ? `<p class="pp__lead">${esc(B.sub[lang])}</p>` : ''}
    <dl class="rdr__meta">${(B.meta[lang] || []).map(m => `<div><dt>${esc(m[0])}</dt><dd>${esc(m[1])}</dd></div>`).join('')}</dl>${note}
    <p class="pp__cta"><button type="button" class="btn" data-go="${saved > 0 && saved <= N() ? saved : 1}">${esc(saved > 0 && saved <= N() ? t.cont : t.start)}</button></p></div></div>
    <nav class="rdr__contents" aria-label="${esc(t.toc)}"><h2 class="pp__h">${esc(t.toc)}</h2><ol>${toc().map((x, i) => `${x.part ? `<li class="rdr__part">${esc(x.part)}</li>` : ''}<li><a href="#" data-go="${i + 1}"><span>${String(i + 1).padStart(2, '0')}</span><b>${esc(x.t)}</b></a></li>`).join('')}</ol></nav>`;
  document.title = B.t[lang] + ' — Doctor Ragimoff';
}

async function show(i, push) {
  const my = ++turn, t = u();
  cur = Math.max(0, Math.min(N(), i | 0));
  document.body.classList.toggle('is-reading', cur > 0); document.body.classList.remove('rd-toc-open');
  $('#rdTitle').hidden = cur !== 0; $('#rdChap').hidden = cur === 0; $('#rdPager').hidden = cur === 0;
  $$('#rdTocL a').forEach(a => a.setAttribute('aria-current', String(+a.dataset.go === cur)));
  const url = 'read.html?b=' + bid + (cur ? '&c=' + cur : '');
  if (push) history.pushState({ c: cur }, '', url); else history.replaceState({ c: cur }, '', url);
  if (cur > 0) {
    store.set(posKey(), cur);
    const x = toc()[cur - 1];
    $('#rdChap').innerHTML = `<header class="rdr__ch"><p class="rdr__n">${cur} ${esc(t.of)} ${N()}</p>${x.part ? `<p class="rdr__pt">${esc(x.part)}</p>` : ''}<h1 class="rdr__h">${esc(x.t)}</h1><span class="rdr__orn" aria-hidden="true"></span></header><div class="rdr__body" lang="${lang}"><p class="rdr__load">…</p></div>`;
    let html = '';
    try { const r = await fetch('books/' + bid + '/' + lang + '/' + String(cur).padStart(3, '0') + '.html?v=' + V); html = r.ok ? await r.text() : ''; } catch (e) { html = ''; }
    if (my !== turn) return;
    $('#rdChap .rdr__body').innerHTML = html || `<p class="rdr__note">${esc(t.none)}</p>`;
    $$('#rdChap .rdr__body table').forEach(tb => { if (!tb.parentElement.classList.contains('rdr__tw')) { const w = document.createElement('div'); w.className = 'rdr__tw'; tb.replaceWith(w); w.appendChild(tb); } });
    const pv = $('#rdPrev'), nx = $('#rdNext');
    pv.querySelector('span').textContent = cur > 1 ? toc()[cur - 2].t : t.title; pv.querySelector('i').textContent = '← ' + t.prev;
    nx.hidden = cur >= N(); if (cur < N()) { nx.querySelector('span').textContent = toc()[cur].t; nx.querySelector('i').textContent = t.next + ' →'; }
  }
  scrollTo(0, 0); progress();
}
function progress() { const d = document.documentElement, h = d.scrollHeight - innerHeight, p = cur > 0 && h > 0 ? scrollY / h : 0; $('#rdProg').style.transform = 'scaleX(' + ((Math.max(0, cur - 1) + p) / Math.max(1, N())).toFixed(4) + ')'; }

const page = initChrome({
  async onRender(t, L, l) {
    site = l;
    const hc = $('#headCta'); if (hc) hc.href = L.form || 'index.html#reg';
    if (!bid || !(await passport())) { $('#rdTitle').innerHTML = `<div class="rdr__ti"><h1 class="pp__t">${esc(u().none)}</h1><p class="pp__cta"><a class="btn" href="shop.html">${esc(u().lib)}</a></p></div>`; $('#rdTitle').hidden = false; return; }
    const want = forced && B.langs.indexOf(forced) >= 0 ? forced : (B.langs.indexOf(site) >= 0 ? site : B.langs[0]);
    const first = lang !== want || !$('#rdTocL').children.length; lang = want;
    frame();
    if (first) show(Math.min(+(q.get('c') || 0) || 0, N()), false); else show(cur, false);
  },
});
page.watch();

document.addEventListener('click', e => {
  const go = e.target.closest('[data-go]'); if (go) { e.preventDefault(); show(+go.dataset.go, true); return; }
  const rl = e.target.closest('[data-rl]'); if (rl) { forced = rl.dataset.rl; store.set('r11_rd_lang_' + bid, forced); lang = forced; frame(); show(0, false); return; }
  if (e.target.closest('#rdTocB')) { document.body.classList.add('rd-toc-open'); return; }
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
addEventListener('popstate', () => { show(+(new URLSearchParams(location.search).get('c') || 0), false); });
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
