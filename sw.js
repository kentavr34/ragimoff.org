/* RAGIMOFF — сервис-воркер перехода (12.11.2026).
   Прежний сайт сохранял страницы и файлы на устройстве. После перехода на новую версию эти копии
   показывали бы старый сайт, поэтому этот файл стирает сохранённое и снимает себя с устройства.
   Новая версия сервис-воркер не ставит. */
self.addEventListener('install', function () { self.skipWaiting(); });
self.addEventListener('activate', function (e) {
  e.waitUntil(caches.keys().then(function (keys) { return Promise.all(keys.map(function (k) { return caches.delete(k); })); })
    .then(function () { return self.registration.unregister(); })
    .then(function () { return self.clients.matchAll({ type: 'window' }); })
    .then(function (cs) { cs.forEach(function (c) { try { c.navigate(c.url); } catch (er) {} }); }));
});
