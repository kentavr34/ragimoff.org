# -*- coding: utf-8 -*-
"""Комплектация коротких работ Фрейда в книги (слово владельца 13.11.2026: короче 100 страниц отдельной книгой не продаём).
Запускать ПОСЛЕ build_library.py / build_library_legacy.py / build_shop.py — он дополняет их результат. Повторный запуск ничего не меняет.

Состав — по немецкому изданию:
 • Книга 16 (freud-gw17) собрана из GW XVII и XIX (дополнительный том, Nachtragsband). В Nachtragsband входят и рефераты,
   рецензии, предисловия и «Психопатические персонажи на сцене» — они добавляются в Книгу 16 отдельными разделами.
 • «О коке» и «К пониманию афазий» — работы до психоанализа, в GW не входят (у немцев изданы отдельно:
   Schriften über Kokain; Zur Auffassung der Aphasien). Вместе — одна книга «Кока и афазия».
Прежние папки коротких работ остаются в библиотеке (старые ссылки открываются), в паспорте помечены merged — в каталоге их нет."""
import os as _o, sys as _s; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); from term_fix import fix_text  # слово Кенана 13.11.2026
import io, os, re, sys, json, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(D)
PAGE = 1800                                   # знаков на страницу — для счёта страниц добавленного

MERGE = [
    {"into": "freud-gw17", "new": False,
     "parts": [("freud-referatlar-1884-1885", "Referatlar (1884–1885)"), ("freud-resenziyalar-1887-1910", "Resenziyalar (1887–1910)"),
               ("freud-sossur-on-sozu", "Kiçik mətnlər"), ("freud-sehnede-psixopatik-personajlar", "")],
     "pages_add": 99},
    {"into": "freud-koka-afaziya", "new": True, "cover_from": "freud-afaziya", "order": "freud-afaziya",
     "parts": [("freud-kokain", "Koka haqqında (1884–1887)"), ("freud-afaziya", "Afaziyaların dərk edilməsinə dair (1891)")],
     "t": {"az": "Koka və afaziya: psixoanalizdən əvvəlki əsərlər", "ru": "Кока и афазия: работы до психоанализа", "en": "Coca and Aphasia: Pre-Psychoanalytic Writings"},
     "meta": {"az": "1884–1891 · 160 səh.", "ru": "1884–1891 · 160 стр.", "en": "1884–1891 · 160 pp."}, "pages": 160},
    # 13.11.2026 (Кенан): письма Цвейгу (49 стр.) и «Афоризмы» (~12 стр.) отдельно не продаются — вместе с письмами Марте одна книга.
    # print: главы сайта строит _tools/build_book_print_freud.py из печатного Word (Print/vne_serii/Mektublar_ve_aforizmler_AZ_v*.docx);
    # здесь — только паспорт (если его нет), пометки merged у частей, картотека и каталог магазина. Цена — как у одной книги (ord).
    {"into": "freud-mektublar-aforizmler", "new": True, "print": True, "cover_from": "freud-sevgi-mektublari", "order": "freud-sevgi-mektublari", "sec": "letters",
     "src_item": "freud-sevgi-mektublari", "years": "1882–1939",
     "parts": [("freud-sevgi-mektublari", ""), ("freud-zweig-mektublari", ""), ("freud-aforizmlar", "")],
     "t": {"az": "Məktublar və aforizmlər", "ru": "Письма и афоризмы", "en": "Letters and Aphorisms"},
     "meta": {"az": "", "ru": "", "en": ""}, "pages": 0},
]


def jload(p):
    return json.load(io.open(p, encoding="utf-8"))


def jsave(p, o):
    s = json.dumps(o, ensure_ascii=False, indent=1) + "\n"
    s = fix_text(s, path=p)[0] if p.endswith(".az.json") or p.endswith("book.json") else s
    if os.path.exists(p) and io.open(p, encoding="utf-8").read() == s:
        return 0
    t = p + ".new"
    io.open(t, "w", encoding="utf-8", newline="\n").write(s)
    os.replace(t, p)
    return 1


n = 0
gone = {}
for m in MERGE:
    tgt = "books/" + m["into"]
    if m.get("print"):
        # книга собрана в печати целиком: части не копируются, главы строит build_book_print_freud.py
        if os.path.exists(tgt + "/book.json"):
            P = jload(tgt + "/book.json")
        else:
            src0 = jload("books/%s/book.json" % m["cover_from"])
            P = {"id": m["into"], "src": "Print", "langs": ["az"], "cover": src0.get("cover", ""), "t": {"az": m["t"]["az"]},
                 "kicker": {"az": "Ziqmund Freyd"}, "sub": {"az": ""}, "meta": {"az": [["Müəllif", "Ziqmund Freyd"], ["Yazılıb", m["years"]], ["Nəşr", "Ragimoff, 2026"]]},
                 "toc": {"az": []}}
        for src, _ in m["parts"]:
            S = jload("books/%s/book.json" % src)
            if S.get("merged") != m["into"]:
                S["merged"] = m["into"]
                n += jsave("books/%s/book.json" % src, S)
            gone[src] = m["into"]
        n += jsave(tgt + "/book.json", P)
        continue
    if m["new"]:
        src0 = jload("books/%s/book.json" % m["cover_from"])
        P = {"id": m["into"], "src": "сборник: " + " + ".join(p for p, _ in m["parts"]), "langs": ["az"], "cover": src0.get("cover", ""), "t": {"az": m["t"]["az"]},
             "kicker": {"az": "Ziqmund Freyd"}, "sub": {"az": ""}, "meta": {"az": [["Müəllif", "Ziqmund Freyd"], ["Yazılıb", "1884–1891"], ["Nəşr", "Ragimoff, 2026"], ["Çap", "B5 · %d səh." % m["pages"]]]},
             "toc": {"az": []}, "parts": [p for p, _ in m["parts"]]}
        base = 0
    else:
        P = jload(tgt + "/book.json")
        base = len(P["toc"]["az"]) if not P.get("parts") else P["own"]
        P.setdefault("own", base)
        P["toc"]["az"] = P["toc"]["az"][:base]
        P["parts"] = [p for p, _ in m["parts"]]
    k = base
    for src, label in m["parts"]:
        S = jload("books/%s/book.json" % src)
        for i, ch in enumerate(S["toc"]["az"], 1):
            k += 1
            a, b = "books/%s/az/%03d.html" % (src, i), "%s/az/%03d.html" % (tgt, k)
            os.makedirs(os.path.dirname(b), exist_ok=True)
            if not os.path.exists(b) or io.open(a, encoding="utf-8").read() != io.open(b, encoding="utf-8").read():
                shutil.copyfile(a, b)
                n += 1
            it = {"t": ch["t"], "n": ch["n"]}
            if i == 1 and label:
                it["part"] = label
            P["toc"]["az"].append(it)
        if S.get("merged") != m["into"]:
            S["merged"] = m["into"]
            n += jsave("books/%s/book.json" % src, S)
        gone[src] = m["into"]
    if not m["new"]:
        for row in P["meta"]["az"]:
            if row[0] == "Fəsillər":
                row[1] = str(len(P["toc"]["az"]))
            if row[0] == "Çap":
                row[1] = "B5 · %d səh." % (96 + m["pages_add"])
    n += jsave(tgt + "/book.json", P)

# картотека библиотеки
ix = jload("books/index.json")
have = set(b["id"] for b in ix["books"])
for m in MERGE:
    P = jload("books/%s/book.json" % m["into"])
    rec = {"id": P["id"], "t": P["t"], "kicker": P["kicker"], "langs": P["langs"], "cover": P["cover"], "chapters": {"az": len(P["toc"]["az"])}, "chars": {"az": sum(x["n"] for x in P["toc"]["az"])}}
    if P["id"] in have:
        ix["books"] = [rec if b["id"] == P["id"] else b for b in ix["books"]]
    else:
        ix["books"].append(rec)
ix["books"].sort(key=lambda b: b["id"])
n += jsave("books/index.json", ix)

# каталог магазина: объединённые работы убираются, сборник добавляется, у Книги 16 — новый объём
for lang in ("az", "ru", "en"):
    p = "data/shop/index.%s.json" % lang
    d = jload(p)
    for g in d["groups"]:
        if g["id"] != "freud":
            continue
        news = [m for m in MERGE if m["new"]]
        prev = {it["id"]: it for it in g["items"]}
        items = []
        for it in g["items"]:
            if it["id"] in gone or any(it["id"] == m["into"] for m in news):
                continue
            items.append(it)
        for m in news:   # сборник встаёт в каталог; сведения (год · страницы) потом ставит shop_facts.py
            sid = m.get("src_item", m.get("order"))
            base = dict(prev.get(m["into"]) or prev.get(sid) or prev.get("freud-afaziya") or {})
            assert base, ("нет исходной карточки для", m["into"])
            base.update({"id": m["into"], "t": m["t"][lang], "meta": m["meta"][lang] or base.get("meta", ""), "read_new": "read.html?b=" + m["into"],
                         "href": "read.html?b=" + m["into"], "ord": m["order"], "sec": m.get("sec", "early")})
            base.pop("toc", None)
            base.pop("tocMore", None)
            items.append(base)
        g["items"] = items
        for sb in g.get("sub", []):
            sb["n"] = sum(1 for it in items if it.get("sec") == sb["id"])
        g["sub"] = [sb for sb in g.get("sub", []) if sb["n"]]
    n += jsave(p, d)
print("объединение: изменено файлов", n, "| убраны из каталога:", ", ".join(sorted(gone)))
