# -*- coding: utf-8 -*-
"""Переход 12.11.2026: версия 11 — корень сайта. Повторный запуск ничего не меняет.
 • сборщики читают прежний сайт из архива (только чтение): libcommon.OLD_SITE;
 • страницы открыты для поисковиков (снят noindex), кроме эскизов;
 • проверочные инструменты по умолчанию смотрят в корень локального сервера."""
import io, os, re, sys, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(D)
OLD = r'D:\Projects\Ragimoff\old_versions\2026-11-12_site_before_v11'
NEWLINE = 'ROOT = r"%s"   # прежний сайт: источник текстов и картинок, только чтение (с 12.11.2026 версия 11 — корень сайта)' % OLD
n = 0
for f in ["build_blog", "build_library", "build_library_legacy", "build_shop", "collect_images", "libcommon", "patch_data_1112b", "verify_data"]:
    p = "_tools/%s.py" % f
    s = io.open(p, encoding="utf-8").read()
    L = s.split("\n")
    for i, l in enumerate(L):
        if l.startswith("ROOT = os.path.abspath("):
            L[i] = NEWLINE
            n += 1
    io.open(p, "w", encoding="utf-8", newline="\n").write("\n".join(L))
p = "_tools/build_klinik.py"
s = io.open(p, encoding="utf-8").read()
a = 'SRC = os.path.abspath(os.path.join(D, "..", "..", "klinik-psixiatriya"))'
if a in s:
    s = s.replace(a, 'SRC = os.path.join(r"%s", "klinik-psixiatriya")   # прежняя книга на сайте — источник, только чтение' % OLD)
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
    n += 1
for p in ["_tools/pages_check.py", "_tools/form_check.py"]:
    s = io.open(p, encoding="utf-8").read()
    s2 = s.replace('"http://localhost:8812/test/11/"', '"http://localhost:8812/"').replace('rs["url"].split("/test/11/")[-1]', 'rs["url"].split("localhost:8812/")[-1]').replace("Запуск из test/11 (сервер: python -m http.server 8812 из корня сайта)", "Запуск из корня сайта (сервер: python -m http.server 8812 из корня сайта)")
    if s2 != s:
        io.open(p, "w", encoding="utf-8", newline="\n").write(s2)
        n += 1
for p in glob.glob("*.html") + ["_tools/make_shells.py"]:
    s = io.open(p, encoding="utf-8").read()
    s2 = re.sub(r'<meta name="robots" content="noindex,nofollow">\r?\n', "", s)
    if s2 != s:
        io.open(p, "w", encoding="utf-8", newline="\n").write(s2)
        n += 1
print("изменено мест:", n)
