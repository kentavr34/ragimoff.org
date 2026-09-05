#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild site-wide search-index.json (root) including samira.html"""
import sys, io, os, glob, re, json, unicodedata, html as htmllib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.join(ROOT, 'klinik-psixiatriya')

def nfc(s): return unicodedata.normalize('NFC', s)
def strip_tags(s):
    s = re.sub(r'<[^>]+>', ' ', s)
    s = htmllib.unescape(s)
    return re.sub(r'\s+', ' ', s).strip()
def get_meta(html, name):
    m = re.search(r'<meta[^>]+name=["\']' + name + r'["\'][^>]+content=["\']([^"\']*)["\']', html, re.I)
    if m: return m.group(1).strip()
    m = re.search(r'<meta[^>]+content=["\']([^"\']*)["\'][^>]+name=["\']' + name + r'["\']', html, re.I)
    return m.group(1).strip() if m else ''
def get_title(html):
    m = re.search(r'<title>([^<]+)</title>', html, re.I)
    return strip_tags(m.group(1)) if m else ''

# --- Build book index first (needed for cross-refs) ---
def extract_book_entries(slug, html, sub):
    entries = []
    content = re.sub(r'<(script|style|nav|header|aside)[^>]*>.*?</\1>', ' ', html, flags=re.DOTALL|re.I)
    heading_pat = re.compile(r'<h([123])\s[^>]*id="([^"]+)"[^>]*>(.*?)</h\1>', re.DOTALL|re.IGNORECASE)
    headings = [(m.start(), int(m.group(1)), m.group(2), strip_tags(m.group(3)))
                for m in heading_pat.finditer(content)]
    for i, (pos, level, hid, title) in enumerate(headings):
        if not hid or any(x in hid for x in ['nav', 'footnote', 'footer']):
            continue
        if len(title) < 2: continue
        end = headings[i+1][0] if i+1 < len(headings) else pos + 800
        block = content[pos:end]
        xbt_lines = re.findall(r'class="xbt-line"[^>]*>(.*?)</div>', block, re.DOTALL)
        codes = ' | '.join(strip_tags(x)[:120] for x in xbt_lines[:6] if strip_tags(x))
        icd_codes = re.findall(r'class="icd">([^<]+)<', block)
        icd_str = ' '.join(sorted(set(c.strip() for c in icd_codes if len(c.strip()) <= 12)))
        para_texts = re.findall(r'<(?:p|li)(?:\s[^>]*)?>(?!<)(.*?)</(?:p|li)>', block, re.DOTALL)
        text_parts = []
        for pt in para_texts[:8]:
            t = strip_tags(pt)
            if len(t) > 20 and not t.startswith('XBT-') and not t.startswith('DSM-'):
                text_parts.append(t)
            if sum(len(x) for x in text_parts) > 350: break
        text = ' '.join(text_parts)[:400]
        entries.append({'page': slug, 'id': hid, 'title': title[:100],
                        'codes': codes[:300], 'icd': icd_str[:200],
                        'text': text[:400], 'sub': sub})
    return entries

SUBS = {
    'bolme-01': 'Bölmə 1 — Neyroinkişaf', 'bolme-02': 'Bölmə 2 — Şizofreniya',
    'bolme-03': 'Bölmə 3 — Katatoniya', 'bolme-04': 'Bölmə 4 — Əhval',
    'bolme-05': 'Bölmə 5 — Təşviş', 'bolme-06': 'Bölmə 6 — OKP',
    'bolme-07': 'Bölmə 7 — Stress', 'bolme-08': 'Bölmə 8 — Dissosiativ',
    'bolme-09': 'Bölmə 9 — Yemə', 'bolme-10': 'Bölmə 10 — İfrazat',
    'bolme-11': 'Bölmə 11 — Bədənsel', 'bolme-12': 'Bölmə 12 — Maddə',
    'bolme-13': 'Bölmə 13 — İmpuls', 'bolme-14': 'Bölmə 14 — Pozucu',
    'bolme-15': 'Bölmə 15 — Şəxsiyyət', 'bolme-16': 'Bölmə 16 — Parafilik',
    'bolme-17': 'Bölmə 17 — Süni', 'bolme-18': 'Bölmə 18 — Yuxu',
    'bolme-19': 'Bölmə 19 — Cinsi', 'bolme-20': 'Bölmə 20 — Neyrokoqnitiv',
    'bolme-21': 'Bölmə 21 — Hamiləlik', 'bolme-22': 'Bölmə 22 — İkincili',
    'bolme-ps': 'Psixosomatik', 'index': 'Önsöz', 'giris': 'Kitab haqqında',
    'giris-yekun': 'Kitab haqqında', 'mugeddime': 'Müqəddimə',
    'abbreviatur': 'Terminoloji Lüğət', 'elave-acde': 'Əlavələr A–E',
    'elave-skalalar': 'Əlavə — Skalalar', 'yekun': 'Yekun',
}

print('Building book search index...')
all_book_entries = []
for fpath in sorted(glob.glob(os.path.join(BOOK, '*.html'))):
    slug = os.path.basename(fpath).replace('.html', '')
    sub = SUBS.get(slug, slug)
    with open(fpath, encoding='utf-8') as f:
        html = nfc(f.read())
    entries = extract_book_entries(slug, html, sub)
    all_book_entries.extend(entries)
    print(f'  {slug}: {len(entries)} entries')

book_idx_path = os.path.join(BOOK, 'search-index.json')
with open(book_idx_path, 'w', encoding='utf-8') as f:
    json.dump(all_book_entries, f, ensure_ascii=False, separators=(',', ':'))
print(f'  Book index: {len(all_book_entries)} entries → {os.path.getsize(book_idx_path)//1024}KB')

# --- Build site-wide search index ---
print('\nBuilding site-wide search index...')

SITE_META = {
    'index':              ('Ana Səhifə — RAGIMOFF', 'site', 'Ana Səhifə'),
    'haqqimda':           ('Kənan Rəhimov Haqqında', 'site', 'Haqqımda'),
    'tehsil':             ('Psixologiya Təhsili', 'site', 'Təhsil'),
    'xidmetler':          ('Psixoterapiya Xidmətləri', 'site', 'Xidmətlər'),
    'blog':               ('Psixologiya Bloqu', 'blog', 'Blog'),
    'depressiya':         ('Depressiya Müalicəsi', 'site', 'Xidmətlər'),
    'panik-ataklar':      ('Panik Ataklar', 'site', 'Xidmətlər'),
    'sosial-fobiya':      ('Sosial Fobiya', 'site', 'Xidmətlər'),
    'enurez':             ('Gecə Enurezi', 'site', 'Xidmətlər'),
    'aile-terapiyasi':    ('Ailə Terapiyası', 'site', 'Xidmətlər'),
    'aile-terapiyasi-usaq': ('Ailə-Uşaq Terapiyası', 'site', 'Xidmətlər'),
    'b2b':                ('Korporativ Proqramlar', 'site', 'Korporativ'),
    'qanunlar':           ('Qanuni Əsaslar', 'site', 'Qanunlar'),
    'program-umumi':      ('Ümumi Psixologiya', 'site', 'Proqramlar'),
    'program-klinik':     ('Klinik Psixologiya DPO', 'site', 'Proqramlar'),
    'program-praktikum':  ('Psixoterapiya Praktikumu', 'site', 'Proqramlar'),
    'klinik-psixiatriya': ('Klinik Psixiatriya Kitabı', 'book', 'Kitab'),
    'samira':             ('Samira Rəhimova — Psixolog', 'site', 'Komanda'),
}

site_entries = []

# Main site pages
for fpath in sorted(glob.glob(os.path.join(ROOT, '*.html'))):
    slug = os.path.basename(fpath).replace('.html', '')
    if slug == 'template': continue
    with open(fpath, encoding='utf-8') as f:
        html = nfc(f.read())
    page_title = get_title(html)
    desc = get_meta(html, 'description')
    meta = SITE_META.get(slug, (page_title, 'blog' if 'blog-' in slug else 'site', 'Blog' if 'blog-' in slug else 'Sayt'))
    etype = meta[1]
    esub = meta[2]

    # Page entry
    site_entries.append({'page': slug, 'id': '', 'title': page_title,
                         'text': desc, 'sub': esub, 'type': etype,
                         'url': slug + '.html'})

    # Section headings
    content = re.sub(r'<(script|style|nav|header|footer)[^>]*>.*?</\1>', ' ', html, flags=re.DOTALL|re.I)
    for m in re.finditer(r'<h([23])[^>]*id=["\']([^"\']+)["\'][^>]*>(.*?)</h\1>', content, re.DOTALL|re.I):
        hid = m.group(2)
        title_text = strip_tags(m.group(3)).strip()
        if len(title_text) < 3: continue
        pos = m.end()
        next_h = re.search(r'<h[1-4][^>]*>', content[pos:])
        end = pos + (next_h.start() if next_h else 400)
        snippet = strip_tags(content[pos:end])[:200].strip()
        site_entries.append({'page': slug, 'id': hid, 'title': title_text,
                              'text': snippet, 'sub': esub, 'type': etype,
                              'url': slug + '.html#' + hid})

# Add book page titles to site index (top-level disorder headings only)
for e in all_book_entries:
    if e['id'] == '':
        continue
    if e['title'] and e['page'].startswith('bolme'):
        site_entries.append({'page': 'klinik-psixiatriya/' + e['page'],
                              'id': e['id'], 'title': e['title'],
                              'text': e['text'][:150], 'sub': 'Kitab: ' + e['sub'],
                              'type': 'book',
                              'url': '/klinik-psixiatriya/' + e['page'] + '.html#' + e['id']})

site_idx_path = os.path.join(ROOT, 'search-index.json')
with open(site_idx_path, 'w', encoding='utf-8') as f:
    json.dump(site_entries, f, ensure_ascii=False, separators=(',', ':'))
print(f'  Site index: {len(site_entries)} entries → {os.path.getsize(site_idx_path)//1024}KB')

# Verify samira is included
samira_entries = [e for e in site_entries if e['page'] == 'samira']
print(f'\nSamira entries: {len(samira_entries)}')
for e in samira_entries:
    print(f'  {e}')