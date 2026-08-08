# -*- coding: utf-8 -*-
"""Replace logo image with text wordmark across all HTML files"""
import sys, re, os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE = os.path.dirname(os.path.abspath(__file__))

# New text logo HTML
TEXT_LOGO = '''<a href="index.html" class="logo-box">
      <span class="logo-text">RAGIMOFF<em>.</em><br><span class="logo-sub">Psixologiya M\u0259kt\u0259bi</span></span>
    </a>'''

# Also a version with just RAGIMOFF. for compact contexts
TEXT_LOGO_COMPACT = '<a href="index.html" class="logo-box"><span class="logo-text">RAGIMOFF<em>.</em><span class="logo-sub">Psixologiya M\u0259kt\u0259bi</span></span></a>'

# Pattern to match the old logo-box with image
logo_pattern = re.compile(
    r'<a href="index\.html" class="logo-box">\s*<img[^>]+alt="RAGIMOFF Logo"[^>]*>\s*</a>',
    re.DOTALL
)

html_files = [f for f in os.listdir(BASE) if f.endswith('.html')]
changed = 0

for fn in sorted(html_files):
    path = os.path.join(BASE, fn)
    with open(path, 'rb') as f:
        raw = f.read()
    c = raw.decode('utf-8', errors='replace')
    
    new_c, n = logo_pattern.subn(TEXT_LOGO_COMPACT, c)
    
    if n > 0:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_c)
        print(f'{fn}: replaced {n} logo(s)')
        changed += 1
    
print(f'\nTotal files updated: {changed}')
