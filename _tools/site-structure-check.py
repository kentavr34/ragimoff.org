#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""site-structure-check — проверка живой копии сайта по SITE-STRUCTURE.json.

Читает паспорт структуры (`SITE-STRUCTURE.json`), обходит перечисленные в нём
страницы и печатает расхождения строками

    страница | язык | класс | причина | было | стало

Классы (те же, что в сплошном аудите; см. SITE-STRUCTURE.md §4):
    a — пропорции и переносы, b — контраст, c — отступы, d — роли шрифтов,
    e — переполнения, f — структура, ссылки, навигация, g — язык и регистр.

Статические проверки (по умолчанию) читают HTML: состав блоков типа страницы,
один H1, <title>, lang, шапка/подвал/переключатель языков, пустые ссылки,
якоря, отсутствующие файлы, `<br>` в лиде героя, реестр регистра.

Отрисованные проверки (`--rendered`) идут через headless Chrome зондом
`_tools/hero-lines.js`: высота героя одна на всех страницах, фото 70–85 %
колонки, деление строк по словам (перекос ≤ 1,3), метка 32, нет горизонтальной
прокрутки. Требует запущенный сервер:

    python -m http.server 8765 --bind 127.0.0.1 -d .
    python _tools/site-structure-check.py --base http://127.0.0.1:8765
    python _tools/site-structure-check.py --base http://127.0.0.1:8765 --rendered --width 390
    python _tools/site-structure-check.py --base http://127.0.0.1:8765 --page index.html

Без `--base` страницы берутся прямо из дерева (--root, по умолчанию корень
репозитория) — удобно в CI до публикации.

Код возврата: 0 — расхождений нет; 1 — есть.
"""
from __future__ import annotations

import argparse
import csv
import html as H
import io
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

RE_TITLE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
RE_LANG = re.compile(r"""<html[^>]*\blang\s*=\s*["']([^"']+)["']""", re.I)
RE_SCRIPT = re.compile(r"<(script|style)\b[^>]*>[\s\S]*?</\1>", re.I)
RE_COMMENT = re.compile(r"<!--[\s\S]*?-->")
RE_HERO_LEAD = re.compile(r"""<p[^>]*class=["'][^"']*\b(hero-lead|ph-sub)\b[^"']*["'][^>]*>(.*?)</p>""", re.S | re.I)

ROWS: list[tuple[str, str, str, str, str, str]] = []


def add(page: str, lang: str, cls: str, why: str, was: str = "", became: str = "") -> None:
    ROWS.append((page, lang, cls, why, was, became))


def fetch(base: str | None, rel: str) -> tuple[int | None, str]:
    """Возвращает (код, html). При --base тянет по HTTP, иначе читает файл."""
    if base:
        url = base.rstrip("/") + "/" + rel
        try:
            with urllib.request.urlopen(url, timeout=20) as r:
                return r.status, r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            return e.code, ""
        except Exception as e:  # noqa: BLE001
            return None, f"__ERR__{e}"
    path = os.path.join(ROOT, rel.replace("/", os.sep))
    if not os.path.isfile(path):
        return None, ""
    with open(path, encoding="utf-8", errors="replace") as f:
        return 200, f.read()


def strip_tags(s: str) -> str:
    return re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def check_page(rec: dict, spec: dict, base: str | None) -> None:
    rel, lang, ptype = rec["path"], rec["lang"], rec["type"]
    tdef = spec["page_types"].get(ptype, {})
    require = tdef.get("require", [])
    strict = ptype not in ("template", "test", "redirect")

    code, s = fetch(base, rel)
    if code != 200:
        add(rel, lang, "f", "страница не отдаётся", f"код {code}", "нет файла/ответа")
        return

    # 1. язык версии
    m = RE_LANG.search(s)
    got = (m.group(1).lower() if m else "")
    if strict and not got.startswith(lang):
        add(rel, lang, "g", "атрибут lang не соответствует версии",
            got or "нет атрибута", lang)

    # 2. <title>
    t = RE_TITLE.search(s)
    if strict and (not t or not strip_tags(t.group(1))):
        add(rel, lang, "f", "нет <title>", "пусто", "заполнить")

    # 3. ровно один H1
    h1n = len(re.findall(r"<h1\b", s, re.I))
    if strict:
        if h1n == 0:
            add(rel, lang, "f", "на странице нет H1", "0", "1")
        elif h1n > 1:
            add(rel, lang, "f", "несколько H1 на странице", f"x{h1n}", "1")

    # 4. обязательные блоки типа
    for req in require:
        token = req.lstrip(".")
        if token.startswith("footer"):
            ok = bool(re.search(r"<footer\b", s, re.I))
        elif token.startswith("section"):
            ok = bool(re.search(r"<section\b", s, re.I))
        elif re.fullmatch(r"h[1-6]", token):
            ok = bool(re.search(r"<" + token + r"\b", s, re.I))
        else:
            ok = bool(re.search(r'class\s*=\s*["\'][^"\']*\b' + re.escape(token) + r'\b', s))
        if not ok:
            add(rel, lang, "f", f"нет обязательного блока {req} для типа «{ptype}»", "нет", "добавить")

    # 5. шапка / подвал / переключатель языков
    if strict:
        if not re.search(r"<header\b", s, re.I):
            add(rel, lang, "f", "нет шапки (<header>)", "нет", "добавить")
        if not re.search(r"<footer\b", s, re.I):
            add(rel, lang, "f", "нет подвала (<footer>)", "нет", "добавить")
        if not re.search(r"lang-drop|mobile-lang", s):
            add(rel, lang, "f", "нет переключателя языков", "нет", "добавить")

    # 6. класс героя соответствует типу страницы
    hero = rec.get("hero_class")
    if strict and not hero:
        add(rel, lang, "f", "нет блока героя", "нет", "добавить")
    elif ptype == "home" and hero not in ("page-hero",):
        add(rel, lang, "f", "на главной не .page-hero", str(hero), "page-hero")
    elif ptype in ("page", "blog-index", "blog-article") and hero not in ("page-hero-x", "pg-hero"):
        add(rel, lang, "f", "на внутренней странице не .page-hero-x", str(hero), "page-hero-x")

    # 7. лид героя: без <br>, непустой
    lm = RE_HERO_LEAD.search(s)
    if strict and lm:
        body = RE_COMMENT.sub(" ", lm.group(2))
        if re.search(r"<br\b", body, re.I):
            add(rel, lang, "a", "в лиде героя жёсткий перенос <br> — мешает балансировке", "<br>", "убрать")
        if not strip_tags(body):
            add(rel, lang, "f", "лид героя пуст", "пусто", "заполнить")

    # 8. пустые ссылки и якоря
    for tag in re.findall(r"<a\b[^>]*>", s, re.I):
        hm = re.search(r"""href\s*=\s*["']([^"']*)["']""", tag, re.I)
        if not hm:
            add(rel, lang, "f", "ссылка без href", tag[:60], "добавить href")
            continue
        href = hm.group(1).strip()
        if href in ("", "#"):
            add(rel, lang, "f", f"пустая ссылка href=\"{href}\"", tag[:60], "убрать/заполнить")
        elif href.startswith("#"):
            frag = href[1:]
            if frag and not re.search(r'id\s*=\s*["\']' + re.escape(frag) + r'["\']', s):
                add(rel, lang, "f", f"якорь #{frag} не найден на странице", href, "поправить")

    # 9. реестр регистра: термины должны встречаться в каноническом регистре
    reg = spec.get("case_register")
    if reg and os.path.isfile(os.path.join(ROOT, reg)):
        check_case(s, rel, lang, reg)


def check_case(s: str, rel: str, lang: str, reg_path: str) -> None:
    """Термин реестра, найденный в тексте в другом регистре, — нарушение."""
    text = strip_tags(RE_SCRIPT.sub(" ", s))
    low = text.lower()
    with open(os.path.join(ROOT, reg_path), encoding="utf-8") as f:
        rd = csv.reader(f, delimiter="\t")
        for row in rd:
            if not row or row[0].startswith("#") or len(row) < 5:
                continue
            ru, az, en = row[1], row[2], row[3]
            canon = row[4]
            if canon.startswith("строчными"):
                variants = [az] if lang == "az" else [ru] if lang == "ru" else [en]
            else:
                continue                      # остальные регистры проверяются книжным casecheck.py
            for v in variants:
                if not v or len(v) < 6:
                    continue
                i = low.find(v.lower())
                if i == -1:
                    continue
                found = text[i:i + len(v)]
                if found != v and found.lower() == v.lower():
                    add(rel, lang, "g", f"регистр термина реестра «{v}»", found, v)


# ───────────────────────── отрисованные проверки ─────────────────────────
def rendered(pages: list[str], width: int, base: str) -> None:
    node = ["node", os.path.join(HERE, "hero-lines.js"), str(width), "--json"] + pages
    env = dict(os.environ)
    env["HERO_PORT"] = base.rsplit(":", 1)[-1].rstrip("/") if base else "8765"
    try:
        out = subprocess.run(node, cwd=ROOT, capture_output=True, text=True,
                             encoding="utf-8", timeout=60 * max(1, len(pages)) + 120,
                             env=env).stdout
        data = json.loads(out)
    except Exception as e:  # noqa: BLE001
        add("(все)", "-", "e", "отрисованный замер не выполнился", str(e)[:80], "повторить")
        return
    heights = {}
    for d in data:
        if d.get("error"):
            add(d.get("file", "?"), "-", "e", "замер не снялся", d["error"][:60], "повторить")
            continue
        rel = d["file"]
        lang = "ru" if rel.startswith("ru/") else "en" if rel.startswith("en/") else "az"
        if d.get("hScroll"):
            add(rel, lang, "e", "горизонтальная прокрутка", f"doc {d.get('docW')} > {d.get('cw')}", "нет")
        ph = d.get("photo")
        if ph and ph.get("colW"):
            r = ph["w"] / ph["colW"]
            if r < 0.70 or r > 0.90:
                add(rel, lang, "a", "пропорция фото героя вне 70–85 % колонки",
                    f"{ph['w']:.0f}px = {r:.2f} колонки", "0,70–0,85")
        if d.get("badgeTop") is not None:
            want = 88 if width >= 861 else (48 if width > 560 else 32)
            if abs(d["badgeTop"] - want) > 1.5:
                add(rel, lang, "c", "верх блока → метка не по шкале",
                    f"{d['badgeTop']:.0f}px", f"{want}px")
        for key, name in (("h1", "H1"), ("lead", "лид")):
            L = d.get(key)
            if not L or not L.get("n"):
                continue
            if L.get("n", 0) > 3:
                add(rel, lang, "a", f"{name}: больше трёх строк", f"{L['n']}", "≤3")
            if L.get("skew") and L["skew"] > 1.31:
                add(rel, lang, "a", f"{name}: строки разной длины (перекос)",
                    f"{L['skew']} при [{', '.join(str(w) for w in L['ws'])}]", "≤1,3")
        if d.get("hero"):
            heights.setdefault(round(d["hero"]["h"]), []).append(rel)
    if len(heights) > 1:
        vals = sorted(heights)
        add("(все)", "-", "a", "высота блока героя разная на разных страницах",
            ", ".join(str(v) for v in vals[:6]), "одна высота")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=None, help="живой сайт, напр. http://127.0.0.1:8765")
    ap.add_argument("--page", action="append", default=[], help="проверить только эти страницы")
    ap.add_argument("--rendered", action="store_true", help="добавить замер в headless Chrome")
    ap.add_argument("--width", type=int, default=1440)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--json", default=None, help="куда положить расхождения (JSON)")
    ap.add_argument("--tsv", default=None, help="куда положить расхождения (TSV)")
    args = ap.parse_args()

    spec = json.load(open(os.path.join(ROOT, "SITE-STRUCTURE.json"), encoding="utf-8"))
    pages = spec["pages"]
    if args.page:
        want = set(args.page)
        pages = [p for p in pages if p["path"] in want]
    if args.limit:
        pages = pages[:args.limit]

    print(f"страниц в паспорте: {len(spec['pages'])}; проверяем: {len(pages)}; "
          f"источник: {args.base or 'дерево репозитория'}")
    for rec in pages:
        check_page(rec, spec, args.base)

    if args.rendered:
        rendered([p["path"] for p in pages], args.width, args.base or "http://127.0.0.1:8765")

    if args.tsv:
        with open(args.tsv, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f, delimiter="\t")
            w.writerow(["страница", "язык", "класс", "причина", "было", "стало"])
            w.writerows(ROWS)
    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump([dict(zip(("page", "lang", "class", "why", "was", "became"), r)) for r in ROWS],
                      f, ensure_ascii=False, indent=1)

    if not ROWS:
        print("OK — расхождений нет")
        return 0
    print(f"РАСХОЖДЕНИЯ: {len(ROWS)}")
    for r in ROWS:
        print(" | ".join(r))
    return 1


if __name__ == "__main__":
    sys.exit(main())
