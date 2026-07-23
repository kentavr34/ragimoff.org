#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build search-index.json for each language copy of the book
(klinik-psixiatriya/{en,ru,tr}/) and point their search JS at the
language-local index. Extraction logic mirrors fix_search_and_seo.py STEP 1."""
import glob, html as htmllib, json, os, re, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, 'klinik-psixiatriya')
LANGS = ['en', 'ru', 'tr']

def nfc(s): return unicodedata.normalize('NFC', s)
def strip_tags(s):
    s = re.sub(r'<[^>]+>', ' ', s)
    s = htmllib.unescape(s)
    return re.sub(r'\s+', ' ', s).strip()

def extract_entries(slug, html, sub):
    entries = []
    content = re.sub(r'<(script|style|nav|header|aside)[^>]*>.*?</\1>', ' ', html, flags=re.DOTALL | re.I)
    heading_pat = re.compile(r'<h([123])\s[^>]*id="([^"]+)"[^>]*>(.*?)</h\1>', re.DOTALL | re.IGNORECASE)
    headings = [(m.start(), int(m.group(1)), m.group(2), strip_tags(m.group(3)))
                for m in heading_pat.finditer(content)]
    for i, (pos, level, hid, title) in enumerate(headings):
        if not hid or any(x in hid for x in ['nav', 'footnote', 'footer']):
            continue
        if len(title) < 2:
            continue
        end = headings[i + 1][0] if i + 1 < len(headings) else pos + 800
        block = content[pos:end]
        xbt_lines = re.findall(r'class="xbt-line"[^>]*>(.*?)</div>', block, re.DOTALL)
        codes = ' | '.join(strip_tags(x)[:120] for x in xbt_lines[:6] if strip_tags(x))
        icd_codes = re.findall(r'class="icd">([^<]+)<', block)
        icd_str = ' '.join(sorted(set(c.strip() for c in icd_codes if len(c.strip()) <= 12)))
        para_texts = re.findall(r'<(?:p|li)(?:\s[^>]*)?>(?!<)(.*?)</(?:p|li)>', block, re.DOTALL)
        text_parts = []
        for pt in para_texts[:8]:
            t = strip_tags(pt)
            if len(t) > 20 and not t.startswith('XBT-') and not t.startswith('DSM-') and not t.startswith('ICD-'):
                text_parts.append(t)
            if sum(len(x) for x in text_parts) > 350:
                break
        text = ' '.join(text_parts)[:400]
        entries.append({'page': slug, 'id': hid, 'title': title[:100],
                        'codes': codes[:300], 'icd': icd_str[:200],
                        'text': text[:400], 'sub': sub})
    return entries

def page_sub(html, slug):
    m = re.search(r'<title>([^<]+)</title>', html, re.I)
    if m:
        return strip_tags(m.group(1)).split('|')[0].strip()[:60] or slug
    return slug

for lang in LANGS:
    d = os.path.join(BOOK, lang)
    if not os.path.isdir(d):
        print(f'[{lang}] dir missing, skip'); continue
    all_entries = []
    n_fixed = 0
    for fpath in sorted(glob.glob(os.path.join(d, '*.html'))):
        slug = os.path.basename(fpath)[:-5]
        with open(fpath, encoding='utf-8') as f:
            html = nfc(f.read())
        all_entries.extend(extract_entries(slug, html, page_sub(html, slug)))
        # point search JS at the language-local index
        new = html.replace("fetch('/klinik-psixiatriya/search-index.json')",
                           f"fetch('/klinik-psixiatriya/{lang}/search-index.json')")
        if new != html:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new)
            n_fixed += 1
    out = os.path.join(d, 'search-index.json')
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(all_entries, f, ensure_ascii=False, separators=(',', ':'))
    print(f'[{lang}] {len(all_entries)} entries -> search-index.json ({os.path.getsize(out)//1024}KB); fetch-URL fixed in {n_fixed} pages')
