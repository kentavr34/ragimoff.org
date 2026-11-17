# -*- coding: utf-8 -*-
"""Названия в меню, оглавлениях и описаниях страниц «Клинической психиатрии» AZ на сайте (17.11.2026), как в AZ_v38:
Turett → Turet (фр. Tourette; Qwen), HA20 «Ağrılı penetrasiya cinsi pozuntusu» → «Cinsi ağrı-penetrasiya pozuntusu» (ВОЗ EN/RU/TR).
Только книги klinik-psixiatriya (AZ) на сайте; копия файла перед правкой — _agent/bak_names_1117/.
  python _tools/klinik_names_1117.py [--dry]"""
import glob, io, os, re, shutil, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(D)
dry = "--dry" in sys.argv
R = [
    (re.compile(r"TURETT(?=[^A-ZƏÖÜĞŞÇİa-z]|$)"), "TURET"),
    (re.compile(r"Turett(?=[^a-zəöüğşçı]|[a-zəöüğşçı])"), "Turet"),
    (re.compile(r"Ağrılı penetrasiya cinsi pozuntusu"), "Cinsi ağrı-penetrasiya pozuntusu"),
    (re.compile(r"ağrılı penetrasiya cinsi pozuntusu"), "cinsi ağrı-penetrasiya pozuntusu"),
    (re.compile(r"AĞRILI PENETRASİYA CİNSİ POZUNTUSU"), "CİNSİ AĞRI-PENETRASİYA POZUNTUSU"),
]
files = sorted(set(glob.glob("az/read/klinik-psixiatriya/*.html") + glob.glob("books/klinik-psixiatriya/az/*.html")
                   + glob.glob("books/klinik-psixiatriya/*.json") + glob.glob("books/klinik-psixiatriya/*.html")))
tot, ch = 0, 0
for f in files:
    t = io.open(f, encoding="utf-8").read()
    n = t
    for rx, rep in R:
        n, k = rx.subn(rep, n)
        tot += k
    if n != t:
        ch += 1
        if not dry:
            b = os.path.join("_agent", "bak_names_1117", f)
            os.makedirs(os.path.dirname(b), exist_ok=True)
            if not os.path.exists(b):
                shutil.copy2(f, b)
            io.open(f + ".new", "w", encoding="utf-8", newline="\n").write(n)
            os.replace(f + ".new", f)
print("файлов", len(files), "изменено", ch, "замен", tot, "(проба)" if dry else "")
