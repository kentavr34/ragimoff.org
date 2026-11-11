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
print('версия', v, '| css', a, 'js', b, 'content', c, 'light', d)

# перед публикацией: отступы только из шкалы (канон N22 / 15.5)
import subprocess, sys
r = subprocess.run([sys.executable, '_tools/css_scale.py', 'check'], capture_output=True, text=True, encoding='utf-8', errors='replace')
if r.returncode:
    print('ВНИМАНИЕ:', r.stdout.strip(), '— выполните: python _tools/css_scale.py fix')
