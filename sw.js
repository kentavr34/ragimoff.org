/* RAGIMOFF — приложение (PWA). Восстановлено 13.11.2026 по слову Кенана для новой версии сайта.
   Всё, что человек открыл (страницы, читалка, главы книг, картинки), сохраняется на устройстве; без интернета открывается из памяти.
   Страницы: сначала сеть (всегда свежая версия), без сети — сохранённая копия. Файлы (стили, сценарии, шрифты, картинки,
   главы книг, данные): сразу из памяти, в фоне обновляются. Заявки и оплата (api.ragimoff.org, POST, /payment/) — никогда.
   Копии прежнего сайта (rgm-v1…v4) при первом запуске стираются. */
var V = 'rgm-v5';
var PAGES = V + '-pages', FILES = V + '-files';
var MAX_PAGES = 400, MAX_FILES = 2500;
var OFFLINE = '<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>RAGIMOFF</title>' +
  '<body style="background:#07090E;color:#e8e2d6;font:16px/1.5 system-ui;display:grid;place-items:center;min-height:100vh;margin:0;padding:24px;text-align:center">' +
  '<div><p style="font-size:28px;margin:0 0 12px">RAGIMOFF</p><p>İnternet yoxdur · Нет интернета · No connection</p><p><a style="color:#c9a961" href="/">↻</a></p></div>';

self.addEventListener('install', function () { self.skipWaiting(); });
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
  var same = url.origin === self.location.origin, fonts = /fonts\.(googleapis|gstatic)\.com$/.test(url.hostname);
  if (!same && !fonts) return;                                   /* оплата, заявки, внешние сервисы — мимо */
  if (url.pathname.indexOf('/payment/') === 0 || /\.apk$/.test(url.pathname)) return;
  if (req.mode === 'navigate' || (req.headers.get('accept') || '').indexOf('text/html') !== -1) {
    e.respondWith(fetch(req).then(function (res) {
      if (res && res.ok) { var copy = res.clone(); caches.open(PAGES).then(function (c) { c.put(req, copy); trim(PAGES, MAX_PAGES); }); }
      return res;
    }).catch(function () {
      return caches.match(req).then(function (hit) {
        return hit || caches.match(req, { ignoreSearch: true }).then(function (h2) {
          return h2 || new Response(OFFLINE, { headers: { 'Content-Type': 'text/html; charset=utf-8' } });
        });
      });
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
