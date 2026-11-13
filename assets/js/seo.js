/* seo.js — постоянные адреса страниц на каждом языке (13.11.2026, слово Кенана: превью и поиск — на языке посетителя).
   Статичные снимки страниц лежат в /az/, /ru/, /en/ (их собирает _tools/build_static.py): в них уже есть текст страницы,
   заголовок, описание, превью и разметка для поисковиков и ИИ. Здесь внутренние ссылки сайта переводятся на эти адреса,
   а смена языка на снимке ведёт на снимок того же адреса на другом языке. */
import { BOOK_LANGS } from './seo-map.js?v=11132210';

const store = { set: (k, v) => { try { localStorage.setItem(k, v); } catch (e) {} } };
const LANGS = ['az', 'ru', 'en'];

/* адрес снимка для ссылки сайта; null — ссылка остаётся как есть */
export function staticHref(h, lang) {
  if (!h || /^(https?:|mailto:|tel:|\/\/|javascript:)/.test(h) || h.charAt(0) === '#') return null;
  const m = h.replace(/^\/+/, '').match(/^([\w-]*\.html)?(\?[^#]*)?(#.*)?$/);
  if (!m) return null;
  const page = (m[1] || 'index.html').replace(/\.html$/, ''), q = new URLSearchParams(m[2] || ''), hash = m[3] || '';
  const P = (s) => '/' + lang + '/' + s + '.html' + hash;
  switch (page) {
    case 'index': return m[2] ? null : '/' + lang + '/' + hash;
    case 'shop': case 'blog': case 'contact': case 'corporate': case 'test': return m[2] ? null : P(page);
    case 'program': return P('program-' + (q.get('p') || 'general'));   /* без программы — первая (общая психология), как в шаблоне */
    case 'specialist': return q.get('s') ? P('specialist-' + q.get('s')) : null;
    case 'consult': { const c = q.get('c'); return !c || c === 'index' ? P('consult') : P('consult-' + c); }
    case 'article': return q.get('a') ? P('article-' + q.get('a')) : null;
    case 'book': return q.get('b') && BOOK_LANGS[q.get('b')] ? P('book-' + q.get('b')) : null;   /* у книг, вошедших в сборник, своей страницы нет */
    case 'read': {
      const b = q.get('b'); if (!b || !BOOK_LANGS[b]) return null;
      const L = BOOK_LANGS[b].indexOf(lang) >= 0 ? lang : BOOK_LANGS[b][0];
      const part = q.get('p') ? q.get('p') : q.get('c') ? q.get('c') : 'index';
      return '/' + L + '/read/' + b + '/' + part + '.html' + hash;
    }
    default: return null;
  }
}

function relink(lang) {
  document.querySelectorAll('a[href]').forEach(a => {
    if (a.closest('[data-keep-href]')) return;
    const n = staticHref(a.getAttribute('href'), lang);
    if (n && n !== a.getAttribute('href')) a.setAttribute('href', n);
  });
}

/* вызывать один раз: следит за перерисовками страницы и переводит ссылки на снимки текущего языка */
export function initSeo(getLang) {
  let t = 0;
  const run = () => { t = 0; relink(getLang()); };
  new MutationObserver(() => { if (!t) t = setTimeout(run, 30); }).observe(document.body, { childList: true, subtree: true });
  run();
}

/* смена языка: на снимке — переход на снимок того же адреса на другом языке; true — переход начат */
export function switchLang(lang) {
  if (LANGS.indexOf(lang) < 0) return false;
  store.set('r11_lang', lang);
  if (!window.__LANG) return false;
  const alt = document.querySelector('link[rel="alternate"][hreflang="' + lang + '"]');
  const to = alt && alt.href ? new URL(alt.href).pathname : '';          /* путь, без домена: работает и на ragimoff.org, и на локальной копии */
  if (to && to !== location.pathname) { location.href = to + location.hash; return true; }
  return false;
}
