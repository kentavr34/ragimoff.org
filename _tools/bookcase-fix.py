#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""bookcase-fix — сплошной проход по книге «Klinik Psixiatriya» (az/ru/en/tr).

Классы правок (всё — по реестру CASE-REGISTER.tsv, канон берётся из casecheck):

  мета-заголовок   <title> и og:title: «раздел | Название книги»
  мета-описание    description / og:description: «Название книги — раздел»
  json-ld          название книги в JSON-LD
  подпись-заказа   data-order кнопки «Заказать»
  шапка-книги      подпись книги в шапке (bk-book__t)
  обложка          h1 обложки (bk-tp__title)
  крошка           текст крошки / пункта «пред/след» / оглавления — регистр по реестру
  пункт-меню       название раздела в меню — регистр по реестру
  заголовок        h2–h4 со строчной первой буквы
  аббревиатура     строчная аббревиатура в скобке (реестровые страницы)
  пунктуация       «( ( ( (», текст после </html>

Каждая правка — строкой «страница | язык | класс | было | стало» (в отчёт .tsv).

Запуск:
    python _tools/bookcase-fix.py --dry
    python _tools/bookcase-fix.py
    python _tools/bookcase-fix.py --scan      # только скан: что ещё осталось
"""
from __future__ import annotations

import argparse
import csv
import os
import re
import sys
from collections import Counter

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import casecheck as cc  # noqa: E402

ROOT = cc.ROOT
BOOK = cc.BOOK
REPORT = os.path.join(ROOT, "_tools", "bookcase-fix-report.tsv")

# классы слотов: regex → (группа с текстом, имя класса для отчёта)
SLOT_RX = [
    (re.compile(r'(<span class="bk-row__t">)(.*?)(</span>)', re.S), 2, "пункт-меню"),
    (re.compile(r'(<span class="bk-toc__t">)(.*?)((?:<span|</span>))', re.S), 2, "оглавление"),
    (re.compile(r'(<span class="bk-pn__t">)(.*?)(</span>)', re.S), 2, "пред/след"),
    (re.compile(r'(<nav class="bk-crumb"[^>]*>\s*<a href="[^"#]+">)(.*?)(</a>)', re.S), 2, "крошка"),
    (re.compile(r'(<span class="tc-(?:range|sc)">[^<]*</span><span>)(.*?)(</span>)', re.S), 2, "оглавление"),
    (re.compile(r'(<h1 class="bk-chead__h1">)(.*?)(</h1>)', re.S), 2, "заголовок"),
]
RE_H24 = re.compile(r'(<h([234])\b[^>]*>)(.*?)(</h\2>)', re.S)
RE_BOOK_SPAN = cc.RE_SLOT_BOOK
RE_TAIL = re.compile(r"(</html>)([\s\S]+)$")
RE_PAREN_MESS = re.compile(r"\((?:\s*\(){2,}\s*")

META_CLASS = {
    "slot:meta-title": "мета-заголовок",
    "slot:og-title": "мета-заголовок",
    "slot:meta-desc": "мета-описание",
    "slot:og-desc": "мета-описание",
    "slot:jsonld-name": "json-ld",
    "slot:data-order": "подпись-заказа",
    "slot:cover-title": "обложка",
    "slot:book-title": "шапка-книги",
}


def text_chunks(raw):
    """Текстовые куски без script/style и без тегов."""
    parts = re.split(r"(?is)<(script|style)\b[^>]*>.*?</\1\s*>", raw)
    out = []
    for i, p in enumerate(parts):
        if i % 2 == 1:
            continue
        out += re.split(r"(?s)<[^>]+>", p)
    return out


def log_add(changes, page, lang, cls, was, now):
    was1 = re.sub(r"\s+", " ", was).strip()
    now1 = re.sub(r"\s+", " ", now).strip()
    if len(was1) > 160:
        was1 = was1[:157] + "..."
    if len(now1) > 160:
        now1 = now1[:157] + "..."
    changes.append((page, lang, cls, was1, now1))


def fix_slots(out, lang, page, changes, names=None):
    """Регистр текстов слотов по реестру (канон «строчными, кроме первого слова»)."""
    for rx, gi, cls in SLOT_RX:
        def repl(m):
            body = m.group(gi)
            if "<" in body:
                return m.group(0)          # со вложенной разметкой не трогаем
            if names and cc.is_book_title(cc.txt(body), lang):
                new = names[lang]["index.html"]   # крошка «имя книги» — по реестру
            else:
                new = cc.norm_sent(body, lang)
            if new == body:
                return m.group(0)
            log_add(changes, page, lang, cls, body, new)
            return m.group(1) + new + m.group(3)
        out = rx.sub(repl, out)
    return out


def fix_headings(out, lang, page, changes):
    """h2–h4: первая буква со строчной → с прописной (кроме техтерминов вроде bvFTD)."""
    def repl(m):
        body = m.group(3)
        if "<" in body:
            return m.group(0)
        mm = re.match(r"([^\W\d_]+)", body, re.U)
        if not mm:
            return m.group(0)
        w = mm.group(1)
        if not w.islower() or len(w) < 3:
            return m.group(0)          # bvFTD, ЭЭГ и прочие — не трогаем
        new = body[:mm.start(1)] + cc.lang_upper1(w[0], lang) + body[mm.start(1) + 1:]
        log_add(changes, page, lang, "заголовок", body, new)
        return m.group(1) + new + m.group(4)
    out = RE_H24.sub(repl, out)
    # «— На 3 языках»: предлог внутри заголовка — со строчной
    def repl2(m):
        body = m.group(3)
        new = re.sub(r"—\s+На(?=\s+\d)", "— на", body)
        if new == body:
            return m.group(0)
        log_add(changes, page, lang, "заголовок", body, new)
        return m.group(1) + new + m.group(4)
    return RE_H24.sub(repl2, out)


def fix_abbr_slots(out, lang, page, changes):
    """Строчная аббревиатура в скобке → канон реестра (и снятие капса с имени)."""
    abbr = None

    def repl(m):
        nonlocal abbr
        if abbr is None:
            _, abbr = cc.load_maps()
        body = m.group(2)
        if "<" in body:
            return m.group(0)
        new = body
        for mm in re.finditer(r"\(([^()\s]{2,8})\)", body):
            tok = mm.group(1)
            canon = abbr[lang].get(cc.lang_lower(tok, lang))
            if canon and canon != tok:
                new = new.replace(mm.group(0), "(" + canon + ")", 1)
        if new != body:
            log_add(changes, page, lang, "аббревиатура", body, new)
            return m.group(1) + new + m.group(3)
        return m.group(0)
    return re.compile(r'(<span class="bk-row__t">)(.*?)(</span>)', re.S).sub(repl, out)


def process_page(path, lang, names, changes):
    raw = open(path, encoding="utf-8").read()
    out = raw
    page = os.path.basename(path)

    stats = Counter()

    def meta_log(kind, was, now):
        log_add(changes, page, lang, META_CLASS.get(kind, kind), was, now)

    out = cc.fix_book_meta(out, lang, page, names, stats, log=meta_log)

    def book_span(m):
        if m.group(2) != names[lang]["index.html"]:
            log_add(changes, page, lang, "шапка-книги", m.group(2), names[lang]["index.html"])
            return m.group(1) + names[lang]["index.html"] + m.group(3)
        return m.group(0)
    out = RE_BOOK_SPAN.sub(book_span, out)

    out = fix_abbr_slots(out, lang, page, changes)   # до norm_sent: (окр) → (ОКР)
    out = fix_slots(out, lang, page, changes, names)
    out = fix_headings(out, lang, page, changes)

    i = out.find("</html>")                          # мусор после </html>
    if i >= 0 and out[i + 7:].strip():
        log_add(changes, page, lang, "пунктуация", out[i + 7:].strip()[:80], "(удалено)")
        out = out[:i + 7] + "\n"

    def paren(m):
        log_add(changes, page, lang, "пунктуация", m.group(0), "(")
        return "("
    out = RE_PAREN_MESS.sub(paren, out)

    if out != raw:
        crlf = b"\r\n" in open(path, "rb").read(200000)
        data = out.replace("\n", "\r\n") if crlf else out
        open(path, "w", encoding="utf-8", newline="").write(data)
    return out != raw


def cmd_fix(a):
    names, _ = cc.load_maps()
    changes = []
    per = Counter()
    for lang in ("ru", "az", "en", "tr"):
        d = cc.folder(lang)
        n = 0
        for f in sorted(os.listdir(d)):
            if not f.endswith(".html"):
                continue
            k0 = len(changes)
            if process_page(os.path.join(d, f), lang, names, changes):
                n += 1
            for ch in changes[k0:]:
                per[(lang, ch[2])] += 1
        print(f"{lang}: файлов изменено {n}, правок {sum(1 for ch in changes if ch[1] == lang)}")
    print("классы правок:")
    for (lg, cls), n in sorted(per.items()):
        print(f"   {lg:3} {cls:14} {n}")
    os.makedirs(os.path.dirname(REPORT), exist_ok=True)
    with open(REPORT, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", quoting=csv.QUOTE_ALL)
        w.writerow(["страница", "язык", "класс", "было", "стало"])
        for row in changes:
            w.writerow(row)
    print(f"всего правок: {len(changes)}; отчёт: {REPORT}")
    return 0


def cmd_scan(a):
    """Скан по классам ошибок: сколько осталось."""
    names, _ = cc.load_maps()
    left = Counter()
    for lang in ("ru", "az", "en", "tr"):
        d = cc.folder(lang)
        for f in sorted(os.listdir(d)):
            if not f.endswith(".html"):
                continue
            raw = open(os.path.join(d, f), encoding="utf-8").read()
            page = os.path.basename(f)
            # мета-слоты
            v, _n = cc.check_book_meta(raw, lang, page, names)
            for it in v:
                left[(lang, "название-книги:" + it["where"])] += 1
            # слоты: строчная первая буква
            for rx, gi, cls in SLOT_RX:
                for m in rx.finditer(raw):
                    body = m.group(gi)
                    if "<" in body or not body.strip():
                        continue
                    t = cc.txt(body)
                    if t[:1].islower() and not re.match(r"^[a-z]{1,2}[A-Z]", t):
                        left[(lang, cls + ":строчная")] += 1
                    if cc.norm_sent(body, lang) != body:
                        left[(lang, cls + ":регистр")] += 1
            i = raw.find("</html>")
            if i >= 0 and raw[i + 7:].strip():
                left[(lang, "пунктуация:хвост-после-html")] += 1
            if RE_PAREN_MESS.search(raw):
                left[(lang, "пунктуация:скобки")] += 1
            # пунктуация и слипшиеся слова — в текстовых кусках (без script/style)
            for ch in text_chunks(raw):
                if re.search(r"\S  +\S", ch):
                    left[(lang, "пунктуация:двойной-пробел")] += 1
                for mm in re.finditer(r"\S [.,;!?](?=\s|$)", ch):
                    # « : » в соотношениях («1,2 : 1», «Kişi : qadın») — стиль книги
                    if not mm.group(0)[0].isdigit():
                        left[(lang, "пунктуация:пробел-перед-знаком")] += 1
                for mm in re.finditer(r"(?<=[a-zа-яё])\.(?=[А-ЯЁA-Z][a-zа-яё])", ch):
                    left[(lang, "пунктуация:нет-пробела-после-точки")] += 1
                for mm in re.finditer(r"[а-яё]{3,}(?<![а-яё]-)[А-ЯЁ][а-яё]{3,}", ch):
                    left[(lang, "слипшиеся-слова")] += 1
    tot = sum(left.values())
    print(f"осталось нарушений по классам: {tot}")
    for (lg, cls), n in sorted(left.items()):
        print(f"   {lg:3} {cls:32} {n}")
    return 1 if tot else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true", help="не писать файлы")
    ap.add_argument("--scan", action="store_true", help="только скан остатков")
    ap.add_argument("--book", default=None, help="каталог книги (по умолчанию klinik-psixiatriya)")
    a = ap.parse_args()
    if a.book:
        cc.BOOK = a.book
    if a.scan:
        return cmd_scan(a)
    if a.dry:
        print("(dry — файлы не меняются; для dry смотрите count через --scan)")
        return 0
    return cmd_fix(a)


if __name__ == "__main__":
    sys.exit(main())
