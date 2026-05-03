#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Builds search-index.json for full-text search across all bolme-*.html files.
Each entry: {page, id, title, codes, text, sub}
  page  — bolme-01, bolme-02, etc.
  id    — anchor id
  title — heading text
  codes — ICD/DSM codes from xbt-lines (searchable)
  text  — first 300 chars of paragraph text after heading
  sub   — chapter subtitle shown in results
"""
import sys, io, os, glob, json, re, unicodedata

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r"C:\Users\SAM\Desktop\sayt2\klinik-psixiatriya"

def strip_tags(s):
    return re.sub(r'<[^>]+>', ' ', s)

def clean(s):
    s = strip_tags(s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def extract_section_entries(fname, html, chapter_sub):
    """Split HTML into sections by headings and extract content for each."""
    entries = []

    # Split into blocks at each heading with an id
    # We'll process line by line
    heading_pat = re.compile(
        r'<h([123])\s[^>]*id="([^"]+)"[^>]*>(.*?)</h\1>', re.DOTALL | re.IGNORECASE
    )

    # Find all headings with positions
    headings = [(m.start(), int(m.group(1)), m.group(2), clean(m.group(3)))
                for m in heading_pat.finditer(html)]

    page = fname.replace('.html', '')

    for i, (pos, level, hid, title) in enumerate(headings):
        # Skip navigation/header sections
        if not hid or any(x in hid for x in ['mündəricat', 'nav', 'footnote']):
            continue

        # Get the block of HTML between this heading and the next
        end = headings[i+1][0] if i+1 < len(headings) else len(html)
        block = html[pos:end]

        # Extract XBT/classification codes text
        xbt_lines = re.findall(r'class="xbt-line"[^>]*>(.*?)</div>', block, re.DOTALL)
        codes = ' | '.join(clean(x)[:120] for x in xbt_lines[:6] if clean(x))

        # Also extract bare ICD codes (span.icd content)
        icd_codes = re.findall(r'class="icd">([^<]+)<', block)
        # Filter to just code-like strings (not too long)
        icd_codes = [c.strip() for c in icd_codes if len(c.strip()) <= 12]
        icd_str = ' '.join(sorted(set(icd_codes)))

        # Extract paragraph and list text (first meaningful content)
        para_texts = re.findall(
            r'<(?:p|li)(?:\s[^>]*)?>(?!<)(.*?)</(?:p|li)>', block, re.DOTALL
        )
        text_parts = []
        for pt in para_texts[:8]:
            t = clean(pt)
            if len(t) > 20 and not t.startswith('XBT-') and not t.startswith('DSM-'):
                text_parts.append(t)
            if sum(len(x) for x in text_parts) > 350:
                break
        text = ' '.join(text_parts)[:400]

        # Build searchable blob (not shown, just searched)
        searchable = f"{title} {codes} {icd_str} {text}"

        entries.append({
            'page': page,
            'id': hid,
            'title': title[:100],
            'codes': codes[:300],
            'icd': icd_str[:200],
            'text': text[:400],
            'sub': chapter_sub,
        })

    return entries

# Chapter subtitles for search results display
CHAPTER_SUBS = {
    'bolme-01': 'Bölmə 1 — Neyroinkişaf pozuntuları',
    'bolme-02': 'Bölmə 2 — Şizofreniya spektri',
    'bolme-03': 'Bölmə 3 — Katatoniya',
    'bolme-04': 'Bölmə 4 — Əhval pozuntuları',
    'bolme-05': 'Bölmə 5 — Təşviş pozuntuları',
    'bolme-06': 'Bölmə 6 — Obsessiv-kompulsiv',
    'bolme-07': 'Bölmə 7 — Stress əlaqəli',
    'bolme-08': 'Bölmə 8 — Dissosiativ',
    'bolme-09': 'Bölmə 9 — Yemə pozuntuları',
    'bolme-10': 'Bölmə 10 — İfrazat pozuntuları',
    'bolme-11': 'Bölmə 11 — Bədənsel disstres',
    'bolme-12': 'Bölmə 12 — Maddə istifadəsi',
    'bolme-13': 'Bölmə 13 — İmpuls nəzarəti',
    'bolme-14': 'Bölmə 14 — Pozucu davranış',
    'bolme-15': 'Bölmə 15 — Şəxsiyyət pozuntuları',
    'bolme-16': 'Bölmə 16 — Parafilik pozuntular',
    'bolme-17': 'Bölmə 17 — Süni pozuntular',
    'bolme-18': 'Bölmə 18 — Yuxu-oyaqlıq',
    'bolme-19': 'Bölmə 19 — Cinsi sağlamlıq',
    'bolme-20': 'Bölmə 20 — Neyrokoqnitiv',
    'bolme-21': 'Bölmə 21 — Hamiləlik dövrü',
    'bolme-22': 'Bölmə 22–23 — İkincili pozuntular',
    'bolme-ps': 'Psixosomatik',
}

all_entries = []

for fpath in sorted(glob.glob(os.path.join(BASE, 'bolme-*.html'))):
    fname = os.path.basename(fpath)
    page = fname.replace('.html', '')
    sub = CHAPTER_SUBS.get(page, page)

    with open(fpath, encoding='utf-8') as f:
        html = f.read()
    html = unicodedata.normalize('NFC', html)

    entries = extract_section_entries(fname, html, sub)
    all_entries.extend(entries)
    print(f'  {fname}: {len(entries)} entries')

# Write JSON
out_path = os.path.join(BASE, 'search-index.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(all_entries, f, ensure_ascii=False, separators=(',', ':'))

size_kb = os.path.getsize(out_path) // 1024
print(f'\nTotal: {len(all_entries)} entries → search-index.json ({size_kb} KB)')
