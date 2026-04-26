# -*- coding: utf-8 -*-
"""
Обновляет .desktop-nav на всех HTML страницах:
- Ana Səhifə → dropdown с Haqqımda
- Təhsil → dropdown с программами + Qanunlar
- Konsultasiya → dropdown с направлениями
- Korporativ, Blog — без dropdown
"""
import re, pathlib, glob

ROOT = pathlib.Path(r"C:\Users\SAM\Desktop\sayt2")

def build_nav(active_page):
    """Build new nav with optional active class on top-level link."""
    def cls(page):
        return ' class="nav-active"' if page == active_page else ''

    return f'''<nav class="desktop-nav">
          <div class="nav-item">
            <a href="index.html"{cls('index')}>Ana Səhifə</a>
            <ul class="nav-dropdown">
              <li><a href="haqqimda.html">Haqqımda</a></li>
            </ul>
          </div>
          <div class="nav-item">
            <a href="tehsil.html"{cls('tehsil')}>Təhsil</a>
            <ul class="nav-dropdown">
              <li><a href="program-umumi.html">Ümumi Psixologiya</a></li>
              <li><a href="program-klinik.html">Klinik Psixologiya DPO</a></li>
              <li><a href="program-praktikum.html">Psixoterapiya Praktikumu</a></li>
              <li><a href="qanunlar.html">Qanuni Əsaslar</a></li>
            </ul>
          </div>
          <div class="nav-item">
            <a href="xidmetler.html"{cls('xidmetler')}>Konsultasiya</a>
            <ul class="nav-dropdown">
              <li><a href="aile-terapiyasi.html">Ailə Terapiyası</a></li>
              <li><a href="aile-terapiyasi-usaq.html">Aile-Uşaq Terapiyası</a></li>
              <li><a href="depressiya.html">Depressiya</a></li>
              <li><a href="panik-ataklar.html">Panik Ataklar</a></li>
              <li><a href="sosial-fobiya.html">Sosial Fobiya</a></li>
              <li><a href="enurez.html">Gecə Enurezi</a></li>
            </ul>
          </div>
          <a href="b2b.html"{cls('b2b')}>Korporativ</a>
          <a href="blog.html"{cls('blog')}>Blog</a>
          <a href="tehsil.html#registration" class="nav-cta">QEYDİYYAT</a>
        </nav>'''

# Map filename to active-page key
PAGE_MAP = {
    'index.html': 'index',
    'haqqimda.html': 'index',  # haqqimda highlights index
    'tehsil.html': 'tehsil',
    'program-umumi.html': 'tehsil',
    'program-klinik.html': 'tehsil',
    'program-praktikum.html': 'tehsil',
    'qanunlar.html': 'tehsil',
    'xidmetler.html': 'xidmetler',
    'aile-terapiyasi.html': 'xidmetler',
    'aile-terapiyasi-usaq.html': 'xidmetler',
    'depressiya.html': 'xidmetler',
    'panik-ataklar.html': 'xidmetler',
    'sosial-fobiya.html': 'xidmetler',
    'enurez.html': 'xidmetler',
    'b2b.html': 'b2b',
    'blog.html': 'blog',
}
# Blog article pages - all highlight blog
for f in glob.glob(str(ROOT / "blog-*.html")):
    PAGE_MAP[pathlib.Path(f).name] = 'blog'

# Pattern matches the entire <nav class="desktop-nav">...</nav> block (multiline)
NAV_RE = re.compile(r'<nav class="desktop-nav">.*?</nav>', re.DOTALL)

count = 0
for f in glob.glob(str(ROOT / "*.html")):
    fname = pathlib.Path(f).name
    page_key = PAGE_MAP.get(fname, 'index')
    s = open(f, encoding='utf-8').read()
    new_nav = build_nav(page_key)
    s2, n = NAV_RE.subn(new_nav, s, count=1)
    if n > 0 and s != s2:
        open(f, 'w', encoding='utf-8').write(s2)
        count += 1
        print(f"  {fname}")

print(f"Done. Updated {count} files.")
