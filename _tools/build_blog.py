# -*- coding: utf-8 -*-
"""Блог → данные test/11: статьи <lang>/bloq/*.html → data/blog/<slug>.<lang>.json, список → data/blog/index.<lang>.json.
Текст дословно, оформление отбрасывается. Повторный запуск даёт тот же результат."""
import sys, re, io, os, json, glob
from bs4 import BeautifulSoup, NavigableString, Comment
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\Projects\Ragimoff\old_versions\2026-11-12_site_before_v11"   # прежний сайт: источник текстов и картинок, только чтение (с 12.11.2026 версия 11 — корень сайта)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "blog")
KEEP = {"p", "h2", "h3", "h4", "ul", "ol", "li", "strong", "em", "b", "i", "a", "br", "sup", "sub", "figure", "img", "figcaption",
        "table", "thead", "tbody", "tr", "th", "td", "caption", "blockquote"}
ATTR = {"a": ["href"], "img": ["src", "alt", "width", "height"], "td": ["colspan", "rowspan"], "th": ["colspan", "rowspan"]}


def txt(el):
    return re.sub(r"\s+", " ", el.get_text(" ", strip=True)).strip() if el else ""


def absurl(u, lang, sub="bloq"):
    """относительный адрес исходной страницы → от корня сайта"""
    if not u or re.match(r"^(https?:|mailto:|tel:|#|/)", u):
        return u
    base = [lang, sub]
    for part in u.split("/"):
        if part == "..":
            if base:
                base.pop()
        elif part != ".":
            base.append(part)
    return "/" + "/".join(base)


def clean(node, lang):
    """оставить только разрешённые теги и атрибуты; рамки-выделения → blockquote"""
    for c in node.find_all(string=lambda s: isinstance(s, Comment)):
        c.extract()
    for t in node.find_all(["script", "style", "svg", "button", "form", "iframe"]):
        t.decompose()
    for t in node.find_all(True):
        if t.name == "div" and t.get("class") and any("box" in c or "note" in c or "callout" in c for c in t.get("class")):
            t.name = "blockquote"
        if t.name == "div" and not t.find(["div", "p", "ul", "ol", "table", "figure", "h2", "h3", "h4", "blockquote"]):
            t.name = "p"                      # строка-«плитка» из div → абзац
        if t.name not in KEEP:
            t.insert_after(" ")               # слова соседних плиток не склеиваются
            t.unwrap()
            continue
        keep = ATTR.get(t.name, [])
        for a in list(t.attrs):
            if a not in keep:
                del t.attrs[a]
        if t.name == "a":
            t["href"] = absurl(t.get("href", ""), lang)
        if t.name == "img":
            t["src"] = absurl(t.get("src", ""), lang)
    h = node.decode_contents()
    h = re.sub(r"\n\s*\n+", "\n", h).strip()
    return h


def article(fn, lang):
    slug = os.path.basename(fn)[:-5]
    s = BeautifulSoup(io.open(fn, encoding="utf-8").read(), "html.parser")
    main = s.find("main") or s
    hero = main.find(class_="n-hero")
    d = {"slug": slug, "lang": lang, "src": "%s/bloq/%s.html" % (lang, slug),
         "eye": txt(hero.find(class_="n-eyebrow")) if hero else "", "title": txt(hero.find("h1")) if hero else txt(main.find("h1")),
         "lead": txt(hero.find(class_="n-lead")) if hero else "", "img": None, "blocks": []}
    cov = main.find("img", class_="art-cover")
    him = hero.find("img") if hero else None
    d["img"] = absurl((cov or him)["src"], lang) if (cov or him) else None
    body = main.find(class_="article-body")
    if not body:
        print("  ! нет article-body:", fn)
        return None
    src = main.find(class_="art-sources")
    if src and body in src.parents:
        pass
    inner_src = body.find(class_="art-sources")
    if inner_src:
        src = inner_src.extract()
    auth = body.find(class_="author-block")
    if auth:
        auth = auth.extract()
    else:
        auth = main.find(class_="author-block")
    d["blocks"].append({"type": "prose", "html": clean(body, lang)})
    if src:
        t = src.find("strong")
        title = txt(t) if t else ""
        if t:
            t.extract()
        items = []
        for p in src.find_all(["p", "li"]):
            h = clean(p, lang)
            if re.sub(r"<[^>]+>", "", h).strip():
                items.append(h)
        if not items:
            h = clean(src, lang)
            if h:
                items = [h]
        d["blocks"].append({"type": "sources", "t": title, "items": items})
    if auth:
        n = auth.find("strong")
        p = auth.find("p")
        d["author"] = [txt(n), txt(p)]
    for sec in main.find_all("section"):
        cards = sec.find_all("a", class_="blog-card")
        if cards and not sec.find(class_="article-body"):
            h = sec.find(class_="sec-h2")
            d["blocks"].append({"type": "articles", "h": txt(h), "items": [os.path.basename(a["href"]).split(".html")[0] for a in cards]})
    band = main.find(class_="cta-band")
    if band:
        h = band.find(class_="sec-h2")
        sub = band.find(class_="sec-sub")
        d["blocks"].append({"type": "cta", "h": txt(h), "sub": txt(sub), "btns": [[txt(a), absurl(a.get("href", ""), lang)] for a in band.find_all("a", class_="btn")]})
    return d


def index(lang):
    fn = os.path.join(ROOT, lang, "bloq", "index.html")
    s = BeautifulSoup(io.open(fn, encoding="utf-8").read(), "html.parser")
    main = s.find("main") or s
    hero = main.find(class_="n-hero")
    d = {"slug": "index", "lang": lang, "src": "%s/bloq/index.html" % lang, "eye": txt(hero.find(class_="n-eyebrow")), "title": txt(hero.find("h1")),
         "lead": txt(hero.find(class_="n-lead")), "cats": [], "items": []}
    for b in main.find_all(class_="filter-btn"):
        m = re.search(r"\('([^']+)'", b.get("onclick", ""))
        d["cats"].append([m.group(1) if m else "all", txt(b)])
    f = main.find(class_="blog-featured")
    if f:
        d["featured"] = {"slug": os.path.basename(f["href"])[:-5], "badge": txt(f.find(class_="blog-featured-badge")), "title": txt(f.find(class_="blog-featured-title")),
                         "meta": txt(f.find(class_="blog-featured-meta")), "excerpt": txt(f.find(class_="blog-featured-excerpt")), "cta": txt(f.find(class_="btn"))}
    grid = main.find(id="blogGrid") or main
    for a in grid.find_all("a", class_="blog-card"):
        im = a.find("img")
        foot = a.find(class_="blog-card-footer")
        spans = foot.find_all("span") if foot else []
        d["items"].append({"slug": os.path.basename(a["href"]).split(".html")[0], "cat": a.get("data-cat", ""), "catLabel": txt(a.find(class_="blog-card-cat")),
                           "title": txt(a.find(class_="blog-card-title")), "excerpt": txt(a.find(class_="blog-card-excerpt")),
                           "meta": txt(spans[0]) if spans else "", "read": txt(spans[-1]) if len(spans) > 1 else "",
                           "cover": absurl(im["src"], lang) if im else None})
    band = main.find(class_="cta-band")
    if band:
        d["cta"] = {"h": txt(band.find(class_="sec-h2")), "sub": txt(band.find(class_="sec-sub")), "btns": [[txt(a), absurl(a.get("href", ""), lang)] for a in band.find_all("a", class_="btn")]}
    return d


def main():
    os.makedirs(OUT, exist_ok=True)
    for lang in ("ru", "az", "en"):
        n = 0
        for fn in sorted(glob.glob(os.path.join(ROOT, lang, "bloq", "*.html"))):
            if os.path.basename(fn) == "index.html":
                continue
            d = article(fn, lang)
            if d:
                json.dump(d, io.open(os.path.join(OUT, "%s.%s.json" % (d["slug"], lang)), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
                n += 1
        ix = index(lang)
        json.dump(ix, io.open(os.path.join(OUT, "index.%s.json" % lang), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(lang, "статей:", n, "в списке:", len(ix["items"]), "рубрик:", len(ix["cats"]))


main()
