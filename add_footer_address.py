#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""На всех страницах добавляем кликабельный адрес с иконкой "проложить маршрут"
между .footer-desc и .social-links. Если адрес уже есть — обновляем."""
import re, os, glob, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = r'C:\Users\SAM\Desktop\sayt2'
MAPS_URL = 'https://www.google.com/maps/search/?api=1&query=Caspian+Business+Center+Baku+AZ1065'

ADDRESS_BLOCKS = {
    'az': (
        f'<a class="footer-address" href="{MAPS_URL}" target="_blank" rel="noopener" '
        f'aria-label="Xəritədə baxın və yol göstərişləri">'
        f'<svg class="fa-pin" width="12" height="12" viewBox="0 0 24 24" fill="var(--bnb-gold,#E6B44A)">'
        f'<path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>'
        f'</svg>'
        f'<span class="fa-text">AZ1065, Bakı şəhəri, Caspian Business Center, 9-cu mərtəbə</span>'
        f'<svg class="fa-dir" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        f'<path d="M14 4l6 8-6 8M20 12H4"/>'
        f'</svg>'
        f'</a>'
    ),
    'ru': (
        f'<a class="footer-address" href="{MAPS_URL}" target="_blank" rel="noopener" '
        f'aria-label="Открыть на карте и проложить маршрут">'
        f'<svg class="fa-pin" width="12" height="12" viewBox="0 0 24 24" fill="var(--bnb-gold,#E6B44A)">'
        f'<path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>'
        f'</svg>'
        f'<span class="fa-text">AZ1065, г. Баку, Caspian Business Center, 9 этаж</span>'
        f'<svg class="fa-dir" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        f'<path d="M14 4l6 8-6 8M20 12H4"/>'
        f'</svg>'
        f'</a>'
    ),
    'en': (
        f'<a class="footer-address" href="{MAPS_URL}" target="_blank" rel="noopener" '
        f'aria-label="Open in maps and get directions">'
        f'<svg class="fa-pin" width="12" height="12" viewBox="0 0 24 24" fill="var(--bnb-gold,#E6B44A)">'
        f'<path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>'
        f'</svg>'
        f'<span class="fa-text">AZ1065, Baku, Caspian Business Center, 9th floor</span>'
        f'<svg class="fa-dir" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        f'<path d="M14 4l6 8-6 8M20 12H4"/>'
        f'</svg>'
        f'</a>'
    ),
}

# Insertion: after </p>.footer-desc and before <div class="social-links">
DESC_TO_SOCIAL = re.compile(
    r'(<p class="footer-desc">[^<]*</p>)\s*(<div class="social-links">)',
    re.DOTALL
)

def get_lang(fp):
    if '/ru/' in fp.replace('\\', '/'): return 'ru'
    if '/en/' in fp.replace('\\', '/'): return 'en'
    return 'az'

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

    # Skip if already has new address link
    if 'class="footer-address"' in html and 'fa-dir' in html:
        continue

    lang = get_lang(fp)
    addr_html = ADDRESS_BLOCKS[lang]

    # Replace existing <p class="footer-address">...</p> if present
    p_addr_pat = re.compile(r'<p class="footer-address">.*?</p>', re.DOTALL)
    if p_addr_pat.search(html):
        html2 = p_addr_pat.sub(addr_html, html, 1)
        if html2 != html:
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(html2)
            modified += 1
            print(f'UPD  {os.path.relpath(fp, ROOT)}')
            continue

    # Otherwise insert between footer-desc and social-links
    new_html, n = DESC_TO_SOCIAL.subn(r'\1\n              ' + addr_html + r'\n              \2', html, count=1)
    if n > 0:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(new_html)
        modified += 1
        print(f'ADD  {os.path.relpath(fp, ROOT)}')

print(f'\nTotal: {modified}')
