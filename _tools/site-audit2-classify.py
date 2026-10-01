#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""site-audit2-classify — сводит находки в таблицу классов (a)–(g).

Классы (SITE-STRUCTURE.md §4):
    a — пропорции и переносы (мобильный герой),
    b — контраст, c — отступы и пустые полосы, d — роли шрифтов,
    e — переполнения и прокрутка, f — структура, ссылки, навигация,
    g — язык и регистр.

Источники:
  * `--raw-1440` / `--raw-390` — JSON сплошного обхода `_tools/site-audit.js`
    (контраст, роли шрифтов, вылеты, герой);
  * `--lang` — TSV `_tools/site-langcheck.py` (класс g);
  * `--structure` — TSV `_tools/site-structure-check.py` (класс f);
  * `--hero` — JSON `_tools/hero-lines.js` (класс a).

Запуск:
    python _tools/site-audit2-classify.py --raw-1440 RAW.json --raw-390 RAW.json \
        --lang lang_check.tsv --structure structure_check.tsv --out site_audit2.tsv
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

BECAME = ""   # заполняется на этапе правок (второй прогон)


def lang_of(rel: str) -> str:
    return "ru" if rel.startswith("ru/") else "en" if rel.startswith("en/") else "az"


def from_raw(path: str, width: int) -> list[list[str]]:
    rows = []
    data = json.load(open(path, encoding="utf-8"))
    for r in data:
        rel = r.get("file") or r.get("url") or "?"
        lang = lang_of(rel)
        if r.get("error"):
            rows.append([rel, lang, "e", "замер не снялся", str(r["error"])[:70], ""])
            continue
        for c in r.get("contrast") or []:
            rows.append([rel, lang, "b",
                         f"контраст {c['ratio']:.1f}:1 < {c['need']}:1 — {c.get('sel','')} [{c.get('cls','')}]",
                         f"{c.get('color','')} {c.get('size','')}px/{c.get('weight','')} «{(c.get('text') or '')[:36]}»", ""])
        for f in r.get("fonts") or []:
            rows.append([rel, lang, "d",
                         f"роль «{f['exp']}», отрисовано «{f['got']}» ({f.get('fam','')}) — {f.get('sel','')} [{f.get('cls','')}]",
                         f"{f.get('size','')}px/{f.get('weight','')} «{(f.get('text') or '')[:36]}»", ""])
        for o in r.get("overflow") or []:
            rows.append([rel, lang, "e", f"вылет за вьюпорт — {o.get('sel','')}",
                         f"right {o.get('right')} при {r.get('cw')}", ""])
        if r.get("hScroll"):
            rows.append([rel, lang, "e", "горизонтальная прокрутка",
                         f"scrollW {r.get('scrollW')} > cw {r.get('cw')}", ""])
        for e in r.get("empty") or []:
            rows.append([rel, lang, "c", f"пустой блок — {e.get('sel','')} [{e.get('cls','')}]",
                         f"высота {e.get('h')}px", ""])
        for m in r.get("media") or []:
            rows.append([rel, lang, "f", f"изображение: {m.get('kind')}", (m.get("src") or "")[:60], ""])
        h = r.get("hero")
        if h and width <= 860:
            if h.get("badgeTop") is not None and abs(h["badgeTop"] - 32) > 1.5:
                rows.append([rel, lang, "c", "верх блока → метка не 32", f"{h['badgeTop']}px", ""])
            if h.get("lastBottom") is not None and abs(h["lastBottom"] - 26) > 1.5:
                rows.append([rel, lang, "c", "низ содержимого → низ блока не 25 (+1 рамка)",
                             f"{h['lastBottom']}px", ""])
    return rows


def from_hero(path: str) -> list[list[str]]:
    rows = []
    if not path or not os.path.isfile(path):
        return rows
    for d in json.load(open(path, encoding="utf-8")):
        if d.get("error"):
            continue
        rel = d.get("file", "?")
        lang = lang_of(rel)
        ph = d.get("photo")
        if ph and ph.get("colW"):
            ratio = ph["w"] / ph["colW"]
            if ratio < 0.70 or ratio > 0.90:
                rows.append([rel, lang, "a", "пропорция фото героя вне 70–85 % колонки",
                             f"{ph['w']:.0f}×{ph['h']:.0f} = {ratio:.2f} колонки", ""])
        for key, name in (("h1", "H1"), ("lead", "лид")):
            L = d.get(key)
            if not L:
                continue
            if L.get("n", 0) > 3:
                rows.append([rel, lang, "a", f"{name}: больше трёх строк", f"{L['n']}", ""])
            if L.get("skew") and L["skew"] > 1.31:
                ws = ", ".join(str(round(w)) for w in (L.get("ws") or []))
                rows.append([rel, lang, "a", f"{name}: строки разной длины (перекос)",
                             f"{L['skew']:.2f} при [{ws}]", ""])
    return rows


def from_tsv(path: str) -> list[list[str]]:
    rows = []
    if not path or not os.path.isfile(path):
        return rows
    with open(path, encoding="utf-8") as f:
        rd = csv.reader(f, delimiter="\t")
        header = next(rd, None)
        for r in rd:
            if len(r) >= 5:
                rows.append([r[0], r[1], r[2], r[3], r[4], r[5] if len(r) > 5 else ""])
            elif len(r) == 4:                     # формат site-структуры: page/lang/класс/причина
                rows.append([r[0], r[1], r[2], r[3], "", ""])
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw-1440")
    ap.add_argument("--raw-390")
    ap.add_argument("--lang")
    ap.add_argument("--structure")
    ap.add_argument("--hero")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    rows = []
    if args.raw_1440:
        rows += from_raw(args.raw_1440, 1440)
    if args.raw_390:
        rows += from_raw(args.raw_390, 390)
    rows += from_hero(args.hero)
    rows += from_tsv(args.lang)
    rows += from_tsv(args.structure)

    seen, uniq = set(), []
    for r in rows:
        k = tuple(r[:5])
        if k in seen:
            continue
        seen.add(k)
        uniq.append(r)

    with open(args.out, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["страница", "язык", "класс", "причина", "было", "стало"])
        w.writerows(uniq)

    import collections
    c = collections.Counter(r[2] for r in uniq)
    print(f"строк: {len(uniq)}; по классам: {dict(sorted(c.items()))}")
    for k in sorted(c):
        print(f"  класс {k}: {c[k]} — напр. " +
              (uniq[[r[2] for r in uniq].index(k)][3][:80] if c[k] else ""))
    print("таблица:", args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
