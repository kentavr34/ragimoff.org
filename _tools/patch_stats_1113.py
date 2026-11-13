# -*- coding: utf-8 -*-
"""Своя статистика (13.11.2026): stats.js в рамке сайта и на главной; заявка и оплата сообщают событие rgm:stat;
страница заказа книг (books/, без модулей) шлёт просмотр и переход к оплате сама. Повторный запуск ничего не меняет."""
import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(D)


def patch(p, pairs):
    s = io.open(p, encoding="utf-8").read()
    o = s
    for a, b in pairs:
        if b in s:
            continue
        assert s.count(a) == 1, (p, a[:70], s.count(a))
        s = s.replace(a, b)
    if s != o:
        io.open(p + ".new", "w", encoding="utf-8", newline="\n").write(s)
        os.replace(p + ".new", p)
        print("исправлен", p)


IMP = "import { initStats } from './stats.js?v=11131700';\n"
patch("assets/js/chrome.js", [
    ("import { initApp } from './app.js", IMP + "import { initApp } from './app.js"),
    ("  initSeo(() => lang); initApp(() => lang);\n", "  initSeo(() => lang); initApp(() => lang); initStats(() => lang);\n"),
])
patch("assets/js/site.js", [
    ("import { initApp } from './app.js", IMP + "import { initApp } from './app.js"),
    ("initSeo(() => lang); initApp(() => lang);", "initSeo(() => lang); initApp(() => lang); initStats(() => lang);"),
])
# форма записи: заявка принята — событие reg; переход к оплате обучения — pay
patch("assets/js/reg.js", [
    ("    .then(x => x.ok ? x.json().catch(() => ({ ok: true })) : null, () => null);\n",
     "    .then(x => x.ok ? x.json().catch(() => ({ ok: true })) : null, () => null);\n"
     "  if (reg) dispatchEvent(new CustomEvent('rgm:stat', { detail: { t: 'reg', x: 'reg:' + (payload.service || payload.kind || k || '') } }));   /* статистика 13.11 */\n"),
    (".then(d => { if (d && d.ok && d.redirect_url) { location.href = d.redirect_url; return; }",
     ".then(d => { if (d && d.ok && d.redirect_url) { dispatchEvent(new CustomEvent('rgm:stat', { detail: { t: 'pay', x: 'pay:training' } })); location.href = d.redirect_url; return; }"),
])
# страница заказа книг: свой маленький отправитель (те же номера посетителя и визита, что у stats.js)
B = """  /* 13.11.2026: статистика сайта (как assets/js/stats.js): просмотр страницы заказа и переход к оплате */
  function rgmStat(t, x) {
    if (!/(^|\\.)ragimoff\\.org$/.test(location.hostname) || navigator.webdriver) return;
    try {
      var v = localStorage.getItem('rgm_vid') || (Math.random().toString(36).slice(2, 10) + Date.now().toString(36));
      localStorage.setItem('rgm_vid', v);
      var s = sessionStorage.getItem('rgm_sid') || (Math.random().toString(36).slice(2, 10) + Date.now().toString(36));
      sessionStorage.setItem('rgm_sid', s);
      var e = { t: t, v: v, s: s, p: location.pathname + location.search, l: document.documentElement.lang || 'az', x: x || '' };
      if (t === 'pv') { e.r = document.referrer || ''; e.d = innerWidth < 700 ? 'mob' : innerWidth < 1100 ? 'tab' : 'desk'; }
      navigator.sendBeacon('https://api.ragimoff.org/api/s', new Blob([JSON.stringify([e])], { type: 'text/plain' }));
    } catch (er) {}
  }
  rgmStat('pv');
"""
patch("books/books.js", [
    ("  var PAY_API = 'https://api.ragimoff.org/api/billing/epoint/create';\n",
     "  var PAY_API = 'https://api.ragimoff.org/api/billing/epoint/create';\n" + B),
    ("        fetch(PAY_API, {", "        rgmStat('pay', 'pay:books');\n        fetch(PAY_API, {"),
])
print("готово")
