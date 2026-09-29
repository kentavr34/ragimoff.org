# -*- coding: utf-8 -*-
"""Баланс тегов в титулах: невыкрытые/лишние </div></main></aside> ломают вложенность демо."""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def counts(s):
    body = s[s.find("<body"):]
    out = {}
    for tag in ("div", "main", "aside", "nav", "section", "ol", "ul", "li", "footer", "span", "a"):
        op = len(re.findall(r"<%s\b" % tag, body))
        cl = len(re.findall(r"</%s>" % tag, body))
        if op != cl:
            out[tag] = (op, cl)
    return out


n = total = 0
for dp, dn, fn in os.walk(ROOT):
    dn[:] = [d for d in dn if not d.startswith(".") and not d.endswith(".bak_20260929")]
    for f in sorted(fn):
        if not f.endswith(".html"):
            continue
        fp = os.path.join(dp, f)
        s = open(fp, encoding="utf-8", errors="replace").read()
        if 'class="bk bk-cover"' not in s[:6000]:
            continue
        bad = counts(s)
        if bad:
            print("%-58s %s" % (os.path.relpath(fp, ROOT).replace("\\", "/"), bad))
            n += 1
        total += 1
print("титулов проверено: %d | с несбалансированными тегами: %d" % (total, n))
