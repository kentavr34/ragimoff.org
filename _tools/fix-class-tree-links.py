# -*- coding: utf-8 -*-
"""_tools/fix-class-tree-links.py — «Клиническая психиатрия»: заголовок группы = ссылка.

Жалоба владельца (2026-09-30):
  «в боковом меню в 7 главе в МКБ-10 подменю опять вышло из оглавления;
   главы в боковом меню сами не кликабельны, хоть у глав есть своя страница —
   где представлен список подглав».

Что было по факту (замер 2026-09-30, 548 страниц книги с деревом классификаций):
  * дерево МКБ-11: 24 заголовка групп — `<a href>` на страницу главы (норма);
  * дерево DSM-5-TR: 19 заголовков — `<span>`, не кликабельны;
  * дерево МКБ-10: 11 заголовков — `<span>`, не кликабельны;
  * у МКБ-10 на странице 7-й главы сразу ДВЕ группы помечены is-on/data-here=1
    (F40–F48 и F90–F98) — место главы в оглавлении показывалось неверно.

Что делает скрипт (идемпотентно, все языки AZ/RU/EN/TR):
 1. Заголовку группы DSM-5-TR и МКБ-10 ставит цель-ссылку:
      — все расстройства группы принадлежат одной главе книги → страница этой
        главы (клик по названию ведёт на страницу главы со списком подглав);
      — группа шире одной главы (F40–F48 = тревожные + ОКР + стресс + диссоциативные)
        → mundericat.html («Содержание» книги).
 2. В каждой классификации оставляет РОВНО одну «текущую» группу (is-on +
    data-here=1): ту, что содержит больше расстройств текущей страницы
    (при равенстве — первую по порядку дерева). Остальные совпадения не
    подсвечиваются — «подменю не выпадает из оглавления».
 3. Кнопка ▶ остаётся отдельной: название ведёт на страницу, стрелка раскрывает.

Запуск:
    python _tools/fix-class-tree-links.py --dry
    python _tools/fix-class-tree-links.py
"""
from __future__ import annotations

import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, "klinik-psixiatriya")
LANGS = ("", "ru", "en", "tr")

TREE_RE = re.compile(r'<div class="cls-tree" data-cls="([a-z0-9]+)"([^>]*)>')
GRP_HEAD_RE = re.compile(
    r'^(<div class="bk-grp")(?P<attrs>[^>]*)>\s*'
    r'<(?P<tag>a|span) class="(?P<cls>[^"]*)"(?P<tagattrs>[^>]*)>\s*'
    r'<span class="bk-row__n">(?P<num>.*?)</span>\s*'
    r'<span class="bk-row__t">(?P<name>.*?)</span>\s*'
    r'</(?P=tag)>', re.S)


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


def split_groups(seg):
    parts = re.split(r'(?=<div class="bk-grp")', seg)
    return parts[0], parts[1:]


def parse_group(part):
    m = GRP_HEAD_RE.match(part)
    if not m:
        return None
    href_m = re.search(r'href="([^"]+)"', m.group("tagattrs") or "")
    return {
        "attrs": m.group("attrs"),
        "tag": m.group("tag"),
        "cls": m.group("cls"),
        "href": href_m.group(1) if href_m else None,
        "subs": re.findall(r'<a class="bk-row bk-row--sub[^"]*" href="([^"]+)"', part),
        "head_end": m.end(),
    }


def set_data_here(attrs, value):
    if 'data-here="' in attrs:
        return re.sub(r'data-here="[^"]*"', 'data-here="%s"' % value, attrs)
    return attrs + ' data-here="%s"' % value


def rebuild_group(part, href, cur, cls):
    """Пересобирает одну группу: заголовок — ссылка (если есть href) + is-on."""
    g = parse_group(part)
    if g is None:
        return part, False
    head = part[:g["head_end"]]
    tail = part[g["head_end"]:]
    classes = [c for c in g["cls"].split() if c != "is-on"]
    if cur:
        classes.append("is-on")
    newcls = " ".join(classes)
    attrs = set_data_here(g["attrs"], "1" if cur else "0")
    if href:
        new_tag = '<a class="%s" href="%s">' % (newcls, href)
        end_tag = "</a>"
    else:
        new_tag = '<span class="%s">' % newcls
        end_tag = "</span>"
    # заменяем открывающий тег заголовка
    new_head = re.sub(r'^(<div class="bk-grp")[^>]*>\s*<(a|span) class="[^"]*"[^>]*>',
                      lambda m: m.group(1) + attrs + ">\n" + new_tag, head, count=1)
    # заменяем закрывающий тег заголовка (первый после строки названия)
    new_head = re.sub(r'(<span class="bk-row__t">.*?</span>)\s*</(a|span)>',
                      lambda m: m.group(1) + "\n" + end_tag, new_head, count=1, flags=re.S)
    changed = (new_head + tail) != part
    return new_head + tail, changed


def normalize_strays(seg, btn_span):
    """Два дефекта старой пересборки, найденные замером 2026-09-30 в 540 файлах:

    1) «выпавший» плоский фрагмент на верхнем уровне дерева —
       `<span class="bk-row bk-row--sec">F70–F79 …</span>` + `<a class="bk-row--sub" …>`
       вне .bk-grp: группа МКБ-10 F70–F79 (Умственная отсталость) не открывается
       и не содержит подменю (жалоба владельца про МКБ-10 в боковом меню);
    2) пустая строка меню `<span class="bk-row--sub">` без текста и ссылки.

    Фрагмент (1) собирается в такую же группу, как соседние: заголовок + ▶ +
    .bk-grp__sub. Кнопка ▶ берётся из уже существующей группы того же дерева —
    чтобы подпись (aria-label) осталась на языке страницы.
    """
    # (2) пустая строка меню
    seg = re.sub(r'\s*<span class="bk-row bk-row--sub">\s*<span class="bk-row__n">\s*</span>\s*'
                 r'<span class="bk-row__t">\s*</span>\s*</span>', '', seg)

    # (1) выпавший фрагмент → группа (класс может нести и is-on: такие
    #     фрагменты нашлись на 8 страницах — глава 01 и расстройство 6A00)
    stray = re.compile(
        r'<span class="bk-row bk-row--sec[^"]*">\s*<span class="bk-row__n">(?P<num>.*?)</span>\s*'
        r'<span class="bk-row__t">(?P<name>.*?)</span>\s*</span>\s*'
        r'(?P<rows>(?:<a class="bk-row bk-row--sub[^"]*"[^>]*>.*?</a>\s*)+)', re.S)

    def to_group(m):
        rows = m.group("rows")
        return ('<div class="bk-grp" data-slug="" data-here="0">\n'
                '<span class="bk-row bk-row--sec"><span class="bk-row__n">%s</span>'
                '<span class="bk-row__t">%s</span></span>\n%s\n'
                '<div class="bk-grp__sub">\n%s</div>\n</div>\n'
                % (m.group("num"), m.group("name"), btn_span, rows))

    return stray.sub(to_group, seg)


def patch_tree(seg, cls_name, chapter_slug, chapter_subs, disc_to_chapter):
    m_btn = re.search(r'<button class="bk-tgl"[^>]*>.*?</button>', seg, re.S)
    btn_span = m_btn.group(0) if m_btn else \
        '<button class="bk-tgl" type="button" tabindex="-1" aria-expanded="false" aria-label="Открыть / закрыть">▶</button>'
    seg = normalize_strays(seg, btn_span)
    pre, parts = split_groups(seg)
    groups = [parse_group(p) for p in parts]
    # текущая группа
    if cls_name == "icd":
        cur_idx = None
        for i, g in enumerate(groups):
            if g and chapter_slug and ('data-slug="%s"' % chapter_slug) in g["attrs"]:
                cur_idx = i
                break
        hrefs = [(g["href"] if g else None) for g in groups]
    else:
        best = None
        for i, g in enumerate(groups):
            if not g:
                continue
            ov = len([s for s in g["subs"] if s in chapter_subs])
            if ov > 0 and (best is None or ov > best[0]):
                best = (ov, i)
        cur_idx = best[1] if best else None
        hrefs = []
        for g in groups:
            if not g:
                hrefs.append(None)
                continue
            chapters = {disc_to_chapter[s] for s in g["subs"] if s in disc_to_chapter}
            if len(chapters) == 1:
                hrefs.append(next(iter(chapters)))
            elif chapters:
                hrefs.append("mundericat.html")
            else:
                hrefs.append(None)

    out = [pre]
    for i, p in enumerate(parts):
        if groups[i] is None:
            out.append(p)
            continue
        np_, _ = rebuild_group(p, hrefs[i], i == cur_idx, cls_name)
        out.append(np_)
    return "".join(out)


def canonical_chapters(ref_html):
    """{slug главы: {файлы расстройств}} и {файл расстройства: slug главы}."""
    chapter_subs, disc_to_chapter = {}, {}
    for m in TREE_RE.finditer(ref_html):
        if m.group(1) != "icd":
            continue
        a, b = tree_bounds(ref_html, m.end())
        _pre, parts = split_groups(ref_html[a:b])
        for p in parts:
            g = parse_group(p)
            if not g or not g["href"]:
                continue
            slug = g["href"].replace(".html", "")
            chapter_subs.setdefault(slug, set()).update(g["subs"])
            for s in g["subs"]:
                disc_to_chapter[s] = g["href"]
    return chapter_subs, disc_to_chapter


def eff_chapter(slug, chapter_subs, disc_to_chapter):
    """Глава, к которой относится страница: страница главы или страница расстройства."""
    if slug in chapter_subs:
        return slug
    ch = disc_to_chapter.get(slug + ".html")
    if ch:
        return ch.replace(".html", "")
    return slug


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    ref = open(os.path.join(BOOK, "index.html"), encoding="utf-8").read()
    chapter_subs, disc_to_chapter = canonical_chapters(ref)

    pages = []
    for lang in LANGS:
        d = os.path.join(BOOK, lang) if lang else BOOK
        if not os.path.isdir(d):
            continue
        for name in sorted(os.listdir(d)):
            if name.endswith(".html") and "_shot" not in name:
                pages.append(os.path.join(d, name))

    n_files = n_trees = 0
    n_links_new = 0
    for path in pages:
        html = open(path, encoding="utf-8", newline="").read()
        if '<div class="cls-tree"' not in html:
            continue
        slug = os.path.basename(path).replace(".html", "")
        # глава текущей страницы: страница главы, либо глава расстройства
        # (на странице расстройства 6B40 группа главы 07-6B4-stress остаётся
        #  открытой и подсвеченной — иначе «место страницы в оглавлении» теряется)
        slug = eff_chapter(slug, chapter_subs, disc_to_chapter)
        subs = chapter_subs.get(slug, set())
        bounds = []
        for m in TREE_RE.finditer(html):
            a, b = tree_bounds(html, m.end())
            bounds.append((m.group(1), a, b))
        if not bounds:
            continue
        before_links = html.count('<a class="bk-row bk-row--sec"')
        out = html
        for cls_name, a, b in sorted(bounds, key=lambda t: -t[1]):
            seg = html[a:b]
            new_seg = patch_tree(seg, cls_name, slug, subs, disc_to_chapter)
            out = out[:a] + new_seg + out[b:]
        after_links = out.count('<a class="bk-row bk-row--sec"')
        n_links_new += after_links - before_links
        if out != html:
            n_files += 1
            if not args.dry:
                with open(path, "w", encoding="utf-8", newline="") as f:
                    f.write(out)
    mode = "DRY" if args.dry else "OK"
    print("[%s] страниц изменено: %d; заголовков-групп стали ссылками: %d"
          % (mode, n_files, n_links_new))


if __name__ == "__main__":
    main()
