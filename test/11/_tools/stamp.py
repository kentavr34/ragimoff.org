"""Номер версии к стилям и скриптам — чтобы телефон не показывал старые файлы. Запуск из test/11 перед публикацией: python _tools/stamp.py"""
import io, re, time

v = time.strftime('%m%d%H%M')
p = 'index.html'
t = io.open(p, encoding='utf-8').read()
t, a = re.subn(r'(assets/css/site\.css)(\?v=\d+)?', r'\1?v=' + v, t)
t, b = re.subn(r'(assets/js/site\.js)(\?v=\d+)?', r'\1?v=' + v, t)
io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
p = 'assets/js/site.js'
t = io.open(p, encoding='utf-8').read()
t, c = re.subn(r"(from '\./content\.js)(\?v=\d+)?'", r"\1?v=" + v + "'", t)
t, d = re.subn(r"(['\"]\./light\.js)(\?v=\d+)?(['\"])", r"\1?v=" + v + r"\3", t)
io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
t = io.open(p, encoding='utf-8').read()
t, e = re.subn(r"(from '\./reg\.js)(\?v=\d+)?'", r"\1?v=" + v + "'", t)
io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
import os
for pg, js in (('program.html', 'page-program'),):
    if os.path.exists(pg):
        x = io.open(pg, encoding='utf-8').read()
        x = re.sub(r'(assets/css/site\.css)(\?v=\d+)?', r'\1?v=' + v, x); x = re.sub(r'(assets/js/' + js + r'\.js)(\?v=\d+)?', r'\1?v=' + v, x)
        io.open(pg, 'w', encoding='utf-8', newline='\n').write(x)
for js in ('chrome', 'page-program'):
    f = 'assets/js/' + js + '.js'
    if os.path.exists(f):
        x = io.open(f, encoding='utf-8').read()
        x = re.sub(r"(from '\./[a-z-]+\.js)(\?v=\d+)?'", r"\1?v=" + v + "'", x)
        io.open(f, 'w', encoding='utf-8', newline='\n').write(x)
print('версия', v, '| css', a, 'js', b, 'content', c, 'light', d)

# перед публикацией: отступы только из шкалы (канон N22 / 15.5)
import subprocess, sys
r = subprocess.run([sys.executable, '_tools/css_scale.py', 'check'], capture_output=True, text=True, encoding='utf-8', errors='replace')
if r.returncode:
    print('ВНИМАНИЕ:', r.stdout.strip(), '— выполните: python _tools/css_scale.py fix')

# все страницы и все сценарии новой версии (оболочки внутренних страниц, блоки) — та же метка
import glob
for pg in glob.glob('*.html'):
    x = io.open(pg, encoding='utf-8').read()
    y = re.sub(r'(assets/(?:css|js)/[\w-]+\.(?:css|js))(\?v=\d+)?', r'\1?v=' + v, x)
    if y != x:
        io.open(pg, 'w', encoding='utf-8', newline='\n').write(y)
for f in glob.glob('assets/js/*.js'):
    x = io.open(f, encoding='utf-8').read()
    y = re.sub(r"(from '\./[\w-]+\.js)(\?v=\d+)?'", r"\1?v=" + v + "'", x)
    y = re.sub(r"const V = '\d+';", "const V = '" + v + "';", y)
    if y != x:
        io.open(f, 'w', encoding='utf-8', newline='\n').write(y)
