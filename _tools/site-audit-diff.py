#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""site-audit-diff — сводит два прогона site-audit.js в одну таблицу
«страница | тип | описание | было | стало».

Строка базового прогона, которой нет в повторном, считается устранённой:
в колонку «стало» пишется, что проверка её больше не находит. Строка,
оставшаяся в повторном прогоне, помечается как неисправленная.

    python _tools/site-audit-diff.py baseline/site_audit.tsv final/site_audit.tsv --out site_audit.tsv
"""
from __future__ import annotations
import argparse
import collections
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def load(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i == 0:
                continue
            p = line.rstrip("\n").split("\t")
            if len(p) >= 4:
                rows.append({"page": p[0], "type": p[1], "desc": p[2], "was": p[3]})
    return rows


def key(r):
    return (r["page"], r["type"], r["desc"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("baseline")
    ap.add_argument("final")
    ap.add_argument("--out", default="site_audit.tsv")
    ap.add_argument("--disputed", default="site_audit_disputed.tsv")
    args = ap.parse_args()

    base = load(args.baseline)
    fin = load(args.final)
    fin_keys = collections.Counter(key(r) for r in fin)

    # спорные — те, что помечены вручную в реестре. Ключ — пара
    # «страница + описание»: одинаковые селекторы на разных страницах
    # не должны становиться спорными из-за одной записи.
    disputed = set()
    try:
        with open(args.disputed, encoding="utf-8") as f:
            for line in f:
                if line.strip() and not line.startswith("#"):
                    p = line.rstrip("\n").split("\t")
                    if len(p) >= 2:
                        disputed.add((p[0], p[1]))
    except OSError:
        pass

    out = ["page\ttype\tdescription\twas\tbecame"]
    fixed = remaining = 0
    for r in base:
        if (r["page"], r["desc"]) in disputed:
            became = "оставлено спорным (см. отчёт)"
            remaining += 1
        elif fin_keys.get(key(r)):
            became = "НЕ исправлено — повторный прогон находит то же"
            remaining += 1
        else:
            became = "устранено — повторный прогон строку не находит"
            fixed += 1
        out.append("\t".join(x.replace("\t", " ").replace("\n", " ") for x in
                             (r["page"], r["type"], r["desc"], r["was"], became)))

    # новые дефекты, которых не было в базовом прогоне (регрессии)
    base_keys = collections.Counter(key(r) for r in base)
    regress = 0
    for r in fin:
        if not base_keys.get(key(r)):
            # строка, известная как спорная (артефакт замера, тестовая
            # страница), не считается регрессией
            if (r["page"], r["desc"]) in disputed:
                out.append("\t".join(x.replace("\t", " ").replace("\n", " ") for x in
                                     (r["page"], r["type"], "[НОВОЕ] " + r["desc"], r["was"], "оставлено спорным (см. отчёт)")))
                regress += 1
                continue
            out.append("\t".join(x.replace("\t", " ").replace("\n", " ") for x in
                                 (r["page"], r["type"], "[НОВОЕ] " + r["desc"], r["was"], "появилось после правок")))
            regress += 1

    with open(args.out, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print("baseline rows: %d  fixed: %d  remaining: %d  new: %d" % (len(base), fixed, remaining, regress))
    print("-> " + args.out)


if __name__ == "__main__":
    main()
