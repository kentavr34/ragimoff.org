"""Fix remaining English/Latin disorder names + terminology violations.

Targets:
  - chapters-v2 source fragments AND injected chapter HTMLs + nav sidebar + TOC.
  - Disorder titles: pure Azerbaijani forms.
  - Stragglers: "klinik mənzərə" (lowercase) -> "klinik təzahürlər",
              "çek-list" -> "meyarlar",
              "baseline" -> "ilkin göstəricilər",
              "ANOREXIA NERVOSA" -> "ANOREKSİYA NERVOZA",
              "BULİMİA NERVOSA" -> "BULİMİYA NERVOZA", etc.
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).parent

# Title-level replacements (full strings)
TITLE_REPLACEMENTS = [
    # 6B80
    ("ANOREXIA NERVOSA", "ANOREKSİYA NERVOZA"),
    ("Anorexia Nervosa", "Anoreksiya Nervoza"),
    ("Anorexia nervosa", "Anoreksiya nervoza"),
    ("anorexia nervosa", "anoreksiya nervoza"),
    # 6B81
    ("BULİMİA NERVOSA", "BULİMİYA NERVOZA"),
    ("Bulimia Nervosa", "Bulimiya Nervoza"),
    ("Bulimia nervosa", "Bulimiya nervoza"),
    ("Bulimia",          "Bulimiya"),
    # 6B82
    ("BİNGE-EATİNG POZUNTUSU (BED)", "KEÇİRTMƏ İLƏ YEMƏ POZUNTUSU (BED)"),
    ("Binge-Eating", "Keçirtmə ilə yemə"),
    ("binge-eating", "keçirtmə ilə yemə"),
    # 6B85
    ("AVOIDANT/RESTRİKTİV QİDA QƏBULU POZUNTUSU (ARFID)",
     "QAÇINMA/MƏHDUDLAŞDIRICI QİDA QƏBULU POZUNTUSU (ARFID)"),
    # 6B23
    ("HİPOXONDRİA", "HİPOXONDRİYA"),
    ("Hipoxondria", "Hipoxondriya"),
    ("hipoxondria", "hipoxondriya"),
    # 6B24 — drop parenthetical English
    ("TOPLAMA POZUNTUSU (HOARDING DISORDER)", "TOPLAMA POZUNTUSU"),
    # 6C90 — drop parenthetical English
    ("DAVRANIŞ POZUNTUSU (CONDUCT DISORDER)", "DAVRANIŞ POZUNTUSU"),
    # 6C20 — replace with Azerbaijani term
    ("SOMATİK SİMPTOM POZUNTUSU (BODILY DISTRESS)",
     "BƏDƏNSƏL DİSSTRES POZUNTUSU"),
    # 6D81 — drop parenthetical English
    ("DAMAR DEMENSİYASI (VASCULAR DEMENTIA)", "DAMAR DEMENSİYASI"),
]

# Terminology stragglers
TERMINOLOGY = [
    # "klinik mənzərə" lowercase forms still in some pages
    ("klinik mənzərə", "klinik təzahürlər"),
    ("Klinik mənzərə", "Klinik təzahürlər"),
    # English/programming jargon
    ("çek-list", "meyarlar"),
    ("ÇEK-LİST", "MEYARLAR"),
    # baseline -> ilkin göstəricilər (word boundary)
    (r"\bbaseline\b", "ilkin göstəricilər"),
]


def fix_file(path: Path) -> tuple[Path, int]:
    text = path.read_text(encoding="utf-8")
    n = 0
    new = text
    for src, dst in TITLE_REPLACEMENTS:
        before = new
        new = new.replace(src, dst)
        n += (before.count(src) if before != new else 0)
    for pat, dst in TERMINOLOGY:
        if pat.startswith(r"\b"):
            new, k = re.subn(pat, dst, new)
            n += k
        else:
            before = new
            new = new.replace(pat, dst)
            n += before.count(pat) if before != new else 0
    if new != text:
        path.write_text(new, encoding="utf-8")
    return path, n


def walk_targets():
    # chapters-v2 fragments
    for p in (ROOT / "_supplements" / "chapters-v2").glob("*.html"):
        yield p
    # injected chapter HTMLs + book pages
    for p in (ROOT / "klinik-psixiatriya").glob("*.html"):
        yield p


def main():
    total = 0
    files = 0
    for p in walk_targets():
        _, n = fix_file(p)
        if n:
            print(f"  {p.relative_to(ROOT)}: {n} replacements")
            total += n
            files += 1
    print(f"\nTotal: {total} replacements across {files} files")


if __name__ == "__main__":
    main()
