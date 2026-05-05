# -*- coding: utf-8 -*-
"""
Mass migrate page heroes to .page-hero-x style.
Handles: pg-hero, pg-hero-plain, en-hero, page-hero (legacy variants).
Skips files that already have page-hero-x.
"""
import os, re, sys, io

ROOT = os.path.dirname(os.path.abspath(__file__))

# ---------- Translation tables ----------
BADGE_TRANS = {
    'BLOQ':            {'ru': 'СТАТЬИ',          'en': 'ARTICLES'},
    'BLOQ MƏQALƏ':     {'ru': 'СТАТЬЯ',          'en': 'ARTICLE'},
    'DİAQNOZ':         {'ru': 'ДИАГНОЗ',         'en': 'DIAGNOSIS'},
    'HÜQUQI MƏLUMAT':  {'ru': 'ПРАВО',           'en': 'LEGAL'},
    'AİLƏ TERAPİYASI': {'ru': 'СЕМЬЯ',           'en': 'FAMILY'},
    'UŞAQ TERAPİYASI': {'ru': 'ДЕТИ',            'en': 'CHILDREN'},
    'PEŞƏ PROQRAMI':   {'ru': 'ОБРАЗОВАНИЕ',     'en': 'EDUCATION'},
    'ƏLAVƏ TƏHSİL':    {'ru': 'ДОПОБРАЗОВАНИЕ',  'en': 'EDUCATION'},
}

PLACEHOLDER = {
    'az': ('Mövzu axtarın...', 'AXTAR'),
    'ru': ('Поиск...',         'ПОИСК'),
    'en': ('Search...',        'SEARCH'),
}

def detect_lang(path):
    p = path.replace('\\','/').lower()
    if '/ru/' in p: return 'ru'
    if '/en/' in p: return 'en'
    return 'az'

def split_h1(text):
    """Split heading text into 2 roughly equal parts by words."""
    # strip <em>/<br/> tags
    text = re.sub(r'</?em[^>]*>', '', text)
    text = re.sub(r'<br\s*/?>', ' ', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    words = text.split()
    if len(words) <= 1:
        return (text, '')
    if len(words) == 2:
        return (words[0], words[1])
    # Split roughly in half by word count
    mid = len(words) // 2
    return (' '.join(words[:mid]), ' '.join(words[mid:]))

def chunk_lead(lead_text, mob_chars=35, desk_chars=70):
    """Break lead text into mobile/desktop chunks."""
    lead_text = re.sub(r'</?em[^>]*>', '', lead_text)
    lead_text = re.sub(r'<br\s*/?>', ' ', lead_text)
    lead_text = re.sub(r'<[^>]+>', '', lead_text)
    lead_text = re.sub(r'&nbsp;', ' ', lead_text)
    lead_text = re.sub(r'\s+', ' ', lead_text).strip()
    if not lead_text:
        return [], []
    words = lead_text.split()
    def pack(words, max_chars):
        lines, cur = [], ''
        for w in words:
            if not cur:
                cur = w
            elif len(cur) + 1 + len(w) <= max_chars:
                cur += ' ' + w
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return lines
    mob = pack(words, mob_chars)[:3]
    desk = pack(words, desk_chars)[:2]
    return mob, desk

def build_hero(badge, h1_w1, h1_w2, mob_lines, desk_lines, bg_url, lang, page_id='page-h1'):
    placeholder, btn = PLACEHOLDER.get(lang, PLACEHOLDER['az'])
    style = f' style="background-image:url(\'{bg_url}\');"' if bg_url else ''
    h1_inner = f'<span class="ph-h1-w1">{h1_w1}</span>'
    if h1_w2:
        h1_inner += f'\n          <span class="ph-h1-w2">{h1_w2}</span>'
    sub_lines = []
    for m in mob_lines:
        sub_lines.append(f'          <span class="ph-sub-mob">{m}</span>')
    for d in desk_lines:
        sub_lines.append(f'          <span class="ph-sub-desk">{d}</span>')
    sub_block = '\n'.join(sub_lines) if sub_lines else f'          <span class="ph-sub-desk">&nbsp;</span>'
    return f'''<section class="page-hero-x" data-theme="dark"{style} aria-labelledby="{page_id}">
      <div class="page-hero-x-inner">
        <span class="ph-badge">{badge}</span>
        <h1 class="ph-h1" id="{page_id}">
          {h1_inner}
        </h1>
        <p class="ph-sub">
{sub_block}
        </p>
        <div class="ph-search-wrap hero-search-wrap">
          <div class="hero-search-bar">
            <input id="hero-si" type="text" placeholder="{placeholder}" autocomplete="off"/>
            <button class="hero-search-btn" onclick="heroSearch()">
              <svg class="search-icon" xmlns="http://www.w3.org/2000/svg" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
              <span>{btn}</span>
            </button>
          </div>
          <div id="hero-sd"></div>
        </div>
      </div>
    </section>'''

# ---------- Hero detection ----------
# Match a <section ...class="...pg-hero..."> ... </section>
SECTION_HERO_RE = re.compile(
    r'<section\b[^>]*class="[^"]*\bpg-hero\b[^"]*"[^>]*>.*?</section>',
    re.DOTALL | re.IGNORECASE
)
# Older "page-hero" (not page-hero-x)
SECTION_PAGE_HERO_RE = re.compile(
    r'<section\b[^>]*class="[^"]*\bpage-hero(?!-x)\b[^"]*"[^>]*>.*?</section>',
    re.DOTALL | re.IGNORECASE
)
# en-hero is a div wrapper
DIV_EN_HERO_RE = re.compile(
    r'<div\s+class="en-hero">\s*<div\s+class="en-hero-inner">.*?</div>\s*</div>\s*</div>',
    re.DOTALL
)

H1_RE   = re.compile(r'<h1[^>]*>(.*?)</h1>', re.DOTALL | re.IGNORECASE)
BADGE_RE = re.compile(r'<span[^>]*class="[^"]*\bbadge\b[^"]*"[^>]*>(.*?)</span>', re.DOTALL | re.IGNORECASE)
LEAD_RE  = re.compile(r'<p[^>]*class="[^"]*\bhero-lead\b[^"]*"[^>]*>(.*?)</p>', re.DOTALL | re.IGNORECASE)
BG_RE    = re.compile(r'background-image:\s*url\(\s*[\'"]?([^\'"\)]+)[\'"]?\s*\)', re.IGNORECASE)

def translate_badge(badge_az, lang):
    if lang == 'az':
        return badge_az
    key = badge_az.upper().strip()
    # Strip trailing punctuation/dots
    key_clean = re.sub(r'\s*[·.]+\s*$', '', key).strip()
    if key_clean in BADGE_TRANS:
        return BADGE_TRANS[key_clean][lang]
    # Try partial matches
    for k, v in BADGE_TRANS.items():
        if k in key_clean:
            return v[lang]
    return badge_az  # fallback

def migrate_section(html, hero_text, lang):
    """Given the original hero block, build replacement and return new html."""
    h1m   = H1_RE.search(hero_text)
    badm  = BADGE_RE.search(hero_text)
    leadm = LEAD_RE.search(hero_text)
    bgm   = BG_RE.search(hero_text)
    if not h1m:
        return None
    h1_text = h1m.group(1)
    # Strip trailing badge dot punctuation
    badge_raw = badm.group(1).strip() if badm else ''
    badge_raw = re.sub(r'\s*[·.]+\s*$', '', badge_raw).strip()
    if not badge_raw:
        # Default per language
        defaults = {'az': 'BLOQ', 'ru': 'СТАТЬИ', 'en': 'ARTICLES'}
        badge_raw = defaults[lang]
    badge = translate_badge(badge_raw, lang)
    # Uppercase for display
    badge_upper = badge.upper()
    w1, w2 = split_h1(h1_text)
    lead_text = leadm.group(1) if leadm else ''
    mob, desk = chunk_lead(lead_text)
    if not desk and not mob:
        # one fallback line
        desk = ['']
    bg = bgm.group(1) if bgm else None
    return build_hero(badge_upper, w1, w2, mob, desk, bg, lang)

def ensure_js_hero_fit(html):
    if 'js-hero-fit.js' in html:
        return html
    # Inject before closing body
    insert = '<script src="js-hero-fit.js"></script>'
    if '/ru/' in html or '/en/' in html or 'src="../js-hero-fit.js"' in html:
        pass
    if re.search(r'</body>', html, re.IGNORECASE):
        html = re.sub(r'</body>', insert + '\n</body>', html, count=1, flags=re.IGNORECASE)
    return html

def fix_js_hero_fit_path(html, path):
    """If file is in subdir ru/ or en/, ensure ../js-hero-fit.js"""
    p = path.replace('\\','/').lower()
    if '/ru/' in p or '/en/' in p:
        # If we just inserted "js-hero-fit.js", change to ../js-hero-fit.js
        html = re.sub(r'src="js-hero-fit\.js"', 'src="../js-hero-fit.js"', html)
    return html

def migrate_file(path):
    with io.open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    if 'page-hero-x' in html:
        return ('skip-already', path)

    lang = detect_lang(path)
    new_html = html
    replaced = False

    # Try pg-hero section
    m = SECTION_HERO_RE.search(new_html)
    if m:
        repl = migrate_section(new_html, m.group(0), lang)
        if repl:
            new_html = new_html[:m.start()] + repl + new_html[m.end():]
            replaced = True

    # Try page-hero (legacy, not page-hero-x)
    if not replaced:
        m = SECTION_PAGE_HERO_RE.search(new_html)
        if m:
            repl = migrate_section(new_html, m.group(0), lang)
            if repl:
                new_html = new_html[:m.start()] + repl + new_html[m.end():]
                replaced = True

    # Try en-hero div
    if not replaced:
        m = DIV_EN_HERO_RE.search(new_html)
        if m:
            block = m.group(0)
            repl = migrate_section(new_html, block, lang)
            if repl:
                new_html = new_html[:m.start()] + repl + new_html[m.end():]
                replaced = True

    if not replaced:
        return ('skip-no-hero', path)

    new_html = ensure_js_hero_fit(new_html)
    new_html = fix_js_hero_fit_path(new_html, path)

    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    return ('migrated', path)

def collect_files(group):
    if group == 'X1':
        return [os.path.join(ROOT, 'enurez.html')]
    if group == 'X2':
        return [os.path.join(ROOT, 'tehsil.html')]
    if group == 'X3':
        return [os.path.join(ROOT, 'blog.html')]
    if group == 'X4':
        files = []
        for fn in sorted(os.listdir(ROOT)):
            if fn.startswith('blog-') and fn.endswith('.html') and fn != 'blog-klinik-psixiatriya.html':
                files.append(os.path.join(ROOT, fn))
        # include blog-klinik-psixiatriya too (it's pending)
        bkpx = os.path.join(ROOT, 'blog-klinik-psixiatriya.html')
        if os.path.exists(bkpx):
            files.append(bkpx)
        return files
    if group == 'X5':
        ru = os.path.join(ROOT, 'ru')
        return [os.path.join(ru, fn) for fn in sorted(os.listdir(ru)) if fn.endswith('.html')]
    if group == 'X6':
        en = os.path.join(ROOT, 'en')
        return [os.path.join(en, fn) for fn in sorted(os.listdir(en)) if fn.endswith('.html')]
    return []

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    groups = sys.argv[1:] or ['X1','X2','X3','X4','X5','X6']
    for g in groups:
        files = collect_files(g)
        print(f'=== Group {g} ({len(files)} files) ===')
        stats = {'migrated':0, 'skip-already':0, 'skip-no-hero':0}
        for p in files:
            try:
                status, _ = migrate_file(p)
                stats[status] = stats.get(status,0) + 1
                print(f'  [{status}] {os.path.relpath(p, ROOT)}')
            except Exception as e:
                print(f'  [ERROR] {os.path.relpath(p, ROOT)}: {e}')
        print(f'  -> {stats}')
