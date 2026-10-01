#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""site-structure-build — собирает SITE-STRUCTURE.json и SITE-STRUCTURE.md.

Обходит те же страницы, что и аудит (`_tools/site-audit.js`): корень + ru/ +
en/, без books/, klinik-psixiatriya/, test/, backend/ и служебных каталогов.
Для каждой страницы снимает паспорт (язык, тип, назначение, состав блоков) и
складывает в машинный JSON; MD — человекочитаемая проекция.

Запуск (из корня репозитория):
    python _tools/site-structure-build.py            # пересобрать оба файла
    python _tools/site-structure-build.py --check    # только сверить, не писать
"""
from __future__ import annotations

import argparse
import html as H
import io
import json
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {"books", "klinik-psixiatriya", "test", "node_modules", ".git",
             "backend", "_supplements", "favicons", "data", "images"}

RE_TITLE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
RE_H1 = re.compile(r"<h1\b[^>]*>(.*?)</h1>", re.S | re.I)
RE_TAG = re.compile(r"<[^>]+>")
RE_HERO = re.compile(r"""class\s*=\s*["'][^"']*\b(page-hero-x|page-hero|pg-hero)\b""")
RE_LANG = re.compile(r"""<html[^>]*\blang\s*=\s*["']([^"']+)["']""", re.I)


def strip_tags(s: str) -> str:
    s = RE_TAG.sub(" ", s)
    s = H.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def lang_of(rel: str) -> str:
    p = rel.replace("\\", "/")
    if p.startswith("ru/"):
        return "ru"
    if p.startswith("en/"):
        return "en"
    return "az"


def classify(rel: str, s: str = "") -> str:
    """Тип страницы. Редирект (meta refresh) — отдельный тип: у него нет ни
    шапки, ни героя, ни подвала, и проверки структуры к нему не применяются."""
    if re.search(r'http-equiv\s*=\s*["\']refresh["\']', s, re.I):
        return "redirect"
    name = os.path.basename(rel)
    if name == "index.html":
        return "home"
    if name == "blog.html":
        return "blog-index"
    if name.startswith("blog-"):
        return "blog-article"
    if name in ("template.html", "temp_index.html"):
        return "template"
    if name.startswith("test-"):
        return "test"
    return "page"


def collect(rel: str) -> dict:
    path = os.path.join(ROOT, rel.replace("/", os.sep))
    s = open(path, encoding="utf-8").read()
    title = strip_tags(RE_TITLE.search(s).group(1)) if RE_TITLE.search(s) else ""
    h1m = RE_H1.search(s)
    h1 = strip_tags(h1m.group(1)) if h1m else ""
    hero = RE_HERO.search(s)
    langattr = RE_LANG.search(s)
    return {
        "path": rel.replace("\\", "/"),
        "lang": lang_of(rel),
        "type": classify(rel, s),
        "title": title,
        "h1": h1,
        "hero_class": hero.group(1) if hero else None,
        "html_lang": (langattr.group(1) if langattr else None),
        "blocks": {
            "header": bool(re.search(r"<header\b", s, re.I)),
            "nav": bool(re.search(r'class="[^"]*(desktop-nav|mobile-nav)', s)),
            "hero": bool(hero),
            "search": bool(re.search(r'id="(hero-si|site-si)"|class="[^"]*(ph-search-bar|hero-search-bar)', s)),
            "sections": len(re.findall(r"<section\b", s, re.I)),
            "footer": bool(re.search(r"<footer\b", s, re.I)),
            "lang_switch": bool(re.search(r"lang-drop|mobile-lang", s)),
        },
        "bytes": len(s.encode("utf-8")),
    }


def pages() -> list[str]:
    out = []
    for d in ("", "ru", "en"):
        base = os.path.join(ROOT, d) if d else ROOT
        for name in sorted(os.listdir(base)):
            if name.startswith("_") or not name.endswith(".html"):
                continue
            full = os.path.join(base, name)
            if not os.path.isfile(full):
                continue
            if d == "" and os.path.isdir(full):
                continue
            out.append((d + "/" + name) if d else name)
    return out


def purpose_of(rec: dict, purpose_map: dict) -> str:
    return purpose_map.get(rec["path"], rec["h1"] or rec["title"])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="не писать файлы, только сверить")
    args = ap.parse_args()

    json_path = os.path.join(ROOT, "SITE-STRUCTURE.json")
    md_path = os.path.join(ROOT, "SITE-STRUCTURE.md")

    spec = json.load(open(json_path, encoding="utf-8"))
    purpose_map = {p["path"]: p.get("purpose", "") for p in spec.get("pages", [])}

    recs = [collect(p) for p in pages()]
    changed = 0
    old_index = {p["path"]: p for p in spec.get("pages", [])}
    for r in recs:
        r["purpose"] = purpose_of(r, purpose_map)
        old = old_index.get(r["path"])
        if old and (old.get("lang") != r["lang"] or old.get("type") != r["type"]):
            changed += 1
    new_paths = [r["path"] for r in recs if r["path"] not in old_index]
    gone = [p for p in old_index if p not in {r["path"] for r in recs}]
    print(f"страниц: {len(recs)}; новых: {len(new_paths)}; пропали: {len(gone)}; "
          f"сменили тип/язык: {changed}")
    if new_paths:
        print("  новые:", ", ".join(new_paths[:10]))
    if gone:
        print("  пропали:", ", ".join(gone[:10]))

    if args.check:
        return 0

    spec["pages"] = recs
    with open(json_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(spec, f, ensure_ascii=False, indent=1)
        f.write("\n")

    md = render_md(spec)
    with open(md_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(md)
    print("записано:", json_path, "и", md_path)
    return 0


def render_md(spec: dict) -> str:
    out = []
    a = out.append
    a("# SITE-STRUCTURE — структура сайта ragimoff.org")
    a("")
    a(spec["intro"].strip())
    a("")
    a("## 1. Языки и каталоги")
    a("")
    a("| язык | каталог | роль |")
    a("|---|---|---|")
    for l in spec["languages"]:
        a(f"| {l['label']} | `{l['dir']}` | {l['role']} |")
    a("")
    a("## 2. Каркас страницы (порядок сверху вниз)")
    a("")
    a("| # | блок | класс/маркер | обязателен | роль |")
    a("|---|---|---|---|---|")
    for i, b in enumerate(spec["frame"], 1):
        a(f"| {i} | {b['name']} | `{b['marker']}` | {b['required']} | {b['role']} |")
    a("")
    a("## 3. Типы страниц и обязательные блоки")
    a("")
    for t, d in spec["page_types"].items():
        a(f"### {t} — {d['title']}")
        a("")
        a(d["note"].strip())
        a("")
        a("Обязательные блоки: " + ", ".join(f"`{x}`" for x in d["require"]) + ".")
        if d.get("count") is not None:
            a("")
            a(f"Страниц этого типа: {d['count']}.")
        a("")
    a("## 4. Проверки, которые обязана проходить каждая страница")
    a("")
    a("| код | класс | проверка | норма | где мерить |")
    a("|---|---|---|---|---|")
    for c in spec["checks"]:
        a(f"| `{c['id']}` | {c['class']} | {c['what']} | {c['norm']} | `{c['tool']}` |")
    a("")
    a("## 5. Страницы")
    a("")
    a("| страница | язык | тип | герой | назначение |")
    a("|---|---|---|---|---|")
    for p in spec["pages"]:
        a(f"| `{p['path']}` | {p['lang']} | {p['type']} | {('`' + p['hero_class'] + '`') if p['hero_class'] else '—'} | {p['purpose']} |")
    a("")
    a(spec["footer"].strip())
    a("")
    return "\n".join(out)


if __name__ == "__main__":
    sys.exit(main())
