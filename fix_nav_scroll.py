#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix sidebar scroll position preservation:
- toggleSub: preserve sidebar scrollTop when expanding/collapsing nav items
- toggleSb:  save/restore scrollTop on mobile open/close
- closeSb:   save scrollTop before hiding
- Auto-scroll sidebar to active open chapter on page load
"""
import sys, io, os, glob, unicodedata

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r"C:\Users\SAM\Desktop\sayt2\klinik-psixiatriya"

OLD_TOGGLE_SUB = 'function toggleSub(btn){\n  var item = btn.closest(\'.nav-has-sub\');\n  item.classList.toggle(\'open\');\n}'
NEW_TOGGLE_SUB = ('function toggleSub(btn){\n'
                  '  var sb=document.getElementById(\'sb\');\n'
                  '  var top=sb?sb.scrollTop:0;\n'
                  '  var item=btn.closest(\'.nav-has-sub\');\n'
                  '  item.classList.toggle(\'open\');\n'
                  '  if(sb) requestAnimationFrame(function(){sb.scrollTop=top;});\n'
                  '}')

OLD_TOGGLE_SB = ('function toggleSb(){\n'
                 '  var sb=document.getElementById(\'sb\'), ov=document.getElementById(\'ov\');\n'
                 '  sb.classList.toggle(\'on\'); ov.classList.toggle(\'on\');\n'
                 '}')
NEW_TOGGLE_SB = ('var _sbScroll=0;\n'
                 'function toggleSb(){\n'
                 '  var sb=document.getElementById(\'sb\'),ov=document.getElementById(\'ov\');\n'
                 '  if(sb.classList.contains(\'on\')){\n'
                 '    _sbScroll=sb.scrollTop;\n'
                 '    sb.classList.remove(\'on\');\n'
                 '    if(ov) ov.classList.remove(\'on\');\n'
                 '  } else {\n'
                 '    sb.classList.add(\'on\');\n'
                 '    if(ov) ov.classList.add(\'on\');\n'
                 '    setTimeout(function(){sb.scrollTop=_sbScroll;},10);\n'
                 '  }\n'
                 '}')

OLD_CLOSE_SB = ('function closeSb(){\n'
                '  var sb=document.getElementById(\'sb\'), ov=document.getElementById(\'ov\');\n'
                '  if(sb) sb.classList.remove(\'on\');\n'
                '  if(ov) ov.classList.remove(\'on\');\n'
                '}')
NEW_CLOSE_SB = ('function closeSb(){\n'
                '  var sb=document.getElementById(\'sb\'),ov=document.getElementById(\'ov\');\n'
                '  if(sb){_sbScroll=sb.scrollTop;sb.classList.remove(\'on\');}\n'
                '  if(ov) ov.classList.remove(\'on\');\n'
                '}')

# Scroll sidebar to active chapter on page load
# Insert after the auto-expand IIFE
OLD_AUTO_EXPAND_END = ('  // Highlight active link\n'
                       '  document.querySelectorAll(\'.nav-link\').forEach(function(a){\n'
                       '    if(a.dataset.slug === path) a.classList.add(\'active\');\n'
                       '  });\n'
                       '})();')
NEW_AUTO_EXPAND_END = ('  // Highlight active link\n'
                       '  document.querySelectorAll(\'.nav-link\').forEach(function(a){\n'
                       '    if(a.dataset.slug === path) a.classList.add(\'active\');\n'
                       '  });\n'
                       '  // Scroll sidebar to show active chapter\n'
                       '  setTimeout(function(){\n'
                       '    var sb=document.getElementById(\'sb\');\n'
                       '    var open=sb&&sb.querySelector(\'.nav-has-sub.open\');\n'
                       '    if(sb&&open){\n'
                       '      var target=open.offsetTop-Math.round(sb.offsetHeight/3);\n'
                       '      sb.scrollTop=Math.max(0,target);\n'
                       '    }\n'
                       '  },80);\n'
                       '})();')

FIXES = [
    (OLD_TOGGLE_SUB, NEW_TOGGLE_SUB),
    (OLD_TOGGLE_SB,  NEW_TOGGLE_SB),
    (OLD_CLOSE_SB,   NEW_CLOSE_SB),
    (OLD_AUTO_EXPAND_END, NEW_AUTO_EXPAND_END),
]

total_files = 0
total_fixes = 0

for fpath in sorted(glob.glob(BASE + r'\bolme-*.html')):
    fname = os.path.basename(fpath)
    with open(fpath, encoding='utf-8') as f:
        html = f.read()
    html_n = unicodedata.normalize('NFC', html)
    changed = 0
    for old, new in FIXES:
        old_n = unicodedata.normalize('NFC', old)
        new_n = unicodedata.normalize('NFC', new)
        if old_n in html_n:
            html_n = html_n.replace(old_n, new_n, 1)
            changed += 1
        else:
            print(f'  MISS {fname}: {old[:50].strip()}')
    if changed:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html_n)
        print(f'  OK {fname}: {changed} fixes')
        total_files += 1
        total_fixes += changed

print(f'\nDone. {total_fixes} fixes in {total_files} files.')
