# -*- coding: utf-8 -*-
"""Автоматическая проверка ВСЕХ внутренних страниц test/11 (Chrome без окна).
На каждой странице, языке и ширине: ошибки сценариев, неоткрывшиеся файлы, выход за ширину экрана, битые картинки,
пустые блоки, «undefined/null» в тексте, число строк заголовка, мелкие области нажатия, битые внутренние ссылки.
Запуск из test/11 (сервер: python -m http.server 8812 из корня сайта):
  python _tools/pages_check.py            — все страницы
  python _tools/pages_check.py quick      — без статей блога
  python _tools/pages_check.py consult    — только адреса, где встречается слово
Код возврата 1, если есть нарушения. Отчёт: _agent/shots/pages_check.json"""
import asyncio, json, sys, subprocess, time, urllib.request, os, tempfile, glob, io
import websockets
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
BASE = os.environ.get("BASE", "http://localhost:8812/test/11/")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PORT = 9397
WIDTHS = [(360, 740), (390, 844), (1366, 768)]
LANGS = ["ru", "az", "en"]

JS = r"""
(async () => {
  const out = {};
  document.querySelectorAll('img[loading=lazy]').forEach(i => { i.loading = 'eager'; });
  document.querySelectorAll('.rv').forEach(e => e.classList.add('is-in'));
  await new Promise(r => setTimeout(r, 700));
  for (let k = 0; k < 30 && [...document.images].some(i => !i.complete); k++) await new Promise(r => setTimeout(r, 250));
  const W = __W__;                      /* заданная ширина экрана: при переполнении браузер сам расширяет окно просмотра */
  out.over = Math.max(document.documentElement.scrollWidth, document.body.scrollWidth) - W;
  const skip = e => e.closest('.tblw, .pg__cats, .mob, .lb, .nav__dd, .head');
  out.out = [...document.querySelectorAll('main *, footer *')].filter(e => { if (skip(e)) return false; const r = e.getBoundingClientRect(); return r.width > 0 && (r.right > W + 1 || r.left < -1); }).slice(0, 5).map(e => e.tagName + '.' + String(e.className).slice(0, 30));
  out.img = [...document.images].filter(i => i.complete && !i.naturalWidth && i.getAttribute('src')).map(i => i.getAttribute('src')).slice(0, 6);
  const h1 = document.querySelector('h1');
  out.h1 = h1 ? Math.round(h1.getBoundingClientRect().height / parseFloat(getComputedStyle(h1).lineHeight)) : 0;
  out.h1t = h1 ? h1.textContent.trim().slice(0, 60) : '';
  out.blocks = document.querySelectorAll('#pgBlocks > section').length;
  const txt = document.querySelector('main').innerText;
  out.bad = (txt.match(/\b(undefined|null|NaN|\[object Object\])\b/g) || []).slice(0, 4);
  out.raw = (txt.match(/<\/?(strong|em|a|br|p|span)\b[^>]{0,20}>|&(amp|nbsp|lt|gt|quot);/g) || []).slice(0, 4);
  out.empty = [...document.querySelectorAll('#pgBlocks .pg__bd')].filter(e => !e.innerText.trim() && !e.querySelector('img')).length;
  out.h2long = [...document.querySelectorAll('#pgBlocks .pp__h')].filter(e => e.getBoundingClientRect().height / parseFloat(getComputedStyle(e).lineHeight) > 4.2).map(e => e.textContent.slice(0, 40)).slice(0, 3);
  out.vw = innerWidth;
  out.tap = W < 700 ? [...document.querySelectorAll('main a.btn, main button, main summary')].filter(e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height < 43.5; }).slice(0, 4).map(e => e.tagName + '.' + String(e.className).slice(0, 24) + ' ' + Math.round(e.getBoundingClientRect().height)) : [];
  out.small = [...document.querySelectorAll('#pgBlocks p, #pgBlocks li, #pgBlocks span, #pgBlocks td')].filter(e => e.children.length === 0 && e.textContent.trim() && parseFloat(getComputedStyle(e).fontSize) < 12).slice(0, 3).map(e => e.className + ' ' + getComputedStyle(e).fontSize);
  out.links = [...new Set([...document.querySelectorAll('main a[href], footer a[href], #nav a[href]')].map(a => a.getAttribute('href')).filter(h => h && !/^(https?:|mailto:|tel:|#)/.test(h)))];
  out.lang = document.documentElement.lang; out.title = document.title;
  out.reg = !!document.querySelector('#regBox form');
  return out;
})()
"""


def pages(mode):
    ps = ["specialist.html?s=kenan", "specialist.html?s=samira", "contact.html", "corporate.html", "law.html", "blog.html"]
    ps += ["consult.html?c=" + os.path.basename(f).split(".")[0] for f in sorted(glob.glob(os.path.join(D, "data", "cons", "*.ru.json"))) if "index." not in f]
    ps += ["program.html?p=" + s for s in ["general", "clinical", "practicum", "psychodiagnostics", "cbt", "psychoanalysis", "family"]]
    if mode != "quick":
        ps += ["article.html?a=" + os.path.basename(f).split(".")[0] for f in sorted(glob.glob(os.path.join(D, "data", "blog", "*.ru.json"))) if "index." not in f]
    if mode not in ("", "quick"):
        ps = [p for p in ps if mode in p]
    return ps


async def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    prof = tempfile.mkdtemp()
    p = subprocess.Popen([CHROME, "--headless=new", "--remote-debugging-port=%d" % PORT, "--user-data-dir=" + prof, "--hide-scrollbars", "about:blank"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    ws_url = None
    for _ in range(60):
        try:
            tabs = json.load(urllib.request.urlopen("http://127.0.0.1:%d/json" % PORT))
            ws_url = [t for t in tabs if t["type"] == "page"][0]["webSocketDebuggerUrl"]
            break
        except Exception:
            time.sleep(.2)
    rep, bad_total, links = [], 0, {}
    try:
        async with websockets.connect(ws_url, max_size=80_000_000) as ws:
            n = [0]
            errs = []

            async def cmd(m, **pr):
                n[0] += 1
                i = n[0]
                await ws.send(json.dumps({"id": i, "method": m, "params": pr}))
                while True:
                    r = json.loads(await ws.recv())
                    if r.get("method") == "Runtime.exceptionThrown":
                        d = r["params"]["exceptionDetails"]
                        errs.append("EXC " + ((d.get("exception") or {}).get("description") or d.get("text") or "")[:160])
                    if r.get("method") == "Network.responseReceived":
                        rs = r["params"]["response"]
                        if rs["status"] >= 400 and "localhost" in rs["url"]:
                            errs.append("HTTP %d %s" % (rs["status"], rs["url"].split("/test/11/")[-1][:80]))
                    if r.get("method") == "Runtime.consoleAPICalled" and r["params"]["type"] == "error":
                        errs.append("CONSOLE " + json.dumps(r["params"]["args"][:1], ensure_ascii=False)[:160])
                    if r.get("id") == i:
                        return r.get("result", {})

            await cmd("Page.enable"); await cmd("Runtime.enable"); await cmd("Network.enable")
            await cmd("Page.navigate", url=BASE + "contact.html")
            await asyncio.sleep(1.5)
            for pg in pages(mode):
                art = pg.startswith("article")
                for lang in LANGS:
                    for (W, H) in (WIDTHS if not art else [(390, 844), (1366, 768)]):
                        errs.clear()
                        await cmd("Emulation.setDeviceMetricsOverride", width=W, height=H, deviceScaleFactor=1, mobile=W < 700)
                        await cmd("Runtime.evaluate", expression="localStorage.setItem('r11_lang','%s')" % lang)
                        await cmd("Page.navigate", url=BASE + pg)
                        await asyncio.sleep(1.1 if art else 1.5)
                        r = await cmd("Runtime.evaluate", expression=JS.replace("__W__", str(W)), returnByValue=True, awaitPromise=True)
                        o = r.get("result", {}).get("value") or {"fail": "нет ответа страницы"}
                        v = []
                        if o.get("fail"): v.append(o["fail"])
                        if errs: v.append("ошибки: " + "; ".join(sorted(set(errs))[:4]))
                        if o.get("vw", W) > W + 1: v.append("страница раздвинута до %d px" % o["vw"])
                        if o.get("over", 0) > 1: v.append("шире экрана на %d px" % o["over"])
                        if o.get("out"): v.append("за краем: " + ", ".join(o["out"]))
                        if o.get("img"): v.append("битые картинки: " + ", ".join(o["img"]))
                        if not pg.startswith("program") and o.get("blocks", 0) < 1: v.append("нет блоков")
                        if o.get("bad"): v.append("мусор в тексте: " + ",".join(o["bad"]))
                        if o.get("raw"): v.append("сырая разметка: " + ",".join(o["raw"]))
                        if o.get("empty"): v.append("пустых блоков: %d" % o["empty"])
                        if o.get("h1", 0) > (4 if W < 700 else 3): v.append("заголовок в %d строк: %s" % (o["h1"], o.get("h1t")))
                        if o.get("h1", 0) == 0: v.append("нет заголовка")
                        if o.get("h2long"): v.append("длинный заголовок раздела: " + " | ".join(o["h2long"]))
                        if o.get("tap"): v.append("мелкая область нажатия: " + ", ".join(o["tap"]))
                        if o.get("small"): v.append("мелкий текст: " + ", ".join(o["small"]))
                        if o.get("lang") != lang: v.append("язык страницы %s" % o.get("lang"))
                        if not o.get("reg"): v.append("нет формы записи")
                        for h in o.get("links", []):
                            links.setdefault(h, pg)
                        rep.append({"page": pg, "lang": lang, "w": W, "viol": v, "h1": o.get("h1"), "blocks": o.get("blocks")})
                        bad_total += len(v)
                        if v:
                            print("✗ %-42s %s %4d: %s" % (pg, lang, W, " ‖ ".join(v)))
            # внутренние ссылки: файл должен существовать, параметр — указывать на существующие данные
            for h, where in sorted(links.items()):
                path, _, qs = h.partition("?")
                path = path.split("#")[0]
                ok = True
                if path.startswith("/"):
                    ok = os.path.exists(os.path.join(D, "..", "..", path.lstrip("/"))) or os.path.exists(os.path.join(D, "..", "..", path.lstrip("/"), "index.html"))
                elif path:
                    ok = os.path.isfile(os.path.join(D, path))
                if ok and qs:
                    k, _, val = qs.split("#")[0].partition("=")
                    dirn = {"s": "spec", "c": "cons", "a": "blog"}.get(k)
                    if dirn:
                        ok = bool(glob.glob(os.path.join(D, "data", dirn, val + ".*.json")))
                if not ok:
                    bad_total += 1
                    print("✗ битая ссылка: %s (на %s)" % (h, where))
    finally:
        p.terminate()
    json.dump(rep, io.open(os.path.join(D, "_agent", "shots", "pages_check.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print("ПРОВЕРЕНО: %d сочетаний, ссылок: %d, НАРУШЕНИЙ: %d" % (len(rep), len(links), bad_total))
    sys.exit(1 if bad_total else 0)


asyncio.run(main())
