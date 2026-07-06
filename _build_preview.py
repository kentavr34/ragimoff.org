# -*- coding: utf-8 -*-
"""
_build_preview.py v2 — Этап 1: ВСЕ главы разбиты на отдельные страницы расстройств.
Парсит структуру из index.html (главы+расстройства), генерит: страницы расстройств,
головные страницы глав, новое оглавление, новый сайдбар (ссылки на превью-страницы).
Компактная навигация (только коды, мобильно). Цвета — переменные тёмной темы.
Вывод: klinik-psixiatriya/preview/. Живые файлы не трогаем.
"""
import pathlib, re, json

RG = pathlib.Path(r"D:/Документы/ragimoff")
SITE = RG / "klinik-psixiatriya"
MASTER = RG / "_supplements" / "chapters-v2"
OUT = SITE / "preview"
OUT.mkdir(exist_ok=True)

# выверяемая таблица кодов XBT-10/DSM (источник — историческая версия f173c21; правится вручную)
CODES = json.loads((RG / "_codes_map.json").read_text(encoding="utf-8")) \
    if (RG / "_codes_map.json").exists() else {}
# соответствие расстройств классам DSM-5-TR (для DSM-оглавления; правится вручную)
DSM = json.loads((RG / "_dsm_toc.json").read_text(encoding="utf-8")) \
    if (RG / "_dsm_toc.json").exists() else {"classes": [], "assign": {}}

# английские названия глав (стандарт ВОЗ ICD-11) — для головной страницы главы
CH_EN = {
    "6A00–6A0Z": "Neurodevelopmental disorders",
    "6A20–6A2Z": "Schizophrenia or other primary psychotic disorders",
    "6A40": "Catatonia",
    "6A60–6A7Z": "Mood disorders",
    "6B00–6B0Z": "Anxiety or fear-related disorders",
    "6B20–6B2Z": "Obsessive-compulsive or related disorders",
    "6B40–6B4Z": "Disorders specifically associated with stress",
    "6B60–6B6Z": "Dissociative disorders",
    "6B80–6B8Z": "Feeding or eating disorders",
    "6C00–6C0Z": "Elimination disorders",
    "6C20": "Disorders of bodily distress or bodily experience",
    "6C40–6C5Z": "Disorders due to substance use or addictive behaviours",
    "6C70–6C7Z": "Impulse control disorders",
    "6C90–6C9Z": "Disruptive behaviour or dissocial disorders",
    "6D10–6D1Z": "Personality disorders and related traits",
    "6D30–6D3Z": "Paraphilic disorders",
    "6D50–6D5Z": "Factitious disorders",
    "6D70–6D8Z": "Neurocognitive disorders",
    "6E20–6E2Z": "Mental or behavioural disorders associated with pregnancy, childbirth or the puerperium",
    "6E40": "Psychological or behavioural factors affecting disorders classified elsewhere",
    "6E60–6E6Z": "Secondary mental or behavioural syndromes",
    "7A00–7A8Z": "Sleep-wake disorders",
    "HA00–HA0Z": "Conditions related to sexual health",
}

idx = (SITE / "index.html").read_text(encoding="utf-8")

# --- разбор глав из сайдбар-навигации index.html ---
chapters = []
for seg in re.split(r'(?=<div class="nav-item)', idx):
    if "nav-has-sub" not in seg:
        continue
    ms = re.search(r'data-slug="([^"]+)"', seg)
    if not ms:
        continue
    slug = ms.group(1)
    rng = re.search(r'<span class="nav-code">([^<]*)</span>', seg)
    ttl = re.search(r'<span class="nav-code">[^<]*</span>\s*<span>([^<]*)</span>', seg)
    ds = [(a.strip(), b.strip()) for a, b in
          re.findall(r'<span class="sub-code">([^<]*)</span><span class="sub-name">([^<]*)</span>', seg)]
    chapters.append({"slug": slug, "range": rng.group(1).strip() if rng else "",
                     "title": ttl.group(1).strip() if ttl else slug, "disorders": ds})

# --- оболочка из блок-страницы 02 ---
block = (SITE / "02-6A2-sizofreniya-spektri.html").read_text(encoding="utf-8")
top = block[: block.index('<div class="content-wrap">') + len('<div class="content-wrap">')]
bottom = block[block.index("  </main>"):]
for a, b in [('href="style.css"', 'href="../style.css"'), ('href="duzelis.css"', 'href="../duzelis.css"'),
             ('src="duzelis.js"', 'src="../duzelis.js"'), ('src="book.js"', 'src="../book.js"'),
             ('src="search.js"', 'src="../search.js"'), ('href="search-index.json"', 'href="../search-index.json"')]:
    top = top.replace(a, b); bottom = bottom.replace(a, b)

# --- новый сайдбар: ссылки на превью-страницы ---
def code_file(code):
    return f"{code}.html"

nav_html = ['<div class="nav-item" data-slug="index"><a href="index.html" class="nav-link"><span>Ana səhifə</span></a></div>']
for ch in chapters:
    subs = "".join(
        f'<a href="{code_file(c)}" class="nav-sub-link"><span class="sub-code">{c}</span>'
        f'<span class="sub-name">{n}</span></a>' for c, n in ch["disorders"])
    nav_html.append(
        f'<div class="nav-item nav-has-sub" data-slug="{ch["slug"]}">'
        f'<a href="{ch["slug"]}.html" class="nav-link is-bolme"><span class="nav-code">{ch["range"]}</span>'
        f'<span>{ch["title"]}</span></a>'
        f'<button class="nav-toggle" onclick="toggleSub(this)" tabindex="-1">▶</button>'
        f'<div class="nav-sub">{subs}</div></div>')
NEWNAV = "\n".join(nav_html)
# заменить содержимое <nav>...</nav> в оболочке
top = re.sub(r'(<nav>).*?(</nav>)', lambda m: m.group(1) + NEWNAV + m.group(2), top, count=1, flags=re.S)

EXTRA_CSS = """
<style>
/* ===== КНИЖНЫЙ ШАБЛОН — правим ТОЛЬКО контент. Шапку САЙТА не трогаем! ===== */
.content-wrap{max-width:44rem;margin:0 auto;padding:1.1rem 1.15rem 5.5rem}
.content-wrap p{margin:.72rem 0}
.content-wrap ul,.content-wrap ol{margin:.72rem 0;padding-left:1.3rem}
.content-wrap li{margin:.32rem 0}
.content-wrap h2{font-size:1.18rem;line-height:1.3;margin:1.8rem 0 .6rem;padding-bottom:.3rem;border-bottom:1px solid var(--border)}
.content-wrap h3{font-size:1.02rem;line-height:1.35;margin:1.15rem 0 .4rem;color:var(--text)}
.content-wrap table{font-size:.92rem}

/* хлебная крошка — тихая строка вверху (вместо сиротской полосы-навигации) */
.crumb{font-size:.82rem;margin:.1rem 0 1.1rem}
.crumb a{color:var(--text2);text-decoration:none}
.crumb a:hover{color:var(--gold)}

/* ШАПКА расстройства — выровненная «невидимая таблица» трёх классификаций */
table.dh{border-collapse:collapse;width:100%;margin:.2rem 0 1.5rem;border:0;border-bottom:2px solid var(--gold)}
table.dh td{border:0;padding:.24rem .7rem .24rem 0;vertical-align:baseline;text-align:left}
table.dh td:last-child{padding-right:0;width:100%}
table.dh .dh-lbl{font-family:var(--mono,monospace);font-size:.66rem;letter-spacing:.05em;text-transform:uppercase;color:var(--text3);white-space:nowrap;font-weight:700}
table.dh .dh-code{font-family:var(--mono,monospace);font-weight:700;color:var(--gold);white-space:nowrap;font-size:.9rem}
table.dh .dh-name{color:var(--text2);font-size:.94rem;line-height:1.3}
table.dh h1{font-size:1.42rem;line-height:1.2;margin:0;letter-spacing:-.01em;font-weight:800;color:var(--text)}
.dh-en{font-style:italic;color:var(--text2);font-size:.9rem;margin-top:.12rem;line-height:1.3;font-weight:400}
table.dh .dh-main .dh-lbl{color:var(--gold)}
table.dh .dh-main .dh-code{font-size:1.02rem}
table.dh .dh-main td{padding-bottom:.7rem}
table.dh tr:not(.dh-main) .dh-name{color:var(--text)}

/* мобайл: комфортная типографика (НИКАКИХ правок шапки сайта) */
@media(max-width:720px){
  body{font-size:16px;line-height:1.6}
  .content-wrap{padding:.9rem 1rem 5.5rem}
  table.dh h1{font-size:1.28rem}
  .content-wrap h2{font-size:1.1rem;margin-top:1.55rem}
  .content-wrap h3{font-size:.98rem}
  .content-wrap p{margin:.66rem 0}
}
/* ГОЛОВА ГЛАВЫ — одна строка: код + название, англ. ниже, подпись */
.chap-head{margin:.1rem 0 1.2rem;padding-bottom:.9rem;border-bottom:2px solid var(--gold)}
.chap-h1{font-size:1.5rem;line-height:1.22;margin:0;letter-spacing:-.01em;font-weight:800;color:var(--text);display:flex;flex-wrap:wrap;align-items:baseline;gap:.55rem}
.chap-range{font-family:var(--mono,monospace);color:var(--gold);font-size:1.02rem;font-weight:700;white-space:nowrap}
.chap-en{font-style:italic;color:var(--text2);font-size:.95rem;margin-top:.3rem;line-height:1.3}
.chap-sub{color:var(--text3);font-size:.88rem;margin:.6rem 0 0}
@media(max-width:720px){.chap-h1{font-size:1.28rem}.chap-range{font-size:.95rem}}
/* меню главы — выровнено в 2 колонки (код | название) */
.chapter-menu{display:flex;flex-direction:column;gap:.45rem;margin:1.3rem 0}
.ch-disorder{display:grid;grid-template-columns:3.8rem 1fr;align-items:baseline;gap:.7rem;padding:.7rem .9rem;border:1px solid var(--border);border-radius:8px;text-decoration:none;color:var(--text);background:var(--bg2);transition:.15s}
.ch-disorder:hover{background:var(--bg3);border-color:var(--gold)}
.ch-code{font-weight:700;color:var(--gold);font-family:var(--mono,monospace);font-variant-numeric:tabular-nums}
.ch-name{font-weight:600;color:var(--text)}
/* нижняя навигация — перелистывание (ТОЛЬКО внизу страницы) */
.d-nav{display:flex;align-items:center;justify-content:space-between;gap:.5rem;margin:2.2rem 0 .5rem;padding:.7rem 0 0;border-top:1px solid var(--border)}
.d-nav a{color:var(--text);text-decoration:none;padding:.35rem .7rem;border-radius:6px;font-family:var(--mono,monospace);font-weight:700;font-size:.95rem;white-space:nowrap}
.d-nav a:hover{background:var(--bg3);color:var(--gold)}
.d-nav .up{color:var(--gold);font-family:var(--font);font-weight:600}
.d-nav .dn-name{color:var(--text2);font-weight:400;font-family:var(--font);font-size:.85rem}
@media(max-width:640px){ .d-nav .dn-name{display:none} .d-nav a{padding:.3rem .5rem} }
.h-chapter{font-size:1.55rem;text-align:center;margin:1rem 0 .3rem;color:var(--text)}
.h-chapter .icd{display:block;color:var(--text2);font-size:.95rem;font-weight:600;letter-spacing:.05em;font-family:var(--mono,monospace)}
.toc-preview{display:flex;flex-direction:column;gap:1.2rem;margin:1.5rem 0}
.toc-ch{border:1px solid var(--border);border-radius:10px;overflow:hidden;background:var(--bg2)}
.toc-ch>a{display:flex;align-items:baseline;gap:.7rem;padding:.85rem 1rem;text-decoration:none;color:var(--text);font-weight:700;background:var(--bg3)}
.toc-ch>a:hover{color:var(--gold)}
.toc-ch .tc-range{color:var(--gold);font-family:var(--mono,monospace);min-width:5rem}
.toc-ch .tc-list{display:flex;flex-direction:column}
/* две выровненные колонки (невидимая таблица): код | название по одной вертикали */
.toc-ch .tc-list a{display:grid;grid-template-columns:4.2rem 1fr;gap:.6rem;align-items:baseline;padding:.5rem 1rem;text-decoration:none;color:var(--text2);border-top:1px solid var(--border)}
.toc-ch .tc-list a:hover{background:var(--bg3);color:var(--text)}
.toc-ch .tc-list .sc{color:var(--gold);font-family:var(--mono,monospace);font-variant-numeric:tabular-nums}
/* двойное оглавление: вкладки XBT-11 / DSM-5 */
.toc-tabs{display:flex;gap:.5rem;justify-content:center;margin:1rem 0 .4rem}
.toc-tab{background:var(--bg2);border:1px solid var(--border);color:var(--text2);border-radius:8px;padding:.5rem 1.15rem;font-weight:700;font-size:.95rem;cursor:pointer;font-family:var(--mono,monospace);letter-spacing:.02em;transition:.15s}
.toc-tab:hover{color:var(--text);border-color:var(--gold)}
.toc-tab.is-active{background:var(--gold);color:var(--bg);border-color:var(--gold)}
.toc-meta{text-align:center;color:var(--text2);margin:.2rem 0 1rem;font-size:.9rem}
.tc-head{display:flex;align-items:baseline;gap:.7rem;padding:.85rem 1rem;color:var(--text);font-weight:700;background:var(--bg3)}
.tc-head .tc-range{color:var(--gold);font-family:var(--mono,monospace);min-width:5rem}
/* ЕДИНАЯ ТИПОГРАФИКА бокового меню (и раскрывающегося overlay) + выравнивание в 2 колонки.
   Только для превью-страниц (EXTRA_CSS в них) — живой сайт не трогаем. */
.sidebar nav .nav-link{font-size:.92rem;letter-spacing:0}
.sidebar nav .nav-code{font-family:var(--mono,monospace);font-size:.8rem;font-variant-numeric:tabular-nums}
.sidebar nav .nav-sub-link{display:grid;grid-template-columns:3.7rem 1fr;gap:.5rem;align-items:baseline;font-size:.85rem}
.sidebar nav .sub-code{color:var(--gold);font-family:var(--mono,monospace);font-size:.78rem;font-variant-numeric:tabular-nums;min-width:0}
.sidebar nav .sub-name{color:var(--text2)}
</style>
"""


def page(content, title):
    t = top.replace("MÜNDƏRİCAT | KLİNİK PSİXİATRİYA", f"{title} | KLİNİK PSİXİATRİYA")
    t = t.replace("</head>", EXTRA_CSS + "</head>")
    return t + "\n" + content + "\n" + bottom


def d_nav(chp, i):
    ds = chp["disorders"]
    prev = ds[i - 1] if i > 0 else None
    nxt = ds[i + 1] if i < len(ds) - 1 else None
    l = (f'<a href="{prev[0]}.html">← {prev[0]} <span class="dn-name">{prev[1][:22]}</span></a>'
         if prev else "<span></span>")
    r = (f'<a href="{nxt[0]}.html"><span class="dn-name">{nxt[1][:22]}</span> {nxt[0]} →</a>'
         if nxt else "<span></span>")
    up = f'<a class="up" href="{chp["slug"]}.html">↑ Fəsil</a>'
    return f'<nav class="d-nav">{l}{up}{r}</nav>'


def crumb(chp):
    t = chp["title"]
    t = (t[:40] + "…") if len(t) > 41 else t
    return f'<nav class="crumb"><a href="{chp["slug"]}.html">‹ {t}</a></nav>'


def crumb_top():
    return '<nav class="crumb"><a href="index.html">‹ Ana səhifə</a></nav>'


def build_dh(frag, code, fallback_name):
    """Шапка расстройства = выровненная «невидимая таблица» трёх классификаций,
    единый стандарт: XBT-11 (главный: код+AZ-имя+англ.курсив), затем XBT-10 и DSM-5-TR —
    у каждой свой код и своё название в этой классификации. Исходный H1 фрагмента убираем."""
    info = CODES.get(code, {})
    az = info.get("name_az") or ""
    if not az:
        m = re.search(r'<h1[^>]*class="h-disorder"[^>]*>(.*?)</h1>', frag, re.S)
        if m:
            inner = re.sub(r'<span[^>]*class="icd"[^>]*>.*?</span>', '', m.group(1), flags=re.S)
            az = re.sub(r'<[^>]+>', '', inner).strip()
    az = az or fallback_name
    en = info.get("en11") or ""
    if not en:
        me = re.search(r'XBT-11:\s*<span[^>]*class="icd"[^>]*>[^<]*</span>\s*([^;<)]+)', frag)
        if me:
            en = re.sub(r'\s+', " ", me.group(1)).strip().rstrip("/").strip()
    i10 = info.get("icd10") or ""
    dsm = info.get("dsm") or ""

    # итоговое название — азербайджанское, ОДИНАКОВОЕ во всех трёх классификациях; отличаются коды
    en_html = f'<div class="dh-en">{en}</div>' if en else ""
    rows = [f'<tr class="dh-main"><td class="dh-lbl">XBT-11</td><td class="dh-code">{code}</td>'
            f'<td class="dh-name"><h1>{az}</h1>{en_html}</td></tr>']
    if i10:
        rows.append(f'<tr><td class="dh-lbl">XBT-10</td><td class="dh-code">{i10}</td>'
                    f'<td class="dh-name">{az}</td></tr>')
    if dsm:
        rows.append(f'<tr><td class="dh-lbl">DSM-5-TR</td><td class="dh-code">{dsm}</td>'
                    f'<td class="dh-name">{az}</td></tr>')
    dh = f'<table class="dh"><tbody>{"".join(rows)}</tbody></table>'
    body = re.sub(r'<h1[^>]*class="h-disorder"[^>]*>.*?</h1>', "", frag, count=1, flags=re.S)
    return dh + body


made_d, made_c = 0, 0
for chp in chapters:
    ds = chp["disorders"]
    # страницы расстройств: крошка → книжная шапка → контент → нижняя навигация
    for i, (code, name) in enumerate(ds):
        mf = MASTER / f"{code}.html"
        frag = mf.read_text(encoding="utf-8") if mf.exists() else \
            f'<h1 class="h-disorder"><span class="icd">{code}</span> {name}</h1>' \
            f'<p style="color:var(--text2)">Bu bölmə hazırlanır.</p>'
        content = crumb(chp) + build_dh(frag, code, name) + d_nav(chp, i)
        (OUT / f"{code}.html").write_text(page(content, name), encoding="utf-8")
        made_d += 1
    # головная страница главы
    links = "".join(
        f'<a class="ch-disorder" href="{c}.html"><span class="ch-code">{c}</span>'
        f'<span class="ch-name">{n}</span></a>' for c, n in ds)
    ch_en = CH_EN.get(chp["range"], "")
    en_line = f'<div class="chap-en">{ch_en}</div>' if ch_en else ""
    head = (f'{crumb_top()}'
            f'<header class="chap-head">'
            f'<h1 class="chap-h1"><span class="chap-range">{chp["range"]}</span>'
            f'<span class="chap-title">{chp["title"]}</span></h1>{en_line}'
            f'<p class="chap-sub">Bu fəsildəki pozuntular — hər biri ayrıca səhifə:</p></header>'
            f'<div class="chapter-menu">{links}</div>')
    (OUT / f'{chp["slug"]}.html').write_text(page(head, chp["title"]), encoding="utf-8")
    made_c += 1

# --- ДВОЙНОЕ оглавление превью (index.html): XBT-11 по главам + DSM-5 по классам ---
name_of = {c: n for chp in chapters for c, n in chp["disorders"]}

# панель XBT-11 — по главам
icd_ch = ""
for chp in chapters:
    lst = "".join(f'<a href="{c}.html"><span class="sc">{c}</span><span>{n}</span></a>' for c, n in chp["disorders"])
    icd_ch += (f'<div class="toc-ch"><a href="{chp["slug"]}.html">'
               f'<span class="tc-range">{chp["range"]}</span><span>{chp["title"]}</span></a>'
               f'<div class="tc-list">{lst}</div></div>')

# панель DSM-5 — по классам DSM
def dsm_code(c):
    return (CODES.get(c, {}) or {}).get("dsm") or ""

groups = {}
for c in name_of:
    groups.setdefault(DSM.get("assign", {}).get(c, "other"), []).append(c)

def dsm_sort(c):
    d = dsm_code(c)
    try:
        return (0, float(d))
    except ValueError:
        return (1, c)

dsm_ch = ""
n_class = 0
for key, title in DSM.get("classes", []):
    items = groups.get(key)
    if not items:
        continue
    n_class += 1
    items = sorted(items, key=dsm_sort)
    # итоговое название — азербайджанское (одинаковое во всех вкладках); в DSM меняется только код
    lst = "".join(
        f'<a href="{c}.html"><span class="sc">{dsm_code(c) or "—"}</span><span>{name_of[c]}</span></a>'
        for c in items)
    dsm_ch += (f'<div class="toc-ch"><div class="tc-head">'
               f'<span>{title}</span></div>'
               f'<div class="tc-list">{lst}</div></div>')

tabs = ('<div class="toc-tabs">'
        '<button class="toc-tab is-active" data-toc="icd" onclick="tocTab(this)">XBT-11</button>'
        '<button class="toc-tab" data-toc="dsm" onclick="tocTab(this)">DSM-5-TR</button></div>')
toggle_js = ('<script>function tocTab(b){var k=b.getAttribute("data-toc");'
             'document.querySelectorAll(".toc-tab").forEach(function(t){t.classList.toggle("is-active",t===b);});'
             'document.querySelectorAll(".toc-panel").forEach(function(p){p.hidden=(p.getAttribute("data-panel")!==k);});}'
             '</script>')
toc = (f'<h1 class="h-chapter">ANA SƏHİFƏ</h1>{tabs}'
       f'<div class="toc-panel" data-panel="icd">'
       f'<p class="toc-meta">{made_d} pozuntu · {made_c} fəsil</p>'
       f'<div class="toc-preview">{icd_ch}</div></div>'
       f'<div class="toc-panel" data-panel="dsm" hidden>'
       f'<p class="toc-meta">{made_d} pozuntu · {n_class} sinif</p>'
       f'<div class="toc-preview">{dsm_ch}</div></div>{toggle_js}')
(OUT / "index.html").write_text(page(toc, "Mündəricat"), encoding="utf-8")

print(f"глав: {made_c} | расстройств: {made_d}")
print("оглавление превью: preview/index.html")
