# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Fix qanunlar.html - remove last Playfair reference
with open('qanunlar.html', 'rb') as f:
    raw = f.read()
c = raw.decode('utf-8', errors='replace')

# Remove inline Playfair in element styles
replacements = [
    ("font-family:'Playfair Display', serif;", ""),
    ("font-family: 'Playfair Display', serif;", ""),
    ("font-family:\\'Playfair Display\\', serif;", ""),
]
for old, new in replacements:
    c = c.replace(old, new)

# Also try with regex
c = re.sub(r"font-family:['\"]?Playfair Display['\"]?, serif;?", "", c)

remaining = c.count('Playfair')
print(f'qanunlar.html: Playfair remaining = {remaining}')
with open('qanunlar.html', 'w', encoding='utf-8') as f:
    f.write(c)

# Fix xidmetler.html - check what's there
with open('xidmetler.html', 'r', encoding='utf-8') as f:
    c = f.read()
print(f'xidmetler.html size: {len(c)}')
print('Has header:', '<header>' in c)
print('Has body:', '<body>' in c)
print('First 500 chars:')
print(c[:500])
