# -*- coding: utf-8 -*-
"""_tools/book-structure-audit.py — сплошной аудит структуры и навигации книг (без браузера).

Браузерные замеры (контраст, кегли по факту отрисовки) делает _tools/book-audit.js;
этот скрипт закрывает всё, что видно по коду, и работает на всём корпусе книг
(books/** + klinik-psixiatriya/**) за секунды. Формат строки — как в book-audit.js:

    книга | язык | страница | класс | причина | было | стало | детали

Классы: (а) структура меню, (б) типографика, (в) контраст (по объявленным цветам),
(г) отступы, (д) ссылки и навигация, (е) пустые/недоделанные страницы, (ж) языковые утечки.

Запуск:
    python _tools/book-structure-audit.py --out <каталог> --tag before
    python _tools/book-structure-audit.py --out <каталог> --tag after --root <каталог репозитория>
"""
from __future__ import annotations

import argparse
import glob
import importlib.util
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

_spec = importlib.util.spec_from_file_location("sc", os.path.join(HERE, "structure-check.py"))
SC = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(SC)

LANGS = ("az", "ru", "en", "tr")
ARIA_AZ = re.compile(r'Aç / bağla|Naviqasiya|Futermenü|Fəsil keçidi|Mündəricat|Kitab axtarışı')
ARIA_AZ_TR = re.compile(r'Aç / bağla(?!p)|Naviqasiya|Futermenü|Fəsil keçidi|Mündəricat|Kitab axtarışı')
ARIA_RU = re.compile(r'Открыть / закрыть|Навигация|Меню подвала|Переход между главами|Закрыть|Оглавление|Язык')
ARIA_EN = re.compile(r'Open / close|Navigation|Footer menu|Chapter navigation|Close|Contents|Language')
LOW_ALPHA = re.compile(r'rgba\(\s*242\s*,\s*237\s*,\s*227\s*,\s*\.(?:[0-4]\d?)\s*\)')


def lang_of(rel):
    parts = rel.replace(os.sep, "/").split("/")
    for L in ("ru", "en", "tr"):
        if L in parts:
            return L
    return "az"


def book_of(rel):
    parts = rel.replace(os.sep, "/").split("/")
    if parts[0] == "klinik-psixiatriya":
        return "klinik"
    if parts[0] == "books":
        if len(parts) == 2:
            return "gallery"
        if len(parts) == 3 and parts[1] in ("ru", "en"):
            return "gallery"
        return parts[1]
    return parts[0]


def list_pages(root):
    out = []
    for base in ("books", "klinik-psixiatriya"):
        d = os.path.join(root, base)
        if not os.path.isdir(d):
            continue
        for dirpath, dirnames, filenames in os.walk(d):
            dirnames[:] = [x for x in dirnames if not x.startswith(".") and not x.startswith("_")
                           and ".bak" not in x and x != "test" and x != "covers" and x != "node_modules"]
            for n in sorted(filenames):
                if n.endswith(".html") and not n.startswith("_") and not n.startswith("_shot") and not n.startswith("_ba") and not n.startswith("_p."):
                    out.append(os.path.relpath(os.path.join(dirpath, n), root).replace(os.sep, "/"))
    return sorted(out)


def audit_page(root, rel):
    findings = []
    path = os.path.join(root, rel)
    html = open(path, encoding="utf-8", errors="replace").read()
    lang = lang_of(rel)
    d = os.path.dirname(path)

    def add(cls, reason, was, became, extra=""):
        findings.append([book_of(rel), lang, rel, cls, reason, str(was), str(became), extra])

    root_node = SC.parse(path)

    # ── (е) редирект-заглушки и пустые страницы ──
    if re.search(r'<meta http-equiv="refresh"', html, re.I):
        add('пустые страницы', 'страница-заглушка (meta refresh)', 'redirect', 'контент или удаление',
            re.search(r'url=([^"\'>\s]+)', html).group(1) if re.search(r'url=([^"\'>\s]+)', html) else '')
    text = re.sub(r'<(script|style)[\s\S]*?</\1>', ' ', html)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = " ".join(text.split())
    if len(text) < 500 and not re.search(r'meta http-equiv="refresh"', html, re.I):
        add('пустые страницы', 'текста меньше 500 знаков', '%d знаков' % len(text), 'страница с содержимым')

    # ── (а) структура меню ──
    nav = SC.find_root(root_node, "nav", "bk-sb__nav")
    if nav is not None:
        rows = SC.parse_sidebar(root_node)
        groups = [r for r in rows if r["kind"] == "group"]
        flat = [r for r in rows if r["kind"] == "flat"]
        link_groups = [g for g in groups if g["tag"] == "a" and g["href"]]
        label_groups = [g for g in groups if not (g["tag"] == "a" and g["href"])]
        with_sub = [g for g in groups if g["has_sub"]]
        with_tgl = [g for g in groups if g["has_toggle"]]
        if groups:
            if len(with_sub) != len(groups):
                add('структура меню', 'группа без подменю', '%d' % (len(groups) - len(with_sub)), '0')
            if len(with_tgl) != len(groups):
                add('структура меню', 'у группы нет кнопки раскрытия', '%d' % (len(groups) - len(with_tgl)), '0')
            sub_only = [g for g in groups if g["sub_count"] > 0]
            bad_label = [g for g in label_groups if g["sub_count"] > 0]
            if bad_label:
                add('структура меню', 'заголовок группы — подпись, не ссылка', '%d' % len(bad_label), 'ссылка на страницу',
                    "; ".join(g["title"][:30] for g in bad_label[:3]))
            # «текущих» групп в каждой классификации должно быть не больше одной
            trees = {}
            for g in groups:
                trees.setdefault(g["tree"], []).append(g)
            for t, gs in trees.items():
                cur = sum(1 for g in gs if g["data_here"] == "1")
                if cur > 1:
                    add('структура меню', 'в классификации %s больше одной текущей группы' % t, '%d' % cur, '1',
                        "; ".join(g["title"][:28] for g in gs if g["data_here"] == "1"))
            # одинаковый пункт дважды (одна страница, разный текст)
            seen = {}
            dup = []
            for r in rows:
                # настоящий дефект — когда одно НАЗВАНИЕ ведёт на РАЗНЫЕ страницы
                if r["href"] and r["title"]:
                    k = (r["tree"], r["title"])
                    if k in seen and seen[k] != r["href"]:
                        dup.append("«%s»: %s / %s" % (r["title"][:30], seen[k], r["href"]))
                    seen[k] = r["href"]
            if dup:
                add('структура меню', 'одно название в меню ведёт на разные страницы', '%d' % len(dup), 'одна страница на название', "; ".join(dup[:3]))
        if flat:
            add('структура меню', 'подпункты выпали из групп (плоский список)', '%d' % len(flat), 'внутри .bk-grp__sub',
                "; ".join(f["title"][:28] for f in flat[:3]))
        empty = [r for r in rows if not r["title"]]
        if empty:
            add('структура меню', 'пустой пункт меню (без текста)', '%d' % len(empty), '0')

    # ── (д) ссылки и навигация ──
    hrefs = re.findall(r'href="([^"]+)"', html)
    broken, anchors_bad = [], []
    ids = set(re.findall(r'\sid="([^"]+)"', html))
    for h in hrefs:
        if re.match(r'^(https?:|mailto:|tel:|javascript:)', h):
            continue
        if h.startswith("#"):
            if len(h) > 1 and h[1:] not in ids:
                anchors_bad.append(h)
            continue
        clean = h.split("#")[0].split("?")[0]
        if not clean:
            continue
        tgt = os.path.join(root, clean.lstrip("/")) if clean.startswith("/") else os.path.join(d, clean)
        if not os.path.exists(tgt):
            broken.append(h)
    if broken:
        add('ссылки и навигация', 'битая ссылка', '%d' % len(broken), 'ссылка на существующий файл', "; ".join(broken[:5]))
    if anchors_bad:
        add('ссылки и навигация', 'ссылка на несуществующий якорь', '%d' % len(anchors_bad), 'якорь существует',
            "; ".join(anchors_bad[:5]))
    canon = (re.search(r'<link rel="canonical" href="([^"]*)"', html) or [None, ""])[1]
    book = book_of(rel)
    if canon:
        cb = "klinik" if "/klinik-psixiatriya" in canon else (re.search(r"/books/([^/\"]+)", canon) or [None, None])[1]
        if cb and cb != book:
            add('ссылки и навигация', 'canonical ведёт в другую книгу', canon, 'canonical своей страницы')
    empty_href = max(0, len(re.findall(r'href=""', html)) - len(re.findall(r'href=""[^>]*aria-hidden', html)))
    if empty_href:
        add('ссылки и навигация', 'пустая ссылка href=""', '%d' % empty_href, '0')

    # ── (ж) языковые утечки ──
    aria = re.findall(r'aria-label="([^"]*)"', html)
    if lang == "ru":
        bad = [a for a in aria if ARIA_AZ.search(a)]
    elif lang == "tr":
        bad = [a for a in aria if ARIA_AZ_TR.search(a) or ARIA_RU.search(a)]
    elif lang == "en":
        bad = [a for a in aria if ARIA_AZ.search(a) or ARIA_RU.search(a)]
    else:
        bad = []
    if bad:
        add('языковые утечки', 'служебная подпись (aria-label) чужого языка', '%d' % len(bad), 'язык страницы',
            "; ".join(sorted(set(bad))[:4]))
    hl = (re.search(r'<html[^>]*\slang="([^"]*)"', html) or [None, ""])[1]
    if hl and not hl.lower().startswith(lang):
        add('языковые утечки', '<html lang> не совпадает с языком каталога', 'lang="%s"' % hl, 'lang="%s"' % lang)
    vis = re.sub(r'<(script|style)[\s\S]*?</\1>', ' ', html)
    vis = re.sub(r'<!--[\s\S]*?-->', ' ', vis)
    vis = re.sub(r'<[^>]+>', ' ', vis)
    cyr = len(re.findall(r'[А-Яа-яЁё]', vis))
    lat = len(re.findall(r'[A-Za-zÀ-ÿƏəĞğİıÖöŞşÜüÇç]', vis))
    share = cyr / (cyr + lat) if (cyr + lat) else 0
    if lang in ("az", "en", "tr") and share > 0.3:
        add('языковые утечки', 'текст не на языке каталога (кириллица доминирует)', "%d%%" % round(share * 100), '≤ 5%')
    azw = len(re.findall(r'\b(və|üçün|ilə|haqqında|səhifə|kitab|fəsil)\b', vis, re.I))
    if lang in ("ru", "en") and azw > 3:
        add('языковые утечки', 'азербайджанские слова в тексте не-азербайджанской версии', '%d слов' % azw, '0')

    # ── (б) типографика по коду ──
    caps = [m.group(2).strip() for m in re.finditer(r'<h([234])[^>]*>([^<]{16,})</h\1>', html)
            if len(re.sub(r'[^A-Za-zÀ-ÿА-Яа-яЁёƏəĞğİıÖşŞüÜçÇ]', '', m.group(2))) > 10
            and re.sub(r'[^A-Za-zÀ-ÿА-Яа-яЁёƏəĞğİıÖşŞüÜçÇ]', '', m.group(2)) ==
            re.sub(r'[^A-Za-zÀ-ÿА-Яа-яЁёƏəĞğİıÖşŞüÜçÇ]', '', m.group(2)).upper()]
    if caps:
        add('типографика', 'заголовок раздела набран капсом', '%d' % len(caps), 'обычный регистр',
            " | ".join(c[:28] for c in caps[:3]))
    h1n = len(re.findall(r'<h1\b', html))
    if h1n == 0:
        add('типографика', 'нет h1 на странице', 0, 'один h1')
    if h1n > 1:
        add('типографика', 'больше одного h1', h1n, 'один')
    if not re.search(r'<title>\s*\S', html):
        add('типографика', 'пустой <title>', '(пусто)', 'заголовок страницы')

    # ── (в) контраст по объявленным цветам (без отрисовки) ──
    inline = re.findall(r'style="[^"]*color:\s*var\(--(?:mute|grey|gray)\)[^"]*"', html)
    if LOW_ALPHA.search(html):
        add('контраст', 'объявлен цвет текста с прозрачностью ниже нормы (rgba .4 и меньше)', 'rgba(242,237,227,<.45)', '≥ 4.5:1')
    if inline:
        add('контраст', 'инлайновая серая подпись (--mute) в разметке', '%d' % len(inline), 'цвет нормы')

    return findings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=r"D:\Документы\ZFreud\_align\book_audit")
    ap.add_argument("--tag", default="audit")
    ap.add_argument("--root", default=REPO)
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    root = args.root
    pages = list_pages(root)
    rows = []
    for rel in pages:
        rows.extend(audit_page(root, rel))
    os.makedirs(args.out, exist_ok=True)
    header = ["книга", "язык", "страница", "класс", "причина", "было", "стало", "детали"]
    out = os.path.join(args.out, "book_audit_%s.tsv" % args.tag)
    with open(out, "w", encoding="utf-8", newline="") as f:
        f.write("\t".join(header) + "\n")
        for r in rows:
            f.write("\t".join(str(x).replace("\t", " ").replace("\n", " ") for x in r) + "\n")
    print("страниц: %d; строк аудита: %d" % (len(pages), len(rows)))
    print("-> " + out)


if __name__ == "__main__":
    main()
