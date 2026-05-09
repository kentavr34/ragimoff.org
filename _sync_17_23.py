#!/usr/bin/env python3
"""Sync supplements for chapters 17-23 into site HTML.
Idempotent via BOOK-SUPPLEMENT markers; inserts before </main>."""
import re
from pathlib import Path

ROOT = Path(__file__).parent
SITE = ROOT / "klinik-psixiatriya"
SUP = ROOT / "_supplements"

INSERTIONS = [
    {"chapter": "17-6D5-faktitioz.html",        "code": "6D5X", "f": SUP / "factitious.html"},
    {"chapter": "18-6D7-neyrokoqnitiv.html",    "code": "6D7X", "f": SUP / "dementia.html"},
    {"chapter": "19-6E2-perinatal.html",        "code": "6E2X", "f": SUP / "perinatal.html"},
    {"chapter": "20-6E4-psixosomatik.html",     "code": "6E4X", "f": SUP / "psychosomatic.html"},
    {"chapter": "21-6E6-ikincili.html",         "code": "6E6X", "f": SUP / "secondary.html"},
    {"chapter": "22-7AB-yuxu.html",             "code": "7ABX", "f": SUP / "sleep.html"},
    {"chapter": "23-HA-cinsi-saglamliq.html",   "code": "HA0X", "f": SUP / "sexual.html"},
]

for ins in INSERTIONS:
    path = SITE / ins["chapter"]
    if not path.exists():
        print(f"SKIP missing: {path}")
        continue
    text = path.read_text(encoding="utf-8")
    open_m = f"<!-- BOOK-SUPPLEMENT:{ins['code']} -->"
    close_m = f"<!-- /BOOK-SUPPLEMENT:{ins['code']} -->"
    text = re.sub(re.escape(open_m) + r".*?" + re.escape(close_m) + r"\s*", "", text, flags=re.DOTALL)
    m = re.search(r"</main\b", text, re.IGNORECASE)
    if not m:
        print(f"NO </main> in {path}")
        continue
    supp = ins["f"].read_text(encoding="utf-8")
    block = f"\n{open_m}\n{supp}\n{close_m}\n"
    text = text[:m.start()] + block + text[m.start():]
    path.write_text(text, encoding="utf-8")
    print(f"OK {ins['chapter']} <- {ins['f'].name}")
