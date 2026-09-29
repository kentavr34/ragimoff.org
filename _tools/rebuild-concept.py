# -*- coding: utf-8 -*-
"""
_tools/rebuild-concept.py — ПЕРЕСБОРКА страниц книг по каркасу дизайн-концепта.

Зачем: раньше концепт подключали как CSS поверх старых страниц (разметка
`.content-wrap` / `.sidebar` / `.home-hero`), а концепт построен на своих классах
`.bk-*`. CSS-адаптер `!important` перекрашивал старое, но каркас оставался старым —
поэтому вид не менялся. Здесь страница РЕНДЕРИТСЯ ЗАНОВО по разметке концепта.

Каркас-эталон (функции head/header/sidebar/footer/shell/langs_html):
    D:\\Документы\\ZFreud\\_align\\design_concept\\_tools\\build_concept.py
Функции перенесены в этот файл (а не импортированы): build_concept.py — скрипт-демо,
он пишет свои файлы и печатает отчёт прямо при импорте.

Данные ПЕРЕНОСЯТСЯ из существующих страниц без перенабора:
  · название книги, автор, год — из шапки/титула страницы;
  · оглавление — из сайдбара (номера) и списка `.book-toc` (названия);
  · заголовок главы, абзацы, таблицы, списки, примечания — из `.content-wrap`;
  · пред/след и «вверх» — из `.d-nav` / `.page-nav`;
  · title, description, canonical, hreflang, OG, JSON-LD, data-lang-* — из <head>.

Пути и имена файлов сохраняются (в т.ч. главы-каталоги `ru/<slug>/index.html`),
поэтому ссылки и sitemap не ломаются.

Запуск:
    python _tools/rebuild-concept.py --dry          # только отчёт
    python _tools/rebuild-concept.py                # пересобрать всё
    python _tools/rebuild-concept.py --book books/freud-musa
"""
import argparse
import glob
import html
import json
import os
import posixpath
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOKS = [
    "books/freud-yuxularin-yozumu",
    "books/freud-musa",
    "books/freud-psixoanalizle-tanishliq",
    "books/freud-seksualligin-psixologiyasi",
    "books/freud-sevgi-mektublari",
    "books/freud-aforizmlar",
    "books/freud-medeniyyetin-sancilari",
    "books/freud-totem-ve-tabu",
    "books/virus-viny",
    "books/shizofreniya",
    "books/phoenix-era",
    "klinik-psixiatriya",
]
SKIP_DIRS = ("test", ".bak")          # books/phoenix-era/test — не пересобираем

FONT_URL = ("https://fonts.googleapis.com/css2?"
            "family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,400"
            "&family=IBM+Plex+Mono:wght@400;500"
            "&family=Literata:ital,opsz,wght@0,7..72,300..700;1,7..72,300..700"
            "&family=Montserrat:wght@300;400;500")
CSS_BOOK = "/books/book.css?v=8"               # концепт (замена содержимого на book-concept.css)
CSS_CONTENT = "/books/book-content.css?v=1"    # содержимое книг: таблицы, списки, обложки

# ── строки интерфейса по языкам страницы ──────────────────────────────────────
UI = {
    "az": {
        "toc": "Mündəricat", "one": "fəsil", "few": "fəsil", "many": "fəsil",
        "prev": "Əvvəlki", "next": "Növbəti", "up": "Kitabın mündəricatı",
        "back": "← Kitablar", "order": "Sifariş et", "nav": "Mündəricat",
        "langs": "Dil", "home": "Ana səhifə",
        "foot": [("Ana Səhifə", "/"), ("Kitablar", "/books/"),
                 ("Telegram", "https://t.me/ragimoff"), ("info@ragimoff.org", "mailto:info@ragimoff.org")],
        "none": "Bu kitab {c} dilində yoxdur",
    },
    "ru": {
        "toc": "Оглавление", "one": "глава", "few": "главы", "many": "глав",
        "prev": "Предыдущая", "next": "Следующая", "up": "Оглавление книги",
        "back": "← Книги", "order": "Заказать", "nav": "Оглавление",
        "langs": "Язык", "home": "Главная страница",
        "foot": [("Главная", "/"), ("Книги", "/books/"),
                 ("Telegram", "https://t.me/ragimoff"), ("info@ragimoff.org", "mailto:info@ragimoff.org")],
        "none": "Этой версии нет на языке {c}",
    },
    "en": {
        "toc": "Contents", "one": "chapter", "few": "chapters", "many": "chapters",
        "prev": "Previous", "next": "Next", "up": "Book contents",
        "back": "← Books", "order": "Order", "nav": "Contents",
        "langs": "Language", "home": "Home",
        "foot": [("Home", "/"), ("Books", "/books/"),
                 ("Telegram", "https://t.me/ragimoff"), ("info@ragimoff.org", "mailto:info@ragimoff.org")],
        "none": "This book is not available in {c}",
    },
    "tr": {
        "toc": "İçindekiler", "one": "bölüm", "few": "bölüm", "many": "bölüm",
        "prev": "Önceki", "next": "Sonraki", "up": "Kitabın içindekiler",
        "back": "← Kitaplar", "order": "Sipariş", "nav": "İçindekiler",
        "langs": "Dil", "home": "Ana sayfa",
        "foot": [("Ana Sayfa", "/"), ("Kitaplar", "/books/"),
                 ("Telegram", "https://t.me/ragimoff"), ("info@ragimoff.org", "mailto:info@ragimoff.org")],
        "none": "Bu kitab {c} dilində yoxdur",
    },
}
LANG_TITLE = {"az": "AZ", "ru": "RU", "en": "EN", "tr": "TR"}


def ui(lang):
    return UI.get(lang, UI["az"])


def plural(lang, n):
    L = ui(lang)
    if lang == "ru":
        if n % 10 == 1 and n % 100 != 11:
            return L["one"]
        if n % 10 in (2, 3, 4) and n % 100 not in (12, 13, 14):
            return L["few"]
        return L["many"]
    if lang == "en":
        return L["one"] if n == 1 else L["many"]
    return L["one"]


# ── микро-помощники ───────────────────────────────────────────────────────────
DIV_RE = re.compile(r"<div\b[^>]*>|</div>", re.I)


def tag_html(raw, start):
    """Возвращает HTML-тег, начинающийся в позиции start."""
    return raw[start:raw.find(">", start) + 1]


def block_end(raw, start, tag="div"):
    """Индекс закрывающего тега </tag> для <tag>, начинающегося в start."""
    rgx = re.compile(r"<%s\b[^>]*>|</%s>" % (tag, tag), re.I)
    depth = 0
    for m in rgx.finditer(raw, start):
        if m.group(0).lower().startswith("</"):
            depth -= 1
            if depth == 0:
                return m.start()
        else:
            depth += 1
    return len(raw)


def block_html(raw, start, tag="div"):
    """Весь блок вместе с закрывающим тегом."""
    end = block_end(raw, start, tag)
    return raw[start:raw.find(">", end) + 1]


def div_inner(raw, start):
    return raw[raw.find(">", start) + 1:block_end(raw, start)]


def strip_tags(s):
    s = re.sub(r"<(script|style)\b.*?</\1>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<br\s*/?>", " ", s, flags=re.I)
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def attr(tag, name):
    m = re.search(r'\b%s\s*=\s*"([^"]*)"' % name, tag)
    if not m:
        m = re.search(r"\b%s\s*=\s*'([^']*)'" % name, tag)
    return m.group(1) if m else None


ACRONYMS = {"DSM", "ICD", "XBT", "PTSD", "OKP", "ADHD", "DDHP", "PMDD", "DCD", "ASP",
            "ABA", "CBT", "DBT", "EMDR", "MBT", "TFP", "ERP", "SSRI", "SSRİ", "FAQ",
            "HIV", "WHO", "TR", "AZ", "RU", "EN", "II", "III", "IV", "VI", "VII", "MMPI",
            "MMSE", "GAF", "IQ", "ABC", "TDA", "PTSP", "DDH", "XBT-11", "XBT-10"}
# азербайджанская/турецкая пара i/İ и ı/I не подчиняется str.lower()/upper()
AZ_LOWER = {"İ": "i", "I": "ı"}
AZ_UPPER = {"i": "İ", "ı": "I"}


def az_lower(t, lang):
    if lang not in ("az", "tr"):
        return t.lower()
    return "".join(AZ_LOWER.get(c, c.lower()) for c in t)


def az_upper1(ch, lang):
    if lang in ("az", "tr") and ch in AZ_UPPER:
        return AZ_UPPER[ch]
    return ch.upper()


def nice_case(s, lang="az"):
    """КАПС → обычный регистр (требование концепта). Аббревиатуры и коды сохраняем:
    так «MUSA VƏ TƏKALLAHLIQ» становится «Musa və təkallahlıq», а «DSM-5-TR» остаётся."""
    s = re.sub(r"\s+", " ", s).strip()
    letters = [c for c in s if c.isalpha()]
    if not letters or any(c.islower() for c in letters):
        return s                      # уже не капс — не трогаем
    out = []
    for tok in s.split(" "):
        core = tok.strip("()[]«»\"'.,;:!?—-–")
        keep = (len(core) <= 1 or any(ch.isdigit() for ch in core)
                or core.upper() in ACRONYMS or not core.isalpha())
        out.append(tok if keep else az_lower(tok, lang))
    txt = " ".join(out)
    # заглавная — в начале строки и после конца предложения
    txt = re.sub(r"(^|[.!?]\s+)([a-zəğıöşüç])",
                 lambda m: m.group(1) + az_upper1(m.group(2), lang), txt)
    return txt


def esc(s):
    return html.escape(s or "", quote=True)


# ── разбор исходной страницы ──────────────────────────────────────────────────
def parse_page(path, book, page_rel, base=None):
    raw = read_source(os.path.join(book, page_rel).replace("\\", "/"), base)
    p = {"path": path, "book": book, "rel": page_rel, "raw": raw}
    head = raw[:raw.find("<body")] if "<body" in raw else raw

    p["html_tag"] = (re.findall(r"<html[^>]*>", raw) or ["<html>"])[0]
    p["lang"] = attr(p["html_tag"], "lang") or "az"
    p["declared"] = [x for x in (attr(p["html_tag"], "data-langs") or "").replace(" ", ",").split(",") if x]
    p["lang_urls"] = {}
    for code in ("az", "ru", "en", "tr"):
        v = attr(p["html_tag"], "data-lang-url-%s" % code)
        if v:
            p["lang_urls"][code] = v
    p["avail"] = [x for x in (attr(p["html_tag"], "data-lang-avail") or "").replace(" ", ",").split(",") if x]

    p["title"] = strip_tags((re.findall(r"<title>(.*?)</title>", head, re.S) or [""])[0])
    p["desc"] = attr((re.findall(r'<meta name="description"[^>]*>', head) or [""])[0], "content") or ""
    p["keywords"] = attr((re.findall(r'<meta name="keywords"[^>]*>', head) or [""])[0], "content") or ""
    p["robots"] = attr((re.findall(r'<meta name="robots"[^>]*>', head) or [""])[0], "content") or "index, follow"
    p["canonical"] = attr((re.findall(r'<link rel="canonical"[^>]*>', head) or [""])[0], "href") or ""
    p["hreflang"] = [(attr(t, "hreflang"), attr(t, "href"))
                     for t in re.findall(r'<link rel="alternate"[^>]*hreflang[^>]*>', head)]
    p["og"] = {}
    for t in re.findall(r'<meta property="og:[^"]*"[^>]*>', head):
        k = re.search(r'property="og:([^"]*)"', t)
        if k:
            p["og"][k.group(1)] = attr(t, "content") or ""
    p["jsonld"] = re.findall(r'<script type="application/ld\+json">(.*?)</script>', head, re.S)

    # языковые версии: свои адреса (data-lang-url-*) важнее hreflang
    p["alt"] = {}
    for code, href in p["hreflang"]:
        if code and code != "x-default" and href:
            p["alt"][code] = href
    for code, v in p["lang_urls"].items():
        p["alt"][code] = v
    if not p["avail"]:
        p["avail"] = [c for c in p["declared"] if c in p["alt"]] or (
            [p["lang"]] if not p["alt"] else sorted(p["alt"]))
    if not p["declared"]:
        p["declared"] = sorted(set(list(p["alt"].keys()) + [p["lang"]]))

    # ── шапка старой страницы: название книги, подпись ──
    st = re.search(r'<div class="hdr-title">(.*?)</div>', raw, re.S)
    p["book_title"] = strip_tags((re.findall(r"<strong>(.*?)</strong>", st.group(1), re.S) or [""])[0]) if st else ""
    p["book_meta"] = strip_tags((re.findall(r"<small>(.*?)</small>", st.group(1), re.S) or [""])[0]) if st else ""

    # ── сайдбар: пункты оглавления ──
    p["side"] = parse_sidebar(raw, path, book, page_rel)

    # ── содержимое ──
    parse_content(p, raw)

    # титул: своей рейки у него нет — берём навигацию книги (в демо она общая)
    if not (p["side"]["front"] or p["side"]["rows"] or p["side"]["trees"]):
        side = cover_side(book, page_rel, base)
        if not side["front"] and not side["rows"] and not side["trees"]:
            side = cover_toc_side(p)
        p["side"] = side
        if not p["side"]["front"] and not p["side"]["rows"] and not p["side"]["trees"]:
            p["side"] = empty_side()
    return p


def parse_sidebar(raw, path, book, page_rel):
    """Пункты навигации: front-ссылки, разделы, главы. Плюс вкладки классификаций (klinik).

    Два источника: исходный `.sidebar` (старая разметка) и уже пересобранный `.bk-sb`
    (каркас концепта). Второй нужен, потому что страницы уже пересобраны, и без него
    повторный прогон терял бы навигацию.
    """
    i = raw.find('<aside class="sidebar"')
    if i < 0:
        return parse_sidebar_bk(raw)
    side = {"front": [], "rows": [], "trees": [], "tabs": []}
    j = raw.find("</aside>", i)
    nav = raw[i:j]

    front_re = re.compile(r'<a\b([^>]*class="[^"]*nav-front[^"]*"[^>]*)>(.*?)</a>', re.S)
    for m in front_re.finditer(nav):
        href = attr(m.group(1), "href") or "index.html"
        side["front"].append({"href": href, "name": strip_tags(m.group(2)), "code": ""})

    row_re = re.compile(r'<(a|span)\b([^>]*class="[^"]*(?:is-bolme|nav-sub-link)[^"]*"[^>]*)>(.*?)</\1>', re.S)

    def rows_in(chunk):
        out = []
        for m in row_re.finditer(chunk):
            at = m.group(2)
            inner = m.group(3)
            cls = attr("<x " + at + ">", "class") or ""
            href = attr("<x " + at + ">", "href")
            code = strip_tags((re.findall(r'<span class="[^"]*(?:nav-code|sub-code)[^"]*">(.*?)</span>', inner, re.S) or [""])[0])
            name = (re.findall(r'<span class="[^"]*sub-name[^"]*">(.*?)</span>', inner, re.S) or [None])[0]
            if name is None:
                name = re.sub(r'<span class="[^"]*(?:nav-code|sub-code)[^"]*">.*?</span>', "", inner, flags=re.S)
            name = strip_tags(name)
            lvl = 1 if "is-bolme" in cls else 2
            out.append({"href": href, "name": name, "code": code, "level": lvl,
                        "active": "is-active" in cls})
        return out

    # вкладки классификаций + деревья (klinik-psixiatriya)
    for m in re.finditer(r'<button\b([^>]*class="[^"]*cls-tab[^"]*"[^>]*)>(.*?)</button>', nav, re.S):
        side["tabs"].append({"cls": attr("<x " + m.group(1) + ">", "data-cls") or "",
                             "label": strip_tags(m.group(2)),
                             "active": "is-active" in (attr("<x " + m.group(1) + ">", "class") or "")})
    for m in re.finditer(r'<div class="cls-tree" data-cls="([^"]*)"([^>]*)>', nav):
        start = m.start()
        end = block_end(nav, start)
        side["trees"].append({"cls": m.group(1), "rows": rows_in(nav[start:end]),
                              "hidden": "hidden" in m.group(2)})

    if not side["trees"]:
        side["rows"] = rows_in(nav)
    return side


def parse_sidebar_bk(raw):
    """Пункты навигации из УЖЕ пересобранной рейки `.bk-sb` (каркас концепта)."""
    side = {"front": [], "rows": [], "trees": [], "tabs": []}
    i = raw.find('<aside class="bk-sb')
    if i < 0:
        return side
    j = raw.find("</aside>", i)
    nav = raw[i:j]

    row_re = re.compile(r'<(a|span)\b([^>]*class="[^"]*\bbk-row\b[^"]*"[^>]*)>(.*?)</\1>', re.S)

    def rows_in(chunk, front):
        """front=True — только безномерные пункты (.bk-row--front), иначе — только главы."""
        out = []
        for m in row_re.finditer(chunk):
            tag = "<x " + m.group(2) + ">"
            cls = attr(tag, "class") or ""
            inner = m.group(3)
            if front != ("bk-row--front" in cls):
                continue
            if front:
                out.append({"href": attr(tag, "href") or "index.html",
                            "name": strip_tags(inner), "code": ""})
                continue
            code = strip_tags((re.findall(r'<span class="bk-row__n">(.*?)</span>', inner, re.S) or [""])[0])
            name = strip_tags((re.findall(r'<span class="bk-row__t">(.*?)</span>', inner, re.S) or [""])[0])
            lvl = 1 if "bk-row--sec" in cls else (2 if "bk-row--sub" in cls else 1)
            out.append({"href": attr(tag, "href"), "name": name, "code": code, "level": lvl,
                        "active": "is-on" in cls})
        return out

    for m in re.finditer(r'<button\b([^>]*class="[^"]*cls-tab[^"]*"[^>]*)>(.*?)</button>', nav, re.S):
        side["tabs"].append({"cls": attr("<x " + m.group(1) + ">", "data-cls") or "",
                             "label": strip_tags(m.group(2)),
                             "active": "is-active" in (attr("<x " + m.group(1) + ">", "class") or "")})
    for m in re.finditer(r'<div class="cls-tree" data-cls="([^"]*)"([^>]*)>', nav):
        start = m.start()
        end = block_end(nav, start)
        side["trees"].append({"cls": m.group(1), "rows": rows_in(nav[start:end], front=False),
                              "hidden": "hidden" in m.group(2)})

    # рейка плоская там, где нет деревьев: front-пункты и главы различаются классом
    if side["trees"]:
        head = nav[:nav.find('<div class="cls-tree"')]
    else:
        head = nav
    side["front"] = rows_in(head, front=True)
    if not side["trees"]:
        side["rows"] = rows_in(nav, front=False)
    return side


def resolve(page_rel, href, path=None):
    """Куда ведёт href со страницы page_rel (путь относительно корня книги)."""
    if not href:
        return None
    if re.match(r"^[a-z]+:", href) or href.startswith("//") or href.startswith("#"):
        return href
    base = posixpath.dirname(page_rel)
    return posixpath.normpath(posixpath.join(base, href.split("#")[0].split("?")[0]))


# ── навигация титула: в демо рейка одна на всю книгу ──────────────────────────
LANG_DIRS = ("az", "ru", "en", "tr")


def rebase_href(href, from_rel, to_rel):
    """Адрес со страницы from_rel → тот же адрес со страницы to_rel (обе — от корня книги)."""
    if not href or re.match(r"^[a-z]+:", href) or href.startswith("//") or href.startswith("#"):
        return href
    clean, tail = href, ""
    for sep in ("#", "?"):
        i = href.find(sep)
        if i >= 0:
            clean, tail = href[:i], href[i:]
            break
    target = resolve(from_rel, clean)
    if not target:
        return href
    base = posixpath.dirname(to_rel) or "."
    return posixpath.relpath(target, base) + tail


def rebase_side(side, from_rel, to_rel):
    """Все адреса рейки пересчитываем на каталог титула."""
    for group in (side["front"], side["rows"]):
        for r in group:
            r["href"] = rebase_href(r.get("href"), from_rel, to_rel)
    for tree in side["trees"]:
        for r in tree["rows"]:
            r["href"] = rebase_href(r.get("href"), from_rel, to_rel)
    return side


def donor_rel(book, page_rel):
    """Соседняя страница книги — донор её рейки: сначала та же папка, потом подпапки
    (кроме языковых каталогов — английская рейка не должна попасть на русский титул)."""
    base = os.path.join(ROOT, book)
    d = posixpath.dirname(page_rel)
    abs_d = os.path.join(base, d.replace("/", os.sep)) if d else base
    if not os.path.isdir(abs_d):
        return None
    for f in sorted(os.listdir(abs_d)):
        if f.endswith(".html") and f != posixpath.basename(page_rel) \
                and os.path.isfile(os.path.join(abs_d, f)):
            return posixpath.join(d, f) if d else f
    for sub in sorted(os.listdir(abs_d)):
        abs_sub = os.path.join(abs_d, sub)
        if sub in LANG_DIRS or not os.path.isdir(abs_sub):
            continue
        for f in sorted(os.listdir(abs_sub)):
            if f.endswith(".html"):
                return posixpath.join(d, sub, f) if d else posixpath.join(sub, f)
    return None


def empty_side():
    return {"front": [], "rows": [], "trees": [], "tabs": []}


def cover_side(book, page_rel, base=None):
    """Рейка титула: те же пункты, что на страницах книги, с адресами от титула."""
    r = donor_rel(book, page_rel)
    if not r:
        return empty_side()
    side = parse_sidebar(read_source(posixpath.join(book, r), base), None, book, r)
    if not (side["front"] or side["rows"] or side["trees"]):
        return empty_side()
    # «Главная» на странице-доноре местами ведёт на неё саму (адрес потерян при
    # пересборке). На титуле этот пункт обязан вести на титул — в демо он и активен.
    self_href = posixpath.basename(page_rel) or "index.html"
    self_rows = [i for i, f in enumerate(side["front"]) if resolve(r, f.get("href")) == r]
    rebase_side(side, r, page_rel)
    for i in self_rows:
        side["front"][i]["href"] = self_href
    return side


def apply_toc_names(p):
    """Подписи пунктов рейки на титуле берём из оглавления той же страницы: в демо
    рейка и оглавление подписаны одинаково, а в старой разметке подписи рейки были
    обрезаны под узкую колонку («III. … birinci bölmə», «от автора»)."""
    toc = {}
    for r in cover_toc(p):
        if r.get("href") and not r.get("part") and r.get("name"):
            k = resolve(p["rel"], r["href"])
            if k:
                toc.setdefault(k, r["name"])
    if not toc:
        return p
    groups = [p["side"]["rows"]] + [t["rows"] for t in p["side"]["trees"]]
    for group in groups:
        for r in group:
            k = resolve(p["rel"], r.get("href"))
            if k in toc:
                r["name"] = toc[k]
    return p


def cover_toc_side(p):
    """Запасной источник для титула: его же оглавление .bk-toc__list (если донора нет)."""
    side = empty_side()
    blk = p["raw"]
    i = blk.find('<ol class="bk-toc__list">')
    if i < 0:
        return side
    blk = blk[i:blk.find("</ol>", i)]
    for m in re.finditer(r'<li class="([^"]*)">(.*?)</li>', blk, re.S):
        cls, inner = m.group(1), m.group(2)
        a = re.search(r"<a\b([^>]*)>", inner)
        href = attr("<x " + a.group(1) + ">", "href") if a else None
        name = strip_tags((re.findall(r'<span class="bk-toc__t">(.*?)</span>', inner, re.S) or [""])[0])
        num = strip_tags((re.findall(r'<span class="bk-toc__n">(.*?)</span>', inner, re.S) or [""])[0])
        if not name:
            continue
        if not href:
            side["front"].append({"href": "", "name": name, "code": ""})
        else:
            side["rows"].append({"href": href, "name": name, "code": num, "level": 1,
                                 "active": False})
    return side


def parse_content_bk(p, raw):
    """Содержимое УЖЕ пересобранного каркаса (глава `.bk-chead` / титул `.bk-tp`) —
    чтобы повторный прогон не терял заголовок, тело, примечания и пред/след."""
    if '<section class="bk-tp"' in raw:
        p["kind"] = "cover"
        rest = re.search(r'<div class="bk-read bk-read--rest">', raw)
        if rest:
            p["body"] = div_inner(raw, rest.start()).strip()
        return

    m = re.search(r'<header class="bk-chead">(.*?)</header>', raw, re.S)
    if not m:
        return
    blk = m.group(1)
    p["chead"] = {
        "code": strip_tags((re.findall(r'<span class="bk-chead__n">(.*?)</span>', blk, re.S) or [""])[0]),
        "title": strip_tags((re.findall(r'<h1 class="bk-chead__h1">(.*?)</h1>', blk, re.S) or [""])[0]),
        "en": strip_tags((re.findall(r'<p class="bk-chead__en">(.*?)</p>', blk, re.S) or [""])[0]),
        "sub": strip_tags((re.findall(r'<p class="bk-chead__sub">(.*?)</p>', blk, re.S) or [""])[0]),
    }
    cr = re.search(r'<nav class="bk-crumb"[^>]*>(.*?)</nav>', raw, re.S)
    if cr:
        a = re.search(r'<a\b([^>]*)>(.*?)</a>', cr.group(1), re.S)
        if a:
            p["crumb"] = {"href": attr("<x " + a.group(1) + ">", "href"), "name": strip_tags(a.group(2))}
    mn = re.search(r'<ul class="bk-toc__list">(.*?)</ul>', raw, re.S)
    if mn:
        p["menu"] = [{"href": attr("<x " + a.group(1) + ">", "href"),
                      "code": strip_tags((re.findall(r'<span class="bk-toc__n">(.*?)</span>', a.group(2), re.S) or [""])[0]),
                      "name": strip_tags((re.findall(r'<span class="bk-toc__t">(.*?)</span>', a.group(2), re.S) or [""])[0])}
                     for a in re.finditer(r'<a\b([^>]*)>(.*?)</a>', mn.group(1), re.S)]
    for nm in re.finditer(r'<section class="bk-notes">(.*?)</section>', raw, re.S):
        blk2 = nm.group(1)
        items = [{"n": strip_tags(n2.group(1)),
                  "t": strip_tags((re.findall(r'<span class="bk-note__t">(.*?)</span>', n2.group(2), re.S) or [""])[0])}
                 for n2 in re.finditer(r'<p class="bk-note"><span class="bk-note__n">(.*?)</span>(.*?)</p>', blk2, re.S)]
        if items:
            p["notes"].append({
                "title": strip_tags((re.findall(r'<h2[^>]*>(.*?)</h2>', blk2, re.S) or [""])[0]),
                "items": items})
    rd = re.search(r'<div class="bk-read">', raw)
    if rd:
        p["body"] = div_inner(raw, rd.start()).strip()
    pn = re.search(r'<nav class="bk-pn"[^>]*>(.*?)</nav>', raw, re.S)
    if pn:
        up = re.search(r'<p class="bk-pn__up"><a\b([^>]*)>(.*?)</a></p>', pn.group(1), re.S)
        if up:
            p["up"] = {"href": attr("<x " + up.group(1) + ">", "href"), "name": strip_tags(up.group(2))}
        links = [{"href": attr("<x " + a.group(1) + ">", "href"),
                  "name": strip_tags((re.findall(r'<span class="bk-pn__t">(.*?)</span>', a.group(2), re.S) or [""])[0]),
                  "dir": strip_tags((re.findall(r'<span class="bk-pn__dir">(.*?)</span>', a.group(2), re.S) or [""])[0])}
                 for a in re.finditer(r'<a\b([^>]*)>(.*?)</a>', pn.group(1), re.S)]
        if len(links) > 0:
            p["prev"] = links[0]
        if len(links) > 1:
            p["next"] = links[1]


def parse_content(p, raw):
    """Содержимое: хлебная крошка, шапка главы, тело, примечания, пред/след."""
    p.update({"crumb": None, "chead": None, "body": "", "notes": [], "prev": None,
              "next": None, "up": None, "kind": "chapter", "menu": None, "cover": None})
    i = raw.find('<div class="content-wrap">')
    if i < 0:
        parse_content_bk(p, raw)      # уже пересобранный каркас концепта
        return
    inner = div_inner(raw, i)

    # хлебная крошка
    m = re.search(r'<nav class="crumb">(.*?)</nav>', inner, re.S)
    if m:
        a = re.search(r'<a\b([^>]*)>(.*?)</a>', m.group(1), re.S)
        if a:
            p["crumb"] = {"href": attr("<x " + a.group(1) + ">", "href"),
                          "name": strip_tags(a.group(2)).lstrip("‹‹ ").strip()}
        inner = inner.replace(m.group(0), "\n")

    # шапка главы — четыре варианта разметки в книгах
    chead = {}
    m = re.search(r'<header class="chap-head">(.*?)</header>', inner, re.S)
    if m:
        blk = m.group(1)
        rng = re.search(r'<span class="chap-range">(.*?)</span>', blk, re.S)
        ttl = re.search(r'<span class="chap-title">(.*?)</span>', blk, re.S)
        en = re.search(r'<div class="chap-en">(.*?)</div>', blk, re.S)
        sub = re.search(r'<p class="chap-sub">(.*?)</p>', blk, re.S)
        chead = {"code": strip_tags(rng.group(1)) if rng else "",
                 "title": strip_tags(ttl.group(1)) if ttl else "",
                 "en": strip_tags(en.group(1)) if en else "",
                 "sub": strip_tags(sub.group(1)) if sub else ""}
        inner = inner.replace(m.group(0), "\n")

    if not chead:
        m = re.search(r'<h1 class="chap-title-wrap"[^>]*>(.*?)</h1>', inner, re.S)
        if m:
            rng = re.search(r'<span class="chap-range">(.*?)</span>', m.group(1), re.S)
            ttl = re.search(r'<span class="chap-title">(.*?)</span>', m.group(1), re.S)
            chead = {"code": strip_tags(rng.group(1)) if rng else "",
                     "title": strip_tags(ttl.group(1) if ttl else m.group(1)), "en": "", "sub": ""}
            inner = inner.replace(m.group(0), "\n")

    if not chead:
        m = re.search(r'<h1[^>]*class="(?:h-chapter|h-section|h-bolme|h-disorder)[^"]*"[^>]*>(.*?)</h1>', inner, re.S)
        if m:
            chead = {"code": "", "title": strip_tags(m.group(1)), "en": "", "sub": ""}
            inner = inner.replace(m.group(0), "\n")

    if not chead:
        m = re.search(r'<table class="dh">', inner)
        if m:
            t_end = inner.find("</table>", m.start()) + len("</table>")
            tbl = inner[m.start():t_end]
            main = re.search(r'<tr class="dh-main">(.*?)</tr>', tbl, re.S)
            if main:
                code = re.search(r'<span class="dh-code">(.*?)</span>', main.group(1), re.S)
                name = re.search(r'<h1[^>]*>(.*?)</h1>', main.group(1), re.S)
                en = re.search(r'<div class="dh-en"[^>]*>(.*?)</div>', main.group(1), re.S)
                chead = {"code": strip_tags(code.group(1)) if code else "",
                         "title": strip_tags(name.group(1)) if name else "",
                         "en": strip_tags(en.group(1)) if en else "", "sub": ""}
                rest = tbl.replace(main.group(0), "")
                rest = re.sub(r'<table class="dh">(.*?)</table>', lambda mm: '<table class="bk-codes">%s</table>' % mm.group(1), rest, flags=re.S)
                inner = inner.replace(tbl, rest + "\n")

    p["chead"] = chead

    # примечания
    m = re.search(r'<div class="notes">', inner)
    while m:
        end = block_end(inner, m.start())
        blk = inner[m.start():end]
        ttl = re.search(r'<h2[^>]*class="notes-title"[^>]*>(.*?)</h2>', blk, re.S)
        notes = []
        for nm in re.finditer(r'<p class="note">(.*?)</p>', blk, re.S):
            n = re.search(r'<span class="note-n">(.*?)</span>', nm.group(1), re.S)
            body = re.sub(r'<span class="note-n">.*?</span>', "", nm.group(1), flags=re.S)
            notes.append({"n": strip_tags(n.group(1)) if n else "",
                          "t": body.strip()})
        if notes:
            p["notes"].append({"title": strip_tags(ttl.group(1)) if ttl else ui(p["lang"])["toc"],
                               "items": notes})
        inner = inner[:m.start()] + inner[end + len("</div>"):]
        m = re.search(r'<div class="notes">', inner)

    # меню главы (klinik): список расстройств главы
    m = re.search(r'<div class="chapter-menu">', inner)
    if m:
        end = block_end(inner, m.start())
        blk = inner[m.start():end + len("</div>")]
        p["menu"] = [{"href": attr("<x " + a.group(1) + ">", "href"),
                      "code": strip_tags((re.search(r'<span class="ch-code">(.*?)</span>', a.group(2), re.S) or [""])[0]),
                      "name": strip_tags((re.search(r'<span class="ch-name">(.*?)</span>', a.group(2), re.S) or [""])[0])}
                     for a in re.finditer(r'<a\b([^>]*class="ch-disorder"[^>]*)>(.*?)</a>', blk, re.S)]
        inner = inner[:m.start()] + inner[end + len("</div>"):]

    # пред/след: .d-nav или .page-nav (klinik). В .d-nav классы могут отсутствовать,
    # поэтому направление определяем по положению относительно ссылки «вверх».
    m = re.search(r'<nav class="d-nav">(.*?)</nav>', inner, re.S) or \
        re.search(r'<nav class="page-nav">(.*?)</nav>', inner, re.S)
    if m:
        blk = m.group(1)
        anchors = []
        for a in re.finditer(r'<a\b([^>]*)>(.*?)</a>', blk, re.S):
            tag = "<x " + a.group(1) + ">"
            cls = (attr(tag, "class") or "").split()
            name = (re.findall(r'<span class="(?:dn-name|pnav-title)">(.*?)</span>', a.group(2), re.S) or [None])[0]
            item = {"href": attr(tag, "href"),
                    "name": strip_tags(name if name is not None else a.group(2)).lstrip("↑←→ ").strip(),
                    "dir": strip_tags((re.findall(r'<span class="pnav-dir">(.*?)</span>', a.group(2), re.S) or [""])[0]).strip("← → ").strip(),
                    "cls": cls, "pos": a.start()}
            anchors.append(item)
        up = [x for x in anchors if "up" in x["cls"]]
        if up:
            p["up"] = {"href": up[0]["href"], "name": up[0]["name"]}
        up_pos = up[0]["pos"] if up else -1
        rest = [x for x in anchors if "up" not in x["cls"]]
        prevs = [x for x in rest if "prev" in x["cls"]] or [x for x in rest if x["pos"] < up_pos]
        nexts = [x for x in rest if "next" in x["cls"]] or [x for x in rest if x["pos"] > up_pos]
        p["prev"] = prevs[-1] if prevs else None
        p["next"] = nexts[0] if nexts else None
        for k in ("prev", "next"):
            if p[k]:
                p[k].pop("cls", None)
                p[k].pop("pos", None)
        inner = inner.replace(m.group(0), "\n")

    # титул книги (обложка): титульный блок и оглавление перерисовываются концептом,
    # остальное содержимое (предисловие, карточки переходов) сохраняем как есть
    if 'class="book-toc"' in inner:
        p["kind"] = "cover"
        m = re.search(r'<div class="home-hero">', inner)
        if m:
            inner = inner[:m.start()] + inner[block_end(inner, m.start()) + len("</div>"):]
        m = re.search(r'<section class="book-toc">', inner)
        if m:
            inner = inner[:m.start()] + inner[block_end(inner, m.start(), "section") + len("</section>"):]

    p["body"] = inner.strip()


# ── сборка новой страницы ─────────────────────────────────────────────────────
def head_html(p, cover=False):
    lang = p["lang"]
    attrs = ['lang="%s"' % esc(lang)]
    if p["declared"]:
        attrs.append('data-langs="%s"' % esc(",".join(p["declared"])))
    for code in ("az", "ru", "en", "tr"):
        if code in p["lang_urls"]:
            attrs.append('data-lang-url-%s="%s"' % (code, esc(p["lang_urls"][code])))
    if p["avail"]:
        attrs.append('data-lang-avail="%s"' % esc(" ".join(p["avail"])))
    out = ['<!doctype html>', '<html %s>' % " ".join(attrs), "<head>",
           '<meta charset="UTF-8">',
           '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
           '<meta name="theme-color" content="#07090E">']
    if p["desc"]:
        out.append('<meta name="description" content="%s">' % esc(p["desc"]))
    if p["keywords"]:
        out.append('<meta name="keywords" content="%s">' % esc(p["keywords"]))
    if p["robots"]:
        out.append('<meta name="robots" content="%s">' % esc(p["robots"]))
    out.append("<title>%s</title>" % esc(p["title"]))
    if p["canonical"]:
        out.append('<link rel="canonical" href="%s">' % esc(p["canonical"]))
    for code, href in p["hreflang"]:
        if code and href:
            out.append('<link rel="alternate" hreflang="%s" href="%s">' % (esc(code), esc(href)))
    for k, v in p["og"].items():
        out.append('<meta property="og:%s" content="%s">' % (esc(k), esc(v)))
    for js in p["jsonld"]:
        out.append('<script type="application/ld+json">%s</script>' % js.strip())
    out += ['<link rel="preconnect" href="https://fonts.googleapis.com">',
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
            '<link href="%s&display=swap" rel="stylesheet">' % FONT_URL,
            '<link rel="stylesheet" href="%s">' % CSS_BOOK,
            '<link rel="stylesheet" href="%s">' % CSS_CONTENT]
    out.append("</head>")
    return "\n".join(out)


def langs_html(p, cls="bk-langs"):
    """Переключатель языков: реальные ссылки на языковые версии (в бою это отдельные каталоги)."""
    lang = p["lang"]
    avail = p["avail"] or [lang]
    if len(avail) < 2:
        return ""
    out = []
    for code in avail:
        if code == lang:
            out.append('<span class="bk-lang is-on" aria-current="true">%s</span>' % LANG_TITLE.get(code, code.upper()))
            continue
        href = p["alt"].get(code)
        if not href:
            continue
        href = re.sub(r"^https?://ragimoff\.org", "", href) or "/"
        out.append('<a class="bk-lang" href="%s" hreflang="%s">%s</a>' % (esc(href), code, LANG_TITLE.get(code, code.upper())))
    if len(out) < 2:
        return ""
    return '\n        '.join(out)


def header_html(p, with_langs=True, extra=""):
    lang = p["lang"]
    L = ui(lang)
    title = nice_case(p["book_title"], p["lang"]) or p["title"]
    meta = p["book_meta"]
    return '''  <header class="bk-hdr">
    <div class="bk-hdr__in">
      <a class="bk-logo" href="/">
        <span class="bk-logo__t">RAGIMOFF<em>.</em></span>
        <span class="bk-logo__s">Peşəkar nüfuzun ünvanı</span>
      </a>
      <span class="bk-hdr__sep" role="presentation"></span>
      <a class="bk-book" href="%(home)s">
        <span class="bk-book__t">%(title)s</span>
        <span class="bk-book__m">%(meta)s</span>
      </a>
      <div class="bk-hdr__sp"></div>
      <div class="bk-langs" role="group" aria-label="%(langs)s">
        %(langs_block)s
      </div>
      %(extra)s<button class="bk-btn" type="button" data-order="%(ordertitle)s" onclick="openKitabModal()">%(order)s</button>
      <button class="bk-burger bk-btn" id="bk-burger" type="button" aria-label="%(nav)s" aria-expanded="false">
        <svg width="16" height="12" viewBox="0 0 16 12" aria-hidden="true" fill="currentColor">
          <rect width="16" height="1.6" rx=".8"/><rect y="5.2" width="16" height="1.6" rx=".8"/><rect y="10.4" width="16" height="1.6" rx=".8"/>
        </svg>
      </button>
    </div>
  </header>''' % {
        "home": esc(p["home_href"]),
        "title": esc(title),
        "meta": esc(meta),
        "langs": esc(L["langs"]),
        "langs_block": langs_html(p) if with_langs else "",
        "extra": extra,
        "ordertitle": esc(title),
        "order": esc(L["order"]),
        "nav": esc(L["nav"]),
    }


def row_html(item, on=False, sub=False, sec=False, lang="az"):
    cls = "bk-row"
    if item.get("front"):
        cls += " bk-row--front"
    if sec:
        cls += " bk-row--sec"
    if sub:
        cls += " bk-row--sub"
    if on:
        cls += " is-on"
    n = esc(item.get("code") or "")
    t = esc(nice_case(item.get("name") or "", lang))
    if item.get("href"):
        return ('<a class="%s" href="%s"><span class="bk-row__n">%s</span>'
                '<span class="bk-row__t">%s</span></a>' % (cls, esc(item["href"]), n, t))
    return ('<span class="%s"><span class="bk-row__n">%s</span>'
            '<span class="bk-row__t">%s</span></span>' % (cls, n, t))


def sidebar_html(p):
    """Сайдбар-оглавление: front-пункты, разделитель, главы (номер отдельной колонкой)."""
    L = ui(p["lang"])
    lang = p["lang"]
    rows = []
    for f in p["side"]["front"]:
        rows.append(row_html({"href": f["href"], "name": f["name"], "code": "", "front": True},
                             on=is_current(p, f["href"]), lang=lang))
    if rows:
        rows.append('<div class="bk-sb__sep" role="presentation"></div>')

    if p["side"]["trees"]:
        tabs = '<div class="cls-tabs cls-tabs-side" role="tablist">%s</div>' % "".join(
            '<button class="cls-tab%s" type="button" data-cls="%s" onclick="setCls(\'%s\')">%s</button>'
            % (" is-active" if t["active"] else "", esc(t["cls"]), esc(t["cls"]), esc(t["label"]))
            for t in p["side"]["tabs"])
        rows.append(tabs)
        for tree in p["side"]["trees"]:
            inner = []
            for r in tree["rows"]:
                inner.append(row_html(r, on=is_current(p, r["href"]),
                                      sub=(r["level"] > 1), sec=(r["level"] == 1), lang=lang))
            rows.append('<div class="cls-tree" data-cls="%s"%s>\n%s\n</div>'
                        % (esc(tree["cls"]), " hidden" if tree.get("hidden") else "", "\n".join(inner)))
    else:
        for r in p["side"]["rows"]:
            rows.append(row_html(r, on=is_current(p, r["href"]), lang=lang))

    return '''    <aside class="bk-sb%(wide)s" id="bk-sb">
      <div class="bk-sb__hdr">
        <a class="bk-sb__back" href="/books/">%(back)s</a>
        <button class="bk-sb__x" id="bk-close" type="button" aria-label="Bağla / Закрыть">
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true">
            <path d="M1 1l12 12M13 1L1 13"/></svg>
        </button>
      </div>
      <div class="bk-sb__langs" role="group" aria-label="%(langs)s">
        %(langs_block)s
      </div>
      <nav class="bk-sb__nav" aria-label="%(nav)s">
        %(rows)s
      </nav>
    </aside>''' % {
        "wide": " bk-sb--wide" if any(len(r.get("code") or "") > 4 for r in p["side"]["rows"]) or
                any(len(x.get("code") or "") > 4 for t in p["side"]["trees"] for x in t["rows"]) else "",
        "back": esc(L["back"]),
        "langs": esc(L["langs"]),
        "langs_block": langs_html(p),
        "nav": esc(L["nav"]),
        "rows": "\n        ".join(rows),
    }


def is_current(p, href):
    if not href:
        return False
    target = resolve(p["rel"], href)
    return target is not None and target == p["rel"]


def crumb_html(p):
    """Хлебная крошка: возврат к книге (на обложке не нужна)."""
    if p["crumb"] and p["crumb"].get("href"):
        return ('      <nav class="bk-crumb" aria-label="Naviqasiya">\n'
                '        <a href="%s">%s</a>\n'
                '        <span class="bk-crumb__sep" aria-hidden="true">/</span>\n'
                '      </nav>\n' % (esc(p["crumb"]["href"]), esc(p["crumb"]["name"] or p["book_title"])))
    home = p["home_href"]
    return ('      <nav class="bk-crumb" aria-label="Naviqasiya">\n'
            '        <a href="%s">%s</a>\n'
            '        <span class="bk-crumb__sep" aria-hidden="true">/</span>\n'
            '      </nav>\n' % (esc(home), esc(nice_case(p["book_title"], p["lang"]))))


def notes_html(p):
    out = []
    for blk in p["notes"]:
        items = "\n".join(
            '          <p class="bk-note"><span class="bk-note__n">%s</span>'
            '<span class="bk-note__t">%s</span></p>' % (esc(n["n"]), n["t"].strip())
            for n in blk["items"])
        out.append('''      <section class="bk-notes">
        <h2 class="bk-label bk-notes__h">%s</h2>
%s
      </section>''' % (esc(nice_case(blk["title"], p["lang"])), items))
    return "\n".join(out)


def menu_html(p):
    if not p.get("menu"):
        return ""
    rows = []
    for i, m in enumerate(p["menu"], start=1):
        code = (m["code"] or "").strip()
        num = code if re.match(r"^[0-9A-Za-z\u0400-\u04FF.\-]{2,6}$", code) and code != "—" else "%02d" % i
        rows.append('''          <li class="bk-toc__row">
            <a class="bk-toc__a" href="%s">
              <span class="bk-toc__n">%s</span>
              <span class="bk-toc__t">%s</span>
            </a>
          </li>''' % (esc(m["href"]), esc(num), esc(nice_case(m["name"], p["lang"]))))
    return '      <ul class="bk-toc__list">\n%s\n      </ul>\n' % "\n".join(rows)


def as_num(code):
    m = re.match(r"^(\d{1,2})$", (code or "").strip())
    return m.group(1).zfill(2) if m else ""


def pn_html(p):
    L = ui(p["lang"])
    up = p["up"] or {"href": p["home_href"], "name": L["up"]}
    prev, nxt = p["prev"], p["next"]

    def block(item, side):
        direction = L["prev"] if side == "prev" else L["next"]
        if item and item.get("href"):
            d = item.get("dir") or direction
            return ('          <a class="bk-pn__a" href="%s">\n'
                    '            <span class="bk-pn__dir">%s</span>\n'
                    '            <span class="bk-pn__t">%s</span>\n'
                    '          </a>' % (esc(item["href"]), esc(d), esc(item["name"] or "—")))
        return ('          <span class="bk-pn__a" aria-disabled="true">\n'
                '            <span class="bk-pn__dir">%s</span>\n'
                '            <span class="bk-pn__t">—</span>\n'
                '          </span>' % esc(direction))

    heads = '''      <nav class="bk-pn" aria-label="Fəsil keçidi / Переход между главами">
        <p class="bk-pn__up"><a href="%s">%s</a></p>''' % (
        esc(up["href"] or p["home_href"]), esc(nice_case(up["name"] or L["up"], p["lang"])))
    if not prev and not nxt:
        return heads + "\n      </nav>"
    return heads + '''
        <div class="bk-pn__grid">
%s
%s
        </div>
      </nav>''' % (block(prev, "prev"), block(nxt, "next"))


def footer_html(p):
    L = ui(p["lang"])
    nav = "\n          ".join('<a href="%s">%s</a>' % (esc(h), esc(t)) for t, h in L["foot"])
    return '''      <footer class="bk-ft">
        <span class="bk-ft__c">RAGIMOFF<em style="color:var(--acc);font-style:normal">.</em></span>
        <nav class="bk-ft__nav" aria-label="Futermenü">
          %s
        </nav>
        <span class="bk-ft__c">© 2026 RAGIMOFF</span>
      </footer>''' % nav


SCRIPT = '''<script>
/* Концепт: два настоящих поведения страницы — выдвижное меню и полоса чтения.
   В бою языки остаются отдельными каталогами (/ru/, /en/), как сейчас: языковые
   кнопки в шапке — настоящие ссылки на версию этого языка. */
(function () {
  var sb = document.getElementById('bk-sb'),
      scrim = document.getElementById('bk-scrim'),
      burger = document.getElementById('bk-burger'),
      close = document.getElementById('bk-close');

  function drawer(open) {
    if (!sb) return;
    sb.classList.toggle('is-open', open);
    if (scrim) scrim.classList.toggle('is-open', open);
    document.documentElement.classList.toggle('bk-lock', open);
    if (burger) burger.setAttribute('aria-expanded', open ? 'true' : 'false');
  }
  if (burger) burger.addEventListener('click', function () { drawer(true); });
  if (close) close.addEventListener('click', function () { drawer(false); });
  if (scrim) scrim.addEventListener('click', function () { drawer(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') drawer(false); });

  var bar = document.getElementById('bk-prog');
  if (bar) {
    var upd = function () {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.width = (h > 0 ? Math.min(100, window.scrollY / h * 100) : 0) + '%';
    };
    window.addEventListener('scroll', upd, { passive: true });
    window.addEventListener('resize', upd);
    upd();
  }
})();
</script>'''


def keep_scripts(raw):
    """Скрипты страницы, которые нужны и в новом каркасе: заказ книги, вкладки классификаций."""
    out = []
    for m in re.finditer(r"<script>(.*?)</script>", raw, re.S):
        body = m.group(1)
        if ("openKitabModal" in body or "setCls" in body or "sifaris=1" in body) \
                and "ALL_PAGES" not in body and "toggleSb" not in body:
            out.append("<script>%s</script>" % body.strip())
    return out


def modal_html(raw):
    """Модал заказа книги переносится как есть (его ids использует скрипт заказа)."""
    m = re.search(r'<div id="kitab-modal" class="kitab-overlay"', raw)
    if not m:
        return ""
    end = block_end(raw, m.start())
    return raw[m.start():end + len("</div>")]


def render(p):
    if p["kind"] == "cover":
        apply_toc_names(p)
        main = cover_main(p)
        body_cls = "bk bk-cover"
        sb = sidebar_html(p)          # титул тоже с рейкой — как в демо (book-cover.html)
        prog = ""
    else:
        main = page_main(p)
        body_cls = "bk bk-chapter"
        sb = sidebar_html(p)
        prog = '<div class="bk-prog" role="presentation"><div class="bk-prog__f" id="bk-prog"></div></div>'
    shell = '''<div class="bk-scrim" id="bk-scrim"></div>
<div class="bk-shell">
%s
  <main class="bk-main">
    <div class="bk-col">
%s
%s
    </div>
  </main>
</div>''' % (sb, main, footer_html(p))
    scripts = [SCRIPT] + keep_scripts(p["raw"])
    return "\n".join([
        head_html(p),
        '<body class="%s">' % body_cls,
        header_html(p),
        prog,
        shell,
        "",
        modal_html(p["raw"]),
        "\n".join(scripts),
        "</body>",
        "</html>",
        "",
    ])


def cover_main(p):
    """Титул книги + оглавление (сайдбара на титуле нет — по концепту)."""
    L = ui(p["lang"])
    title, author, year, sub = cover_texts(p)
    toc = cover_toc(p)
    n = len([r for r in toc if r["href"]])
    rows = []
    for r in toc:
        cls = "bk-toc__row" + (" bk-toc__row--front" if not r["href"] else "")
        inner = '<span class="bk-toc__t">%s%s</span>' % (
            esc(nice_case(r["name"], p["lang"])),
            '<span class="bk-toc__r">%s</span>' % esc(r["range"]) if r.get("range") else "")
        if r["href"]:
            body = ('<a class="bk-toc__a" href="%s"><span class="bk-toc__n">%s</span>%s</a>'
                    % (esc(r["href"]), esc(r["num"] or ""), inner))
        else:
            body = ('<span class="bk-toc__a" aria-disabled="true"><span class="bk-toc__n"></span>%s</span>' % inner)
        rows.append('          <li class="%s">%s</li>' % (cls, body))
    notes = notes_html(p)
    rest = re.sub(r"</main>", "", p["body"]).strip()      # лишний </main> из старой разметки
    rest_html = ('\n      <div class="bk-read bk-read--rest">\n%s\n      </div>\n' % rest) if rest else "\n"
    return '''      <section class="bk-tp">
        <div class="bk-tp__mark" role="presentation"></div>
        <div class="bk-tp__box">
          <h1 class="bk-tp__title">%(title)s</h1>%(sub)s
          <p class="bk-tp__meta">
            <span class="bk-tp__author">%(author)s</span>
            <span class="bk-tp__year">%(year)s</span>
          </p>
        </div>
      </section>

      <section class="bk-toc" aria-labelledby="bk-toc-h">
        <div class="bk-toc__hdr">
          <h2 class="bk-label" id="bk-toc-h">%(lbl)s</h2>
          <span class="bk-label">%(cnt)s</span>
        </div>
        <ol class="bk-toc__list">
%(rows)s
        </ol>
      </section>%(rest)s%(notes)s
''' % {
        "title": esc(nice_case(title, p["lang"])),
        "sub": ('\n          <p class="bk-tp__sub">%s</p>' % esc(sub)) if sub else "",
        "author": esc(author),
        "year": esc(year),
        "lbl": esc(L["toc"]),
        "cnt": esc("%d %s" % (n, plural(p["lang"], n))),
        "rows": "\n".join(rows),
        "notes": notes,
        "rest": rest_html,
    }


def cover_texts(p):
    """Название / автор / год титула. Берём из титульного блока, откат — подпись в шапке."""
    raw = p["raw"]
    m = re.search(r'<div class="home-hero">(.*?)</div>', raw, re.S)
    hero = m.group(1) if m else ""
    if not hero and '<h1 class="bk-tp__title">' in raw:
        # уже пересобранный титул: тексты берём из него самого
        tp = re.search(r'<section class="bk-tp">(.*?)</section>', raw, re.S)
        tp = tp.group(1) if tp else raw
        return (strip_tags((re.findall(r'<h1 class="bk-tp__title">(.*?)</h1>', tp, re.S) or [""])[0]),
                strip_tags((re.findall(r'<span class="bk-tp__author">(.*?)</span>', tp, re.S) or [""])[0]),
                strip_tags((re.findall(r'<span class="bk-tp__year">(.*?)</span>', tp, re.S) or [""])[0]),
                strip_tags((re.findall(r'<p class="bk-tp__sub">(.*?)</p>', tp, re.S) or [""])[0]))
    title = strip_tags((re.findall(r"<h1[^>]*>(.*?)</h1>", hero, re.S) or [""])[0]) or p["book_title"]
    subs = [strip_tags(x) for x in re.findall(r'<p class="sub"[^>]*>(.*?)</p>', hero, re.S)]
    years = re.findall(r'<p class="sub year"[^>]*>(.*?)</p>', hero, re.S)
    author = year = sub = ""
    if years:
        year = strip_tags(years[0])
        author = subs[0] if subs else ""
        sub = " · ".join(subs[1:]) if len(subs) > 1 else ""
    else:
        # года в титуле нет (книги К.Рагимова): подпись — это подзаголовок, а не автор
        sub = " · ".join(subs)
    meta = [x.strip() for x in (p["book_meta"] or "").split("·") if x.strip()]
    if not author and meta:
        # «XBT-11 · K.Rəhimov · 2026» — автор посередине; «Ziqmund Freyd · 1939» — в начале
        author = meta[1] if len(meta) >= 3 else meta[0]
    if not year and len(meta) > 1:
        year = meta[-1]
    return title, author, year, sub


def cover_toc(p):
    """Оглавление титула: список пунктов книги (номера — из сайдбара, дальше по порядку)."""
    raw = p["raw"]
    i = raw.find('<section class="book-toc">')
    if i < 0:
        return cover_toc_bk(raw)
    blk = raw[i:block_end(raw, i, "section")]
    codes, by_name = {}, {}
    all_rows = p["side"]["rows"] + [x for t in p["side"]["trees"] for x in t["rows"]]
    for r in all_rows:
        if r.get("href"):
            key = resolve(p["rel"], r["href"])
            if key:
                codes[key] = r.get("code") or ""
        if r.get("name"):
            by_name[key_of(r["name"])] = r
    out, seq = [], 0
    for m in re.finditer(r'<div class="(toc-chapter|toc-sub|toc-part)"', blk):
        kind = m.group(1)
        end = block_end(blk, m.start())
        inner = blk[blk.find(">", m.start()) + 1:end]
        a = re.search(r'<a\b([^>]*)>(.*?)</a>', inner, re.S)
        name = strip_tags((re.findall(r'<span class="toc-name">(.*?)</span>', inner, re.S) or [inner])[0])
        rng = strip_tags((re.findall(r'<span class="toc-range">(.*?)</span>', inner, re.S) or [""])[0])
        href = attr("<x " + a.group(1) + ">", "href") if a else None
        part = kind != "toc-chapter"        # подпись части/раздела — без номера
        num = ""
        if not href:
            # пункт без ссылки: ищем ту же страницу в сайдбаре (иначе ссылка терялась бы)
            twin = by_name.get(key_of(name))
            if twin:
                href = twin["href"]
        if href and not part:
            key = resolve(p["rel"], href)
            # номер из сайдбара берём только если он вида 01..99; иначе — по порядку
            cand = codes.get(key, "")
            num = cand if re.match(r"^\d{2}$", cand) else ""
            if not num:
                seq += 1
                num = "%02d" % seq
        out.append({"name": name, "href": href, "num": num, "range": rng, "part": part})
    return out


def cover_toc_bk(raw):
    """Оглавление УЖЕ пересобранного титула (`.bk-toc__list`) — повторный прогон не теряет список."""
    i = raw.find('<ol class="bk-toc__list">')
    if i < 0:
        return []
    blk = raw[i:raw.find("</ol>", i)]
    out = []
    for m in re.finditer(r'<li class="([^"]*)">(.*?)</li>', blk, re.S):
        cls, inner = m.group(1), m.group(2)
        a = re.search(r"<a\b([^>]*)>", inner)
        name = (re.findall(r'<span class="bk-toc__t">(.*?)</span>', inner, re.S) or [""])[0]
        rng = strip_tags((re.findall(r'<span class="bk-toc__r">(.*?)</span>', name, re.S) or [""])[0])
        name = re.sub(r'<span class="bk-toc__r">.*?</span>', "", name, flags=re.S)
        out.append({"name": strip_tags(name),
                    "href": attr("<x " + a.group(1) + ">", "href") if a else None,
                    "num": strip_tags((re.findall(r'<span class="bk-toc__n">(.*?)</span>', inner, re.S) or [""])[0]),
                    "range": rng,
                    "part": not a})
    return out


def key_of(name):
    """Ключ сравнения названий: без регистра и знаков."""
    return re.sub(r"[^0-9a-zа-яəğıöşüç]+", "", az_lower(name or "", "az"))


def page_main(p):
    chead = p["chead"] or {}
    code = chead.get("code") or ""
    if not code:
        for r in p["side"]["rows"] + [x for t in p["side"]["trees"] for x in t["rows"]]:
            if is_current(p, r.get("href")) and r.get("code"):
                code = r["code"]
                break
    top = ('        <p class="bk-chead__top">\n'
           '          <span class="bk-chead__n">%s</span>\n'
           '          <span class="bk-chead__rule" role="presentation"></span>\n'
           '        </p>\n' % esc(code) if code else
           '        <p class="bk-chead__top">\n'
           '          <span class="bk-chead__rule" role="presentation"></span>\n'
           '        </p>\n')
    en = ('        <p class="bk-chead__en">%s</p>\n' % esc(chead.get("en"))) if chead.get("en") else ""
    sub = ('        <p class="bk-chead__sub">%s</p>\n' % esc(chead.get("sub"))) if chead.get("sub") else ""
    head = ""
    if chead.get("title"):
        head = (crumb_html(p) +
                '      <header class="bk-chead">\n%s'
                '        <h1 class="bk-chead__h1">%s</h1>\n%s%s      </header>\n'
                % (top, esc(nice_case(chead["title"], p["lang"])), en, sub))
    else:
        head = crumb_html(p)
    body = p["body"].strip()
    if body:
        body = '      <div class="bk-read">\n%s\n      </div>\n' % body
    parts = [head]
    if p.get("menu"):
        parts.append(menu_html(p))
    if body:
        parts.append(body)
    parts.append(notes_html(p) + "\n" if p["notes"] else "")
    parts.append(pn_html(p))
    return "\n".join(x for x in parts if x and x.strip())


# ── обход книг ────────────────────────────────────────────────────────────────
def walk(book, src_base=None):
    base = os.path.join(ROOT, book)
    out = []
    for dp, dn, fn in os.walk(base):
        dn[:] = [d for d in dn if not any(s in d for s in SKIP_DIRS)]
        for f in sorted(fn):
            if not f.endswith(".html"):
                continue
            full = os.path.join(dp, f)
            raw = read_source(os.path.join(book, rel_of(full, base)).replace("\\", "/"), src_base)[:4000]
            if "http-equiv=\"refresh\"" in raw or "http-equiv=refresh" in raw:
                continue                      # страница-редирект: не трогаем
            out.append((full, rel_of(full, base)))
    return out


def rel_of(full, base):
    return os.path.relpath(full, base).replace("\\", "/")


def read_source(rel, base=None):
    """Исходная страница: из рабочего дерева или (если пересборка уже была) из коммита-донора."""
    if base:
        out = subprocess.run(["git", "show", "%s:%s" % (base, rel)], cwd=ROOT,
                             capture_output=True, text=True, encoding="utf-8", errors="replace")
        if out.returncode == 0:
            return out.stdout
    with open(os.path.join(ROOT, rel), encoding="utf-8", errors="replace") as fh:
        return fh.read()


def sync_cover(path, book, page_rel, base=None):
    """Титул: дописать рейку `.bk-sb` (если её нет) и убрать мусор старой разметки.
    Остальное содержимое не трогаем — так титулы правятся точечно, главы не при чём."""
    raw = read_source(posixpath.join(book, page_rel), base)
    out, fixed = drop_stray_main(raw)
    what = ["убрано лишнее </main>"] if fixed else []
    p = parse_page(path, book, page_rel, base)
    if not (p["side"]["front"] or p["side"]["rows"] or p["side"]["trees"]):
        return "нет навигации"
    apply_toc_names(p)
    sb = sidebar_html(p)
    i = out.find('<aside class="bk-sb')
    if i < 0:
        m = re.search(r'^([ \t]*)<main class="bk-main">', out, re.M)
        if not m:
            return "нет .bk-main"
        out = out[:m.start()] + sb + "\n\n" + out[m.start():]
        what.insert(0, "рейка .bk-sb")
    else:
        j = out.find("</aside>", i) + len("</aside>")
        if out[i:j].strip() != sb.strip():
            out = out[:i] + sb + out[j:]
            what.insert(0, "рейка .bk-sb переписана")
    if out == raw:
        return "без изменений"
    with open(path, "w", encoding="utf-8", newline="\r\n") as fh:
        fh.write(out)
    return ", ".join(what)


def drop_stray_main(raw):
    """В «остатке» старой разметки на титуле оставался лишний </main>: он закрывал
    .bk-main раньше времени, и футер уезжал ПОД сайдбар (в демо он внутри колонки).
    Настоящий </main> один — последний; лишние убираем."""
    if raw.count("</main>") < 2:
        return raw, False
    i = raw.rfind("</main>")
    return raw[:i].replace("</main>", "") + raw[i:], True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true", help="только отчёт")
    ap.add_argument("--book", action="append", help="одна книга (путь от корня репозитория)")
    ap.add_argument("--base", help="читать исходники из этого коммита (пересборка повторяема)")
    ap.add_argument("--sync-covers", action="store_true",
                    help="только титулы: дописать рейку .bk-sb (главы не трогать)")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()

    books = a.book or BOOKS
    if a.sync_covers:
        stat = {"изменено": 0, "без изменений": 0}
        for book in books:
            for full, rel in walk(book):
                if 'class="bk bk-cover"' not in read_source(posixpath.join(book, rel))[:6000]:
                    continue
                res = "dry-run" if a.dry else sync_cover(full, book, rel)
                key = ("без изменений" if res == "без изменений"
                       else ("проблемы" if res.startswith("нет ") else "изменено"))
                stat[key] = stat.get(key, 0) + 1
                if not a.quiet:
                    print("  %-24s %s/%s" % (res, book, rel))
        print("титулы: изменено %d | уже в порядке %d | проблемных %d"
              % (stat.get("изменено", 0), stat.get("без изменений", 0), stat.get("проблемы", 0)))
        if a.dry:
            print("(dry-run: файлы не изменены)")
        return
    stats = {"pages": 0, "cover": 0, "chapter": 0, "chars": 0, "toc": 0, "rows": 0,
             "langs": 0, "notes": 0, "bad_head": 0, "files": [], "skipped": []}
    for book in books:
        bp = 0
        for full, rel in walk(book, a.base):
            p = parse_page(full, book, rel, a.base)
            p["home_href"] = home_href(p)
            new = render(p)
            bp += 1
            stats["pages"] += 1
            stats[p["kind"]] = stats.get(p["kind"], 0) + 1
            stats["chars"] += len(strip_tags(p["body"]))
            stats["notes"] += sum(len(b["items"]) for b in p["notes"])
            if p["side"]["rows"] or p["side"]["trees"] or p["side"]["front"]:
                stats["rows"] += len(p["side"]["rows"]) + len(p["side"]["front"]) + \
                    sum(len(t["rows"]) for t in p["side"]["trees"])
            if p["avail"] and len(p["avail"]) > 1:
                stats["langs"] += 1
            if not (p["chead"] or {}).get("title") and p["kind"] != "cover":
                stats["bad_head"] += 1
            stats["files"].append((full, len(new), p["kind"]))
            if not a.dry:
                with open(full, "w", encoding="utf-8", newline="\r\n") as fh:
                    fh.write(new)
        if not a.quiet:
            print("%-40s %4d страниц" % (book, bp))
    print("итого страниц:", stats["pages"], "| обложек:", stats.get("cover", 0),
          "| внутренних:", stats.get("chapter", 0), "| без заголовка главы:", stats["bad_head"])
    print("пунктов навигации перенесено:", stats["rows"], "| блоков примечаний:", stats["notes"],
          "| страниц с переключателем языков:", stats["langs"])
    if a.dry:
        print("(dry-run: файлы не изменены)")


def home_href(p):
    """Относительная ссылка на титул книги со текущей страницы."""
    rel = p["rel"]
    depth = rel.count("/")
    return "../" * depth + "index.html"


if __name__ == "__main__":
    main()
