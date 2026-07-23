/* Переключатель языков AZ/RU/EN/TR (ragimoff.org) — компактный ДРОПДАУН на месте логотипа КП.
   Заменяет бейдж .logo (КП) кнопкой языка (глобус + код). Клик → попап с кодами AZ/RU/EN/TR → переход.
   Только аббревиатуры. Вычисляет ссылки на языковые версии текущей страницы из URL. Кенан 2026-07-23. */
(function () {
  "use strict";
  var LANGS = [
    { code: "az", short: "AZ" }, { code: "ru", short: "RU" },
    { code: "en", short: "EN" }, { code: "tr", short: "TR" }
  ];
  var LCODES = { ru: 1, en: 1, tr: 1 };

  function build() {
    var path = window.location.pathname;
    if (path.charAt(path.length - 1) === "/") path += "index.html";
    if (path.charAt(0) === "/") path = path.slice(1);
    var segs = path.split("/");
    var li = segs.length - 2;
    var cur = "az";
    if (li >= 0 && LCODES[segs[li]]) cur = segs[li];
    var base = segs.slice();
    if (cur !== "az") base.splice(li, 1);
    function urlFor(code) {
      var s = base.slice();
      if (code !== "az") s.splice(s.length - 1, 0, code);
      return "/" + s.join("/");
    }
    return { cur: cur, urlFor: urlFor };
  }

  function injectStyle() {
    if (document.getElementById("lang-switch-css")) return;
    var css = "" +
      ".lsw{position:relative;display:inline-flex;vertical-align:middle;font:700 14px/1 system-ui,-apple-system,sans-serif}" +
      ".lsw-btn{display:inline-flex;align-items:center;gap:5px;padding:8px 12px;border-radius:9px;cursor:pointer;" +
      "background:#f2c94c;color:#1b3a5b;border:none;font:inherit}" +
      ".lsw-btn:hover{background:#e8bf3e}.lsw-btn svg{width:16px;height:16px;fill:currentColor}" +
      ".lsw-menu{position:absolute;top:calc(100% + 6px);left:0;min-width:64px;background:#fff;border-radius:10px;" +
      "box-shadow:0 6px 24px rgba(0,0,0,.22);padding:5px;z-index:99999;display:none}" +
      ".lsw.open .lsw-menu{display:block}" +
      ".lsw-menu a{display:block;padding:9px 14px;border-radius:7px;text-decoration:none;color:#1b3a5b;font-weight:700;text-align:center}" +
      ".lsw-menu a:hover{background:#f5f6f8}.lsw-menu a.on{background:#f2c94c}";
    var st = document.createElement("style");
    st.id = "lang-switch-css"; st.textContent = css;
    document.head.appendChild(st);
  }

  var GLOBE = '<svg viewBox="0 0 24 24"><path d="M12 2a10 10 0 100 20 10 10 0 000-20zm6.9 6h-2.6a15.7 15.7 0 00-1.4-3.6A8 8 0 0118.9 8zM12 4c.8 1.2 1.5 2.5 1.9 4h-3.8c.4-1.5 1.1-2.8 1.9-4zM4.3 14a8 8 0 010-4h3a17.5 17.5 0 000 4h-3zm.8 2h2.6c.4 1.3.9 2.5 1.4 3.6A8 8 0 015.1 16zm2.6-8H5.1a8 8 0 013.9-3.6C8.4 5.5 7.9 6.7 7.7 8zM12 20c-.8-1.2-1.5-2.5-1.9-4h3.8c-.4 1.5-1.1 2.8-1.9 4zm2.3-6H9.7a15.5 15.5 0 010-4h4.6a15.5 15.5 0 010 4zm.6 5.6c.5-1.1 1-2.3 1.4-3.6h2.6a8 8 0 01-4 3.6zM16.7 14a17.5 17.5 0 000-4h3a8 8 0 010 4h-3z"/></svg>';

  function makeSwitcher(host, info) {
    var cur = LANGS.filter(function (L) { return L.code === info.cur; })[0] || LANGS[0];
    var items = LANGS.map(function (L) {
      var on = L.code === info.cur;
      return '<a href="' + (on ? "#" : info.urlFor(L.code)) + '"' + (on ? ' class="on" aria-current="page"' : "") + ">" + L.short + "</a>";
    }).join("");
    host.className = "lsw";
    host.removeAttribute("href"); host.removeAttribute("onclick");
    host.innerHTML = '<span class="lsw-btn" role="button" aria-haspopup="true" aria-label="Dil / Язык / Language">' +
      GLOBE + '<span>' + cur.short + '</span></span><div class="lsw-menu" role="menu">' + items + '</div>';
    host.querySelector(".lsw-btn").addEventListener("click", function (e) {
      e.preventDefault(); e.stopPropagation(); host.classList.toggle("open");
    });
  }

  function render() {
    injectStyle();
    var info = build();
    var logos = document.querySelectorAll(".hdr-logo");
    if (logos.length) {
      // заменяем бейдж КП на переключатель; скрываем прежний контейнер справа
      logos.forEach(function (el) { makeSwitcher(el, info); });
      Array.prototype.forEach.call(document.querySelectorAll("[data-lang-switch]"), function (c) {
        c.style.display = "none";
      });
    } else {
      var host = document.querySelector("[data-lang-switch]");
      if (host) makeSwitcher(host, info);
    }
    document.addEventListener("click", function () {
      Array.prototype.forEach.call(document.querySelectorAll(".lsw.open"), function (x) { x.classList.remove("open"); });
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", render);
  else render();
})();
