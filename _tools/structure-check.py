# -*- coding: utf-8 -*-
"""_tools/structure-check.py — «структура книги»: снимок и сторож регрессий.

Требование владельца (2026-09-30): у каждой книги — свой файл структуры, чтобы
видеть и сохранять структурность; для основного сайта один, для каждой книги
отдельный (каждая книга — как отдельный сайт со своей структурой). Источник
данных — фактическое оглавление текущей версии, а не память.

Файлы:  books/<slug>/STRUCTURE.json   (машинный)
        books/<slug>/STRUCTURE.md     (человеческий)
Для клиники корень — klinik-psixiatriya/ (папка книги, а не books/<slug>).

Режимы:
    python _tools/structure-check.py --write      # снять структуру с живой версии
    python _tools/structure-check.py              # сверить живое с записанным
    python _tools/structure-check.py --book klinik
    python _tools/structure-check.py --json       # машиночитаемый отчёт

Что фиксирует снимок:
  * перечень разделов/глав/подглав в порядке следования, их слаги и URL;
  * какой пункт ведёт на свою страницу, а какой — группа-подпись;
  * число страниц, число пунктов меню, языки, классификации/ветки;
  * обязательные проверки: страницы = пункты меню, 0 битых ссылок, группы
    раскрываются (есть ▶ и .bk-grp__sub), заголовок группы — ссылка, в каждой
    классификации ровно одна «текущая» группа, подпункты не выпадают из групп.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANGS = ("az", "ru", "en", "tr")


# ─────────────────────────── лёгкий разбор HTML ───────────────────────────
class Node:
    __slots__ = ("tag", "attrs", "children", "text", "parent")

    def __init__(self, tag, attrs, parent):
        self.tag = tag
        self.attrs = attrs
        self.children = []
        self.text = ""
        self.parent = parent


class Tree(HTMLParser):
    VOID = {"br", "img", "meta", "link", "input", "hr", "source", "area", "base", "col", "embed", "param", "track", "wbr"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#root", {}, None)
        self.cur = self.root

    def handle_starttag(self, tag, attrs):
        n = Node(tag, dict(attrs), self.cur)
        self.cur.children.append(n)
        if tag not in self.VOID:
            self.cur = n

    def handle_startendtag(self, tag, attrs):
        n = Node(tag, dict(attrs), self.cur)
        self.cur.children.append(n)

    def handle_endtag(self, tag):
        if tag in self.VOID:
            return
        e = self.cur
        while e is not None and e.tag != tag:
            e = e.parent
        if e is not None and e.parent is not None:
            self.cur = e.parent

    def handle_data(self, data):
        self.cur.text += data


def parse(path):
    t = Tree()
    with open(path, encoding="utf-8", errors="replace") as f:
        t.feed(f.read())
    return t.root


def walk(node, pred):
    for ch in node.children:
        if pred(ch):
            yield ch
        yield from walk(ch, pred)


def cls(n):
    return (n.attrs.get("class") or "")


def has_cls(n, name):
    return name in cls(n).split()


def norm_text(n):
    """Нормализованный текст: принимает и узел, и строку."""
    if isinstance(n, str):
        return " ".join(n.split())
    if n is None:
        return ""
    return " ".join(n.text.split())


def text_of(node):
    """Текст узла целиком (со вложенными)."""
    out = [node.text]
    for ch in node.children:
        out.append(text_of(ch))
    return " ".join(" ".join(out).split())


def find_root(node, tag, name=None):
    for n in walk(node, lambda x: x.tag == tag and (name is None or has_cls(x, name))):
        return n
    return None


# ─────────────────────────── структура книги ───────────────────────────
def lang_dir(book_root, lang):
    return book_root if lang == "az" else os.path.join(book_root, lang)


def list_html(d):
    if not os.path.isdir(d):
        return []
    return sorted(n for n in os.listdir(d) if n.endswith(".html"))


def parse_sidebar(root):
    """Пункты меню страницы: (kind, text, href, code, tree, in_group).

    kind: group — заголовок раздела (может быть ссылкой или подписью),
          item  — подпункт внутри группы,
          flat  — подпункт, выпавший из группы (дефект),
          link  — плоский пункт рейки книги без классификаций.
    """
    rows = []
    for tr in walk(root, lambda x: x.tag == "div" and has_cls(x, "cls-tree")):
        tree_key = tr.attrs.get("data-cls")
        for grp in walk(tr, lambda x: x.tag == "div" and has_cls(x, "bk-grp")):
            head = None
            for ch in grp.children:
                if ch.tag in ("a", "span") and has_cls(ch, "bk-row--sec"):
                    head = ch
                    break
            if head is None:
                continue
            href = head.attrs.get("href")
            sub = find_root(grp, "div", "bk-grp__sub")
            rows.append({
                "tree": tree_key,
                "kind": "group",
                "tag": head.tag,
                "href": href,
                "code": norm_text(attr_of(head, "bk-row__n")) if attr_of(head, "bk-row__n") else "",
                "title": norm_text(attr_of(head, "bk-row__t")) if attr_of(head, "bk-row__t") else norm_text(text_of(head)),
                "data_here": grp.attrs.get("data-here"),
                "has_sub": sub is not None,
                "has_toggle": find_root(grp, "button", "bk-tgl") is not None,
                "sub_count": len([a for a in walk(grp, lambda x: x.tag == "a" and has_cls(x, "bk-row--sub"))]),
            })
            if sub is not None:
                for a in walk(sub, lambda x: x.tag == "a" and has_cls(x, "bk-row--sub")):
                    rows.append({
                        "tree": tree_key, "kind": "item", "tag": "a", "href": a.attrs.get("href"),
                        "code": norm_text(attr_of(a, "bk-row__n")) if attr_of(a, "bk-row__n") else "",
                        "title": norm_text(attr_of(a, "bk-row__t")) if attr_of(a, "bk-row__t") else norm_text(text_of(a)),
                        "data_here": None, "has_sub": False, "has_toggle": False, "sub_count": 0,
                    })
        # подпункты, выпавшие из групп (прямо в дереве)
        for ch in tr.children:
            if ch.tag in ("a", "span") and has_cls(ch, "bk-row--sub"):
                rows.append({"tree": tree_key, "kind": "flat", "tag": ch.tag,
                             "href": ch.attrs.get("href"), "code": "", "title": norm_text(text_of(ch)),
                             "data_here": None, "has_sub": False, "has_toggle": False, "sub_count": 0})
    if not rows:
        nav = find_root(root, "nav", "bk-sb__nav")
        if nav:
            for a in walk(nav, lambda x: x.tag in ("a", "span") and has_cls(x, "bk-row")):
                rows.append({"tree": None, "kind": "link", "tag": a.tag, "href": a.attrs.get("href"),
                             "code": norm_text(attr_of(a, "bk-row__n")) if attr_of(a, "bk-row__n") else "",
                             "title": norm_text(attr_of(a, "bk-row__t")) if attr_of(a, "bk-row__t") else norm_text(text_of(a)),
                             "data_here": None, "has_sub": False, "has_toggle": False, "sub_count": 0})
    return rows


def attr_of(node, cls_name):
    for n in node.children:
        if n.tag == "span" and has_cls(n, cls_name):
            return n
    return None


def page_menu_pages(root):
    """Пункты меню с адресом (то, что «ведёт на страницу») + подпункты."""
    out = []
    for a in walk(root, lambda x: x.tag == "a" and (has_cls(x, "bk-row"))):
        href = a.attrs.get("href")
        if href:
            out.append(href)
    return out


def snapshot_book(book_name, book_root, rel_root):
    data = {
        "book": book_name,
        "root": rel_root,
        "languages": [],
        "langs": {},
        "classifications": [],
        "chapters": [],
        "counts": {},
        "checks": {},
    }
    langs = [L for L in LANGS if os.path.isdir(lang_dir(book_root, L))]
    if "az" not in langs and os.path.isdir(book_root):
        langs = list(langs)
    data["languages"] = langs

    ref = None
    for L in ("az", "ru", "en", "tr"):
        idx = os.path.join(lang_dir(book_root, L), "index.html")
        if os.path.isfile(idx):
            ref = (L, idx)
            break
    if ref is None:
        data["checks"] = {"error": "нет index.html ни на одном языке"}
        return data

    for L in langs:
        d = lang_dir(book_root, L)
        files = list_html(d)
        idx = os.path.join(d, "index.html")
        root = parse(idx) if os.path.isfile(idx) else None
        rows = parse_sidebar(root) if root is not None else []
        pages = set(files)
        menu_urls = set()
        for r in rows:
            if r["href"]:
                menu_urls.add(r["href"])
        for a in (root and walk(root, lambda x: x.tag == "a") or []):
            h = a.attrs.get("href") or ""
            if h and not h.startswith(("http", "/", "mailto", "#")):
                menu_urls.add(h)
        broken = sorted(u for u in menu_urls if not os.path.exists(os.path.join(d, u.split("#")[0]))
                        and u.split("#")[0] != "")
        # страницы-переходы (meta refresh) — прежние адреса книги, в рейке их нет by design
        stubs = set()
        for f in files:
            try:
                head = open(os.path.join(d, f), encoding="utf-8", errors="replace").read(2000)
            except OSError:
                continue
            if 'http-equiv="refresh"' in head:
                stubs.add(f)
        content_pages = [f for f in files if f not in stubs]
        unlinked = sorted(f for f in content_pages if f not in menu_urls)
        groups = [r for r in rows if r["kind"] == "group"]
        flat = [r for r in rows if r["kind"] == "flat"]
        data["langs"][L] = {
            "pages": len(files),
            "menu_rows": len(rows),
            "menu_pages": len(menu_urls),
            "groups": len(groups),
            "groups_with_sub": sum(1 for g in groups if g["has_sub"]),
            "groups_with_toggle": sum(1 for g in groups if g["has_toggle"]),
            "groups_linked": sum(1 for g in groups if g["tag"] == "a" and g["href"]),
            "groups_label_only": sum(1 for g in groups if g["tag"] != "a" or not g["href"]),
            "flat_rows": len(flat),
            "current_groups": sum(1 for g in groups if g["data_here"] == "1"),
            "broken_links": len(broken),
            "broken_sample": broken[:5],
            "trees": sorted({r["tree"] for r in rows if r["tree"]}),
            "files": files,
            "stub_pages": len(stubs),
            "content_pages": len(content_pages),
            "unlinked_pages": unlinked,
        }
        if L == ref[0]:
            for tr in sorted({r["tree"] for r in rows if r["tree"]}):
                data["classifications"].append({
                    "key": tr,
                    "groups": [
                        {"code": r["code"], "title": r["title"], "url": r["href"],
                         "is_page": bool(r["tag"] == "a" and r["href"]), "sub_items": r["sub_count"]}
                        for r in rows if r["tree"] == tr and r["kind"] == "group"
                    ],
                })
            if not data["classifications"]:
                data["chapters"] = [
                    {"code": r["code"], "title": r["title"], "url": r["href"],
                     "is_page": bool(r["href"]), "kind": r["kind"]}
                    for r in rows
                ]

    # обязательные проверки структуры (по каждому языку)
    checks = {}
    for L, s in data["langs"].items():
        checks[L] = {
            "pages_equals_menu_items": s["content_pages"] > 0 and not s["unlinked_pages"],
            "broken_links_zero": s["broken_links"] == 0,
            "groups_expandable": s["groups"] == s["groups_with_sub"] == s["groups_with_toggle"] or s["groups"] == 0,
            "group_headers_are_links": s["groups_label_only"] == 0,
            "no_flat_rows": s["flat_rows"] == 0,
            "one_current_group_per_tree": s["current_groups"] <= len(s["trees"]),
        }
    data["checks"] = checks
    data["counts"] = {
        "pages_total": sum(s["pages"] for s in data["langs"].values()),
        "content_pages_total": sum(s["content_pages"] for s in data["langs"].values()),
        "stub_pages_total": sum(s["stub_pages"] for s in data["langs"].values()),
        "unlinked_pages_total": sum(len(s["unlinked_pages"]) for s in data["langs"].values()),
        "menu_items_total": sum(s["menu_rows"] for s in data["langs"].values()),
        "groups_total": sum(s["groups"] for s in data["langs"].values()),
        "flat_rows_total": sum(s["flat_rows"] for s in data["langs"].values()),
        "broken_links_total": sum(s["broken_links"] for s in data["langs"].values()),
    }
    return data


def structure_paths(book_root):
    return os.path.join(book_root, "STRUCTURE.json"), os.path.join(book_root, "STRUCTURE.md")


def write_md(data, path):
    L = []
    L.append("# Структура книги: %s" % data["book"])
    L.append("")
    L.append("Снимок фактического оглавления версии (источник — живой HTML, не память).")
    L.append("Файл ведёт `_tools/structure-check.py`: `--write` пересобирает, без ключей — сверяет.")
    L.append("")
    L.append("| параметр | значение |")
    L.append("|---|---|")
    L.append("| корень | `%s` |" % data["root"])
    L.append("| языки | %s |" % ", ".join(data["languages"]))
    c = data.get("counts", {})
    L.append("| страниц всего | %s (из них страниц-переходов %s) |" % (c.get("pages_total"), c.get("stub_pages_total")))
    L.append("| страниц с содержанием | %s |" % c.get("content_pages_total"))
    L.append("| страниц без ссылки из меню | %s |" % c.get("unlinked_pages_total"))
    L.append("| пунктов меню всего | %s |" % c.get("menu_items_total"))
    L.append("| групп (разделов) | %s |" % c.get("groups_total"))
    L.append("| выпавших подпунктов | %s |" % c.get("flat_rows_total"))
    L.append("| битых ссылок | %s |" % c.get("broken_links_total"))
    L.append("")
    L.append("## Языки")
    L.append("")
    L.append("| язык | страниц | пунктов меню | групп | групп-ссылок | групп-подписей | выпавших | битых | текущих |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    for lg in data["languages"]:
        s = data["langs"].get(lg)
        if not s:
            continue
        L.append("| %s | %d | %d | %d | %d | %d | %d | %d | %d |" % (
            lg, s["pages"], s["menu_rows"], s["groups"], s["groups_linked"],
            s["groups_label_only"], s["flat_rows"], s["broken_links"], s["current_groups"]))
    if data["classifications"]:
        L.append("")
        L.append("## Классификации и главы (язык %s)" % data["languages"][0])
        L.append("")
        for cl in data["classifications"]:
            L.append("### %s" % cl["key"])
            L.append("")
            L.append("| код | раздел | ведёт на страницу | подпунктов |")
            L.append("|---|---|---|---|")
            for g in cl["groups"]:
                L.append("| %s | %s | %s | %d |" % (g["code"], g["title"], g["url"] or "— (подпись)", g["sub_items"]))
            L.append("")
    if data["chapters"]:
        L.append("")
        L.append("## Главы")
        L.append("")
        L.append("| № | глава | URL | ведёт на страницу |")
        L.append("|---|---|---|---|")
        for i, g in enumerate(data["chapters"], 1):
            L.append("| %d | %s | %s | %s |" % (i, g["title"], g["url"] or "—", "да" if g["is_page"] else "нет"))
    L.append("")
    L.append("## Обязательные проверки")
    L.append("")
    L.append("| язык | страницы = пункты | 0 битых | группы раскрываются | заголовок = ссылка | нет выпавших |")
    L.append("|---|---|---|---|---|---|")
    for lg, ch in data["checks"].items():
        if not isinstance(ch, dict) or "pages_equals_menu_items" not in ch:
            continue
        mark = lambda v: "да" if v else "**НЕТ**"
        L.append("| %s | %s | %s | %s | %s | %s |" % (
            lg, mark(ch["pages_equals_menu_items"]), mark(ch["broken_links_zero"]),
            mark(ch["groups_expandable"]), mark(ch["group_headers_are_links"]), mark(ch["no_flat_rows"])))
    L.append("")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write("\n".join(L))


def books_list():
    out = []
    kr = os.path.join(ROOT, "klinik-psixiatriya")
    if os.path.isdir(kr):
        out.append(("klinik", kr, "klinik-psixiatriya"))
    for d in sorted(glob.glob(os.path.join(ROOT, "books", "*"))):
        if not os.path.isdir(d) or ".bak" in os.path.basename(d):
            continue
        if os.path.basename(d) in ("covers", "ru", "en"):
            continue
        out.append((os.path.basename(d), d, "books/" + os.path.basename(d)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="пересобрать STRUCTURE.json/md из живой версии")
    ap.add_argument("--book", default=None, help="только одна книга (slug или klinik)")
    ap.add_argument("--json", action="store_true", help="машиночитаемый отчёт сверки")
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    report = {"mode": "write" if args.write else "check", "books": {}}
    for name, path, rel in books_list():
        if args.book and args.book not in (name, rel):
            continue
        data = snapshot_book(name, path, rel)
        js, md = structure_paths(path)
        if args.write:
            data["generated"] = "structure-check.py --write"
            with open(js, "w", encoding="utf-8", newline="") as f:
                json.dump(data, f, ensure_ascii=False, indent=1)
            write_md(data, md)
            changed = sum(1 for c in data["checks"].values() if isinstance(c, dict) and not all(c.values()))
            report["books"][name] = {
                "written": True,
                "counts": data.get("counts"),
                "failed_checks": changed,
            }
            print("[write] %-22s страниц %s | пунктов %s | групп %s | выпавших %s | битых %s | проверок с замечанием %d"
                  % (name, data.get("counts", {}).get("pages_total"), data.get("counts", {}).get("menu_items_total"),
                     data.get("counts", {}).get("groups_total"), data.get("counts", {}).get("flat_rows_total"),
                     data.get("counts", {}).get("broken_links_total"), changed))
        else:
            if not os.path.isfile(js):
                print("[check] %-22s STRUCTURE.json нет — запустите --write" % name)
                report["books"][name] = {"error": "no STRUCTURE.json"}
                continue
            old = json.load(open(js, encoding="utf-8"))
            diffs = []
            for L in data["langs"]:
                o = old.get("langs", {}).get(L)
                n = data["langs"][L]
                if not o:
                    diffs.append("язык %s: появился/пропал" % L)
                    continue
                for k in ("pages", "menu_rows", "groups", "groups_linked", "groups_label_only",
                          "flat_rows", "broken_links"):
                    if o.get(k) != n[k]:
                        diffs.append("%s: %s было %s → стало %s" % (L, k, o.get(k), n[k]))
                of, nf = set(o.get("files") or []), set(n["files"])
                if of - nf:
                    diffs.append("%s: пропали страницы: %s" % (L, ", ".join(sorted(of - nf)[:5])))
                if nf - of:
                    diffs.append("%s: новые страницы: %s" % (L, ", ".join(sorted(nf - of)[:5])))
            for L, ch in data["checks"].items():
                if isinstance(ch, dict):
                    for k, v in ch.items():
                        if not v:
                            diffs.append("%s: проверка не проходит — %s" % (L, k))
            report["books"][name] = {"diffs": diffs}
            if diffs:
                print("[check] %-22s расхождений: %d" % (name, len(diffs)))
                for d in diffs[:12]:
                    print("        - " + d)
            else:
                print("[check] %-22s структура совпадает с записанной" % name)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
