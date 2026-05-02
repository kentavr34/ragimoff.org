#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Сравнить заголовки глав из нового DOCX с текущим сайтом.
Найти изменённые названия, термины.
"""
import zipfile, re

DOCX = r"D:\BOOKS\FINAL\kp_new\KLINIK_PSIXIATRIYA.docx"

# ─── Читаем XML ──────────────────────────────────────────────────────────────
with zipfile.ZipFile(DOCX) as z:
    with z.open("word/document.xml") as f:
        xml = f.read().decode("utf-8")

# Разбиваем на параграфы
paras_raw = re.split(r'</w:p>', xml)
paragraphs = []
for p in paras_raw:
    # Определяем стиль параграфа
    style_m = re.search(r'<w:pStyle w:val="([^"]+)"', p)
    style = style_m.group(1) if style_m else ""
    t = re.sub(r'<[^>]+>', '', p)
    t = re.sub(r'\s+', ' ', t).strip()
    if t:
        paragraphs.append((style, t))

# ─── Найти все BÖLMƏ заголовки и их следующие строки ─────────────────────────
BOLME_RE = re.compile(r'^BÖLM[ƏE]\s*(\d+)\s*$', re.IGNORECASE)

print("=" * 70)
print("СТРУКТУРА ГЛАВ В НОВОМ DOCX:")
print("=" * 70)

chapters_new = []
i = 0
while i < len(paragraphs):
    style, text = paragraphs[i]
    m = BOLME_RE.match(text.strip())
    if m:
        num = int(m.group(1))
        # Следующий непустой параграф = подзаголовок главы
        subtitle = ""
        for j in range(i+1, min(i+5, len(paragraphs))):
            s2, t2 = paragraphs[j]
            if t2.strip() and not BOLME_RE.match(t2.strip()):
                subtitle = t2.strip()
                break
        chapters_new.append((num, subtitle[:100]))
        print(f"  BÖLMƏ {num:2d}: {subtitle[:90]}")
    i += 1

# ─── Текущие заголовки на сайте ──────────────────────────────────────────────
import os, glob
BASE = r"C:\Users\SAM\Desktop\sayt2\klinik-psixiatriya"

print("\n" + "=" * 70)
print("ТЕКУЩИЕ ЗАГОЛОВКИ НА САЙТЕ (h2 после h-bolme):")
print("=" * 70)

H2_RE  = re.compile(r'<h2[^>]*>([^<]+)</h2>')
BOLME_H1 = re.compile(r'<h1[^>]*class="h-bolme"[^>]*>BÖLM[ƏE]\s*(\d+)</h1>')

site_chapters = []
for fpath in sorted(glob.glob(os.path.join(BASE, "bolme-*.html"))):
    slug = os.path.basename(fpath)
    with open(fpath, encoding='utf-8') as f:
        html = f.read()
    m_num = BOLME_H1.search(html)
    if not m_num:
        continue
    num = int(m_num.group(1))
    # найти первый h2 после h-bolme
    after = html[m_num.end():]
    m_h2 = H2_RE.search(after)
    title = m_h2.group(1).strip() if m_h2 else "?"
    # убрать добавленные нами коды (6A00–6A0Z · ...)
    title_clean = re.sub(r'^[0-9A-Z]{4,}[–-][0-9A-Z]{4,}\s*[·•]\s*', '', title)
    site_chapters.append((num, slug, title_clean))
    print(f"  BÖLMƏ {num:2d} [{slug}]: {title_clean}")

# ─── Сравнение ───────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("РАЗЛИЧИЯ (новый DOCX vs сайт):")
print("=" * 70)

site_dict = {num: title for num, slug, title in site_chapters}
new_dict  = {num: title for num, title in chapters_new}

diffs = []
for num in sorted(set(list(site_dict.keys()) + list(new_dict.keys()))):
    site_t = site_dict.get(num, "НЕТ НА САЙТЕ")
    new_t  = new_dict.get(num, "НЕТ В DOCX")
    if site_t != new_t:
        diffs.append((num, site_t, new_t))
        print(f"\n  BÖLMƏ {num}:")
        print(f"    Сайт:  {site_t}")
        print(f"    DOCX:  {new_t}")

if not diffs:
    print("  Различий не найдено.")

print(f"\nГлав в DOCX: {len(chapters_new)}")
print(f"Глав на сайте: {len(site_chapters)}")
