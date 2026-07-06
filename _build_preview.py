# -*- coding: utf-8 -*-
"""
_build_preview.py v2 — Этап 1: ВСЕ главы разбиты на отдельные страницы расстройств.
Парсит структуру из index.html (главы+расстройства), генерит: страницы расстройств,
головные страницы глав, новое оглавление, новый сайдбар (ссылки на превью-страницы).
Компактная навигация (только коды, мобильно). Цвета — переменные тёмной темы.
Вывод: klinik-psixiatriya/preview/. Живые файлы не трогаем.
"""
import pathlib, re

RG = pathlib.Path(r"D:/Документы/ragimoff")
SITE = RG / "klinik-psixiatriya"
MASTER = RG / "_supplements" / "chapters-v2"
OUT = SITE / "preview"
OUT.mkdir(exist_ok=True)

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

nav_html = ['<div class="nav-item" data-slug="index"><a href="index.html" class="nav-link"><span>Mündəricat</span></a></div>']
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

/* ТИТУЛЬНЫЙ БЛОК расстройства — книжная шапка страницы */
.dh{margin:.1rem 0 1.5rem;padding-bottom:1rem;border-bottom:2px solid var(--gold)}
.dh-kicker{font-family:var(--mono,monospace);font-size:.78rem;letter-spacing:.09em;color:var(--gold);font-weight:700;text-transform:uppercase;margin-bottom:.4rem}
.dh h1{font-size:1.6rem;line-height:1.18;margin:0 0 .35rem;letter-spacing:-.01em;color:var(--text)}
.dh-en{font-style:italic;color:var(--text2);font-size:.96rem;margin:0 0 .8rem;line-height:1.3}
.dh-codes{display:flex;flex-wrap:wrap;gap:.4rem}
.dh-c{display:inline-flex;align-items:baseline;gap:.35rem;background:var(--bg2);border:1px solid var(--border);border-radius:6px;padding:.24rem .55rem}
.dh-c b{color:var(--text3);font-weight:600;font-size:.68rem;letter-spacing:.04em;text-transform:uppercase}
.dh-c i{color:var(--gold);font-style:normal;font-family:var(--mono,monospace);font-weight:700;font-size:.82rem}

/* мобайл: комфортная типографика (НИКАКИХ правок шапки сайта) */
@media(max-width:720px){
  body{font-size:16px;line-height:1.6}
  .content-wrap{padding:.9rem 1rem 5.5rem}
  .dh h1{font-size:1.4rem}
  .content-wrap h2{font-size:1.1rem;margin-top:1.55rem}
  .content-wrap h3{font-size:.98rem}
  .content-wrap p{margin:.66rem 0}
}
.chapter-menu{display:flex;flex-direction:column;gap:.45rem;margin:1.3rem 0}
.ch-disorder{display:flex;align-items:baseline;gap:.7rem;padding:.7rem .9rem;border:1px solid var(--border);border-radius:8px;text-decoration:none;color:var(--text);background:var(--bg2);transition:.15s}
.ch-disorder:hover{background:var(--bg3);border-color:var(--gold)}
.ch-code{font-weight:700;color:var(--gold);min-width:3.6rem;font-family:var(--mono,monospace)}
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
.toc-ch .tc-list a{display:flex;gap:.6rem;padding:.5rem 1rem;text-decoration:none;color:var(--text2);border-top:1px solid var(--border)}
.toc-ch .tc-list a:hover{background:var(--bg3);color:var(--text)}
.toc-ch .tc-list .sc{color:var(--gold);font-family:var(--mono,monospace);min-width:3.4rem}
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


def build_dh(frag, code, fallback_name):
    """Книжная шапка расстройства: кикер XBT-11·код, H1 (AZ), англ. курсивом, строка кодов.
    H1 берём из фрагмента, англ. название и DSM-код — из первого абзаца; исходный H1 убираем."""
    m = re.search(r'<h1[^>]*class="h-disorder"[^>]*>(.*?)</h1>', frag, re.S)
    if m:
        inner = re.sub(r'<span[^>]*class="icd"[^>]*>.*?</span>', '', m.group(1), flags=re.S)
        title = re.sub(r'<[^>]+>', '', inner).strip()
    else:
        title = ""
    title = title or fallback_name
    # английское название международной классификации (после code-span в абзаце "XBT-11: …")
    en = ""
    me = re.search(r'XBT-11:\s*<span[^>]*class="icd"[^>]*>[^<]*</span>\s*([^;<)]+)', frag)
    if me:
        en = re.sub(r'\s+', " ", me.group(1)).strip().rstrip("/").strip()
    # DSM-5-TR код из первого абзаца (если указан)
    dsm = ""
    md = re.search(r'DSM-5-TR:\s*([0-9][0-9.]*)', frag)
    if md:
        dsm = md.group(1)
    chips = ""
    if dsm:
        chips += f'<span class="dh-c"><b>DSM-5-TR</b><i>{dsm}</i></span>'
    codes_html = f'<div class="dh-codes">{chips}</div>' if chips else ""
    en_html = f'<div class="dh-en">{en}</div>' if en else ""
    dh = (f'<header class="dh"><div class="dh-kicker">XBT-11 · {code}</div>'
          f'<h1>{title}</h1>{en_html}{codes_html}</header>')
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
    head = (f'<h1 class="h-chapter"><span class="icd">{chp["range"]} · XBT-11</span>{chp["title"]}</h1>'
            f'<p style="text-align:center;color:var(--text2)">Bu fəsildəki pozuntular — hər biri ayrıca səhifə:</p>'
            f'<div class="chapter-menu">{links}</div>')
    (OUT / f'{chp["slug"]}.html').write_text(page(head, chp["title"]), encoding="utf-8")
    made_c += 1

# --- оглавление превью (index.html) ---
toc_ch = ""
for chp in chapters:
    lst = "".join(f'<a href="{c}.html"><span class="sc">{c}</span><span>{n}</span></a>' for c, n in chp["disorders"])
    toc_ch += (f'<div class="toc-ch"><a href="{chp["slug"]}.html">'
               f'<span class="tc-range">{chp["range"]}</span><span>{chp["title"]}</span></a>'
               f'<div class="tc-list">{lst}</div></div>')
toc = (f'<h1 class="h-chapter">MÜNDƏRİCAT</h1>'
       f'<p style="text-align:center;color:var(--text2)">XBT-11 · {made_d} pozuntu · {made_c} fəsil</p>'
       f'<div class="toc-preview">{toc_ch}</div>')
(OUT / "index.html").write_text(page(toc, "Mündəricat"), encoding="utf-8")

print(f"глав: {made_c} | расстройств: {made_d}")
print("оглавление превью: preview/index.html")
