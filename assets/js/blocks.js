/* test/11 — блоки внутренних страниц: один набор на специалистов, консультации, контакты, тренинги, право, блог.
   Данные — data/<kind>/<slug>.<lang>.json (формат: _agent/docs/DATA_SCHEMA.md), подписи — content.js (T[l].pg), стили — site.css (раздел PG). */
import { esc } from './chrome.js?v=11131356';

/* старые адреса сайта → адреса новой версии (одно место на весь сайт) */
const PROG = { 'umumi-psixologiya': 'general', 'klinik-psixologiya': 'clinical', 'psixoterapiya-praktikumu': 'practicum', psixodiaqnostika: 'psychodiagnostics', qisamuddetli: 'cbt', psixoanaliz: 'psychoanalysis', 'aile-terapiyasi': 'family' };
export function fixUrl(u) {
  if (!u) return '#';
  if (/^(https?:|mailto:|tel:|#)/.test(u)) return u;
  let m;
  const p = u.replace(/^\/(az|ru|en)\//, '/').replace(/^(\.\.\/)+/, '/');
  const hash = (p.match(/#.*$/) || [''])[0], q = p.replace(/#.*$/, '');
  if (/#registration|#qeydiyyat|#order/.test(hash)) return '#reg';
  if ((m = q.match(/^\/mutexessisler\/(kenan|samire)/))) return 'specialist.html?s=' + (m[1] === 'kenan' ? 'kenan' : 'samira');
  if (/^\/mutexessisler\//.test(q)) return 'index.html#spec';
  if (/^\/konsultasiya\/(index\.html)?$/.test(q)) return 'index.html#cons';
  if ((m = q.match(/^\/konsultasiya\/([\w-]+)\.html$/))) return 'consult.html?c=' + m[1];
  if (/^\/bloq\/(index\.html)?$/.test(q)) return 'blog.html';
  if ((m = q.match(/^\/bloq\/([\w-]+)\.html$/))) return 'article.html?a=' + m[1];
  if (/^\/telim\/qanuni-esaslar/.test(q)) return 'program.html?p=general#law';
  if (/^\/telim\/(index\.html)?$/.test(q)) return 'index.html#edu';
  if ((m = q.match(/^\/telim\/([\w-]+)\.html$/)) && PROG[m[1]]) return 'program.html?p=' + PROG[m[1]];
  if (/^\/korporativ\//.test(q)) return 'corporate.html';
  if (/^\/elaqe\//.test(q)) return 'contact.html';
  if (/^\/(index\.html)?$/.test(q)) return 'index.html' + hash;
  /* прежние адреса книг → единая читалка и каталог (с 12.11.2026 старых читалок на сайте нет) */
  if ((m = q.match(/^\/klinik-psixiatriya(?:\/(?:(?:ru|en|tr)\/)?(?:([\w-]+)\.html)?)?$/))) return 'read.html?b=klinik-psixiatriya' + (m[1] && m[1] !== 'index' ? '&p=' + m[1] : '') + hash;
  if (/^\/books\/((ru|en)\/)?(index\.html)?$/.test(q)) return 'shop.html';
  if ((m = q.match(/^\/books\/([\w-]+)\//)) && !/^(ru|en|covers)$/.test(m[1])) return 'read.html?b=' + m[1];
  return u;                                        /* прочее — как есть */
}
export const fixImg = u => (u && u.indexOf('/images/') === 0 ? 'assets/img/' + u.slice(8) : u);

/* строка с разрешённой разметкой: strong, em, b, i, a, br, sup, sub — всё остальное экранируется */
export function rich(s) {
  return esc(s)
    .replace(/&lt;(\/?)(strong|em|b|i|sup|sub)&gt;/g, '<$1$2>')
    .replace(/&lt;br\s*\/?&gt;/g, '<br>')
    .replace(/&lt;a href=&quot;(.*?)&quot;[^&]*?&gt;/g, (m, h) => { const u = fixUrl(h.replace(/&amp;/g, '&')); return `<a href="${esc(u)}"${/^https?:/.test(u) ? ' target="_blank" rel="noopener"' : ''}>`; })
    .replace(/&lt;\/a&gt;/g, '</a>')
    .replace(/\+\d[\d ]{8,16}\d/g, m => `<span class="nw">${m}</span>`);        /* номер телефона не рвётся */
}
const ext = u => (/^https?:/.test(u) ? ' target="_blank" rel="noopener"' : '');
const btns = (list, cls) => (list && list.length ? `<p class="pg__btns${cls || ''}">${list.map((b, i) => { const u = fixUrl(b[1]); return `<a class="btn${i ? ' btn--line' : ''}" href="${esc(u)}"${ext(u)}>${esc(String(b[0]).replace(/\s*[→›↗]+\s*$/, ''))}</a>`; }).join('')}</p>` : '');
const sub = b => (b.sub ? `<p class="pg__sub">${rich(b.sub)}</p>` : '');

const R = {
  cards: (b) => `<ol class="pcs${b.num ? ' pcs--num' : ''}">${b.items.map((x, i) => `<li class="pc2 rv">${x.n ? `<span class="pc2__n pc2__n--big">${esc(x.n)}</span>` : b.num ? `<span class="pc2__n">${String(i + 1).padStart(2, '0')}</span>` : ''}${x.t ? `<h3 class="pc2__t">${rich(x.t)}</h3>` : ''}${x.d ? `<p class="pc2__d">${rich(x.d)}</p>` : ''}</li>`).join('')}</ol>`,
  groups: (b) => `<div class="grps">${b.items.map(x => `<article class="grp rv">${x.meta ? `<p class="grp__m">${rich(x.meta)}</p>` : ''}<h3 class="grp__t${String(x.t || '').length > 70 ? ' grp__t--long' : ''}">${rich(x.t)}</h3>${x.d ? `<p class="grp__d">${rich(x.d)}</p>` : ''}${x.list && x.list.length ? `<ul class="grp__l">${x.list.map(i => `<li>${rich(i)}</li>`).join('')}</ul>` : ''}</article>`).join('')}</div>`,
  timeline: (b) => `<ol class="tl">${b.items.map(x => `<li class="tl__i rv"><span class="tl__y">${esc(x.y || '')}</span><div class="tl__b">${x.t ? `<h3 class="tl__t">${rich(x.t)}</h3>` : ''}${x.d ? `<p class="tl__d">${rich(x.d)}</p>` : ''}${x.a ? `<a class="tl__a" href="${esc(fixUrl(x.a[1]))}">${esc(x.a[0])}</a>` : ''}</div></li>`).join('')}</ol>`,
  gallery: (b) => `<div class="gal">${b.items.map(x => `<button type="button" class="gal__i rv" data-zoom="${esc(fixImg(x.src))}" data-cap="${esc(x.cap || '')}"><img src="${esc(fixImg(x.src))}" alt="${esc(x.cap || '')}" loading="lazy"><span>${esc(x.cap || '')}</span></button>`).join('')}</div>`,
  videos: (b, u) => `<div class="vds">${b.items.map(x => `<a class="vd rv" href="https://youtu.be/${esc(x.yt)}" target="_blank" rel="noopener"><span class="vd__ph"><img src="https://i.ytimg.com/vi/${esc(x.yt)}/hqdefault.jpg" alt="" loading="lazy" width="480" height="360"><i aria-hidden="true"></i></span><b class="vd__t">${rich(x.t || '')}</b>${x.d ? `<span class="vd__d">${rich(x.d)}</span>` : ''}</a>`).join('')}</div>${b.channel ? btns([b.channel]) : ''}`,
  who: (b, u, ctx) => `<div class="tchs">${(b.ids || []).map(id => { const i = id === 'samira' ? 1 : 0, p = ctx.t.spec.p[i]; return `<a class="tch rv" href="specialist.html?s=${i ? 'samira' : 'kenan'}"><span class="tch__ph"><img src="assets/img/specialists/${i ? 'samira' : 'kenan'}.jpg" alt="${esc(p.n)}" loading="lazy" width="96" height="96"></span><span class="tch__b"><b>${esc(p.n)}</b><span>${esc(p.r)}</span></span></a>`; }).join('')}</div>`,
  prices: (b, u) => {
    if (b.set && u.prices[b.set]) { const P = u.prices[b.set]; return `<div class="prices rv">${P.rows.map(r => `<div class="prow"><span>${esc(r[0])}${r[2] ? `<small>${esc(r[2])}</small>` : ''}</span><b>${esc(r[1])}</b></div>`).join('')}<p class="pnote">${esc(P.note)}</p></div>`; }
    return `<div class="prices rv">${(b.rows || []).map(r => `<div class="prow"><span>${rich(r[0])}</span><b>${rich(r[1])}</b></div>`).join('')}${b.note ? `<p class="pnote">${rich(b.note)}</p>` : ''}</div>`;
  },
  articles: (b, u, ctx) => `<div class="psts">${(b.items || []).map(s => { const a = ctx.blog[s]; if (!a) return ''; return `<a class="pst rv" href="article.html?a=${esc(s)}">${a.cover ? `<span class="pst__ph"><img src="${esc(fixImg(a.cover))}" alt="" loading="lazy" width="1600" height="900"></span>` : ''}<span class="pst__b"><span class="pst__m">${esc(a.meta || a.catLabel || '')}</span><b class="pst__t">${esc(a.title)}</b>${b.full && a.excerpt ? `<span class="pst__d">${esc(a.excerpt)}</span>` : ''}</span></a>`; }).join('')}</div>`,
  faq: (b) => `<div class="accs">${b.items.map(q => `<details class="acc rv"><summary><span>${rich(q[0])}</span><i aria-hidden="true"></i></summary><p>${rich(q[1])}</p></details>`).join('')}</div>`,
  list: (b) => `<ul class="facts pp__list rv">${b.items.map(x => `<li><span>${rich(x)}</span></li>`).join('')}</ul>`,
  text: (b) => `<div class="txt rv">${(b.p || []).map(x => `<p>${rich(x)}</p>`).join('')}</div>`,
  stats: (b) => `<dl class="pp__facts pg__stats rv">${b.items.map(x => `<div class="fact"><dd>${rich(x[0])}</dd><dt>${rich(x[1])}</dt></div>`).join('')}</dl>`,
  table: (b) => `<div class="tblw rv"><table class="tbl">${b.caption ? `<caption>${rich(b.caption)}</caption>` : ''}${b.head && b.head.length ? `<thead><tr>${b.head.map(x => `<th>${rich(x)}</th>`).join('')}</tr></thead>` : ''}<tbody>${(b.rows || []).map(r => `<tr>${r.map(x => `<td>${rich(x)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`,
  quotes: (b) => `<div class="qts">${b.items.map(x => `<figure class="qt rv"><blockquote>${rich(x.text)}</blockquote><figcaption><b>${rich(x.name || '')}</b>${x.meta ? `<span>${rich(x.meta)}</span>` : ''}</figcaption></figure>`).join('')}</div>`,
  contact: (b) => `<div class="cts">${b.items.map(x => `<div class="ct rv"><h3 class="ct__t">${rich(x.t || '')}</h3>${(x.p || []).map(p => `<p class="ct__p">${rich(p)}</p>`).join('')}${btns(x.btns)}${x.note ? `<p class="pnote">${rich(x.note)}</p>` : ''}</div>`).join('')}</div>`,
  links: (b) => `<ul class="lks rv">${b.items.map(x => { const u = fixUrl(x[1]); return `<li><a href="${esc(u)}"${ext(u)}>${rich(x[0])}</a>${x[2] ? `<span>${rich(x[2])}</span>` : ''}</li>`; }).join('')}</ul>`,
  note: (b) => `<div class="nt rv">${b.t ? `<h3 class="nt__t">${rich(b.t)}</h3>` : ''}${b.d ? `<p>${rich(b.d)}</p>` : ''}</div>`,
  figure: (b) => `<figure class="fig rv"><img src="${esc(fixImg(b.src))}" alt="${esc(b.cap || '')}" loading="lazy">${b.cap ? `<figcaption>${rich(b.cap)}</figcaption>` : ''}</figure>`,
  cta: (b) => btns(b.btns, ' rv'),
  sources: (b) => `<div class="srcs rv">${b.items.map(x => `<p>${proseHtml(x)}</p>`).join('')}</div>`,
};

/* статья: разметка собрана нашим же инструментом (build_blog.py) из страниц сайта — правим только адреса */
function proseHtml(h) {
  return String(h).replace(/(<a\s+href=")([^"]*)(")/g, (m, a, u, c) => { const f = fixUrl(u.replace(/&amp;/g, '&')); return a + esc(f) + c + ext(f); })
    .replace(/(<img\b[^>]*\ssrc=")([^"]*)(")/g, (m, a, u, c) => a + esc(fixImg(u)) + c + ' loading="lazy"')
    .replace(/<table>/g, '<div class="tblw"><table class="tbl">').replace(/<\/table>/g, '</table></div>');
}

/* один раздел: заголовок слева, содержимое справа (как на странице программы); у статьи — одна колонка чтения */
export function renderBlocks(blocks, u, ctx) {
  return (blocks || []).map((b0, i) => { let b = b0;
    if (b.type === 'prose') return `<section class="sec sec--prose"><div class="wrap"><article class="prose">${proseHtml(b.html)}</article></div></section>`;
    const fn = R[b.type]; if (!fn) return '';
    
    let h = b.h || (b.type === 'who' ? b.label : '') || (b.type === 'sources' ? b.t : '') || '';
    if (h.length > 64) { b = Object.assign({}, b, { sub: h + (b.sub ? ' ' + b.sub : '') }); h = ''; }   /* длинная фраза — не заголовок раздела, а подзаголовок */
    const body = fn(b, u, ctx); if (!body) return '';
    if (b.type === 'stats') return `<section class="sec sec--stats"><div class="wrap">${body}</div></section>`;
    return `<section class="sec${h ? '' : ' sec--tail'}" data-b="${b.type}"><div class="wrap pp__two"><div class="pg__hd">${h ? `<h2 class="pp__h rv">${rich(h)}</h2>` : ''}</div><div class="pg__bd">${sub(b)}${body}</div></div></section>`;
  }).join('');
}
