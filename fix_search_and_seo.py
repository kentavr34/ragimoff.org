#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1. Update search-index.json to include supplementary book pages
2. Fix old search JS in 8 book pages (index, giris, giris-yekun, mugeddime,
   abbreviatur, elave-acde, elave-skalalar, yekun) → use full-text index
3. Build site-wide search-index.json at root
4. Add search widget + SEO meta tags to all main site pages
"""
import sys, io, os, glob, re, json, unicodedata, html as htmllib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT  = r"C:\Users\SAM\Desktop\sayt2"
BOOK  = os.path.join(ROOT, 'klinik-psixiatriya')

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

# ═══════════════════════════════════════════════════════════
# STEP 1: Update book search-index.json to include all pages
# ═══════════════════════════════════════════════════════════
print('STEP 1: Rebuilding book search-index.json...')

def extract_entries(slug, html, sub):
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
    'bolme-01': 'Bölmə 1 — Neyroinkişaf',
    'bolme-02': 'Bölmə 2 — Şizofreniya',
    'bolme-03': 'Bölmə 3 — Katatoniya',
    'bolme-04': 'Bölmə 4 — Əhval',
    'bolme-05': 'Bölmə 5 — Təşviş',
    'bolme-06': 'Bölmə 6 — OKP',
    'bolme-07': 'Bölmə 7 — Stress',
    'bolme-08': 'Bölmə 8 — Dissosiativ',
    'bolme-09': 'Bölmə 9 — Yemə',
    'bolme-10': 'Bölmə 10 — İfrazat',
    'bolme-11': 'Bölmə 11 — Bədənsel',
    'bolme-12': 'Bölmə 12 — Maddə',
    'bolme-13': 'Bölmə 13 — İmpuls',
    'bolme-14': 'Bölmə 14 — Pozucu',
    'bolme-15': 'Bölmə 15 — Şəxsiyyət',
    'bolme-16': 'Bölmə 16 — Parafilik',
    'bolme-17': 'Bölmə 17 — Süni',
    'bolme-18': 'Bölmə 18 — Yuxu',
    'bolme-19': 'Bölmə 19 — Cinsi',
    'bolme-20': 'Bölmə 20 — Neyrokoqnitiv',
    'bolme-21': 'Bölmə 21 — Hamiləlik',
    'bolme-22': 'Bölmə 22 — İkincili',
    'bolme-ps': 'Psixosomatik',
    'index': 'Önsöz',
    'giris': 'Kitab haqqında',
    'giris-yekun': 'Kitab haqqında',
    'mugeddime': 'Müqəddimə',
    'abbreviatur': 'Terminoloji Lüğət',
    'elave-acde': 'Əlavələr A–E',
    'elave-skalalar': 'Əlavə — Skalalar',
    'yekun': 'Yekun',
}

all_entries = []
for fpath in sorted(glob.glob(os.path.join(BOOK, '*.html'))):
    slug = os.path.basename(fpath).replace('.html', '')
    sub = SUBS.get(slug, slug)
    with open(fpath, encoding='utf-8') as f:
        html = nfc(f.read())
    entries = extract_entries(slug, html, sub)
    all_entries.extend(entries)
    print(f'  {slug}: {len(entries)} entries')

book_idx_path = os.path.join(BOOK, 'search-index.json')
with open(book_idx_path, 'w', encoding='utf-8') as f:
    json.dump(all_entries, f, ensure_ascii=False, separators=(',', ':'))
print(f'  Book index: {len(all_entries)} entries → {os.path.getsize(book_idx_path)//1024}KB')

# ═══════════════════════════════════════════════════════════
# STEP 2: Fix old search JS in 8 non-bolme book pages
# ═══════════════════════════════════════════════════════════
print('\nSTEP 2: Fixing old search JS in non-bolme book pages...')

OLD_SEARCH_PATTERN = re.compile(
    r'const idx=\[\];.*?'
    r'(?:document\.addEventListener.*?Escape.*?\}\);|'
    r'si\.addEventListener.*?Escape.*?\}\);)',
    re.DOTALL
)

NEW_SEARCH_JS = """// Search — full-text index (lazy loaded from search-index.json)
let _srIdx=null,_srLoading=false;
function _srLoad(cb){
  if(_srIdx){cb(_srIdx);return;}
  if(_srLoading){setTimeout(()=>_srLoad(cb),80);return;}
  _srLoading=true;
  fetch('/klinik-psixiatriya/search-index.json')
    .then(r=>r.json())
    .then(d=>{_srIdx=d;_srLoading=false;cb(d);})
    .catch(()=>{_srIdx=[];_srLoading=false;cb([]);});
}

const si=document.getElementById('search-input');
const sd=document.getElementById('search-drop');
if(si&&sd){
  si.addEventListener('focus',()=>_srLoad(()=>{}),{once:true});
  let tmr;
  si.addEventListener('input',()=>{
    clearTimeout(tmr);
    tmr=setTimeout(()=>{
      const q=si.value.trim().toLowerCase();
      if(q.length<2){sd.classList.remove('on');return;}
      _srLoad(idx=>{
        const esc=q.replace(/[.*+?^${}()|[\\]\\\\]/g,'\\\\$&');
        const re=new RegExp(esc,'gi');
        const hl=s=>s?String(s).replace(re,m=>'<mark>'+m+'</mark>'):s;
        const res=idx.filter(x=>(x.title+' '+(x.codes||'')+' '+(x.icd||'')+' '+(x.text||'')).toLowerCase().includes(q)).slice(0,20);
        if(!res.length){sd.innerHTML='<div class="sr"><div class="sr-title">N\\u0259tic\\u0259 tap\\u0131lmad\\u0131</div></div>';sd.classList.add('on');return;}
        sd.innerHTML=res.map(r=>{
          let snip='';
          const txt=r.text||'';
          const lo=txt.toLowerCase();
          const i2=lo.indexOf(q);
          if(i2>=0){const s=Math.max(0,i2-50);snip=txt.slice(s,s+140).trim();}
          else{const co=(r.codes||'').toLowerCase();const i3=co.indexOf(q);
            if(i3>=0){const s=Math.max(0,i3-30);snip=(r.codes||'').slice(s,s+120).trim();}}
          return `<div class="sr" onclick="goTo('${r.page}','${r.id}')">
            <div class="sr-title">${hl(r.title)}</div>
            ${snip?`<div class="sr-snip">${hl(snip)}</div>`:''}
            <div class="sr-sub">${r.sub||r.page+'.html'}</div></div>`;
        }).join('');
        sd.classList.add('on');
      });
    },200);
  });
  document.addEventListener('click',e=>{if(!e.target.closest('.hdr-search'))sd.classList.remove('on');});
  si.addEventListener('keydown',e=>{if(e.key==='Escape'){si.value='';sd.classList.remove('on');}});
}"""

NON_BOLME = ['index', 'giris', 'giris-yekun', 'mugeddime', 'abbreviatur',
             'elave-acde', 'elave-skalalar', 'yekun']
fixed_search = 0
for slug in NON_BOLME:
    fpath = os.path.join(BOOK, slug + '.html')
    if not os.path.exists(fpath): continue
    with open(fpath, encoding='utf-8') as f:
        html = nfc(f.read())
    new_html, n = OLD_SEARCH_PATTERN.subn(lambda m: NEW_SEARCH_JS, html, count=1)
    if n:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_html)
        fixed_search += 1
        print(f'  Fixed: {slug}.html')
    else:
        print(f'  SKIP (no old pattern): {slug}.html')

print(f'  Search fixed in {fixed_search} pages')

# ═══════════════════════════════════════════════════════════
# STEP 3: Build site-wide search index
# ═══════════════════════════════════════════════════════════
print('\nSTEP 3: Building site-wide search index...')

# Titles and categories for main site pages
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

# Add book page titles to site index
for e in all_entries:
    if e['id'] == '':
        continue
    # Add top-level disorder headings only
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

# ═══════════════════════════════════════════════════════════
# STEP 4: Add SEO meta tags to ALL pages (main site + book)
# ═══════════════════════════════════════════════════════════
print('\nSTEP 4: Adding/updating SEO meta tags...')

# Base keywords relevant to all pages
BASE_KW_AZ = 'psixoterapevt, psixoloq, psixiatr, həkim, Kənan Rəhimov, Bakı, psixologiya, psixoterapiya, depressiya, həyəcan, fobiya, OKP, PTSD'
BASE_KW_RU = 'психотерапевт, психолог, психиатр, врач, Кенан Рагимов, Баку, психология, психотерапия'

# Page-specific keywords
PAGE_KW = {
    'index':     'psixoterapevt Bakı, psixoloq Bakı, psixiatr, psixologiya məktəbi, psixologiya kursu',
    'haqqimda':  'Kənan Rəhimov, psixiatr, psixoterapevt, 23 il, IPAS, Bexterev',
    'tehsil':    'psixologiya kursu Bakı, DPO sertifikat, psixologiya peşəsi, psixoterapevt olma',
    'xidmetler': 'psixoterapiya seansı, fərdi konsultasiya, onlayn psixoloq, psixiatr qəbulu',
    'blog':      'psixologiya məqaləsi, depressiya, panik ataklar, sosial fobiya, OKP, ailə terapiyası',
    'depressiya': 'depressiya müalicəsi, kədər, əhval, antidepressant, CBT, psixoterapiya',
    'panik-ataklar': 'panik atak, panik pozuntu, həyəcan, nəfəs tutulması, ürək döyüntüsü',
    'sosial-fobiya': 'sosial fobiya, sosial həyəcan, utancaqlıq, ictimai yerlərdə qorxu',
    'enurez': 'gecə enurezi, sidikburaxma, uşaq enurezi, enürez müalicəsi',
    'aile-terapiyasi': 'ailə terapiyası, münaqişə, cütlük terapiyası, nikah problemi',
    'aile-terapiyasi-usaq': 'uşaq terapiyası, valideyn-uşaq münasibəti, davranış problemləri',
    'b2b': 'korporativ psixologiya, komanda birliyə, stress idarəetmə, işçi sağlamlığı',
    'klinik-psixiatriya': 'klinik psixiatriya kitabı, ICD-11, DSM-5, psixiatrik diaqnoz, XBT-11',
}

# JSON-LD for Person (main site only)
PERSON_JSONLD = '''<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Person",
"name":"Kənan Rəhimov","jobTitle":"Həkim-Psixiatr, Psixoterapevt",
"description":"23 illik klinik təcrübəyə malik həkim-psixiatr, psixoterapevt və psixologiya müəllimi.",
"url":"https://ragimoff.org","sameAs":["https://ragimoff.org/haqqimda.html"],
"knowsAbout":["Psixiatriya","Psixoterapiya","CBT","EMDR","Depressiya","OKP","PTSD"],
"worksFor":{"@type":"Organization","name":"RAGIMOFF Psixologiya Məktəbi","url":"https://ragimoff.org"},
"address":{"@type":"PostalAddress","addressLocality":"Bakı","addressCountry":"AZ"}}
</script>'''

# JSON-LD for Book (book pages)
BOOK_JSONLD = '''<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Book",
"name":"Klinik Psixiatriya","inLanguage":"az",
"author":{"@type":"Person","name":"Kənan Rəhimov"},
"about":"Psixiatrik pozuntuların diaqnostikası və müalicəsi üzrə klinik bələdçi. ICD-11, DSM-5.",
"url":"https://ragimoff.org/klinik-psixiatriya/",
"keywords":"psixiatriya, psixiatr, diaqnoz, ICD-11, DSM-5, klinik protokol"}
</script>'''

seo_updated = 0

def update_seo(fpath, page_kw, is_book=False):
    global seo_updated
    with open(fpath, encoding='utf-8') as f:
        html = nfc(f.read())

    slug = os.path.basename(fpath).replace('.html', '')
    specific_kw = PAGE_KW.get(slug, '')
    keywords = ', '.join(filter(None, [specific_kw, BASE_KW_AZ]))

    # Check if keywords already exist
    has_kw = bool(re.search(r'<meta[^>]+name=["\']keywords["\']', html, re.I))
    has_robots = bool(re.search(r'<meta[^>]+name=["\']robots["\']', html, re.I))
    has_og = bool(re.search(r'<meta[^>]+property=["\']og:title["\']', html, re.I))
    has_jsonld = bool(re.search(r'application/ld\+json', html))
    has_canonical = bool(re.search(r'<link[^>]+rel=["\']canonical["\']', html, re.I))

    insert_tags = []

    if not has_kw:
        insert_tags.append(f'    <meta name="keywords" content="{keywords}" />')

    if not has_robots:
        insert_tags.append('    <meta name="robots" content="index, follow" />')

    # Open Graph
    if not has_og:
        title = get_title(html)
        desc = get_meta(html, 'description') or 'Psixoterapevt, psixoloq, psixiatr — Kənan Rəhimov. Bakı.'
        page_path = ('klinik-psixiatriya/' if is_book else '') + slug + '.html'
        insert_tags += [
            f'    <meta property="og:title" content="{title}" />',
            f'    <meta property="og:description" content="{desc}" />',
            '    <meta property="og:type" content="website" />',
            f'    <meta property="og:url" content="https://ragimoff.org/{page_path}" />',
            '    <meta property="og:locale" content="az_AZ" />',
        ]

    if not has_canonical:
        page_path = ('klinik-psixiatriya/' if is_book else '') + slug + '.html'
        insert_tags.append(f'    <link rel="canonical" href="https://ragimoff.org/{page_path}" />')

    if not has_jsonld:
        insert_tags.append(BOOK_JSONLD if is_book else PERSON_JSONLD)

    if not insert_tags:
        return  # Nothing to add

    # Insert before </head>
    new_html = html.replace('</head>', '\n'.join(insert_tags) + '\n  </head>', 1)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(new_html)
    seo_updated += 1

# Main site pages
for fpath in sorted(glob.glob(os.path.join(ROOT, '*.html'))):
    slug = os.path.basename(fpath).replace('.html', '')
    if slug == 'template': continue
    update_seo(fpath, PAGE_KW.get(slug, ''), is_book=False)

# Book pages
for fpath in sorted(glob.glob(os.path.join(BOOK, '*.html'))):
    update_seo(fpath, '', is_book=True)

print(f'  SEO updated: {seo_updated} pages')

# ═══════════════════════════════════════════════════════════
# STEP 5: Add search widget to main site header (all pages)
# ═══════════════════════════════════════════════════════════
print('\nSTEP 5: Adding search to main site header...')

SEARCH_CSS = """<style id="site-search-css">
.site-search-wrap{position:relative;margin-left:12px}
#site-si{background:rgba(255,255,255,0.1);border:1px solid rgba(181,155,114,0.3);
  border-radius:4px;color:#fff;font-family:inherit;font-size:13px;
  padding:6px 34px 6px 12px;width:200px;outline:none;
  transition:border-color .2s,width .3s,background .2s}
#site-si:focus{border-color:#d4af6a;background:rgba(255,255,255,0.15);width:260px}
#site-si::placeholder{color:rgba(255,255,255,0.4)}
.site-search-ico{position:absolute;right:10px;top:50%;transform:translateY(-50%);
  color:rgba(255,255,255,0.45);font-size:14px;pointer-events:none}
#site-sd{display:none;position:absolute;top:calc(100% + 6px);right:0;width:360px;
  background:#0e1a24;border:1px solid rgba(181,155,114,0.25);border-radius:6px;
  max-height:400px;overflow-y:auto;z-index:2000;
  box-shadow:0 16px 48px rgba(0,0,0,0.6)}
#site-sd.on{display:block}
.ssr{padding:10px 14px;border-bottom:1px solid rgba(255,255,255,0.06);
  cursor:pointer;transition:background .15s}
.ssr:last-child{border-bottom:none}
.ssr:hover{background:rgba(255,255,255,0.06)}
.ssr-title{font-size:13px;font-weight:600;color:#e0e0e0;margin-bottom:2px}
.ssr-snip{font-size:11px;color:rgba(255,255,255,0.5);line-height:1.5}
.ssr-sub{font-size:10px;color:#d4af6a;margin-top:3px;text-transform:uppercase;letter-spacing:.05em}
.ssr mark{background:rgba(212,175,106,0.35);color:#fff;border-radius:2px}
@media(max-width:900px){.site-search-wrap{display:none}}
</style>"""

SEARCH_HTML = """<div class="site-search-wrap">
          <input id="site-si" type="text" placeholder="Axtar..." autocomplete="off">
          <span class="site-search-ico">&#128269;</span>
          <div id="site-sd"></div>
        </div>"""

SEARCH_JS = """<script id="site-search-js">
(function(){
  var si=document.getElementById('site-si'),sd=document.getElementById('site-sd');
  if(!si||!sd)return;
  var idx=null,loading=false;
  function load(cb){
    if(idx){cb(idx);return;}
    if(loading){setTimeout(function(){load(cb);},80);return;}
    loading=true;
    fetch('/search-index.json').then(function(r){return r.json();})
      .then(function(d){idx=d;loading=false;cb(d);})
      .catch(function(){idx=[];loading=false;cb([]);});
  }
  si.addEventListener('focus',function(){load(function(){});},{once:true});
  var tmr;
  si.addEventListener('input',function(){
    clearTimeout(tmr);
    tmr=setTimeout(function(){
      var q=si.value.trim().toLowerCase();
      if(q.length<2){sd.classList.remove('on');return;}
      load(function(data){
        var esc=q.replace(/[.*+?^${}()|[\\]\\\\]/g,'\\\\$&');
        var re=new RegExp(esc,'gi');
        function hl(s){return s?String(s).replace(re,function(m){return'<mark>'+m+'</mark>'}):''}
        var res=data.filter(function(x){
          return(x.title+' '+(x.text||'')).toLowerCase().includes(q);
        }).slice(0,15);
        if(!res.length){sd.innerHTML='<div class="ssr"><div class="ssr-title">Nəticə tapılmadı</div></div>';sd.classList.add('on');return;}
        sd.innerHTML=res.map(function(r){
          var snip='';var txt=r.text||'';var lo=txt.toLowerCase();var i2=lo.indexOf(q);
          if(i2>=0){var s=Math.max(0,i2-50);snip=txt.slice(s,s+120).trim();}
          var url=r.url||(r.page+'.html'+(r.id?'#'+r.id:''));
          return '<div class="ssr" onclick="window.location.href=\\''+url+'\\'">'
            +'<div class="ssr-title">'+hl(r.title)+'</div>'
            +(snip?'<div class="ssr-snip">'+hl(snip)+'</div>':'')
            +'<div class="ssr-sub">'+r.sub+'</div></div>';
        }).join('');
        sd.classList.add('on');
      });
    },200);
  });
  document.addEventListener('click',function(e){if(!e.target.closest('.site-search-wrap'))sd.classList.remove('on');});
  si.addEventListener('keydown',function(e){if(e.key==='Escape'){si.value='';sd.classList.remove('on');}});
})();
</script>"""

search_added = 0
# Add to all main site HTML pages
for fpath in sorted(glob.glob(os.path.join(ROOT, '*.html'))):
    slug = os.path.basename(fpath).replace('.html', '')
    if slug == 'template': continue
    with open(fpath, encoding='utf-8') as f:
        html = nfc(f.read())

    # Skip if already has site-search
    if 'site-search-wrap' in html or 'site-si' in html:
        continue

    # Add CSS before </head>
    html = html.replace('</head>', SEARCH_CSS + '\n  </head>', 1)

    # Add search input inside desktop-nav, before the last </nav> close but after lang-switch
    # Insert before </nav> of desktop-nav
    # Pattern: find lang-switch and insert after it
    html = html.replace(
        '<a href="ru/index.html" class="lang-switch"',
        SEARCH_HTML + '\n          <a href="ru/index.html" class="lang-switch"',
        1
    )

    # Add JS before </body>
    html = html.replace('</body>', SEARCH_JS + '\n</body>', 1)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)
    search_added += 1

print(f'  Search added to {search_added} main site pages')
print('\nDone.')
