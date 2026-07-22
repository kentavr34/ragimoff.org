/* Универсальный переключатель языков AZ/RU/EN (ragimoff.org).
   Вычисляет ссылки на языковые версии ТЕКУЩЕЙ страницы из URL —
   одинаковая разметка работает на всех языках (главная + книга),
   не требует переписывания ссылок при inject. Кенан 2026-07-22.

   Использование: положить в шапку контейнер
     <div class="lang-switch-bar" data-lang-switch></div>
   и подключить <script src="/_lang-switch.js" defer></script>.
   Структура URL: AZ = base; RU = <dir>/ru/<file>; EN = <dir>/en/<file>. */
(function () {
  "use strict";
  var LANGS = [
    { code: "az", label: "AZ", aria: "Azərbaycanca" },
    { code: "ru", label: "RU", aria: "Русская версия" },
    { code: "en", label: "EN", aria: "English" }
  ];

  function build() {
    var path = window.location.pathname;
    // индекс каталога (trailing "/") → явный index.html (GitHub Pages его и отдаёт)
    if (path.charAt(path.length - 1) === "/") path += "index.html";
    if (path.charAt(0) === "/") path = path.slice(1);
    var segs = path.split("/");

    // текущий язык = сегмент перед файлом, если это ru/en
    var li = segs.length - 2;
    var cur = "az";
    if (li >= 0 && (segs[li] === "ru" || segs[li] === "en")) {
      cur = segs[li];
    }
    // база (AZ) — без языкового сегмента
    var base = segs.slice();
    if (cur !== "az") base.splice(li, 1);

    function urlFor(code) {
      var s = base.slice();
      if (code !== "az") {
        // вставить язык перед файлом (последним сегментом)
        s.splice(s.length - 1, 0, code);
      }
      return "/" + s.join("/");
    }
    return { cur: cur, urlFor: urlFor };
  }

  function render() {
    var host = document.querySelector("[data-lang-switch]");
    if (!host) return;
    var info = build();
    var html = "";
    LANGS.forEach(function (L) {
      var active = L.code === info.cur ? " lang-active" : "";
      var href = L.code === info.cur ? "#" : info.urlFor(L.code);
      html += '<a href="' + href + '" class="lang-switch' + active + '" aria-label="' + L.aria + '"' +
        (L.code === info.cur ? ' aria-current="page"' : "") + ">" + L.label + "</a>";
    });
    host.innerHTML = html;
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", render);
  } else {
    render();
  }
})();
