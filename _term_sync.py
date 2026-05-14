"""Terminology sync — pulls APPROVED corrections from the Google Sheet
(filled via 'Düzəlt' widget on the site) and applies them everywhere:
  - _supplements/chapters-v2/*.html
  - klinik-psixiatriya/*.html (book pages incl. abbreviatur)
  - _build_abbreviatur.py CANONICAL_TERMS list (so the header stays in sync)
  - TYPOGRAPHY.md §0b table

WORKFLOW
========
1. User submits via 'Düzəlt' button → row appears in Google Sheet
   (columns: Timestamp · Original · Proposed · Note · Status).
2. User marks Status = 'ok' (or 'approved') manually in the sheet.
3. GAS script exposes GET ?action=approved → returns JSON list of rows
   where Status starts with 'ok'.
4. Run `python _term_sync.py` at session start.
5. Script fetches approved rows, applies replacements via
   _fix_terminology4.py-style protected substitution, rebuilds
   abbreviatur and book.

Local fallback: if no internet, read from `_terms_approved.json`
(same format as the GAS response).
"""
from __future__ import annotations
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent

# Same endpoint as duzelis.js (configured in duzelis-gas.txt)
ENDPOINT = "https://script.google.com/macros/s/AKfycbzS9vijozxUyEB3pWJcQY09y4MzmSmk_wvE-3w9ThYTLnqG79yWwhQggfRNW3roLv2m2A/exec"
LOCAL_FALLBACK = ROOT / "_terms_approved.json"

PROTECT_REF  = re.compile(r'<ol class="ref-list">[\s\S]*?</ol>', re.IGNORECASE)
PROTECT_ATTR = re.compile(r'title="[^"]*"', re.IGNORECASE)


def fetch_approved() -> list[dict]:
    """Fetch approved corrections from GAS. Falls back to local JSON."""
    # Try local first (offline-friendly)
    if LOCAL_FALLBACK.exists():
        print(f"Using local fallback: {LOCAL_FALLBACK}")
        return json.loads(LOCAL_FALLBACK.read_text(encoding="utf-8"))
    try:
        url = f"{ENDPOINT}?action=approved"
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception as e:
        print(f"Could not fetch from GAS ({e}); no local fallback either.")
        return []


def apply_replacement(orig: str, prop: str, files: list[Path]) -> tuple[int, int]:
    """Replace orig → prop across files, protecting ref-lists and abbr titles."""
    if not orig or not prop or orig == prop:
        return (0, 0)
    total_files = 0
    total_count = 0
    for p in files:
        try:
            d = p.read_text(encoding="utf-8")
        except Exception:
            continue
        # Skip protected zones
        stash = []
        def stash_fn(m):
            stash.append(m.group(0))
            return f"\x00P{len(stash)-1}\x00"
        work = PROTECT_REF.sub(stash_fn, d)
        work = PROTECT_ATTR.sub(stash_fn, work)
        if orig not in work:
            continue
        n = work.count(orig)
        work = work.replace(orig, prop)
        # Also try common case variants
        if orig.upper() != orig and orig.upper() in work:
            work = work.replace(orig.upper(), prop.upper())
            n += d.count(orig.upper())
        work = re.sub(r'\x00P(\d+)\x00', lambda m: stash[int(m.group(1))], work)
        if work != d:
            p.write_text(work, encoding="utf-8")
            total_files += 1
            total_count += n
    return (total_count, total_files)


def main():
    approved = fetch_approved()
    if not approved:
        print("No approved corrections to apply.")
        return
    print(f"Got {len(approved)} approved corrections.")

    # Gather target files (book content + supplements + abbreviatur)
    targets = []
    for sub in ("_supplements/chapters-v2", "klinik-psixiatriya"):
        d = ROOT / sub
        if d.exists():
            for root, _, files in __import__("os").walk(d):
                for f in files:
                    if f.endswith(".html"):
                        targets.append(Path(root) / f)

    grand_total = 0
    for row in approved:
        orig = (row.get("original") or "").strip()
        prop = (row.get("proposed") or "").strip()
        if not orig or not prop:
            continue
        cnt, files = apply_replacement(orig, prop, targets)
        if cnt:
            print(f"  '{orig}' → '{prop}': {cnt} replacements in {files} files")
            grand_total += cnt

    print(f"\nTotal: {grand_total} replacements.")
    print("\nNow run:")
    print("  python _build_abbreviatur.py    (regen canonical-terms header)")
    print("  python _rebuild_book_nav.py     (regen sidebar/TOC)")
    print("  python build_book.py            (rebuild DOCX)")


if __name__ == "__main__":
    main()
