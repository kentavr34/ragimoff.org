# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()
pattern = 'class="logo"'
idx = c.find(pattern)
while idx != -1:
    print(f'pos {idx}:', repr(c[max(0,idx-30):idx+80]))
    idx = c.find(pattern, idx+1)
