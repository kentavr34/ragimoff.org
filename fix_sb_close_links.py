#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Добавить в JS каждого HTML-файла книги:
- закрытие сайдбара при клике на любую ссылку внутри него (мобильный)
- закрытие при нажатии Escape
"""
import glob, os

BASE = r"C:\Users\SAM\Desktop\sayt2\klinik-psixiatriya"

# Вставляем сразу после определения функции toggleSb
OLD = """function toggleSb(){
  document.getElementById('sb').classList.toggle('on');
  document.getElementById('ov').classList.toggle('on');
}"""

NEW = """function toggleSb(){
  var sb=document.getElementById('sb'), ov=document.getElementById('ov');
  sb.classList.toggle('on'); ov.classList.toggle('on');
}
function closeSb(){
  var sb=document.getElementById('sb'), ov=document.getElementById('ov');
  if(sb) sb.classList.remove('on');
  if(ov) ov.classList.remove('on');
}
// Закрыть сайдбар при клике по любой ссылке внутри (мобильный)
var sbNav=document.querySelector('#sb nav');
if(sbNav){
  sbNav.addEventListener('click',function(e){
    if(window.innerWidth<960){
      var a=e.target.closest('a');
      if(a) setTimeout(closeSb, 80);
    }
  });
}
// Закрыть по Escape
document.addEventListener('keydown',function(e){
  if(e.key==='Escape') closeSb();
});"""

files = sorted(glob.glob(os.path.join(BASE, "*.html")))
updated = 0

for fpath in files:
    with open(fpath, encoding='utf-8') as f:
        html = f.read()
    if OLD in html and 'closeSb' not in html:
        html = html.replace(OLD, NEW, 1)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html)
        updated += 1

print(f"Обновлено: {updated} файлов")
