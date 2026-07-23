/* Переключатель языков AZ/RU/EN/TR (ragimoff.org). Вычисляет ссылки на языковые версии
   ТЕКУЩЕЙ страницы из URL — одна разметка на всех языках, не требует переписывания при inject.
   Самодостаточные стили (высокий контраст, видно и кликается на любом фоне). Кенан 2026-07-22/23.
   Использование: <div class="lang-switch-bar" data-lang-switch></div> + <script src="/_lang-switch.js" defer>. */
(function () {
  "use strict";
  var LANGS = [
    { code: "az", label: "AZ", aria: "Azərbaycanca" },
    { code: "ru", label: "RU", aria: "Русская версия" },
    { code: "en", label: "EN", aria: "English" },
    { code: "tr", label: "TR", aria: "Türkçe" }
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
      ".lang-switch-bar{display:inline-flex;gap:4px;align-items:center;vertical-align:middle}" +
      ".lang-switch-bar a.ls{display:inline-block;min-width:30px;padding:3px 8px;border-radius:6px;" +
      "font:600 12px/1.2 system-ui,sans-serif;text-decoration:none;text-align:center;" +
      "background:#fff;color:#1b3a5b;border:1px solid rgba(0,0,0,.18);transition:all .15s}" +
      ".lang-switch-bar a.ls:hover{background:#f2c94c;color:#1b3a5b;border-color:#f2c94c}" +
      ".lang-switch-bar a.ls.ls-active{background:#f2c94c;color:#1b3a5b;border-color:#f2c94c;cursor:default;font-weight:700}";
    var st = document.createElement("style");
    st.id = "lang-switch-css"; st.textContent = css;
    document.head.appendChild(st);
  }

  function render() {
    var host = document.querySelector("[data-lang-switch]");
    if (!host) return;
    injectStyle();
    var info = build();
    var html = "";
    LANGS.forEach(function (L) {
      var active = L.code === info.cur;
      var href = active ? "#" : info.urlFor(L.code);
      html += '<a href="' + href + '" class="ls' + (active ? " ls-active" : "") +
        '" aria-label="' + L.aria + '"' + (active ? ' aria-current="page"' : "") + ">" + L.label + "</a>";
    });
    host.classList.add("lang-switch-bar");
    host.innerHTML = html;
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", render);
  } else {
    render();
  }
})();
