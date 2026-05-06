#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build.py — RAGIMOFF static site components renderer.

Renders header / mobile-nav / footer / hero-search / kitab-modal partials
into all HTML pages of the site (AZ root + ru/ + en/), per language and
with per-page parameters (active nav tab, lang switches).

USAGE
=====
  python build.py                  # render all pages
  python build.py --check          # dry-run, show which files would change
  python build.py --watch          # watch _partials/ + _i18n.json, rebuild on change
  python build.py haqqimda.html    # build a single file
  python build.py ru/blog.html     # works with subpath too
  python build.py --migrate        # one-shot: convert raw <header>/<footer>/...
                                   # blocks in legacy pages into @include markers,
                                   # then render. Safe to re-run.

DESIGN
======
Each managed component appears in source HTML as:

    <!-- @include NAME [param=value ...] -->
    <!-- BEGIN: NAME -->
    ... rendered HTML ...
    <!-- END: NAME -->

The `@include` line is the directive (never modified after being placed).
The BEGIN/END block is auto-generated and rewritten on every build.

When --migrate runs the first time, it locates legacy raw component blocks
(e.g. `<header class="site-header">…</header>`) and replaces each with the
marker pair. Subsequent builds touch ONLY content between BEGIN/END.

Pages WITHOUT markers are left untouched (so index.html, klinik-psixiatriya/
etc. remain safe).

Active-nav detection: the URL basename (e.g. "tehsil.html") is matched
against a small map; the corresponding nav link gets `class="nav-active"`.

Exit codes:
  0 — OK / no changes needed (with --check: nothing to change)
  1 — error
  2 — with --check, changes WOULD be made (use in CI)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Dict, Iterable, Tuple

ROOT = Path(__file__).parent.resolve()
PARTIALS_DIR = ROOT / "_partials"
I18N_FILE = ROOT / "_i18n.json"

# Files / directories never touched by build.
SKIP_DIRS = {"_partials", "klinik-psixiatriya", "backend", "data", "images", ".git", "node_modules"}
SKIP_FILES = {"index.html", "template.html"}  # index.html is the etalon — do NOT modify.
# Files skipped in ANY directory (not just root).
SKIP_FILES_ANYWHERE = {"template.html"}

LANG_DIRS = {"ru": "ru", "en": "en"}  # subdir -> lang code; root = "az"

COMPONENTS = ("header", "mobile-nav", "footer", "hero-search", "kitab-modal")

# ───────── active nav detection ─────────
# basename -> active key used in template (cls_KEY)
ACTIVE_MAP = {
    "index.html":          "home",
    "haqqimda.html":       "home",
    "tehsil.html":         "tehsil",
    "program-umumi.html":  "tehsil",
    "program-klinik.html": "tehsil",
    "program-praktikum.html": "tehsil",
    "qanunlar.html":       "tehsil",
    "xidmetler.html":      "xidmetler",
    "aile-terapiyasi.html":      "xidmetler",
    "aile-terapiyasi-usaq.html": "xidmetler",
    "depressiya.html":     "xidmetler",
    "panik-ataklar.html":  "xidmetler",
    "sosial-fobiya.html":  "xidmetler",
    "enurez.html":         "xidmetler",
    "b2b.html":            "b2b",
    "blog.html":           "blog",
}

# ───────── helpers ─────────

def load_i18n() -> dict:
    with open(I18N_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def load_partial(name: str) -> str:
    path = PARTIALS_DIR / f"{name}.html"
    return path.read_text(encoding="utf-8")

def detect_lang(html_path: Path) -> str:
    """ru/ -> ru, en/ -> en, root -> az."""
    rel = html_path.relative_to(ROOT)
    parts = rel.parts
    if len(parts) > 1 and parts[0] in LANG_DIRS:
        return LANG_DIRS[parts[0]]
    return "az"

def detect_active(html_path: Path) -> str:
    return ACTIVE_MAP.get(html_path.name, "")

def lang_switches(lang: str, html_path: Path) -> Tuple[str, str]:
    """Return (desktop_switches_html, mobile_switches_html) for the given page lang.
    Paths are relative to the file's directory."""
    # From AZ root: ru/index.html, en/index.html
    # From ru/ or en/:  ../index.html (AZ),  ../ru/index.html, ../en/index.html
    if lang == "az":
        az = "index.html"; ru = "ru/index.html"; en = "en/index.html"
    elif lang == "ru":
        az = "../index.html"; ru = "index.html"; en = "../en/index.html"
    else:  # en
        az = "../index.html"; ru = "../ru/index.html"; en = "index.html"

    def link(href, label, aria, active):
        cls = "lang-switch lang-active" if active else "lang-switch"
        return f'<a href="{href}" class="{cls}" aria-label="{aria}">{label}</a>'

    desk_az = link(az, "AZ", "Azərbaycan dili", lang == "az")
    desk_ru = link(ru, "RU", "Русский",        lang == "ru")
    desk_en = link(en, "EN", "English",        lang == "en")
    # Order: AZ RU EN (alphabetical-ish, mirrors prior site convention)
    desktop = desk_az + desk_ru + desk_en

    # Mobile lang switches: link to OTHER languages (not current).
    mob_links = []
    if lang != "az":
        mob_links.append(f'<a href="{az}" class="mobile-lang">Azərbaycan dili</a>')
    if lang != "ru":
        mob_links.append(f'<a href="{ru}" class="mobile-lang">Русский</a>')
    if lang != "en":
        mob_links.append(f'<a href="{en}" class="mobile-lang">English</a>')
    mobile = "\n  ".join(mob_links)
    return desktop, mobile

def home_href(lang: str, html_path: Path) -> str:
    # All inner pages link to "index.html" within their own lang directory.
    return "index.html"

def render_partial(name: str, lang: str, html_path: Path, i18n: dict, params: dict) -> str:
    tpl = load_partial(name)
    tr = i18n[lang]

    # Build context with all i18n keys, then overlay computed values.
    ctx: Dict[str, str] = dict(tr)

    desk_lang, mob_lang = lang_switches(lang, html_path)
    ctx["lang_switches"] = desk_lang
    ctx["mobile_lang_switches"] = mob_lang
    ctx["home_href"] = home_href(lang, html_path)

    # Active nav class injection (placed *inside* the <a> tag opening).
    active = params.get("active") or detect_active(html_path)
    for key in ("home", "tehsil", "xidmetler", "b2b", "blog"):
        ctx[f"cls_{key}"] = ' class="nav-active"' if active == key else ""

    # Allow per-include overrides (e.g. hero-search placeholder=…).
    for k, v in params.items():
        if k != "active":
            ctx[k] = v

    # Substitute {{var}} (simple, non-recursive).
    def repl(m):
        key = m.group(1).strip()
        return ctx.get(key, m.group(0))
    return re.sub(r"\{\{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\}\}", repl, tpl)


# ───────── marker handling ─────────

# Match: <!-- @include NAME [param=value ...] -->
INCLUDE_RE = re.compile(
    r"<!--\s*@include\s+(?P<name>[a-zA-Z0-9_-]+)(?P<params>[^-]*?)-->",
    re.IGNORECASE,
)

def parse_params(s: str) -> dict:
    """Parse `key="value"` or `key=value` pairs from include directive tail."""
    out = {}
    if not s:
        return out
    for m in re.finditer(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(?:"([^"]*)"|(\S+))', s):
        out[m.group(1)] = m.group(2) if m.group(2) is not None else m.group(3)
    return out

def render_block(component: str, rendered: str) -> str:
    return (f"<!-- BEGIN: {component} (auto-generated, do not edit by hand) -->\n"
            f"{rendered.rstrip()}\n"
            f"<!-- END: {component} -->")

def update_html(content: str, lang: str, html_path: Path, i18n: dict) -> str:
    """For every @include directive, ensure a fresh BEGIN/END block follows it."""
    # Pattern: directive optionally followed by an existing BEGIN/END block.
    # We'll walk includes in order and rebuild output.
    out = []
    pos = 0
    for m in INCLUDE_RE.finditer(content):
        name = m.group("name").lower()
        params = parse_params(m.group("params") or "")
        out.append(content[pos:m.end()])

        # Check if a BEGIN/END block immediately follows (allow whitespace).
        tail = content[m.end():]
        end_re = re.compile(
            r"\A(\s*)<!--\s*BEGIN:\s*" + re.escape(name) +
            r"[^>]*-->.*?<!--\s*END:\s*" + re.escape(name) + r"\s*-->",
            re.DOTALL | re.IGNORECASE,
        )
        em = end_re.match(tail)
        try:
            rendered = render_partial(name, lang, html_path, i18n, params)
        except FileNotFoundError:
            print(f"  !! unknown partial '{name}' in {html_path} — left as-is", file=sys.stderr)
            if em:
                out.append(tail[:em.end()])
                pos = m.end() + em.end()
            else:
                pos = m.end()
            continue
        block = render_block(name, rendered)
        if em:
            # Replace existing BEGIN/END block (preserve leading whitespace before BEGIN).
            ws = em.group(1)
            out.append(ws + block)
            pos = m.end() + em.end()
        else:
            # Insert new block right after the directive.
            out.append("\n" + block)
            pos = m.end()
    out.append(content[pos:])
    return "".join(out)


# ───────── one-shot legacy migration ─────────

# Each entry: component name -> regex matching a legacy raw block in source HTML.
# We use a minimal, anchored match so we don't grab unrelated content.
LEGACY_BLOCKS = [
    ("header",
     re.compile(r'(^[ \t]*)<header\s+class="site-header"[\s\S]*?</header>\s*\n',
                re.MULTILINE)),
    ("mobile-nav",
     re.compile(r'(^[ \t]*)<nav\s+[^>]*class="mobile-nav"[\s\S]*?</nav>\s*\n',
                re.MULTILINE)),
    ("footer",
     re.compile(r'(^[ \t]*)<footer\s+class="site-footer"[\s\S]*?</footer>\s*\n',
                re.MULTILINE)),
    ("kitab-modal",
     re.compile(r'(^[ \t]*)<!--\s*[─=\s]*Kitab[^>]*?-->\s*\n[\s\S]*?<div\s+id="kitab-modal"[\s\S]*?</div>\s*\n\s*<script[\s\S]*?KITAB_API[\s\S]*?</script>\s*\n',
                re.MULTILINE | re.IGNORECASE)),
]

def migrate(content: str) -> Tuple[str, list]:
    """Replace raw component blocks in legacy HTML with @include markers.
    Returns (new_content, [components_replaced])."""
    replaced = []
    for name, rx in LEGACY_BLOCKS:
        # Skip if an include directive for this component already exists.
        if re.search(r"<!--\s*@include\s+" + re.escape(name) + r"\b", content, re.IGNORECASE):
            continue
        m = rx.search(content)
        if not m:
            continue
        indent = m.group(1) or ""
        marker = f"{indent}<!-- @include {name} -->\n"
        content = content[:m.start()] + marker + content[m.end():]
        replaced.append(name)
    return content, replaced


# ───────── walk + main ─────────

def iter_html_files(only: Iterable[Path] | None = None) -> Iterable[Path]:
    if only:
        for p in only:
            yield p.resolve()
        return
    for dirpath, dirnames, filenames in os.walk(ROOT):
        # prune
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        for fn in filenames:
            if not fn.endswith(".html"):
                continue
            if fn in SKIP_FILES_ANYWHERE:
                continue
            if fn in SKIP_FILES and Path(dirpath).resolve() == ROOT:
                continue
            yield Path(dirpath) / fn

def process_file(path: Path, i18n: dict, do_migrate: bool, check: bool) -> Tuple[bool, list]:
    """Return (changed, notes)."""
    notes = []
    text = path.read_text(encoding="utf-8")
    original = text

    if do_migrate:
        text, mig = migrate(text)
        if mig:
            notes.append("migrated: " + ",".join(mig))

    lang = detect_lang(path)
    text = update_html(text, lang, path, i18n)

    changed = text != original
    if changed and not check:
        path.write_text(text, encoding="utf-8")
    return changed, notes

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*", help="Specific HTML file(s) to build (relative to site root).")
    ap.add_argument("--check", action="store_true", help="Dry-run; report which files would change.")
    ap.add_argument("--watch", action="store_true", help="Watch _partials/ + _i18n.json and rebuild.")
    ap.add_argument("--migrate", action="store_true",
                    help="One-shot conversion of legacy raw blocks into @include markers.")
    args = ap.parse_args()

    if not PARTIALS_DIR.is_dir():
        print(f"error: {PARTIALS_DIR} not found", file=sys.stderr)
        sys.exit(1)
    if not I18N_FILE.is_file():
        print(f"error: {I18N_FILE} not found", file=sys.stderr)
        sys.exit(1)

    i18n = load_i18n()

    only = None
    if args.files:
        only = []
        for f in args.files:
            p = (ROOT / f).resolve()
            if not p.exists():
                print(f"error: {p} not found", file=sys.stderr); sys.exit(1)
            only.append(p)

    def one_pass():
        n_changed = 0; n_total = 0; n_migrated = 0
        for p in iter_html_files(only):
            n_total += 1
            try:
                changed, notes = process_file(p, i18n, args.migrate, args.check)
            except Exception as e:
                print(f"  ERR {p}: {e}", file=sys.stderr)
                continue
            if any(n.startswith("migrated") for n in notes):
                n_migrated += 1
            if changed or notes:
                rel = p.relative_to(ROOT)
                tag = "[would change]" if args.check else "[updated]"
                extra = (" " + "; ".join(notes)) if notes else ""
                if changed:
                    print(f"  {tag} {rel}{extra}")
                elif notes:
                    print(f"  [no-op]    {rel}{extra}")
            if changed:
                n_changed += 1
        verb = "would change" if args.check else "updated"
        print(f"\nDone: {n_changed}/{n_total} files {verb}" +
              (f", {n_migrated} migrated" if n_migrated else ""))
        return n_changed

    if args.watch:
        watched = [I18N_FILE] + sorted(PARTIALS_DIR.glob("*.html"))
        last = {p: p.stat().st_mtime for p in watched}
        print("Initial build…")
        one_pass()
        print("Watching for changes (Ctrl+C to stop)…")
        try:
            while True:
                time.sleep(1)
                changed = False
                cur_files = [I18N_FILE] + sorted(PARTIALS_DIR.glob("*.html"))
                for p in cur_files:
                    m = p.stat().st_mtime
                    if last.get(p) != m:
                        changed = True; last[p] = m
                if changed:
                    print(f"\n[{time.strftime('%H:%M:%S')}] Change detected → rebuild")
                    one_pass()
        except KeyboardInterrupt:
            print("\nstopped.")
        return

    n = one_pass()
    if args.check and n > 0:
        sys.exit(2)

if __name__ == "__main__":
    main()
