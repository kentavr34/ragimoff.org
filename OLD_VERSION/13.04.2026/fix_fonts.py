# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def fix_fonts(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        c = f.read()
    
    orig_count = c.count('Playfair')
    
    # Remove Playfair Display from Google Fonts link - target the link tag itself
    c = re.sub(
        r"<link href=\"https://fonts\.googleapis\.com/css2\?family=Playfair[^\"]*\" rel=\"stylesheet\"\s*/>\n?",
        "",
        c
    )
    
    # Replace Playfair Display font-family declarations in CSS with Inter
    c = c.replace("font-family: 'Playfair Display', serif", "font-family: 'Inter', -apple-system, sans-serif")
    c = c.replace('font-family: "Playfair Display", serif', "font-family: 'Inter', -apple-system, sans-serif")
    
    new_count = c.count('Playfair')
    print(f'{filename}: Playfair references {orig_count} -> {new_count}')
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(c)

for fn in ['blog.html', 'haqqimda.html']:
    fix_fonts(fn)

print('Done')
