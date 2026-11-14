# -*- coding: utf-8 -*-
"""Библиотека: работы Фрейда вне серии, которые лежат в прежнем формате читалки (страницы глав с <main class="site-main">):
«О коке», «К пониманию афазий», «Детский церебральный паралич», «Рецензии», «Рефераты», предисловие к Соссюру,
«Психопатические персонажи на сцене». Результат — тот же, что у остальных книг: books/<книга>/book.json и
books/<книга>/az/NNN.html. Источник (site/books/<книга>/) не меняется. Запуск: python build_library_legacy.py,
затем python build_library.py (он дочитывает паспорта в картотеку).
ВНИМАНИЕ (13.11.2026): паспорта book.json этот сборщик пишет по старым данным — у freud-kokain, -afaziya, -referatlar, -resenziyalar,
-sehnede, -sossur он стирает обложку и меняет название, у freud-usaq-iflici — страницы. После запуска вернуть паспорта:
git checkout -- books/<книга>/book.json (главы az/NNN.html он пишет верно, термины — через term_fix)."""
import io, os, re, sys, json, glob
from bs4 import BeautifulSoup
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import libcommon
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ROOT = r"D:\Projects\Ragimoff\old_versions\2026-11-12_site_before_v11"   # прежний сайт: источник текстов и картинок, только чтение (с 12.11.2026 версия 11 — корень сайта)
SRC = os.path.join(ROOT, "books")
OUT = os.path.join(D, "books")
BOOKS = ["freud-kokain", "freud-afaziya", "freud-usaq-iflici", "freud-resenziyalar-1887-1910", "freud-referatlar-1884-1885", "freud-sossur-on-sozu", "freud-sehnede-psixopatik-personajlar"]
shop = json.load(io.open(os.path.join(D, "data", "shop", "index.az.json"), encoding="utf-8"))
SHOP = dict((it["id"], it) for g in shop["groups"] for it in g["items"])


import os as _o, sys as _s; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); from term_fix import fix_text  # названия болезней по принятой номенклатуре (слово Кенана 13.11.2026)


def write(path, text):
    text = fix_text(text, path=path)[0] if "/az/" in path.replace("\\", "/") or path.endswith("book.json") else text
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path) and io.open(path, encoding="utf-8").read() == text:
        return 0
    for _ in range(6):
        try:
            io.open(path, "w", encoding="utf-8", newline="\n").write(text)
            return 1
        except OSError:
            import time; time.sleep(1.2)
    raise SystemExit("не записан: " + path)


def body_of(soup):
    """Содержание страницы без служебного: крошки, заголовок, поиск, меню."""
    m = soup.select_one("main.site-main")
    w = m.select_one(".content-wrap") or m
    for x in w.select("nav.crumb, .sr, .lang-switch-bar, script, .home-hero, .prog-bar, .book-toc .toc-chapter"):
        x.decompose()
    h1 = w.find("h1")
    title = h1.get_text(" ", strip=True) if h1 else ""
    if h1:
        h1.decompose()
    lead = [x for x in m.select(".sci-note") if x not in w.descendants]                # примечание стоит перед колонкой текста
    html = "".join(str(x) for x in lead) + w.decode_contents()
    html = re.sub(r'\s+style="[^"]*"', "", html)                                        # вид задаёт читалка, а не строка в тексте
    html = re.sub(r'<h2 class="toc-title">[^<]*</h2>\s*(?=</section>)', "", html)
    html = re.sub(r"<section[^>]*>\s*</section>", "", html)
    return title, html.strip()


def split(html, title):
    """Сборник делится на отдельные тексты: каждая рецензия, каждое приложение, каждый год рефератов — своя глава с названием.
    Сноска, на которую ссылается глава, переносится вместе с ней (иначе всплывающее окно сноски было бы пустым)."""
    soup = BeautifulSoup("<div id='x'>" + html + "</div>", "html.parser")
    root = soup.select_one("#x")
    kids = [c for c in root.find_all(recursive=False)]
    reviews = [c for c in kids if c.name == "section" and "rd-review" in (c.get("class") or [])]
    by_review = 2 <= len(reviews) <= 30

    def starts(c):
        cl = c.get("class") or []
        if c.name == "section" and "rd-appendix" in cl and (c.get("id") or "").startswith("elave"):
            return True
        if c.name == "section" and "rd-review" in cl and by_review:
            return True
        return c.name == "h2" and "sec" in cl and (c.get("id") or "").startswith("y") and len(reviews) > 30

    if not any(starts(c) for c in kids):
        return [(title, html)]
    chunks, cur_t, cur = [], title, []
    for c in list(root.contents):
        if getattr(c, "name", None) and starts(c):
            if "".join(str(x) for x in cur).strip():
                chunks.append((cur_t, cur))
            h = c if c.name == "h2" else c.find(["h2", "h3", "h4"])
            cur_t = h.get_text(" ", strip=True) if h else title
            if h is not None and c.name != "h2":
                h.extract()                                   # заголовок текста выводит читалка
            cur = [] if c.name == "h2" else [c]
        else:
            cur.append(c)
    if "".join(str(x) for x in cur).strip():
        chunks.append((cur_t, cur))
    notes = dict((n.get("id"), n) for n in root.select(".rd-notes [id]"))
    out = []
    for t, parts in chunks:
        h = "".join(str(x) for x in parts)
        need = [i for i in dict.fromkeys(re.findall(r'href="#([^"]+)"', h)) if i in notes and 'id="%s"' % i not in h]
        if need:
            h += '<aside class="rd-notes">' + "".join(str(notes[i]) for i in need) + "</aside>"
        if len(re.sub(r"<[^>]+>", "", h).strip()) >= 40:
            out.append((t, h.strip()))
    return out


wrote = 0
for b in BOOKS:
    d = os.path.join(SRC, b)
    idx = BeautifulSoup(io.open(os.path.join(d, "index.html"), encoding="utf-8", errors="replace").read(), "html.parser")
    files = sorted(f for f in glob.glob(os.path.join(d, "[0-9][0-9]-*.html")))
    toc, n = [], 0
    book_title = (idx.select_one(".home-title") or idx.find("h1") or idx.title).get_text(" ", strip=True).split("|")[0].strip()
    for f in files:
        s = BeautifulSoup(io.open(f, encoding="utf-8", errors="replace").read(), "html.parser")
        if not s.select_one("main.site-main"):
            continue
        t, html = body_of(s)
        if len(re.sub(r"<[^>]+>", "", html)) < 40:
            continue
        for ct, ch in split(html, t or book_title):
            n += 1
            wrote += write(os.path.join(OUT, b, "az", "%03d.html" % n), ch + "\n")
            toc.append({"t": ct or book_title, "n": len(re.sub(r"<[^>]+>", "", ch))})
    t, html = body_of(idx)                               # главная страница книги: у малых работ это весь текст, у больших — сведения об издании
    if len(re.sub(r"<[^>]+>", "", html)) >= 40:
        for ct, ch in split(html, (book_title if not files else "Nəşr haqqında")):
            n += 1
            wrote += write(os.path.join(OUT, b, "az", "%03d.html" % n), ch + "\n")
            toc.append({"t": ct or book_title, "n": len(re.sub(r"<[^>]+>", "", ch))})
    for old in glob.glob(os.path.join(OUT, b, "az", "*.html")):
        if int(os.path.basename(old)[:-5]) > n:
            os.remove(old)
    it = SHOP.get(b, {})
    P = {"id": b, "src": "books/" + b, "langs": ["az"], "cover": it.get("img", ""), "t": {"az": it.get("t") or book_title}, "kicker": {"az": "Ziqmund Freyd"}, "sub": {"az": ""},
         "meta": {"az": [["Müəllif", "Ziqmund Freyd"]] + ([["Nəşr", it["meta"]]] if it.get("meta") else [])}, "toc": {"az": toc}}
    libcommon.finish(P)
    wrote += write(os.path.join(OUT, b, "book.json"), json.dumps(P, ensure_ascii=False, indent=1) + "\n")
    print("%-40s глав: %d  знаков: %d" % (b, n, sum(x["n"] for x in toc)))
print("файлов записано:", wrote)
