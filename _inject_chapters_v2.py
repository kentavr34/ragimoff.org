"""Inject chapters-v2 disorder fragments into klinik-psixiatriya/NN-*.html.

For each chapter HTML file:
  1. Preserve <head>, <header>, sidebar, navigation, <main><div.content-wrap> opening
  2. Preserve chapter intro (everything inside content-wrap BEFORE the first
     <h1 class="h-disorder">)
  3. Replace all disorder bodies with chapters-v2 fragments for ICD codes
     mapped to this chapter
  4. Preserve prev/next pnav and closing tags
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
BOOK = ROOT / "klinik-psixiatriya"
V2 = ROOT / "_supplements" / "chapters-v2"

# Chapter file -> ordered list of v2 ICD codes
CHAPTER_CODES = {
    "01-6A0-neyroinkisaf.html":          ["6A00","6A01","6A02","6A03","6A04","6A05","6A06","6A07"],
    "02-6A2-sizofreniya-spektri.html":   ["6A20","6A21","6A22","6A23","6A24","6A25"],
    "03-6A4-katatoniya.html":            ["6A40"],
    "04-6A6-ehval-pozuntulari.html":     ["6A60","6A61","6A62","6A70","6A71","6A72","6A73"],
    "05-6B0-narahatliq.html":            ["6B00","6B01","6B02","6B03","6B04","6B05","6B06"],
    "06-6B2-okp.html":                   ["6B20","6B21","6B22","6B23","6B24","6B25"],
    "07-6B4-stress.html":                ["6B40","6B41","6B42","6B43","6B44","6B45"],
    "08-6B6-dissosiativ.html":           ["6B60","6B61","6B62","6B63","6B64"],
    "09-6B8-qida-qebulu.html":           ["6B80","6B81","6B82","6B83","6B84","6B85"],
    "10-6C0-ifrazat.html":               ["6C00","6C01"],
    "11-6C2-bedensel-disstres.html":     ["6C20"],
    "12-6C4-madde-asililiq.html":        ["6C40","6C41","6C42","6C43","6C44","6C45","6C46","6C47","6C50"],
    "13-6C7-impuls-nezareti.html":       ["6C70","6C71","6C72","6C73"],
    "14-6C9-pozucu-davranis.html":       ["6C90","6C91"],
    "15-6D1-sexsiyyet.html":             ["6D10","6D11"],
    "16-6D3-parafilik.html":             ["6D30","6D31","6D32","6D33","6D34"],
    "17-6D5-faktitioz.html":             ["6D50","6D51"],
    "18-6D7-neyrokoqnitiv.html":         ["6D70","6D71","6D72","6D80","6D81","6D82","6D83"],
    "19-6E2-perinatal.html":             ["6E20","6E21"],
    "20-6E4-psixosomatik.html":          ["6E40"],
    "21-6E6-ikincili.html":              ["6E60","6E61","6E62"],
    "22-7AB-yuxu.html":                  ["7A00","7A20","7A40","7A60","7A80"],
    "23-HA-cinsi-saglamliq.html":        ["HA00","HA01","HA02","HA03","HA04","HA05"],
}

H_DISORDER_RE = re.compile(r'<h1 [^>]*class="h-disorder"', re.IGNORECASE)
PNAV_RE = re.compile(r'<nav class="pnav"[\s\S]*?</nav>', re.IGNORECASE)
MAIN_OPEN_RE = re.compile(r'<main[^>]*>\s*<div class="content-wrap">', re.IGNORECASE)
MAIN_CLOSE_RE = re.compile(r'(?:</div>\s*</main>|</main>)', re.IGNORECASE)


def load_v2(code: str) -> str:
    p = V2 / f"{code}.html"
    if not p.exists():
        raise FileNotFoundError(p)
    return p.read_text(encoding="utf-8").strip()


def process(chapter_file: str, codes: list[str]) -> tuple[int, int]:
    src_path = BOOK / chapter_file
    src = src_path.read_text(encoding="utf-8")

    m_open = MAIN_OPEN_RE.search(src)
    if not m_open:
        raise RuntimeError(f"{chapter_file}: <main><div.content-wrap> not found")
    m_close = MAIN_CLOSE_RE.search(src, m_open.end())
    if not m_close:
        raise RuntimeError(f"{chapter_file}: </div></main> not found")

    pre  = src[:m_open.end()]
    body = src[m_open.end():m_close.start()]
    post = src[m_close.start():]

    # Chapter intro = body before first h-disorder; if none, keep all body.
    m_first = H_DISORDER_RE.search(body)
    if m_first:
        intro = body[:m_first.start()]
    else:
        # find pnav; intro = body without pnav
        m_pnav = PNAV_RE.search(body)
        intro = body[:m_pnav.start()] if m_pnav else body

    # Preserve trailing pnav if present
    m_pnav = PNAV_RE.search(body)
    pnav = m_pnav.group(0) if m_pnav else ""

    # Assemble new body
    new_body_parts = [intro.rstrip(), "\n"]
    for code in codes:
        frag = load_v2(code)
        # Wrap each disorder in a section for styling/anchoring
        new_body_parts.append(f'\n<section class="disorder" data-icd="{code}">\n')
        new_body_parts.append(frag)
        new_body_parts.append("\n</section>\n")
    if pnav:
        new_body_parts.append("\n" + pnav + "\n    ")

    new_src = pre + "\n      " + "".join(new_body_parts) + post
    src_path.write_text(new_src, encoding="utf-8")
    return len(codes), len(new_src)


def main():
    total_codes = 0
    for ch, codes in CHAPTER_CODES.items():
        n, size = process(ch, codes)
        total_codes += n
        print(f"  {ch:<40s} {n:>2d} disorders   {size//1024:>4d} KB")
    print(f"\nTotal disorders injected: {total_codes}")


if __name__ == "__main__":
    main()
