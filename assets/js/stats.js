/* stats.js — своя статистика сайта (Кенан 13.11.2026). Данные уходят только на сервер школы (api.ragimoff.org/api/s),
   смотреть — в админке, вкладка «Статистика». Посетитель анонимный: случайный номер в браузере, без имени и IP.
   Что отмечается: просмотр страницы (источник, метки рекламы, язык, устройство), уход (время на странице, прокрутка),
   действия (WhatsApp, телефон, форма записи, отправленная заявка, «Читать», «В корзину», переход к оплате),
   чтение книг (книга, глава, сколько процентов главы прочитано). Работает только на ragimoff.org — не на локальных проверках. */
const API = 'https://api.ragimoff.org/api/s';
const ON = /(^|\.)ragimoff\.org$/.test(location.hostname) && !navigator.webdriver;
const st = (s, k, v) => { try { if (v === undefined) return s.getItem(k); s.setItem(k, v); } catch (e) { return null; } return v; };
const rid = () => Math.random().toString(36).slice(2, 10) + Date.now().toString(36);
let VID = '', SID = '', getLang = () => document.documentElement.lang, queue = [], timer = 0;

function ids() {
  VID = st(localStorage, 'rgm_vid') || st(localStorage, 'rgm_vid', rid());
  const last = +(st(localStorage, 'rgm_last') || 0), now = Date.now();
  SID = st(sessionStorage, 'rgm_sid');
  if (!SID || now - last > 30 * 60e3) SID = st(sessionStorage, 'rgm_sid', rid());      /* визит: вкладка, 30 мин без действий — новый */
  st(localStorage, 'rgm_last', String(now));
}
const device = () => (innerWidth < 700 ? 'mob' : innerWidth < 1100 ? 'tab' : 'desk');
function flush(beacon) {
  if (!queue.length) return;
  const body = JSON.stringify(queue.splice(0, 30));
  try { if (beacon && navigator.sendBeacon && navigator.sendBeacon(API, new Blob([body], { type: 'text/plain' }))) return; } catch (e) {}
  try { fetch(API, { method: 'POST', body, headers: { 'Content-Type': 'text/plain' }, keepalive: true, mode: 'cors', credentials: 'omit' }).catch(() => {}); } catch (e) {}
}
export function stat(t, extra) {
  if (!ON) return;
  st(localStorage, 'rgm_last', String(Date.now()));
  queue.push(Object.assign({ t, v: VID, s: SID, p: location.pathname + location.search, l: getLang() }, extra || {}));
  clearTimeout(timer); timer = setTimeout(() => flush(false), 1500);
}

/* прокрутка и время на странице */
let shownAt = Date.now(), visible = 0, depth = 0;
const scrollPct = () => { const h = document.documentElement.scrollHeight - innerHeight; return h > 0 ? Math.min(100, Math.round(100 * scrollY / h)) : 100; };
addEventListener('scroll', () => { depth = Math.max(depth, scrollPct()); }, { passive: true });

/* чтение книги: глава и сколько процентов прочитано (страница читалки) */
let chap = null;
function chapNow() {
  if (document.body.dataset.kind !== 'read') return null;
  const b = (document.querySelector('.rdr') || {}).dataset ? document.querySelector('.rdr').dataset.book : '';
  const q = new URLSearchParams(location.search || window.__Q || ''), m = location.pathname.match(/\/read\/([\w-]+)\/([^/]+)\.html$/);
  const c = q.get('p') || q.get('c') || (m && m[2] !== 'index' ? m[2] : '');
  return b && c && c !== '0' ? { b, c } : null;
}
function chapFlush(beacon) {
  if (chap) { stat('read', { b: chap.b, c: chap.c, pc: chap.max }); if (beacon) flush(true); }
  chap = null;
}
function chapTrack() {
  const n = chapNow();
  if (chap && n && n.b === chap.b && n.c === chap.c) return;
  chapFlush(false);
  if (n) chap = Object.assign(n, { max: scrollPct() });
}
addEventListener('scroll', () => { if (chap) chap.max = Math.max(chap.max, scrollPct()); }, { passive: true });

function leave() {
  if (!ON) return;
  if (document.visibilityState === 'hidden') {
    visible += Date.now() - shownAt;
    stat('leave', { du: Math.round(visible / 1000), dp: Math.max(depth, scrollPct()) });
    if (chap) stat('read', { b: chap.b, c: chap.c, pc: chap.max });
    flush(true);
  } else shownAt = Date.now();
}

/* действия по щелчку */
function onClick(e) {
  const a = e.target.closest('a, button');
  if (!a) return;
  const h = a.getAttribute('href') || '';
  if (/wa\.me|whatsapp/i.test(h) || a.closest('.fab')) return stat('click', { x: 'whatsapp:' + location.pathname });
  if (/^tel:/.test(h)) return stat('click', { x: 'tel:' + location.pathname });
  if (a.matches('[data-reg]') || /#reg$/.test(h) || a.matches('.head__cta, .mob__cta')) return stat('form', { x: 'form:' + location.pathname });
  if (a.matches('[data-cart]')) return stat('cart', { x: 'cart:' + a.dataset.cart });
  if (/read\.html|\/read\//.test(h)) return stat('click', { x: 'read:' + h.replace(/^\/(az|ru|en)\//, '').slice(0, 60) });
}

/* вызывать один раз на странице */
export function initStats(lang) {
  if (!ON) return;
  if (lang) getLang = lang;
  ids();
  const u = new URLSearchParams(location.search);
  stat('pv', { r: document.referrer || '', d: device(), us: u.get('utm_source') || '', um: u.get('utm_medium') || '', uc: u.get('utm_campaign') || '' });
  document.addEventListener('visibilitychange', leave);
  addEventListener('pagehide', () => { if (document.visibilityState !== 'hidden') { document.dispatchEvent(new Event('visibilitychange')); } });
  document.addEventListener('click', onClick, true);
  /* заявка отправлена, переход к оплате — сообщают формы через событие */
  addEventListener('rgm:stat', e => { const d = e.detail || {}; if (d.t) stat(d.t, { x: d.x || '' }); if (d.t === 'pay') flush(true); });
  /* читалка: смена главы меняет адрес (pushState) — отмечаем прочитанную главу */
  if (document.body.dataset.kind === 'read') {
    const wrap = k => { const f = history[k]; history[k] = function () { const r = f.apply(this, arguments); setTimeout(chapTrack, 50); return r; }; };
    wrap('pushState'); wrap('replaceState');
    addEventListener('popstate', () => setTimeout(chapTrack, 50));
    setTimeout(chapTrack, 1500);
  }
}
