#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_all.py — три задачи:
1. Убрать "Bl.X —" из подписей глав в сайдбаре (во всех 31 файлах)
2. Добавить диапазон кодов к h2 заголовку каждой болме-страницы
3. Слить K L İ N İ K + P S İ X İ A T R İ Y A в одну строку в index.html
"""
import re, os, glob

BASE = r"C:\Users\SAM\Desktop\sayt2\klinik-psixiatriya"

# ─── ШАГ 1: собрать данные из каждого bolme файла ────────────────────────────
# chapter title = первый h2 после h1.h-bolme
# code range    = XBT-11 строка вида:  <span class="icd">6A00</span>–6A0Z

H2_RE      = re.compile(r'<h2[^>]*>([^<]+)</h2>')
XBT_RE     = re.compile(
    r'XBT-11[^<]*<span class="icd">([^<]+)</span>[–—\-]([A-Z0-9]+)',
    re.IGNORECASE
)
# альтернативный вариант — ищем только первую icd пару в xbt-line
XBT_LINE_RE = re.compile(
    r'<div class="xbt-line">.*?<span class="icd">([^<]+)</span>[–—\-]([A-Z0-9]+)',
    re.IGNORECASE | re.DOTALL
)

chapters = []   # [(slug, code_range, full_title), ...]

bolme_files = sorted(glob.glob(os.path.join(BASE, "bolme-*.html")))

for fpath in bolme_files:
    slug = os.path.splitext(os.path.basename(fpath))[0]
    with open(fpath, encoding='utf-8') as f:
        html = f.read()

    # найти первый h2 ПОСЛЕ h1.h-bolme
    m_bolme_pos = re.search(r'<h1[^>]*class="h-bolme"[^>]*>', html)
    h2_title = ""
    if m_bolme_pos:
        after = html[m_bolme_pos.end():]
        m_h2 = H2_RE.search(after)
        if m_h2:
            h2_title = m_h2.group(1).strip()

    # найти диапазон кодов (XBT-11 строка)
    code_range = ""
    m_xbt = XBT_RE.search(html)
    if m_xbt:
        code_range = f"{m_xbt.group(1)}–{m_xbt.group(2)}"
    else:
        m_xbt2 = XBT_LINE_RE.search(html)
        if m_xbt2:
            code_range = f"{m_xbt2.group(1)}–{m_xbt2.group(2)}"

    if h2_title:
        chapters.append((slug, code_range, h2_title))
        print(f"{slug}: h2='{h2_title}'  code='{code_range}'")

print(f"\nВсего глав: {len(chapters)}")

# ─── ШАГ 2: собрать disorders из каждого bolme файла ─────────────────────────
DISORDER_RE = re.compile(
    r'<h1\s+id="([^"]+)"\s+class="h-disorder"[^>]*>'
    r'\s*<span class="icd">([^<]+)</span>\s*([^<\n]+)',
    re.IGNORECASE
)

disorders = {}   # slug -> [(anchor, icd_code, title), ...]
for fpath in bolme_files:
    slug = os.path.splitext(os.path.basename(fpath))[0]
    with open(fpath, encoding='utf-8') as f:
        html = f.read()
    dis = DISORDER_RE.findall(html)
    disorders[slug] = [(a.strip(), c.strip(), t.strip()) for a, c, t in dis]

# ─── ШАГ 3: перестроить sidebar HTML ─────────────────────────────────────────
PREAMBLE = """<div class="nav-item" data-slug="index">
  <a href="index.html" class="nav-link" data-slug="index">
    <span>Titul + Önsöz</span>
  </a>
</div>
<div class="nav-item" data-slug="giris">
  <a href="giris.html" class="nav-link" data-slug="giris">
    <span>Giriş</span>
  </a>
</div>
<div class="nav-item" data-slug="giris-yekun">
  <a href="giris-yekun.html" class="nav-link" data-slug="giris-yekun">
    <span>Kitab haqqında</span>
  </a>
</div>
<div class="nav-item" data-slug="mugeddime">
  <a href="mugeddime.html" class="nav-link" data-slug="mugeddime">
    <span>Müqəddimə</span>
  </a>
</div>
<div class="nav-item" data-slug="abbreviatur">
  <a href="abbreviatur.html" class="nav-link" data-slug="abbreviatur">
    <span>Abbreviaturalar</span>
  </a>
</div>"""

chapter_nav_parts = []
for slug, code_range, h2_title in chapters:
    dis_list = disorders.get(slug, [])
    label = h2_title  # теперь без "Bl.X —"
    nav_code_html = f"<span class='nav-code'>{code_range}</span>" if code_range else ""

    if dis_list:
        sub_links = "\n".join(
            f'    <a href="{slug}.html#{anchor}" class="nav-sub-link">'
            f'<span class="sub-code">{icd}</span>'
            f'<span class="sub-name">{title}</span></a>'
            for anchor, icd, title in dis_list
        )
        chapter_nav_parts.append(
            f'<div class="nav-item nav-has-sub" data-slug="{slug}">\n'
            f'  <a href="{slug}.html" class="nav-link is-bolme" data-slug="{slug}">\n'
            f'    {nav_code_html}\n'
            f'    <span>{label}</span>\n'
            f'  </a>\n'
            f'  <button class="nav-toggle" aria-label="Aç/bağla" '
            f'onclick="toggleSub(this)" tabindex="-1">▶</button>\n'
            f'  <div class="nav-sub">\n'
            f'{sub_links}\n'
            f'  </div>\n'
            f'</div>'
        )
    else:
        chapter_nav_parts.append(
            f'<div class="nav-item" data-slug="{slug}">\n'
            f'  <a href="{slug}.html" class="nav-link is-bolme" data-slug="{slug}">\n'
            f'    {nav_code_html}\n'
            f'    <span>{label}</span>\n'
            f'  </a>\n'
            f'</div>'
        )

new_nav_content = PREAMBLE + "\n" + "\n".join(chapter_nav_parts)

# JS (как было)
JS_INJECT = """<script>
(function(){
  var path = location.pathname.split('/').pop().replace('.html','');
  document.querySelectorAll('.nav-has-sub').forEach(function(item){
    if(item.dataset.slug === path){ item.classList.add('open'); }
  });
  document.querySelectorAll('.nav-link').forEach(function(a){
    if(a.dataset.slug === path) a.classList.add('active');
  });
})();
function toggleSub(btn){
  var item = btn.closest('.nav-has-sub');
  item.classList.toggle('open');
}
</script>"""

SIDEBAR_RE = re.compile(r'(<aside[^>]*class="sidebar"[^>]*>.*?<nav>)(.*?)(</nav>)', re.DOTALL)

# ─── ШАГ 4: обновить все HTML файлы ──────────────────────────────────────────
all_html = sorted(glob.glob(os.path.join(BASE, "*.html")))
updated = 0

for fpath in all_html:
    with open(fpath, encoding='utf-8') as f:
        html = f.read()

    original = html

    # 4a. заменить сайдбар
    def replace_nav(m):
        return m.group(1) + "\n" + new_nav_content + "\n" + m.group(3)

    html = SIDEBAR_RE.sub(replace_nav, html)

    # 4b. JS — убедиться что в конце тела
    if '<script>' not in html or 'toggleSub' not in html:
        html = html.replace('</body>', JS_INJECT + '\n</body>', 1)

    if html != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html)
        updated += 1

print(f"Обновлено сайдбаров: {updated} файлов")

# ─── ШАГ 5: добавить код к h2 на каждой bolme-странице ───────────────────────
h2_updated = 0
for slug, code_range, h2_title in chapters:
    if not code_range:
        print(f"  ПРОПУСК {slug}: нет code_range")
        continue

    fpath = os.path.join(BASE, f"{slug}.html")
    with open(fpath, encoding='utf-8') as f:
        html = f.read()

    original = html

    # найти первый h2 после h1.h-bolme и обновить его текст
    # Паттерн: <h2 id="...">TITLE</h2> (первый после h1.h-bolme)
    # Заменяем только если текст ещё не содержит код
    new_heading = f"{code_range} · {h2_title}"

    # regex: ищем первый h2 сразу после h1.h-bolme
    # Используем позиционирование через split
    m_bolme = re.search(r'<h1[^>]*class="h-bolme"[^>]*>', html)
    if not m_bolme:
        print(f"  ПРОПУСК {slug}: нет h1.h-bolme")
        continue

    before = html[:m_bolme.end()]
    after  = html[m_bolme.end():]

    # заменяем первый h2 в after
    H2_EXACT_RE = re.compile(r'(<h2[^>]*>)(' + re.escape(h2_title) + r')(</h2>)')
    def replace_h2(m):
        return m.group(1) + new_heading + m.group(3)

    new_after, count = H2_EXACT_RE.subn(replace_h2, after, count=1)

    if count:
        html = before + new_after
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html)
        h2_updated += 1
        print(f"  h2 обновлён: {slug}: '{new_heading}'")
    else:
        # может уже обновлён
        if code_range in after:
            print(f"  h2 уже содержит код: {slug}")
        else:
            print(f"  h2 НЕ найден: {slug}")

print(f"\nОбновлено h2: {h2_updated} файлов")

# ─── ШАГ 6: исправить заголовок в index.html ─────────────────────────────────
idx = os.path.join(BASE, "index.html")
with open(idx, encoding='utf-8') as f:
    idx_html = f.read()

original_idx = idx_html

# Ищем K L İ N İ K и P S İ X İ A T R İ Y A на двух отдельных строках
# Варианты: через <br>, через \n внутри элемента, или разные <span>/<p>
idx_html = re.sub(
    r'K\s*L\s*[İI]\s*N\s*[İI]\s*K\s*\n\s*P\s*S\s*[İI]\s*X\s*[İI]\s*A\s*T\s*R\s*[İI]\s*Y\s*A',
    'K L İ N İ K  P S İ X İ A T R İ Y A',
    idx_html
)
idx_html = re.sub(
    r'(K\s+L\s+[İI]\s+N\s+[İI]\s+K)<br\s*/?>\s*(P\s+S\s+[İI]\s+X\s+[İI]\s+A\s+T\s+R\s+[İI]\s+Y\s+A)',
    r'K L İ N İ K  P S İ X İ A T R İ Y A',
    idx_html
)

if idx_html != original_idx:
    with open(idx, 'w', encoding='utf-8') as f:
        f.write(idx_html)
    print("index.html: заголовок объединён в одну строку")
else:
    print("index.html: паттерн не найден — проверяем вручную")
    # покажем контекст вокруг KLINIK
    pos = idx_html.find('K L İ N İ K')
    if pos >= 0:
        print(repr(idx_html[pos:pos+120]))

print("\nГотово.")
