#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""site-audit-summary — сводка по TSV аудита: что и на скольких страницах.

    python _tools/site-audit-summary.py baseline/site_audit.tsv
    python _tools/site-audit-summary.py final/site_audit.tsv --type font-role
"""
from __future__ import annotations
import argparse
import collections
import io
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# ключ группировки: убираем всё, что меняется от страницы к странице
NUM = re.compile(r"\d+(?:\.\d+)?")
SELTAIL = re.compile(r"(#[A-Za-z0-9_-]+|>\s*[a-z]+(?:[.#][\w-]+)?)+$")


def key_of(desc: str) -> str:
    d = desc
    d = re.sub(r"\([^)]*\)", "(...)", d)
    d = NUM.sub("N", d)
    d = re.sub(r"«[^»]*»", "«…»", d)
    d = re.sub(r"#[A-Za-z0-9_-]+", "#…", d)
    return d[:110]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tsv")
    ap.add_argument("--type", default=None)
    ap.add_argument("--top", type=int, default=30)
    args = ap.parse_args()

    rows = [l.rstrip("\n").split("\t") for l in open(args.tsv, encoding="utf-8")][1:]
    rows = [r for r in rows if len(r) >= 5]
    if args.type:
        rows = [r for r in rows if r[1] == args.type]

    by_type = collections.Counter(r[1] for r in rows)
    print("rows: %d" % len(rows))
    print("by type: %s" % dict(by_type))
    print()

    groups = collections.defaultdict(lambda: {"pages": set(), "n": 0, "sample": None})
    for page, typ, desc, was, *rest in rows:
        k = (typ, key_of(desc))
        g = groups[k]
        g["pages"].add(page)
        g["n"] += 1
        if g["sample"] is None:
            g["sample"] = (page, desc, was)

    for (typ, k), g in sorted(groups.items(), key=lambda kv: -len(kv[1]["pages"]))[: args.top]:
        print("%-14s %3d стр. %4d раз  %s" % (typ, len(g["pages"]), g["n"], k))
        if g["sample"]:
            print("        напр.: %s | %s" % (g["sample"][0], g["sample"][2][:100]))


if __name__ == "__main__":
    main()
