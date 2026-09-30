#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""klinik-register — единый регистр и «язык версии» в книге «Klinik Psixiatriya».

Правила владельца, которые здесь измеряются (жалоба 2026-09-30):

 1. Заголовки и пункты меню — единый регистр по всему дереву: первое слово с
    заглавной, остальные строчные (кроме имён собственных и аббревиатур).
    Ни «содержание» рядом с «Предисловие», ни «ОБСЕССИВНО-КОМПУЛЬСИВНЫЕ»
    рядом с «расстройства нейроразвития».
 2. «С» вместо «с» внутри строки — след автокапитализации («связанные С
    психоактивными веществами»). Вычищается.
 3. Аббревиатуры — заглавными и по канону версии: (СДВГ) (ОКР) (ЛВД) в RU,
    (DDHP) (OKP) (FTD) в AZ, (DEHB) (OKB) (TSSB) в TR, (ADHD) (OCD) в EN.
    Никогда «(сдвг)», «(окр)», «(ftd)».
 4. Латинские названия — не в основном тексте: иноязычное ТОЛЬКО в скобках при
    первом упоминании. Значит отдельной строки «Neurodevelopmental disorders»
    в русской версии быть не может; «Somatic Symptom Disorder (F45.1)» →
    «соматическое симптоматическое расстройство (somatic symptom disorder,
    F45.1)». Коды (F45.1, DSM-5, МКБ-11, XBT-11, ICD-11) — исключение.

Область проверки:
  · «меню и заголовки» — рейка .bk-sb, оглавление .bk-toc/.toc-ch/.tc-list,
    страх .bk-pn__t, хлебная крошка, шапка главы .bk-chead__h1/__en: правила 1–3.
  · «основной текст» — колонка чтения .bk-read: правило 4.

Единица счёта утечек — «английская простыня»: 2+ английских слова подряд вне
скобок, кавычек, span[lang=en], кодов и имён. Словарь — _tools/en-lexicon.txt
(слова английской версии книги) минус словарный запас самой версии.

Запуск:
    python _tools/klinik-register.py scan --out DIR        # отчёт + JSON
    python _tools/klinik-register.py scan --json DIR/x.json
    python _tools/klinik-register.py compare before.json after.json
"""
from __future__ import annotations

import argparse
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
if "--book" in sys.argv:                      # замер другого дерева (до/после)
    BOOK = os.path.abspath(sys.argv[sys.argv.index("--book") + 1])
VERSIONS = {"az": BOOK, "ru": os.path.join(BOOK, "ru"),
            "en": os.path.join(BOOK, "en"), "tr": os.path.join(BOOK, "tr")}
REGISTRY = {"abbreviatur.html", "terminoloji-luget.html"}
RE_LANG_DIR = None

# ── регион: где живёт текстовый узел ─────────────────────────────────────────
MENU_CLS = re.compile(r"\b(bk-row__t|bk-row__n|cls-tab|bk-crumb|bk-toc__t|bk-toc__n|"
                      r"bk-toc__g|tc-range|tc-head|tc-name|sc|nav-code|sub-code|"
                      r"bk-pn__t|bk-pn__dir|bk-chead__h1|bk-chead__en|bk-chead__n|"
                      r"bk-sb__back|bk-lang)\b")
READ_CLS = re.compile(r"\bbk-read\b")
CHEAD_CLS = re.compile(r"\bbk-chead\b")

RE_SCRIPT = re.compile(r"<(script|style)\b.*?</\1>", re.S | re.I)
RE_COMMENT = re.compile(r"<!--.*?-->", re.S)
RE_TAG = re.compile(r"<[^>]+>")
VOID = {"br", "hr", "img", "input", "meta", "link", "source", "col", "area",
        "wbr", "path", "rect", "circle", "use", "stop"}
# «C/С»-автокапитализация: строчное слово, одинокая заглавная, строчное слово
RE_CAP_MID = re.compile(r"(?<![^\W\d_])([^\W\d_]{2,})\s+([А-ЯЁӘĞŞÇÖÜİ])\s+([а-яёәəğıöşüç]{2,})",
                        re.U)
# аббревиатура в скобках, записанная строчными: «(сдвг)», «(okp)»
RE_PAREN_TOKEN = re.compile(r"\(([^()\s]{2,14})\)")

# ── канон аббревиатур по версиям (реестр книги abbreviatur.html) ─────────────
ABBR_CANON = {
    "ru": {"окр": "ОКР", "okp": "ОКР", "сдвг": "СДВГ", "adhd": "СДВГ",
           "ftd": "ЛВД", "лвд": "ЛВД", "птср": "ПТСР", "гтр": "ГТР",
           "дри": "ДРИ", "овр": "ОВР", "к-птср": "К-ПТСР", "кптср": "КПТСР",
           "bdd": "BDD", "ors": "ORS", "bed": "BED", "arfid": "ARFID",
           "ied": "IED", "mci": "MCI", "dlb": "DLB", "osa": "OSA", "ed": "ED",
           "pe": "PE", "hsdd": "HSDD", "dcd": "DCD", "pmdd": "PMDD",
           "мci": "MCI"},
    "az": {"ddhp": "DDHP", "okp": "OKP", "ftd": "FTD", "gad": "GAD",
           "bdd": "BDD", "kptsp": "KPTSP", "dip": "DİP", "ıed": "İED",
           "ied": "İED", "odd": "ODD", "asp": "ASP", "pmdd": "PMDD",
           "ptsp": "PTSP", "arfid": "ARFID", "dcd": "DCD", "adhd": "ADHD"},
    "en": {"ocd": "OCD", "asd": "ASD", "gad": "GAD", "bdd": "BDD", "ors": "ORS",
           "did": "DID", "bed": "BED", "arfid": "ARFID", "ied": "IED",
           "odd": "ODD", "mci": "MCI", "dlb": "DLB", "ftd": "FTD", "osa": "OSA",
           "ed": "ED", "pe": "PE", "hsdd": "HSDD", "adhd": "ADHD",
           "ptsd": "PTSD", "cptsd": "CPTSD", "pmdd": "PMDD", "dcd": "DCD"},
    "tr": {"okb": "OKB", "osb": "OSB", "dehb": "DEHB", "yab": "YAB",
           "bdd": "BDD", "ors": "ORS", "tssb": "TSSB", "ktssb": "KTSSB",
           "dkb": "DKB", "bed": "BED", "arfıd": "ARFID", "arfid": "ARFID",
           "ıed": "İED", "ied": "İED", "odd": "ODD", "mcı": "MCI", "dlb": "DLB",
           "ftd": "FTD", "osa": "OSA", "ed": "ED", "pe": "PE", "hsdd": "HSDD",
           "pmdd": "PMDD", "dcd": "DCD"},
}
# то же в верхнем регистре — «это аббревиатура, её не трогаем»
ABBR_OK = {lg: {k.upper(): v for k, v in m.items()} for lg, m in ABBR_CANON.items()}


def load_register_abbr():
    """Канон аббревиатур из реестра CASE-REGISTER.tsv (единый источник с casecheck)."""
    import csv
    p = os.path.join(ROOT, "CASE-REGISTER.tsv")
    if not os.path.exists(p):
        return
    with open(p, encoding="utf-8") as fh:
        rd = csv.reader(fh, delimiter="	")
        next(rd, None)
        for r in rd:
            if len(r) < 8 or r[5] != "ВСЕ ЗАГЛАВНЫЕ (аббревиатура)":
                continue
            for i, lg in enumerate(("ru", "az", "en", "tr"), start=1):
                v = r[i].strip()
                if v:
                    ABBR_OK[lg][v.upper()] = v
                    ABBR_CANON[lg][v.lower()] = v
            key = r[0].strip().lower()
            if key:
                for lg in ("ru", "az", "en", "tr"):
                    canon = r[{"ru": 1, "az": 2, "en": 3, "tr": 4}[lg]].strip()
                    if canon:
                        ABBR_CANON[lg][key] = canon


load_register_abbr()
# имена собственные и римские цифры, законные в любом регистре
NAMES_OK = {"I", "II", "III", "IV", "V", "VI", "VII", "VIII", "DSM", "DSM-5",
            "DSM-5-TR", "XBT", "XBT-11", "XBT-10", "ICD", "ICD-11", "ICD-10",
            "МКБ", "МКБ-11", "МКБ-10", "IDC", "ВОЗ", "WHO", "NICE", "СИОЗС",
            "СИОЗСН", "ТЦА", "СПИД", "ВИЧ", "IQ", "САН", "МРТ", "КТ", "ЭЭГ",
            "ЭКГ", "ЭСТ", "КПТ", "ДПТ", "ТОК", "ТПО", "ИМТ", "PHQ", "GAD",
            "MDD", "SARS", "COVID", "SLA", "NPT", "ЭПО", "ПЦР", "USA", "US",
            "UK", "EU", "KZ", "AZ", "RU", "EN", "TR"}
# страны/языки/файлы, которые не считаем дефектом — служебные подписи
ALLOW_TOKENS = {"НТЦ", "БКИ", "AZ", "EN", "RU", "TR", "ID", "URL", "HTML",
                "UTF", "LGBT", "HIV"}
# интернациональная медицинская лексика — не «английский термин»
INTL = set("""test risk plan faktor factor syndrome syndrom distress screening
score scale index patient compliance screening follow-up baseline checklist
placebo trauma stress coping relaps relapse random control case cohort study
session protocol mindfulness insight compliance adherence validity reliability
criteria criterion cluster dimension spectrum symptom somatic cognitive
behaviour behavior therapy therapist psychological psychiatry psychiatric
dementia delirium bipolar panic phobia anamnesis diagnosis prognosis
comorbidity epidemiology etiologi aetiology prevalence incidence survey
interview questionnaire scoring list item domain assessment inventory""".split())

RE_WORD = re.compile(
    r"[A-Za-z\u00C0-\u024F\u0400-\u04FF\u0130\u0131\u0259\u018F\u011E\u011F"
    r"\u015E\u015F\u00C7\u00E7\u00D6\u00F6\u00DC\u00FC]"
    r"[A-Za-z\u00C0-\u024F\u0400-\u04FF\u0130\u0131\u0259\u018F\u011E\u011F"
    r"\u015E\u015F\u00C7\u00E7\u00D6\u00F6\u00DC\u00FC'’\-]*")
EN_STOP = set("""the and or of with for in on by is are was were be been being not
no from to at as its their this that these those has have had can may will would
should could who whom whose which what when where why how than then there here
both each other another such only also more most less least very much many few
between among within without during after before under over about into out up
down first second third disorder disorders patient patients treatment symptoms
diagnosis criteria including included includes based according""".split())


# ── разбор HTML в текстовые узлы с контекстом ────────────────────────────────
def walk(html: str, prepared: bool = False):
    """Текстовые узлы с контекстом: stack тегов, глубина скобок/кавычек, смещение."""
    if not prepared:
        html = RE_SCRIPT.sub(" ", html)
        html = RE_COMMENT.sub(" ", html)
    stack = []          # [(tag, cls)]
    chunks = []         # (text, stack, off)
    pos = 0
    for m in re.finditer(r"<(/?)([a-zA-Z][a-zA-Z0-9]*)([^>]*?)(/?)>", html):
        if m.start() > pos:
            chunks.append((html[pos:m.start()], stack[:], pos))
        closing, tag, attrs, selfclose = m.group(1), m.group(2).lower(), m.group(3), m.group(4)
        if closing:
            for i in range(len(stack) - 1, -1, -1):
                if stack[i][0] == tag:
                    del stack[i:]
                    break
        elif tag not in VOID and not selfclose:
            cls = (re.search(r'class="([^"]*)"', attrs) or [None, ""])[1]
            stack.append((tag, cls))
        pos = m.end()
    if pos < len(html):
        chunks.append((html[pos:], stack[:], pos))
    out = []
    dp = dq = 0
    in_read = False
    last_blk = ""
    for text, st, off in chunks:
        # колонка чтения — самостоятельная область: счётчики скобок/кавычек в ней
        # начинаются заново (иначе чужая кавычка в рейке сбивает разбор текста)
        now_read = any("bk-read" in (c or "") for t, c in st)
        if now_read and not in_read:
            dp = dq = 0
        in_read = now_read
        blk = next((t for t, c in reversed(st) if t in
                    ("p", "li", "td", "th", "h1", "h2", "h3", "h4", "blockquote",
                     "figcaption", "caption")), "")
        if blk != last_blk:
            dp = dq = 0
            last_blk = blk
        out.append({"text": text, "stack": st, "paren": dp, "quote": dq, "off": off})
        for ch in text:
            if ch == "(":
                dp += 1
            elif ch == ")":
                dp = max(0, dp - 1)
            elif ch in "«“\"":
                dq += 1
            elif ch in "»”\"":
                dq = max(0, dq - 1)
    return out


def region_of(stack, text):
    """menu | chead | read | other."""
    outer = ""
    for tag, cls in stack:
        if tag in ("aside", "main", "div", "nav", "header", "footer", "p", "span", "h1", "h2", "h3", "li", "table", "section"):
            if "bk-chead__en" in cls:
                return "chead"
            if READ_CLS.search(cls):
                return "read"
            if MENU_CLS.search(cls):
                return "menu"
            if "bk-sb" in cls:
                return "menu"
            if "bk-toc" in cls or "toc-ch" in cls or "toc-preview" in cls or "tc-list" in cls:
                return "menu"
            if CHEAD_CLS.search(cls):
                outer = "chead"
    return "chead" if outer else "other"


# библиография: список источников сохраняет язык оригинала — это норма учебника
RE_BIB_ITEM = re.compile(r"(doi:|DOI|PMID|https?://|\bet al\.|"
                         r"\b(19|20)\d{2}[;:,)]|;\s*\d+\(\d+\))", re.U)


def bib_ranges(html: str):
    """Интервалы со ссылками на источники и чужими названиями — из проверки исключаются."""
    out = []
    for m in re.finditer(r"<(li|p)\b[^>]*>(.*?)</\1>", html, re.S | re.I):
        txt = H.unescape(RE_TAG.sub(" ", m.group(2)))
        if RE_BIB_ITEM.search(txt):
            out.append((m.start(), m.end()))
    for m in re.finditer(r'<(ol|ul|div)\b[^>]*class="[^"]*ref-list[^"]*"[^>]*>.*?</\1>',
                         html, re.S | re.I):
        out.append((m.start(), m.end()))
    # span lang="en" целиком — название шкалы/руководства/источника: латиница по праву
    for m in re.finditer(r'<span[^>]*lang="en"[^>]*>(.*?)</span>', html, re.S):
        body = H.unescape(RE_TAG.sub(" ", m.group(1)))
        if INSTRUMENT.search(body) or RE_BIB_ITEM.search(body):
            out.append((m.start(), m.end()))
    return out


def in_ranges(pos, ranges):
    return any(s <= pos < e for s, e in ranges)


def nodes_of(path):
    raw = open(path, encoding="utf-8").read()
    body = raw[raw.find("<body"):] if "<body" in raw else raw
    w = RE_SCRIPT.sub(" ", body)
    w = RE_COMMENT.sub(" ", w)
    return raw, w, walk(w, prepared=True)


# ── правило 1–3: регистр в меню и заголовках ─────────────────────────────────
def cap_tokens(s, lang):
    """Слова-КАПСЫ длиной 3+ (не аббревиатуры, не коды, не имена)."""
    bad = []
    for m in RE_WORD.finditer(s):
        w = m.group(0)
        for part in re.split(r"[-–—/]", w):
            core = part.strip("'’")
            if len(core) < 3 or not core.isalpha():
                continue
            if core.isupper() and core.upper() not in ABBR_OK[lang] \
                    and core not in NAMES_OK and core not in ALLOW_TOKENS:
                bad.append(part)
    return bad


def lower_start(s):
    m = re.match(r"[\s«„\"'(\[]*([^\W\d_]{3,})", s, re.U)
    if m and m.group(1)[0].islower():
        return m.group(1)
    return None


def cap_mid(s):
    return [f"{m.group(1)} {m.group(2)} {m.group(3)}" for m in RE_CAP_MID.finditer(s)]


def lower_abbr(s, lang):
    bad = []
    for m in RE_PAREN_TOKEN.finditer(s):
        tok = m.group(1)
        if tok.islower() and (tok.lower() in ABBR_CANON[lang]):
            bad.append(tok)
        elif tok.islower() and re.fullmatch(r"[a-zа-яёәəğıöşüç]{2,6}", tok) \
                and tok.upper() in ABBR_OK[lang]:
            bad.append(tok)
    return bad


# ── правило 4: «язык версии» в основном тексте ───────────────────────────────
# слова, после которых латинская строка — название инструмента/руководства,
# а не название расстройства на чужом языке (в учебнике это законная латиница)
INSTRUMENT = re.compile(r"\b(Test|Scale|Index|Inventory|Questionnaire|Checklist|"
                        r"Guideline|Guidelines|Manual|Criteria|Interview|Training|"
                        r"Rating|Schedule|Screen|Survey|Score|Assessment|"
                        r"Practice|Consensus|Reference|Guide|Study|Trial|Review|"
                        r"Association|Society|College|Academy|Journal|Medicine|"
                        r"Centre|Center|National|Institute|International|University|"
                        r"Foundation|Programme|Service|Council|Committee|Board|Studies|"
                        r"Psychiatry|Neurology|Pediatrics|Lancet|Report|Standards|"
                        r"Recommendations|Treatment|Diagnosis|Management|Protocol)\b")
# то, что владелец назвал прямо: одна латинская фраза = утечка
OWNER_TERMS = ["reassurance", "care-seeking", "care-avoiding", "doctor shopping",
               "single physician", "illness anxiety disorder",
               "somatic symptom disorder"]


def load_lexicon():
    p = os.path.join(ROOT, "_tools", "en-lexicon.txt")
    if not os.path.exists(p):
        return set()
    out = set()
    for line in open(p, encoding="utf-8"):
        w = line.strip().lower()
        if w.isalpha():
            out.add(w)
    return out


def en_disorder_names():
    """Английские названия расстройств — заголовки и пункты EN-версии."""
    names = set()
    folder = VERSIONS["en"]
    for f in sorted(os.listdir(folder)):
        if not f.endswith(".html"):
            continue
        t = open(os.path.join(folder, f), encoding="utf-8").read()
        for m in re.finditer(r'<span class="bk-row__t">(.*?)</span>', t):
            names.add(H.unescape(m.group(1)))
        m = re.search(r'<h1 class="bk-chead__h1">(.*?)</h1>', t, re.S)
        if m:
            names.add(H.unescape(m.group(1)))
    out = set()
    for n in names:
        n = re.sub(r"\s*\([^)]*\)\s*$", "", n).strip().lower()
        n = re.sub(r"^(with|without)\s+psychosis\s*—\s*", "", n)
        if len(n.split()) >= 2 and re.search(r"[a-z]{3,}", n):
            out.add(n)          # чисто-кодовые строки (F32–F34 · N94) — не названия
    out |= set(OWNER_TERMS)
    return out


def inside_quote(text, pos, depth=0):
    """Внутри кавычек: «…», “…” (однозначные пары) + глубина узла."""
    return depth + (text.count("«", 0, pos) - text.count("»", 0, pos)
                    + text.count("“", 0, pos) - text.count("”", 0, pos)) > 0


def en_term_hits(text, names, depth=0, qdepth=0):
    """Латинская фраза = английское название расстройства (иноязычная утечка).

    Строчная английская фраза в тексте версии — утечка. Латиница с Прописных —
    имя собственное (шкала, руководство, название из DSM/ICD) — латиница по праву.
    """
    low = text.lower()
    out = []
    for nm in names:
        i = low.find(nm)
        if i < 0:
            continue
        if inside_paren(text, i, depth) or inside_quote(text, i, qdepth):
            continue                     # в скобках или в кавычках — цитата названия
        if re.match(r"\s*-\s*\d", text[i + len(nm):]):
            continue                     # «Prolonged Grief Disorder-13» — имя шкалы
        if nm in OWNER_TERMS or not _titlecase(nm):
            out.append(nm)
    return out


def inside_paren(text, pos, depth=0):
    """Внутри скобок: стартовая глубина узла + баланс до позиции."""
    return depth + text.count("(", 0, pos) - text.count(")", 0, pos) > 0


def _titlecase(phrase):
    return all(w[0].isupper() for w in phrase.split() if w[:1].isalpha())


def native_vocab(folder):
    """Слова, реально встречающиеся в тексте версии (латиница/кириллица)."""
    v = Counter()
    for f in sorted(os.listdir(folder)):
        if not f.endswith(".html") or f in REGISTRY:
            continue
        _raw, _body, nodes = nodes_of(os.path.join(folder, f))
        for n in nodes:
            if region_of(n["stack"], n["text"]) == "other":
                continue
            for w in RE_WORD.findall(H.unescape(n["text"])):
                v[w.lower()] += 1
    return v


def en_runs2(text, lexi, native, lang):
    """Английские простыни с позицией: 2+ английских слова подряд."""
    out = []
    run, start = [], -1
    for m in RE_WORD.finditer(text):
        w = m.group(0)
        lw = w.lower()
        strong = lw in EN_STOP or (lw in lexi and native.get(lw, 0) == 0
                                   and lw not in INTL and len(lw) >= 4
                                   and not re.fullmatch(r"[A-Z]", w))
        if strong and not re.fullmatch(r"[A-Z]{1,5}\d*", w):
            if not run:
                start = m.start()
            run.append(w)
        else:
            if len(run) >= 2:
                out.append((run[:], start))
            run = []
    if len(run) >= 2:
        out.append((run[:], start))
    return out


def en_runs(text, lexi, native, lang):
    """Английские простыни: 2+ английских слова подряд."""
    out = []
    words = [(m.group(0), m.start(), m.end()) for m in RE_WORD.finditer(text)]
    run = []
    for w, s, e in words:
        lw = w.lower()
        strong = lw in EN_STOP or (lw in lexi and native.get(lw, 0) == 0
                                   and lw not in INTL and len(lw) >= 4
                                   and not re.fullmatch(r"[A-Z]", w))
        if strong and not re.fullmatch(r"[A-Z]{1,5}\d*", w):
            run.append(w)
        else:
            if len(run) >= 2:
                out.append(run[:])
            run = []
    if len(run) >= 2:
        out.append(run[:])
    return out


# ── scan ─────────────────────────────────────────────────────────────────────
def scan_file(path, rel, lang, lexi, native, names, detail):
    raw, body, nodes = nodes_of(path)
    bib = bib_ranges(body)
    res = {"register": [], "lang": []}
    for n in nodes:
        txt = n["text"]
        if not txt.strip():
            continue
        reg = region_of(n["stack"], txt)
        cls = " ".join(c for _, c in n["stack"])
        in_en = any('lang="en"' in (c or "") for t, c in n["stack"])
        if reg in ("menu", "chead"):
            plain = H.unescape(txt)
            for tok in cap_tokens(plain, lang):
                res["register"].append({"rule": "caps", "text": tok, "ctx": plain.strip()[:120]})
            ls = lower_start(plain.strip())
            if ls and not plain.strip().startswith(("«", '"')):
                res["register"].append({"rule": "lower_start", "text": ls,
                                        "ctx": plain.strip()[:120]})
            for cm in cap_mid(plain):
                res["register"].append({"rule": "cap_C", "text": cm, "ctx": plain.strip()[:120]})
            for la in lower_abbr(plain, lang):
                res["register"].append({"rule": "lower_abbr", "text": la,
                                        "ctx": plain.strip()[:120]})
            if lang != "en" and reg == "chead" and "bk-chead__en" in cls \
                    and plain.strip():
                res["lang"].append({"rule": "bare_en_line", "text": plain.strip()[:120],
                                    "ctx": plain.strip()[:120]})
        elif reg == "read":
            if lang == "en" or in_ranges(n["off"], bib):
                continue
            plain = H.unescape(txt)
            outside = n["paren"] == 0 and n["quote"] == 0
            if not outside:
                continue
            if in_en and INSTRUMENT.search(plain):
                continue                     # название шкалы/руководства — латиница по праву
            for nm in en_term_hits(plain, names, n["paren"], n["quote"]):
                res["lang"].append({"rule": "en_term", "text": nm,
                                    "ctx": plain.strip()[:160]})
            if not in_en:
                for run, pos in en_runs2(plain, lexi, native, lang):
                    if inside_paren(plain, pos, n["paren"]) or                             inside_quote(plain, pos, n["quote"]):
                        continue
                    res["lang"].append({"rule": "en_run", "text": " ".join(run),
                                        "ctx": plain.strip()[:160]})
    for kind, items in res.items():
        for it in items:
            it["file"] = rel
            it["kind"] = kind
            detail.append(it)
    return res


def en_enough(plain):
    """Латиница без пометки lang=en: 2+ английских слова подряд."""
    ws = [w for w in RE_WORD.findall(plain)
          if re.fullmatch(r"[A-Za-z][A-Za-z'’\-]+", w)]
    return len(ws) >= 2 and any(w.lower() in EN_STOP for w in ws)


def scan_version(lang, lexi, names, detail):
    folder = VERSIONS[lang]
    native = native_vocab(folder)
    per_file = Counter()
    counts = Counter()
    for f in sorted(os.listdir(folder)):
        if not f.endswith(".html") or f in REGISTRY:
            continue
        res = scan_file(os.path.join(folder, f), f, lang, lexi, native, names, detail)
        n = len(res["register"]) + len(res["lang"])
        if n:
            per_file[f] = n
        for it in res["register"]:
            counts["register:" + it["rule"]] += 1
        for it in res["lang"]:
            counts["lang:" + it["rule"]] += 1
    return counts, per_file


def cmd_scan(a):
    lexi = load_lexicon()
    names = en_disorder_names()
    report = {}
    print(f"{'версия':<8}{'регистр':>9}{'капс':>7}{'стр.с':>7}{'«С»':>7}"
          f"{'аббр':>7}{'англ.терм':>11}{'en-строка':>10}{'файлов':>8}")
    print("-" * 78)
    for lg in VERSIONS:
        detail = []
        counts, per_file = scan_version(lg, lexi, names, detail)
        print(f"{lg:<8}{sum(v for k, v in counts.items() if k.startswith('register')):>9}"
              f"{counts['register:caps']:>7}{counts['register:lower_start']:>7}"
              f"{counts['register:cap_C']:>7}{counts['register:lower_abbr']:>7}"
              f"{sum(v for k, v in counts.items() if k.startswith('lang:')):>11}"
              f"{counts['lang:bare_en_line']:>10}{len(per_file):>8}")
        report[lg] = {"register": sum(v for k, v in counts.items() if k.startswith("register")),
                      "lang": sum(v for k, v in counts.items() if k.startswith("lang")),
                      "by_rule": dict(counts), "files": len(per_file),
                      "detail": detail}
    r = {"versions": report}
    if a.json:
        os.makedirs(os.path.dirname(os.path.abspath(a.json)), exist_ok=True)
        json.dump(r, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"\nJSON: {a.json}")
    if a.out:
        os.makedirs(a.out, exist_ok=True)
        import csv
        p = os.path.join(a.out, "register-report.tsv")
        with open(p, "w", encoding="utf-8", newline="") as fh:
            w = csv.writer(fh, delimiter="\t", quoting=csv.QUOTE_ALL)
            w.writerow(["version", "kind", "rule", "file", "text", "context"])
            for lg, rep in report.items():
                for it in rep["detail"]:
                    w.writerow([lg, it["kind"], it["rule"], it["file"],
                                it["text"][:90], it["ctx"][:140]])
        print(f"TSV: {p}")
    return 0


def cmd_compare(a):
    b = json.load(open(a.before, encoding="utf-8"))["versions"]
    c = json.load(open(a.after, encoding="utf-8"))["versions"]
    print(f"{'версия':<7}{'регистр':>18}{'англ.':>16}")
    print(f"{'':<7}{'было':>9}{'стало':>9}{'было':>8}{'стало':>8}")
    print("-" * 40)
    for lg in VERSIONS:
        print(f"{lg:<7}{b[lg]['register']:>9}{c[lg]['register']:>9}"
              f"{b[lg]['lang']:>8}{c[lg]['lang']:>8}")
    return 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("scan")
    s.add_argument("--out")
    s.add_argument("--json")
    s.add_argument("--book")
    s.set_defaults(func=cmd_scan)
    c = sub.add_parser("compare")
    c.add_argument("before")
    c.add_argument("after")
    c.set_defaults(func=cmd_compare)
    a = ap.parse_args()
    return a.func(a)


if __name__ == "__main__":
    sys.exit(main())
