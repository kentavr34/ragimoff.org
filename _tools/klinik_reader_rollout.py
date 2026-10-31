"""Раскат читалки reader-pages.js (A−/A+, бумага/ночь, ←/→ и свайп) на все страницы «Клинической психиатрии» (4 языка).
Образец — 02-6A2-sizofreniya-spektri.html и 6A20.html, «ок» Кенана 31.10.2026. Идемпотентно: страницы с reader-pages.js пропускаются."""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent / 'klinik-psixiatriya'
PRE = ('<script>try{var t=localStorage.getItem("rd-theme");if(t)document.documentElement.setAttribute("data-rd",t);'
       'var f=localStorage.getItem("rd-fs");if(f)document.documentElement.style.setProperty("--rd-k",(f/1.1).toFixed(3))}catch(e){}</script>\n')
TAG = '<script src="/books/reader/reader-pages.js?v=20261031b" defer></script>\n'
n = skip = bad = 0
for p in sorted(ROOT.rglob('*.html')):
    s = p.read_text(encoding='utf-8')
    if 'reader-pages.js' in s:
        skip += 1
        continue
    if s.count('</head>') != 1 or s.count('</body>') != 1:
        bad += 1
        print('skip structure', p.relative_to(ROOT))
        continue
    s = s.replace('</head>', PRE + '</head>', 1).replace('</body>', TAG + '</body>', 1)
    p.write_text(s, encoding='utf-8')
    n += 1
print('patched', n, 'already', skip, 'bad', bad)
