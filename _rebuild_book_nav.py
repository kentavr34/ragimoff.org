"""Rebuild sidebar navigation and book index.html TOC from injected v2 chapters.

Matches the existing <aside class="sidebar"> structure:
  <aside class="sidebar" id="sb">
    <div class="sb-hdr">…</div>
    <nav>
      <div class="nav-item" data-slug="…">…</div>
      <div class="nav-item nav-has-sub" data-slug="…">
        <a class="nav-link is-bolme">…</a>
        <button class="nav-toggle">▶</button>
        <div class="nav-sub">
          <a class="nav-sub-link">…</a>
          …
        </div>
      </div>
      …
    </nav>
  </aside>
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).parent / "klinik-psixiatriya"

CHAPTER_TITLES = {
    "01-6A0-neyroinkisaf.html":          ("NEYROİNKİŞAF POZUNTULARI",        "6A00–6A0Z"),
    "02-6A2-sizofreniya-spektri.html":   ("ŞİZOFRENİYA SPEKTRİ",             "6A20–6A2Z"),
    "03-6A4-katatoniya.html":            ("KATATONİYA",                       "6A40"),
    "04-6A6-ehval-pozuntulari.html":     ("ƏHVAL POZUNTULARI",               "6A60–6A7Z"),
    "05-6B0-narahatliq.html":            ("NARAHATLIQ POZUNTULARI",          "6B00–6B0Z"),
    "06-6B2-okp.html":                   ("OBSESSİV-KOMPULSİV (OKP)",        "6B20–6B2Z"),
    "07-6B4-stress.html":                ("STRESS İLƏ ƏLAQƏLİ",              "6B40–6B4Z"),
    "08-6B6-dissosiativ.html":           ("DİSSOSİATİV POZUNTULAR",          "6B60–6B6Z"),
    "09-6B8-qida-qebulu.html":           ("QİDA QƏBULU POZUNTULARI",         "6B80–6B8Z"),
    "10-6C0-ifrazat.html":               ("İFRAZAT POZUNTULARI",             "6C00–6C0Z"),
    "11-6C2-bedensel-disstres.html":     ("BƏDƏNSƏL DİSTRES",                "6C20"),
    "12-6C4-madde-asililiq.html":        ("MADDƏ İLƏ ƏLAQƏLİ",               "6C40–6C5Z"),
    "13-6C7-impuls-nezareti.html":       ("İMPULS NƏZARƏTİ",                 "6C70–6C7Z"),
    "14-6C9-pozucu-davranis.html":       ("POZUCU DAVRANIŞ",                 "6C90–6C9Z"),
    "15-6D1-sexsiyyet.html":             ("ŞƏXSİYYƏT POZUNTULARI",           "6D10–6D1Z"),
    "16-6D3-parafilik.html":             ("PARAFİLİK POZUNTULAR",            "6D30–6D3Z"),
    "17-6D5-faktitioz.html":             ("FAKTİTİOZ POZUNTULAR",            "6D50–6D5Z"),
    "18-6D7-neyrokoqnitiv.html":         ("NEYROKOQNİTİV (DEMENSİYA)",       "6D70–6D8Z"),
    "19-6E2-perinatal.html":             ("PERİNATAL POZUNTULAR",            "6E20–6E2Z"),
    "20-6E4-psixosomatik.html":          ("PSİXOSOMATİK FAKTORLAR",          "6E40"),
    "21-6E6-ikincili.html":              ("İKİNCİLİ PSİXİATRİYA",            "6E60–6E6Z"),
    "22-7AB-yuxu.html":                  ("YUXU POZUNTULARI",                "7A00–7A8Z"),
    "23-HA-cinsi-saglamliq.html":        ("CİNSİ SAĞLAMLIQ",                 "HA00–HA0Z"),
}

H1_RE = re.compile(
    r'<h1 id="([^"]+)" class="h-disorder"[^>]*>'
    r'\s*<span class="icd">([0-9A-Z]+)</span>\s*([^<]+?)\s*</h1>',
    re.IGNORECASE,
)


def extract_disorders(ch: str):
    d = (ROOT / ch).read_text(encoding="utf-8")
    return [(m.group(1), m.group(2), m.group(3).strip()) for m in H1_RE.finditer(d)]


def slug(path: str) -> str:
    return path.replace(".html", "")


def build_aside(active_slug: str | None = None) -> str:
    parts = ['<aside class="sidebar" id="sb">']
    parts.append('    <div class="sb-hdr"><h3>📋 Mündəricat</h3>'
                 '<button class="sb-close" onclick="toggleSb()" aria-label="Bağla">✕</button></div>')
    parts.append('    <nav>')

    # Top static links — reorganized 2026-05-14 per user's TOC vision:
    # giris-yekun.html was merged into mugeddime.html; melumat.html added at end.
    for ch, label in [
        ("index.html",        "Mündəricat"),
        ("mugeddime.html",    "Müqəddimə"),
        ("abbreviatur.html",  "Qısaltmalar"),
    ]:
        s = slug(ch)
        active = " is-active" if s == active_slug else ""
        parts.append(f'<div class="nav-item" data-slug="{s}">')
        parts.append(f'  <a href="{ch}" class="nav-link{active}" data-slug="{s}"><span>{label}</span></a>')
        parts.append('</div>')

    # Chapters
    for ch, (title, code_range) in CHAPTER_TITLES.items():
        s = slug(ch)
        disorders = extract_disorders(ch)
        active = " is-active" if s == active_slug else ""
        parts.append(f'<div class="nav-item nav-has-sub" data-slug="{s}">')
        parts.append(f'  <a href="{ch}" class="nav-link is-bolme{active}" data-slug="{s}">')
        parts.append(f'    <span class="nav-code">{code_range}</span>')
        parts.append(f'    <span>{title}</span>')
        parts.append('  </a>')
        parts.append('  <button class="nav-toggle" aria-label="Aç/bağla" onclick="toggleSub(this)" tabindex="-1">▶</button>')
        parts.append('  <div class="nav-sub">')
        for anchor, code, name in disorders:
            parts.append(f'    <a href="{ch}#{anchor}" class="nav-sub-link">'
                         f'<span class="sub-code">{code}</span>'
                         f'<span class="sub-name">{name}</span></a>')
        parts.append('  </div>')
        parts.append('</div>')

    # Appendix: terminology, psychopathology, clinical interview, legal-ethics
    parts.append('<div class="nav-item" data-slug="melumat">')
    parts.append('  <a href="melumat.html" class="nav-link" data-slug="melumat"><span>Məlumat bölməsi</span></a>')
    parts.append('</div>')

    parts.append('    </nav>')
    parts.append('  </aside>')
    return "\n".join(parts)


ASIDE_RE = re.compile(r'<aside class="sidebar"[\s\S]*?</aside>', re.IGNORECASE)


def rewrite_sidebars():
    base_pages = [
        "index.html", "mugeddime.html", "abbreviatur.html",
        "melumat.html",
        # legacy redirect (still gets sidebar so it stays consistent if visited)
        "giris-yekun.html",
    ]
    pages = list(CHAPTER_TITLES.keys()) + base_pages
    count = 0
    for ch in pages:
        path = ROOT / ch
        if not path.exists():
            continue
        d = path.read_text(encoding="utf-8")
        if not ASIDE_RE.search(d):
            print(f"  skip (no sidebar): {ch}")
            continue
        new_aside = build_aside(active_slug=slug(ch))
        new_d = ASIDE_RE.sub(new_aside, d, count=1)
        path.write_text(new_d, encoding="utf-8")
        count += 1
    print(f"Sidebars rewritten in {count} pages")


def build_index_toc() -> str:
    parts = ['<section class="book-toc">']
    parts.append('  <h2 class="toc-title">MÜNDƏRİCAT</h2>')
    for i, (ch, (title, code_range)) in enumerate(CHAPTER_TITLES.items(), start=1):
        disorders = extract_disorders(ch)
        parts.append('  <div class="toc-chapter">')
        parts.append(f'    <a href="{ch}" class="toc-chapter-title">'
                     f'<span class="toc-num">FƏSİL {i:02d}</span>'
                     f'<span class="toc-name">{title}</span>'
                     f'<span class="toc-range">{code_range}</span></a>')
        if disorders:
            parts.append('    <ul class="toc-disorders">')
            for anchor, code, name in disorders:
                parts.append(f'      <li><a href="{ch}#{anchor}">'
                             f'<span class="toc-code">{code}</span>'
                             f'<span class="toc-dot-leader"></span>'
                             f'<span class="toc-dname">{name}</span></a></li>')
            parts.append('    </ul>')
        parts.append('  </div>')
    parts.append('</section>')
    return "\n".join(parts)


TOC_MARKER_RE = re.compile(
    r'<!--\s*BOOK-TOC:START\s*-->[\s\S]*?<!--\s*BOOK-TOC:END\s*-->',
    re.IGNORECASE,
)


def rewrite_index_toc():
    path = ROOT / "index.html"
    d = path.read_text(encoding="utf-8")
    toc = build_index_toc()
    block = f'<!-- BOOK-TOC:START -->\n      {toc}\n      <!-- BOOK-TOC:END -->'
    if TOC_MARKER_RE.search(d):
        new_d = TOC_MARKER_RE.sub(block, d)
    else:
        # Find content-wrap and inject TOC at the end of it
        m = re.search(r'</main>', d)
        if not m:
            print("WARN: cannot find </main> in index.html")
            return
        # Look for existing book-toc block and replace; otherwise insert before </main>
        existing = re.search(r'<section class="book-toc">[\s\S]*?</section>', d)
        if existing:
            new_d = d[:existing.start()] + block + d[existing.end():]
        else:
            new_d = d[:m.start()] + block + "\n  " + d[m.start():]
    path.write_text(new_d, encoding="utf-8")
    print("index.html TOC rewritten")


if __name__ == "__main__":
    n = sum(len(extract_disorders(ch)) for ch in CHAPTER_TITLES)
    print(f"Found {n} disorders across {len(CHAPTER_TITLES)} chapters\n")
    rewrite_sidebars()
    print()
    rewrite_index_toc()
