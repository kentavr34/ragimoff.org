"""COMPREHENSIVE round-5 fix. Applies everything in one pass — only ONE rebuild after.

Fixes:
  1. ICD-11 code drift in 6B40-6B43 (cyclic content reassignment per WHO 2024):
       6B40 = PTSD (currently has Adjustment → move out)
       6B41 = cPTSD (currently has PTSD)
       6B42 = Prolonged Grief (currently has cPTSD)
       6B43 = Adjustment (currently has Prolonged Grief)
       (6B44 = RAD, 6B45 = Disinhibited social — already correct)
  2. Three English transliteration titles:
       HA01: PREMATURE EJAKULYASİYA  → TEZBİR EJAKULYASİYA
       6B45: DİSİNHİBE              → DEZİNHİBİSİYALI
       6B22: İY REFERANS             → İY REFERANSI (ORS) — add (ORS)
  3. Cross-references in body text updated for code swaps.

Run order:
  python _fix_all_v5.py
  python _inject_chapters_v2.py    (reflows fresh v2 into chapter HTMLs)
  python _rebuild_book_nav.py      (regenerates sidebar + TOC)
  python build_book.py             (final DOCX)
"""
from __future__ import annotations
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
V2 = ROOT / "_supplements" / "chapters-v2"


# ── 1. Cyclic file rename for 6B40-6B43 ─────────────────────────────────────
def swap_6b40_6b43_cycle():
    """Currently:
        6B40.html = Adjustment content
        6B41.html = PTSD content
        6B42.html = cPTSD content
        6B43.html = Prolonged Grief content
       Target (WHO 2024):
        6B40.html = PTSD content      ← rename from 6B41.html
        6B41.html = cPTSD content     ← rename from 6B42.html
        6B42.html = Prolonged Grief   ← rename from 6B43.html
        6B43.html = Adjustment        ← rename from 6B40.html
    """
    # Stage to temp, then swap
    temp_dir = V2 / "_tmp_swap"
    temp_dir.mkdir(exist_ok=True)

    mapping = {
        "6B40": "6B43",  # Adjustment moves from 6B40 → 6B43
        "6B41": "6B40",  # PTSD     moves from 6B41 → 6B40
        "6B42": "6B41",  # cPTSD    moves from 6B42 → 6B41
        "6B43": "6B42",  # P.Grief  moves from 6B43 → 6B42
    }

    # Move all four to temp first
    for old in ("6B40", "6B41", "6B42", "6B43"):
        src = V2 / f"{old}.html"
        dst = temp_dir / f"{old}.html"
        shutil.move(str(src), str(dst))

    # Rewrite codes inside and place at new location
    for old_code, new_code in mapping.items():
        tmp_file = temp_dir / f"{old_code}.html"
        text = tmp_file.read_text(encoding="utf-8")
        # Replace the OLD code with the NEW code in:
        #   <span class="icd">OLDCODE</span>
        #   id="oldcode-..." (slug uses lowercase)
        #   "OLDCODE", "OLDCODE.X" references inside text
        text = text.replace(old_code, new_code)
        text = text.replace(old_code.lower(), new_code.lower())
        # Save to final location
        (V2 / f"{new_code}.html").write_text(text, encoding="utf-8")
        tmp_file.unlink()

    temp_dir.rmdir()
    print(f"  Cyclic swap 6B40-6B43 applied.")


# ── 2. Title transliteration fixes ──────────────────────────────────────────
TITLE_REPL = [
    # HA01 — PREMATURE → TEZBİR
    ("PREMATURE EJAKULYASİYA (PE)",  "TEZBİR EJAKULYASİYA (PE)"),
    ("Premature Ejakulyasiya (PE)",  "Tezbir Ejakulyasiya (PE)"),
    ("Premature Ejakulyasiya",       "Tezbir Ejakulyasiya"),
    ("Premature ejakulyasiya",       "Tezbir ejakulyasiya"),
    ("premature ejakulyasiya",       "tezbir ejakulyasiya"),
    # Anchor slug
    ("premature-ejakulyasiya", "tezbir-ejakulyasiya"),
    # 6B45 — DİSİNHİBE → DEZİNHİBİSİYALI
    ("DİSİNHİBE SOSİAL CƏLBEDİCİLİK POZUNTUSU",
     "DEZİNHİBİSİYALI SOSİAL CƏLBEDİCİLİK POZUNTUSU"),
    ("Disinhibe Sosial Cəlbedicilik",
     "Dezinhibisiyalı Sosial Cəlbedicilik"),
    ("Disinhibe sosial cəlbedicilik",
     "Dezinhibisiyalı sosial cəlbedicilik"),
    ("disinhibe sosial cəlbedicilik",
     "dezinhibisiyalı sosial cəlbedicilik"),
    ("DİSİNHİBE ", "DEZİNHİBİSİYALI "),
    ("Disinhibe ", "Dezinhibisiyalı "),
    # 6B22 — add (ORS) suffix
    ("İY REFERANS POZUNTUSU",  "İY REFERANSI POZUNTUSU (ORS)"),
    ("İy Referans Pozuntusu",  "İy Referansı Pozuntusu (ORS)"),
    ("İy referans pozuntusu",  "İy referansı pozuntusu (ORS)"),
]

# Protected zones — preserve original
PROTECT_REF  = re.compile(r'<ol class="ref-list">[\s\S]*?</ol>', re.IGNORECASE)
PROTECT_ATTR = re.compile(r'title="[^"]*"', re.IGNORECASE)


def apply_protected(text: str):
    stash = []
    def s(m): stash.append(m.group(0)); return f'\x00P{len(stash)-1}\x00'
    work = PROTECT_REF.sub(s, text)
    work = PROTECT_ATTR.sub(s, work)
    for a, b in TITLE_REPL:
        work = work.replace(a, b)
    return re.sub(r'\x00P(\d+)\x00', lambda m: stash[int(m.group(1))], work)


def fix_terminology_all():
    targets = list(V2.glob("*.html")) + list((ROOT / "klinik-psixiatriya").glob("*.html"))
    total = 0
    for p in targets:
        orig = p.read_text(encoding="utf-8")
        new = apply_protected(orig)
        if new != orig:
            cnt = sum(orig.count(s) for s, _ in TITLE_REPL if s in orig)
            p.write_text(new, encoding="utf-8")
            total += cnt
    print(f"  Terminology fixes: {total} replacements.")


if __name__ == "__main__":
    print("Step 1: Cyclic file swap for ICD-11 codes 6B40-6B43 (WHO 2024 alignment)...")
    swap_6b40_6b43_cycle()
    print("\nStep 2: Title transliteration fixes...")
    fix_terminology_all()
    print("\nDone. Now run:")
    print("  python _inject_chapters_v2.py")
    print("  python _rebuild_book_nav.py")
    print("  python build_book.py")
