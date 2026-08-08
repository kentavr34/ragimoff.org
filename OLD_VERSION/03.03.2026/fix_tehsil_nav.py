# -*- coding: utf-8 -*-
"""Fix tehsil.html - update nav to include Blog link"""
import sys, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Read as binary, decode with error handling
with open('tehsil.html', 'rb') as f:
    raw = f.read()
c = raw.decode('utf-8', errors='replace')

print(f'tehsil.html: {len(c)} chars')

# Fix the desktop nav - replace it wholesale
old_nav_pattern = r'<nav class="desktop-nav">.*?</nav>'
m = re.search(old_nav_pattern, c, re.DOTALL)
if m:
    print(f'Found nav at pos {m.start()}: {repr(m.group(0)[:100])}')
    new_nav = """<nav class="desktop-nav">
      <a href="index.html">Ana S\u0259hif\u0259</a>
      <a href="tehsil.html" class="active">T\u0259hsil</a>
      <a href="index.html#services">Konsultasiya</a>
      <a href="b2b.html">Korporativ</a>
      <a href="blog.html">Blog</a>
      <a href="#registration" class="btn nav-cta">QEYD\u0130YYAT</a>
    </nav>"""
    c = c[:m.start()] + new_nav + c[m.end():]
    print('  + Desktop nav updated')

# Fix mobile nav too
mob_nav_pattern = r'<div class="mobile-nav"[^>]*>.*?</div>'
m2 = re.search(mob_nav_pattern, c, re.DOTALL)
if m2:
    mob = m2.group(0)
    if 'blog.html' not in mob:
        new_mob = """<div class="mobile-nav" id="mobileNav">
  <button class="mobile-nav-close" onclick="toggleMenu()"><svg viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg></button>
  <a href="index.html" onclick="toggleMenu()">Ana S\u0259hif\u0259</a>
  <a href="tehsil.html" onclick="toggleMenu()">T\u0259hsil</a>
  <a href="index.html#services" onclick="toggleMenu()">Konsultasiya</a>
  <a href="b2b.html" onclick="toggleMenu()">Korporativ</a>
  <a href="blog.html" onclick="toggleMenu()">Blog</a>
  <a href="#registration" class="btn btn-primary" onclick="toggleMenu()">QEYD\u0130YYAT</a>
</div>"""
        c = c[:m2.start()] + new_mob + c[m2.end():]
        print('  + Mobile nav updated')
    else:
        print('  = Mobile nav already has Blog')

with open('tehsil.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('  + Saved')

# Verify
with open('tehsil.html', 'rb') as f:
    raw2 = f.read()
c2 = raw2.decode('utf-8', errors='replace')
nav_m = re.search(r'<nav class="desktop-nav">.*?</nav>', c2, re.DOTALL)
if nav_m:
    print('Verified nav:', 'blog.html' in nav_m.group(0))
