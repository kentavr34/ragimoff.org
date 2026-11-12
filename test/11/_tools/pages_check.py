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
  const skip = e => e.closest('.shp__chips, .gal--docs, .tblw, .pg__cats, .mob, .lb, .nav__dd, .head, .cine, .belt, .rib, .shelf, .rail, [data-rail]');
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
  /* ряд карточек: у карточек одного ряда одна высота, а нижние элементы (линия с ценой, кнопка) стоят на одном уровне */
  out.rows = [];
  [...document.querySelectorAll('main *')].forEach(p => {
    const ch = [...p.children].filter(c => c.getBoundingClientRect().width > 0);
    if (ch.length < 2 || !ch[0].className || ch.some(c => c.className !== ch[0].className || c.children.length < 2)) return;
    const d = getComputedStyle(p).display; if (d.indexOf('grid') < 0 && d.indexOf('flex') < 0) return;
    const rows = {}; ch.forEach(c => { const r = c.getBoundingClientRect(); (rows[Math.round(r.top / 4)] = rows[Math.round(r.top / 4)] || []).push(c); });
    Object.values(rows).forEach(g => { if (g.length < 2) return;
      const hs = g.map(c => Math.round(c.getBoundingClientRect().height));
      const sig = c => { const r = c.getBoundingClientRect(), k = [...c.children].filter(x => x.getBoundingClientRect().height > 0 && (x.matches('.btn, button, a.btn') || parseFloat(getComputedStyle(x).borderTopWidth) > 0)); return k.slice(-2).map(x => String(x.className).split(' ')[0] + ':' + Math.round(x.getBoundingClientRect().top - r.top)); };
      const names = g.map(c => sig(c).map(x => x.split(':')[0]).join()), tops = g.map(c => sig(c).map(x => +x.split(':')[1]));
      if (Math.max(...hs) - Math.min(...hs) > 2) out.rows.push(String(ch[0].className).split(' ')[0] + ' высоты ' + hs.join('/'));
      else if (new Set(names).size === 1 && tops[0].length && tops[0].some((_, i) => Math.max(...tops.map(t => t[i])) - Math.min(...tops.map(t => t[i])) > 2)) out.rows.push(String(ch[0].className).split(' ')[0] + ' низ ' + tops.map(t => t.join('+')).join(' / '));
    });
  });
  out.rows = [...new Set(out.rows)].slice(0, 4);
  /* номер телефона не должен рваться по строкам: либо неразрывные пробелы, либо .nw */
  out.tel = []; { const tw = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n; while ((n = tw.nextNode())) { if (/\+\d[\d ]*\d \d/.test(n.nodeValue) && /\+\d[\d ]{8,16}\d/.test(n.nodeValue) && !n.parentElement.closest('.nw, script, style')) out.tel.push(n.nodeValue.trim().slice(0, 50)); } out.tel = out.tel.slice(0, 3); }
  out.top = !!document.querySelector('#toTop');
  const ps = [...document.querySelectorAll('#posts > *')]; out.postsRow = W >= 1000 && ps.length > 1 ? new Set(ps.map(x => Math.round(x.getBoundingClientRect().top))).size : 1;
  /* замок: устройство каждого раздела (сколько карточек, во сколько колонок, какой ширины) — сверяется с согласованным снимком */
  out.lock = {};
  [...document.querySelectorAll('main > section, #pgBlocks > section')].forEach((sec, si) => {
    let best = null, bn = 0;
    [sec, ...sec.querySelectorAll('*')].forEach(p => { const ch = [...p.children].filter(c => c.getBoundingClientRect().width > 0 && c.className); if (ch.length >= 2 && ch.every(c => String(c.className).split(' ')[0] === String(ch[0].className).split(' ')[0]) && ch.length > bn) { best = p; bn = ch.length; } });
    const key = sec.id || ('b' + si + '.' + String(sec.className).replace(/\s*(sec|is-in|rv)\b/g, '').trim().split(' ').pop());
    const h = sec.querySelector('h2');
    const o = { h2: h ? Math.round(parseFloat(getComputedStyle(h).fontSize)) : 0 };
    if (best) { const ch = [...best.children].filter(c => c.getBoundingClientRect().width > 0); const r0 = ch[0].getBoundingClientRect();
      o.box = String(ch[0].className).split(' ')[0]; o.n = ch.length; o.cols = new Set(ch.map(c => Math.round(c.getBoundingClientRect().left / 8))).size; o.rows = new Set(ch.map(c => Math.round(c.getBoundingClientRect().top / 8))).size; o.w = Math.round(r0.width / W * 20) * 5; }
    out.lock[key] = o;
  });
  return out;
})()
"""


# Замок согласованного (требование владельца 12.11.2026): устройство разделов этих страниц записано в _agent/lock/layout.json.
# Любое расхождение — нарушение; принять намеренное изменение можно только явной командой: python pages_check.py accept
LOCKED = ["index.html", "specialist.html?s=kenan", "contact.html", "corporate.html", "blog.html", "consult.html?c=enurez", "consult.html?c=panik-ataklar", "program.html?p=general", "program.html?p=cbt"]
LOCKF = os.path.join(D, "_agent", "lock", "layout.json")
LOCK = json.load(io.open(LOCKF, encoding="utf-8")) if os.path.exists(LOCKF) else {}
NEWLOCK = {}


def pages(mode):
    if mode == "accept":
        return LOCKED
    ps = ["index.html", "shop.html", "book.html?b=klinik", "book.html?b=art-freud-gw02", "specialist.html?s=kenan", "specialist.html?s=samira", "contact.html", "corporate.html", "blog.html"]
    ps += ["consult.html?c=" + os.path.basename(f).split(".")[0] for f in sorted(glob.glob(os.path.join(D, "data", "cons", "*.ru.json"))) if "index." not in f]
    ps += ["program.html?p=" + s for s in ["general", "clinical", "practicum", "psychodiagnostics", "cbt", "psychoanalysis", "family"]]
    if mode != "quick":
        ps += ["article.html?a=" + os.path.basename(f).split(".")[0] for f in sorted(glob.glob(os.path.join(D, "data", "blog", "*.ru.json"))) if "index." not in f]
    if mode not in ("", "quick", "accept"):
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
                        if o.get("out") and not pg.startswith("index"): v.append("за краем: " + ", ".join(o["out"]))
                        if o.get("rows"): v.append("ряд карточек не выровнен: " + "; ".join(o["rows"]))
                        if o.get("tel"): v.append("номер телефона может разорваться: " + "; ".join(o["tel"]))
                        if o.get("top") is False: v.append("нет кнопки «наверх»")
                        if o.get("postsRow", 1) > 1: v.append("блог на главной не в один ряд")
                        lk = "%s|%s|%d" % (pg, lang, W)
                        if lang == "ru" and W != 360 and (pg in LOCKED):
                            NEWLOCK[lk] = o.get("lock", {})
                            base = LOCK.get(lk)
                            if base is not None and mode != "accept":
                                for sec in sorted(set(base) | set(NEWLOCK[lk])):
                                    a, b = base.get(sec), NEWLOCK[lk].get(sec)
                                    if a != b:
                                        v.append("ЗАМОК: согласованный раздел «%s» изменился: было %s → стало %s (намеренно — python pages_check.py accept)" % (sec, json.dumps(a, ensure_ascii=False), json.dumps(b, ensure_ascii=False)))
                        if o.get("img"): v.append("битые картинки: " + ", ".join(o["img"]))
                        if not pg.startswith(("program", "index", "shop", "book")) and o.get("blocks", 0) < 1: v.append("нет блоков")
                        if o.get("bad"): v.append("мусор в тексте: " + ",".join(o["bad"]))
                        if o.get("raw"): v.append("сырая разметка: " + ",".join(o["raw"]))
                        if o.get("empty"): v.append("пустых блоков: %d" % o["empty"])
                        if o.get("h1", 0) > (4 if W < 700 else 3): v.append("заголовок в %d строк: %s" % (o["h1"], o.get("h1t")))
                        if o.get("h1", 0) == 0: v.append("нет заголовка")
                        if o.get("h2long"): v.append("длинный заголовок раздела: " + " | ".join(o["h2long"]))
                        if o.get("tap"): v.append("мелкая область нажатия: " + ", ".join(o["tap"]))
                        if o.get("small"): v.append("мелкий текст: " + ", ".join(o["small"]))
                        if o.get("lang") != lang: v.append("язык страницы %s" % o.get("lang"))
                        if not o.get("reg") and not pg.startswith(("shop", "book")): v.append("нет формы записи")
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
    if mode == "accept" or not LOCK:
        os.makedirs(os.path.dirname(LOCKF), exist_ok=True)
        LOCK.update(NEWLOCK)
        json.dump(LOCK, io.open(LOCKF, "w", encoding="utf-8"), ensure_ascii=False, indent=0, sort_keys=True)
        print("ЗАМОК: снимок согласованного состояния записан (%d страниц × ширин)" % len(NEWLOCK))
    print("ПРОВЕРЕНО: %d сочетаний, ссылок: %d, НАРУШЕНИЙ: %d" % (len(rep), len(links), bad_total))
    sys.exit(1 if bad_total else 0)


asyncio.run(main())
