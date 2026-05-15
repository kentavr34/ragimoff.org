"""Terminology sync — pulls APPROVED corrections from _corrections/PENDING.json
(written by the Cloudflare Worker, manually approved by you on GitHub).

WORKFLOW
========
1. Student clicks ✎ Düzəlt on the site → POST to Cloudflare Worker
   → Worker appends a {status: "pending", original, proposed, note} entry
     to _corrections/PENDING.json in this repo via the GitHub API.
2. You open _corrections/PENDING.json on GitHub web UI (pencil icon → Edit).
3. For each entry you accept, change "status": "pending" → "status": "approved".
4. Commit.
5. Next agent session — run `python _term_sync.py`:
   - Reads _corrections/PENDING.json
   - For every status="approved" entry: applies the replacement across
     _supplements/chapters-v2/*.html and klinik-psixiatriya/*.html
     (protecting <ol class="ref-list"> and <abbr title>).
   - Marks applied entries as status="applied" and timestamp.
   - Commits the rewritten PENDING.json back.
"""
from __future__ import annotations
import json
import os
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent
PENDING_FILE = ROOT / "_corrections" / "PENDING.json"

PROTECT_REF  = re.compile(r'<ol class="ref-list">[\s\S]*?</ol>', re.IGNORECASE)
PROTECT_ATTR = re.compile(r'title="[^"]*"', re.IGNORECASE)


def load_pending():
    if not PENDING_FILE.exists():
        return []
    text = PENDING_FILE.read_text(encoding="utf-8").strip()
    if not text:
        return []
    try:
        data = json.loads(text)
        return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []


def save_pending(entries):
    PENDING_FILE.parent.mkdir(parents=True, exist_ok=True)
    PENDING_FILE.write_text(json.dumps(entries, indent=2, ensure_ascii=False) + "\n",
                            encoding="utf-8")


def apply_replacement(orig: str, prop: str, files):
    """Replace orig → prop across given files, protecting ref-lists and
    <abbr title> attributes. Returns (occurrences_count, files_changed)."""
    if not orig or not prop or orig == prop:
        return 0, 0
    total_count = 0
    total_files = 0
    for p in files:
        try:
            d = p.read_text(encoding="utf-8")
        except Exception:
            continue
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
        work = re.sub(r'\x00P(\d+)\x00', lambda m: stash[int(m.group(1))], work)
        if work != d:
            p.write_text(work, encoding="utf-8")
            total_count += n
            total_files += 1
    return total_count, total_files


def main():
    entries = load_pending()
    if not entries:
        print("PENDING.json is empty — nothing to do.")
        return

    approved = [e for e in entries if e.get("status") == "approved"]
    print(f"Total entries: {len(entries)}")
    print(f"  pending: {sum(1 for e in entries if e.get('status') == 'pending')}")
    print(f"  approved (to apply): {len(approved)}")
    print(f"  applied: {sum(1 for e in entries if e.get('status') == 'applied')}")
    print(f"  rejected: {sum(1 for e in entries if e.get('status') == 'rejected')}")

    if not approved:
        print("\nNo approved corrections — nothing to apply.")
        return

    # Gather all book HTML files
    files = []
    for sub in ("_supplements/chapters-v2", "klinik-psixiatriya"):
        d = ROOT / sub
        if d.exists():
            for root, _, fs in os.walk(d):
                for f in fs:
                    if f.endswith(".html"):
                        files.append(Path(root) / f)

    grand_count = 0
    grand_files = set()
    for entry in approved:
        orig = entry.get("original", "").strip()
        prop = entry.get("proposed", "").strip()
        if not orig or not prop:
            continue
        cnt, n_files = apply_replacement(orig, prop, files)
        if cnt:
            print(f"  '{orig[:40]}' → '{prop[:40]}': {cnt} replacements in {n_files} files")
            grand_count += cnt
        entry["status"] = "applied"
        entry["applied_ts"] = datetime.utcnow().isoformat() + "Z"
        entry["applied_count"] = cnt

    save_pending(entries)
    print(f"\nTotal: {grand_count} replacements applied.")
    print(f"PENDING.json updated — {len(approved)} entries marked as 'applied'.")
    print("\nNext steps (manual):")
    print("  python _build_abbreviatur.py    # regen canonical-terms header")
    print("  python _rebuild_book_nav.py     # regen sidebar/TOC")
    print("  python build_book.py            # rebuild DOCX")
    print("  git add . && git commit && git push")


if __name__ == "__main__":
    main()
