# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
with open('tehsil.html', 'rb') as f:
    raw = f.read()
c = raw.decode('utf-8', errors='replace')
nav_start = c.find('<nav class="desktop-nav">')
nav_end = c.find('</nav>', nav_start) + 7
nav = c[nav_start:nav_end]
print('Desktop NAV:')
print(nav[:800])
print()
print('Blog in nav:', 'blog.html' in nav.lower())
