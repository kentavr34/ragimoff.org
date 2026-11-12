# -*- coding: utf-8 -*-
"""Каталог для прототипа книжного магазина (test/11/shop.html, book.html).
Источник — действующий магазин site/books/{,ru/,en/}index.html (сам магазин не меняется): названия, авторы, обложки,
цены, сведения о книге, адрес чтения. Короткие описания «почему эта книга» — из content.js (блок книг главной).
Результат: data/shop/index.<lang>.json. Запуск: python build_shop.py"""
import io, os, re, sys, json, subprocess
from bs4 import BeautifulSoup
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ROOT = os.path.abspath(os.path.join(D, "..", ".."))
SRC = {"az": "books/index.html", "ru": "books/ru/index.html", "en": "books/en/index.html"}
H = {"ru": ("Книги", "Учебник, авторские книги и полное собрание Фрейда на азербайджанском. Читать можно бесплатно; печатную книгу — заказать.", "Все", "Читать бесплатно", "Заказать печатную книгу", "О книге", "Другие книги", "Цена печатной книги", "Скоро", "Содержание", "Книга издана на азербайджанском языке", "и ещё"),
     "az": ("Kitablar", "Dərslik, müəllif kitabları və Azərbaycan dilində Freydin tam külliyyatı. Pulsuz oxumaq olar; çap nüsxəsini sifariş etmək mümkündür.", "Hamısı", "Pulsuz oxuyun", "Çap nüsxəsini sifariş edin", "Kitab haqqında", "Digər kitablar", "Çap nüsxəsinin qiyməti", "Tezliklə", "Mündəricat", "Kitab Azərbaycan dilində nəşr olunub", "və daha"),
     "en": ("Books", "A textbook, our own books and the complete Freud in Azerbaijani. Read for free; order a printed copy.", "All", "Read for free", "Order a printed copy", "About the book", "Other books", "Price of the printed book", "Coming soon", "Contents", "The book is published in Azerbaijani", "and more")}
# описания с главной: номер в T[l].books.b → название карточки магазина (азербайджанское, как data-title)
FACTS_FOR = {0: "klinik", 2: "phoenix", 3: "guilt", 4: "pandemic"}

js = ("import('file:///%s/assets/js/content.js').then(m => { const o = {}; for (const l of ['ru','az','en']) o[l] = m.T[l].books.b.map(x => ({k: x.k, f: x.f})); process.stdout.write(JSON.stringify(o)); })" % D.replace("\\", "/"))
facts = json.loads(subprocess.run(["node", "--input-type=module", "-e", js], capture_output=True, check=True).stdout.decode("utf-8"))

def book_id(img, href):
    """Свой адрес у каждой книги: у авторских — по обложке (klinik, guilt…), у томов Фрейда — по адресу чтения."""
    base = os.path.basename(img).split("?")[0].rsplit(".", 1)[0] if img else ""
    if base in ("klinik", "guilt", "pandemic", "phoenix"):
        return base
    parts = [x for x in href.strip("/").split("/") if x and x not in ("books", "ru", "en", "az") and not x.endswith(".html")]      # адрес — папка книги, не файл главы
    return parts[-1] if parts else base


AZ_PRICE = {}
# разделы каталога Фрейда: название раздела на языках; порядок разделов — как в списке
SUBS = [("series", {"ru": "Собрание сочинений", "az": "Toplu əsərlər", "en": "Collected works"}),
        ("letters", {"ru": "Переписка", "az": "Məktublar", "en": "Correspondence"}),
        ("early", {"ru": "Ранние и отдельные работы", "az": "Erkən və ayrı əsərlər", "en": "Early and separate works"}),
        ("anthology", {"ru": "Антология", "az": "Antologiya", "en": "Anthology"}),
        ("small", {"ru": "Малые тексты", "az": "Kiçik mətnlər", "en": "Short texts"})]
SMALL_NOTE = {"ru": "Тексты в несколько страниц. Отдельными книгами они не издавались — их место в томе собрания сочинений будет уточнено по немецкому изданию.",
              "az": "Bir neçə səhifəlik mətnlər. Ayrıca kitab kimi nəşr olunmayıb — toplu əsərlərin cildindəki yeri alman nəşrinə əsasən dəqiqləşdiriləcək.",
              "en": "Texts of a few pages. They were never published as separate books — their place in a volume of the collected works will be settled against the German edition."}


def section(it):
    """К какому разделу каталога относится книга Фрейда: по сведениям о книге (номер книги, письма, число страниц)."""
    m = re.match(r"^(?:Книга|Kitab|Book)\s+(\d+)", it["meta"])
    if m:
        return "series", int(m.group(1))
    if re.search(r"писем|məktub|letters", it["meta"]):
        return "letters", 0
    if "aforizm" in it["id"]:
        return "anthology", 0
    pg = re.search(r"(\d+)\s*(?:стр|səh|pp)", it["meta"])
    if pg and int(pg.group(1)) <= 10:
        return "small", int(pg.group(1))
    return "early", 0
LIB = set(os.listdir(os.path.join(D, "books"))) if os.path.isdir(os.path.join(D, "books")) else set()      # книги, перенесённые в библиотеку
LIB_ID = {"klinik": "klinik-psixiatriya", "guilt": "virus-viny", "pandemic": "shizofreniya", "phoenix": "phoenix-era"}
for lang, rel in sorted(SRC.items(), key=lambda x: x[0] != "az"):
    soup = BeautifulSoup(io.open(os.path.join(ROOT, rel), encoding="utf-8").read(), "html.parser")
    groups, cur = [], None
    for el in soup.select("h2.author-sec, article.card"):
        if el.name == "h2":
            cur = {"id": el.get("data-author") or "other", "name": el.get_text(" ", strip=True), "items": []}
            groups.append(cur)
            continue
        if cur is None:
            cur = {"id": "other", "name": "", "items": []}
            groups.append(cur)
        cov = el.select_one(".cover")
        m = re.search(r"url\((?:&quot;|\"|')?([^\"')&]+)", (cov.get("style") or "") if cov else "")
        img = m.group(1) if m else ""
        a = el.select_one("a.card__cover")
        price = el.select_one(".card__price")
        read = el.select_one(".btn--read")
        it = {"id": book_id(img, (a.get("href") if a else "") or ""),
              "t": el.select_one(".card__title").get_text(" ", strip=True), "meta": (el.select_one(".card__meta").get_text(" ", strip=True) if el.select_one(".card__meta") else ""),
              "price": price.get_text(" ", strip=True).replace("₼", "AZN") if price else "", "img": img, "href": (a.get("href") if a else "") or "",
              "a": (cov.select_one(".cover__author").get_text(" ", strip=True) if cov and cov.select_one(".cover__author") else ""),
              "y": (cov.select_one(".cover__year").get_text(" ", strip=True) if cov and cov.select_one(".cover__year") else ""),
              "read": bool(read)}
        # оглавление — из читалки книги (тома Фрейда изданы на азербайджанском: оглавление одно на все языки сайта)
        bf = os.path.join(ROOT, it["href"].strip("/").split("?")[0], "index.html") if it["href"].startswith("/books/freud") else ""
        if bf and os.path.isfile(bf):
            bs = BeautifulSoup(io.open(bf, encoding="utf-8").read(), "html.parser")
            toc = []
            for x in bs.select(".toc-row .toc-t"):
                tt = x.get_text(" ", strip=True)
                if tt and tt not in toc:
                    toc.append(tt)
            if toc:
                it["toc"] = toc[:16]
                it["tocMore"] = max(0, len(toc) - 16)
        lib = LIB_ID.get(it["id"], it["id"])
        if lib in LIB:
            it["read_new"] = "read.html?b=" + lib               # единая читалка новой системы
        if lang == "az":
            AZ_PRICE[it["id"]] = it["price"]
        elif not it["price"] and AZ_PRICE.get(it["id"]):
            it["price"] = AZ_PRICE[it["id"]]                     # цена печатной книги одна на всех языках
        cur["items"].append(it)
    for i, key in FACTS_FOR.items():
        for g in groups:
            for it in g["items"]:
                if it["id"] == key and i < len(facts[lang]):
                    it["k"], it["f"] = facts[lang][i]["k"], list(facts[lang][i]["f"])
                    mp = re.search(r"(\d{3,4})\s*(стр|səh|pp|pages)", it["meta"])         # число страниц в описании — как в сведениях о книге
                    if mp:
                        it["f"] = [re.sub(r"\b8[0-9]{2}\b(?=\s*(печатн|çap|printed))", mp.group(1), x) for x in it["f"]]
    for g in groups:
        if g["id"] != "freud":
            continue
        buckets = dict((k, []) for k, _ in SUBS)
        for it in g["items"]:
            k, order = section(it)
            it["_o"] = order
            if k == "small":
                it["small"] = True
            buckets[k].append(it)
        buckets["series"].sort(key=lambda x: x["_o"])
        g["sub"] = [{"id": k, "t": names[lang], "n": len(buckets[k])} for k, names in SUBS if buckets[k]]
        g["items"] = []
        for k, _ in SUBS:
            for it in buckets[k]:
                it["sec"] = k
                it.pop("_o", None)
                g["items"].append(it)
        g["smallNote"] = SMALL_NOTE[lang]
    h = H[lang]
    out = {"lang": lang, "src": rel, "title": h[0], "lead": h[1], "u": {"all": h[2], "read": h[3], "order": h[4], "about": h[5], "other": h[6], "price": h[7], "soon": h[8], "toc": h[9], "azNote": h[10], "more": h[11]},
           "orderUrl": "/" + rel.replace("index.html", ""), "groups": [g for g in groups if g["items"]]}
    os.makedirs(os.path.join(D, "data", "shop"), exist_ok=True)
    json.dump(out, io.open(os.path.join(D, "data", "shop", "index.%s.json" % lang), "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
    print(lang, [(g["id"], len(g["items"])) for g in out["groups"]], sum(1 for g in groups for it in g["items"] if it.get("f")))
