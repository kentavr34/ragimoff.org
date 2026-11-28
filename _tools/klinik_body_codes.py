# -*- coding: utf-8 -*-
"""28.11.2026: те же правки текста, что в базе (EN_v85 / AZ_v64 / RU_v81 / TR_v62, D:/Projects/_MEMORY/tools/dx_body_code_fix.py):
код и название в скобках текста раздела = шапке расстройства (6B82, 7A21–7A26, 8A05.0, 6E20). Правит страницы книги
books/klinik-psixiatriya/<язык>/*.html; снимки /az/ /ru/ пересобирает build_static.py.
  python _tools/klinik_body_codes.py [--dry]"""
import glob, io, os, sys
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ALL = [("DSM-5-TR: F50.81)", "DSM-5-TR: F50.810–F50.819)")]
R = {"en": [("DSM-5-TR: G47.10 Hypersomnolence Disorder", "DSM-5-TR: F51.11 Hypersomnolence Disorder")],
     "az": [("DSM-5-TR: G47.10 Hypersomnolence Disorder", "DSM-5-TR: F51.11 Hipersomnolens pozuntusu"),
            ("(ing. XBT-11: 7A21–7A26", "(XBT-11: 7A21–7A26"),
            ("6E20 Mental and Behavioural Disorders Associated with Pregnancy, Childbirth or the Puerperium",
             "6E20 Hamiləlik, doğuş və ya zahılıq dövrü ilə əlaqəli psixi və ya davranış pozuntuları, psixotik simptomsuz")],
     "ru": [("DSM-5-TR: G47.10 Расстройство гиперсомнолентности", "DSM-5-TR: F51.11 Расстройство гиперсомнолентности"),
            ("8A05.0 Primary Tics or Tic Disorders", "8A05.0 Первичные тики или тикозные расстройства"),
            ("6E20 Mental and Behavioural Disorders Associated with Pregnancy, Childbirth or the Puerperium",
             "6E20 Психические и поведенческие расстройства, связанные с беременностью, родами или послеродовым периодом, без психотических симптомов")],
     "tr": [("DSM-5-TR: G47.10 Hypersomnolence Disorder", "DSM-5-TR: F51.11 Hipersomnolans Bozukluğu"),
            ("8A05.0 Primary Tics or Tic Disorders", "8A05.0 Primer tikler veya tik bozuklukları"),
            ("6E20 Mental and Behavioural Disorders Associated with Pregnancy, Childbirth or the Puerperium",
             "6E20 Gebelik, doğum veya lohusalık ile ilişkili ruhsal veya davranışsal bozukluklar, psikotik belirtisiz")]}
n = 0
for L, pairs in R.items():
    for f in sorted(glob.glob(os.path.join(D, "books", "klinik-psixiatriya", L, "*.html"))):
        t = io.open(f, encoding="utf-8", newline="").read()
        t2 = t
        for old, new in ALL + pairs:
            t2 = t2.replace(old, new)
        if t2 != t:
            n += 1
            print(L, os.path.basename(f))
            if "--dry" not in sys.argv:
                io.open(f, "w", encoding="utf-8", newline="").write(t2)
print("страниц:", n)
