# -*- coding: utf-8 -*-
"""Fix remaining pages before deployment"""
import sys, re, os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE = os.path.dirname(os.path.abspath(__file__))

MOBILE_NAV_CSS = """
    .mobile-nav {
      display: none; position: fixed; top: 0; right: 0; width: 80vw; max-width: 320px; height: 100vh;
      background: #061826; z-index: 2000; padding: 40px 30px; flex-direction: column; gap: 4px;
      box-shadow: -20px 0 60px rgba(0,0,0,0.5); overflow-y: auto;
    }
    .mobile-nav.open { display: flex; }
    .mobile-nav a { color: rgba(255,255,255,0.8); text-decoration: none; font-size: 0.9rem; font-weight: 700; padding: 16px 0; border-bottom: 1px solid rgba(255,255,255,0.08); text-transform: uppercase; letter-spacing: 1px; transition: color 0.2s; }
    .mobile-nav a:hover { color: var(--accent); }
    .mobile-nav .btn-primary { margin-top: 16px; text-align: center; background: var(--accent); color: var(--navy); padding: 16px; font-weight: 800; border-radius: 2px; }
    .mobile-nav-close { background: none; border: none; color: rgba(255,255,255,0.6); cursor: pointer; margin-bottom: 20px; align-self: flex-end; padding: 4px; }
    .mobile-nav-close svg { width: 28px; height: 28px; fill: currentColor; }
    footer { background: #061826; color: rgba(255,255,255,0.6); }
    .wa-float { position: fixed; bottom: 28px; right: 28px; width: 58px; height: 58px; background: #25D366; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 8px 25px rgba(37,211,102,0.4); z-index: 1500; transition: transform 0.3s; text-decoration: none; }
    .wa-float:hover { transform: scale(1.1); }
    .wa-float svg { width: 30px; height: 30px; fill: white; }
    .logo-box { height: 60px; padding: 5px; background: rgba(255,255,255,0.05); border-radius: 4px; display: flex; align-items: center; border: 1px solid rgba(181,155,114,0.1); text-decoration: none; }
    .logo-box img { height: 100%; border-radius: 2px; }
"""

STANDARD_FOOTER = """<footer>
  <div class="footer-inner" style="max-width:1300px; margin:0 auto; padding:80px 40px;">
    <div style="display:grid; grid-template-columns:2fr 1fr 1fr 1fr; gap:60px; align-items:start; margin-bottom:60px;">
      <div>
        <a href="index.html" class="logo-box" style="display:inline-flex; margin-bottom:20px;">
          <img src="images/Logo-Ragimoff-Psy.jpg" alt="RAGIMOFF Logo" style="height:50px; border-radius:2px; opacity:0.85;">
        </a>
        <p style="font-size:0.9rem; color:rgba(255,255,255,0.55); line-height:1.7; max-width:280px;">K\u0259nan R\u0259himov \u2014 H\u0259kim-Psixiatr, Psixoterapevt. 23 il klinik t\u0259cr\u00fcb\u0259. Bak\u0131, Az\u0259rbaycan.</p>
        <div style="display:flex; gap:10px; margin-top:20px;">
          <a href="https://t.me/ragimoff" target="_blank" style="background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.15); color:rgba(255,255,255,0.7); padding:8px 14px; font-size:0.75rem; font-weight:700; text-decoration:none; border-radius:2px; letter-spacing:1px;">TG</a>
          <a href="https://www.facebook.com/Ragimoff.az" target="_blank" style="background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.15); color:rgba(255,255,255,0.7); padding:8px 14px; font-size:0.75rem; font-weight:700; text-decoration:none; border-radius:2px; letter-spacing:1px;">FB</a>
          <a href="https://www.instagram.com/dr.ragimoff" target="_blank" style="background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.15); color:rgba(255,255,255,0.7); padding:8px 14px; font-size:0.75rem; font-weight:700; text-decoration:none; border-radius:2px; letter-spacing:1px;">IG</a>
          <a href="https://youtube.com/@kragimoff" target="_blank" style="background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.15); color:rgba(255,255,255,0.7); padding:8px 14px; font-size:0.75rem; font-weight:700; text-decoration:none; border-radius:2px; letter-spacing:1px;">YT</a>
        </div>
      </div>
      <div>
        <h4 style="font-size:0.7rem; font-weight:800; letter-spacing:2px; text-transform:uppercase; color:var(--accent); margin-bottom:20px;">Terapiya</h4>
        <ul style="list-style:none; padding:0; display:grid; gap:10px;">
          <li><a href="aile-terapiyasi.html" style="color:rgba(255,255,255,0.6); text-decoration:none; font-size:0.85rem;">Ail\u0259 Terapiyas\u0131</a></li>
          <li><a href="enurez.html" style="color:rgba(255,255,255,0.6); text-decoration:none; font-size:0.85rem;">Enurez M\u00fcalic\u0259si</a></li>
          <li><a href="panik-ataklar.html" style="color:rgba(255,255,255,0.6); text-decoration:none; font-size:0.85rem;">Panik Ataklar</a></li>
          <li><a href="depressiya.html" style="color:rgba(255,255,255,0.6); text-decoration:none; font-size:0.85rem;">Depressiya</a></li>
          <li><a href="sosial-fobiya.html" style="color:rgba(255,255,255,0.6); text-decoration:none; font-size:0.85rem;">Sosial Fobiya</a></li>
        </ul>
      </div>
      <div>
        <h4 style="font-size:0.7rem; font-weight:800; letter-spacing:2px; text-transform:uppercase; color:var(--accent); margin-bottom:20px;">T\u0259hsil</h4>
        <ul style="list-style:none; padding:0; display:grid; gap:10px;">
          <li><a href="tehsil.html" style="color:rgba(255,255,255,0.6); text-decoration:none; font-size:0.85rem;">Klinik Psixologiya DPO</a></li>
          <li><a href="tehsil.html" style="color:rgba(255,255,255,0.6); text-decoration:none; font-size:0.85rem;">Psixoterapiya Praktikumu</a></li>
          <li><a href="blog.html" style="color:rgba(255,255,255,0.6); text-decoration:none; font-size:0.85rem;">Psixologiya Blogu</a></li>
          <li><a href="https://youtube.com/@kragimoff" target="_blank" style="color:rgba(255,255,255,0.6); text-decoration:none; font-size:0.85rem;">YouTube D\u0259rsl\u0259r</a></li>
        </ul>
      </div>
      <div>
        <h4 style="font-size:0.7rem; font-weight:800; letter-spacing:2px; text-transform:uppercase; color:var(--accent); margin-bottom:20px;">\u018flaq\u0259</h4>
        <ul style="list-style:none; padding:0; display:grid; gap:10px;">
          <li><a href="tel:+994702200376" style="color:rgba(255,255,255,0.6); text-decoration:none; font-size:0.85rem;">(+994) 70-220-03-76</a></li>
          <li><a href="https://wa.me/994702200376" style="color:rgba(255,255,255,0.6); text-decoration:none; font-size:0.85rem;">WhatsApp</a></li>
          <li><a href="https://t.me/dockenan" style="color:rgba(255,255,255,0.6); text-decoration:none; font-size:0.85rem;">Telegram</a></li>
        </ul>
      </div>
    </div>
    <div style="border-top:1px solid rgba(255,255,255,0.08); padding-top:40px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:16px;">
      <p style="font-size:0.82rem; color:rgba(255,255,255,0.35);">&copy; 2026 RAGIMOFF Pe\u015f\u0259kar Psixologiya M\u0259kt\u0259bi. Pe\u015f\u0259kar N\u00fcfuzun \u00dcnvan\u0131.</p>
      <a href="https://www.psychotherapyru.com" target="_blank" style="font-size:0.82rem; color:rgba(255,255,255,0.4); text-decoration:none;">Russkaya versiya &rarr;</a>
    </div>
  </div>
</footer>

<a href="https://wa.me/994702200376" class="wa-float" target="_blank">
  <svg viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
</a>"""

ACTIVE_MAP = {
    'qanunlar.html': '',
    'xidmetler.html': 'konsultasiya',
    'proqram.html': 'tehsil',
}

def build_header(active=''):
    a = ' class="active"'
    return """<header>
  <div class="header-inner">
    <a href="index.html" class="logo-box">
      <img src="images/Logo-Ragimoff-Psy.jpg" alt="RAGIMOFF Logo">
    </a>
    <nav class="desktop-nav">
      <a href="index.html"%(ana)s>Ana S\u0259hif\u0259</a>
      <a href="tehsil.html"%(tehsil)s>T\u0259hsil</a>
      <a href="index.html#services"%(konsul)s>Konsultasiya</a>
      <a href="b2b.html"%(korp)s>Korporativ</a>
      <a href="blog.html"%(blog)s>Blog</a>
      <a href="tehsil.html#registration" class="btn nav-cta">QEYD\u0130YYAT</a>
    </nav>
    <button class="mobile-toggle" onclick="toggleMenu()" aria-label="Menu">
      <svg viewBox="0 0 24 24"><path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z"/></svg>
    </button>
  </div>
</header>

<div class="mobile-nav" id="mobileNav">
  <button class="mobile-nav-close" onclick="toggleMenu()"><svg viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg></button>
  <a href="index.html" onclick="toggleMenu()">Ana S\u0259hif\u0259</a>
  <a href="tehsil.html" onclick="toggleMenu()">T\u0259hsil</a>
  <a href="index.html#services" onclick="toggleMenu()">Konsultasiya</a>
  <a href="b2b.html" onclick="toggleMenu()">Korporativ</a>
  <a href="blog.html" onclick="toggleMenu()">Blog</a>
  <a href="tehsil.html#registration" class="btn btn-primary" onclick="toggleMenu()">QEYD\u0130YYAT</a>
</div>""" % {
    'ana': a if active == 'ana' else '',
    'tehsil': a if active == 'tehsil' else '',
    'konsul': a if active == 'konsultasiya' else '',
    'korp': a if active == 'korporativ' else '',
    'blog': a if active == 'blog' else '',
}


for fn, active in ACTIVE_MAP.items():
    path = os.path.join(BASE, fn)
    if not os.path.exists(path):
        print(f'SKIP: {fn}')
        continue
    
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        c = f.read()
    
    print(f'[{fn}]')
    
    # Remove Playfair
    c = re.sub(
        r'<link href="https://fonts\.googleapis\.com/css2\?family=Playfair[^"]*" rel="stylesheet"\s*/>\s*\n?',
        '', c
    )
    for old, new in [
        ("font-family: 'Playfair Display', serif", "font-family: 'Inter', -apple-system, sans-serif"),
        ('font-family: "Playfair Display", serif', "font-family: 'Inter', -apple-system, sans-serif"),
        ("font-family:'Playfair Display',serif", "font-family:'Inter',-apple-system,sans-serif"),
    ]:
        c = c.replace(old, new)
    
    # Add CSS if needed
    if '.mobile-nav {' not in c and '.logo-box {' not in c:
        idx = c.rfind('</style>')
        if idx != -1:
            c = c[:idx] + MOBILE_NAV_CSS + c[idx:]
            print('  + CSS added')
    
    # Replace header
    new_hdr = build_header(active)
    hdr_pat = r'<header>.*?</header>(\s*<div[^>]*(?:mobile-nav|burger|mobileNav)[^>]*>.*?</div>)*'
    m = re.search(hdr_pat, c, re.DOTALL)
    if m:
        c = c[:m.start()] + new_hdr + c[m.end():]
        print('  + Header replaced')
    elif 'back-nav' in c:
        # proqram.html has back-nav instead of header - inject header before back-nav
        bn = c.find('<div class="back-nav">')
        if bn != -1:
            c = c[:bn] + new_hdr + '\n\n' + c[bn:]
            print('  + Header injected before back-nav')
    
    # Replace footer
    ft_pat = r'<footer[^>]*>.*?</footer>(\s*<a[^>]*wa-float[^>]*>.*?</a>)?'
    m2 = re.search(ft_pat, c, re.DOTALL)
    if m2:
        c = c[:m2.start()] + STANDARD_FOOTER + c[m2.end():]
        print('  + Footer replaced')
    else:
        body_idx = c.rfind('</body>')
        if body_idx != -1:
            c = c[:body_idx] + '\n\n' + STANDARD_FOOTER + '\n\n' + c[body_idx:]
            print('  + Footer appended')
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print('  + Saved\n')

# tehsil.html - only needs footer upgrade (add 4-col), header already OK
print('[tehsil.html]')
with open('tehsil.html', 'r', encoding='utf-8') as f:
    c = f.read()
    
ft_pat = r'<footer[^>]*>.*?</footer>(\s*<a[^>]*wa-float[^>]*>.*?</a>)?'
m2 = re.search(ft_pat, c, re.DOTALL)
if m2:
    existing = m2.group(0)
    if 'grid-template-columns:2fr' not in existing:
        c = c[:m2.start()] + STANDARD_FOOTER + c[m2.end():]
        print('  + Footer upgraded to 4-col')
    else:
        print('  = Footer already OK')

with open('tehsil.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('  + Saved\n')

print('All done!')
