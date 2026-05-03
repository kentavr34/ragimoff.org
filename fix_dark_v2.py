#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix v2 dark theme issues:
1. Replace inline background:var(--white/--light) → dark values
2. Add hero search bar to index.html and all main pages
3. Add address to footer on all pages
4. Fix gallery duplicates (image thumbnails)
"""
import sys, io, os, glob, re, unicodedata

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = r"C:\Users\SAM\Desktop\sayt2"

def nfc(s): return unicodedata.normalize('NFC', s)

DARK_BG   = '#0B0E11'
DARK_SURF = '#1E2026'
DARK_CARD = '#2B2F36'

# ═══════════════════════════════════════════════
# STEP 1: Fix inline background colors in ALL HTML
# ═══════════════════════════════════════════════
print('STEP 1: Fixing inline background colors...')

INLINE_REPLACEMENTS = [
    # White/light backgrounds → dark surface
    (r'(style="[^"]*background\s*:\s*)var\(--white\)', r'\g<1>' + DARK_SURF),
    (r"(style='[^']*background\s*:\s*)var\(--white\)", r'\g<1>' + DARK_SURF),
    (r'(style="[^"]*background\s*:\s*)#fff\b', r'\g<1>' + DARK_SURF),
    (r"(style='[^']*background\s*:\s*)#fff\b", r'\g<1>' + DARK_SURF),
    (r'(style="[^"]*background\s*:\s*)#ffffff\b', r'\g<1>' + DARK_SURF),
    (r'(style="[^"]*background\s*:\s*)var\(--light\)', r'\g<1>' + DARK_BG),
    (r'(style="[^"]*background\s*:\s*)#f8f9fa\b', r'\g<1>' + DARK_BG),
    # Navy → even darker (already dark but standardize)
    (r'(style="[^"]*background\s*:\s*)var\(--navy\)', r'\g<1>' + DARK_BG),
    # CSS in <style> tags: background:var(--white) in class definitions
    # (these are in inline <style> blocks, not style attributes)
]

# Also fix <style> tag content
STYLE_REPLACEMENTS = [
    (r'\bbackground\s*:\s*var\(--white\)\s*!important', f'background:{DARK_SURF}!important'),
    (r'\bbackground\s*:\s*var\(--white\)', f'background:{DARK_SURF}'),
    (r'\bbackground\s*:\s*#fff\b\s*!important', f'background:{DARK_SURF}!important'),
    (r'\bbackground\s*:\s*#fff\b(?!\s*!important)', f'background:{DARK_SURF}'),
    (r'\bbackground\s*:\s*#ffffff\b', f'background:{DARK_SURF}'),
    (r'\bbackground\s*:\s*var\(--light\)', f'background:{DARK_BG}'),
    (r'\bcolor\s*:\s*var\(--text\)\b(?!\s*!important)', 'color:var(--bnb-text)'),
    (r'\bcolor\s*:\s*var\(--navy\)\b(?!\s*!important)', 'color:var(--bnb-text)'),
    # form/input backgrounds
    (r'\bbackground\s*:\s*var\(--white\);\s*color\s*:\s*var\(--clr-text\)',
     f'background:{DARK_CARD};color:var(--bnb-text)'),
]

fixed_files = 0
for fpath in sorted(glob.glob(os.path.join(ROOT, '*.html'))):
    slug = os.path.basename(fpath).replace('.html', '')
    if slug == 'template': continue
    with open(fpath, encoding='utf-8') as f:
        html = nfc(f.read())
    original = html

    # Fix inline style= attributes
    for pattern, repl in INLINE_REPLACEMENTS:
        html = re.sub(pattern, repl, html)

    # Fix <style> block content
    def fix_style_block(m):
        s = m.group(0)
        for pattern, repl in STYLE_REPLACEMENTS:
            s = re.sub(pattern, repl, s)
        return s
    html = re.sub(r'<style[^>]*>.*?</style>', fix_style_block, html,
                  flags=re.DOTALL|re.IGNORECASE)

    if html != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html)
        fixed_files += 1

print(f'  Inline backgrounds fixed: {fixed_files} files')

# ═══════════════════════════════════════════════
# STEP 2: Add hero search bar to index.html
# ═══════════════════════════════════════════════
print('\nSTEP 2: Adding hero search bar to index.html...')

HERO_SEARCH_HTML = '''
          <div class="hero-search-wrap">
            <div class="hero-search-bar">
              <input id="hero-si" type="text" placeholder="Mövzu, xidmət, diaqnoz axtarın..." autocomplete="off">
              <button class="hero-search-btn" onclick="heroSearch()"><span>AXTAR</span></button>
            </div>
            <div id="hero-sd"></div>
          </div>'''

HERO_SEARCH_JS = '''
<script>
(function(){
  var si2=document.getElementById('hero-si'),sd2=document.getElementById('hero-sd');
  if(!si2||!sd2)return;
  var idx2=null,loading2=false;
  function load2(cb){
    if(idx2){cb(idx2);return;}
    if(loading2){setTimeout(function(){load2(cb);},80);return;}
    loading2=true;
    fetch('/search-index.json').then(function(r){return r.json();})
      .then(function(d){idx2=d;loading2=false;cb(d);})
      .catch(function(){idx2=[];loading2=false;cb([]);});
  }
  function showResults(q, data){
    var esc=q.replace(/[.*+?^${}()|[\\]\\\\]/g,'\\\\$&');
    var re=new RegExp(esc,'gi');
    function hl(s){return s?String(s).replace(re,function(m){return'<mark>'+m+'</mark>'}):''}
    var res=data.filter(function(x){
      return(x.title+' '+(x.text||'')).toLowerCase().includes(q.toLowerCase());
    }).slice(0,12);
    if(!res.length){sd2.innerHTML='<div class="ssr"><div class="ssr-title">Nəticə tapılmadı</div></div>';sd2.classList.add('on');return;}
    sd2.innerHTML=res.map(function(r){
      var snip='';var txt=r.text||'';var lo=txt.toLowerCase();var i2=lo.indexOf(q.toLowerCase());
      if(i2>=0){var s=Math.max(0,i2-40);snip=txt.slice(s,s+100).trim();}
      var url=r.url||(r.page+'.html'+(r.id?'#'+r.id:''));
      return '<div class="ssr" onclick="window.location.href=\\''+url+'\\'">'
        +'<div class="ssr-title">'+hl(r.title)+'</div>'
        +(snip?'<div class="ssr-snip">'+hl(snip)+'</div>':'')
        +'<div class="ssr-sub">'+r.sub+'</div></div>';
    }).join('');
    sd2.classList.add('on');
  }
  window.heroSearch=function(){
    var q=si2.value.trim();
    if(q.length<2)return;
    load2(function(data){showResults(q,data);});
  };
  si2.addEventListener('focus',function(){load2(function(){});},{once:true});
  var tmr2;
  si2.addEventListener('input',function(){
    clearTimeout(tmr2);
    tmr2=setTimeout(function(){
      var q=si2.value.trim();
      if(q.length<2){sd2.classList.remove('on');return;}
      load2(function(data){showResults(q,data);});
    },200);
  });
  si2.addEventListener('keydown',function(e){
    if(e.key==='Enter'){heroSearch();}
    if(e.key==='Escape'){si2.value='';sd2.classList.remove('on');}
  });
  document.addEventListener('click',function(e){
    if(!e.target.closest('.hero-search-wrap'))sd2.classList.remove('on');
  });
})();
</script>'''

idx_path = os.path.join(ROOT, 'index.html')
with open(idx_path, encoding='utf-8') as f:
    html = nfc(f.read())

if 'hero-search-bar' not in html:
    # Insert after hero-btns div
    html = html.replace(
        '</div>\n\n        </div>\n\n        <div class="photo-col">',
        f'{HERO_SEARCH_HTML}\n        </div>\n\n        <div class="photo-col">',
        1
    )
    # Try alternative pattern
    if 'hero-search-bar' not in html:
        html = re.sub(
            r'(<div class="hero-btns">.*?</div>)',
            r'\1' + HERO_SEARCH_HTML,
            html, count=1, flags=re.DOTALL
        )
    # Add JS before </body>
    if 'hero-si' in html and 'window.heroSearch' not in html:
        html = html.replace('</body>', HERO_SEARCH_JS + '\n</body>', 1)
    with open(idx_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print('  Hero search added to index.html')
else:
    print('  Hero search already present in index.html')

# ═══════════════════════════════════════════════
# STEP 3: Add address to footer on ALL pages
# ═══════════════════════════════════════════════
print('\nSTEP 3: Adding address to footer...')

ADDRESS_HTML = '''<p class="footer-address">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="var(--bnb-gold)" style="vertical-align:middle;margin-right:4px"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
              AZ1065, Bakı şəhəri, Caspian Business Center, 9-cu mərtəbə
            </p>'''

addr_updated = 0
for fpath in sorted(glob.glob(os.path.join(ROOT, '*.html'))):
    slug = os.path.basename(fpath).replace('.html', '')
    if slug == 'template': continue
    with open(fpath, encoding='utf-8') as f:
        html = nfc(f.read())

    if 'footer-address' in html or 'Caspian Business' in html:
        continue

    # Find footer-desc and add address after it
    if 'footer-desc' in html:
        html = re.sub(
            r'(</p>\s*)(</div>\s*<div class="social-links">)',
            r'\1\n              ' + ADDRESS_HTML.strip() + r'\n            \2',
            html, count=1, flags=re.DOTALL
        )
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html)
        addr_updated += 1

print(f'  Address added to {addr_updated} pages')

# ═══════════════════════════════════════════════
# STEP 4: Add footer-address CSS to gtc-dark.css
# ═══════════════════════════════════════════════
print('\nSTEP 4: Adding footer-address CSS...')

ADDR_CSS = """
/* ─── Footer address ─── */
.footer-address {
  font-size: 0.75rem;
  color: var(--bnb-dim);
  margin: 8px 0 0;
  line-height: 1.5;
}
"""

dark_css_path = os.path.join(ROOT, 'gtc-dark.css')
with open(dark_css_path, encoding='utf-8') as f:
    dark_css = f.read()

if 'footer-address' not in dark_css:
    with open(dark_css_path, 'a', encoding='utf-8') as f:
        f.write(ADDR_CSS)
    print('  footer-address CSS added')

print('\nDone.')
