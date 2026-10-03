# -*- coding: utf-8 -*-
"""_tools/fix-class-tree-align.py — «Клиническая психиатрия»: деревья классификаций.

Жалоба владельца (2026-10-03): «ссылки глав ведут в неправильные адреса и
страницы»; заголовок группы в DSM-5-TR и МКБ-10 (28 496 ссылок, добавлены
2026-10-01) вёл на mundericat.html («Содержание») либо не совпадал с главой:
группы классификаций (F40–F48 и т.п.) шире одной главы книги, поэтому
«страница главы со списком её подглав» для них не находилась.

Что делает скрипт (идемпотентно, все языки AZ/RU/EN/TR, все страницы книги):
 1. Берёт за образец дерево XBT-11 — оно уже выровнено по главам книги
    (24 группы = 23 главы + строка «Məlumat bölməsi»).
 2. Пересобирает по этому образцу деревья DSM-5-TR и XBT-10: те же главы,
    те же названия (язык страницы), те же ссылки, порядок и раскрытие
    (data-here/is-on наследуются от XBT-11) — меняются только коды:
      * заголовок группы — код-диапазон главы в этой классификации
        (например «F40–F94», «F01–F05 · G30–G31»);
      * строка расстройства — код страницы в этой классификации.
 3. Источник кодов — таблица соответствий на самой странице расстройства
    (XBT-10/МКБ-10/ICD-10 и DSM-5-TR), пустой код — «—».
 4. Заголовок каждой группы ведёт на страницу главы со списком подглав —
    проверяется `_tools/check-klinik-links.py` (вердикт WRONG_SEC).

Запуск:
    python _tools/fix-class-tree-align.py --dry
    python _tools/fix-class-tree-align.py
"""
from __future__ import annotations

import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, "klinik-psixiatriya")
LANGS = ("", "ru", "en", "tr")

TREE_OPEN = '<div class="cls-tree" data-cls="%s"%s>'
CODE_LBL = ("XBT-10", "МКБ-10", "ICD-10")
SUB_RE = re.compile(
    r'(<a class="bk-row bk-row--sub[^"]*" href="(?P<href>[^"]+)">\s*'
    r'<span class="bk-row__n">)(?P<num>.*?)(</span>)')
SEC_RE = re.compile(
    r'(<a class="bk-row bk-row--sec[^"]*" href="(?P<href>[^"]+)">\s*'
    r'<span class="bk-row__n">)(?P<num>.*?)(</span>)')
LABEL_ROW_RE = re.compile(
    r'(?P<pre><a class="bk-row bk-row--(?P<kind>sub|sec|front)" href="(?P<href>[^"]+)"[^>]*>\s*'
    r'<span class="bk-row__n">)(?P<num>.*?)(?P<mid></span>\s*<span class="bk-row__t">)'
    r'(?P<name>.*?)(?P<post></span>)', re.S)


def clean(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s or "")).strip()


def tree_bounds(html, start):
    """Границы содержимого div.cls-tree (позиция после открывающего тега → конец)."""
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


def page_codes(path):
    html = open(path, encoding="utf-8", errors="replace").read()
    rows = re.findall(r'<span class="dh-lbl">(.*?)</span><span class="dh-code">(.*?)</span>', html)
    m = {}
    for lbl, code in rows:
        m[clean(lbl).upper()] = clean(code)
    xbt = next((m[k] for k in CODE_LBL if k in m), "")
    return xbt, m.get("DSM-5-TR", "")


def tokens(code):
    out = []
    for tok in re.split(r"[/+·,]", code or ""):
        m = re.match(r"^\s*([A-Za-z]+)(\d+)(?:\.(\d+))?", tok)
        if m:
            out.append((m.group(1).upper(), int(m.group(2)), int(m.group(3) or 0),
                        len(m.group(2))))
    return out


def range_label(codes, empty="—"):
    """Из кодов главы — подпись диапазона: «F40–F94», «F01–F05 · G30–G31»."""
    by = {}
    for c in codes:
        for letter, major, minor, width in tokens(c):
            by.setdefault(letter, []).append((major, minor, width))
    if not by:
        return empty
    parts = []
    for letter in sorted(by):
        vals = sorted(by[letter])
        lo, hi = vals[0], vals[-1]
        width = max(v[2] for v in vals)
        a = f"{letter}{lo[0]:0{width}d}"
        if lo[0] == hi[0]:
            parts.append(a)
        else:
            parts.append(f"{a}–{letter}{hi[0]:0{width}d}")
    return " · ".join(parts)


def build_tree(icd_inner, codes_of, chapter_range):
    """Копия дерева XBT-11 с кодами другой классификации."""
    def sub(m):
        href, num = m.group("href"), m.group("num")
        new = codes_of.get(href, None)
        if new is None:
            return m.group(1) + num + m.group(4)
        return m.group(1) + (new or "—") + m.group(4)

    def sec(m):
        href = m.group("href")
        new = chapter_range.get(href)
        return m.group(1) + (new if new else m.group("num")) + m.group(4)

    return SUB_RE.sub(sub, SEC_RE.sub(sec, icd_inner))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    n_files = n_sub = n_sec = n_fix = 0
    for lang in LANGS:
        d = os.path.join(BOOK, lang) if lang else BOOK
        pages = sorted(n for n in os.listdir(d) if n.endswith(".html"))
        codes = {}
        for n in pages:
            codes[n] = page_codes(os.path.join(d, n))
        # канонические подписи меню — с index.html той же версии
        canon = {}
        idx_html = open(os.path.join(d, "index.html"), encoding="utf-8", errors="replace").read()
        for m in re.finditer(r'<div class="cls-tree" data-cls="([a-z0-9]+)"([^>]*)>', idx_html):
            a, b = tree_bounds(idx_html, m.end())
            for r in LABEL_ROW_RE.finditer(idx_html[a:b]):
                canon[(m.group(1), r.group("kind"), r.group("href"))] = \
                    (r.group("num"), r.group("name"))
        for name in pages:
            path = os.path.join(d, name)
            html = open(path, encoding="utf-8", newline="").read()
            m = re.search(r'<div class="cls-tree" data-cls="icd"([^>]*)>', html)
            if not m:
                continue
            a, b = tree_bounds(html, m.end())
            icd_inner = html[a:b]
            chapters = {}
            for g in re.split(r'(?=<div class="bk-grp")', icd_inner)[1:]:
                h = re.search(r'bk-row--sec[^"]*" href="([^"]+)"', g)
                subs = re.findall(r'<a class="bk-row bk-row--sub"[^>]*href="([^"]+)"', g)
                if h:
                    chapters[h.group(1)] = subs
            new_blocks = {}
            for cls, idx in (("dsm", 1), ("icd10", 0)):
                codes_of = {n: codes[n][idx] for n in codes}
                chapter_range = {ch: range_label([codes[s][idx] for s in subs if s in codes])
                                 for ch, subs in chapters.items()}
                new_blocks[cls] = build_tree(icd_inner, codes_of, chapter_range)
            out = html
            for cls in ("dsm", "icd10"):
                mm = re.search(r'<div class="cls-tree" data-cls="%s"(\s+hidden)?>' % cls, out)
                if not mm:
                    continue
                x, y = tree_bounds(out, mm.end())
                if out[x:y] != new_blocks[cls]:
                    out = out[:x] + new_blocks[cls] + out[y:]
            # подписи меню → канонические (страницы словаря несли старую версию)
            def repl(r, cls):
                key = (cls, r.group("kind"), r.group("href"))
                ln, lname = canon.get(key, (r.group("num"), r.group("name")))
                return r.group("pre") + ln + r.group("mid") + lname + r.group("post")

            bounds = []
            for m2 in re.finditer(r'<div class="cls-tree" data-cls="([a-z0-9]+)"([^>]*)>', out):
                x, y = tree_bounds(out, m2.end())
                bounds.append((m2.group(1), x, y))
            for cls, x, y in sorted(bounds, key=lambda t: -t[1]):   # с конца, чтобы не сдвигать
                seg = out[x:y]
                before = [(r.group("num"), r.group("name")) for r in LABEL_ROW_RE.finditer(seg)]
                seg = LABEL_ROW_RE.sub(lambda r: repl(r, cls), seg)
                after = [(r.group("num"), r.group("name")) for r in LABEL_ROW_RE.finditer(seg)]
                n_fix += sum(1 for p, q in zip(before, after) if p != q)
                out = out[:x] + seg + out[y:]
            if out != html:
                n_files += 1
                n_sub += len(re.findall(r'<a class="bk-row bk-row--sub', new_blocks["dsm"]))
                n_sec += len(re.findall(r'<a class="bk-row bk-row--sec', new_blocks["dsm"]))
                if not args.dry:
                    with open(path, "w", encoding="utf-8", newline="") as f:
                        f.write(out)
    mode = "DRY" if args.dry else "OK"
    print(f"[{mode}] языков: {len(LANGS)}; страниц изменено: {n_files}; "
          f"строк подглав переписано (DSM): {n_sub}; заголовков групп: {n_sec}; "
          f"подписей меню выровнено: {n_fix}")


if __name__ == "__main__":
    main()
