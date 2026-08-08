# -*- coding: utf-8 -*-
"""Fix tehsil.html nav (add Blog link) and check haqqimda footer"""
import sys, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# ===== FIX TEHSIL.HTML =====
print('[tehsil.html]')
with open('tehsil.html', 'rb') as f:
    raw = f.read()
c = raw.decode('utf-8', errors='replace')

# Find desktop nav and add Blog link before QEYDİYYAT
# Pattern: looking for the nav-cta link
old_nav_cta = '<a href="tehsil.html#registration" class="btn nav-cta">'
if old_nav_cta in c:
    # Check if Blog is already in nav
    nav_section = c[c.find('<nav class="desktop-nav">'):c.find('</nav>')+6]
    if 'blog.html' not in nav_section.lower():
        # Insert Blog link before the nav-cta button
        c = c.replace(
            old_nav_cta,
            '<a href="blog.html">Blog</a>\n      ' + old_nav_cta,
            1
        )
        print('  + Blog link added to desktop nav')
    else:
        print('  = Blog already in desktop nav')

# Also fix mobile nav
old_mob_nav_cta = '<a href="tehsil.html#registration" class="btn btn-primary" onclick="toggleMenu()">'
if old_mob_nav_cta in c:
    mob_nav_start = c.find('<div class="mobile-nav"')
    mob_nav_end = c.find('</div>', mob_nav_start) + 6
    mob_section = c[mob_nav_start:mob_nav_end]
    if 'blog.html' not in mob_section.lower():
        c = c.replace(
            old_mob_nav_cta,
            '<a href="blog.html" onclick="toggleMenu()">Blog</a>\n  ' + old_mob_nav_cta,
            1
        )
        print('  + Blog link added to mobile nav')

with open('tehsil.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('  + Saved\n')

# ===== CHECK HAQQIMDA FOOTER =====
print('[haqqimda.html]')
with open('haqqimda.html', 'r', encoding='utf-8') as f:
    c = f.read()

ft_match = re.search(r'<footer[^>]*>.*?</footer>', c, re.DOTALL)
if ft_match:
    ft = ft_match.group(0)
    has_4col = 'grid-template-columns:2fr 1fr 1fr 1fr' in ft
    print(f'  Footer found, 4-col={has_4col}, size={len(ft)}')
    if not has_4col:
        print('  ! Footer needs upgrade - re-run fix_all_pages approach')
else:
    print('  ! Footer not found')

# Check for Playfair remaining
playfair_count = c.count('Playfair')
print(f'  Playfair references: {playfair_count}')

print('\nDone.')
