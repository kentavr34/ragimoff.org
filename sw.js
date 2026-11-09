/* RAGIMOFF — приложение (PWA, Кенан 09.11.2026).
   Всё, что человек открыл (страницы сайта, читалка, главы книг, картинки), сохраняется на устройстве;
   без интернета открывается из памяти телефона.
   Страницы: сначала сеть (свежая версия), при отсутствии сети — сохранённая копия.
   Файлы (стили, скрипты, шрифты, картинки, главы читалки): сразу из памяти, в фоне обновляются.
   Заявки и оплата (api.ragimoff.org, POST) не кэшируются никогда. */
var V = 'rgm-v3';
var PAGES = V + '-pages', FILES = V + '-files';
var OFFLINE = '/offline.html';
var CORE = [OFFLINE, '/assets/css/nocturne.css', '/assets/js/nocturne.js', '/favicons/android-chrome-192x192.png'];
var MAX_PAGES = 300, MAX_FILES = 1500;

self.addEventListener('install', function (e) {
  e.waitUntil(caches.open(FILES).then(function (c) { return c.addAll(CORE); }).then(function () { return self.skipWaiting(); }));
});

self.addEventListener('activate', function (e) {
  e.waitUntil(caches.keys().then(function (keys) {
    return Promise.all(keys.filter(function (k) { return k.indexOf(V) !== 0; }).map(function (k) { return caches.delete(k); }));
  }).then(function () { return self.clients.claim(); }));
});

function trim(name, max) {
  caches.open(name).then(function (c) {
    c.keys().then(function (keys) { if (keys.length > max) { c.delete(keys[0]).then(function () { trim(name, max); }); } });
  });
}

self.addEventListener('fetch', function (e) {
  var req = e.request, url = new URL(req.url);
  if (req.method !== 'GET') return;
  var sameOrigin = url.origin === self.location.origin;
  var fonts = /fonts\.(googleapis|gstatic)\.com$/.test(url.hostname);
  if (!sameOrigin && !fonts) return;                       /* оплата, заявки, внешние сервисы — мимо */
  if (url.pathname.indexOf('/payment/') === 0) return;     /* страницы оплаты — всегда из сети */

  if (req.mode === 'navigate' || (req.headers.get('accept') || '').indexOf('text/html') !== -1) {
    e.respondWith(fetch(req).then(function (res) {
      if (res && res.ok) { var copy = res.clone(); caches.open(PAGES).then(function (c) { c.put(req, copy); trim(PAGES, MAX_PAGES); }); }
      return res;
    }).catch(function () {
      return caches.match(req, { ignoreSearch: true }).then(function (hit) { return hit || caches.match(OFFLINE); });
    }));
    return;
  }

  e.respondWith(caches.match(req).then(function (hit) {
    var net = fetch(req).then(function (res) {
      if (res && (res.ok || res.type === 'opaque')) { var copy = res.clone(); caches.open(FILES).then(function (c) { c.put(req, copy); trim(FILES, MAX_FILES); }); }
      return res;
    }).catch(function () { return hit; });
    return hit || net;
  }));
});
