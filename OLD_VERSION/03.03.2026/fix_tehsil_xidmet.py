# -*- coding: utf-8 -*-
"""Fix tehsil.html footer and xidmetler header"""
import sys, re, os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

STANDARD_FOOTER = """<footer>
  <div class="footer-inner" style="max-width:1300px; margin:0 auto; padding:80px 40px;">
    <div style="display:grid; grid-template-columns:2fr 1fr 1fr 1fr; gap:60px; align-items:start; margin-bottom:60px;">
      <div>
        <a href="index.html" class="logo-box" style="display:inline-flex; margin-bottom:20px;">
          <img src="images/Logo-Ragimoff-Psy.jpg" alt="RAGIMOFF Logo" style="height:50px; border-radius:2px; opacity:0.85;">
        </a>
        <p style="font-size:0.9rem; color:rgba(255,255,255,0.55); line-height:1.7; max-width:280px;">K\u0259nan R\u0259himov \u2014 H\u0259kim-Psixiatr, Psixoterapevt. 23 il klinik t\u0259cr\u00fcb\u0259.</p>
        <div style="display:flex; gap:10px; margin-top:20px;">
          <a href="https://t.me/ragimoff" target="_blank" style="background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.15); color:rgba(255,255,255,0.7); padding:8px 14px; font-size:0.75rem; font-weight:700; text-decoration:none; border-radius:2px;">TG</a>
          <a href="https://www.instagram.com/dr.ragimoff" target="_blank" style="background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.15); color:rgba(255,255,255,0.7); padding:8px 14px; font-size:0.75rem; font-weight:700; text-decoration:none; border-radius:2px;">IG</a>
          <a href="https://youtube.com/@kragimoff" target="_blank" style="background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.15); color:rgba(255,255,255,0.7); padding:8px 14px; font-size:0.75rem; font-weight:700; text-decoration:none; border-radius:2px;">YT</a>
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
          <li><a href="blog.html" style="color:rgba(255,255,255,0.6); text-decoration:none; font-size:0.85rem;">Blog</a></li>
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
      <p style="font-size:0.82rem; color:rgba(255,255,255,0.35);">&copy; 2026 RAGIMOFF Pe\u015f\u0259kar Psixologiya M\u0259kt\u0259bi.</p>
    </div>
  </div>
</footer>

<a href="https://wa.me/994702200376" class="wa-float" target="_blank">
  <svg viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
</a>"""

# Fix tehsil.html - read with errors=replace, upgrade footer
print('[tehsil.html]')
with open('tehsil.html', 'rb') as f:
    raw = f.read()

# Try to decode as UTF-8 with replacement
c = raw.decode('utf-8', errors='replace')
ft_pat = r'<footer[^>]*>.*?</footer>(\s*<a[^>]*wa-float[^>]*>.*?</a>)?'
m2 = re.search(ft_pat, c, re.DOTALL)
if m2:
    if 'grid-template-columns:2fr' not in m2.group(0):
        c = c[:m2.start()] + STANDARD_FOOTER + c[m2.end():]
        print('  + Footer upgraded')
    else:
        print('  = Footer already OK')
else:
    body_idx = c.rfind('</body>')
    if body_idx != -1:
        c = c[:body_idx] + '\n\n' + STANDARD_FOOTER + '\n\n' + c[body_idx:]
        print('  + Footer appended')

with open('tehsil.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('  + Saved\n')

# Fix xidmetler.html - may need header
print('[xidmetler.html]')
with open('xidmetler.html', 'r', encoding='utf-8') as f:
    c = f.read()

if 'logo-box' not in c:
    # Replace old header
    hdr_pat = r'<header>.*?</header>'
    m = re.search(hdr_pat, c, re.DOTALL)
    if m:
        new_hdr = """<header>
  <div class="header-inner">
    <a href="index.html" class="logo-box">
      <img src="images/Logo-Ragimoff-Psy.jpg" alt="RAGIMOFF Logo">
    </a>
    <nav class="desktop-nav">
      <a href="index.html">Ana S\u0259hif\u0259</a>
      <a href="tehsil.html">T\u0259hsil</a>
      <a href="index.html#services" class="active">Konsultasiya</a>
      <a href="b2b.html">Korporativ</a>
      <a href="blog.html">Blog</a>
      <a href="tehsil.html#registration" class="btn nav-cta">QEYD\u0130YYAT</a>
    </nav>
    <button class="mobile-toggle" onclick="toggleMenu()" aria-label="Menu">
      <svg viewBox="0 0 24 24"><path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z"/></svg>
    </button>
  </div>
</header>"""
        c = c[:m.start()] + new_hdr + c[m.end():]
        print('  + Header replaced')
    
    # Upgrade footer
    ft_pat = r'<footer[^>]*>.*?</footer>'
    m2 = re.search(ft_pat, c, re.DOTALL)
    if m2:
        c = c[:m2.start()] + STANDARD_FOOTER + c[m2.end():]
        print('  + Footer upgraded')
    
    with open('xidmetler.html', 'w', encoding='utf-8') as f:
        f.write(c)
    print('  + Saved\n')
else:
    print('  = Already has logo-box')

print('Done!')
