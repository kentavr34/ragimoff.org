#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build KLINIK_PSIXIATRIYA_6.docx from updated site HTML."""
import re
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).parent.resolve()
SITE = ROOT / "klinik-psixiatriya"
BUILD_DIR = ROOT / "_build"
BUILD_DIR.mkdir(exist_ok=True)

OUT_HTML = BUILD_DIR / "book_combined.html"
OUT_DOCX = SITE / "KLINIK_PSIXIATRIYA_6.docx"
REFERENCE_DOCX = SITE / "KLINIK_PSIXIATRIYA_5.docx"

ORDER = [
    "mugeddime.html",
    "giris-yekun.html",
    "01-6A0-neyroinkisaf.html",
    "02-6A2-sizofreniya-spektri.html",
    "03-6A4-katatoniya.html",
    "04-6A6-ehval-pozuntulari.html",
    "05-6B0-narahatliq.html",
    "06-6B2-okp.html",
    "07-6B4-stress.html",
    "08-6B6-dissosiativ.html",
    "09-6B8-qida-qebulu.html",
    "10-6C0-ifrazat.html",
    "11-6C2-bedensel-disstres.html",
    "12-6C4-madde-asililiq.html",
    "13-6C7-impuls-nezareti.html",
    "14-6C9-pozucu-davranis.html",
    "15-6D1-sexsiyyet.html",
    "16-6D3-parafilik.html",
    "17-6D5-faktitioz.html",
    "18-6D7-neyrokoqnitiv.html",
    "19-6E2-perinatal.html",
    "20-6E4-psixosomatik.html",
    "21-6E6-ikincili.html",
    "22-7AB-yuxu.html",
    "23-HA-cinsi-saglamliq.html",
    "elave-acde.html",
    "elave-skalalar.html",
    "yekun.html",
]

MAIN_RE = re.compile(r'<main\b[^>]*>(.*?)</main>', re.DOTALL | re.IGNORECASE)
SUPP_MARKER_RE = re.compile(r'<!--\s*/?BOOK-SUPPLEMENT:[^>]*-->', re.IGNORECASE)


def extract_main(html: str) -> str:
    m = MAIN_RE.search(html)
    if not m:
        return ""
    body = m.group(1)
    body = SUPP_MARKER_RE.sub("", body)
    body = re.sub(r'<aside\b.*?</aside>', '', body, flags=re.DOTALL | re.IGNORECASE)
    body = re.sub(r'<script\b.*?</script>', '', body, flags=re.DOTALL | re.IGNORECASE)
    body = re.sub(r'<style\b.*?</style>', '', body, flags=re.DOTALL | re.IGNORECASE)
    # Strip nav blocks (page-nav at the bottom, breadcrumbs, etc.)
    body = re.sub(r'<nav\b.*?</nav>', '', body, flags=re.DOTALL | re.IGNORECASE)
    return body.strip()


def strip_links(html: str) -> str:
    """Convert <a href="...">text</a> → text (book has no clickable links)."""
    # Strip ALL <a> wrappers, keep inner text
    html = re.sub(r'<a\b[^>]*>(.*?)</a>', r'\1', html, flags=re.DOTALL | re.IGNORECASE)
    return html


def strip_inline_bold(html: str) -> str:
    """Remove <strong>/<b> inside paragraphs and list items (AI-style label markers).
    Preserve bold inside table cells (<th>/<td>)."""
    # Process paragraphs and li only, leaving table cells intact.
    def strip_in(tag, text):
        pattern = re.compile(rf'(<{tag}\b[^>]*>)(.*?)(</{tag}>)', re.DOTALL | re.IGNORECASE)
        def repl(m):
            inner = m.group(2)
            inner = re.sub(r'</?(?:strong|b)\b[^>]*>', '', inner, flags=re.IGNORECASE)
            return m.group(1) + inner + m.group(3)
        return pattern.sub(repl, text)

    for tag in ('p', 'li', 'em'):
        html = strip_in(tag, html)
    return html


def shift_levels(html: str) -> str:
    """Chapter h2 → h1; everything else demoted 1 level."""
    def chapter_to_h1(m):
        attrs = m.group(1)
        if 'data-chapter' not in attrs:
            attrs += ' data-chapter="1"'
        return f'<h1{attrs}>{m.group(2)}</h1>'
    html2, n = re.subn(r'<h2([^>]*)>(.*?)</h2>', chapter_to_h1, html, count=1, flags=re.DOTALL)
    if n == 0:
        return html

    out = []
    i = 0
    pat = re.compile(r'<(/?)h([1-5])(\b[^>]*)>', re.IGNORECASE)
    for m in pat.finditer(html2):
        out.append(html2[i:m.start()])
        slash, lvl, attrs = m.group(1), int(m.group(2)), m.group(3)
        if lvl == 1 and 'data-chapter' in attrs:
            out.append(f'<{slash}h1{attrs}>')
        else:
            new_lvl = min(lvl + 1, 6)
            out.append(f'<{slash}h{new_lvl}{attrs}>')
        i = m.end()
    out.append(html2[i:])
    return "".join(out)


def split_yekun_signature(html: str) -> str:
    """Insert a page-break marker before the author's closing signature in yekun."""
    # Find the closing block (Kitabın məqsədi → signature)
    marker = '<p><strong>Kitabın məqsədi:</strong>'
    if marker in html:
        # Replace preceding <hr> with page-break div, drop <hr>
        html = re.sub(r'<hr\s*/?>\s*' + re.escape(marker),
                      '<div class="pagebreak-before"></div>' + marker,
                      html, flags=re.IGNORECASE)
    return html


def build_title_page() -> str:
    """No HTML title page — pandoc generates one from metadata (Title style,
    not Heading 1, so it stays out of the TOC)."""
    return ""


def main():
    print("Extracting content...")
    parts = [build_title_page()]
    for fn in ORDER:
        path = SITE / fn
        if not path.exists():
            print(f"  SKIP missing: {fn}")
            continue
        html = path.read_text(encoding="utf-8")
        body = extract_main(html)
        if not body:
            continue
        is_chapter = re.match(r'^\d{2}-', fn) is not None
        if is_chapter:
            body = shift_levels(body)
        if fn == "yekun.html":
            body = split_yekun_signature(body)
        body = strip_links(body)
        body = strip_inline_bold(body)
        parts.append(f"<!-- ===== {fn} ===== -->\n{body}\n")
        print(f"  OK {fn}")

    combined = "\n".join(parts)
    full = (
        "<!DOCTYPE html>\n<html lang='az'><head><meta charset='utf-8'>"
        "<title>Klinik Psixiatriya</title></head><body>\n"
        + combined +
        "\n</body></html>"
    )
    OUT_HTML.write_text(full, encoding="utf-8")
    print(f"\nCombined HTML: {OUT_HTML} ({len(full):,} chars)")

    print("\nRunning pandoc...")
    import pypandoc
    extra_args = [
        f"--reference-doc={REFERENCE_DOCX}",
        "--toc",
        "--toc-depth=2",
        "--metadata=toc-title:MÜNDƏRİCAT",
        "--metadata=title:KLİNİK PSİXİATRİYA",
        "--metadata=subtitle:XBT-11 və DSM-5-TR əsasında klinik bələdçi",
        "--metadata=author:Dr. Kənan Rəhimov",
        "--metadata=date:Bakı — 2026",
        "--standalone",
    ]
    pypandoc.convert_file(
        str(OUT_HTML),
        "docx",
        outputfile=str(OUT_DOCX),
        extra_args=extra_args,
        format="html",
    )
    print(f"DOCX: {OUT_DOCX}")

    print("\nPost-processing DOCX...")
    fix_docx(OUT_DOCX)
    print(f"\nDONE: {OUT_DOCX}")
    print(f"Size: {OUT_DOCX.stat().st_size / 1024:.0f} KB")


def fix_docx(path: Path):
    from docx import Document
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement

    doc = Document(str(path))

    # ── 1. Force-clear first-line indent in EVERY table cell paragraph ──
    def kill_indent(par):
        pPr = par._p.get_or_add_pPr()
        ind = pPr.find(qn('w:ind'))
        if ind is None:
            ind = OxmlElement('w:ind')
            pPr.append(ind)
        # Explicit zero overrides style inheritance.
        ind.set(qn('w:firstLine'), '0')
        ind.set(qn('w:left'), '0')
        ind.set(qn('w:start'), '0')
        # Remove any opposing attributes
        for attr in ('w:hanging', 'w:firstLineChars', 'w:leftChars', 'w:startChars'):
            if ind.get(qn(attr)):
                del ind.attrib[qn(attr)]

    def set_cell_border(cell):
        tc_pr = cell._tc.get_or_add_tcPr()
        tcBorders = tc_pr.find(qn('w:tcBorders'))
        if tcBorders is None:
            tcBorders = OxmlElement('w:tcBorders')
            tc_pr.append(tcBorders)
        for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
            b = tcBorders.find(qn(f'w:{edge}'))
            if b is None:
                b = OxmlElement(f'w:{edge}')
                tcBorders.append(b)
            b.set(qn('w:val'), 'single')
            b.set(qn('w:sz'), '4')
            b.set(qn('w:color'), '666666')

    for tbl in doc.tables:
        tbl.autofit = True
        for row in tbl.rows:
            for cell in row.cells:
                set_cell_border(cell)
                for par in cell.paragraphs:
                    kill_indent(par)
                    # Also clear pStyle indent inheritance via direct override
                    for child in par._p.iter():
                        if child.tag.endswith('}pStyle'):
                            # Leave pStyle but our w:ind override above wins
                            pass

    # ── 2. Page break before each Heading 1 and Heading 2 ──
    HEADING_STYLES = {'Heading1', 'Heading 1', 'Heading2', 'Heading 2',
                      'heading 1', 'heading 2'}
    body = doc.element.body
    paragraphs = body.findall(qn('w:p'))
    for p in paragraphs:
        pPr = p.find(qn('w:pPr'))
        if pPr is None:
            continue
        pStyle = pPr.find(qn('w:pStyle'))
        if pStyle is None:
            continue
        sty = pStyle.get(qn('w:val')) or ''
        if sty in HEADING_STYLES:
            # Add page-break-before via pageBreakBefore element
            pbb = pPr.find(qn('w:pageBreakBefore'))
            if pbb is None:
                pbb = OxmlElement('w:pageBreakBefore')
                # Insert near top of pPr
                pPr.insert(0, pbb)

    # ── 3. Remove first heading's page break (avoids blank first page) ──
    for p in paragraphs:
        pPr = p.find(qn('w:pPr'))
        if pPr is None:
            continue
        pStyle = pPr.find(qn('w:pStyle'))
        if pStyle is None:
            continue
        sty = pStyle.get(qn('w:val')) or ''
        if sty in HEADING_STYLES:
            pbb = pPr.find(qn('w:pageBreakBefore'))
            if pbb is not None:
                pPr.remove(pbb)
            break  # only first heading

    # ── 4. Yekun signature page break: paragraph containing "Kitabın məqsədi" ──
    for p in paragraphs:
        text = "".join(t.text or "" for t in p.iter(qn('w:t')))
        if text.startswith("Kitabın məqsədi:"):
            pPr = p.find(qn('w:pPr'))
            if pPr is None:
                pPr = OxmlElement('w:pPr')
                p.insert(0, pPr)
            if pPr.find(qn('w:pageBreakBefore')) is None:
                pbb = OxmlElement('w:pageBreakBefore')
                pPr.insert(0, pbb)
            break

    doc.save(str(path))


if __name__ == "__main__":
    main()
