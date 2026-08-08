# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
for fn in ['enurez.html', 'blog-aile.html', 'index.html']:
    with open(fn, 'r', encoding='utf-8') as f:
        c = f.read()
    lb = c.count('logo-box')
    lb_css = '.logo-box {' in c
    old_logo = 'class="logo"' in c
    print(f'{fn}: logo-box mentions={lb}, has .logo-box CSS={lb_css}, old logo class={old_logo}')
