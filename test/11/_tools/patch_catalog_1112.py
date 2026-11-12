# -*- coding: utf-8 -*-
"""Каталог книг (слова владельца 12.11.2026). Повторный запуск ничего не меняет.
 1. Название энуреза: «ночное недержание мочи» (так грамматически верно; замечание критика принято).
 2. Каталог Фрейда отсортирован по разделам: собрание сочинений (книги по номерам), переписка, ранние и отдельные работы,
    антология; тексты в несколько страниц (до 10) — не книги: идут отдельным списком без обложки
    (две такие работы стояли с одной и той же чужой обложкой).
 3. Адрес книги — имя её папки (раньше у двух работ адресом было имя файла главы)."""
import io, os, sys, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(D)


def rep(s, a, b):
    assert s.count(a) == 1, "ожидалось 1: " + a[:70]
    return s.replace(a, b)


# 1. энурез
PAIRS = [(u"Ночной энурез (ночное мочеиспускание)", u"Ночной энурез (ночное недержание мочи)"), (u"Gecə enurezi (gecə sidik ifrazı)", u"Gecə enurezi (gecə sidik saxlamama)")]
n = 0
for fn in glob.glob("data/*/*.json") + ["assets/js/content.js", "_tools/patch_owner_1112.py"]:
    s = io.open(fn, encoding="utf-8").read()
    o = s
    for a, b in PAIRS:
        s = s.replace(a, b)
    if s != o:
        for _ in range(6):
            try:
                io.open(fn, "w", encoding="utf-8", newline="\n").write(s)
                break
            except OSError:
                import time; time.sleep(1.2)
        n += 1
print("название энуреза исправлено в файлах:", n)

# 2–3. каталог
p = "_tools/build_shop.py"
s = io.open(p, encoding="utf-8").read()
if "SUBS = " not in s:
    s = rep(s, '''    parts = [x for x in href.strip("/").split("/") if x and x not in ("books", "ru", "en", "az")]''',
            '''    parts = [x for x in href.strip("/").split("/") if x and x not in ("books", "ru", "en", "az") and not x.endswith(".html")]      # адрес — папка книги, не файл главы''')
    s = rep(s, "AZ_PRICE = {}", '''AZ_PRICE = {}
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
    m = re.match(r"^(?:Книга|Kitab|Book)\\s+(\\d+)", it["meta"])
    if m:
        return "series", int(m.group(1))
    if re.search(r"писем|məktub|letters", it["meta"]):
        return "letters", 0
    if "aforizm" in it["id"]:
        return "anthology", 0
    pg = re.search(r"(\\d+)\\s*(?:стр|səh|pp)", it["meta"])
    if pg and int(pg.group(1)) <= 10:
        return "small", int(pg.group(1))
    return "early", 0''')
    s = rep(s, '    h = H[lang]\n', '''    for g in groups:
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
''')
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
    print("build_shop: разделы каталога и адреса книг")

p = "assets/js/page-shop.js"
s = io.open(p, encoding="utf-8").read()
if "const card = " not in s:
    # одна карточка книги на весь сайт: каталог, «Другие книги» — меняется в одном месте
    s = rep(s, "function shop(d, lang) {", '''/* ЕДИНАЯ КАРТОЧКА КНИГИ: обложка, название, сведения, цена. Используется в каталоге и в блоке «Другие книги» —
   изменение здесь меняет вид всех книг сразу. Малые тексты (несколько страниц) выводятся строкой без обложки. */
const card = (it, lang) => `<a class="shp__card rv" href="${url(it)}"><span class="shp__cv">${cover(it, lang)}</span><span class="shp__cb"><b>${esc(it.t)}</b><span>${esc(it.meta)}</span>${it.price ? `<em>${esc(it.price)}</em>` : ''}</span></a>`;
const line = it => `<li><a href="${esc(it.read_new || it.href)}"><b>${esc(it.t)}</b><span>${esc(it.meta)}</span></a></li>`;
const grid = (items, lang) => items.length ? `<div class="shp__grid">${items.map(it => card(it, lang)).join('')}</div>` : '';

function shop(d, lang) {''')
    s = rep(s, '''      ${rest.length ? `<div class="shp__grid">${rest.map(it => `<a class="shp__card rv" href="${url(it)}"><span class="shp__cv">${cover(it, lang)}</span><span class="shp__cb"><b>${esc(it.t)}</b><span>${esc(it.meta)}</span>${it.price ? `<em>${esc(it.price)}</em>` : ''}</span></a>`).join('')}</div>` : ''}''',
            '''      ${g.sub ? g.sub.map(sb => { const its = rest.filter(it => it.sec === sb.id); return `<h3 class="shp__sh rv"><span>${esc(sb.t)}</span><i>${sb.n}</i></h3>` + (sb.id === 'small' ? `<p class="shp__note rv">${esc(g.smallNote || '')}</p><ul class="shp__lines rv">${its.map(line).join('')}</ul>` : grid(its, lang)); }).join('') : grid(rest, lang)}''')
    s = rep(s, '''    <div class="shp__grid">${other.map(x => `<a class="shp__card rv" href="${url(x)}"><span class="shp__cv">${cover(x, lang)}</span><span class="shp__cb"><b>${esc(x.t)}</b><span>${esc(x.meta)}</span>${x.price ? `<em>${esc(x.price)}</em>` : ''}</span></a>`).join('')}</div></div></section>`;''',
            '''    ${grid(other, lang)}</div></section>`;''')
    s = rep(s, "const sib = all.filter(x => x.g.id === it.g.id && x.id !== it.id), lead =", "const sib = all.filter(x => x.g.id === it.g.id && x.id !== it.id && !x.small && (!it.sec || x.sec === it.sec || it.small)), lead =")
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
    print("page-shop: единая карточка, разделы каталога")

p = "_agent/lab/shp2.css"
if not os.path.exists(p):
    io.open(p, "w", encoding="utf-8", newline="\n").write("""
/* SHP: разделы каталога и список малых текстов (12.11.2026) */
.shp__sh { display: flex; align-items: baseline; gap: var(--p12); margin-top: var(--r3); padding-bottom: var(--p10); border-bottom: 1px solid var(--line); font: 400 clamp(22px, 2vw, 30px)/1.15 var(--f-display); color: var(--milk); }
.shp__sh i { font: 400 13px/1 var(--f-num); font-style: normal; letter-spacing: .14em; color: var(--gold); }
.shp__sh + .shp__note { margin-top: var(--p14); max-width: 70ch; }
.shp__lines { list-style: none; margin: var(--p14) 0 0; padding: 0; border-top: 1px solid var(--line); }
.shp__lines a { display: flex; align-items: baseline; justify-content: space-between; gap: var(--r1); min-height: var(--tap); padding: var(--p12) 0; border-bottom: 1px solid var(--line); }
.shp__lines b { font: 400 clamp(18px, 1.4vw, 21px)/1.3 var(--f-display); color: var(--milk); transition: color var(--t1); } .shp__lines a:hover b { color: var(--gold-hi); }
.shp__lines span { flex: 0 0 auto; font: 400 13px/1.3 var(--f-num); color: var(--smoke); }
@media (max-width: 760px) { .shp__lines a { flex-direction: column; gap: var(--p4); } }
""")
    print("стили разделов каталога подготовлены (_agent/lab/shp2.css) — будут добавлены в site.css после переноса «Клинической психиатрии»")
