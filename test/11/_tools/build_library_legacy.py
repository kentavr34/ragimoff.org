# -*- coding: utf-8 -*-
"""Библиотека: работы Фрейда вне серии, которые лежат в прежнем формате читалки (страницы глав с <main class="site-main">):
«О коке», «К пониманию афазий», «Детский церебральный паралич», «Рецензии», «Рефераты», предисловие к Соссюру,
«Психопатические персонажи на сцене». Результат — тот же, что у остальных книг: books/<книга>/book.json и
books/<книга>/az/NNN.html. Источник (site/books/<книга>/) не меняется. Запуск: python build_library_legacy.py,
затем python build_library.py (он дочитывает паспорта в картотеку)."""
import io, os, re, sys, json, glob
from bs4 import BeautifulSoup
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ROOT = os.path.abspath(os.path.join(D, "..", ".."))
SRC = os.path.join(ROOT, "books")
OUT = os.path.join(D, "books")
BOOKS = ["freud-kokain", "freud-afaziya", "freud-usaq-iflici", "freud-resenziyalar-1887-1910", "freud-referatlar-1884-1885", "freud-sossur-on-sozu", "freud-sehnede-psixopatik-personajlar"]
shop = json.load(io.open(os.path.join(D, "data", "shop", "index.az.json"), encoding="utf-8"))
SHOP = dict((it["id"], it) for g in shop["groups"] for it in g["items"])


def write(path, text):
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
        n += 1
        wrote += write(os.path.join(OUT, b, "az", "%03d.html" % n), html + "\n")
        toc.append({"t": t or book_title, "n": len(re.sub(r"<[^>]+>", "", html))})
    t, html = body_of(idx)                               # главная страница книги: у малых работ это весь текст, у больших — сведения об издании
    if len(re.sub(r"<[^>]+>", "", html)) >= 40:
        n += 1
        wrote += write(os.path.join(OUT, b, "az", "%03d.html" % n), html + "\n")
        toc.append({"t": (book_title if not files else "Nəşr haqqında"), "n": len(re.sub(r"<[^>]+>", "", html))})
    for old in glob.glob(os.path.join(OUT, b, "az", "*.html")):
        if int(os.path.basename(old)[:-5]) > n:
            os.remove(old)
    it = SHOP.get(b, {})
    P = {"id": b, "src": "books/" + b, "langs": ["az"], "cover": it.get("img", ""), "t": {"az": it.get("t") or book_title}, "kicker": {"az": "Ziqmund Freyd"}, "sub": {"az": ""},
         "meta": {"az": [["Müəllif", "Ziqmund Freyd"]] + ([["Nəşr", it["meta"]]] if it.get("meta") else [])}, "toc": {"az": toc}}
    wrote += write(os.path.join(OUT, b, "book.json"), json.dumps(P, ensure_ascii=False, indent=1) + "\n")
    print("%-40s глав: %d  знаков: %d" % (b, n, sum(x["n"] for x in toc)))
print("файлов записано:", wrote)
