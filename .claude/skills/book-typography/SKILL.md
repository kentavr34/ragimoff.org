---
name: book-typography
description: Apply Klinik Psixiatriya textbook typography rules (DOCX + HTML). Use whenever the user touches book layout, page breaks, title page, heading hierarchy, chapter formatting, DOCX rebuild, or asks about verstka/typography rules. Read TYPOGRAPHY.md and apply its rules without asking the user to repeat them.
---

# Klinik Psixiatriya — Book Typography Skill

## Trigger
Any layout/verstka work on the book — DOCX rebuild, page-break complaints, heading hierarchy fixes, title page issues, blank pages.

## Read first
- `C:\Users\SAM\Desktop\sayt2\TYPOGRAPHY.md` — full rules, do not ignore
- `C:\Users\SAM\Desktop\sayt2\CLAUDE.md` — global agent brief

## Mental model
Two layers control book layout:
1. **HTML chapters** (`klinik-psixiatriya/*.html`) — semantic structure (`<section class="disorder">`, `<h1 class="h-disorder">`, etc.)
2. **DOCX build** (`build_book.py`) — pandoc converts HTML → DOCX, then `fix_docx()` post-processes via python-docx

## Hard rules (from TYPOGRAPHY.md)

### Title page
ONE page only:
- Top, centered: `KLİNİK PSİXİATRİYA` (44pt, bold)
- Below: `Diaqnostika və terapiya standartları` (18pt, italic)
- Below: `XBT-11 və DSM-5-TR əsasında klinik bələdçi` (14pt, italic, grey)
- Big vertical gap
- Bottom, centered: `Dr. Kənan Rəhimov` (14pt, bold) + `Bakı · 2026` (12pt, grey)
- Page break, then TOC starts on its own page

Do **NOT** use pandoc's auto title block (Title + Subtitle + Author + Date as separate stacked paragraphs). Build the title page manually in `build_title_page_xml()`.

### Heading hierarchy
| Level | Size | Weight | Align | Used for |
|---|---|---|---|---|
| Heading 1 | 28pt | Bold | Center | Chapter name (e.g. NEYROİNKİŞAF POZUNTULARI) |
| Heading 2 | 20pt | Bold | Left | Disorder title with ICD code (6A00 …) |
| Heading 3 | 14pt | Bold | Left | Disorder section (1. Tərif, 2. Tarixçə …) |
| Heading 4 | 12pt | Bold | Left | Subsection (6.1, 6.2 …) |
| Heading 5 | 11pt | Bold | Left | Myth N: "…" |

Never let a sub-heading appear larger or bolder than its parent.

### Page-break-before
Allowed on:
- **Heading 1** (every chapter starts on new page)
- **Heading 2 whose text starts with an ICD-code pattern** (matched by `^([0-9][A-Z][0-9][0-9A-Z]?|HA[0-9]{2})\b`) — i.e. disorder titles only

Never on:
- Chapter-intro Heading 2 (Bu bölmənin tərkibi, Konseptual yenilik)
- Heading 3, 4, 5 (sub-sections, sub-sub-sections, myths)
- Tables, paragraphs

First heading's page break is always stripped (no blank leading page).

### TOC
`--toc --toc-depth=2 --metadata=toc-title:MÜNDƏRİCAT`. Pandoc-generated. No deeper levels.

### Terminology
See TYPOGRAPHY.md §6. Use `_fix_terminology3.py` to enforce.

## Build pipeline
```bash
# 1. (if you touched chapter content)
python _inject_chapters_v2.py
python _rebuild_book_nav.py

# 2. (clean terminology if needed)
python _fix_terminology3.py

# 3. (always last)
python build_book.py
```

`build_book.py` outputs to `klinik-psixiatriya/KLINIK_PSIXIATRIYA_6.docx` by default. If the file is locked by Word, override:
```python
import build_book
build_book.OUT_DOCX = build_book.SITE / "KLINIK_PSIXIATRIYA_7.docx"
build_book.main()
```

## Verification
After build, run a sanity check:
```python
from docx import Document
from docx.oxml.ns import qn
import re
doc = Document('klinik-psixiatriya/KLINIK_PSIXIATRIYA_7.docx')
ICD = re.compile(r'^\s*([0-9][A-Z][0-9][0-9A-Z]?|HA[0-9]{2})\b')
h1_pbb, h2_pbb_icd, h2_pbb_intro, h3plus_pbb = 0, 0, 0, 0
for p in doc.element.body.findall(qn('w:p')):
    pPr = p.find(qn('w:pPr'))
    if pPr is None: continue
    sty_el = pPr.find(qn('w:pStyle'))
    if sty_el is None: continue
    sty = sty_el.get(qn('w:val')) or ''
    if pPr.find(qn('w:pageBreakBefore')) is None: continue
    txt = ''.join(t.text or '' for t in p.iter(qn('w:t')))
    if '1' in sty and 'Heading' in sty: h1_pbb += 1
    elif '2' in sty and 'Heading' in sty:
        if ICD.match(txt): h2_pbb_icd += 1
        else: h2_pbb_intro += 1
    elif any(f'Heading{i}' in sty or f'Heading {i}' in sty for i in (3,4,5)):
        h3plus_pbb += 1
assert h2_pbb_intro == 0, f"non-ICD H2 has page break: {h2_pbb_intro}"
assert h3plus_pbb == 0, f"sub-section has page break: {h3plus_pbb}"
print(f"OK: H1 pbb={h1_pbb}, disorder H2 pbb={h2_pbb_icd}")
```

If `h2_pbb_intro > 0` or `h3plus_pbb > 0`, the post-processing logic in `build_book.fix_docx()` regressed — re-check the ICD regex and the SUB_HEADINGS set.

## Anti-patterns (what NOT to do)
- ❌ Page break before every h2 (causes 100+ blank pages)
- ❌ Pandoc auto title block (puts title/subtitle/author each on own line, no bottom alignment)
- ❌ Heading 1 smaller than Heading 2 (inverted hierarchy)
- ❌ Sub-section heading bold + huge — looks like a chapter
- ❌ Asking the user to re-explain rules — read TYPOGRAPHY.md
