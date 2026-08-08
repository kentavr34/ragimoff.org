import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

design_system = {
    'fonts': 'https://fonts.googleapis.com/css2?family=Playfair+Display',
    'mobile_nav': '.mobile-nav.open',
    'id_mobile': 'mobileNav'
}

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    has_playfair = design_system['fonts'] in content
    has_inter = 'family=Inter' in content
    has_noto = 'family=Noto+Sans' in content
    has_mobile_open = 'classList.toggle(\'open\')' in content or '.open' in content
    has_mobile_show = '.show' in content
    
    print(f"--- {file} ---")
    print(f"  Playfair: {'OK' if has_playfair else 'MISSING'}")
    print(f"  Noto Sans: {'OK' if has_noto else 'MISSING'}")
    print(f"  Inter: {'PRESENT (REDUNDANT)' if has_inter else 'OK'}")
    print(f"  Mobile Nav: {'Uses .open' if has_mobile_open else 'MISSING .open'}")
    if has_mobile_show:
        print(f"  WARNING: Found '.show' class (potential conflict)")
    print("\n")
