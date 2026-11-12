# -*- coding: utf-8 -*-
"""Картинки внутренних страниц: всё, на что ссылаются data/**/*.json (/images/…), копируется в assets/img/site/ — новая версия не зависит от старых папок.
Запуск: python collect_images.py — показывает число файлов, объём и отсутствующие."""
import io, os, re, glob, shutil, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ROOT = r"D:\Projects\Ragimoff\old_versions\2026-11-12_site_before_v11"   # прежний сайт: источник текстов и картинок, только чтение (с 12.11.2026 версия 11 — корень сайта)
used = set()
for fn in glob.glob(os.path.join(D, "data", "*", "*.json")):
    used |= set(re.findall(r'/images/[^" <>\n\t\\]+?\.(?:jpg|jpeg|png|webp|gif|svg)', io.open(fn, encoding="utf-8").read(), flags=re.I))
n = size = 0
miss = []
for u in sorted(used):
    src = os.path.join(ROOT, u.lstrip("/").replace("/", os.sep))
    dst = os.path.join(D, "assets", "img", "site", u[len("/images/"):].replace("/", os.sep))
    if not os.path.isfile(src):
        miss.append(u)
        continue
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if not os.path.isfile(dst) or os.path.getsize(dst) != os.path.getsize(src):
        shutil.copy2(src, dst)
    n += 1
    size += os.path.getsize(src)
print("картинок: %d, объём: %.1f МБ, нет файла: %d" % (n, size / 1e6, len(miss)))
for m in miss:
    print("  нет:", m)
big = sorted(((os.path.getsize(os.path.join(ROOT, u.lstrip('/'))), u) for u in used if os.path.isfile(os.path.join(ROOT, u.lstrip('/')))), reverse=True)[:8]
for s, u in big:
    print("  %.0f КБ %s" % (s / 1e3, u))
