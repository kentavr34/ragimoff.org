# -*- coding: utf-8 -*-
"""Разовое закрытие чтения английских версий четырёх книг (слово Кенана 21.11.2026).
Паспорт книги получает "closed": ["en"]; английские главы уходят с сайта в локальный архив _archive/ (в git не попадает);
в каталоге магазина кнопка «Читать» становится неактивной. Оглавление в паспорте остаётся полным.
  python -X utf8 _tools/close_en_read_1121.py"""
import io, os, sys, json, glob, shutil, subprocess
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import libcommon
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
ARCH = "_archive/en_closed_2026-11-21"
for bid, lang in sorted(libcommon.CLOSED_READ):
    pj = "books/%s/book.json" % bid
    P = json.load(io.open(pj, encoding="utf-8"))
    if bid == "virus-viny" and len(P["toc"].get("en", [])) < 10:      # после отрывка от 21.11 вернуть полное оглавление
        old = json.loads(subprocess.run(["git", "show", "ffffdfb:" + pj], capture_output=True).stdout.decode("utf-8"))
        P["toc"]["en"] = old["toc"]["en"]
    P["closed"] = sorted(set(P.get("closed", [])) | {lang})
    io.open(pj, "w", encoding="utf-8", newline="\n").write(json.dumps(P, ensure_ascii=False, indent=1) + "\n")
    dst = os.path.join(ARCH, bid, lang)
    os.makedirs(dst, exist_ok=True)
    files = glob.glob("books/%s/%s/*.html" % (bid, lang))
    for f in files:
        shutil.move(f, os.path.join(dst, os.path.basename(f)))
    print("%s %s: глав в оглавлении %d, файлов убрано в архив %d" % (bid, lang, len(P["toc"].get(lang, [])), len(files)))
for lang in ("en",):
    p = "data/shop/index.%s.json" % lang
    J = json.load(io.open(p, encoding="utf-8"))
    n = 0
    for g in J["groups"]:
        for it in g["items"]:
            if (it["id"], lang) in libcommon.CLOSED_READ:
                it["read"], it["closed"] = False, True
                n += 1
    io.open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(J, ensure_ascii=False, indent=1) + "\n")
    print(p, "— закрытых книг:", n)
