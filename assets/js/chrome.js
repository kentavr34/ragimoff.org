/* test/11 — общая «рама» внутренних страниц: шапка, меню, тема, язык, соцсети, подвал. Тексты — из content.js, стили — из site.css.
   Страница передаёт onRender(t, L, lang): он вызывается при загрузке и при каждой смене языка. */
import { initTop } from './totop.js?v=11132210';
import { T, LINKS3 as LINKS } from './content.js?v=11132210';
import { PROGRAMS } from './programs.js?v=11132210';
import { initStats } from './stats.js?v=11132210';
import { initApp } from './app.js?v=11132210';
import { initSeo, switchLang } from './seo.js?v=11132210';

const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
export const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
export const ARR = '<span class="arrow">→</span>';
const CHEV = '<svg viewBox="0 0 10 10" aria-hidden="true"><path d="M2 3.5l3 3 3-3" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>';
const store = { get: k => { try { return localStorage.getItem(k); } catch (e) { return null; } }, set: (k, v) => { try { localStorage.setItem(k, v); } catch (e) {} } };
export const progUrl = slug => 'program.html?p=' + slug;

export function initChrome({ home = 'index.html', onRender }) {
  let lang = T[document.documentElement.lang] ? document.documentElement.lang : 'az';
  const head = $('#head');

  function render() {
    const t = T[lang], L = LINKS(lang);
    document.documentElement.lang = lang;
    const groups = [
      { k: 'spec', href: home + '#spec', sub: t.spec.p.map((p, i) => [L.spec[i], p.n]) },
      { k: 'books', href: L.shop || home + '#books', sub: t.books.b.map((b, i) => [L.books[i], b.t]).concat(L.shop && t.books.allBooks ? [[L.shop, t.books.allBooks]] : []) },
      { k: 'edu', href: 'program.html', sub: PROGRAMS.order.map(s => [progUrl(s), PROGRAMS.items[s][lang].title]) },
      { k: 'cons', href: 'consult.html?c=index', sub: t.cons.t.map((x, i) => [L.cons[i], x[0]]) },
      { k: 'corp', href: L.corp || 'corporate.html', sub: (t.corp.t || []).map(x => [L.corp || 'corporate.html', x]) }, { k: 'blog', href: L.blogAll || 'blog.html', sub: [] }, { k: 'contact', href: L.contact, sub: [] },
    ];
    $('#nav').innerHTML = groups.map(g => `<div class="nav__i"><a class="nav__l" href="${g.href}">${esc(t.nav[g.k])}${g.sub.length ? CHEV : ''}</a>${g.sub.length ? `<div class="nav__dd">${g.sub.map(s => `<a href="${s[0]}">${esc(s[1])}</a>`).join('')}</div>` : ''}</div>`).join('');
    $('#mobIn').innerHTML = `<a class="btn mob__cta" href="#reg">${esc(t.nav.cta)}</a>` + groups.map(g => `<div class="mob__g"><div class="mob__row"><a class="mob__big" href="${g.href}">${esc(t.nav[g.k])}</a>${g.sub.length ? `<button class="mob__tog" type="button" aria-label="+">${CHEV.replace('<svg', '<svg width="14" height="14"')}</button>` : ''}</div>${g.sub.length ? `<div class="mob__sub">${g.sub.map(s => `<a href="${s[0]}">${esc(s[1])}</a>`).join('')}</div>` : ''}</div>`).join('');
    const hc = $('#headCta'); hc.textContent = t.nav.cta;
    $$('[data-theme-btn]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.themeBtn === document.documentElement.dataset.theme)));
    $$('[data-lang-btn]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.langBtn === lang)));
    const ax = t.a11y; if (ax) { $('#nav').setAttribute('aria-label', ax.menu); $('#burger').setAttribute('aria-label', ax.menu); $('#themes').setAttribute('aria-label', ax.theme); $('#langs').setAttribute('aria-label', ax.lang); $$('[data-theme-btn]').forEach(b => b.setAttribute('aria-label', ax[b.dataset.themeBtn])); }
    const sh = $('#socH'); if (sh) sh.textContent = t.soc.h;
    const sl = $('#socList'); if (sl) sl.innerHTML = t.soc.l.map((x, i) => `<li><a href="${L.soc[i]}" target="_blank" rel="noopener">${esc(x)}</a></li>`).join('');
    const fc = t.foot.cols || [], fl = L.foot || [];
    const fb = $('#footCols'); if (fb) fb.innerHTML = fc.map((c, i) => `<div class="foot__col"><h3>${esc(c.h)}</h3><ul>${c.l.map((x, j) => { const u = (fl[i] || [])[j]; return `<li>${u ? `<a href="${u}"${/^https?:/.test(u) ? ' target="_blank" rel="noopener"' : ''}>${esc(x)}</a>` : esc(x)}</li>`; }).join('')}</ul></div>`).join('');
    const fp = $('#footCopy'); if (fp) fp.innerHTML = (t.foot.copy || []).map(x => `<span>${esc(x)}</span>`).join('');
    const fab = $('#fab'); if (fab) fab.href = L.wa;
    if (onRender) onRender(t, L, lang);
  }

  function setMenu(open) { $('#mob').classList.toggle('is-open', open); $('#mob').setAttribute('aria-hidden', String(!open)); $('#burger').setAttribute('aria-expanded', String(open)); document.documentElement.style.overflow = open ? 'hidden' : ''; head.classList.toggle('is-menu', open); if (open) head.classList.remove('is-hidden'); }
  document.addEventListener('click', e => {
    const tog = e.target.closest('.mob__tog'); if (tog) { tog.closest('.mob__g').classList.toggle('is-open'); return; }
    if (e.target.closest('#burger')) { setMenu(!$('#mob').classList.contains('is-open')); return; }
    if (e.target.closest('#mob a')) setMenu(false);
    let th = e.target.closest('[data-theme-btn]');
    if (th && innerWidth < 761 && th.getAttribute('aria-pressed') === 'true') { const all = $$('[data-theme-btn]'); th = all[(all.indexOf(th) + 1) % all.length]; }
    if (th) { document.documentElement.dataset.theme = th.dataset.themeBtn; store.set('r11_theme', th.dataset.themeBtn); render(); return; }
    const lg = e.target.closest('[data-lang-btn]'); if (lg) { if (switchLang(lg.dataset.langBtn)) return; lang = lg.dataset.langBtn; store.set('r11_lang', lang); render(); return; }
    const a = e.target.closest('a[href^="#"]'); if (a && a.getAttribute('href').length > 1) { const el = $(a.getAttribute('href')); if (el) { e.preventDefault(); scrollTo({ top: el.getBoundingClientRect().top + scrollY - 10, behavior: 'smooth' }); } }
  });
  let lastY = 0, travel = 0;
  addEventListener('scroll', () => {            /* шапка уходит при чтении вниз и возвращается при движении вверх */
    const y = scrollY, dy = y - lastY; if ((dy > 0) !== (travel > 0)) travel = 0; travel += dy; lastY = y;
    head.classList.toggle('is-solid', y > 20);
    if (y < 120 || $('#mob').classList.contains('is-open')) head.classList.remove('is-hidden'); else if (travel > 48) head.classList.add('is-hidden'); else if (travel < -32) head.classList.remove('is-hidden');
    const fab = $('#fab'); if (fab) { fab.classList.add('is-on'); fab.classList.toggle('is-off', innerWidth < 761 && head.classList.contains('is-hidden')); }
  }, { passive: true });
  const io = new IntersectionObserver(es => es.forEach(en => { if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); } }), { rootMargin: '0px 0px -8% 0px' });
  const watch = () => $$('.rv:not(.is-in)').forEach(el => io.observe(el));
  render(); watch();
  initSeo(() => lang); initApp(() => lang); initStats(() => lang);
  return { render, watch, get lang() { return lang; } };
}

initTop();
