/* Переключатель языков AZ/RU/EN/TR (ragimoff.org) — КОМПАКТНЫЙ ДРОПДАУН (мобиле-friendly).
   Одна кнопка (глобус + текущий язык) → клик → попап с 4 языками → выбор → переход.
   Вычисляет ссылки на языковые версии ТЕКУЩЕЙ страницы из URL. Самодостаточные стили.
   Использование: <div class="lang-switch-bar" data-lang-switch></div> + <script src="/_lang-switch.js" defer>.
   Кенан 2026-07-22/23. */
(function () {
  "use strict";
  var LANGS = [
    { code: "az", label: "Azərbaycan", short: "AZ" },
    { code: "ru", label: "Русский", short: "RU" },
    { code: "en", label: "English", short: "EN" },
    { code: "tr", label: "Türkçe", short: "TR" }
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
      ".lsw{position:relative;display:inline-block;vertical-align:middle;font:600 13px/1 system-ui,-apple-system,sans-serif}" +
      ".lsw-btn{display:inline-flex;align-items:center;gap:5px;padding:6px 10px;border-radius:8px;cursor:pointer;" +
      "background:#f2c94c;color:#1b3a5b;border:none;font:inherit;font-weight:700}" +
      ".lsw-btn:hover{background:#e8bf3e}" +
      ".lsw-btn svg{width:15px;height:15px;fill:currentColor}" +
      ".lsw-menu{position:absolute;top:calc(100% + 6px);right:0;min-width:140px;background:#fff;border-radius:10px;" +
      "box-shadow:0 6px 24px rgba(0,0,0,.18);padding:6px;z-index:9999;display:none}" +
      ".lsw.open .lsw-menu{display:block}" +
      ".lsw-menu a{display:flex;align-items:center;gap:8px;padding:9px 12px;border-radius:7px;text-decoration:none;" +
      "color:#1b3a5b;font-weight:600;white-space:nowrap}" +
      ".lsw-menu a:hover{background:#f5f6f8}" +
      ".lsw-menu a.on{background:#f2c94c;font-weight:700}" +
      ".lsw-menu a .code{font-size:11px;opacity:.6;margin-left:auto}";
    var st = document.createElement("style");
    st.id = "lang-switch-css"; st.textContent = css;
    document.head.appendChild(st);
  }

  var GLOBE = '<svg viewBox="0 0 24 24"><path d="M12 2a10 10 0 100 20 10 10 0 000-20zm6.9 6h-2.6a15.7 15.7 0 00-1.4-3.6A8 8 0 0118.9 8zM12 4c.8 1.2 1.5 2.5 1.9 4h-3.8c.4-1.5 1.1-2.8 1.9-4zM4.3 14a8 8 0 010-4h3a17.5 17.5 0 000 4h-3zm.8 2h2.6c.4 1.3.9 2.5 1.4 3.6A8 8 0 015.1 16zm2.6-8H5.1a8 8 0 013.9-3.6C8.4 5.5 7.9 6.7 7.7 8zM12 20c-.8-1.2-1.5-2.5-1.9-4h3.8c-.4 1.5-1.1 2.8-1.9 4zm2.3-6H9.7a15.5 15.5 0 010-4h4.6a15.5 15.5 0 010 4zm.6 5.6c.5-1.1 1-2.3 1.4-3.6h2.6a8 8 0 01-4 3.6zM16.7 14a17.5 17.5 0 000-4h3a8 8 0 010 4h-3z"/></svg>';

  function render() {
    var host = document.querySelector("[data-lang-switch]");
    if (!host) return;
    injectStyle();
    var info = build();
    var curL = LANGS.filter(function (L) { return L.code === info.cur; })[0] || LANGS[0];
    var items = LANGS.map(function (L) {
      var on = L.code === info.cur;
      var href = on ? "#" : info.urlFor(L.code);
      return '<a href="' + href + '"' + (on ? ' class="on" aria-current="page"' : "") +
        '>' + L.label + '<span class="code">' + L.short + '</span></a>';
    }).join("");
    host.className = "lsw";
    host.innerHTML = '<button type="button" class="lsw-btn" aria-haspopup="true" aria-label="Dil / Язык / Language">' +
      GLOBE + '<span>' + curL.short + '</span></button><div class="lsw-menu" role="menu">' + items + '</div>';
    var btn = host.querySelector(".lsw-btn");
    btn.addEventListener("click", function (e) {
      e.stopPropagation(); host.classList.toggle("open");
    });
    document.addEventListener("click", function () { host.classList.remove("open"); });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", render);
  } else {
    render();
  }
})();
