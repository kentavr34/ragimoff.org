#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Делаем адрес кликабельным с иконкой "проложить маршрут" на всех страницах.
Добавляем margin-bottom чтобы оторвать от social links."""
import re, os, glob, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = r'C:\Users\SAM\Desktop\sayt2'

# Caspian Business Center, Baku — координаты из Google Maps
MAPS_URL = 'https://www.google.com/maps/search/?api=1&query=Caspian+Business+Center+Baku+AZ1065'

# Эталонная замена: вся строка <p class="footer-address">...</p> заменяется на ссылку
# Поддерживаем три языка по найденному тексту
PATTERNS_AND_REPLACEMENTS = [
    # AZ
    (
        re.compile(
            r'<p class="footer-address">\s*<svg[^>]*>.*?</svg>\s*'
            r'(AZ\d{4},\s*Bakı şəhəri[^<]+)\s*</p>',
            re.DOTALL
        ),
        f'<a class="footer-address" href="{MAPS_URL}" target="_blank" rel="noopener" '
        f'aria-label="Xəritədə baxın və yol göstərişləri">'
        f'<svg class="fa-pin" width="12" height="12" viewBox="0 0 24 24" fill="var(--bnb-gold)">'
        f'<path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>'
        f'</svg>'
        f'<span class="fa-text">\\1</span>'
        f'<svg class="fa-dir" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        f'<path d="M14 4l6 8-6 8M20 12H4"/>'
        f'</svg>'
        f'</a>'
    ),
    # RU (адрес уже переведённый — оставим тот же текст или возьмём «Баку, Каспий Бизнес Центр»)
    (
        re.compile(
            r'<p class="footer-address">\s*<svg[^>]*>.*?</svg>\s*'
            r'((?:AZ\d{4},?\s*)?(?:г\.\s*)?Баку[^<]+)\s*</p>',
            re.DOTALL | re.IGNORECASE
        ),
        f'<a class="footer-address" href="{MAPS_URL}" target="_blank" rel="noopener" '
        f'aria-label="Открыть на карте и проложить маршрут">'
        f'<svg class="fa-pin" width="12" height="12" viewBox="0 0 24 24" fill="var(--bnb-gold)">'
        f'<path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>'
        f'</svg>'
        f'<span class="fa-text">\\1</span>'
        f'<svg class="fa-dir" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        f'<path d="M14 4l6 8-6 8M20 12H4"/>'
        f'</svg>'
        f'</a>'
    ),
    # EN
    (
        re.compile(
            r'<p class="footer-address">\s*<svg[^>]*>.*?</svg>\s*'
            r'((?:AZ\d{4},?\s*)?Baku[^<]+)\s*</p>',
            re.DOTALL
        ),
        f'<a class="footer-address" href="{MAPS_URL}" target="_blank" rel="noopener" '
        f'aria-label="Open in maps and get directions">'
        f'<svg class="fa-pin" width="12" height="12" viewBox="0 0 24 24" fill="var(--bnb-gold)">'
        f'<path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>'
        f'</svg>'
        f'<span class="fa-text">\\1</span>'
        f'<svg class="fa-dir" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        f'<path d="M14 4l6 8-6 8M20 12H4"/>'
        f'</svg>'
        f'</a>'
    ),
]

modified = 0
all_files = (
    glob.glob(os.path.join(ROOT, '*.html')) +
    glob.glob(os.path.join(ROOT, 'ru', '*.html')) +
    glob.glob(os.path.join(ROOT, 'en', '*.html'))
)
for fp in all_files:
    if 'template.html' in fp:
        continue
    with open(fp, encoding='utf-8') as f:
        html = f.read()
    orig = html
    for pat, repl in PATTERNS_AND_REPLACEMENTS:
        html = pat.sub(repl, html)
    if html != orig:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(html)
        modified += 1
        print(f'OK   {os.path.relpath(fp, ROOT)}')

print(f'\nTotal modified: {modified}')
