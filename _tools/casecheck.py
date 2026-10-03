#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""casecheck — реестр регистра книги и проверка по нему.

Идея владельца: «регистр — где и как идут — важно вести правильный реестр».
То есть регистр книги задаётся НЕ по месту в тексте, а реестром `CASE-REGISTER.tsv`
(рядом с EDITORIAL-STANDARDS.md): термины Ru/Az/En/Tr, канонический регистр,
где применяется и почему. Правки делаются только по реестру, проверка — тем же
реестром.

Колонки реестра:
    термин_ru | термин_az | термин_en | термин_tr | канонический_регистр |
    где_применяется | примечание

Канонический регистр (одна из четырёх формулировок):
    «строчными, кроме первого слова» — названия расстройств, глав, разделов;
    «ВСЕ ЗАГЛАВНЫЕ (аббревиатура)»   — аббревиатуры в скобках-расшифровках;
    «С прописной (имя собственное)»  — авторы, руководства, шкалы-имена;
    «как в оригинале (латиница в скобках)» — латинское название/код.

Запуск:
    python _tools/casecheck.py build                 # собрать реестр из дерева
    python _tools/casecheck.py fix --dry             # правки по реестру (показать)
    python _tools/casecheck.py fix                   # правки по реестру
    python _tools/casecheck.py check --out DIR       # проверка: нарушений 0
    python _tools/casecheck.py check --book <путь>   # проверить другую книгу
"""
from __future__ import annotations

import argparse
import csv
import html as H
import io
import json
import os
import re
import sys
from collections import Counter, defaultdict

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, "klinik-psixiatriya")
REGISTER_TSV = os.path.join(ROOT, "CASE-REGISTER.tsv")
REGISTRY_PAGES = {"abbreviatur.html", "terminoloji-luget.html"}

RULE_SENT = "строчными, кроме первого слова"
RULE_ABBR = "ВСЕ ЗАГЛАВНЫЕ (аббревиатура)"
RULE_NAME = "С прописной (имя собственное)"
RULE_LAT = "как в оригинале (латиница в скобках)"

# ── аббревиатуры: смысловой ключ → форма по версиям ─────────────────────────
# ключ: (ru, az, en, tr, расшифровка_ru)
ABBR_ROWS = [
    ("ADHD", "СДВГ", "DDHP", "ADHD", "DEHB", "синдром дефицита внимания с гиперактивностью"),
    ("OCD", "ОКР", "OKP", "OCD", "OKB", "обсессивно-компульсивное расстройство"),
    ("FTD", "ЛВД", "FTD", "FTD", "FTD", "лобно-височная деменция"),
    ("PTSD", "ПТСР", "PTSP", "PTSD", "TSSB", "посттравматическое стрессовое расстройство"),
    ("cPTSD", "КПТСР", "KPTSP", "cPTSD", "KTSSB", "комплексное ПТСР"),
    ("GAD", "ГТР", "GAD", "GAD", "YAB", "генерализованное тревожное расстройство"),
    ("ASD", "РАС", "ASP", "ASD", "OSB", "расстройство аутистического спектра"),
    ("BDD", "BDD", "BDD", "BDD", "BDD", "дисморфическое расстройство"),
    ("DID", "ДРИ", "DİP", "DID", "DKB", "диссоциативное расстройство идентичности"),
    ("ARFID", "ARFID", "ARFID", "ARFID", "ARFID", "избегающе-ограничительное расстройство приёма пищи"),
    ("IED", "IED", "İED", "IED", "İED", "интермиттирующее эксплозивное расстройство"),
    ("ODD", "ОВР", "ODD", "ODD", "ODD", "оппозиционно-вызывающее расстройство"),
    ("MCI", "MCI", "MCI", "MCI", "MCI", "умеренное когнитивное нарушение"),
    ("DLB", "DLB", "DLB", "DLB", "DLB", "деменция с тельцами Леви"),
    ("OSA", "OSA", "OSA", "OSA", "OSA", "обструктивное апноэ сна"),
    ("ED", "ED", "ED", "ED", "ED", "эректильная дисфункция"),
    ("PE", "PE", "PE", "PE", "PE", "преждевременная эякуляция"),
    ("HSDD", "HSDD", "HSDD", "HSDD", "HSDD", "снижение сексуального влечения"),
    ("DCD", "DCD", "DCD", "DCD", "DCD", "расстройство развития координации"),
    ("PMDD", "ПМДР", "PMDD", "PMDD", "PMDD", "предменструальное дисфорическое расстройство"),
    ("ORS", "ORS", "ORS", "ORS", "ORS", "обонятельное расстройство"),
    ("BED", "BED", "BED", "BED", "BED", "приступообразное переедание"),
]
CLASS_ROWS = [
    ("ICD11", "МКБ-11", "XBT-11", "ICD-11", "ICD-11", "классификация МКБ-11 / XBT-11"),
    ("ICD10", "МКБ-10", "XBT-10", "ICD-10", "ICD-10", "классификация МКБ-10 / XBT-10"),
    ("DSM5", "DSM-5-TR", "DSM-5-TR", "DSM-5-TR", "DSM-5-TR", "классификация DSM-5-TR"),
]

# строчные формы, которые надо поднять в канон (реальная ошибка регистра)
ABBR_LOWER_EXTRA = {"ru": ["окр", "сдвг", "ftd", "птср", "гтр", "дри", "овр",
                           "bdd", "ors", "bed", "arfid", "ied", "mci", "dlb",
                           "osa", "ed", "pe", "hsdd", "пмдр", "кптср", "к-птср"],
                    "az": ["okp", "ddhp", "ftd", "gad", "bdd", "kptsp", "dip",
                           "ıed", "ied", "odd", "asp", "pmdd", "ptsp", "arfid",
                           "dcd", "adhd", "ors", "bed", "mci", "dlb", "osa",
                           "ed", "pe", "hsdd"],
                    "en": ["ocd", "asd", "gad", "bdd", "ors", "did", "bed",
                           "arfid", "ied", "odd", "mci", "dlb", "ftd", "osa",
                           "ed", "pe", "hsdd", "cptsd"],
                    "tr": ["okb", "osb", "dehb", "yab", "bdd", "ors", "tssb",
                           "ktssb", "dkb", "bed", "arfıd", "arfid", "ıed",
                           "ied", "odd", "mcı", "dlb", "ftd", "osa", "ed",
                           "pe", "hsdd"]}

VERSIONS = {"az": os.path.join(BOOK, "(az)"), "ru": os.path.join(BOOK, "ru"),
            "en": os.path.join(BOOK, "en"), "tr": os.path.join(BOOK, "tr")}

RE_PAREN_TOKEN = re.compile(r"\(([^()\s]{2,14})\)")

TURK_LOWER = str.maketrans({"I": "ı", "İ": "i"})


def lang_lower(s: str, lang: str) -> str:
    return s.translate(TURK_LOWER).lower() if lang in ("az", "tr") else s.lower()


def lang_upper1(c: str, lang: str) -> str:
    if lang in ("az", "tr"):
        return {"i": "İ", "ı": "I"}.get(c, c.upper())
    return c.upper()


def folder(lang: str, base: str = None) -> str:
    b = base or BOOK
    return b if lang == "az" else os.path.join(b, lang)


# ── сборка реестра ───────────────────────────────────────────────────────────
RE_ROW = re.compile(r'<a class="bk-row bk-row--(?:sec|sub)" href="([^"#]+)[^"]*">'
                    r'<span class="bk-row__n">[^<]*</span><span class="bk-row__t">(.*?)</span>')
RE_H1 = re.compile(r'<h1 class="bk-chead__h1">(.*?)</h1>', re.S)
RE_TC = re.compile(r'<a href="([^"]+)"><span class="tc-(?:range|sc)">[^<]*</span><span>(.*?)</span>')
RE_TOC = re.compile(r'<a class="bk-toc__a" href="([^"]+)">\s*<span class="bk-toc__n">[^<]*</span>\s*'
                    r'<span class="bk-toc__t">(.*?)(?:<span|</span>)', re.S)
RE_EN_SPAN = re.compile(r'<span lang="en">(.*?)</span>', re.S)
RE_TAG = re.compile(r"<[^>]+>")


def txt(x: str) -> str:
    return re.sub(r"\s+", " ", H.unescape(RE_TAG.sub("", x))).strip()


def collect(base: str = None):
    """Собирает по версиям: {lang: {slug: Counter(имя)}}, h1, шкалы."""
    names = {lg: defaultdict(Counter) for lg in VERSIONS}
    h1s = {lg: {} for lg in VERSIONS}
    scales = {lg: Counter() for lg in VERSIONS}
    for lg in VERSIONS:
        d = folder(lg, base)
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            if not f.endswith(".html"):
                continue
            t = open(os.path.join(d, f), encoding="utf-8").read()
            if f not in REGISTRY_PAGES:
                for m in RE_ROW.finditer(t):
                    names[lg][os.path.basename(m.group(1))][txt(m.group(2))] += 1
                for m in RE_TC.finditer(t):
                    names[lg][os.path.basename(m.group(1))][txt(m.group(2))] += 1
                for m in RE_TOC.finditer(t):
                    names[lg][os.path.basename(m.group(1))][txt(m.group(2))] += 1
            m = RE_H1.search(t)
            if m:
                h1s[lg][f] = txt(m.group(1))
            body = t[t.find('<div class="bk-read">'):]
            body = re.sub(r'<(li|p)\b[^>]*>.*?</\1>', " ", body, flags=re.S)
            for m in RE_EN_SPAN.finditer(body):
                v = txt(m.group(1))
                if 1 <= len(v.split()) <= 6 and re.search(r"[A-Za-z]", v):
                    scales[lg][v] += 1
    return names, h1s, scales


def abbr_rows():
    """Строки реестра для аббревиатур и классификаций (+ обратный индекс)."""
    rows = []
    for key, ru, az, en, tr, gloss_ru in ABBR_ROWS:
        rows.append({"key": key, "ru": ru, "az": az, "en": en, "tr": tr,
                     "rule": RULE_ABBR, "where": "скобка-расшифровка",
                     "note": f"аббревиатура: {gloss_ru}"})
    for key, ru, az, en, tr, gloss_ru in CLASS_ROWS:
        rows.append({"key": key, "ru": ru, "az": az, "en": en, "tr": tr,
                     "rule": RULE_LAT, "where": "код классификации",
                     "note": gloss_ru})
    return rows


def abbr_index(rows):
    """{lang: {форма в любом регистре: КАНОН этой версии}} из строк реестра."""
    langs = ("ru", "az", "en", "tr")
    idx = {lg: {} for lg in langs}
    for r in rows:
        if r["rule"] != RULE_ABBR:
            continue
        for lg in langs:
            canon = r[lg].strip()
            if not canon:
                continue
            idx[lg][lang_lower(canon, lg)] = canon
            if re.fullmatch(r"[A-Za-zİı]+", r["key"]):
                idx[lg][r["key"].lower()] = canon
            if lg == "ru":                      # латинские формы соседних версий
                for o in ("az", "en", "tr"):
                    v = r[o].strip()
                    if v and re.fullmatch(r"[A-Za-zİı]+", v):
                        idx[lg][v.lower()] = canon
    # строчные формы, встреченные в дереве
    for lg, lows in ABBR_LOWER_EXTRA.items():
        for low in lows:
            key = lang_lower(low, lg)
            if key in idx[lg]:
                continue
            for r in rows:
                if r["rule"] != RULE_ABBR:
                    continue
                forms = {lang_lower(r[o], o) for o in langs if r[o]}
                forms.add(r["key"].lower())
                forms = {f.replace("ı", "i").replace("İ", "i") for f in forms}
                if lang_lower(low, "en").replace("ı", "i").replace("İ", "i") in forms:
                    idx[lg][key] = r[lg] or r["key"]
                    break
    for lg in idx:
        for canon in idx[lg].values():
            ABBR_SAFE.add(canon.upper())
    return idx


EXTRA_NAME_ROWS = [
    {"key": "index.html", "ru": "Клиническая психиатрия", "az": "Klinik Psixiatriya",
     "en": "Clinical Psychiatry", "tr": "Klinik Psikiyatri", "rule": RULE_NAME,
     "where": "название книги: обложка, шапка, <title>, og, JSON-LD, подпись заказа",
     "note": "название книги — имя собственное: каждое слово с прописной (RU — первое слово), не капсом"},
]


# ── слоты названия книги: <title>, og, описания, JSON-LD, подписи ────────────
RE_TITLE = re.compile(r"<title>(.*?)</title>", re.S)
RE_OG_TITLE = re.compile(r'(<meta property="og:title" content=")([^"]*)(")')
RE_DESC = re.compile(r'(<meta name="description" content=")([^"]*)(")')
RE_OG_DESC = re.compile(r'(<meta property="og:description" content=")([^"]*)(")')
RE_JSONLD_NAME = re.compile(r'("name"\s*:\s*")([^"]*)(")')
RE_DATA_ORDER = re.compile(r'(data-order=")([^"]*)(")')
RE_SLOT_TP = re.compile(r'(<h1 class="bk-tp__title">)(.*?)(</h1>)', re.S)

# как название книги может быть написано в любой из версий (чужое имя — тоже ошибка)
BOOK_FORMS = {
    "ru": "клиническая психиатрия",
    "az": "klinik psixiatriya",
    "en": "clinical psychiatry",
    "tr": "klinik psikiyatri",
}


def is_book_title(s: str, lang: str) -> bool:
    """Строка — название книги (в любой версии, любом регистре)?"""
    k = re.sub(r"\s+", " ", lang_lower(s, lang)).strip().replace("\u0307", "")
    k = k.rstrip(".").strip()
    if not k:
        return False
    return k in set(BOOK_FORMS.values())


def title_part(h1_text: str, canon: str) -> str:
    """Часть «до |» в <title>: канон реестра + префикс из h1 («Без психоза — …»)."""
    h1 = re.sub(r"\s+", " ", h1_text).strip()
    if not h1:
        return ""
    if canon:
        if h1 == canon:
            return canon
        if h1.startswith(canon):
            tail = h1[len(canon):].strip()
            if not tail or (tail.startswith("(") and tail.endswith(")")):
                return canon
        pre, sep, rest = h1.rpartition("—")
        if sep:
            rest = rest.strip()
            if rest.startswith(canon):
                tail = rest[len(canon):].strip()
                if not tail or (tail.startswith("(") and tail.endswith(")")):
                    return pre.strip() + " — " + canon
    return re.sub(r"\s*\([^()]*\)\s*$", "", h1).strip() or h1


def canon_text(s: str, lang: str, abbr: dict) -> str:
    """Канон названия: «строчными, кроме первого слова» + аббревиатуры в скобках."""
    s = norm_sent(s, lang)
    def repl(m):
        tok = m.group(1)
        key = lang_lower(tok, lang).replace("–", "-").replace("—", "-")
        if key in abbr:
            return "(" + abbr[key] + ")"
        return m.group(0)
    return RE_PAREN_TOKEN.sub(repl, s)


def cmd_build(a):
    base = a.book
    names, h1s, scales = collect(base)
    abbr = abbr_index(abbr_rows())
    slugs = set()
    for lg in names:
        slugs |= set(names[lg]) | set(h1s[lg])
    # имя по версии: большинство пунктов меню, иначе заголовок страницы
    def pick(lg, slug):
        c = names[lg].get(slug)
        if c:
            return c.most_common(1)[0][0]
        return h1s[lg].get(slug, "")
    rows = []
    for slug in sorted(slugs):
        vals = {lg: pick(lg, slug) for lg in ("ru", "az", "en", "tr")}
        if not any(vals.values()):
            continue
        vals = {lg: canon_text(v, lg, abbr[lg]) for lg, v in vals.items()}
        rows.append({"key": slug, **vals, "rule": RULE_SENT,
                     "where": "заголовок раздела / пункт меню", "note": ""})
    rows = [r for r in rows if r["key"] not in {x["key"] for x in EXTRA_NAME_ROWS}]
    rows += EXTRA_NAME_ROWS + abbr_rows()
    # шкалы и инструменты — латиница по праву (взяты из <span lang="en">)
    seen_scale = Counter()
    for lg in ("ru", "az", "en", "tr"):
        for k, v in scales[lg].items():
            if re.search(r"\d", k) or re.fullmatch(r"[A-Z][A-Za-z\-]+", k):
                seen_scale[k] += v
    for k, v in seen_scale.most_common(a.scales):
        rows.append({"key": "", "ru": k, "az": k, "en": k, "tr": k,
                     "rule": RULE_LAT, "where": "основной текст",
                     "note": "шкала/инструмент — латиница по праву"})
    os.makedirs(os.path.dirname(REGISTER_TSV), exist_ok=True)
    with open(REGISTER_TSV, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", quoting=csv.QUOTE_MINIMAL)
        w.writerow(["#key", "термин_ru", "термин_az", "термин_en", "термин_tr",
                    "канонический_регистр", "где_применяется", "примечание"])
        for r in rows:
            w.writerow([r["key"], r["ru"], r["az"], r["en"], r["tr"],
                        r["rule"], r["where"], r["note"]])
    print(f"CASE-REGISTER.tsv: {len(rows)} строк → {REGISTER_TSV}")
    return 0


def load_registry():
    rows = []
    with open(REGISTER_TSV, encoding="utf-8") as fh:
        rd = csv.reader(fh, delimiter="\t")
        head = next(rd)
        for r in rd:
            if not r or len(r) < 7:
                continue
            rows.append({"key": r[0], "ru": r[1], "az": r[2], "en": r[3], "tr": r[4],
                         "rule": r[5], "where": r[6], "note": r[7] if len(r) > 7 else ""})
    return rows


RE_ROMAN = re.compile(r"^[IVXLCDM]{1,4}$")
ABBR_SAFE = set()           # заполняется abbr_index(): все каноны аббревиатур


def norm_sent(s: str, lang: str) -> str:
    """Канон «строчными, кроме первого слова»: КАПС → строчные, «С» внутри → «с».

    Не трогает: коды (с цифрами), аббревиатуры в скобках и без, римские цифры,
    всё, что стоит в скобках (там расшифровка-аббревиатура живёт по канону реестра).
    """
    words = re.findall(r"[^\W\d_]+(?:[-–—'’][^\W\d_]+)*", s, re.U)
    for m in re.finditer(r"[^\W\d_]+(?:[-–—'’][^\W\d_]+)*", s, re.U):
        w = m.group(0)
        if RE_ROMAN.match(w) or w.upper() in ABBR_SAFE:
            continue                     # римская цифра или аббревиатура
        parts = [p for p in re.split(r"([-–—])", w) if re.search(r"[^\W\d_]", p)]
        if all(p.isupper() for p in parts) and all(len(p) >= 2 for p in parts):
            s = s[:m.start()] + "".join(lang_lower(p, lang) if p.isalpha() else p
                                        for p in re.split(r"([-–—])", w)) + s[m.end():]
            continue
        if len(w) == 1 and re.match(r"[А-ЯЁӘĞŞÇÖÜİ]", w):
            s = s[:m.start()] + lang_lower(w, lang) + s[m.end():]
    m = re.match(r"[\s«„\"'(\[]*([^\W\d_])", s, re.U)
    if m and m.group(1).islower():
        i = m.start(1)
        s = s[:i] + lang_upper1(s[i], lang) + s[i + 1:]
    return s


# ── слоты имён: где живут названия в разметке концепта ───────────────────────
RE_SLOT_ROW = re.compile(
    r'<a class="bk-row bk-row--(sec|sub)[^"]*" href="([^"#]+)"([^>]*)>'
    r'(<span class="bk-row__n">[^<]*</span>)?<span class="bk-row__t">(.*?)</span>', re.S)
RE_SLOT_TOC = re.compile(
    r'<a class="bk-toc__a[^"]*" href="([^"#]+)"[^>]*>\s*<span class="bk-toc__n">[^<]*</span>\s*'
    r'<span class="bk-toc__t">(.*?)(<span class="bk-toc__r">|</span>)', re.S)
RE_SLOT_PN = re.compile(
    r'(<a class="bk-pn__a[^"]*" href="([^"#]+)"[^>]*>\s*<span class="bk-pn__dir">[^<]*</span>\s*'
    r'<span class="bk-pn__t">)(.*?)(</span>)', re.S)
RE_SLOT_CRUMB = re.compile(r'(<nav class="bk-crumb"[^>]*>\s*<a href="([^"#]+)">)(.*?)(</a>)', re.S)
RE_SLOT_TC = re.compile(
    r'(<a href="([^"#]+)"><span class="tc-(?:range|sc)">[^<]*</span><span>)(.*?)(</span>)', re.S)
RE_SLOT_BOOK = re.compile(r'(<span class="bk-book__t">)(.*?)(</span>)', re.S)
RE_CHEAD = re.compile(
    r'<h1 class="bk-chead__h1">(.*?)</h1>(\s*)(<p class="bk-chead__en">(.*?)</p>)?', re.S)
RE_CHEAD_EN = re.compile(r'<p class="bk-chead__en">(.*?)</p>\s*', re.S)
RE_LONE_CAP = re.compile(r"([^\W\d_]{2,})(\s+)([А-ЯЁ])(\s+)([а-яё]{2,})", re.U)


def slot_ok(canon: str, actual: str, lang: str) -> bool:
    """Слот по реестру: имя; «Prefix — имя»; имя + (латиница); оба украшения вместе."""
    a = re.sub(r"\s+", " ", actual).strip()
    c = re.sub(r"\s+", " ", canon).strip()
    if a == c:
        return True
    m = re.match(r"^(.*?)\s*\(([^()]*)\)$", a)
    if m and lang_lower(m.group(2), lang) != lang_lower(c, lang):
        a = m.group(1)          # первое упоминание латинского названия — в скобках
    if a == c:
        return True
    return bool(re.match(r"^(.{0,32}—\s*)" + re.escape(c) + r"$", a))


def load_maps(base: str = None):
    """Из реестра: имя по слагу для каждой версии + канон аббревиатур."""
    rows = load_registry()
    names = {lg: {} for lg in VERSIONS}
    for r in rows:
        if r["rule"] not in (RULE_SENT, RULE_NAME) or not r["key"]:
            continue
        for lg in VERSIONS:
            if r[lg].strip():
                names[lg][r["key"]] = r[lg].strip()
    return names, abbr_index(rows)


def skip_zone(raw: str) -> tuple:
    """Зона деревьев DSM-5-TR и МКБ-10: их пункты — имена классификаций, не реестра."""
    a = raw.find('<div class="cls-tree" data-cls="dsm"')
    if a < 0:
        return -1, -1
    b = raw.find("</aside>", a)
    return a, b if b > a else len(raw)


def page_part(out: str, lang: str, slug: str, names: dict) -> str:
    """«Часть до |» для заголовка страницы: из h1 (канон + префикс), иначе из <title>."""
    canon = names[lang].get(slug, "")
    mh = RE_CHEAD.search(out)
    if mh:
        return title_part(txt(mh.group(1)), canon)
    mt = RE_TITLE.search(out)
    if mt and "|" in mt.group(1):
        return re.sub(r"\s+", " ", mt.group(1).split("|")[0]).strip()
    return ""


def fix_book_meta(out: str, lang: str, slug: str, names: dict, stats: Counter,
                  log=None) -> str:
    """Название книги в <title>, og:title, описаниях, JSON-LD, подписи заказа.

    Форматы: «{часть} | {название книги}» и «{название книги} — {часть}».
    """
    bt = names[lang].get("index.html")
    if not bt:
        return out
    part = page_part(out, lang, slug, names)

    def sub_g(m, rx, gi, kind, new_of):
        inner = m.group(gi)
        new = new_of(inner)
        if new is None or new == inner:
            return m.group(0)
        stats[kind] += 1
        if log:
            log(kind, inner, new)
        s = m.group(0)
        a, b = m.start(gi) - m.start(0), m.end(gi) - m.start(0)
        return s[:a] + new + s[b:]

    def pair_of(inner):
        if "|" not in inner:
            return None
        new = (part or re.sub(r"\s+", " ", inner.split("|")[0]).strip()) + " | " + bt
        return new

    def desc_of(inner):
        head, sep, rest = inner.partition(" — ")
        if not sep or not is_book_title(head, lang):
            return None
        new = bt + " — " + (part or rest.strip())
        return new if new != inner else None

    out = RE_TITLE.sub(lambda m: sub_g(m, RE_TITLE, 1, "slot:meta-title", pair_of), out)
    out = RE_OG_TITLE.sub(lambda m: sub_g(m, RE_OG_TITLE, 2, "slot:og-title", pair_of), out)
    out = RE_DESC.sub(lambda m: sub_g(m, RE_DESC, 2, "slot:meta-desc", desc_of), out)
    out = RE_OG_DESC.sub(lambda m: sub_g(m, RE_OG_DESC, 2, "slot:og-desc", desc_of), out)
    out = RE_JSONLD_NAME.sub(
        lambda m: sub_g(m, RE_JSONLD_NAME, 2, "slot:jsonld-name",
                        lambda s: bt if is_book_title(s, lang) else None), out)
    out = RE_DATA_ORDER.sub(
        lambda m: sub_g(m, RE_DATA_ORDER, 2, "slot:data-order",
                        lambda s: bt if is_book_title(s, lang) else None), out)
    out = RE_SLOT_TP.sub(
        lambda m: sub_g(m, RE_SLOT_TP, 2, "slot:cover-title",
                        lambda s: bt if is_book_title(txt(s), lang) else None), out)
    return out


def fix_page(path: str, lang: str, names: dict, abbr: dict, dry: bool, stats: Counter,
             changes: list, rows=None, latin=None):
    raw = open(path, encoding="utf-8").read()
    out = raw
    slug = os.path.basename(path)
    reg_page = slug in REGISTRY_PAGES

    def sub_slot(rx, name_idx, kind, href_idx=2, per_match=False):
        """Меняет ТОЛЬКО текст слота (группа name_idx) на имя из реестра."""
        nonlocal out
        n = [0]

        za, zb = skip_zone(raw)          # деревья DSM/МКБ-10 — имена классификаций

        def repl(m):
            href = os.path.basename(m.group(href_idx))
            canon = names[lang].get(href)
            old = m.group(name_idx)
            if not canon or reg_page or "—" in old or canon == old:
                return m.group(0)
            if za >= 0 and za <= m.start() < zb:
                return m.group(0)
            s = m.group(0)
            a = m.start(name_idx) - m.start(0)
            b = m.end(name_idx) - m.start(0)
            n[0] += 1
            return s[:a] + canon + s[b:]

        out2 = rx.sub(repl, out)
        if n[0]:
            stats["slot:" + kind] += n[0] if per_match else 1
        out = out2

    sub_slot(RE_SLOT_ROW, 5, "menu-row", href_idx=2, per_match=True)
    sub_slot(RE_SLOT_TOC, 2, "toc", href_idx=1, per_match=True)
    sub_slot(RE_SLOT_PN, 3, "prev-next", href_idx=2, per_match=True)
    sub_slot(RE_SLOT_CRUMB, 3, "crumb", href_idx=2, per_match=True)
    sub_slot(RE_SLOT_TC, 3, "toc-page", href_idx=2, per_match=True)
    # подпись шапки книги — по строке реестра index.html
    bt = names[lang].get("index.html")
    if bt:
        def book_repl(m):
            if m.group(2) != bt:
                stats["slot:book-title"] += 1
                return m.group(1) + bt + m.group(3)
            return m.group(0)
        out = RE_SLOT_BOOK.sub(book_repl, out)
        out = fix_book_meta(out, lang, slug, names, stats)

    # ── заголовок главы/страницы + латинское название в скобках ──────────────
    def chead_repl(m):
        old, nl, pen, en = m.group(1), m.group(2), m.group(3) or "", m.group(4)
        canon = names[lang].get(slug)
        pref = ""
        mm = re.match(r"^([^—]{0,32}—\s*)(.*)$", old)
        if mm and canon and lang_lower(canon, lang) in lang_lower(norm_sent(mm.group(2), lang), lang):
            pref = mm.group(1)
        base = norm_sent(canon, lang) if canon else norm_sent(old, lang)
        base = pref + base
        if en and lang != "en":
            if lang_lower(norm_sent(en, lang), lang) == lang_lower(base, lang):
                stats["chead:dup-line-removed"] += 1
                return '<h1 class="bk-chead__h1">' + base + "</h1>" + nl.rstrip()
            add = " (" + norm_sent(en, lang) + ")"
            stats["chead:latin-in-parens"] += 1
            return '<h1 class="bk-chead__h1">' + base + add + "</h1>"
        if en and lang == "en" and norm_sent(en, lang) == base:
            stats["chead:dup-line-removed"] += 1
            return '<h1 class="bk-chead__h1">' + base + "</h1>" + nl.rstrip()
        return '<h1 class="bk-chead__h1">' + base + "</h1>" + nl + pen

    out = RE_CHEAD.sub(chead_repl, out)

    # ── латинское название главы/расстройства — в скобках при первом упоминании ─
    if lang != "en" and not reg_page:
        en_name = ""
        for r in (rows or []):
            if r["key"] == slug and r["rule"] == RULE_SENT:
                en_name = re.sub(r"\s*\([^)]*\)\s*$", "", r["en"]).strip()
                break
        if en_name:
            def latin_repl(m):
                body = m.group(1)
                mm = re.match(r"^(.*?)\s*\(([^()]*)\)\s*$", body)
                if mm:            # скобка уже есть: дубль имени → латинское название
                    if lang_lower(mm.group(2), lang) == lang_lower(mm.group(1), lang)                             and lang_lower(en_name, lang) != lang_lower(mm.group(1), lang):
                        stats["chead:latin-fixed"] += 1
                        return ('<h1 class="bk-chead__h1">' + mm.group(1) + " (" +
                                en_name + ")</h1>")
                    return m.group(0)
                if lang_lower(en_name, lang) == lang_lower(body, lang):
                    return m.group(0)
                stats["chead:latin-in-parens"] += 1
                return '<h1 class="bk-chead__h1">' + body + " (" + en_name + ")</h1>"
            out = re.sub(r'<h1 class="bk-chead__h1">(.*?)</h1>', latin_repl, out, count=1, flags=re.S)

    # ── аббревиатуры: строчные формы → канон реестра (все версии, кроме реестров)
    if not reg_page:
        def abbr_repl(m):
            tok = m.group(1)
            key = lang_lower(tok, lang).replace("–", "-").replace("—", "-")
            canon = abbr.get(key)
            if canon and canon != tok:
                stats["abbr:" + canon] += 1
                return "(" + canon + ")"
            return m.group(0)
        out = RE_PAREN_TOKEN.sub(abbr_repl, out)

    # ── «С»/«И»/«К»/«В» внутри строки — автокапитализация (только меню/заголовки)
    if not reg_page:
        def lone(m):
            stats["lone-cap"] += 1
            return m.group(1) + m.group(2) + lang_lower(m.group(3), lang) + m.group(4) + m.group(5)
        head = out[:out.find('<main')] if '<main' in out else ""
        i = out.find('<aside')
        j = out.find('</aside>') + 8 if '<aside' in out else 0
        k = out.find('<div class="bk-read">')
        seg1 = out[i:j] if j else ""
        seg2 = out[j:k] if k > j else ""
        seg1 = RE_LONE_CAP.sub(lone, seg1)
        seg2 = RE_LONE_CAP.sub(lone, seg2)
        out = out[:i] + seg1 + seg2 + out[k:] if j and k > j else out
    # ── иноязычные названия расстройств вне скобок → имя версии по реестру ────
    if latin and not reg_page:
        out = fix_foreign_names(out, lang, names, rows, latin, stats)

    if out != raw:
        changes.append((slug, stats))
        if not dry:
            crlf = b"\r\n" in open(path, "rb").read(200000)
            data = out.replace("\n", "\r\n") if crlf else out
            open(path, "w", encoding="utf-8", newline="").write(data)
    return out != raw


RE_TD = re.compile(r"(<td[^>]*>)([^<]{2,90}?)(\s*\((?:[A-Z]{1,3}\d[\w.–—\- ]*|6[A-Z]\d\d(?:\.\d)?|F\d\d(?:\.\d+x?)?)\))?(</td>)")
RE_PAREN_LATIN = re.compile(r"\(([^()]{2,200})\)")
# «Имя (МКБ-11: 6C20 Имя; …» — дубль имени внутри кодовой скобки
RE_DUP_NAME = re.compile(
    r"(«?)([А-ЯЁA-ZƏİ][^<>()«»]{4,90}?)\s*\(((?:МКБ|XBT|ICD)\s*-?\s*1[01]|DSM-5-TR):"
    r"(\s*<span class=\"icd\">[^<]*</span>)?\s*([^();<>]{4,90}?)\s*([;,)])")


def latin_term_map(rows):
    """{латинское название (en): слаг} — чтобы менять иноязычный термин на имя версии."""
    out = {}
    for r in rows:
        if r["rule"] != RULE_SENT or not r["key"]:
            continue
        en = re.sub(r"\s*\([^)]*\)\s*$", "", r["en"]).strip()
        if len(en.split()) >= 2 and re.search(r"[a-z]{3,}", en):
            out[en.lower()] = r["key"]
    return out


def lang_name(names, slug, lang, fallback=True):
    return names[lang].get(slug, "")


def fix_foreign_names(raw, lang, names, rows, latin, stats):
    """Иноязычное название расстройства вне скобок/кода → имя версии (реестр).

    Две формы: ячейка таблицы «<td>Latin Name (6B22)</td>» и расшифровка в скобках
    «(МКБ-11: 6B42 Latin Name; DSM-5-TR: …)».
    """
    i = raw.find('<div class="bk-read">')
    if i < 0:
        return raw                       # у страницы нет колонки чтения — не трогаем
    head, tail = raw[:i], raw[i:]
    raw = tail

    def td_repl(m):
        body = m.group(2).strip()
        key = body.lower()
        slug = latin.get(key)
        if not slug or not names[lang].get(slug):
            return m.group(0)
        stats["foreign:table-cell"] += 1
        return m.group(1) + names[lang][slug] + (m.group(3) or "") + m.group(4)
    raw = RE_TD.sub(td_repl, raw)

    def paren_repl(m):
        inner = m.group(1)
        new = inner
        for nm, slug in latin.items():
            if nm in new.lower() and names[lang].get(slug):
                i = new.lower().find(nm)
                orig = new[i:i + len(nm)]
                if orig[0].isupper():       # название с прописной — это термин, не проза
                    new = new[:i] + names[lang][slug] + new[i + len(nm):]
                    stats["foreign:definition-line"] += 1
        return "(" + new + ")"
    if lang != "en":
        raw = RE_PAREN_LATIN.sub(paren_repl, raw)
    # убираем дубль: «Телесный дистресс (МКБ-11: 6C20 Телесный дистресс; …)» → без повтора
    def dup_repl(m):
        name, code, tail = m.group(2).strip(), m.group(4) or "", m.group(5).strip()
        if tail.lower() == name.lower():
            stats["foreign:dup-name-in-paren"] += 1
            return f"{m.group(1)}{name} ({m.group(3)}:{code}{m.group(6)}"
        return m.group(0)
    raw = RE_DUP_NAME.sub(dup_repl, raw)
    return head + raw


# ── иноязычное вне скобок → язык версии (правило 4 стандарта) ────────────────
# Владелец: иноязычное — только в скобках при первом упоминании; «Somatic Symptom
# Disorder (F45.1)» → «соматическое симптоматическое расстройство (somatic symptom
# disorder, F45.1)»; «care-seeking и care-avoiding» → «поиск помощи и избегание
# помощи (care-seeking / care-avoiding)»; «reassurance» → «успокаивающая проверка
# (reassurance)». Строки ниже — ровно эти случаи в четырёх версиях.
# ── иноязычное вне скобок → язык версии (правило 4 стандарта) ────────────────
# Владелец: иноязычное — только в скобках при первом упоминании; «Somatic Symptom
# Disorder (F45.1)» → «соматическое симптоматическое расстройство (somatic symptom
# disorder, F45.1)»; «care-seeking и care-avoiding» → «поиск помощи и избегание
# помощи (care-seeking / care-avoiding)»; «reassurance» → «успокаивающая проверка
# (reassurance)». Строки ниже — ровно эти случаи в четырёх версиях.
LATIN_FIX = [
    # ── ru ────────────────────────────────────────────────────────────────
    ("ru", "6B23.html", '<strong><span lang="en">Somatic Symptom Disorder</span></strong> (F45.1)',
     '<strong>соматическое симптоматическое расстройство</strong> (somatic symptom disorder, F45.1)'),
    ("ru", "6B23.html", '<strong>Illness Anxiety Disorder</strong> (F45.21)',
     '<strong>тревожное расстройство болезни</strong> (illness anxiety disorder, F45.21)'),
    ("ru", "6B23.html", 'DSM-5-TR: F45.21 Illness Anxiety Disorder — новое название',
     'DSM-5-TR: F45.21 тревожное расстройство болезни (illness anxiety disorder) — новое название'),
    ("ru", "6B23.html", 'разделение illness anxiety disorder и somatic symptom disorder',
     'разделение тревожного расстройства болезни (illness anxiety disorder) и соматического симптоматического расстройства (somatic symptom disorder)'),
    ("ru", "6B23.html", 'подтипы care-seeking и care-avoiding',
     'подтипы поиск помощи и избегание помощи (care-seeking / care-avoiding)'),
    ("ru", "6B23.html", '<strong>Care-seeking</strong>', '<strong>Поиск помощи (care-seeking)</strong>'),
    ("ru", "6B23.html", '<strong>Care-avoiding</strong>', '<strong>Избегание помощи (care-avoiding)</strong>'),
    ("ru", "6B23.html", 'предотвращение проверки тела и поиска reassurance (экспозиция',
     'предотвращение проверки тела и поиска успокаивающей проверки (reassurance; экспозиция'),
    ("ru", "6B23.html", 'Лимит reassurance —', 'Лимит успокаивающей проверки (reassurance) —'),
    ("ru", "6B23.html", 'поиском reassurance, экспозиция', 'поиском успокаивающей проверки (reassurance), экспозиция'),
    ("ru", "6C20.html", 'ограниченное «reassurance»', 'ограниченное «успокаивающая проверка» (reassurance)'),
    ("ru", "6C49.html", 'обстановка, reassurance,', 'обстановка, успокаивающая проверка (reassurance),'),
    ("ru", "6C20.html", '«Bodily Distress Disorder»', '«телесный дистресс»'),
    ("ru", "6C50.html", '«Gambling Disorder»', '«расстройство вследствие пристрастия к азартным играм»'),
    # ── az ────────────────────────────────────────────────────────────────
    ("az", "6B23.html", '<strong><span lang="en">Somatic Symptom Disorder</span></strong> (F45.1)',
     '<strong>somatik simptom pozuntusu</strong> (somatic symptom disorder, F45.1)'),
    ("az", "6B23.html", '<strong>Illness Anxiety Disorder</strong> (F45.21)',
     '<strong>xəstəlik təşvişi pozuntusu</strong> (illness anxiety disorder, F45.21)'),
    ("az", "6B23.html", 'F45.21 Illness Anxiety Disorder — yeni adı',
     'F45.21 xəstəlik təşvişi pozuntusu (illness anxiety disorder) — yeni adı'),
    ("az", "6B23.html", '<strong>Care-seeking</strong>', '<strong>Yardım axtarma (care-seeking)</strong>'),
    ("az", "6B23.html", '<strong>Care-avoiding</strong>', '<strong>Yardımdan qaçınma (care-avoiding)</strong>'),
    ("az", "6B23.html", 'Tibbi reassurance qısamüddətli', 'Tibbi təsdiq axtarışı (reassurance) qısamüddətli'),
    ("az", "6B23.html", 'reassurance axtarışının qarşısının alınması', 'təsdiq axtarışının (reassurance) qarşısının alınması'),
    ("az", "6B23.html", 'reassurance axtarışının davranış eksperimentləri', 'təsdiq axtarışının (reassurance) davranış eksperimentləri'),
    ("az", "6B23.html", 'reassurance pozuntunu gücləndirir', 'təsdiq axtarışı (reassurance) pozuntunu gücləndirir'),
    ("az", "6C20.html", '<strong>Bodily Distres Disorder</strong>', '<strong>Bədənsəl distres pozuntusu</strong>'),
    ("az", "6C20.html", '«Bodily Distress Disorder»', '«bədənsəl distres»'),
    ("az", "6C20.html", '<strong><span lang="en">Somatic Symptom Disorder</span></strong>',
     '<strong>somatik simptom pozuntusu (somatic symptom disorder)</strong>'),
    ("az", "6C20.html", '«Doctor shopping»', '«həkimdən həkimə gəzmə» (doctor shopping)'),
    ("az", "6C49.html", 'mühit, reassurance,', 'mühit, təsdiq axtarışı (reassurance),'),
    ("az", "6C50.html", '«Gambling Disorder»', '«qumar oynama pozuntusu»'),
    ("az", "6C51.html", '«Gaming Disorder»', '«oyun oynama pozuntusu»'),
    ("az", "6A22.html", 'Schizotypal Personality Disorder şəxsiyyət pozuntuları',
     'Şizotipik şəxsiyyət pozuntusu (schizotypal personality disorder) şəxsiyyət pozuntuları'),
    ("az", "6A22.html", '«schizophrenia spectrum»', '«şizofreniya spektri» (schizophrenia spectrum)'),
    ("az", "6E40.html", 'Psychological or behavioural factors affecting disorders or diseases classified elsewhere;',
     'Psixoloji və ya davranış amilləri, başqa yerdə təsnif edilən pozuntulara və ya xəstəliklərə təsir edən;'),
    ("az", "6B83.html", '«Feeding Disorder of Infancy or Early Childhood»',
     '«körpəlik və erkən uşaqlıq dövrünün qidalanma pozuntusu» (feeding disorder of infancy or early childhood)'),
    # ── tr ────────────────────────────────────────────────────────────────
    ("tr", "6B23.html", '<strong><span lang="en">Somatic Symptom Disorder</span></strong> (F45.1)',
     '<strong>somatik semptom bozukluğu</strong> (somatic symptom disorder, F45.1)'),
    ("tr", "6B23.html", '<strong>Illness Anxiety Disorder</strong> (F45.21)',
     '<strong>hastalık kaygısı bozukluğu</strong> (illness anxiety disorder, F45.21)'),
    ("tr", "6B23.html", 'F45.21 Illness Anxiety Disorder — yeni adı',
     'F45.21 hastalık kaygısı bozukluğu (illness anxiety disorder) — yeni adı'),
    ("tr", "6B23.html", '<strong>Care-seeking</strong>', '<strong>Yardım arayışı (care-seeking)</strong>'),
    ("tr", "6B23.html", '<strong>Care-avoiding</strong>', '<strong>Yardımdan kaçınma (care-avoiding)</strong>'),
    ("tr", "6B23.html", 'Reassurance (‘sen sağlıklısın’)', 'Güvence arayışı (‘sen sağlıklısın’)'),
    ("tr", "6C20.html", '“Doctor shopping”', '“doktor doktor dolaşma” (doctor shopping)'),
    ("tr", "6C20.html", '<strong>Bodily Distres Disorder</strong>', '<strong>Bedensel distres bozukluğu</strong>'),
    ("tr", "6C20.html", '“Bodily Distress Disorder”', '“bedensel distres”'),
    ("tr", "6C50.html", '“Gambling Disorder”', '“kumar oynama bozukluğu”'),
    ("tr", "6C51.html", '“Gaming Disorder”', '“oyun oynama bozukluğu”'),
    ("tr", "6A22.html", 'Cluster A Personality Disorder ve schizophrenia spectrum listesinde',
     'Cluster A kişilik bozukluğu ve şizofreni spektrumu listesinde'),
    ("tr", "6B83.html", '“Feeding Disorder of Infancy or Early Childhood”',
     '“bebeklik veya erken çocukluk dönemi beslenme bozukluğu” (feeding disorder of infancy or early childhood)'),

    # вторая партия: «различия между источниками» и эпидемиология
    ("ru", "6B23.html", 'DSM-5-TR — Illness Anxiety Disorder (F45.21);',
     'DSM-5-TR — тревожное расстройство болезни (illness anxiety disorder, F45.21);'),
    ("ru", "6C20.html", '«bodily distress syndrome» (Fink P.)',
     '«синдром телесного дистресса» (bodily distress syndrome, Fink P.)'),
    ("ru", "6C50.html", 'Gambling Disorder, распространённость',
     'Расстройство вследствие пристрастия к азартным играм, распространённость'),
    ("az", "6B23.html", 'Illness Anxiety Disorder (F45.21); care-seeking və care-avoiding alt-tipləri.',
     'xəstəlik təşvişi pozuntusu (illness anxiety disorder, F45.21); yardım axtarma və yardımdan qaçınma alt-tipləri (care-seeking / care-avoiding).'),
    ("az", "6A22.html", 'Cluster A Personality Disorder və schizophrenia spectrum siyahısında',
     'Cluster A şəxsiyyət pozuntusu və şizofreniya spektri (schizophrenia spectrum) siyahısında'),
    ("az", "6C20.html", '— «bədənsəl distres» — bodily distres üzrə',
     '— «bədənsəl distres» — bədənsəl distres üzrə'),
    ("az", "6C50.html", 'Gambling Disorder ömürlük yayılma',
     'Qumar oynama pozuntusu (gambling disorder) — ömürlük yayılma'),
    ("tr", "6B23.html", 'Illness Anxiety Disorder (F45.21); care-seeking ve care-avoiding alt tipleri.',
     'hastalık kaygısı bozukluğu (illness anxiety disorder, F45.21); yardım arayışı ve yardımdan kaçınma alt tipleri (care-seeking / care-avoiding).'),
    ("tr", "6C20.html", '“bodily distress syndrome” (Fink P.)',
     '“bedensel distres sendromu” (bodily distress syndrome, Fink P.)'),
    ("tr", "6C50.html", 'Gambling Disorder yaşam boyu',
     'Kumar oynama bozukluğu (gambling disorder) — yaşam boyu'),
]


def cmd_fix(a):
    names, abbr = load_maps(a.book)
    rows = load_registry()
    latin = latin_term_map(rows)
    total = 0
    for lang in ("ru", "az", "en", "tr"):
        d = folder(lang, a.book)
        if not os.path.isdir(d):
            continue
        stats = Counter()
        st_v = Counter()
        for f in sorted(os.listdir(d)):
            if not f.endswith(".html"):
                continue
            st_v.clear()
            if fix_page(os.path.join(d, f), lang, names, abbr, a.dry, st_v, [],
                        rows=rows, latin=latin):
                total += 1
            stats.update(st_v)
        print(f"{lang}: файлов изменено {sum(1 for _ in [0]) if False else ''}"
              f"— правок {sum(stats.values())} {dict(stats.most_common(12))}")
    print(f"всего файлов с правками: {total}{' (dry)' if a.dry else ''}")
    return 0


def check_book_meta(raw: str, lang: str, slug: str, names: dict) -> tuple:
    """Проверка названия книги в <title>, og, описаниях, JSON-LD, подписях."""
    bt = names[lang].get("index.html")
    if not bt:
        return [], 0
    viol = []
    n = 0
    part = page_part(raw, lang, slug, names)

    def add(where, was, term=None):
        viol.append({"lang": lang, "file": slug, "where": where,
                     "term": term or bt, "was": was})

    m = RE_TITLE.search(raw)
    if m and "|" in m.group(1):
        n += 1
        want = (part or re.sub(r"\s+", " ", m.group(1).split("|")[0]).strip()) + " | " + bt
        if m.group(1) != want:
            add("<title>", re.sub(r"\s+", " ", m.group(1)))
    m = RE_OG_TITLE.search(raw)
    if m and "|" in m.group(2):
        n += 1
        want = (part or re.sub(r"\s+", " ", m.group(2).split("|")[0]).strip()) + " | " + bt
        if m.group(2) != want:
            add("og:title", m.group(2))
    for rx, where in ((RE_DESC, "meta description"), (RE_OG_DESC, "og:description")):
        m = rx.search(raw)
        if m:
            head, sep, rest = m.group(2).partition(" — ")
            if sep and is_book_title(head, lang):
                n += 1
                want = bt + " — " + (part or rest.strip())
                if m.group(2) != want:
                    add(where, m.group(2), term=want)
    m = RE_JSONLD_NAME.search(raw)
    if m and is_book_title(m.group(2), lang):
        n += 1
        if m.group(2) != bt:
            add("JSON-LD name", m.group(2))
    m = RE_DATA_ORDER.search(raw)
    if m and is_book_title(m.group(2), lang):
        n += 1
        if m.group(2) != bt:
            add("подпись заказа (data-order)", m.group(2))
    m = RE_SLOT_TP.search(raw)
    if m and is_book_title(txt(m.group(2)), lang):
        n += 1
        if m.group(2) != bt:
            add("заголовок обложки", txt(m.group(2)))
    return viol, n


def cmd_check(a):
    names, abbr = load_maps(a.book)
    rows = load_registry()
    viol = []
    checked = 0
    for lang in ("ru", "az", "en", "tr"):
        d = folder(lang, a.book)
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            if not f.endswith(".html"):
                continue
            raw = open(os.path.join(d, f), encoding="utf-8").read()
            slug = f
            v2, n2 = check_book_meta(raw, lang, slug, names)
            viol.extend(v2)
            checked += n2
            if f in REGISTRY_PAGES:
                continue
            za, zb = skip_zone(raw)
            for rx, gi, what in ((RE_SLOT_ROW, 5, "пункт меню"), (RE_SLOT_TOC, 2, "оглавление главы"),
                                 (RE_SLOT_PN, 3, "пред/след"), (RE_SLOT_CRUMB, 3, "крошка"),
                                 (RE_SLOT_TC, 3, "оглавление книги")):
                for m in rx.finditer(raw):
                    if za >= 0 and za <= m.start() < zb:
                        continue        # DSM/МКБ-10-деревья: имена классификаций по праву
                    checked += 1
                    href = os.path.basename(m.group(2))
                    canon = names[lang].get(href)
                    if not canon or "—" in m.group(gi):
                        continue
                    if not slot_ok(canon, txt(m.group(gi)), lang):
                        viol.append({"lang": lang, "file": f, "where": what,
                                     "term": canon, "was": txt(m.group(gi))})
            bt = names[lang].get("index.html")
            m = RE_SLOT_BOOK.search(raw)
            if m and bt:
                checked += 1
                if m.group(2) != bt:
                    viol.append({"lang": lang, "file": f, "where": "подпись шапки книги",
                                 "term": bt, "was": m.group(2)})
            m = RE_CHEAD.search(raw)
            if m:
                checked += 1
                canon = names[lang].get(slug)
                if canon and not slot_ok(canon, txt(m.group(1)), lang):
                    viol.append({"lang": lang, "file": f, "where": "заголовок страницы",
                                 "term": canon, "was": txt(m.group(1))})
            if RE_CHEAD_EN.search(raw) and lang != "en":
                viol.append({"lang": lang, "file": f, "where": "подпись латиницей",
                             "term": "латиница только в скобках",
                             "was": txt(RE_CHEAD_EN.search(raw).group(1))})
            # аббревиатуры в скобках
            for m in RE_PAREN_TOKEN.finditer(raw):
                tok = m.group(1)
                key = lang_lower(tok, lang).replace("–", "-").replace("—", "-")
                canon = abbr.get(key)
                if canon and canon != tok:
                    viol.append({"lang": lang, "file": f, "where": "скобка-расшифровка",
                                 "term": canon + " (аббревиатура)", "was": "(" + tok + ")"})
    print(f"проверено слотов: {checked}; нарушений: {len(viol)}")
    if viol:
        agg = Counter((v["lang"], v["where"], v["term"], v["was"]) for v in viol)
        for (lg, where, term, was), n in agg.most_common(a.limit):
            print(f"  {n:5} {lg:3} {where:22} {was[:42]!r} → {term[:42]!r}")
    if a.out:
        os.makedirs(a.out, exist_ok=True)
        with open(os.path.join(a.out, "casecheck.tsv"), "w", encoding="utf-8", newline="") as fh:
            w = csv.writer(fh, delimiter="\t", quoting=csv.QUOTE_ALL)
            w.writerow(["язык", "файл", "где", "термин (канон реестра)", "было"])
            for v in viol:
                w.writerow([v["lang"], v["file"], v["where"], v["term"], v["was"]])
        print("отчёт: " + os.path.join(a.out, "casecheck.tsv"))
    return 1 if viol else 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("--book", default=None)
    b.add_argument("--scales", type=int, default=40)
    b.set_defaults(func=cmd_build)
    f = sub.add_parser("fix")
    f.add_argument("--book", default=None)
    f.add_argument("--dry", action="store_true")
    f.set_defaults(func=cmd_fix)
    c = sub.add_parser("check")
    c.add_argument("--book", default=None)
    c.add_argument("--out")
    c.add_argument("--limit", type=int, default=25)
    c.set_defaults(func=cmd_check)
    a = ap.parse_args()
    return a.func(a)


if __name__ == "__main__":
    sys.exit(main())
