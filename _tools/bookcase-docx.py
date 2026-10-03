#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""bookcase-docx — правки регистра/пунктуации в мастер-файлах книги (Word).

Классы правок (по реестру CASE-REGISTER.tsv):
  аббревиатура   — чужая/латинская аббревиатура в скобке → канон версии
                   (PMDD→ПМДР, FTD→ЛВД, ADHD→DDHP/DEHB, IED→İED; англ. цитаты
                   и подстрочные латинские глоссы не трогаются);
  двойные пробелы — «код  НАЗВАНИЕ» в оглавлении → один пробел.

НЕ трогает: капс обложки/колонтитула и капс-заголовки глав — это вёрстка
мастера (так в обоих наборах мастеров, BOOKS/Psychiatrist и в репо);
структуру и стили не меняет — правится только текст runs.

Запуск:
    python _tools/bookcase-docx.py --src "<папка с оригиналами>" \
        --dst "D:/Документы/ZFreud/_align/book_docx"
"""
from __future__ import annotations

import argparse
import csv
import os
import re
import shutil
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import casecheck as cc  # noqa: E402

LANGS = {"Klinicheskaya_Psikhiatriya.docx": "ru",
         "Klinik_Psixiatriya.docx": "az",
         "Clinical_Psychiatry.docx": "en",
         "Klinik_Psikiyatri.docx": "tr"}

RE_CITATION = re.compile(r"(Cochrane|Pediatrics|Neurology|Lancet|JAMA|BMJ|"
                         r"et al\.|Psychiatry \d|Rev \d|doi:|https?://|"
                         r"Am J|J Child|Sleep \d)")
RE_ABBR = re.compile(r"\(([^()\s]{2,10})\)")
RE_DBL = re.compile(r"  +")


def para_text(p):
    return "".join(r.text for r in p.runs)


def fix_para(p, lang, abbr, log, where):
    """Правит только текст runs (структуру и стили не трогает)."""
    changed = False
    full = para_text(p)
    is_cit = bool(RE_CITATION.search(full))
    cyr = len(re.findall(r"[А-Яа-яЁё]", full))
    for r in p.runs:
        t = r.text
        if not t:
            continue
        # 1) двойные пробелы внутри run
        if "  " in t:
            new = RE_DBL.sub(" ", t)
            if new != t:
                log.append((where, lang, "двойные пробелы",
                            re.sub(r"\s+", " ", t)[:60],
                            re.sub(r"\s+", " ", new)[:60]))
                t = new
                changed = True
        # 2) аббревиатуры в скобках внутри run
        if RE_ABBR.search(t):
            for m in reversed(list(RE_ABBR.finditer(t))):
                tok = m.group(1)
                canon = abbr[lang].get(cc.lang_lower(tok, lang))
                if not canon or canon == tok:
                    continue
                if is_cit or (lang == "ru" and cyr < 5):
                    continue
                pre = t[max(0, m.start() - 40):m.start()]
                if re.search(re.escape(canon) + r"\s*$", pre):
                    continue                 # латинская глосса после своего термина
                log.append((where, lang, "аббревиатура", m.group(0), "(" + canon + ")"))
                t = t[:m.start()] + "(" + canon + ")" + t[m.end():]
                changed = True
        if t != r.text:
            r.text = t
    return changed


def iter_paras(doc):
    yield from doc.paragraphs
    for tb in doc.tables:
        for row in tb.rows:
            for cell in row.cells:
                yield from cell.paragraphs
    for s in doc.sections:
        for pn in ("header", "footer", "first_page_header", "first_page_footer",
                   "even_page_header", "even_page_footer"):
            part = getattr(s, pn, None)
            if part is not None:
                yield from part.paragraphs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--dst", required=True)
    a = ap.parse_args()
    import docx

    _, abbr = cc.load_maps()
    os.makedirs(a.dst, exist_ok=True)
    log = []
    for name, lang in LANGS.items():
        src = os.path.join(a.src, name)
        if not os.path.exists(src):
            print("нет файла:", src)
            continue
        shutil.copy2(src, os.path.join(a.dst, name))     # оригинал — не перезаписываем
        d = docx.Document(src)
        n = 0
        for i, p in enumerate(iter_paras(d)):
            if fix_para(p, lang, abbr, log, f"{name}"):
                n += 1
        out = os.path.join(a.dst, os.path.splitext(name)[0] + "_FIXED.docx")
        d.save(out)
        print(f"{name} [{lang}]: абзацев изменено {n} → {os.path.basename(out)}")
    rep = os.path.join(a.dst, "_ПРАВКИ.tsv")
    with open(rep, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", quoting=csv.QUOTE_ALL)
        w.writerow(["файл", "язык", "класс", "было", "стало"])
        w.writerows(log)
    print(f"всего правок: {len(log)}; отчёт: {rep}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
