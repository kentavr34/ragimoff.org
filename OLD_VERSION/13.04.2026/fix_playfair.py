# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
with open('haqqimda.html', 'r', encoding='utf-8') as f:
    c = f.read()
old = "font-family:'Playfair Display',serif"
new = "font-family:'Inter',-apple-system,sans-serif"
c = c.replace(old, new)
with open('haqqimda.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('Fixed. Remaining Playfair:', c.count('Playfair'))
