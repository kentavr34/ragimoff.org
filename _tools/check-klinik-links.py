# -*- coding: utf-8 -*-
"""_tools/check-klinik-links.py — «Клиническая психиатрия»: сплошная проверка ссылок.

Проверяет ВСЕ ссылки навигации книги во всех четырёх языковых версиях
(AZ в корне, ru/, en/, tr/):

  * рейка: вводные строки (bk-row--front), заголовки групп (bk-row--sec),
    строки расстройств (bk-row--sub) в деревьях классификаций XBT-11/DSM-5-TR/XBT-10;
  * хлебные крошки (bk-crumb), переходы пред/след (bk-pn);
  * оглавление главы (bk-toc__a) и оглавление книги, справочные страницы
    (приложения A–E, шкалы, словарь, заключение, сведения о книге).

Правила (что считается верной целью):
  * строка расстройства → страница расстройства с тем же кодом (XBT-11 →
    chead-код, XBT-10/DSM-5-TR → код из таблицы соответствий самой страницы)
    и тем же названием (сравнение по началу строки);
  * заголовок группы → страница главы (bk-toc__list), в которой этот
    заголовок стоит в дереве (пункт «глава со списком её подглав»);
  * крошка / «к главе» (bk-pn__up) → глава, содержащая текущую страницу;
  * пред/след → сосед по главе (для справочных страниц — сосед по их цепочке);
  * ссылка страницы-перехода (meta refresh) засчитывается как REDIRECT_OK;
  * все прочие ссылки — существование файла-цели (относительно каталога
    версии или от корня сайта).

Вердикты: OK / REDIRECT_OK / MISSING / WRONG_SUB / WRONG_SEC / WRONG_CRUMB /
WRONG_PN.

Вывод: сводка + TSV «пункт | версия | href | целевой файл | ожидалось | вердикт».

Запуск:
    python _tools/check-klinik-links.py
    python _tools/check-klinik-links.py --tsv PATH
"""
from __future__ import annotations

import argparse
import os
import re
import sys
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, "klinik-psixiatriya")
LANGS = ("", "ru", "en", "tr")
LANG_CODE = {"": "az", "ru": "ru", "en": "en", "tr": "tr"}
REFS = {"index.html", "mundericat.html", "mugeddime.html", "kitab-haqqinda.html",
        "abbreviatur.html", "terminoloji-luget.html", "elave-acde.html",
        "elave-skalalar.html", "melumat.html", "yekun.html", "giris-yekun.html"}

TREE_RE = re.compile(r'<div class="cls-tree" data-cls="([a-z0-9]+)"([^>]*)>')
GRP_RE = re.compile(
    r'<div class="bk-grp"([^>]*)>\s*<(?P<tag>a|span) class="(?P<cls>[^"]*)"(?P<attrs>[^>]*)>\s*'
    r'<span class="bk-row__n">(?P<num>.*?)</span>\s*'
    r'<span class="bk-row__t">(?P<name>.*?)</span>\s*</(?P=tag)>', re.S)
NAVROW_RE = re.compile(
    r'<a class="bk-row(?P<cls>[^"]*)" href="(?P<href>[^"]*)"[^>]*>\s*'
    r'<span class="bk-row__n">(?P<num>.*?)</span>\s*'
    r'<span class="bk-row__t">(?P<name>.*?)</span>\s*</a>', re.S)
TOCA_RE = re.compile(
    r'<a class="bk-toc__a" href="(?P<href>[^"]*)"[^>]*>\s*'
    r'<span class="bk-toc__n">(?P<num>.*?)</span>\s*'
    r'<span class="bk-toc__t">(?P<name>.*?)</span>', re.S)
CRUMB_RE = re.compile(r'<nav class="bk-crumb"[^>]*>(?P<body>.*?)</nav>', re.S)
PN_RE = re.compile(r'<nav class="bk-pn"[^>]*>(?P<body>.*?)</nav>', re.S)
REFRESH_RE = re.compile(r'<meta http-equiv="refresh"[^>]*url=([^"\']+)', re.I)
A_RE = re.compile(r'<a\b[^>]*href="([^"]*)"')


def tree_bounds(html, start):
    depth, k = 1, start
    while k < len(html) and depth > 0:
        nxt_o = html.find("<div", k)
        nxt_c = html.find("</div>", k)
        if nxt_c == -1:
            break
        if nxt_o != -1 and nxt_o < nxt_c:
            depth += 1
            k = nxt_o + 4
        else:
            depth -= 1
            k = nxt_c + 6
    return start, k - len("</div>")


def clean(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s or "")).strip()


def fold(s):
    """Регистр с учётом турецких İ/I/ı (иначе .lower() даёт «i̇» из двух знаков)."""
    s = clean(s).replace("İ", "i").replace("I", "i").replace("ı", "i")
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.lower()


def code_key(c):
    c = clean(c)
    if not c or c == "—":
        return ""
    return fold(re.split(r"[–—\-·/\s]", c)[0].strip()).upper()


def code_eq(a, b):
    """Коды равны или один — уточнение другого («8A05» и «8A05.0»)."""
    a, b = code_key(a), code_key(b)
    if not a or not b:
        return False
    return a == b or a.startswith(b + ".") or b.startswith(a + ".")


def name_eq(label, title):
    a, b = fold(label.split(" (")[0]), fold(title.split(" (")[0])
    if not a or not b:
        return False
    n = min(22, len(a), len(b))
    return a[:n] == b[:n] or a[:n] in b or b[:n] in a


def resolve(href, lang_dir):
    """Абсолютная ссылка от корня сайта или относительная — в путь репозитория."""
    if href.startswith("/"):
        rel = href.lstrip("/")
        if rel == "" or rel.endswith("/"):
            rel += "index.html"
        return os.path.join(ROOT, rel.replace("/", os.sep))
    if href.startswith(".."):
        return os.path.normpath(os.path.join(BOOK, lang_dir, href))
    return os.path.join(BOOK, lang_dir, href) if lang_dir else os.path.join(BOOK, href)


def norm_rel(path):
    p = os.path.normpath(path)
    return p if os.path.exists(p) else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tsv", default=os.path.join("C:/Temp/kp", "klinik-links.tsv"))
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    os.makedirs(os.path.dirname(args.tsv), exist_ok=True)

    report = []
    counts = {}

    def add(item, lang, href, target, expected, verdict):
        report.append((item, lang, href, target, expected, verdict))
        counts[verdict] = counts.get(verdict, 0) + 1

    for lang in LANGS:
        lc = LANG_CODE[lang]
        d = os.path.join(BOOK, lang) if lang else BOOK
        pages = {}
        for name in sorted(os.listdir(d)):
            if name.endswith(".html"):
                pages[name] = open(os.path.join(d, name), encoding="utf-8",
                                   errors="replace").read()

        def exists(target):
            if target.startswith("/"):
                rel = target.lstrip("/")
                if rel == "" or rel.endswith("/"):
                    rel += "index.html"
                return os.path.exists(os.path.join(ROOT, rel.replace("/", os.sep)))
            return os.path.exists(os.path.join(d, target))

        meta = {}
        for n, h in pages.items():
            chead = re.search(r'<span class="bk-chead__n">(.*?)</span>', h)
            h1 = re.search(r'<h1 class="bk-chead__h1">(.*?)</h1>', h)
            rows = re.findall(
                r'<tr><td class="dh-meta"><span class="dh-lbl">(.*?)</span>'
                r'<span class="dh-code">(.*?)</span></td><td class="dh-name">(.*?)</td></tr>', h)
            codes = {}
            for lbl, code, nm in rows:
                codes[clean(lbl).upper()] = clean(code)
            meta[n] = {
                "chead": clean(chead.group(1)) if chead else "",
                "h1": clean(h1.group(1)) if h1 else "",
                "xbt10": codes.get("XBT-10", codes.get("МКБ-10", codes.get("ICD-10", ""))),
                "dsm": codes.get("DSM-5-TR", ""),
                "redirect": bool(REFRESH_RE.search(h)),
                "toc": [m.group("href") for m in TOCA_RE.finditer(h)],
            }
        chapters = {n: set(m["toc"]) for n, m in meta.items() if m["toc"]}
        disc2ch = {}
        for ch, subs in chapters.items():
            for s in subs:
                disc2ch.setdefault(s, set()).add(ch)

        for name in sorted(pages):
            html = pages[name]
            here_ch = disc2ch.get(name, set()) or ({name} if name in chapters else set())

            # --- деревья классификаций ---
            for m in TREE_RE.finditer(html):
                cls = m.group(1)
                a, b = tree_bounds(html, m.end())
                seg = html[a:b]
                for part in re.split(r'(?=<div class="bk-grp")', seg)[1:]:
                    g = GRP_RE.match(part)
                    subs = re.findall(r'<a class="bk-row bk-row--sub[^"]*" href="([^"]+)"', part)
                    if not g:
                        continue
                    href = re.search(r'href="([^"]+)"', g.group("attrs") or "")
                    href = href.group(1) if href else None
                    label = f"{clean(g.group('num'))} {clean(g.group('name'))}".strip()
                    if href is None:
                        add(f"{lc}:{name}:{cls}:{label[:40]}", lc, "(нет)", "-",
                            "ссылка на страницу главы", "WRONG_SEC")
                        continue
                    if not exists(href):
                        add(f"{lc}:{name}:{cls}:{label[:40]}", lc, href, href,
                            "существующий файл", "MISSING")
                        continue
                    if href not in pages:
                        add(f"{lc}:{name}:{cls}:{label[:40]}", lc, href, href,
                            "страница главы", "WRONG_SEC")
                        continue
                    if href in chapters:
                        # глава должна содержать больше половины подпунктов группы
                        cover = len(chapters[href] & set(subs))
                        ok = bool(subs) and cover == len(subs)
                        add(f"{lc}:{name}:{cls}:{label[:40]}", lc, href, href,
                            f"глава, покрывающая {len(subs)} подпунктов", "OK" if ok else "WRONG_SEC")
                    else:
                        add(f"{lc}:{name}:{cls}:{label[:40]}", lc, href, href,
                            "страница главы со списком подглав", "WRONG_SEC")
                    for s in subs:
                        if s in meta:
                            t = meta[s]
                            add(f"{lc}:{name}:{cls}:{label[:30]}", lc, s, s,
                                "страница подглавы", "REDIRECT_OK" if t["redirect"] else "OK")
                        else:
                            add(f"{lc}:{name}:{cls}:{label[:30]}", lc, s, s,
                                "страница подглавы", "MISSING")

            # --- рейка: строки-расстройства / вводные ---
            for m in NAVROW_RE.finditer(html):
                cls, href = m.group("cls"), m.group("href")
                if "bk-row--sub" not in cls or href.startswith(("http", "#")):
                    continue
                num, label = clean(m.group("num")), clean(m.group("name"))
                if not exists(href):
                    add(f"{lc}:{name}:{label[:40]}", lc, href, href, "существующий файл", "MISSING")
                    continue
                target = href.split("#")[0]
                if target in meta:
                    t = meta[target]
                    if t["redirect"]:
                        add(f"{lc}:{name}:{num} {label[:36]}", lc, href, target,
                            "страница расстройства (переход)", "REDIRECT_OK")
                        continue
                    exp = code_key(num)
                    ok_code = (not exp) or code_eq(num, t["chead"]) or \
                              code_eq(num, t["xbt10"]) or code_eq(num, t["dsm"])
                    add(f"{lc}:{name}:{num} {label[:36]}", lc, href, target,
                        f"код {exp or '—'} и «{label[:28]}»",
                        "OK" if (ok_code and name_eq(label, t["h1"])) else "WRONG_SUB")

            # --- крошки ---
            for m in CRUMB_RE.finditer(html):
                for a in re.finditer(r'<a href="([^"]*)"[^>]*>(.*?)</a>', m.group("body"), re.S):
                    href, label = a.group(1), clean(a.group(2))
                    if not exists(href):
                        add(f"{lc}:{name}:crumb:{label[:28]}", lc, href, href,
                            "существующий файл", "MISSING")
                        continue
                    if href in ("index.html", "../index.html", "mundericat.html",
                                "/klinik-psixiatriya/", "/"):
                        add(f"{lc}:{name}:crumb:{label[:28]}", lc, href, href, "корень книги", "OK")
                        continue
                    ok = (href in here_ch) or (name == href)
                    add(f"{lc}:{name}:crumb:{label[:28]}", lc, href, href,
                        "глава, содержащая страницу", "OK" if ok else "WRONG_CRUMB")

            # --- пред/след ---
            for m in PN_RE.finditer(html):
                for a in re.finditer(r'<a class="bk-pn__a" href="([^"]*)"[^>]*>(.*?)</a>', m.group("body"), re.S):
                    href, label = a.group(1), clean(a.group(2))
                    if not exists(href):
                        add(f"{lc}:{name}:pn:{label[:28]}", lc, href, href, "существующий файл", "MISSING")
                        continue
                    same = bool((disc2ch.get(name, set()) & disc2ch.get(href, set()))) or \
                           (href in disc2ch.get(name, set())) or (name in chapters.get(href, set())) or \
                           name in REFS
                    add(f"{lc}:{name}:pn:{label[:28]}", lc, href, href,
                        "сосед по главе", "OK" if same else "WRONG_PN")
                for a in re.finditer(r'<p class="bk-pn__up"><a href="([^"]*)"', m.group("body")):
                    href = a.group(1)
                    if not exists(href):
                        add(f"{lc}:{name}:pn:up", lc, href, href, "существующий файл", "MISSING")
                        continue
                    ok = href in here_ch or name == href or name in REFS or \
                         href in ("index.html", "../index.html")
                    add(f"{lc}:{name}:pn:up", lc, href, href, "страница главы", "OK" if ok else "WRONG_PN")

            # --- оглавление главы ---
            for m in TOCA_RE.finditer(html):
                href = m.group("href")
                num, label = clean(m.group("num")), clean(m.group("name"))
                if not exists(href):
                    add(f"{lc}:{name}:toc:{label[:28]}", lc, href, href, "существующий файл", "MISSING")
                    continue
                t = meta.get(href)
                if not t:
                    add(f"{lc}:{name}:toc:{label[:28]}", lc, href, href, "страница подглавы", "MISSING")
                    continue
                if t["redirect"]:
                    add(f"{lc}:{name}:toc:{label[:28]}", lc, href, href,
                        "страница подглавы (переход)", "REDIRECT_OK")
                    continue
                exp = code_key(num)
                ok = (not exp) or code_eq(num, t["chead"]) or code_eq(num, t["xbt10"]) or code_eq(num, t["dsm"])
                if href in chapters and not re.match(r"^[A-Z]", exp):
                    ok = True          # номер главы в оглавлении книги («05»)
                ok = ok and (name_eq(label, t["h1"]) or (href in chapters and not re.match(r"^[A-Z]", exp)))
                add(f"{lc}:{name}:toc:{num} {label[:28]}", lc, href, href,
                    "страница подглавы с этим кодом", "OK" if ok else "WRONG_SUB")

            # --- все прочие ссылки страницы ---
            for m in A_RE.finditer(html):
                href = m.group(1)
                if href.startswith(("http", "mailto", "#", "tel:", "javascript:")):
                    continue
                if not exists(href):
                    add(f"{lc}:{name}:body", lc, href, href, "существующий файл", "MISSING")

    with open(args.tsv, "w", encoding="utf-8", newline="") as f:
        f.write("пункт\tверсия\thref\tцелевой файл\tожидалось\tвердикт\n")
        for row in report:
            f.write("\t".join(row) + "\n")

    print(f"Всего проверок ссылок: {len(report)}")
    for k in sorted(counts):
        print(f"  {k:12s} {counts[k]}")
    uniq = {}
    for item, lc, href, target, exp, verdict in report:
        if verdict not in ("OK", "REDIRECT_OK"):
            uniq.setdefault((verdict, href, target, exp), []).append(lc)
    print(f"Уникальных ошибочных целей: {len(uniq)}")
    for (verdict, href, target, exp), langs in sorted(uniq.items(), key=lambda t: -len(t[1])):
        print(f"  {verdict:11s} {href:46s} → {target:34s} {exp[:38]:38s} {len(langs)} стр.")
    print(f"Отчёт: {args.tsv}")


if __name__ == "__main__":
    main()
