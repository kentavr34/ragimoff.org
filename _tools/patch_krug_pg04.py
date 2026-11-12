# -*- coding: utf-8 -*-
"""Четвёртый круг критика (12.11.2026): прототип магазина, правовой блок, азербайджанский. Повторный запуск ничего не меняет.
Магазин: у каждого тома свой адрес (по адресу чтения, а не по картинке обложки); цена печатной книги одинакова на трёх языках
(берётся из азербайджанского каталога — он полнее); число страниц в описании совпадает со строкой сведений."""
import io, os, sys, json, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(D)


def rep(s, a, b):
    assert s.count(a) == 1, "ожидалось 1: " + a[:70]
    return s.replace(a, b)


p = "_tools/build_shop.py"
s = io.open(p, encoding="utf-8").read()
if "def book_id" not in s:
    s = rep(s, "for lang, rel in SRC.items():", '''def book_id(img, href):
    """Свой адрес у каждой книги: у авторских — по обложке (klinik, guilt…), у томов Фрейда — по адресу чтения."""
    base = os.path.basename(img).split("?")[0].rsplit(".", 1)[0] if img else ""
    if base in ("klinik", "guilt", "pandemic", "phoenix"):
        return base
    parts = [x for x in href.strip("/").split("/") if x and x not in ("books", "ru", "en", "az")]
    return parts[-1] if parts else base


AZ_PRICE = {}
for lang, rel in sorted(SRC.items(), key=lambda x: x[0] != "az"):''')
    s = rep(s, '''        it = {"id": os.path.basename(img).rsplit(".", 1)[0] if img else re.sub(r"\\W+", "-", el.get("data-title", "")).lower(),''',
            '''        it = {"id": book_id(img, (a.get("href") if a else "") or ""),''')
    s = rep(s, '        cur["items"].append(it)', '''        if lang == "az":
            AZ_PRICE[it["id"]] = it["price"]
        elif not it["price"] and AZ_PRICE.get(it["id"]):
            it["price"] = AZ_PRICE[it["id"]]                     # цена печатной книги одна на всех языках
        cur["items"].append(it)''')
    s = rep(s, '''                    it["k"], it["f"] = facts[lang][i]["k"], facts[lang][i]["f"]''',
            '''                    it["k"], it["f"] = facts[lang][i]["k"], list(facts[lang][i]["f"])
                    mp = re.search(r"(\\d{3,4})\\s*(стр|səh|pp|pages)", it["meta"])         # число страниц в описании — как в сведениях о книге
                    if mp:
                        it["f"] = [re.sub(r"\\b8[0-9]{2}\\b(?=\\s*(печатн|çap|printed))", mp.group(1), x) for x in it["f"]]''')
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
    print("build_shop: адреса книг, цены, страницы")

p = "assets/js/page-shop.js"
s = io.open(p, encoding="utf-8").read()
if "shp__nf" not in s:
    s = rep(s, "const it = all.find(x => x.id === bid) || all[0];", "const it = all.find(x => x.id === bid); if (!it) { location.replace('shop.html'); return; }                 /* нет такой книги — в каталог */")
    s = rep(s, "const sib = all.filter(x => x.g.id === it.g.id && x.id !== it.id).slice(0, 8), other = sib.length >= 3 ? sib : all.filter(x => x.id !== it.id && x.f).concat(sib).slice(0, 8);",
            "const sib = all.filter(x => x.g.id === it.g.id && x.id !== it.id), lead = all.filter(x => x.id !== it.id && x.f && x.g.id !== it.g.id), seen = {};\n  const other = (sib.length >= 3 ? sib : sib.concat(lead)).filter(x => !seen[x.id] && (seen[x.id] = 1)).slice(0, 8);   /* shp__nf: без повторов */")
    s = rep(s, "${it.k ? `<p class=\"pp__kind\">${esc(it.k)}</p>` : `<p class=\"pp__kind\">${esc(it.y)}</p>`}<h1", "<p class=\"pp__kind\">${esc(it.k || it.g.name)}</p><h1")
    s = rep(s, "<p class=\"shp__au\">${esc(it.g.name)}</p><p class=\"shp__m\">", "${it.k ? `<p class=\"shp__au\">${esc(it.g.name)}</p>` : ''}<p class=\"shp__m\">")
    s = rep(s, "`<p class=\"pp__kind\">Doctor Ragimoff</p><h1 class=\"pp__t\">${esc(d.title)}</h1>", "`<h1 class=\"pp__t\">${esc(d.title)}</h1>")
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
    print("page-shop: без повторов, нет книги → каталог")

p = "assets/js/page-program.js"
s = io.open(p, encoding="utf-8").read()
if "lb--doc" not in s:
    s = rep(s, "const z = e.target.closest('.gal__i'); if (z) { const lb = $('#lb');", "const z = e.target.closest('.gal__i'); if (z) { const lb = $('#lb'); lb.classList.add('lb--doc');     /* документ открывается во всю ширину и листается */")
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
    print("page-program: документ в полный размер")

p = "_tools/pages_check.py"
s = io.open(p, encoding="utf-8").read()
if "book.html?b=art-freud-gw02" in s:
    s = s.replace("book.html?b=art-freud-gw02", "book.html?b=freud-gw02")
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)

# подписи к выписке из реестра: откуда второй номер и название
CAP = {"ru": ("Выписка из реестра лицензий — страница 1", "Выписка из реестра лицензий (26.06.2023): лицензия действует, регистрационный № Л035-01282-43/00222332, нынешнее название — Санкт-Петербургский институт ДПО для психологов и психотерапевтов"),
       "az": ("Lisenziyalar reyestrindən çıxarış — 1-ci səhifə", "Lisenziyalar reyestrindən çıxarış (26.06.2023): lisenziya qüvvədədir, qeydiyyat № Л035-01282-43/00222332, indiki ad — Sankt-Peterburq Psixoloqlar və Psixoterapevtlər üçün Əlavə Təhsil İnstitutu"),
       "en": ("Extract from the register of licences — page 1", "Extract from the register of licences (26.06.2023): the licence is valid, registration No. Л035-01282-43/00222332, current name — St Petersburg Institute of Additional Professional Education for Psychologists and Psychotherapists")}
CAP0 = {"ru": ("Лицензия на образовательную деятельность № 1724 от 05.10.2020 — страница 1", "Лицензия на образовательную деятельность № 1724 от 05.10.2020 (выдана под прежним названием института) — страница 1"),
        "az": ("Təhsil fəaliyyəti üzrə lisenziya № 1724, 05.10.2020 — 1-ci səhifə", "Təhsil fəaliyyəti üzrə lisenziya № 1724, 05.10.2020 (institutun əvvəlki adı ilə verilib) — 1-ci səhifə"),
        "en": ("Licence for educational activity No. 1724 of 05.10.2020 — page 1", "Licence for educational activity No. 1724 of 05.10.2020 (issued under the institute’s former name) — page 1")}
for l in ("ru", "az", "en"):
    fn = "_agent/archive/law_page/law.%s.json" % l
    t = io.open(fn, encoding="utf-8").read()
    t2 = t.replace(json.dumps(CAP[l][0], ensure_ascii=False), json.dumps(CAP[l][1], ensure_ascii=False)).replace(json.dumps(CAP0[l][0], ensure_ascii=False), json.dumps(CAP0[l][1], ensure_ascii=False))
    if t2 != t:
        io.open(fn, "w", encoding="utf-8", newline="\n").write(t2)
        print("подписи лицензии:", l)

# азербайджанский: оставшиеся опечатки и кальки
AZ = [("Struktur pozuntularıı", "Struktur pozuntuları"), ("məsləhətləşmələşmə", "məsləhətləşmə"),
      ("Dərman olmadan belə nəticə görmüşdüm ki deyərdim yalan. Amma özüm gözümüzlə gördüm.", "Dərmansız belə nəticə ola biləcəyinə inanmazdım. Amma öz gözümlə gördüm."),
      ("birinci xətt müalicəsində", "birinci sıra müalicəsində"), ("real keyslərin izahı", "real klinik halların izahı"),
      ("@kragimoff — Kanala Bax", "@kragimoff — kanala baxın"), ("IPAS Ambassador", "IPAS Ambasadoru")]
n = 0
for fn in glob.glob("data/*/*.az.json"):
    t = io.open(fn, encoding="utf-8").read()
    o = t
    for a, b in AZ:
        t = t.replace(a, b)
    if "enurez" in fn:
        t = t.replace("<strong>WHO, ICCS, NICE, EAU/ESPU</strong>", "<strong>ÜST, ICCS, NICE, EAU/ESPU</strong>").replace("(WHO, ICCS,", "(ÜST, ICCS,")
    if t != o:
        io.open(fn, "w", encoding="utf-8", newline="\n").write(t)
        n += 1
print("азербайджанских файлов:", n)
p = "assets/js/programs.js"
s = io.open(p, encoding="utf-8").read()
o = s
for a, b in [("Keysin koqnitiv konseptuallaşdırılması", "Klinik halın koqnitiv konseptuallaşdırılması"), ("Öz keysləriniz üzrə", "Öz klinik hallarınız üzrə"), ("Keyslərin təhlili", "Klinik halların təhlili"),
             ("Qəbul və məsuliyyət terapiyası (ACT)", "Qəbul və öhdəlik terapiyası (ACT)"), ("şüurluluğa əsaslanan terapiya", "şüurlu fərqindəlik əsaslı koqnitiv terapiya")]:
    s = s.replace(a, b)
if s != o:
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
    print("programs.js: термины КПТ по книге")

# надпись над заголовком одинакова по смыслу на трёх языках
EYE = {"panik-ataklar": "KLİNİK TERAPİYA", "depressiya": "KLİNİK TERAPİYA", "sosial-fobiya": "KLİNİK TERAPİYA"}
for slug, e in EYE.items():
    fn = "data/cons/%s.az.json" % slug
    d = json.load(io.open(fn, encoding="utf-8"))
    if d.get("eye") != e:
        d["eye"] = e
        json.dump(d, io.open(fn, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
for fn in glob.glob("data/*/*.en.json"):
    t = io.open(fn, encoding="utf-8").read()
    t2 = t.replace("PARENTS SCHOOL", "PARENTS’ SCHOOL").replace("Child-Parent therapy", "Child–parent therapy").replace("Child-Parent Therapy", "Child–parent therapy")
    if t2 != t:
        io.open(fn, "w", encoding="utf-8", newline="\n").write(t2)
