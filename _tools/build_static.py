# -*- coding: utf-8 -*-
"""build_static.py — постоянные страницы сайта на каждом языке для поисковиков, ИИ-моделей и превью ссылок (13.11.2026).

Слово Кенана: ссылка в WhatsApp показывала превью по-русски; сайт должен открываться и показываться на языке посетителя
(по умолчанию — азербайджанский), а все страницы, включая книги и главы книг, — находиться поисковиками и ИИ (ChatGPT,
Claude, DeepSeek, Qwen…). Эти боты не выполняют JavaScript, поэтому текст должен быть в самом HTML.

Что делает:
  • /az/, /ru/, /en/ — снимок каждой страницы (как её рисует браузер) с готовым текстом; главы книг — из шаблона читалки
    и готового текста главы (books/<книга>/<язык>/NNN.html), только на языках, на которых книга есть;
  • в каждой: <html lang>, title, description, canonical, hreflang (+x-default = AZ), Open Graph и Twitter (превью),
    разметка schema.org (Organization, WebSite, Person, Book + Offer, Course, Article, Chapter) — только то, что есть на странице;
  • в шаблонах корня (index.html, book.html …) — тот же блок по-азербайджански (превью ragimoff.org — на AZ, canonical → /az/);
  • assets/js/seo-map.js (языки книг), sitemap.xml (все адреса с языковыми парами), robots.txt (боты ИИ разрешены), llms.txt.
Блоки в <head> стоят между <!--seo--> и <!--/seo-->: повторный запуск их заменяет.
Нужен локальный сервер из корня сайта: python -m http.server 8812.
  python _tools/build_static.py            # всё
  python _tools/build_static.py pages      # только страницы (без глав)
  python _tools/build_static.py chapters   # только главы"""
import asyncio, glob, html, io, json, os, re, shutil, subprocess, sys, tempfile, time, urllib.request
import websockets
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(D)
SITE = "https://ragimoff.org"
BASE = os.environ.get("BASE", "http://localhost:8812/")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PORT = 9398
LANGS = ["az", "ru", "en"]
LOCALE = {"az": "az_AZ", "ru": "ru_RU", "en": "en_US"}
OG_DEFAULT = "/assets/img/og/ragimoff.jpg"
mode = sys.argv[1] if len(sys.argv) > 1 else "all"
jl = lambda p: json.load(io.open(p, encoding="utf-8"))
E = lambda s: html.escape(str(s or ""), quote=True)


def write(p, s):
    os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
    if os.path.exists(p) and io.open(p, encoding="utf-8").read() == s:
        return 0
    io.open(p + ".new", "w", encoding="utf-8", newline="\n").write(s)
    os.replace(p + ".new", p)
    return 1


def clip(t, n=158):
    t = re.sub(r"\s+", " ", t or "").strip()
    if len(t) <= n:
        return t
    t = t[:n].rsplit(" ", 1)[0].rstrip(",;:—-– ")
    return t + "…"


# ---------- книги: паспорта, языки, каталог
BOOKS = {}
for b in jl("books/index.json")["books"]:
    P = jl("books/%s/book.json" % b["id"])
    if P.get("merged"):
        continue
    BOOKS[b["id"]] = P
BOOK_LANGS = {k: [l for l in P["langs"] if l in LANGS] or ["az"] for k, P in BOOKS.items()}
SHOP = {l: jl("data/shop/index.%s.json" % l) for l in LANGS}
ITEMS = {l: {it["id"]: dict(it, g=g["name"], gid=g["id"]) for g in SHOP[l]["groups"] for it in g["items"]} for l in LANGS}
FACTS = jl("_tools/shop_facts.json") if os.path.exists("_tools/shop_facts.json") else {}


# ---------- описания: главные страницы — написаны вручную; книги — из сведений каталога
DESC = {
    "index": {"az": "Doctor Ragimoff — psixiatr-psixoterapevt Kənan Rəhimovun psixologiya məktəbi (Bakı): psixoterapiya və konsultasiyalar, psixoloq təhsili, təlimlər, kitablar, Freydin əsərləri Azərbaycan dilində.",
              "ru": "Doctor Ragimoff — школа психологии психиатра-психотерапевта Кенана Рагимова (Баку): психотерапия и консультации, обучение психологов, тренинги, книги, Фрейд на азербайджанском.",
              "en": "Doctor Ragimoff — the school of psychology of psychiatrist and psychotherapist Kenan Ragimov in Baku: psychotherapy, consultations, psychologist training, books, Freud in Azerbaijani."},
    "blog": {"az": "Psixiatr və psixoterapevtin psixi sağlamlıq, münasibətlər və psixoterapiya haqqında məqalələri — Doctor Ragimoff bloqu.",
             "ru": "Статьи психиатра и психотерапевта о психическом здоровье, отношениях и психотерапии — блог Doctor Ragimoff.",
             "en": "Articles by a psychiatrist and psychotherapist on mental health, relationships and psychotherapy — the Doctor Ragimoff blog."},
    "contact": {"az": "Doctor Ragimoff ilə əlaqə: konsultasiyaya yazılış, təhsil və təlimlər haqqında suallar — telefon, WhatsApp, ünvan (Bakı).",
                "ru": "Контакты Doctor Ragimoff: запись на консультацию, вопросы об обучении и тренингах — телефон, WhatsApp, адрес в Баку.",
                "en": "Contact Doctor Ragimoff: book a consultation, ask about training and courses — phone, WhatsApp, address in Baku."},
}
FT = {}
try:
    FT = {v["az"]: v for v in json.load(io.open("D:/Projects/Freud/tools/print/series_titles.json", encoding="utf-8")).values()}
except Exception:
    pass
PAGE_W = {"az": "səh.", "ru": "стр.", "en": "pp."}
FREE = {"az": "Pulsuz onlayn oxuyun və ya çap nüsxəsini sifariş edin.", "ru": "Читайте бесплатно онлайн или закажите печатную книгу.", "en": "Read free online or order a printed copy."}
FREUD_AZ = {"az": "Ziqmund Freyd, Azərbaycan dilində tərcümə", "ru": "Зигмунд Фрейд, перевод на азербайджанский язык", "en": "Sigmund Freud, translated into Azerbaijani"}


def book_desc(bid, lang):
    it = ITEMS[lang].get(bid) or ITEMS["az"].get(bid) or {}
    f = FACTS.get(bid, {})
    pg = (f.get("pages") or {}).get(lang) or (f.get("pages") or {}).get("az")
    meta = " %s · %s %s." % (f.get("year", ""), pg, PAGE_W[lang]) if pg else ""
    if bid.startswith("freud"):
        az_t = (ITEMS["az"].get(bid) or {}).get("t", "")
        sub = (FT.get(az_t) or {}).get("sub", "") if lang == "az" else ""
        return "%s — %s.%s%s %s" % (it.get("t", ""), FREUD_AZ[lang], (" " + sub + ".") if sub else "", meta, FREE[lang])
    f0 = (it.get("f") or [""])[0]
    return "%s — %s. %s%s %s" % (it.get("t", ""), it.get("g", ""), f0, meta, FREE[lang])


# ---------- адреса: ссылка шаблона → адрес снимка (тот же порядок, что assets/js/seo.js)
def static_href(h, lang):
    if not h or re.match(r"^(https?:|mailto:|tel:|//|javascript:|#)", h):
        return None
    m = re.match(r"^([\w-]*\.html)?(\?[^#]*)?(#.*)?$", h.lstrip("/"))
    if not m:
        return None
    page = (m.group(1) or "index.html")[:-5]
    q = dict(re.findall(r"([\w]+)=([^&]*)", (m.group(2) or "").lstrip("?").replace("&amp;", "&")))
    hs = m.group(3) or ""
    P = lambda s: "/%s/%s.html%s" % (lang, s, hs)
    if page == "index":
        return None if m.group(2) else "/%s/%s" % (lang, hs)
    if page in ("shop", "blog", "contact", "corporate", "test"):
        return None if m.group(2) else P(page)
    if page == "program":
        return P("program-" + (q.get("p") or "general"))
    if page == "specialist":
        return P("specialist-" + q["s"]) if q.get("s") else None
    if page == "consult":
        c = q.get("c")
        return P("consult") if not c or c == "index" else P("consult-" + c)
    if page == "article":
        return P("article-" + q["a"]) if q.get("a") else None
    if page == "book":
        return P("book-" + q["b"]) if q.get("b") in BOOK_LANGS else None
    if page == "read":
        b = q.get("b")
        if not b or b not in BOOK_LANGS:
            return None
        L = lang if lang in BOOK_LANGS[b] else BOOK_LANGS[b][0]
        return "/%s/read/%s/%s.html%s" % (L, b, q.get("p") or q.get("c") or "index", hs)
    return None


def relink(s, lang):
    def rep(m):
        n = static_href(html.unescape(m.group(2)), lang)
        return m.group(1) + E(n) + m.group(3) if n else m.group(0)
    return re.sub(r'(<a\b[^>]*?\bhref=")([^"]*)(")', rep, s)


# ---------- список страниц (без глав)
slugs = lambda sec, lang: sorted(set(os.path.basename(f).split(".")[0] for f in glob.glob("data/%s/*.%s.json" % (sec, lang))))
progs = re.findall(r"'([\w-]+)'", re.search(r"order:\s*\[([^\]]*)\]", io.open("assets/js/programs.js", encoding="utf-8").read()).group(1))


def page_list():
    out = []   # (url шаблона, slug снимка, тип, [языки])
    for u, s in (("index.html", "index"), ("shop.html", "shop"), ("blog.html", "blog"), ("contact.html", "contact"), ("corporate.html", "corporate"),
                 ("test.html", "test"), ("consult.html?c=index", "consult")):
        out.append((u, s, s, LANGS))
    out += [("program.html?p=" + p, "program-" + p, "program", LANGS) for p in progs]
    for s in sorted(set(slugs("spec", "az")) | set(slugs("spec", "ru"))):
        out.append(("specialist.html?s=" + s, "specialist-" + s, "specialist", [l for l in LANGS if os.path.exists("data/spec/%s.%s.json" % (s, l))]))
    for s in sorted(set(sum([slugs("cons", l) for l in LANGS], []))):
        if s != "index":
            out.append(("consult.html?c=" + s, "consult-" + s, "consult", [l for l in LANGS if os.path.exists("data/cons/%s.%s.json" % (s, l))]))
    for s in sorted(set(sum([slugs("blog", l) for l in LANGS], []))):
        if s != "index":
            out.append(("article.html?a=" + s, "article-" + s, "article", [l for l in LANGS if os.path.exists("data/blog/%s.%s.json" % (s, l))]))
    for b in BOOKS:
        if b in ITEMS["az"]:
            out.append(("book.html?b=" + b, "book-" + b, "book", LANGS))
    return out


def url_of(slug, lang):
    return "%s/%s/" % (SITE, lang) if slug == "index" else "%s/%s/%s.html" % (SITE, lang, slug)


# ---------- разметка schema.org
ORG = {"@type": "Organization", "@id": SITE + "/#org", "name": "Doctor Ragimoff", "url": SITE + "/", "logo": SITE + "/assets/img/og/ragimoff.jpg"}
KENAN = {"az": "Kənan Rəhimov", "ru": "Кенан Рагимов", "en": "Kenan Ragimov"}


def person(lang, desc="", img=""):
    p = {"@type": "Person", "@id": SITE + "/#kenan", "name": KENAN[lang], "alternateName": [v for k, v in KENAN.items() if k != lang],
         "url": url_of("specialist-kenan", lang), "jobTitle": {"az": "Psixiatr, psixoterapevt", "ru": "Психиатр, психотерапевт", "en": "Psychiatrist, psychotherapist"}[lang],
         "worksFor": {"@id": SITE + "/#org"}, "address": {"@type": "PostalAddress", "addressLocality": "Bakı" if lang == "az" else ("Баку" if lang == "ru" else "Baku"), "addressCountry": "AZ"}}
    if desc:
        p["description"] = desc
    if img:
        p["image"] = img
    return p


def jsonld(kind, slug, lang, o):
    url = url_of(slug, lang)
    g = [dict(ORG), {"@type": "WebSite", "@id": SITE + "/#site", "url": SITE + "/", "name": "Doctor Ragimoff", "inLanguage": ["az", "ru", "en"], "publisher": {"@id": SITE + "/#org"}}]
    page = {"@type": "WebPage", "@id": url, "url": url, "name": o["title"], "description": o["desc"], "inLanguage": lang, "isPartOf": {"@id": SITE + "/#site"}}
    if kind == "index":
        g.append(person(lang))
    elif kind == "specialist":
        if slug.endswith("kenan"):
            g.append(person(lang, o["desc"], o["img"]))
            page["mainEntity"] = {"@id": SITE + "/#kenan"}
        else:
            g.append({"@type": "Person", "name": o["h1"], "description": o["desc"], "image": o["img"], "url": url, "worksFor": {"@id": SITE + "/#org"}})
    elif kind == "book":
        bid = slug[5:]
        it = ITEMS[lang].get(bid) or ITEMS["az"][bid]
        f = FACTS.get(bid, {})
        bk = {"@type": "Book", "@id": url + "#book", "name": it["t"], "author": {"@type": "Person", "name": it.get("a", "").title() or it["g"]},
              "inLanguage": BOOK_LANGS.get(bid, ["az"]), "bookFormat": "https://schema.org/Paperback", "image": o["img"], "url": url,
              "publisher": {"@id": SITE + "/#org"}}
        if f.get("pages"):
            bk["numberOfPages"] = f["pages"].get(lang) or f["pages"].get("az")
        if f.get("year"):
            bk["datePublished"] = str(f["year"])
        if it.get("price") and (lang in BOOK_LANGS.get(bid, ["az"]) or not bid.startswith("freud")):
            pr = re.match(r"(\d+)", it["price"])
            if pr:
                bk["offers"] = {"@type": "Offer", "price": pr.group(1), "priceCurrency": "AZN", "availability": "https://schema.org/InStock", "url": url}
        if it.get("read"):
            bk["workExample"] = {"@type": "Book", "bookFormat": "https://schema.org/EBook", "url": SITE + static_href("read.html?b=" + bid, lang).split("#")[0], "isAccessibleForFree": True}
        g.append(bk)
        page["mainEntity"] = {"@id": url + "#book"}
    elif kind == "program":
        g.append({"@type": "Course", "name": o["h1"], "description": o["desc"], "url": url, "inLanguage": lang, "provider": {"@id": SITE + "/#org"}})
    elif kind == "article":
        g.append({"@type": "Article", "headline": o["h1"][:110], "description": o["desc"], "url": url, "inLanguage": lang, "image": o["img"], "publisher": {"@id": SITE + "/#org"}})
    elif kind == "chapter":
        g.append({"@type": "Chapter", "name": o["h1"], "url": url, "inLanguage": lang, "isPartOf": {"@type": "Book", "name": o["book"], "url": SITE + static_href("book.html?b=" + o["bid"], lang)}})
    g.append(page)
    return json.dumps({"@context": "https://schema.org", "@graph": g}, ensure_ascii=False).replace("</", "<\\/")


def head_block(kind, slug, lang, langs, o, q=""):
    url = url_of(slug, lang)
    alts = "".join('<link rel="alternate" hreflang="%s" href="%s">' % (l, url_of(slug, l)) for l in langs)
    alts += '<link rel="alternate" hreflang="x-default" href="%s">' % url_of(slug, "az" if "az" in langs else langs[0])
    img = o["img"] if o["img"].startswith("http") else SITE + (o["img"] if o["img"].startswith("/") else "/" + o["img"])
    o = dict(o, img=img)
    boot = "<script>window.__LANG=%s;window.__Q=%s;try{localStorage.setItem('r11_lang',%s)}catch(e){}</script>" % (json.dumps(lang), json.dumps(q), json.dumps(lang))
    og_type = {"book": "book", "article": "article", "chapter": "article"}.get(kind, "website")
    return ("<!--seo-->" + boot + '<base href="/">'
            '<meta name="description" content="%s"><link rel="canonical" href="%s">%s'
            '<meta property="og:site_name" content="Doctor Ragimoff"><meta property="og:type" content="%s"><meta property="og:title" content="%s">'
            '<meta property="og:description" content="%s"><meta property="og:url" content="%s"><meta property="og:image" content="%s"><meta property="og:locale" content="%s">%s'
            '<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="%s"><meta name="twitter:description" content="%s"><meta name="twitter:image" content="%s">'
            '<script type="application/ld+json">%s</script><!--/seo-->') % (
        E(o["desc"]), url, alts, og_type, E(o["title"]), E(o["desc"]), url, E(img), LOCALE[lang],
        "".join('<meta property="og:locale:alternate" content="%s">' % LOCALE[l] for l in langs if l != lang),
        E(o["title"]), E(o["desc"]), E(img), jsonld(kind, slug, lang, o))


def finish(doc, kind, slug, lang, langs, o, q):
    doc = re.sub(r"<!--seo-->.*?<!--/seo-->\n*", "", doc, flags=re.S)
    doc = re.sub(r"<html\b[^>]*>", '<html lang="%s" data-theme="night" data-static="1">' % lang, doc, count=1)
    doc = re.sub(r"<title>.*?</title>", "<title>%s</title>" % E(o["title"]), doc, count=1, flags=re.S)
    doc = doc.replace("<head>", "<head>\n" + head_block(kind, slug, lang, langs, o, q), 1)
    # 13.11 (Кенан: публиковать порционно, без лишних файлов): номер версии stamp.py в снимках не нужен — GitHub Pages обновляет
    # кэш файлов через 10 мин; без него снимок меняется только при смене текста страницы, и в коммит идут только изменённые страницы
    doc = re.sub(r'((?:href|src)="assets/[^"?]+\.(?:css|js))\?v=\d+"', r'\1"', doc)
    return relink(doc, lang)


# ---------- снимки страниц в Chrome
GRAB = r"""
(async () => {
  const txt = () => (document.querySelector('main') || document.body).innerText.trim().length;
  for (let k = 0; k < 40 && (document.readyState !== 'complete' || txt() < 120); k++) await new Promise(r => setTimeout(r, 150));
  /* 13.11: ждать, пока страница перейдёт на язык снимка (иначе заголовок мог остаться на языке шаблона) */
  for (let k = 0; k < 40 && document.documentElement.lang !== '__L__'; k++) await new Promise(r => setTimeout(r, 100));
  document.querySelectorAll('.rv').forEach(e => e.classList.add('is-in'));
  await new Promise(r => setTimeout(r, 350));
  const pick = sels => { for (const s of sels) { for (const e of document.querySelectorAll(s)) { const t = (e.innerText || '').trim(); if (t.length > 40) return t; } } return ''; };
  const h1 = (document.querySelector('main h1, h1') || {}).innerText || '';
  const img = [...document.querySelectorAll('main img')].map(i => i.getAttribute('src')).find(s => s && !/\.svg$/.test(s) && !/^data:/.test(s)) || '';
  return { title: document.title, h1: h1.trim(), desc: pick(['.pp__lead', '.hero__lead', '.pg__lead', 'main .lead', 'main p']), img,
           html: '<!doctype html>\n' + document.documentElement.outerHTML };
})()
"""


async def snap_pages(todo):
    prof = tempfile.mkdtemp()
    p = subprocess.Popen([CHROME, "--headless=new", "--remote-debugging-port=%d" % PORT, "--user-data-dir=" + prof, "--hide-scrollbars", "--window-size=1366,900", "about:blank"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    ws_url = None
    for _ in range(300):
        try:
            ws_url = [t for t in json.load(urllib.request.urlopen("http://127.0.0.1:%d/json" % PORT)) if t["type"] == "page"][0]["webSocketDebuggerUrl"]
            break
        except Exception:
            time.sleep(.2)
    if not ws_url:
        raise SystemExit("Chrome не поднял порт %d" % PORT)
    res, n = [], [0]
    try:
        async with websockets.connect(ws_url, max_size=200_000_000) as ws:
            async def cmd(m, **pr):
                n[0] += 1
                i = n[0]
                await ws.send(json.dumps({"id": i, "method": m, "params": pr}))
                while True:
                    r = json.loads(await ws.recv())
                    if r.get("id") == i:
                        return r.get("result", {})
            await cmd("Page.enable")
            await cmd("Page.navigate", url=BASE + "contact.html")
            await asyncio.sleep(1.5)
            for k, (u, slug, kind, lang, langs) in enumerate(todo):
                await cmd("Runtime.evaluate", expression="localStorage.setItem('r11_lang','%s')" % lang)
                await cmd("Page.navigate", url=BASE + u)
                await asyncio.sleep(.6)
                r = await cmd("Runtime.evaluate", expression=GRAB.replace("__L__", lang), returnByValue=True, awaitPromise=True)
                o = (r.get("result") or {}).get("value")
                if not o:
                    print("  нет ответа:", lang, u)
                    continue
                res.append((u, slug, kind, lang, langs, o))
                if k % 40 == 0:
                    print("  снимков: %d/%d" % (k + 1, len(todo)))
    finally:
        p.kill()
        shutil.rmtree(prof, ignore_errors=True)
    return res


def build_pages():
    todo = [(u, s, kind, l, langs) for (u, s, kind, langs) in page_list() for l in langs]
    print("страниц для снимков:", len(todo))
    # 13.11.2026: страж — сервер упал посреди сборки, и вместо страниц записалась страница ошибки Chrome (262 снимка).
    # Перед сборкой сервер должен отвечать; снимок с признаками страницы ошибки или без содержимого не записывается.
    try:
        urllib.request.urlopen(BASE + "index.html", timeout=5)
    except Exception as e:
        raise SystemExit("СТОП: локальный сервер %s не отвечает (%s) — запустите python -m http.server 8812 из корня сайта" % (BASE, e))
    res = asyncio.run(snap_pages(todo))
    bad = [(u, lang) for (u, slug, kind, lang, langs, o) in res
           if re.search(r"neterror|ERR_CONNECTION|ERR_NAME_NOT|id=\"main-frame-error\"", o["html"]) or 'data-kind=' not in o["html"] and 'id="top"' not in o["html"]]
    if bad or len(res) != len(todo):
        raise SystemExit("СТОП: %d снимков похожи на страницу ошибки браузера, %d страниц без ответа — ничего не записано. Примеры: %s"
                         % (len(bad), len(todo) - len(res), bad[:5]))
    # 13.11.2026: страж — статья снялась недогруженной (title «Doctor Ragimoff», без текста) и затёрла хороший снимок.
    # Недогруженные снимаются ещё раз; если и повтор такой же — прежний файл остаётся, страница называется в отчёте.
    half = lambda o: o["title"].strip() in ("", "Doctor Ragimoff") and not o["h1"].strip()
    redo = [r[:5] for r in res if half(r[5]) and not r[0].split("?")[0].endswith("index.html")]
    if redo:
        again = {r[0] + r[3]: r for r in asyncio.run(snap_pages(redo))}
        keep = []
        for r in res:
            if half(r[5]) and not r[0].split("?")[0].endswith("index.html"):
                n = again.get(r[0] + r[3])
                if n and not half(n[5]):
                    keep.append(n)
                else:
                    print("ПРОПУЩЕНО (недогружено дважды, прежний снимок оставлен):", r[0], r[3])
            else:
                keep.append(r)
        res = keep
    w, az_head = 0, {}
    for (u, slug, kind, lang, langs, o) in res:
        q = "?" + u.split("?", 1)[1] if "?" in u else ""
        title = o["title"] or (o["h1"] + " — Doctor Ragimoff")
        desc = clip(DESC[slug][lang] if slug in DESC else (book_desc(slug[5:], lang) if kind == "book" else (o["desc"] or o["h1"])))
        img = OG_DEFAULT if slug in DESC or not o["img"] or o["img"].endswith(".webp") else o["img"]
        if kind == "book":
            it = ITEMS[lang].get(slug[5:])
            img = "/assets/img/books/covers/%s-%s.jpg" % (it["cov"], lang) if it and it.get("cov") else OG_DEFAULT
        oo = {"title": title, "desc": desc, "img": img, "h1": o["h1"]}
        doc = re.sub(r'(<(?:nav|div) class="(?:nav|mob__in)"[^>]*>)', r"\1", o["html"])
        w += write("%s/%s.html" % (lang, slug) if slug != "index" else "%s/index.html" % lang, finish(doc, kind, slug, lang, langs, oo, q))
        if lang == "az":
            az_head[u.split("?")[0] if "?" not in u or u.startswith("consult.html?c=index") else None] = (kind, slug, langs, oo, q)
    # шаблоны корня: AZ-превью и canonical для страниц без параметров (index, shop, blog, contact, corporate, test, consult)
    for tpl, v in az_head.items():
        if not tpl:
            continue
        kind, slug, langs, oo, q = v
        p = "index.html" if tpl == "index.html" else tpl
        s = io.open(p, encoding="utf-8").read()
        s = re.sub(r"<!--seo-->.*?<!--/seo-->\n*", "", s, flags=re.S)
        blk = head_block(kind, slug, "az", langs, oo, "").replace('<base href="/">', "")
        blk = re.sub(r"<script>window.__LANG=.*?</script>", "", blk)        # корень остаётся живым: язык выбирает посетитель
        s = s.replace("<head>", "<head>\n" + blk, 1)
        w += write(p, s)
    # шаблоны с параметрами (book.html, read.html …): общее AZ-описание сайта, чтобы превью не было пустым
    base = az_head.get("index.html")
    if base:
        for p in ("book.html", "read.html", "program.html", "specialist.html", "article.html"):
            s = io.open(p, encoding="utf-8").read()
            s = re.sub(r"<!--seo-->.*?<!--/seo-->\n*", "", s, flags=re.S)
            oo = base[3]
            blk = ('<!--seo--><meta name="description" content="%s"><meta property="og:site_name" content="Doctor Ragimoff"><meta property="og:type" content="website">'
                   '<meta property="og:title" content="%s"><meta property="og:description" content="%s"><meta property="og:image" content="%s"><meta property="og:locale" content="az_AZ">'
                   '<meta name="twitter:card" content="summary_large_image"><!--/seo-->') % (E(oo["desc"]), E(oo["title"]), E(oo["desc"]), E(SITE + OG_DEFAULT))
            w += write(p, s.replace("<head>", "<head>\n" + blk, 1))
    print("страниц записано:", w, "из", len(res))
    return [(slug, lang, langs) for (u, slug, kind, lang, langs, o) in res]


# ---------- главы книг: шаблон читалки + текст главы
def build_chapters():
    tpl = io.open("read.html", encoding="utf-8").read()
    tpl = re.sub(r"<!--seo-->.*?<!--/seo-->\n*", "", tpl, flags=re.S)
    w, urls = 0, []
    for bid, P in BOOKS.items():
        langs = BOOK_LANGS[bid]
        for lang in langs:
            toc = [x for x in P["toc"].get(lang, [])]
            if not toc:
                continue
            bt = P["t"].get(lang) or P["t"].get("az")
            it = ITEMS[lang].get(bid) or ITEMS["az"].get(bid) or {}
            img = "/assets/img/books/covers/%s-%s.jpg" % (it["cov"], lang) if it.get("cov") else (P.get("cover") or OG_DEFAULT)
            for i, ch in enumerate(toc, 1):
                key = ch.get("id") or str(i)
                f = "books/%s/%s/%03d.html" % (bid, lang, i)
                if not os.path.exists(f):
                    continue
                body = io.open(f, encoding="utf-8").read()
                plain = re.sub(r"<[^>]+>", " ", body)
                title = "%s — %s | Doctor Ragimoff" % (re.sub(r"<[^>]+>", "", ch["t"]), bt)
                o = {"title": title, "desc": clip(plain), "img": img, "h1": re.sub(r"<[^>]+>", "", ch["t"]), "book": bt, "bid": bid}
                slug = "read/%s/%s" % (bid, key)
                navl = "".join('<li><a href="/%s/read/%s/%s.html">%s</a></li>' % (lang, bid, x.get("id") or str(j), E(re.sub(r"<[^>]+>", "", x["t"]))) for j, x in enumerate(toc, 1))
                # оглавление для поисковиков — внутри #rdTitle (читалка его перерисовывает); #rdTocL пустой: по нему читалка узнаёт первый запуск
                main = ('<div id="rdTitle"><div class="rdr__ti"><p class="pp__kind"><a href="/%s/book-%s.html">%s</a></p><nav class="rdr__stoc"><ol>%s</ol></nav></div></div>'
                        '<article class="rdr__chap" id="rdChap"><h1 class="rdr__h">%s</h1><div class="rdr__body">%s</div></article>') % (lang, bid, E(bt), navl, E(o["h1"]), body)
                doc = tpl.replace('<div id="rdTitle"></div>\n    <article class="rdr__chap" id="rdChap" hidden></article>', main, 1)
                q = "?b=%s&%s=%s" % (bid, "p" if ch.get("id") else "c", key)
                w += write("%s/%s.html" % (lang, slug), finish(doc, "chapter", slug, lang, langs, o, q))
                urls.append((slug, lang, langs))
            # оглавление книги в читалке (read.html?b=<книга>) → /<язык>/read/<книга>/index.html = первая глава
            first = toc[0].get("id") or "1"
            src = "%s/read/%s/%s.html" % (lang, bid, first)
            if os.path.exists(src):
                s = io.open(src, encoding="utf-8").read().replace("/read/%s/%s.html\">" % (bid, first), "/read/%s/%s.html\">" % (bid, first))
                s = s.replace('<link rel="canonical" href="%s">' % url_of("read/%s/%s" % (bid, first), lang), '<link rel="canonical" href="%s">' % url_of("read/%s/%s" % (bid, first), lang))
                w += write("%s/read/%s/index.html" % (lang, bid), s)
    print("глав записано:", w, "| адресов глав:", len(urls))
    return urls


def build_maps(pages, chapters):
    write("assets/js/seo-map.js", "/* языки книг для постоянных адресов (собирает _tools/build_static.py) */\nexport const BOOK_LANGS = %s;\n" % json.dumps(BOOK_LANGS, ensure_ascii=False))
    day = time.strftime("%Y-%m-%d")
    allu = pages + chapters
    x = ['<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for slug, lang, langs in allu:
        alts = "".join('<xhtml:link rel="alternate" hreflang="%s" href="%s"/>' % (l, url_of(slug, l)) for l in langs)
        x.append("<url><loc>%s</loc><lastmod>%s</lastmod>%s</url>" % (url_of(slug, lang), day, alts))
    x.append("</urlset>\n")
    write("sitemap.xml", "\n".join(x))
    robots = ("# robots.txt — ragimoff.org (13.11.2026): сайт открыт для поисковиков и ИИ-моделей\n"
              "User-agent: *\nAllow: /\nDisallow: /_tools/\nDisallow: /_agent/\nDisallow: /sketch/\nDisallow: /payment/\n\n"
              + "".join("User-agent: %s\nAllow: /\n\n" % b for b in ("GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-User", "Claude-SearchBot", "PerplexityBot",
                                                                   "Google-Extended", "Applebot-Extended", "CCBot", "DeepSeekBot", "Bytespider", "YandexBot", "Bingbot"))
              + "Sitemap: %s/sitemap.xml\n" % SITE)
    write("robots.txt", robots)
    print("карта сайта: адресов", len(allu))


def build_llms():
    L = ["# Doctor Ragimoff — ragimoff.org", "",
         "> Kənan Rəhimov (Kenan Ragimov, Кенан Рагимов) — psychiatrist and psychotherapist in Baku, Azerbaijan; school of psychology, consultations, "
         "training programs and books. Site languages: Azerbaijani (main), Russian, English. Every page exists at /az/, /ru/ and /en/.", ""]
    for lang, head in (("az", "Azərbaycan dilində"), ("ru", "На русском"), ("en", "In English")):
        it = ITEMS[lang]
        L += ["## %s" % head, "",
              "- [%s](%s)" % ({"az": "Ana səhifə", "ru": "Главная", "en": "Home"}[lang], url_of("index", lang)),
              "- [%s](%s)" % (KENAN[lang], url_of("specialist-kenan", lang)),
              "- [%s](%s)" % (SHOP[lang]["title"], url_of("shop", lang))]
        for p in progs:
            L.append("- [%s](%s)" % (p, url_of("program-" + p, lang)))
        for bid, x in it.items():
            if bid in BOOKS:
                f = FACTS.get(bid, {})
                pg = (f.get("pages") or {}).get(lang) or (f.get("pages") or {}).get("az")
                L.append("- [%s](%s)%s — %s%s" % (x["t"], url_of("book-" + bid, lang), " (%s)" % x["g"], ("%s pp. · " % pg) if pg else "",
                                                     "read free: " + SITE + static_href("read.html?b=" + bid, lang).split("#")[0] if x.get("read") else ""))
        L.append("")
    L += ["## Notes", "", "- Freud's works are translated into Azerbaijani by the school (first complete Azerbaijani edition); other languages of Freud are not published here.",
          "- Contact: %s" % url_of("contact", "en"), ""]
    write("llms.txt", "\n".join(L))


if __name__ == "__main__":
    t0 = time.time()
    build_maps([], [])            # seo-map.js нужен сценариям до снимков
    pages = build_pages() if mode in ("all", "pages") else []
    chapters = build_chapters() if mode in ("all", "chapters") else []
    if mode == "all":
        build_maps(pages, chapters)
        build_llms()
    print("готово за %d с" % (time.time() - t0))
