#!/usr/bin/env python3
"""Replace 'Pillə-pillə' → 'Addım-Addım' globally in supplements + site chapters."""
import sys, io
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).parent
TARGETS = list((ROOT / "_supplements").glob("*.html")) + \
          list((ROOT / "klinik-psixiatriya").glob("*.html"))

PAIRS = [
    ("Pillə-pillə", "Addım-Addım"),
    ("pillə-pillə", "addım-addım"),
]

for path in TARGETS:
    text = path.read_text(encoding="utf-8")
    orig = text
    for a, b in PAIRS:
        text = text.replace(a, b)
    if text != orig:
        path.write_text(text, encoding="utf-8")
        n = sum(orig.count(a) for a, _ in PAIRS)
        print(f"  {path.relative_to(ROOT)}: {n} replacements")
print("done")
