---
name: book-typography-icd11
description: Apply ICD-11 (МКБ-11 РФ 2022) typography style to the Klinik Psixiatriya textbook (DOCX + HTML). Use whenever the user touches book layout, page breaks, title page, headings, chapter formatting, DOCX rebuild, TOC, page headers/footers, or asks about verstka/typography rules. Read TYPOGRAPHY.md and apply its rules without asking the user to repeat them. The reference PDF is at _supplements/ICD-11_RU_2022_reference.pdf — inspect it for style decisions.
---

# Klinik Psixiatriya — ICD-11 Style Typography

## Trigger
Any layout/verstka work on the book: DOCX rebuild, page-break complaints, heading hierarchy, title page, TOC, headers, chapter starts, colours.

## Session-start: term sync
At the very beginning of each session that touches the book, run:
```
python _term_sync.py
```
This pulls APPROVED corrections from the Google Sheet (filled by users via the
'Düzəlt' button on the site) and applies them everywhere. Then rebuild:
```
python _build_abbreviatur.py
python _rebuild_book_nav.py
python build_book.py
```
Record what was applied in PROGRESS.md and HISTORY.json.

## Single source of truth for canonical terms
`klinik-psixiatriya/abbreviatur.html` has a `#cari-terminler` header section
listing ALL canonical AZ terms used on the site. The list lives in
`_build_abbreviatur.py CANONICAL_TERMS` and is rendered into the page header.

**RULE: Any rename of a term MUST update three places at once:**
1. `_supplements/chapters-v2/*.html` (master content)
2. `klinik-psixiatriya/*.html` (rendered book + abbreviatur)
3. `_build_abbreviatur.py CANONICAL_TERMS` list (header)

Otherwise the abbreviatur page header will drift from actual book content.

## Verified disorder name list (canonical)
The 103 disorder names with WHO ICD-11 2024 codes are listed in `TYPOGRAPHY.md` section 0b. Always check against that table before editing any disorder title. Do NOT revert to old forms (e.g. `OPOZİSİONAL DEFİANT POZUNTU` → must remain `MÜXALİF-İNADKAR POZUNTU`).

## Translation rule (per 994 grammar bible, az.md)
- **Keep Latinisms** (medical professional vocabulary): şizofreniya, bipolyar, paranoya, depressiya, katatoniya, narkolepsiya, kleptomaniya, pyromaniya, anorgasmiya, hipersomnia, etc.
- **Do NOT keep English transliterations**: `binge`, `follow-up`, `screening`, `compliance`, `defiant`, `disinhibe`, `premature`, `kültür`. Replace with proper Azerbaijani forms.
- **Check the WHO ICD-11 browser** (https://icd.who.int/browse/2024-01/mms/en) for exact codes — РФ МКБ-11 PDF may be one version behind.
- **Reference 994 project** when unsure: `C:\Users\SAM\Desktop\994\grammar_bibles\az.md` (local) or production server `94.156.35.89` (via jump host `185.203.116.131`).

## ICD-11 code drift (already fixed in v14)
WHO 2024 vs older drafts: 6B40-6B45 were renumbered.
Current (correct): 6B40 PTSD · 6B41 cPTSD · 6B42 Prolonged Grief · 6B43 Adjustment · 6B44 RAD · 6B45 Disinhibited Social.

## HARD COLOUR RULE — black only
All text is `#000000` (pure black). No blue/cyan/Office accent (`#4F81BD`, `#0563C1`, theme colours). The only allowed non-black is **grey `#555555`** for the title-page sub-slogan and year/city.

Enforced in `build_book.py → fix_docx()`:
- Heading 1–9 + `Hyperlink` style: `RGBColor(0, 0, 0)`, no underline on links
- Final sweep over every `<w:color>` element in body + table cells: any value → `000000` (except `555555`)
- Theme colour attributes (`w:themeColor`, `w:themeShade`, `w:themeTint`) stripped

If the user complains about colour anywhere in the book, re-run the build — the sweep should catch it. Never relax this rule.

## Reference source (МКБ-11 РФ 2022)
- Local: `_supplements/ICD-11_RU_2022_reference.pdf` (138×228 mm, 454 pp)
- Online: https://psymos.ru/storage/jofwtsdKUqnRaVriTQPE/PMR8K3dB9lxWw1sFHXBwNY5HEVAHSX5N7tOf2G5T.pdf
- WHO browser: https://icd.who.int/browse/2024-01/mms/ru

## Adaptation logic (ICD-11 → our book)

| Aspect | ICD-11 РФ | Our book | Why |
|---|---|---|---|
| Font | Calibri/Arial sans-serif | Times New Roman serif | "Шрифт наш" — professional medical textbook |
| Page size | 138×228 mm | A4 | Wider audience / printable |
| Title page | Subtitled by edition | Slogan + sub-slogan + author block | Same hierarchy |
| Chapter title | ALL CAPS multi-line centered | Same | Adopted |
| Block code | `БЛОК L1-6A0` under title | `6A00–6A0Z` range | Adapted naming |
| Disorder code | `6A00  Name` (regular case) | `6A00 NAME` (ALL CAPS) | We have full sections, not list — emphasis OK |
| TOC depth | 2 (chapter + sub-chapter) | 2 (chapter + disorder) | Same |
| TOC leader | dot leaders + right page nums | Same (pandoc auto) | Adopted |
| Headers | left=source, right=book | Same | Adopted |
| Body | justified, small ~10pt | TNR 11pt, justified, first-line 0.5cm | Adapted (larger for readability + accessibility) |
| Chapter starts | always on right (odd) page | optional — page-break only | Adapted (Word printing differs from offset) |

## Build pipeline
```bash
# After content changes
python _inject_chapters_v2.py
python _rebuild_book_nav.py
python _fix_terminology3.py      # if terminology needs fixing
python build_book.py             # final DOCX build (pandoc + python-docx)
```

If the output `KLINIK_PSIXIATRIYA_*.docx` is locked by Word, increment the version:
```python
import build_book
build_book.OUT_DOCX = build_book.SITE / "KLINIK_PSIXIATRIYA_8.docx"
build_book.main()
```

## Verification snippet
```python
from docx import Document
from docx.oxml.ns import qn
import re
doc = Document('klinik-psixiatriya/KLINIK_PSIXIATRIYA_8.docx')
ICD = re.compile(r'^\s*([0-9][A-Z][0-9][0-9A-Z]?|HA[0-9]{2})\b')
h1, disorders, intros, subs = 0, 0, 0, 0
for p in doc.element.body.findall(qn('w:p')):
    pPr = p.find(qn('w:pPr'))
    if pPr is None: continue
    s = pPr.find(qn('w:pStyle'))
    if s is None: continue
    sty = s.get(qn('w:val')) or ''
    has_pbb = pPr.find(qn('w:pageBreakBefore')) is not None
    if not has_pbb: continue
    txt = ''.join(t.text or '' for t in p.iter(qn('w:t')))
    if 'Heading 1' in sty: h1 += 1
    elif 'Heading 2' in sty:
        if ICD.match(txt): disorders += 1
        else: intros += 1
    elif any(f'Heading {i}' in sty for i in (3,4,5)): subs += 1
assert intros == 0 and subs == 0
print(f"OK: {h1} chapter breaks, {disorders} disorder breaks")
```

## Design accuracy cases (examples to learn from)

User caught several issues that traced back to bulk-text or double-injection
artifacts. Patterns to watch for:

### Case 1: Double-injected `<abbr>` tags → leaked title text
When `_inject_abbr.py` runs twice, abbr terms that already had wrappers get
re-wrapped — but the title attribute of the OUTER abbr now contains an INNER
abbr's `<` and `>`, breaking the attribute. Browser parses it as text.

Visible result:
```
WHO), 2019, qüvvəyə minmə 2022.">XBT-11 kodu       ← bad
XBT-11 kodu                                          ← fixed (in <th>)
WHO, 2019, qüvvəyə minmə 2022 — XBT-11 kodu         ← fixed (in body)
```

Fix script: `_fix_abbr_leaks.py` — context-aware (in `<th>`: just term;
in body: readable form with em-dash separator).

### Case 2: TOC dot-leader direction
User: *"we read left to right"*. TOC entries were rendered as
`6A00 ......................... NAME`. Fixed by flexbox `order`:
- `.toc-code` order 1, `.toc-dname` order 2 (next to code), `.toc-dot-leader` order 3 (stretches right).

### Case 3: Section names smaller than sub-section names (broken hierarchy)
Chapter title in DOCX appeared as `Body Text` while disorders appeared as
`Heading 2` — chapter LARGER than disorder is the correct hierarchy.

Root cause: `shift_levels()` bug. The function promoted `<h2>` → `<h1>` on
the opening tag but the closing `</h1>` got demoted to `</h2>` by the second
pass (which doesn't know about chapter status because close tags carry no
`data-chapter` attribute). Solution: track `in_chapter_h1` state.

### Case 4: Page header label vs page purpose
User: *"this page should be called Mündəricat, not Önsöz"*. The book's TOC
page (index.html) was labelled "Önsöz" (Foreword) — but it actually shows
the table of contents. Renamed everywhere.

### Case 5: Redundant columns
User wanted columns dropped from abbreviatur:
- 'Rəsmi AZ' on disorders table (Düzəlt workflow covers it)
- 'Русский' on abbreviations table (already in disorders table)

→ implemented as `strip_columns_*_table()` in `_build_abbreviatur.py`.

### Case 6: Modal text invisible (white on white)
The Düzəliş et modal had light-theme background but inherited page's
dark-theme text colour. Solution: modal ALWAYS dark, explicit colour
on every child element.

### General principle
After any bulk-text operation (replace, inject, transform):
1. Inspect ONE rendered example (TH, body, modal, etc.)
2. Don't trust the operation — verify the result visually
3. Add to this list when a new artifact surfaces

## Anti-patterns
- ❌ Pandoc auto title block (4 stacked Title/Subtitle/Author/Date paragraphs)
- ❌ Page-break-before on every Heading 2 (causes 100+ blank pages)
- ❌ Heading 2 bigger than Heading 1
- ❌ Italic/oblique for chapter titles
- ❌ Adding running blank pages "for symmetry" — academic Word DOCX, not offset print
- ❌ Repeating these rules in a chat — they live in TYPOGRAPHY.md

## Files
- Rules: `C:\Users\SAM\Desktop\sayt2\TYPOGRAPHY.md` (read FIRST)
- Reference PDF: `C:\Users\SAM\Desktop\sayt2\_supplements\ICD-11_RU_2022_reference.pdf`
- Build script: `C:\Users\SAM\Desktop\sayt2\build_book.py`
- Project skill copy: `C:\Users\SAM\Desktop\sayt2\.claude\skills\book-typography-icd11\SKILL.md`
- Global skill copy: `C:\Users\SAM\.claude\skills\book-typography-icd11\SKILL.md` (this file)
