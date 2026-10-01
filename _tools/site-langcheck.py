#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""site-langcheck — языковые утечки и регистр на страницах сайта (класс «g»).

Правило владельца: основной текст языковой версии — на языке версии,
иноязычное написание допустимо только в скобках или кавычках; термины — по
реестру регистра (`CASE-REGISTER.tsv`).

Что считается утечкой:
  * AZ/EN-страницы: кириллическая «простыня» — два и более кириллических
    слова подряд вне скобок и кавычек. Исключение — переключатель языков
    («Русская версия»), он называет язык его же письмом;
  * RU-страницы: азербайджанские буквы (ə ğ ı İ ö ü ş ç) вне скобок;
    исключения — «Azərbaycan dili» в переключателе и имена из списка ниже;
  * RU/EN-страницы: английская «простыня» — два и более латинских слова
    подряд вне скобок. Коды (DSM-5, ICD-11), бренды и имена собственные —
    не утечка, они в списке ALLOW.

Запуск:
    python _tools/site-langcheck.py                 # сводка
    python _tools/site-langcheck.py --tsv FILE      # строки аудита
"""
from __future__ import annotations

import argparse
import csv
import html as H
import io
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RE_SCRIPT = re.compile(r"<(script|style|noscript)\b[^>]*>[\s\S]*?</\1>", re.I)
RE_COMMENT = re.compile(r"<!--[\s\S]*?-->")
RE_TITLE = re.compile(r"<title[\s\S]*?</title>", re.I)
RE_TAG = re.compile(r"<[^>]+>")
CUT = re.compile(r"\([^()]{0,160}\)|«[^»]{0,160}»|„[^“]{0,160}“|\u201c[^\u201d]{0,160}\u201d")
# библиография и списки источников: язык оригинала — норма (та же граница, что
# у книжного langcheck.py: «библиография сохраняет язык оригинала»), иначе
# 10 000 «утечек» — это названия книг и издательств в списке литературы
RE_SOURCES = re.compile(
    r'<(ol|ul|div|section|aside)\b[^>]*class="[^"]*'
    r'(art-sources|sources|references|bibliography|istochnik|menbe|mənbə)'
    r'[^"]*"[^>]*>[\s\S]*?</\1>', re.I)
CYR_RUN = re.compile(r"[А-Яа-яЁёІіЇїЄєҐґ]{2,}(?:[\s,;:—-]+[А-Яа-яЁёІіЇїЄєҐґ]{2,})+")
AZ_CHARS = re.compile(r"[əğıöüşçƏĞİÖÜŞÇ]")   # без ASCII I: он есть в любом латинском тексте
LAT_RUN = re.compile(r"\b[A-Za-z][a-z]{2,}(?:\s+[A-Za-z][a-z]{2,}){2,}\b")
RE_YEAR = re.compile(r"\b(19|20)\d\d\b")

# легальные вкрапления: коды, имена, бренды, языковой переключатель
ALLOW = re.compile(
    r"(RAGIMOFF|IPAS|DSM|ICD|WHO|CBT|EMDR|OKP|OKB|PTSD|XBT|MKБ|МКБ|WhatsApp|Telegram|Instagram|YouTube|Facebook|TikTok|LinkedIn|iPhone|iPad|macOS|iOS|GitHub|PayPal|Zoom|Space|Center|Business|Sankt|Peterburq|Azərbaycan dili|Azərbaycan|English|Русская версия|"
    r"Ragimov|Rəhimov|Kenan|Kənan|Freud|Stark|Walker|Bowlby|Ainsworth|Gottman|Toastmasters|BetterHelp|Talkspace|NavPress|BirBank|TamKart|BolKart|WorldKart|Neuro|"
    # имена собственные документов и организаций (в тексте-версии допустимы)
    r"Children and Young People|National Institute for Health and Care Excellence|Global Training and Consulting|Psychology School)",
    re.I)


def pages():
    out = []
    for d in ("", "ru", "en"):
        base = os.path.join(ROOT, d) if d else ROOT
        for name in sorted(os.listdir(base)):
            if not name.endswith(".html") or name.startswith("_"):
                continue
            if not os.path.isfile(os.path.join(base, name)):
                continue
            out.append(((d + "/" + name) if d else name, d or "az"))
    return out


def text_of(s: str) -> str:
    s = RE_COMMENT.sub(" ", s)
    s = RE_SCRIPT.sub(" ", s)
    s = RE_TITLE.sub(" ", s)
    s = RE_SOURCES.sub(" ", s)
    s = RE_TAG.sub(" ", s)
    return re.sub(r"\s+", " ", H.unescape(s))


def scan():
    rows = []
    for rel, lang in pages():
        s = open(os.path.join(ROOT, rel.replace("/", os.sep)), encoding="utf-8", errors="replace").read()
        t = CUT.sub(" ", text_of(s))
        if lang in ("az", "en"):
            for m in CYR_RUN.finditer(t):
                # «Русская версия» — подпись переключателя языков: язык назван
                # своим письмом, это не утечка (ALLOW)
                if ALLOW.search(m.group(0)):
                    continue
                rows.append((rel, lang, "g", "кириллица в тексте версии " + lang.upper(),
                             m.group(0)[:60], "язык версии"))
        if lang == "ru":
            for m in AZ_CHARS.finditer(t):
                seg = t[max(0, m.start() - 30):m.start() + 30]
                if ALLOW.search(seg):
                    continue
                rows.append((rel, lang, "g", "азербайджанская буква в русском тексте",
                             seg.strip()[:60], "язык версии"))
        if lang == "ru":
            for m in LAT_RUN.finditer(t):
                w = m.group(0)
                if ALLOW.search(w):
                    continue
                if RE_YEAR.search(t[m.start():m.start() + 90]):
                    continue          # цитата с годом: «Doherty, 2019» — источник
                if RE_YEAR.search(t[m.start():m.start() + 90]):
                    continue
                rows.append((rel, lang, "g", "английская фраза вне скобок",
                             w[:60], "в скобки/кавычки или перевод"))
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tsv", default=None)
    ap.add_argument("--top", type=int, default=40)
    args = ap.parse_args()

    rows = scan()
    print(f"страниц: {len(pages())}; строк: {len(rows)}")
    import collections
    c = collections.Counter(r[3] for r in rows)
    for k, v in c.most_common():
        print(f"  {v:4d}  {k}")
    for r in rows[:args.top]:
        print(" | ".join(r))
    if args.tsv:
        with open(args.tsv, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f, delimiter="\t")
            w.writerow(["страница", "язык", "класс", "причина", "было", "стало"])
            w.writerows(rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
