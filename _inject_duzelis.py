#!/usr/bin/env python3
"""Inject duzelis.css + duzelis.js into every klinik-psixiatriya HTML page.
Idempotent — skips files that already have the marker."""
from pathlib import Path
import re

ROOT = Path(__file__).parent
SITE = ROOT / "klinik-psixiatriya"

MARK = "<!-- DUZELIS-WIDGET -->"
HEAD_LINK = '<link rel="stylesheet" href="duzelis.css">'
BODY_SCRIPT = '<script src="duzelis.js" defer></script>'

for p in sorted(SITE.glob("*.html")):
    text = p.read_text(encoding="utf-8")
    if MARK in text:
        continue
    new = text
    # Inject CSS into <head>
    if "</head>" in new:
        new = new.replace("</head>", f"  {MARK}\n  {HEAD_LINK}\n  {BODY_SCRIPT}\n</head>", 1)
        p.write_text(new, encoding="utf-8")
        print(f"OK {p.name}")
    else:
        print(f"SKIP no </head>: {p.name}")
