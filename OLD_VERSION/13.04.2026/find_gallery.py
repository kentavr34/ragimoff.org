# -*- coding: utf-8 -*-
"""Find and fix cert gallery in tehsil.html"""
import sys, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

with open('tehsil.html', 'rb') as f:
    raw = f.read()
c = raw.decode('utf-8', errors='replace')

# Find all gallery sections - look for img with cert images
cert_imgs = [(m.start(), m.group(0)) for m in re.finditer(r'<img[^>]+cert[^>]+>', c, re.IGNORECASE)]
print(f'Found {len(cert_imgs)} cert images')
if cert_imgs:
    first_img = cert_imgs[0][0]
    print('First cert img context:')
    # Look for the parent container
    # Find the nearest div before this img
    div_before = c.rfind('<div', 0, first_img)
    print(repr(c[div_before:first_img+300]))

# Also find the testimony/carousel pattern with multiple images
print()
# Find grid/flex containers for images
for m in re.finditer(r'display:\s*(?:flex|grid)[^;]*;[^"]*"[^>]*>\s*(?:\s*<img|\s*<a[^>]*>\s*<img)', c, re.DOTALL):
    print('Image container:', repr(m.group(0)[:200]))
    print('  at pos:', m.start())
    print()
