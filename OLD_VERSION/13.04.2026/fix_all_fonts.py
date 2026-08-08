# -*- coding: utf-8 -*-
"""Fix Playfair Display font references in all HTML pages"""
import sys, re, os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE = os.path.dirname(os.path.abspath(__file__))

ALL_HTML = [f for f in os.listdir(BASE) if f.endswith('.html') and not f.startswith('cert')]

REPLACEMENTS = [
    ("font-family: 'Playfair Display', serif", "font-family: 'Inter', -apple-system, sans-serif"),
    ('font-family: "Playfair Display", serif', "font-family: 'Inter', -apple-system, sans-serif"),
    ("font-family:'Playfair Display',serif", "font-family:'Inter',-apple-system,sans-serif"),
    ("font-family: 'Playfair Display'", "font-family: 'Inter', -apple-system, sans-serif"),
]

for fn in sorted(ALL_HTML):
    path = os.path.join(BASE, fn)
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        c = f.read()
    
    orig = c.count('Playfair')
    if orig == 0:
        continue
    
    # Remove Playfair from Google Fonts import
    c = re.sub(
        r'<link href="https://fonts\.googleapis\.com/css2\?family=Playfair[^"]*" rel="stylesheet"\s*/>\s*\n?',
        '',
        c
    )
    
    for old, new in REPLACEMENTS:
        c = c.replace(old, new)
    
    remaining = c.count('Playfair')
    print(f'{fn}: {orig} -> {remaining} Playfair refs')
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)

print('\nAll done.')
