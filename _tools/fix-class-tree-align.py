# -*- coding: utf-8 -*-
"""_tools/fix-class-tree-align.py — «Клиническая психиатрия»: деревья классификаций (рейка + оглавление).

ВЕРСИЯ 2026-11-07 (замена версии от 2026-10-03). Что изменилось и почему.
Старая версия копировала дерево XBT-11 (23 главы МКБ-11) в DSM-5-TR и XBT-10, меняя только коды;
заголовок группы = размах min–max кодов подпунктов («F40–F94», «F42–F63», «F52–F63»), названия
глав — МКБ-11. Такие блоки не существуют ни в МКБ-10, ни в DSM-5-TR (проверка CODES_CHECK_AZ_20261107).

Теперь:
  * XBT-11  — как раньше: 23 главы МКБ-11 (в оригинале дерево строится в другом месте, здесь
              правятся только подписи диапазонов глав по МКБ-11 ВОЗ);
  * XBT-10  — настоящие блоки МКБ-10 ВОЗ: F00–F09, F10–F19, … F90–F98, F99 + группы «G47 · N94»
              (коды вне главы V) и «—» (нет соответствия). Блок страницы определяется по коду XBT-10
              из таблицы соответствий страницы;
  * DSM-5-TR — главы DSM-5-TR (состав задан явно в _tools/klinik_class_groups.json), подпись
              группы — перечень кодов её подпунктов («F40–F41 · F93–F94»), не размах;
  * заголовок группы XBT-10/DSM-5-TR ведёт на mundericat.html (оглавление с теми же группами);
  * подпункты — коды из таблиц соответствий страниц (XBT-10 / DSM-5-TR), «—» если кода нет;
  * то же дерево на всех страницах книги (меняется только раскрытая группа и подсветка);
  * оглавление mundericat.html: панели XBT-10 и DSM-5-TR пересобираются из тех же групп.
Названия блоков/глав на языках AZ/RU/EN/TR — в _tools/klinik_class_groups.json.

Запуск (идемпотентно, все языки):
    python _tools/fix-class-tree-align.py --dry
    python _tools/fix-class-tree-align.py
"""
from __future__ import annotations

import argparse
import html as htmllib
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, "klinik-psixiatriya")
LANGS = ("", "ru", "en", "tr")
LKEY = {"": "az", "ru": "ru", "en": "en", "tr": "tr"}
GROUPS = json.load(open(os.path.join(ROOT, "_tools", "klinik_class_groups.json"), encoding="utf-8"))

CODE_LBL = ("XBT-10", "МКБ-10", "ICD-10")
# подписи диапазонов глав МКБ-11 (дерево XBT-11), уточнены по ВОЗ (ICD API 2024-01)
SEC11_FIX = {
    "03-6A4-katatoniya.html": "6A40–6A4Z",
    "04-6A6-ehval-pozuntulari.html": "6A60–6A8Z",
    "11-6C2-bedensel-disstres.html": "6C20–6C2Z",
    "22-7AB-yuxu.html": "7A00–7B2Z",
    "23-HA-cinsi-saglamliq.html": "HA00–HA2Z · HA40",
}
SEC11_FIX_TOC = {  # то же, как подписано в оглавлении (tc-range)
    "03-6A4-katatoniya.html": "6A40–6A4Z",
    "04-6A6-ehval-pozuntulari.html": "6A60–6A8Z",
    "11-6C2-bedensel-disstres.html": "6C20–6C2Z",
    "22-7AB-yuxu.html": "7A00–7B2Z",
    "23-HA-cinsi-saglamliq.html": "HA00–HA2Z · HA40",
}
TOC_TARGET = "mundericat.html"

TREE_RE = re.compile(r'<div class="cls-tree" data-cls="([a-z0-9]+)"([^>]*)>')
SUBROW_RE = re.compile(r'<a class="bk-row bk-row--sub[^"]*" href="(?P<href>[^"]+)">.*?</a>', re.S)
SECROW_RE = re.compile(r'<a class="bk-row bk-row--sec[^"]*" href="(?P<href>[^"]+)"><span class="bk-row__n">(?P<num>.*?)</span>'
                       r'(?P<mid><span class="bk-row__t">)(?P<name>.*?)(?P<post></span>\s*</a>)', re.S)
NUM_RE = re.compile(r'(<span class="bk-row__n">)(.*?)(</span>)', re.S)
TOGGLE_RE = re.compile(r'<button class="bk-tgl"[^>]*>.*?</button>', re.S)


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
            out.append((m.group(1).upper(), int(m.group(2)), int(m.group(3) or 0), len(m.group(2))))
    return out


def sort_key(code, order):
    t = tokens(code)
    if not t:
        return (1, "", 0, 0, order)
    return (0, t[0][0], t[0][1], t[0][2], order)


def icd10_block(code):
    """Индекс блока МКБ-10 ВОЗ по коду страницы или None (группа вне главы V / нет кода)."""
    t = tokens(code)
    if not t:
        return "none"
    letter, major = t[0][0], t[0][1]
    if letter == "F":
        if major == 99:
            return 10
        return min(major // 10, 9)  # F00–F09 → 0 … F90–F98 → 9
    return "g47n94"


def dsm_label(codes):
    """Подпись главы DSM: перечень диапазонов кодов подпунктов; при >4 фрагментов — общий размах."""
    by = {}
    for c in codes:
        for letter, major, minor, width in tokens(c):
            if letter not in ("F", "G"):
                continue   # L98.1 (кожа) и т.п. — не коды психических глав
            by.setdefault(letter, set()).add((major, width))
    if not by:
        return "—"
    segs, spans = [], []
    for letter in sorted(by):
        vals = sorted(by[letter])
        width = max(v[1] for v in vals)
        lo = prev = vals[0][0]
        run = []
        for major, _ in vals[1:]:
            if major - prev <= 2:
                prev = major
                continue
            run.append((lo, prev))
            lo = prev = major
        run.append((lo, prev))
        for a, b in run:
            segs.append(f"{letter}{a:0{width}d}" + (f"–{letter}{b:0{width}d}" if b != a else ""))
        spans.append(f"{letter}{vals[0][0]:0{width}d}" + (f"–{letter}{vals[-1][0]:0{width}d}" if vals[-1][0] != vals[0][0] else ""))
    return " · ".join(segs if len(segs) <= 4 else spans)


def build_groups(lang, subs_order, codes, titles=None):
    """→ {'icd10': [(range, name, [hrefs])...], 'dsm': [...]}; subs_order — порядок страниц в дереве XBT-11."""
    key = LKEY[lang]
    order = {h: i for i, h in enumerate(subs_order)}
    g10 = GROUPS["icd10"][key]
    icd10 = []
    blocks = [[r, n, []] for r, n in g10["blocks"]]
    extra = {"g47n94": [g10["g47n94"][0], g10["g47n94"][1], []], "none": [g10["none"][0], g10["none"][1], []]}
    for h in subs_order:
        b = icd10_block(codes[h][0])
        (extra[b][2] if isinstance(b, str) else blocks[b][2]).append(h)
    for grp in blocks + [extra["g47n94"], extra["none"]]:
        grp[2].sort(key=lambda h: sort_key(codes[h][0], order[h]))
        if grp[2] or grp[0] == "F99":
            icd10.append(tuple(grp))
    dsm = []
    for i, members in enumerate(GROUPS["dsm"]["members"]):
        hs = [m + ".html" for m in members if m + ".html" in codes]
        hs.sort(key=lambda h: sort_key(codes[h][1], order.get(h, 0)))
        dsm.append((dsm_label([codes[h][1] for h in hs]), GROUPS["dsm"][key]["names"][i], hs))
    return {"icd10": icd10, "dsm": dsm}


def esc(s):
    return s  # названия уже в виде HTML-текста


def render_tree(cls, groups, subrow, sectpl, toggle, here, nl):
    """Разметка содержимого cls-tree."""
    out = []
    for i, (rng, name, hs) in enumerate(groups):
        is_here = "1" if any(h in here for h in hs) else "0"
        parts = [f'<div class="bk-grp" data-slug="{cls}-{i + 1:02d}" data-here="{is_here}">',
                 f'<a class="bk-row bk-row--sec" href="{TOC_TARGET}"><span class="bk-row__n">{rng}</span>'
                 f'<span class="bk-row__t">{name}</span>', "</a>"]
        if hs:
            parts.append(toggle)
            parts.append('<div class="bk-grp__sub">')
            for h in hs:
                parts.append(subrow(h, cls))
            parts.append("</div>")
        parts.append("</div>")
        out.append(nl.join(parts))
    return nl.join(out)


def collect_titles(panels_html):
    t = {}
    for h, n in re.findall(r'<a href="([^"]+\.html)"><span class="sc">[^<]*</span><span>([^<]*)</span>', panels_html):
        t.setdefault(h, n)
    return t


def render_panel(cls, groups, codes_idx, titles, empty_txt, nl=""):
    parts = []
    for rng, name, hs in groups:
        items = "".join(f'<a href="{h}"><span class="sc">{codes_idx(h) or "—"}</span><span>{titles[h]}</span></a>' for h in hs)
        if not items:
            items = f'<div class="tc-empty">{empty_txt}</div>'
        parts.append(f'<div class="toc-ch"><div class="tc-head"><span class="tc-range">{rng}</span><span>{name}</span></div>'
                     f'<div class="tc-list">{items}</div></div>')
    return "".join(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    n_files = 0
    for lang in LANGS:
        d = os.path.join(BOOK, lang) if lang else BOOK
        pages = sorted(n for n in os.listdir(d) if n.endswith(".html"))
        codes = {n: page_codes(os.path.join(d, n)) for n in pages}
        codes = {n: c for n, c in codes.items() if c != ("", "")}
        # --- эталонный порядок и список страниц расстройств: дерево XBT-11 индекса ---
        idx = open(os.path.join(d, "index.html"), encoding="utf-8", errors="replace").read()
        m = TREE_RE.search(idx)
        a, b = tree_bounds(idx, m.end())
        subs_order = [h for h in dict.fromkeys(x.group("href") for x in SUBROW_RE.finditer(idx[a:b])) if h in codes]
        groups = build_groups(lang, subs_order, codes)
        # --- оглавление: пересобрать панели ---
        toc_path = os.path.join(d, "mundericat.html")
        toc = open(toc_path, encoding="utf-8", newline="").read()
        titles = collect_titles(toc)
        empty_txt = (re.search(r'<div class="tc-empty">([^<]*)</div>', toc) or [0, "—"])[1]
        new_toc = toc
        for cls, idxc in (("dsm", 1), ("icd10", 0)):
            pm = re.search(r'(<div class="cls-panel" data-cls="%s"[^>]*><p class="toc-meta">)([^<]*)(</p><div class="toc-preview">)' % cls, new_toc)
            if not pm:
                print("!! нет панели", cls, lang)
                continue
            s0 = pm.end()
            # конец toc-preview: баланс div, начиная сразу после открывающего <div class="toc-preview">
            e0, e1 = tree_bounds(new_toc, s0)
            body = render_panel(cls, groups[cls], lambda h: codes[h][idxc], titles, empty_txt)
            meta = re.sub(r"\d+(\s*\S+\s*)$", lambda mm: "%d%s" % (len(groups[cls]), mm.group(1)), pm.group(2)) if re.search(r"\d+\s*\S+\s*$", pm.group(2)) else pm.group(2)
            new_toc = new_toc[:pm.start(2)] + meta + new_toc[pm.end(2):s0] + body + new_toc[e1:]
        # диапазоны глав XBT-11 в панели icd
        for href, rng in SEC11_FIX_TOC.items():
            new_toc = re.sub(r'(<a href="%s"><span class="tc-range">)[^<]*(</span>)' % re.escape(href), lambda mm: mm.group(1) + rng + mm.group(2), new_toc)
        if new_toc != toc:
            n_files += 1
            if not args.dry:
                with open(toc_path, "w", encoding="utf-8", newline="") as f:
                    f.write(new_toc)
        # --- деревья рейки на каждой странице ---
        for name in pages:
            path = os.path.join(d, name)
            html = open(path, encoding="utf-8", newline="").read()
            m = re.search(r'<div class="cls-tree" data-cls="icd"([^>]*)>', html)
            if not m:
                continue
            nl = "\r\n" if "\r\n" in html else "\n"
            a, b = tree_bounds(html, m.end())
            icd_inner = html[a:b]
            # образцы разметки из дерева XBT-11 этой страницы
            rows = {x.group("href"): x.group(0) for x in SUBROW_RE.finditer(icd_inner)}
            tgl = TOGGLE_RE.search(icd_inner)
            toggle = tgl.group(0) if tgl else ""
            here = set()
            for g in re.split(r'(?=<div class="bk-grp")', icd_inner)[1:]:
                if re.search(r'data-here="1"', g[:120]):
                    here |= set(x.group("href") for x in SUBROW_RE.finditer(g))
            if name in codes:
                here.add(name)

            def subrow(h, cls, _rows=rows):
                row = _rows.get(h)
                if row is None:
                    return ""
                idxc = 1 if cls == "dsm" else 0
                code = codes[h][idxc] or "—"
                return NUM_RE.sub(lambda mm: mm.group(1) + code + mm.group(3), row, count=1)

            out = html
            # ICD-11: подписи диапазонов глав
            def fix_sec(mm):
                new = SEC11_FIX.get(mm.group("href"))
                if not new:
                    return mm.group(0)
                return mm.group(0).replace('<span class="bk-row__n">' + mm.group("num") + "</span>", '<span class="bk-row__n">' + new + "</span>", 1)
            new_icd = SECROW_RE.sub(fix_sec, icd_inner)
            if new_icd != icd_inner:
                out = out[:a] + new_icd + out[b:]
            for cls in ("dsm", "icd10"):
                mm = re.search(r'<div class="cls-tree" data-cls="%s"(\s+hidden)?>' % cls, out)
                if not mm:
                    continue
                x, y = tree_bounds(out, mm.end())
                new_inner = render_tree(cls, groups[cls], subrow, None, toggle, here, nl)
                if out[x:y] != new_inner:
                    out = out[:x] + new_inner + out[y:]
            if out != html:
                n_files += 1
                if not args.dry:
                    with open(path, "w", encoding="utf-8", newline="") as f:
                        f.write(out)
    mode = "DRY" if args.dry else "OK"
    print(f"[{mode}] языков: {len(LANGS)}; файлов изменено: {n_files}; "
          f"групп XBT-10: {len(groups['icd10'])}; глав DSM-5-TR: {len(groups['dsm'])}")


if __name__ == "__main__":
    main()
