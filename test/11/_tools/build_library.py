# -*- coding: utf-8 -*-
"""Библиотека книг новой системы: текст хранится отдельно от страницы (решение владельца 12.11.2026).

Было: у каждой книги на каждом языке своя страница-читалка со всем текстом внутри (site/books/<книга>/[ru|en/]index.html).
Стало (test/11/books/):
    books/index.json                 — картотека библиотеки: все книги, языки, число глав
    books/<книга>/book.json          — паспорт книги: названия, сведения, обложка, оглавление по языкам
    books/<книга>/<язык>/NN.html     — текст главы NN (только содержание, без шапки и меню)
Показывает книгу одна читалка: read.html?b=<книга> (assets/js/reader.js). Новая книга или новый язык = новая папка
с текстом; новых страниц не появляется.

Источник текста — действующие читалки (не меняются). Запуск: python build_library.py [книга …]
Поиск по библиотеке: python library_find.py <слова>"""
import io, os, re, sys, json, glob
from bs4 import BeautifulSoup
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ROOT = os.path.abspath(os.path.join(D, "..", ".."))
SRC = os.path.join(ROOT, "books")
OUT = os.path.join(D, "books")
ONLY = sys.argv[1:]
LANGDIR = {"az": "", "ru": "ru", "en": "en", "tr": "tr"}


def low(w, lang):
    return w.replace("I", "ı").replace("İ", "i").lower() if lang == "az" else w.lower()


def clean_title(t, lang):
    """В источнике заголовки набраны капителью и приходят то строчными, то ПРОПИСНЫМИ, то со случайными заглавными
    («как вирус попадает В систему», «1-Cİ fəsil», «as A mechanism») — приводим к виду предложения."""
    t = re.sub(r"\s+", " ", t).strip()
    words = t.split(" ")
    out = []
    for w in words:
        core = re.sub(r"[^A-Za-zА-Яа-яЁёƏəÖöÜüĞğŞşÇçİı]", "", w)
        if len(core) >= 2 and core.upper() == core and core not in ("IPAS", "DSM", "ICD", "XBT", "МКБ", "КПТ", "CBT", "KDT", "OKP", "ОКР", "PTSD", "II", "III", "IV", "VI", "VII", "VIII", "IX", "XI", "XII"):
            q = w[:1] in u"«“\"„"
            w = low(w, lang)                                    # слово целиком прописными
            if q and len(w) > 1:                                # название в кавычках — с заглавной: «Феникс», «Лилит»
                w = w[0] + ("İ" if w[1] == "i" and lang == "az" else w[1].upper()) + w[2:]
        elif len(core) == 1 and core.isupper() and out and not re.search(r"[.!?:]$", out[-1]) and core not in ("I", "V", "X"):
            w = low(w, lang)                                    # одиночная заглавная в середине фразы: «В», «И», «A»
        out.append(w)
    t = " ".join(out)
    t = re.sub(r"(\d)-(C[İIUÜ])(?![A-Za-zƏəÖöÜüĞğŞşÇçİı])", lambda m: m.group(1) + "-" + low(m.group(2), "az"), t)
    cap = lambda m: m.group(1) + m.group(2).upper().replace("İ", "İ")
    up = lambda ch: ("İ" if ch == "i" and lang == "az" else "I" if ch == "ı" else ch.upper())
    if t:
        t = up(t[0]) + t[1:]
    t = re.sub(r"([.!?]\s+)([a-zа-яёəöüğşçıi])", lambda m: m.group(1) + up(m.group(2)), t)          # новое предложение — с заглавной
    t = re.sub(u"([«“])([a-zа-яёəöüğşçıi])([^ «»“”]*[»”])", lambda m: m.group(1) + up(m.group(2)) + m.group(3), t)   # одно слово в кавычках — имя: «Лилит», «Феникс»
    return t


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


catalog, wrote = [], 0
for bdir in sorted(os.listdir(SRC)):
    if ONLY and bdir not in ONLY:
        continue
    passport = {"id": bdir, "src": "books/" + bdir, "langs": [], "cover": "", "t": {}, "kicker": {}, "sub": {}, "meta": {}, "toc": {}}
    for lang, sub in LANGDIR.items():
        f = os.path.join(SRC, bdir, sub, "index.html")
        if not os.path.isfile(f):
            continue
        html = io.open(f, encoding="utf-8", errors="replace").read()
        if 'class="rd-chap"' not in html:
            continue
        soup = BeautifulSoup(html, "html.parser")
        tp = soup.select_one("#rd-title")
        cov = soup.select_one(".bk-cover")
        m = re.search(r"url\(['\"]?([^'\")]+)", (cov.get("style") or "") if cov else "")
        if m and not passport["cover"]:
            passport["cover"] = m.group(1)
        g = lambda sel: (tp.select_one(sel).get_text(" ", strip=True) if tp and tp.select_one(sel) else "")
        passport["t"][lang] = g(".rd-h1") or (soup.title.get_text().split("|")[0].strip() if soup.title else bdir)
        passport["kicker"][lang] = g(".rd-kicker")
        passport["sub"][lang] = g(".rd-sub")
        passport["meta"][lang] = [[re.sub(r"\s+", " ", li.get_text(" ", strip=True).replace(li.b.get_text(" ", strip=True), "", 1)).strip(), li.b.get_text(" ", strip=True)] for li in (tp.select(".rd-meta li") if tp else []) if li.b]
        toc = []
        for i, art in enumerate(soup.select("article.rd-chap"), 1):
            title = clean_title(art.get("data-title") or (art.h2.get_text(" ", strip=True) if art.h2 else str(i)), lang)
            part = art.select_one(".rd-chap__part")
            for x in art.select(".rd-chap__n, .rd-orn, .rd-chap__part"):
                x.decompose()
            if art.h2:
                art.h2.decompose()                                   # заголовок главы выводит читалка — из оглавления
            body = art.decode_contents().strip()
            wrote += write(os.path.join(OUT, bdir, lang, "%03d.html" % i), body + "\n")
            item = {"t": title, "n": len(re.sub(r"<[^>]+>", "", body))}
            if part:
                item["part"] = part.get_text(" ", strip=True)
            toc.append(item)
        # лишние файлы глав (если глав стало меньше) убираем из папки языка
        for old in glob.glob(os.path.join(OUT, bdir, lang, "*.html")):
            if (int(os.path.basename(old)[:-5]) > len(toc) or len(os.path.basename(old)) != 8):
                os.remove(old)
        passport["toc"][lang] = toc
        passport["langs"].append(lang)
    if not passport["langs"]:
        continue
    wrote += write(os.path.join(OUT, bdir, "book.json"), json.dumps(passport, ensure_ascii=False, indent=1) + "\n")
    catalog.append({"id": bdir, "t": passport["t"], "kicker": passport["kicker"], "langs": passport["langs"], "cover": passport["cover"],
                    "chapters": dict((l, len(passport["toc"][l])) for l in passport["langs"]), "chars": dict((l, sum(x["n"] for x in passport["toc"][l])) for l in passport["langs"])})
    print("%-34s %s  глав: %s" % (bdir, ",".join(passport["langs"]), "/".join(str(len(passport["toc"][l])) for l in passport["langs"])))
if not ONLY:
    # книги, которых нет в старых читалках (собираются своими инструментами, например build_klinik.py), — в картотеку из их паспортов
    have = set(c["id"] for c in catalog)
    for pj in sorted(glob.glob(os.path.join(OUT, "*", "book.json"))):
        P = json.load(io.open(pj, encoding="utf-8"))
        if P["id"] in have:
            continue
        catalog.append({"id": P["id"], "t": P["t"], "kicker": P["kicker"], "langs": P["langs"], "cover": P["cover"],
                        "chapters": dict((l, len(P["toc"][l])) for l in P["langs"]), "chars": dict((l, sum(x["n"] for x in P["toc"][l]) ) for l in P["langs"])})
        print("%-34s %s  (паспорт из папки)" % (P["id"], ",".join(P["langs"])))
    catalog.sort(key=lambda c: c["id"])
    wrote += write(os.path.join(OUT, "index.json"), json.dumps({"about": "Картотека библиотеки: одна запись — одна книга. Текст — в папке книги по языкам, паспорт — book.json.", "books": catalog}, ensure_ascii=False, indent=1) + "\n")
print("книг: %d, файлов записано: %d" % (len(catalog), wrote))
