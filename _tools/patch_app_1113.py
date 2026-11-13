# -*- coding: utf-8 -*-
"""Приложение RAGIMOFF (13.11.2026): описание приложения и значки в каждой странице, модуль app.js в рамке сайта,
стили плашки установки, ярлыки приложения на новые адреса. Повторный запуск ничего не меняет."""
import glob, io, json, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(D)


def patch(p, pairs):
    s = io.open(p, encoding="utf-8").read()
    o = s
    for a, b in pairs:
        if b in s:
            continue
        assert s.count(a) == 1, (p, a[:60], s.count(a))
        s = s.replace(a, b)
    if s != o:
        io.open(p + ".new", "w", encoding="utf-8", newline="\n").write(s)
        os.replace(p + ".new", p)
        print("исправлен", p)


HEADL = ('<meta name="theme-color" content="#07090E">\n'
         '<link rel="manifest" href="/app.webmanifest"><link rel="apple-touch-icon" href="/favicons/android-chrome-192x192.png">'
         '<meta name="apple-mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-title" content="RAGIMOFF">')
for p in sorted(glob.glob("*.html")):
    s = io.open(p, encoding="utf-8").read()
    if '<meta name="theme-color" content="#07090E">' in s and 'rel="manifest"' not in s:
        patch(p, [('<meta name="theme-color" content="#07090E">', HEADL)])

APP = "import { initApp } from './app.js?v=11131300';\n"
patch("assets/js/chrome.js", [
    ("import { initSeo, switchLang } from './seo.js", APP + "import { initSeo, switchLang } from './seo.js"),
    ("  initSeo(() => lang);\n  return { render, watch", "  initSeo(() => lang); initApp(() => lang);\n  return { render, watch"),
])
patch("assets/js/site.js", [
    ("import { initSeo, switchLang } from './seo.js", APP + "import { initSeo, switchLang } from './seo.js"),
    ("render(); cineLoad(); initSeo(() => lang);", "render(); cineLoad(); initSeo(() => lang); initApp(() => lang);"),
])

CSS = """
/* APP (13.11): плашка «Приложение RAGIMOFF» — сверху по центру, выезжает и уходит; показ — app.js (не навязчиво) */
.app-bar { position: fixed; left: 50%; top: .75rem; z-index: 1000; display: flex; align-items: center; gap: .875rem; width: min(35rem, calc(100vw - 1.5rem));
  padding: .75rem .75rem .75rem .875rem; border-radius: 1.125rem; background: color-mix(in srgb, var(--bg) 94%, transparent); border: 1px solid color-mix(in srgb, var(--gold) 35%, transparent);
  box-shadow: var(--shadow); backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px); transform: translate(-50%, -140%); transition: transform .55s var(--e); }
.app-bar.is-in { transform: translate(-50%, 0); }
.app-bar__ico { position: relative; flex: 0 0 auto; width: 2.75rem; height: 2.75rem; border-radius: .75rem; background: #061826; color: #fff; display: grid; place-items: center; font: 800 1.5rem/1 var(--f-text); }
.app-bar__ico i { position: absolute; right: .45rem; bottom: .55rem; width: .45rem; height: .45rem; border-radius: 50%; background: var(--gold); }
.app-bar__txt { display: flex; flex-direction: column; gap: .125rem; min-width: 0; flex: 1; }
.app-bar__txt b { font: 600 .95rem/1.3 var(--f-text); color: var(--milk); }
.app-bar__txt small { font: 400 .85rem/1.4 var(--f-read); color: var(--txt); }
.app-bar__go { flex: 0 0 auto; min-height: var(--tap, 2.75rem); padding: 0 1.1rem; border: 0; border-radius: 99px; background: var(--gold); color: var(--on-gold); font: 500 .95rem/1 var(--f-read); cursor: pointer; }
.app-bar__x { flex: 0 0 auto; width: var(--tap, 2.75rem); height: var(--tap, 2.75rem); border: 0; border-radius: 50%; background: transparent; color: var(--smoke); font-size: 1.4rem; cursor: pointer; }
@media (prefers-reduced-motion: reduce) { .app-bar { transition: none; } }
"""
p = "assets/css/site.css"
s = io.open(p, encoding="utf-8").read()
if ".app-bar {" not in s:
    io.open(p + ".new", "w", encoding="utf-8", newline="\n").write(s.rstrip("\n") + "\n" + CSS)
    os.replace(p + ".new", p)
    print("исправлен", p)

p = "app.webmanifest"
m = json.load(io.open(p, encoding="utf-8"))
new = [{"name": "Kitablar", "url": "/az/shop.html"}, {"name": "Konsultasiya", "url": "/az/consult.html"}, {"name": "Təhsil", "url": "/az/program-general.html"}]
if m.get("shortcuts") != new:
    m["shortcuts"] = new
    io.open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(m, ensure_ascii=False, indent=1))
    print("исправлен", p)
print("готово")
