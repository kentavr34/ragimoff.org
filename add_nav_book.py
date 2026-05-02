#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Добавить пункт "Klinik Psixiatriya / Клиническая Психиатрия"
в дропдаун "Главная / Ana Səhifə" на всех страницах сайта.
"""
import glob, os

ROOT = r"C:\Users\SAM\Desktop\sayt2"

# ─── AZ файлы (корень + en/) ──────────────────────────────────────────────────
AZ_DESKTOP_OLD = '<li><a href="haqqimda.html">Haqqımda</a></li>'
AZ_DESKTOP_NEW = (
    '<li><a href="haqqimda.html">Haqqımda</a></li>\n'
    '              <li><a href="/klinik-psixiatriya/">Klinik Psixiatriya</a></li>'
)

AZ_MOBILE_OLD  = '<a href="index.html" onclick="toggleMenu()">Ana Səhifə</a>'
AZ_MOBILE_NEW  = (
    '<a href="index.html" onclick="toggleMenu()">Ana Səhifə</a>\n'
    '      <a href="/klinik-psixiatriya/" onclick="toggleMenu()">Klinik Psixiatriya</a>'
)

# ─── RU файлы (ru/) ──────────────────────────────────────────────────────────
RU_DESKTOP_OLD = '<li><a href="haqqimda.html">Обо мне</a></li>'
RU_DESKTOP_NEW = (
    '<li><a href="haqqimda.html">Обо мне</a></li>\n'
    '              <li><a href="/klinik-psixiatriya/">Клиническая Психиатрия</a></li>'
)

RU_MOBILE_OLD  = '<a href="index.html" onclick="toggleMenu()">Главная</a>'
RU_MOBILE_NEW  = (
    '<a href="index.html" onclick="toggleMenu()">Главная</a>\n'
    '      <a href="/klinik-psixiatriya/" onclick="toggleMenu()">Клиническая Психиатрия</a>'
)

def patch(fpath, replacements):
    with open(fpath, encoding='utf-8') as f:
        html = f.read()
    original = html
    for old, new in replacements:
        html = html.replace(old, new, 1)
    if html != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html)
        return True
    return False

# AZ — корень (исключаем ru/, en/, klinik-psixiatriya/)
az_files  = glob.glob(os.path.join(ROOT, "*.html"))
az_files += glob.glob(os.path.join(ROOT, "en", "*.html"))

az_updated = 0
for fpath in az_files:
    if patch(fpath, [(AZ_DESKTOP_OLD, AZ_DESKTOP_NEW), (AZ_MOBILE_OLD, AZ_MOBILE_NEW)]):
        az_updated += 1

print(f"AZ обновлено: {az_updated} файлов")

# RU — ru/
ru_files = glob.glob(os.path.join(ROOT, "ru", "*.html"))

ru_updated = 0
for fpath in ru_files:
    if patch(fpath, [(RU_DESKTOP_OLD, RU_DESKTOP_NEW), (RU_MOBILE_OLD, RU_MOBILE_NEW)]):
        ru_updated += 1

print(f"RU обновлено: {ru_updated} файлов")
print("Готово.")
