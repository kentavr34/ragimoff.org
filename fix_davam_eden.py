#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Замена устаревших терминов 'Davam edən' на правильные азербайджанские."""
import os

BASE = r"C:\Users\SAM\Desktop\sayt2\klinik-psixiatriya"

CHANGES = [
    # (файл, старый текст, новый текст)

    # bolme-02: диагностический код F22
    ("bolme-02.html",
     "Davam edən sayıqlama pozuntusu",
     "Xroniki sayıqlama pozuntusu"),

    # bolme-02: подраздел "поддерживающая терапия" + id заголовка
    ("bolme-02.html",
     '<h3 id="davam-edən-saxlanma-müalicə" class="">Davam edən (saxlanma) müalicə</h3>',
     '<h3 id="dəstəkci-müalicə" class="">Dəstəkci müalicə</h3>'),

    # bolme-04: подраздел
    ("bolme-04.html",
     '<h3 id="davam-edən-və-saxlanma-müalicəsi" class="">Davam edən və saxlanma müalicəsi</h3>',
     '<h3 id="dəstəkci-müalicəsi" class="">Dəstəkci müalicəsi</h3>'),

    # bolme-05: два одинаковых подраздела (replace_all)
    ("bolme-05.html",
     '<h3 id="davam-edən-və-saxlanma-müalicə" class="">Davam edən və saxlanma müalicə</h3>',
     '<h3 id="dəstəkci-müalicə" class="">Dəstəkci müalicə</h3>'),

    # bolme-06: подраздел
    ("bolme-06.html",
     '<h3 id="davam-edən-və-saxlanma-müalicəsi" class="">Davam edən və saxlanma müalicəsi</h3>',
     '<h3 id="dəstəkci-müalicəsi" class="">Dəstəkci müalicəsi</h3>'),

    # bolme-01: симптом/мониторинг
    ("bolme-01.html",
     "Davam edən nəzarət",
     "Daimi nəzarət"),
]

for fname, old, new in CHANGES:
    fpath = os.path.join(BASE, fname)
    with open(fpath, encoding="utf-8") as f:
        html = f.read()
    count = html.count(old)
    if count:
        html = html.replace(old, new)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  {fname}: '{old[:50]}...' → замен: {count}")
    else:
        print(f"  {fname}: НЕ НАЙДЕНО: '{old[:60]}'")
