"""Rebuild klinik-psixiatriya/abbreviatur.html:
   1. Insert 'Fəsil adları' (chapter names) table at top — 23 chapters.
   2. Add 'Düzəlt' column with edit buttons to all existing tables.
   Buttons are wired to duzelis.js per-term editor (see duzelis.js v2).
"""
from __future__ import annotations
import re
import html
from pathlib import Path

ROOT = Path(__file__).parent
PAGE = ROOT / "klinik-psixiatriya" / "abbreviatur.html"

# 23 chapter names (matches CHAPTER_TITLES from _rebuild_book_nav.py)
CHAPTERS = [
    ("01-6A0-neyroinkisaf.html",         "NEYROİNKİŞAF POZUNTULARI",                "6A00–6A0Z"),
    ("02-6A2-sizofreniya-spektri.html",  "ŞİZOFRENİYA SPEKTRİ POZUNTULAR",          "6A20–6A2Z"),
    ("03-6A4-katatoniya.html",           "KATATONİYA",                              "6A40"),
    ("04-6A6-ehval-pozuntulari.html",    "ƏHVAL POZUNTULARI",                       "6A60–6A7Z"),
    ("05-6B0-narahatliq.html",           "NARAHATLIQ POZUNTULARI",                  "6B00–6B0Z"),
    ("06-6B2-okp.html",                  "OBSESSİV-KOMPULSİV POZUNTULAR",           "6B20–6B2Z"),
    ("07-6B4-stress.html",               "STRESS İLƏ ƏLAQƏLİ POZUNTULAR",           "6B40–6B4Z"),
    ("08-6B6-dissosiativ.html",          "DİSSOSİATİV POZUNTULAR",                  "6B60–6B6Z"),
    ("09-6B8-qida-qebulu.html",          "QİDA QƏBULU POZUNTULARI",                 "6B80–6B8Z"),
    ("10-6C0-ifrazat.html",              "İFRAZAT POZUNTULARI",                     "6C00–6C0Z"),
    ("11-6C2-bedensel-disstres.html",    "BƏDƏN DİSSTRES POZUNTUSU",                "6C20"),
    ("12-6C4-madde-asililiq.html",       "MADDƏ İSTİFADƏSİ POZUNTULARI",            "6C40–6C5Z"),
    ("13-6C7-impuls-nezareti.html",      "İMPULS NƏZARƏTİ POZUNTULARI",             "6C70–6C7Z"),
    ("14-6C9-pozucu-davranis.html",      "POZUCU DAVRANIŞ POZUNTULARI",             "6C90–6C9Z"),
    ("15-6D1-sexsiyyet.html",            "ŞƏXSİYYƏT POZUNTULARI",                   "6D10–6D1Z"),
    ("16-6D3-parafilik.html",            "PARAFİLİK POZUNTULAR",                    "6D30–6D3Z"),
    ("17-6D5-faktitioz.html",            "FAKTİTİOZ POZUNTULAR",                    "6D50–6D5Z"),
    ("18-6D7-neyrokoqnitiv.html",        "NEYROKOQNİTİV POZUNTULAR (DEMENSİYA)",    "6D70–6D8Z"),
    ("19-6E2-perinatal.html",            "PERİNATAL PSİXİ POZUNTULAR",              "6E20–6E2Z"),
    ("20-6E4-psixosomatik.html",         "PSİXOSOMATİK AMİLLƏR",                    "6E40"),
    ("21-6E6-ikincili.html",             "İKİNCİLİ PSİXİ SİNDROMLAR",               "6E60–6E6Z"),
    ("22-7AB-yuxu.html",                 "YUXU POZUNTULARI",                        "7A00–7A8Z"),
    ("23-HA-cinsi-saglamliq.html",       "CİNSİ SAĞLAMLIQ POZUNTULARI",             "HA00–HA0Z"),
]


def edit_btn(term: str, kind: str) -> str:
    """Render an inline edit button. term carried via data-az attribute."""
    safe = html.escape(term, quote=True)
    return (
        f'<button class="dzl-row-btn" type="button" '
        f'data-row-kind="{kind}" data-az="{safe}" '
        f'aria-label="Düzəlt: {safe}">✎ Düzəlt</button>'
    )


def build_chapters_table() -> str:
    rows = []
    rows.append('<h2 id="fesil-adlari">Fəsil Adları</h2>')
    rows.append('<p>Kitabın 23 fəsli — XBT-11 koduna görə düzülmüş. '
                'Hər sətrin yanında <strong>Düzəlt</strong> düyməsinə basaraq '
                'düzgün adı təklif edə bilərsiniz.</p>')
    rows.append('<div class="tbl-wrap"><table>')
    rows.append('<tr><th style="width:90px">Kod</th>'
                '<th>Fəsil adı (cari)</th>'
                '<th style="width:110px">Düzəlt</th></tr>')
    for href, title, code_range in CHAPTERS:
        rows.append(
            f'<tr><td class="kod-cell">{html.escape(code_range)}</td>'
            f'<td><a href="{href}">{html.escape(title)}</a></td>'
            f'<td class="rasmi-cell">{edit_btn(title, "chapter")}</td></tr>'
        )
    rows.append('</table></div>')
    rows.append('<hr>')
    return "\n".join(rows)


def add_edit_column(html_text: str) -> str:
    """For every table after the chapters table, append a 'Düzəlt' column.
       Heuristic: each <table>...</table> block — add an extra <th> at the
       end of the header row, and a <td> with the edit button at the end of
       every data row. Skip tables that already have a `dzl-row-btn`.
    """
    out = []
    pos = 0
    for m in re.finditer(r'<table\b[^>]*>([\s\S]*?)</table>', html_text):
        out.append(html_text[pos:m.start()])
        table = m.group(0)
        if 'dzl-row-btn' in table:
            out.append(table)
            pos = m.end()
            continue
        # Insert <th>Düzəlt</th> at end of FIRST <tr> (header row)
        def header_repl(m_tr):
            inner = m_tr.group(1)
            return f'<tr>{inner}<th style="width:110px">Düzəlt</th></tr>'
        # Match only the FIRST <tr>
        first_tr_re = re.compile(r'<tr>([\s\S]*?)</tr>', re.IGNORECASE)
        m_first = first_tr_re.search(table)
        if not m_first:
            out.append(table); pos = m.end(); continue
        new_table = table[:m_first.start()] + header_repl(m_first) + table[m_first.end():]
        # Now add edit btn to every subsequent <tr>. We use a stateful counter.
        def row_repl(m_tr, _state={'i': 0}):
            _state['i'] += 1
            if _state['i'] == 1:
                return m_tr.group(0)  # header row, already done
            inner = m_tr.group(1)
            # Take text of FIRST <td> as the 'term' identifier
            m_td = re.search(r'<td[^>]*>([\s\S]*?)</td>', inner)
            term_raw = m_td.group(1) if m_td else ''
            # Strip nested <abbr>/<a>/tags
            term_clean = re.sub(r'<[^>]+>', '', term_raw).strip()
            return f'<tr>{inner}<td class="rasmi-cell">{edit_btn(term_clean, "term")}</td></tr>'
        new_table = first_tr_re.sub(row_repl, new_table)
        out.append(new_table)
        pos = m.end()
    out.append(html_text[pos:])
    return "".join(out)


def insert_chapters_table(html_text: str) -> str:
    # Insert chapters table right after the intro <p>...</p> following the H1.
    marker = '<h1 id="terminoloji-lüğət" class="h-section">TERMİNOLOJİ LÜĞƏT</h1>'
    if marker not in html_text:
        print("WARN: H1 marker not found")
        return html_text
    # Find end of first <p> after H1
    after = html_text.index(marker) + len(marker)
    m = re.search(r'</p>', html_text[after:])
    if not m:
        print("WARN: first <p> not found after H1")
        return html_text
    insert_at = after + m.end()
    return html_text[:insert_at] + "\n\n" + build_chapters_table() + "\n" + html_text[insert_at:]


def main():
    text = PAGE.read_text(encoding="utf-8")

    # Strip previously injected chapters table (for idempotent re-run)
    text = re.sub(
        r'<h2 id="fesil-adlari">[\s\S]*?<hr>\s*',
        '', text
    )
    # Strip previously added edit buttons (idempotent)
    text = re.sub(
        r'<th style="width:110px">Düzəlt</th>\s*</tr>',
        '</tr>', text
    )
    text = re.sub(
        r'<td class="rasmi-cell"><button class="dzl-row-btn"[\s\S]*?</button></td>\s*</tr>',
        '</tr>', text
    )

    # Now insert fresh chapters table + edit columns
    text = insert_chapters_table(text)
    text = add_edit_column(text)

    PAGE.write_text(text, encoding="utf-8")
    print(f"OK: rebuilt {PAGE}")


if __name__ == "__main__":
    main()
