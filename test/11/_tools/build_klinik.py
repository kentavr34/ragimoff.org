# -*- coding: utf-8 -*-
"""Книга «Клиническая психиатрия» -> библиотека новой системы (12.11.2026).

Источник (только чтение): site/klinik-psixiatriya/ (az — корень, ru/, en/, tr/): 161 файл на язык, из них 137 настоящих страниц
(есть <main class="bk-main">), остальные — переадресации bolme-*.html и giris-yekun.html.
Результат (test/11/books/klinik-psixiatriya/):
    book.json         — паспорт: как у остальных книг + у пунктов toc поля id, lvl, code, en, sub; корневое поле trees —
                        дерево меню по трём классификациям (icd — МКБ-11, icd10 — МКБ-10, dsm — DSM-5) на каждом языке
    <язык>/NNN.html   — текст страницы по порядку чтения (без хлебных крошек, шапки главы, переходов и подвала)
Ссылки на другие страницы книги переписаны в read.html?b=klinik-psixiatriya&p=<имя файла без .html>[#якорь].
Показывает книгу общая читалка read.html?b=klinik-psixiatriya (assets/js/reader.js).
Запуск без аргументов; повторный запуск ничего не меняет. Картотеку books/index.json дополняет build_library.py."""
import io, os, re, sys, json, time
from urllib.parse import unquote
from bs4 import BeautifulSoup
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.abspath(os.path.join(D, "..", "..", "klinik-psixiatriya"))
BID = "klinik-psixiatriya"
OUT = os.path.join(D, "books", BID)
LANGS = ["az", "ru", "en", "tr"]
SUB = {"az": "", "ru": "ru", "en": "en", "tr": "tr"}

FRONT = ["index", "kitab-haqqinda", "mugeddime", "mundericat"]
BACK = ["elave-skalalar", "elave-acde", "yekun", "melumat", "terminoloji-luget", "abbreviatur"]

# сведения о книге (названия и описание — из JSON-LD и титула источника; печатные страницы — из каталога магазина)
BOOK = {
    "az": {"t": "Klinik Psixiatriya", "author": "Kənan Rəhimov", "kind": "Dərslik", "sub": "Psixiatrik pozuntuların diaqnostikası və müalicəsi üzrə klinik bələdçi. ICD-11, DSM-5.",
           "lab": ["Müəllif", "İlk nəşr", "Dillər", "Çap", "Fəsillər", "Pozuntular"], "print": "B5 · 822 səh."},
    "ru": {"t": "Клиническая психиатрия", "author": "Кенан Рагимов", "kind": "Учебник", "sub": "Клиническое руководство по диагностике и лечению психических расстройств. ICD-11, DSM-5.",
           "lab": ["Автор", "Первое издание", "Языки", "Печать", "Глав", "Расстройств"], "print": "B5 · 887 стр."},
    "en": {"t": "Clinical Psychiatry", "author": "Kenan Ragimov", "kind": "Textbook", "sub": "A clinical guide to the diagnosis and treatment of psychiatric disorders. ICD-11, DSM-5.",
           "lab": ["Author", "First edition", "Languages", "Print", "Chapters", "Disorders"], "print": "B5 · 790 pp."},
    "tr": {"t": "Klinik Psikiyatri", "author": "Kenan Ragimov", "kind": "Ders kitabı", "sub": "Psikiyatrik bozuklukların tanısı ve tedavisi üzerine klinik rehber. ICD-11, DSM-5.",
           "lab": ["Yazar", "İlk baskı", "Diller", "Baskı", "Bölüm", "Bozukluk"], "print": "B5"},
}
COVER = "/books/covers/klinik.jpg"
INDEX_TITLE = {"az": "Müəllifin müraciəti", "ru": "Обращение автора", "en": "Author's note", "tr": "Yazarın notu"}


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path) and io.open(path, encoding="utf-8", newline="").read() == text:
        return 0
    for _ in range(6):
        try:
            io.open(path, "w", encoding="utf-8", newline="\n").write(text)
            return 1
        except OSError:
            time.sleep(1.2)
    raise SystemExit("не записан: " + path)


def soup_of(lang, name):
    p = os.path.join(SRC, SUB[lang], name + ".html")
    return BeautifulSoup(io.open(p, encoding="utf-8").read(), "html.parser")


def real_pages(lang):
    d = os.path.join(SRC, SUB[lang])
    out = []
    for f in sorted(os.listdir(d)):
        if f.endswith(".html") and 'class="bk-main"' in io.open(os.path.join(d, f), encoding="utf-8").read():
            out.append(f[:-5])
    return out


def txt(el):
    return re.sub(r"\s+", " ", el.get_text(" ", strip=True)).strip() if el else ""


def page_id(href):
    """Имя страницы книги по ссылке или None, если ссылка не на страницу книги. Возвращает (id, #якорь)."""
    m = re.match(r"^(?:https?://[^/]+)?(.*?)(#.*)?$", href)
    path, frag = m.group(1), m.group(2) or ""
    if re.match(r"^(mailto:|tel:|javascript:)", href):
        return None
    if path.startswith("/"):
        m2 = re.match(r"^/klinik-psixiatriya/(?:(?:ru|en|tr)/)?([^/]*)$", path)
        if not m2:
            return None
        name = m2.group(1)
        return ("index" if name in ("", "index.html") else name[:-5] if name.endswith(".html") else None), frag
    if "://" in href:
        return None
    name = re.sub(r"^(\./|\.\./)+", "", path)
    if "/" in name:
        return None
    if name in ("", "index.html"):
        return "index", frag
    return (name[:-5] if name.endswith(".html") else None), frag


def read_tree(lang):
    """Боковое меню языка: три классификации -> группы -> страницы (одинаково на всех страницах языка)."""
    s = soup_of(lang, "index")
    nav = s.select_one(".bk-sb__nav")
    names, order = {}, []
    for b in nav.select(".cls-tabs-side .cls-tab"):
        names[b["data-cls"]] = txt(b); order.append(b["data-cls"])
    tree = {}
    for tr in nav.select(".cls-tree"):
        groups = []
        for g in tr.select(":scope > .bk-grp"):
            sec = g.select_one(":scope > .bk-row--sec")
            gid = sec["href"][:-5] if sec and sec.get("href", "").endswith(".html") else ""
            grp = {"t": txt(sec.select_one(".bk-row__t")), "code": txt(sec.select_one(".bk-row__n")), "items": []}
            if gid and gid != "mundericat":                          # у групп DSM и МКБ-10 ссылка ведёт на общее содержание, а не на страницу группы
                grp["id"] = gid
            for a in g.select(".bk-grp__sub > a"):
                grp["items"].append({"t": txt(a.select_one(".bk-row__t")), "code": txt(a.select_one(".bk-row__n")), "id": a["href"][:-5]})
            groups.append(grp)
        tree[tr["data-cls"]] = groups
    menu = {}                                                        # названия страниц из меню (для оглавления)
    for a in nav.select("a.bk-row"):
        h = a.get("href", "")
        if h.endswith(".html") and "/" not in h:
            menu.setdefault(h[:-5], txt(a.select_one(".bk-row__t")))
    return {"order": order, "names": names, **tree}, menu


def extract(lang, pid, menu):
    s = soup_of(lang, pid)
    col = s.select_one("main.bk-main .bk-col")
    head = col.select_one(".bk-chead")
    info = {"id": pid, "t": "", "code": "", "en": "", "sub": ""}
    if head is not None:
        h1 = txt(head.select_one(".bk-chead__h1"))
        info["code"] = txt(head.select_one(".bk-chead__n"))
        info["sub"] = txt(head.select_one(".bk-chead__sub"))
        en = txt(head.select_one(".bk-chead__en"))
        mt = menu.get(pid, "")
        m = re.search(r"\s*\(([^()]+)\)\s*$", h1)
        if mt and h1.startswith(mt):
            rest = h1[len(mt):].strip()
            mm = re.match(r"^\(([^()]+)\)$", rest)
            en = en or (mm.group(1) if mm else "")
            info["t"] = mt
        elif m:
            en = en or m.group(1)
            info["t"] = h1[:m.start()].strip()
        else:
            info["t"] = mt or h1
        info["en"] = en if en and en.lower() != info["t"].lower() else ""
    else:                                                            # главная страница: титул и обращение автора
        an = col.select_one(".author-note-title")
        info["t"] = INDEX_TITLE[lang] if an is None else txt(an)
    for x in col.select(".bk-crumb, .bk-chead, .bk-pn, .bk-ft, .bk-tp, .bk-toc, script, style, .btn-order"):
        x.decompose()
    for b in col.select("button[onclick]"):                           # вкладки классификаций: переключает читалка по data-cls
        del b["onclick"]
        b["type"] = "button"
    for e in col.select("[style]"):                                   # жёсткие цвета и ширины убираем: цвет знака — классом, остальное — стилями читалки
        st = e.get("style", "")
        del e["style"]
        if "#2a9d5c" in st:
            e["class"] = ["mk-ok"]
        elif "#e63946" in st:
            e["class"] = ["mk-no"]
    parts = []
    if info["sub"]:
        parts.append('<p class="bk-chead__sub">%s</p>' % info["sub"].replace("&", "&amp;").replace("<", "&lt;"))
    for ch in col.children:
        if getattr(ch, "name", None) is None:
            continue
        if "bk-read" in (ch.get("class") or []):
            parts.append(ch.decode_contents().strip())
        else:
            parts.append(str(ch))
    return info, "\n".join(p for p in parts if p).strip()


stats = {"rewritten": 0, "broken": [], "broken_anchor": [], "ext": 0, "other": []}


def fix_links(html, lang, pid, pageset, ids_of):
    s = BeautifulSoup(html, "html.parser")
    own_ids = set(e["id"] for e in s.find_all(id=True))
    for a in s.find_all("a"):
        h = a.get("href")
        if h is None or h == "":
            continue
        if h.startswith("#"):
            if len(h) > 1 and unquote(h[1:]) not in own_ids:
                stats["broken_anchor"].append("%s/%s: %s" % (lang, pid, h))
            continue
        r = page_id(h)
        if r is None or r[0] is None:
            if re.match(r"^(https?:)?//|^/|^mailto:|^tel:", h):
                stats["ext"] += 1
            else:
                stats["other"].append("%s/%s: %s" % (lang, pid, h))
            continue
        name, frag = r
        if name not in pageset:
            stats["broken"].append("%s/%s: %s" % (lang, pid, h))
            continue
        if frag and len(frag) > 1 and unquote(frag[1:]) not in ids_of.get(name, set()):
            stats["broken_anchor"].append("%s/%s: %s" % (lang, pid, h))
        a["href"] = "read.html?b=%s&p=%s%s" % (BID, name, frag)
        stats["rewritten"] += 1
    return s.decode_contents()


def main():
    wrote = 0
    P = {"id": BID, "src": "klinik-psixiatriya", "langs": list(LANGS), "cover": COVER, "t": {}, "kicker": {}, "sub": {}, "meta": {}, "toc": {}, "trees": {}}
    pages, ids_all = {}, {}
    orders = {}
    for lang in LANGS:
        real = real_pages(lang)
        tree, menu = read_tree(lang)
        P["trees"][lang] = tree
        icd = tree["icd"]
        order = list(FRONT)
        for g in icd:
            order.append(g["id"])
            order += [i["id"] for i in g["items"]]
        order += BACK
        rest = [p for p in real if p not in order]
        order += rest
        missing = [p for p in order if p not in real]
        if rest or missing:
            print("[%s] вне порядка: %s; нет страниц: %s" % (lang, rest, missing))
        orders[lang] = [p for p in order if p in real]
        disorder_ids = set(i["id"] for g in icd for i in g["items"])
        infos, bodies = {}, {}
        for pid in orders[lang]:
            infos[pid], bodies[pid] = extract(lang, pid, menu)
            infos[pid]["lvl"] = 1 if pid in disorder_ids else 0
        ids_of = {}
        for pid, b in bodies.items():
            ids_of[pid] = set(e["id"] for e in BeautifulSoup(b, "html.parser").find_all(id=True))
        toc = []
        for n, pid in enumerate(orders[lang], 1):
            body = fix_links(bodies[pid], lang, pid, set(orders[lang]), ids_of)
            wrote += write(os.path.join(OUT, lang, "%03d.html" % n), body + "\n")
            i = infos[pid]
            item = {"t": i["t"], "n": len(re.sub(r"<[^>]+>", "", body)), "id": pid, "lvl": i["lvl"], "code": i["code"]}
            if i["en"]:
                item["en"] = i["en"]
            if i["sub"]:
                item["sub"] = i["sub"]
            toc.append(item)
        # лишние файлы страниц (если страниц стало меньше)
        d = os.path.join(OUT, lang)
        for f in os.listdir(d):
            if re.match(r"^\d{3}\.html$", f) and int(f[:3]) > len(toc):
                os.remove(os.path.join(d, f))
        P["toc"][lang] = toc
        b = BOOK[lang]
        nch = sum(1 for g in icd)
        ndis = sum(len(g["items"]) for g in icd)
        P["t"][lang] = b["t"]
        P["kicker"][lang] = b["author"] + " · " + b["kind"]
        P["sub"][lang] = b["sub"]
        L = b["lab"]
        P["meta"][lang] = [[L[0], b["author"]], [L[1], "2026"], [L[2], "AZ · RU · EN · TR"], [L[3], b["print"]], [L[4], str(nch)], [L[5], str(ndis)]]
        print("[%s] страниц: %d (глав %d, расстройств %d)" % (lang, len(toc), nch, ndis))
    # сверка языков
    base = [x["id"] for x in P["toc"]["az"]]
    for lang in LANGS[1:]:
        cur = [x["id"] for x in P["toc"][lang]]
        if cur != base:
            print("[%s] расхождение с az: нет у %s: %s; лишние: %s; порядок %s" % (lang, lang, sorted(set(base) - set(cur)), sorted(set(cur) - set(base)), "тот же" if sorted(cur) == sorted(base) else "разный"))
    print("id совпадают на всех языках: %s" % all([x["id"] for x in P["toc"][l]] == base for l in LANGS[1:]))
    # деревья: все id известны
    badtree = []
    for lang in LANGS:
        ids = set(x["id"] for x in P["toc"][lang])
        for k in P["trees"][lang]["order"]:
            for g in P["trees"][lang][k]:
                for i in ([g] if g.get("id") else []) + g["items"]:
                    if i["id"] not in ids:
                        badtree.append("%s/%s: %s" % (lang, k, i["id"]))
    print("в деревьях ссылок на несуществующие страницы: %d %s" % (len(badtree), badtree[:5]))
    wrote += write(os.path.join(OUT, "book.json"), json.dumps(P, ensure_ascii=False, indent=1) + "\n")
    print("внутренних ссылок переписано: %d" % stats["rewritten"])
    print("битых внутренних ссылок (страницы нет): %d %s" % (len(stats["broken"]), stats["broken"][:10]))
    print("битых якорей (id нет на странице): %d %s" % (len(stats["broken_anchor"]), stats["broken_anchor"][:10]))
    print("ссылок наружу и на остальной сайт (не тронуты): %d; прочих непонятных: %d %s" % (stats["ext"], len(stats["other"]), stats["other"][:5]))
    print("файлов записано: %d" % wrote)
    return 1 if (stats["broken"] or badtree) else 0


sys.exit(main())
