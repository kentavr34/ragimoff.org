# -*- coding: utf-8 -*-
"""
_build_preview.py — Этап 1, ПРЕВЬЮ: дробление главы на отдельные страницы расстройств.
Демо на главе «Шизофрения-спектр» (6A20–6A25). Переиспуем существующую оболочку/дизайн.
Живые файлы НЕ трогаем — вывод в klinik-psixiatriya/preview/.
"""
import pathlib

RG = pathlib.Path(r"D:/Документы/ragimoff")
SITE = RG / "klinik-psixiatriya"
MASTER = RG / "_supplements" / "chapters-v2"
OUT = SITE / "preview"
OUT.mkdir(exist_ok=True)

# --- оболочка из блок-страницы 02 ---
block = (SITE / "02-6A2-sizofreniya-spektri.html").read_text(encoding="utf-8")
MARK_TOP = '<div class="content-wrap">'
top = block[: block.index(MARK_TOP) + len(MARK_TOP)]
bottom = block[block.index("  </main>"):]

# ссылки на style.css/duzelis лежат на уровень выше (preview/ вложена) → поправить относительные пути
top = top.replace('href="style.css"', 'href="../style.css"').replace('href="duzelis.css"', 'href="../duzelis.css"')
top = top.replace('src="duzelis.js"', 'src="../duzelis.js"')
bottom = bottom.replace('src="book.js"', 'src="../book.js"').replace('src="search.js"', 'src="../search.js"')

# небольшой доп-стиль для новых элементов (головная страница главы + навигация расстройств)
EXTRA_CSS = """
<style>
/* новые элементы превью используют ПЕРЕМЕННЫЕ ТЕМЫ сайта (тёмная тема — текст светлый) */
.chapter-menu{display:flex;flex-direction:column;gap:.5rem;margin:1.5rem 0}
.ch-disorder{display:flex;align-items:baseline;gap:.8rem;padding:.75rem 1rem;border:1px solid var(--border);border-radius:8px;text-decoration:none;color:var(--text);background:var(--bg2);transition:.15s}
.ch-disorder:hover{background:var(--bg3);border-color:var(--gold)}
.ch-code{font-weight:700;color:var(--gold);min-width:3.4rem;font-family:var(--mono,monospace)}
.ch-name{font-weight:600;color:var(--text)}
.d-nav{display:flex;justify-content:space-between;gap:1rem;margin:1.2rem 0;padding:.6rem 0;border-top:1px solid var(--border);border-bottom:1px solid var(--border);font-size:.9rem}
.d-nav a{color:var(--text2);text-decoration:none;padding:.3rem .6rem;border-radius:6px}
.d-nav a:hover{background:var(--bg3);color:var(--text)}
.d-nav .up{font-weight:600;color:var(--gold)}
.h-chapter{font-size:1.6rem;text-align:center;margin:1rem 0 .3rem;color:var(--text)}
.h-chapter .icd{display:block;color:var(--text2);font-size:1rem;font-weight:600;letter-spacing:.05em}
</style>
"""

CHAPTER = {
    "code": "6A2", "range": "6A20–6A2Z", "title": "ŞİZOFRENİYA SPEKTRİ POZUNTULARI",
    "disorders": [
        ("6A20", "ŞİZOFRENİYA"), ("6A21", "ŞİZOAFFEKTİV POZUNTU"),
        ("6A22", "ŞİZOTİPİK POZUNTU"), ("6A23", "KƏSKİN VƏ KEÇİCİ PSİXOTİK POZUNTU"),
        ("6A24", "SAYIQLAMA POZUNTUSU"),
        ("6A25", "İLKİN PSİXOTİK POZUNTULARIN SİMPTOM DOMENLƏRİ"),
    ],
}


def page(content: str, title: str) -> str:
    t = top.replace("MÜNDƏRİCAT | KLİNİK PSİXİATRİYA", f"{title} | KLİNİK PSİXİATRİYA")
    t = t.replace("</head>", EXTRA_CSS + "</head>")
    return t + "\n" + content + "\n" + bottom


def d_nav(idx, ds):
    prev = ds[idx - 1] if idx > 0 else None
    nxt = ds[idx + 1] if idx < len(ds) - 1 else None
    l = f'<a href="{prev[0]}.html">← {prev[0]} {prev[1]}</a>' if prev else "<span></span>"
    r = f'<a href="{nxt[0]}.html">{nxt[0]} {nxt[1]} →</a>' if nxt else "<span></span>"
    up = f'<a class="up" href="{CHAPTER["code"]}-index.html">↑ {CHAPTER["title"]}</a>'
    return f'<nav class="d-nav">{l}{up}{r}</nav>'


ds = CHAPTER["disorders"]
made = []
for idx, (code, name) in enumerate(ds):
    frag_path = MASTER / f"{code}.html"
    if not frag_path.exists():
        continue
    frag = frag_path.read_text(encoding="utf-8")
    nav = d_nav(idx, ds)
    (OUT / f"{code}.html").write_text(page(nav + frag + nav, name), encoding="utf-8")
    made.append(code)

# головная страница главы
links = "".join(
    f'<a class="ch-disorder" href="{c}.html"><span class="ch-code">{c}</span>'
    f'<span class="ch-name">{n}</span></a>' for c, n in ds)
head_html = (f'<h1 class="h-chapter"><span class="icd">{CHAPTER["range"]} · XBT-11</span>'
             f'{CHAPTER["title"]}</h1>'
             f'<p style="text-align:center;color:var(--text2)">Bu fəsildəki pozuntular — hər biri ayrıca səhifə:</p>'
             f'<div class="chapter-menu">{links}</div>')
(OUT / f'{CHAPTER["code"]}-index.html').write_text(page(head_html, CHAPTER["title"]), encoding="utf-8")

print("preview собран в", OUT)
print("страницы расстройств:", made)
print("головная страница главы:", f'{CHAPTER["code"]}-index.html')
